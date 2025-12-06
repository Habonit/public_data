# 15일차: LangGraph 메모리 관리 + Tool Calling 통합

## 개요

LangGraph의 **ToolNode**를 활용하여 메모리 관리와 Tool Calling을 통합 구현합니다.

- **핵심 주제**: 메모리 방식별 Tool Calling 통합
- **학습 환경**: Google Colab
- **사용 모델**: Claude 4.5 시리즈

---

## 학습 순서

```
01_buffer_memory   →  02_window_memory  →  03_summary_memory
(전체 저장 + 도구)     (최근 N개 + 도구)     (요약 + 도구)
```

---

## 노트북별 학습 내용

### 01. Buffer Memory + Tool Calling

**파일**: `15_01_buffer_memory.ipynb`

| 개념 | 설명 |
|:-----|:-----|
| Buffer Memory | 모든 대화 메시지 누적 저장 |
| `@tool` 데코레이터 | 커스텀 도구 정의 |
| ToolNode | LangGraph 도구 실행 노드 |
| `bind_tools()` | LLM에 도구 바인딩 |

**그래프 구조**:
```
START → chatbot → [tool_calls?] → tools → chatbot
                → [no tools]   → END
```

**핵심 코드 패턴**:
```python
from langgraph.prebuilt import ToolNode

# 도구 정의
@tool
def calculator(a: float, b: float, operation: str) -> str:
    """두 숫자의 사칙연산을 수행합니다."""
    ...

# LLM에 도구 바인딩
llm_with_tools = llm.bind_tools(all_tools)

# 도구 노드 생성
tool_node = ToolNode(tools=all_tools)
```

---

### 02. Window Memory + Tool Calling

**파일**: `15_02_window_memory.ipynb`

| 개념 | 설명 |
|:-----|:-----|
| Window Memory | 최근 N개 메시지만 유지 |
| `RemoveMessage` | 오래된 메시지 삭제 |
| `window_memory` 노드 | 메시지 트리밍 처리 |

**그래프 구조 (Buffer와 차이)**:
```
START → chatbot → [tool_calls?] → tools → chatbot
                → [no tools]   → window_memory → END
```

**핵심 코드 패턴**:
```python
from langchain_core.messages import RemoveMessage

def window_memory_node(state: State) -> dict:
    """오래된 메시지를 삭제"""
    messages = state["messages"]

    if len(counted_msgs) > WINDOW_SIZE:
        # 삭제할 메시지 지정
        return {"messages": [RemoveMessage(id=m.id) for m in old_msgs]}
    return {"messages": []}
```

**카운트 규칙**:
- ✅ `HumanMessage` - 카운트 대상
- ✅ `AIMessage` (content만) - 카운트 대상
- ❌ `AIMessage` (tool_calls) - 카운트 제외, 유지
- ❌ `ToolMessage` - 카운트 제외, 유지

---

### 03. Summary Memory + Tool Calling

**파일**: `15_03_summary_memory.ipynb`

| 개념 | 설명 |
|:-----|:-----|
| Summary Memory | 오래된 대화를 요약으로 압축 |
| `summarizer` 노드 | 요약 생성 및 메시지 삭제 |
| 누적 요약 | 기존 요약 + 새 대화 통합 |

**그래프 구조**:
```
START → chatbot → [tool_calls?] → tools → chatbot
                → [no tools]   → summarizer → END
```

**상태 정의**:
```python
class State(TypedDict):
    messages: Annotated[list, add_messages]
    summary: str  # 요약 텍스트 추가
```

**핵심 코드 패턴**:
```python
def summarizer(state: State) -> dict:
    """오래된 메시지를 요약으로 변환"""
    messages = state["messages"]
    summary = state.get("summary", "")

    # 가장 오래된 2쌍(4개) 요약
    to_summarize = counted_msgs[:SUMMARY_WINDOW * 2]
    new_summary = create_summary(to_summarize, summary)

    return {
        "messages": [RemoveMessage(id=m.id) for m in to_summarize],
        "summary": new_summary
    }
```

---

## 핵심 개념 요약

### 메모리 + Tool Calling 통합 비교

| 방식 | 그래프 노드 | 종료 흐름 | 특징 |
|:-----|:-----------|:---------|:-----|
| Buffer | chatbot, tools | chatbot → END | 단순, 토큰 증가 |
| Window | chatbot, tools, **window_memory** | chatbot → **window_memory** → END | 오래된 정보 삭제 |
| Summary | chatbot, tools, **summarizer** | chatbot → **summarizer** → END | 요약으로 압축 |

### 사용된 도구

**커스텀 도구 (3개)**:
| 도구 | 설명 |
|:-----|:-----|
| `get_current_time` | 현재 날짜/시간 조회 |
| `calculator` | 사칙연산 수행 |
| `random_number` | 범위 내 랜덤 숫자 생성 |

**외부 도구 (2개)**:
| 도구 | 설명 |
|:-----|:-----|
| `WikipediaQueryRun` | 위키피디아 검색 |
| `DuckDuckGoSearchRun` | 웹 검색 |

### LangGraph 핵심 구성요소

| 구성요소 | 설명 |
|:---------|:-----|
| `StateGraph` | 상태 기반 그래프 |
| `ToolNode` | 도구 실행 노드 |
| `add_messages` | 메시지 누적 Reducer |
| `RemoveMessage` | 메시지 삭제 |
| `SqliteSaver` | SQLite 영구 저장 |

---

## 토큰 비용 비교

| 대화 쌍 | Buffer | Window (K=6) | Summary | 절감률 |
|:--------|:-------|:-------------|:--------|:------|
| 5 | 1,000 | 600 | 750 | 25% |
| 10 | 2,000 | 600 | 1,050 | 47% |
| 20 | 4,000 | 600 | 1,800 | 55% |
| 50 | 10,000 | 600 | 4,050 | 60% |

---

## 권장 설정

| 파라미터 | 권장 값 | 설명 |
|:---------|:--------|:-----|
| WINDOW_SIZE | 6 | 최근 3턴 대화 유지 |
| SUMMARY_WINDOW | 2 | 2쌍(4개) 메시지 요약 |

---

## 학습 체크리스트

- [ ] `@tool` 데코레이터로 커스텀 도구 정의
- [ ] `ToolNode`로 도구 실행 노드 생성
- [ ] `bind_tools()`로 LLM에 도구 바인딩
- [ ] 메모리 방식별 그래프 구조 차이 이해
- [ ] `RemoveMessage`로 메시지 삭제
- [ ] Summary 누적 로직 이해
- [ ] tool_calls/ToolMessage 카운트 제외 규칙

---

## 참고 자료

- [LangGraph 문서](https://langchain-ai.github.io/langgraph/)
- [LangChain Tools](https://python.langchain.com/docs/concepts/tools/)
- [Anthropic Claude API](https://docs.anthropic.com/)
