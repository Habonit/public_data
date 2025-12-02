# Research: App v1.1.1 Upgrade

**Feature Branch**: `003-app-v111-upgrade`
**Research Date**: 2025-12-02
**Status**: Completed

---

## 1. Anthropic Tool Calling API

### 결정 사항

**Decision**: Anthropic Python SDK의 Tool Use 기능을 사용하여 15개 분석 도구 구현

### 근거

1. **공식 지원**: Anthropic SDK 0.39.0+에서 tool use가 정식 지원됨
2. **스키마 기반**: JSON Schema 형식으로 도구 입력을 정의하여 타입 안정성 확보
3. **반복 제어**: `stop_reason`을 통해 도구 호출 필요 여부 감지 가능
4. **오류 처리**: `is_error: true`로 도구 실행 실패를 Claude에게 전달 가능

### 검토한 대안

1. **LangChain Tool Calling**: 추상화 레이어 추가로 복잡성 증가, 직접 SDK 사용이 더 단순
2. **사용자 정의 프롬프트 파싱**: 불안정하고 유지보수 어려움
3. **Function Calling (OpenAI 스타일)**: Anthropic SDK에서는 tool use가 표준

### 핵심 구현 패턴

```python
# 도구 정의 형식
tools = [
    {
        "name": "get_column_statistics",
        "description": "특정 컬럼의 통계 정보 (평균, 중앙값, 표준편차 등)",
        "input_schema": {
            "type": "object",
            "properties": {
                "column": {
                    "type": "string",
                    "description": "분석할 컬럼명"
                }
            },
            "required": ["column"]
        }
    }
]

# API 호출
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    tools=tools,
    messages=messages
)

# 도구 호출 감지
if response.stop_reason == "tool_use":
    tool_uses = [b for b in response.content if b.type == "tool_use"]
    # 도구 실행...
```

### 반복 제어 패턴 (Max 3 Iterations)

```python
MAX_ITERATIONS = 3

for iteration in range(MAX_ITERATIONS):
    response = client.messages.create(...)

    if response.stop_reason != "tool_use":
        break  # 완료

    # 도구 실행 및 결과 추가
    tool_results = [...]
    messages.append({"role": "assistant", "content": response.content})
    messages.append({"role": "user", "content": tool_results})

# 반복 초과 시 안내 메시지
if iteration >= MAX_ITERATIONS - 1:
    return "현재 앱이 답변할 수 없는 질문입니다."
```

---

## 2. Streamlit 스트리밍 응답

### 결정 사항

**Decision**: `client.messages.stream()` + `st.write_stream()` 조합 사용

### 근거

1. **네이티브 지원**: Streamlit 1.28.0+에서 `st.write_stream()` 지원
2. **호환성**: Anthropic SDK의 `stream.text_stream`과 직접 호환
3. **Tool Use 호환**: 스트리밍 후 `get_final_message()`로 tool_use 블록 확인 가능

### 검토한 대안

1. **Fine-grained Tool Streaming (Beta)**: 아직 베타, 불완전 JSON 처리 복잡
2. **Polling 방식**: 비효율적이고 UX 저하
3. **WebSocket**: Streamlit 아키텍처와 맞지 않음

### 구현 패턴

```python
# 스트리밍 응답
with st.chat_message("assistant"):
    with client.messages.stream(
        model=model,
        max_tokens=max_tokens,
        tools=tools,
        messages=messages
    ) as stream:
        # 텍스트 스트리밍
        response_text = st.write_stream(stream.text_stream)

        # 최종 메시지 (tool_use 확인용)
        final_message = stream.get_final_message()

        if final_message.stop_reason == "tool_use":
            # 도구 실행 로직...
```

### 주의사항

- Tool Calling 중에는 스트리밍이 도구 실행 전까지만 동작
- 도구 실행 결과 후 후속 응답도 스트리밍 가능

---

## 3. 지도 캐싱 전략

### 결정 사항

**Decision**: `st.session_state`에 Folium 지도 객체 캐싱 + `returned_objects=[]` 설정

### 근거

1. **성능**: 지도 재생성 비용 절감 (마커 5000개 기준 약 2-3초 절약)
2. **Streamlit 친화적**: session_state는 Streamlit의 권장 상태 관리 방식
3. **리렌더링 방지**: `returned_objects=[]`로 줌/패닝 시 리렌더링 방지

### 검토한 대안

1. **`@st.cache_data`**: Folium Map 객체는 직렬화 불가, 사용 불가
2. **`@st.cache_resource`**: 가능하나 키 관리 복잡
3. **HTML 캐싱**: 지도를 HTML로 변환 후 저장, 추가 복잡성

