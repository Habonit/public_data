# Quickstart: App v1.1.1 Upgrade

**Feature Branch**: `003-app-v111-upgrade`
**Created**: 2025-12-02

---

## 빠른 시작 가이드

### 1. 의존성 확인

```bash
# requirements.txt에 추가된 의존성 확인
pip install anthropic>=0.39.0
```

### 2. 기존 앱 실행

```bash
streamlit run app.py
```

### 3. 변경 파일 목록

| 파일 | 변경 유형 | 설명 |
|:-----|:---------|:-----|
| `app.py` | 수정 | 모델 목록 업데이트, 대화 컨텍스트 분리, 버그 수정 |
| `utils/chatbot.py` | 수정 | Tool Calling 구현, 스트리밍 응답 |
| `utils/visualizer.py` | 수정 | 지도 캐싱, 빈 DataFrame 처리, itertuples |
| `utils/tools.py` | 신규 | 15개 분석 도구 구현 |

---

## 핵심 구현 예시

### Tool Calling 기본 패턴

```python
from anthropic import Anthropic
from utils.tools import TOOLS, execute_tool

client = Anthropic(api_key=api_key)

MAX_ITERATIONS = 3

for iteration in range(MAX_ITERATIONS):
    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=4096,
        tools=TOOLS,
        messages=messages
    )

    # 도구 호출 완료 확인
    if response.stop_reason != "tool_use":
        break

    # 도구 실행
    tool_uses = [b for b in response.content if b.type == "tool_use"]
    tool_results = []

    for tool_use in tool_uses:
        result = execute_tool(tool_use.name, tool_use.input, df)
        tool_results.append({
            "type": "tool_result",
            "tool_use_id": tool_use.id,
            "content": str(result)
        })

    # 대화 이력 업데이트
    messages.append({"role": "assistant", "content": response.content})
    messages.append({"role": "user", "content": tool_results})
```

### 스트리밍 응답

```python
with st.chat_message("assistant"):
    with client.messages.stream(
        model=model,
        max_tokens=max_tokens,
        tools=TOOLS,
        messages=messages
    ) as stream:
        response_text = st.write_stream(stream.text_stream)
        final_message = stream.get_final_message()

        if final_message.stop_reason == "tool_use":
            # 도구 실행...
```

### 데이터셋별 대화 컨텍스트

```python
# 초기화
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = {}

# 데이터셋별 이력 접근
def get_chat_history(dataset_name: str) -> list:
    if dataset_name not in st.session_state.chat_history:
        st.session_state.chat_history[dataset_name] = []
    return st.session_state.chat_history[dataset_name]

# 사용
messages = get_chat_history(selected_dataset_key)
```

### 지도 캐싱

```python
cache_key = f"map_{dataset_name}_{len(df)}"

if cache_key not in st.session_state:
    st.session_state[cache_key] = create_folium_map(
        df, lat_col, lng_col, popup_cols, color, name
    )

st_folium(
    st.session_state[cache_key],
    width=700,
    height=500,
    returned_objects=[]  # 리렌더링 방지
)
```

---

## 테스트 체크리스트

- [ ] API Key 입력 후 모델 선택 드롭다운에서 Claude 4.5 시리즈 확인
- [ ] 데이터 업로드 후 "평균값을 알려줘" 질문으로 Tool Calling 동작 확인
- [ ] 탭 전환 시 각 데이터셋의 대화 이력이 분리되는지 확인
- [ ] 빈 CSV 파일 업로드 시 오류 없이 처리되는지 확인
- [ ] 지도 줌 인/아웃 시 페이지 리렌더링 없음 확인
- [ ] 응답 텍스트가 실시간으로 스트리밍되는지 확인

---

## 참고 자료

- [Anthropic Tool Use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/implement-tool-use)
- [Streamlit write_stream](https://docs.streamlit.io/library/api-reference/write-magic/st.write_stream)
- [streamlit-folium](https://github.com/randyzwitch/streamlit-folium)
