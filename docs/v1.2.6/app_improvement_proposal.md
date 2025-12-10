# 대구 공공데이터 시각화 앱 개선 제안서 (v1.2.5 → v1.2.6)

**문서 버전**: v1.2.6
**작성일**: 2025-12-10
**참고 문서**: `docs/v1.2.6/note.md`

---

## 1. 개요

본 문서는 대구 공공데이터 시각화 앱 v1.2.5의 현재 상태(AS-IS)와 v1.2.6에서 목표하는 개선 상태(TO-BE)를 비교 분석한다.

v1.2.6의 핵심 목표:
1. **🔴 버그 수정**: Tool Calling 시 `config` 전달 방식 수정 (22개 도구 영향)
2. **🔧 UX 개선**: 마크다운 다운로드 버튼 → 응답별 복사 버튼으로 변경

---

## 2. 기능별 AS-IS / TO-BE 비교

### 2.1 Tool Calling config 전달 방식 (🔴 Critical Bug)

| 구분 | AS-IS (v1.2.5) | TO-BE (v1.2.6) |
|:-----|:---------------|:---------------|
| **config 전달** | input dict에 병합 `{**tool_input, "config": config}` | 별도 인자로 전달 `invoke(tool_input, config=config)` |
| **도구 실행** | ❌ 22개 도구 모두 실패 | ✅ 모든 도구 정상 작동 |
| **오류 메시지** | "현재 활성화된 데이터셋이 없습니다" | 정상 결과 반환 |

#### 2.1.1 문제 발생 흐름

```
AS-IS (v1.2.5) - 문제 발생 흐름:
┌─────────────────────────────────────────────────────────────────┐
│  1. app.py: stream_chat_response_with_tools(df=df) 호출         │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  2. chatbot.py: execute_tool(tool_name, tool_input, df) 호출    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  3. tools.py:1178                                               │
│     tool_func.invoke({**tool_input, "config": config})          │
│     └─ ❌ config가 input dict에 포함되지만                       │
│        @tool 데코레이터가 이를 RunnableConfig로 인식하지 못함    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  4. get_sample_rows 등: config=None (기본값 사용됨)              │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│  5. get_dataframe_from_config(None) → KeyError 발생             │
│     "현재 활성화된 데이터셋이 없습니다"                           │
└─────────────────────────────────────────────────────────────────┘
```

#### 2.1.2 영향받는 도구 목록 (22개 전체)

| 줄 | 도구명 | config 파라미터 | 카테고리 |
|:---|:-------|:---------------|:---------|
| 46 | `get_dataframe_info` | 필수 | 데이터 정보 |
| 73 | `get_column_statistics` | 필수 | 데이터 정보 |
| 113 | `get_missing_values` | 필수 | 데이터 정보 |
| 140 | `get_value_counts` | 선택 | 데이터 정보 |
| 166 | `filter_dataframe` | 필수 | 데이터 조작 |
| 215 | `sort_dataframe` | 선택 | 데이터 조작 |
| 248 | `get_correlation` | 선택 | 통계 분석 |
| 281 | `group_by_aggregate` | 필수 | 통계 분석 |
| 327 | `get_unique_values` | 필수 | 데이터 조작 |
| 355 | `get_date_range` | 필수 | 시계열 |
| 392 | `get_outliers` | 선택 | 통계 분석 |
| 441 | `get_sample_rows` | 선택 | 데이터 조작 |
| 481 | `calculate_percentile` | 필수 | 통계 분석 |
| 514 | `get_geo_bounds` | 필수 | 지리 |
| 554 | `cross_tabulation` | 선택 | 통계 분석 |
| 594 | `analyze_missing_pattern` | 필수 | 데이터 품질 |
| 664 | `get_column_correlation_with_target` | 필수 | 통계 분석 |
| 717 | `detect_data_types` | 필수 | 데이터 품질 |
| 794 | `get_temporal_pattern` | 필수 | 시계열 |
| 854 | `summarize_categorical_distribution` | 필수 | 데이터 품질 |
| 912 | `predict_eclo` | 필수 | 예측 |
| 1004 | `predict_eclo_batch` | 필수 | 예측 |

---

### 2.2 AI 응답 복사 기능 (🔧 UX 개선)

| 구분 | AS-IS (v1.2.5) | TO-BE (v1.2.6) |
|:-----|:---------------|:---------------|
| **복사 방식** | 보고서에만 마크다운 다운로드 버튼 | 모든 응답에 복사 버튼 |
| **사용 편의성** | 다운로드 후 파일 열어야 함 | 클릭 시 바로 클립보드 복사 |
| **적용 범위** | 헤더(`#`) 포함 응답만 | 모든 AI 응답 |

#### 2.2.1 UI 변경

```
AS-IS (v1.2.5):
┌─────────────────────────────────────────┐
│  AI 응답 내용...                         │
│                                          │
│  [📥 마크다운 다운로드]  ← 보고서만 표시   │
└─────────────────────────────────────────┘

TO-BE (v1.2.6):
┌─────────────────────────────────────────┐
│  AI 응답 내용...                    [📋] │  ← 모든 응답에 복사 버튼
└─────────────────────────────────────────┘
```

---

## 3. 코드 품질 개선

### 3.1 Tool Calling config 전달 버그 (🔴 Critical)