### 구현 패턴

```python
# 캐시 키 생성
cache_key = f"map_{dataset_name}_{len(df)}_{hash_columns}"

# 캐싱 로직
if cache_key not in st.session_state:
    st.session_state[cache_key] = create_folium_map(
        df, lat_col, lng_col, popup_cols, color, name
    )

# 지도 렌더링 (인터랙션 분리)
st_folium(
    st.session_state[cache_key],
    width=700,
    height=500,
    returned_objects=[]  # 리렌더링 방지
)
```

---

## 4. 데이터셋별 대화 컨텍스트 분리

### 결정 사항

**Decision**: `st.session_state.chat_history`를 딕셔너리 구조로 변경

### 근거

1. **직관적**: 데이터셋명을 키로 사용하여 명확한 분리
2. **효율적**: 탭 전환 시 해당 데이터셋의 이력만 로드
3. **호환성**: 기존 메시지 형식 유지 가능

### 검토한 대안

1. **별도 session key**: `chat_history_cctv`, `chat_history_lights` 등 - 관리 복잡
2. **메시지에 dataset 태그 추가**: 필터링 로직 필요, 비효율적
3. **로컬 스토리지**: Streamlit에서 직접 접근 어려움

### 구현 패턴

```python
# 초기화 (기존 구조에서 변경)
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = {}

# 데이터셋별 이력 접근
def get_chat_history(dataset_name: str) -> list:
    if dataset_name not in st.session_state.chat_history:
        st.session_state.chat_history[dataset_name] = []
    return st.session_state.chat_history[dataset_name]

# 데이터셋별 이력 삭제
def clear_chat_history(dataset_name: str):
    st.session_state.chat_history[dataset_name] = []
```

---

## 5. 최신 Claude 모델 목록

### 결정 사항

**Decision**: Claude 4.5 시리즈 3개 모델 지원

### 근거

1. **최신성**: 2025년 기준 최신 모델 제공
2. **다양성**: 성능/비용 균형에 따른 선택 옵션
3. **호환성**: Tool Use 기능 완전 지원

### 모델 목록

| 모델명 | Model ID | 용도 |
|:-------|:---------|:-----|
| Claude Sonnet 4.5 | `claude-sonnet-4-5-20250929` | 빠른 응답, 비용 효율적 (권장) |
| Claude Opus 4.5 | `claude-opus-4-5-20251101` | 복잡한 분석에 적합 |
| Claude Haiku 4.5 | `claude-haiku-4-5-20250901` | 간단한 질문에 최적 |

### 참고 문서

- https://platform.claude.com/docs/en/get-started#python

---

## 6. 버그 수정 패턴

### 6.1 ZeroDivisionError 방지

**위치**: `app.py:645`

```python
# AS-IS
missing_pct = df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100

# TO-BE
total_cells = len(df) * len(df.columns)
missing_pct = (df.isnull().sum().sum() / total_cells * 100) if total_cells > 0 else 0
```

### 6.2 빈 DataFrame 지도 렌더링

**위치**: `visualizer.py:321-326`

```python
# TO-BE: early return 추가
df_clean = df.dropna(subset=[lat_col, lng_col]).copy()
if df_clean.empty:
    # 기본 대구 중심 좌표로 빈 지도 반환
    return folium.Map(location=[35.8714, 128.6014], zoom_start=12)
```

### 6.3 NaN 값 포맷팅

**위치**: `chatbot.py:51`

```python
# TO-BE: NaN 체크 추가
if pd.api.types.is_numeric_dtype(df[col]):
    col_min = df[col].min()
    col_max = df[col].max()
    col_mean = df[col].mean()
    if pd.isna(col_min) or pd.isna(col_max) or pd.isna(col_mean):
        stats = "모든 값이 결측치입니다"
    else:
        stats = f"min={col_min:.2f}, max={col_max:.2f}, mean={col_mean:.2f}"
```

### 6.4 성능 개선 (iterrows -> itertuples)

**위치**: `visualizer.py:357,475`

```python
# AS-IS
for idx, row in df_clean.iterrows():
    lat = row[lat_col]

# TO-BE
for row in df_clean.itertuples(index=False):
    lat = getattr(row, lat_col)
```

---

## 참고 자료

- [Anthropic Tool Use Documentation](https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use)
- [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python)
- [Streamlit write_stream](https://docs.streamlit.io/library/api-reference/write-magic/st.write_stream)
- [streamlit-folium returned_objects](https://github.com/randyzwitch/streamlit-folium)
