# Data Model: App v1.1.1 Upgrade

**Feature Branch**: `003-app-v111-upgrade`
**Created**: 2025-12-02

---

## 1. 핵심 엔티티

### 1.1 Tool (분석 도구)

15개의 데이터 분석 도구를 정의합니다.

| 필드 | 타입 | 설명 |
|:-----|:-----|:-----|
| `name` | `str` | 도구 고유 이름 (snake_case) |
| `description` | `str` | 도구 설명 (한글) |
| `input_schema` | `dict` | JSON Schema 형식의 입력 스키마 |
| `handler` | `Callable` | 도구 실행 함수 |

**도구 목록**:

| # | 도구명 | 설명 | 필수 파라미터 |
|:--|:-------|:-----|:-------------|
| 1 | `get_dataframe_info` | DataFrame 기본 정보 | - |
| 2 | `get_column_statistics` | 특정 컬럼의 통계 정보 | `column` |
| 3 | `get_missing_values` | 결측치 현황 분석 | - |
| 4 | `get_value_counts` | 범주형 컬럼의 값 분포 | `column`, `top_n` (optional) |
| 5 | `filter_dataframe` | 조건에 따른 데이터 필터링 | `column`, `operator`, `value` |
| 6 | `sort_dataframe` | 특정 컬럼 기준 정렬 | `column`, `ascending` (optional) |
| 7 | `get_correlation` | 수치형 컬럼 간 상관관계 | `columns` (optional) |
| 8 | `group_by_aggregate` | 그룹별 집계 연산 | `group_column`, `agg_column`, `operation` |
| 9 | `get_unique_values` | 특정 컬럼의 고유값 목록 | `column` |
| 10 | `get_date_range` | 날짜 컬럼의 범위 분석 | `column` |
| 11 | `get_outliers` | 이상치 탐지 (IQR 기반) | `column` |
| 12 | `get_sample_rows` | 조건부 샘플 데이터 추출 | `n` (optional), `condition` (optional) |
| 13 | `calculate_percentile` | 백분위수 계산 | `column`, `percentile` |
| 14 | `get_geo_bounds` | 위경도 데이터의 지리적 범위 | - |
| 15 | `cross_tabulation` | 교차표 생성 | `row_column`, `col_column` |

---

### 1.2 ChatHistory (대화 이력)

데이터셋별로 분리된 대화 이력을 관리합니다.

```python
# 데이터 구조
chat_history: dict[str, list[ChatMessage]] = {
    "cctv": [
        {"role": "user", "content": "..."},
        {"role": "assistant", "content": [ContentBlock, ...]},
        {"role": "user", "content": [ToolResult, ...]},
    ],
    "lights": [...],
    # ...
}
```

**ChatMessage 필드**:

| 필드 | 타입 | 설명 |
|:-----|:-----|:-----|
| `role` | `str` | `"user"` 또는 `"assistant"` |
| `content` | `str \| list` | 텍스트 또는 ContentBlock 리스트 |

**ContentBlock 타입**:

1. **TextBlock**: `{"type": "text", "text": "..."}`
2. **ToolUseBlock**: `{"type": "tool_use", "id": "...", "name": "...", "input": {...}}`
3. **ToolResultBlock**: `{"type": "tool_result", "tool_use_id": "...", "content": "..."}`

---

### 1.3 MapCache (지도 캐시)

지도 객체를 캐싱하여 재렌더링을 방지합니다.

```python
# session_state 키 패턴
map_cache_key = f"map_{dataset_name}_{row_count}"

# 저장 객체
st.session_state[map_cache_key] = folium.Map(...)
```

| 필드 | 타입 | 설명 |
|:-----|:-----|:-----|
| `cache_key` | `str` | `map_{dataset}_{rows}` 형식 |
| `map_object` | `folium.Map` | Folium 지도 객체 |

---

### 1.4 TokenUsage (토큰 사용량)

API 호출의 토큰 사용량을 추적합니다.

```python
tokens: dict[str, int] = {
    "input": 0,    # 입력 토큰 누적
    "output": 0,   # 출력 토큰 누적
    "total": 0     # 총 토큰 누적
}
```

---

## 2. 상태 전이 (State Transitions)

### 2.1 Tool Calling 상태 흐름

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   [User Question]                                           │
│         │                                                   │
│         ▼                                                   │
│   ┌───────────┐                                             │
│   │ API Call  │                                             │
│   └─────┬─────┘                                             │
│         │                                                   │
│         ▼                                                   │
│   ┌───────────────────┐                                     │
│   │ stop_reason check │                                     │
│   └─────────┬─────────┘                                     │
│             │                                               │
│     ┌───────┴───────┐                                       │
│     │               │                                       │
│     ▼               ▼                                       │
│ [tool_use]     [end_turn]                                   │
│     │               │                                       │
│     ▼               ▼                                       │
│ ┌─────────┐   ┌──────────┐                                  │
│ │Execute  │   │ Display  │                                  │
│ │ Tools   │   │ Response │                                  │
│ └────┬────┘   └──────────┘                                  │
│      │                                                      │
│      ▼                                                      │
│ [iteration < 3?]──No──▶ "답변할 수 없는 질문입니다"           │
│      │                                                      │
│      Yes                                                    │
│      │                                                      │
│      ▼                                                      │
│ [Add tool_result]                                           │
│      │                                                      │
│      └──────────▶ [API Call] (반복)                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 데이터셋 전환 시 상태 변화

```
[탭 전환: CCTV → 보안등]
         │
         ▼
┌───────────────────────┐
│ selected_dataset =    │
│   "lights"            │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ 대화 이력 로드:       │
│ chat_history["lights"]│
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ 지도 캐시 확인:       │
│ map_lights_{rows}     │
└───────────────────────┘
```

---

## 3. 검증 규칙

### 3.1 Tool 입력 검증

| 도구 | 검증 규칙 |
|:-----|:---------|
| `get_column_statistics` | `column`이 DataFrame에 존재해야 함, 수치형이어야 함 |
| `filter_dataframe` | `operator`가 허용된 연산자여야 함 |
| `group_by_aggregate` | `operation`이 `sum`, `mean`, `count`, `min`, `max` 중 하나 |
| `calculate_percentile` | `percentile`이 0-100 사이 값 |
| `cross_tabulation` | 두 컬럼이 모두 존재해야 함 |

### 3.2 API 응답 검증

| 조건 | 처리 |
|:-----|:-----|
| `stop_reason == "tool_use"` | 도구 실행 후 재호출 |
| `stop_reason == "end_turn"` | 최종 응답 표시 |
| `iteration >= 3` | 타임아웃 메시지 표시 |
| 도구 실행 실패 | `is_error: true`로 결과 전달 |

---

## 4. 에러 응답 정의

| 상황 | 응답 메시지 |
|:-----|:-----------|
| 도구 미발견 (3회 iteration 후) | "현재 앱이 답변할 수 없는 질문입니다." |
| 데이터 무관 질문 | "데이터와 관련 없는 질문에 대해서는 대답할 수 없습니다." |
| 도구 실행 오류 | "분석 중 오류가 발생했습니다. 다시 시도해주세요." |
| 컬럼 미존재 | "'{column}' 컬럼을 찾을 수 없습니다." |
| 빈 DataFrame | 해당 통계에 대해 "데이터가 없습니다" 반환 |