| 위치 | AS-IS (v1.2.5) | TO-BE (v1.2.6) | 심각도 |
|:-----|:---------------|:---------------|:-------|
| `utils/tools.py:1178` | `tool_func.invoke({**tool_input, "config": config})` | `tool_func.invoke(tool_input, config=config)` | 🔴 Error |

#### 3.1.1 코드 수정 상세

```python
# AS-IS (v1.2.5) - utils/tools.py:1172-1178
def execute_tool(tool_name: str, tool_input: dict, df: pd.DataFrame) -> str:
    # ...
    try:
        config = {"configurable": {"dataframe": df, "current_dataset": ""}}
        tool_func = tools_map[tool_name]

        # ❌ 문제: config가 input dict에 포함됨
        return tool_func.invoke({**tool_input, "config": config})
    except Exception as e:
        return f"도구 실행 중 오류가 발생했습니다: {str(e)}"

# TO-BE (v1.2.6)
def execute_tool(tool_name: str, tool_input: dict, df: pd.DataFrame) -> str:
    # ...
    try:
        config = {"configurable": {"dataframe": df, "current_dataset": ""}}
        tool_func = tools_map[tool_name]

        # ✅ 수정: config를 별도 인자로 전달
        return tool_func.invoke(tool_input, config=config)
    except Exception as e:
        return f"도구 실행 중 오류가 발생했습니다: {str(e)}"
```

### 3.2 마크다운 다운로드 → 복사 버튼 (🔧 개선)

| 위치 | AS-IS (v1.2.5) | TO-BE (v1.2.6) | 심각도 |
|:-----|:---------------|:---------------|:-------|
| `app.py:1144-1158` | `st.download_button()` (조건부) | `st.button()` + clipboard (모든 응답) | 🔧 개선 |

#### 3.2.1 코드 수정 상세

```python
# AS-IS (v1.2.5) - app.py:1144-1158
# 응답에 마크다운 헤더가 있으면 보고서로 판단
if full_response and ('# ' in full_response or '## ' in full_response):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"report_{selected_display_name}_{timestamp}.md"
    st.download_button(
        label="📥 마크다운 다운로드",
        data=full_response,
        file_name=filename,
        mime="text/markdown",
        key=f"download_{timestamp}"
    )

# TO-BE (v1.2.6)
# 모든 AI 응답에 복사 버튼 추가
import pyperclip  # 또는 streamlit-clipboard 사용

col1, col2 = st.columns([0.95, 0.05])
with col1:
    response_container.markdown(full_response)
with col2:
    if st.button("📋", key=f"copy_{timestamp}", help="마크다운 복사"):
        st.session_state['clipboard'] = full_response
        st.toast("복사되었습니다!")
```

---

## 4. 변경 요약표

| 영역 | 변경 유형 | 내용 |
|:-----|:---------|:-----|
| `utils/tools.py` | 🐛 수정 | `execute_tool` config 전달 방식 수정 |
| `app.py` | 🔄 변경 | 마크다운 다운로드 → 복사 버튼으로 변경 |
| `app.py` | ➖ 제거 | 조건부 다운로드 버튼 제거 |

---

## 5. 구현 우선순위

### 🔴 P0 - 버그 수정 (필수/긴급)

| 순위 | 항목 | 설명 |
|:-----|:-----|:-----|
| 1 | **execute_tool config 수정** | 22개 도구 정상 작동을 위한 필수 수정 |

### 🟡 P1 - UX 개선 (중요)

| 순위 | 항목 | 설명 |
|:-----|:-----|:-----|
| 2 | 응답별 복사 버튼 추가 | 모든 AI 응답에 마크다운 복사 기능 |
| 3 | 다운로드 버튼 제거 | 기존 조건부 다운로드 버튼 제거 |

### 🟢 P2 - 테스트 (권장)

| 순위 | 항목 | 설명 |
|:-----|:-----|:-----|
| 4 | Tool Calling 통합 테스트 | 22개 도구 전체 정상 작동 확인 |
| 5 | 복사 기능 테스트 | 다양한 브라우저에서 클립보드 복사 확인 |

---

## 6. 테스트 계획

### 6.1 Tool Calling 테스트

| 테스트 케이스 | 도구 | 예상 결과 |
|:-------------|:-----|:---------|
| TC1 | `get_sample_rows(n=10)` | 10개 샘플 데이터 반환 |
| TC2 | `get_dataframe_info()` | 데이터프레임 기본 정보 반환 |
| TC3 | `get_column_statistics(column="ECLO")` | 컬럼 통계량 반환 |
| TC4 | `predict_eclo(...)` | ECLO 예측 결과 반환 |

### 6.2 복사 버튼 테스트

| 테스트 케이스 | 입력 | 예상 결과 |
|:-------------|:-----|:---------|
| TC5 | 짧은 응답 복사 | 클립보드에 마크다운 복사됨 |
| TC6 | 긴 보고서 복사 | 클립보드에 전체 내용 복사됨 |
| TC7 | 코드 블록 포함 응답 | 코드 블록 포함하여 복사됨 |

---

## 7. 다음 단계

1. **P0 구현**: `execute_tool` 함수 config 전달 방식 수정
2. **P0 테스트**: 22개 도구 정상 작동 확인
3. **P1 구현**: 복사 버튼 UI 구현
4. **P2 테스트**: 전체 기능 통합 테스트
5. **문서화**: README.md 버전 히스토리 업데이트
