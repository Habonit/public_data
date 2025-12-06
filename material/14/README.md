# 14일차: LangChain & LangGraph 대화 메모리 관리

## 개요

LangChain과 LangGraph를 활용하여 AI 챗봇의 **대화 메모리**를 관리하는 4가지 방식을 학습합니다.

- **학습 환경**: Google Colab
- **사용 모델**: Claude 4.5 시리즈 (Haiku, Sonnet, Opus)
- **핵심 라이브러리**: `langchain`, `langchain-anthropic`, `langgraph`

---

## 학습 순서

```
01_buffer_memory   →  02_window_memory  →  03_summary_memory  →  04_hybrid_memory
(전체 저장)           (최근 N개)            (요약 저장)            (하이브리드)
```

---

## 노트북별 학습 내용

### 01. Buffer Memory

**파일**: `14_01_buffer_memory.ipynb`

| 개념 | 설명 |
|:-----|:-----|
| Buffer Memory | 모든 대화를 그대로 저장 |
| InMemoryChatMessageHistory | LangChain 기본 메모리 저장소 |
| MemorySaver | LangGraph 메모리 체크포인터 |
| SqliteSaver | SQLite 기반 영구 저장 |

**장단점**:
- 장점: 구현 간단, 모든 맥락 유지
- 단점: 대화가 길어지면 토큰 비용 급증

---

### 02. Window Memory

**파일**: `14_02_window_memory.ipynb`

| 개념 | 설명 |
|:-----|:-----|
| Window Memory | 최근 N개 메시지만 유지 |
| trim_messages | 메시지 개수/토큰 기준 트리밍 |
| 커스텀 Reducer | `windowed_add_messages` 구현 |

**핵심 코드 패턴**:
```python
def trim_messages_to_window(messages: list, window_size: int) -> list:
    if len(messages) <= window_size:
        return messages
    return messages[-window_size:]
```

**장단점**:
- 장점: 토큰 비용 일정, 구현 간단
- 단점: 오래된 중요 정보 손실

---

### 03. Summary Memory

**파일**: `14_03_summary_memory.ipynb`

| 개념 | 설명 |
|:-----|:-----|
| Summary Memory | LLM으로 대화 요약 후 저장 |
| 요약 트리거 | N개 메시지마다 요약 실행 |
| 누적 요약 | 기존 요약 + 새 대화 통합 |

**핵심 코드 패턴**:
```python
def summarize_conversation(messages: list, existing_summary: str) -> str:
    prompt = f"기존 요약: {existing_summary}\n새 대화: {text}\n통합 요약:"
    response = summarizer_llm.invoke([HumanMessage(content=prompt)])
    return response.content
```

**장단점**:
- 장점: 적은 토큰으로 전체 맥락 유지
- 단점: 요약 시 세부 정보 손실 가능, 추가 LLM 호출 필요

---

### 04. Hybrid Memory (Window + Summary)

**파일**: `14_04_hybrid_memory.ipynb`

| 개념 | 설명 |
|:-----|:-----|
| Hybrid Memory | Window + Summary 결합 |
| 윈도우 영역 | 최근 N개 메시지 (세부 맥락) |
| 요약 영역 | 오래된 대화 요약 (장기 맥락) |

**메모리 구조**:
```
┌────────────────────────────────────────────┐
│ [요약] 이전 대화의 핵심 정보              │
├────────────────────────────────────────────┤
│ [윈도우] 최근 6개 메시지 (세부 맥락 유지)  │
└────────────────────────────────────────────┘
```

**장단점**:
- 장점: 최근 맥락 + 장기 맥락 모두 유지, 토큰 효율적
- 단점: 구현 복잡도 높음

---

## 핵심 개념 요약

### 메모리 방식 비교

| 방식 | 토큰 효율 | 맥락 유지 | 구현 복잡도 | 적합한 사용 사례 |
|:-----|:---------|:---------|:-----------|:---------------|
| Buffer | 낮음 | 완벽 | 매우 쉬움 | 짧은 대화 |
| Window | 높음 | 최근만 | 쉬움 | 간단한 Q&A |
| Summary | 높음 | 좋음 | 중간 | 장기 대화 |
| Hybrid | 높음 | 매우 좋음 | 높음 | 복잡한 작업 |

### LangChain 핵심 클래스

| 클래스 | 설명 |
|:-------|:-----|
| `ChatAnthropic` | Claude 모델 래퍼 |
| `HumanMessage` | 사용자 메시지 |
| `AIMessage` | AI 응답 메시지 |
| `SystemMessage` | 시스템 프롬프트 |
| `InMemoryChatMessageHistory` | 메모리 기반 대화 저장소 |

### LangGraph 핵심 구성요소

| 구성요소 | 설명 |
|:---------|:-----|
| `StateGraph` | 상태 기반 그래프 정의 |
| `TypedDict` | 상태 스키마 정의 |
| `Annotated` | Reducer 함수 지정 |
| `add_messages` | 메시지 누적 Reducer |
| `MemorySaver` | 메모리 체크포인터 |
| `SqliteSaver` | SQLite 영구 저장 |

### LangGraph 그래프 구조

```python
# 상태 정의
class State(TypedDict):
    messages: Annotated[list, add_messages]
    summary: str

# 그래프 구성
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot_node)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# 컴파일
graph = graph_builder.compile(checkpointer=MemorySaver())
```

---

## 권장 설정

| 파라미터 | 권장 값 | 설명 |
|:---------|:--------|:-----|
| 윈도우 크기 | 4-6개 | 최근 2-3턴 대화 유지 |
| 요약 임계값 | 윈도우 × 1.5~2 | 요약 트리거 시점 |

---

## 사용된 모델

| 모델 | ID | 용도 |
|:-----|:---|:-----|
| Claude 4.5 Haiku | `claude-haiku-4-5-20251001` | 빠른 테스트용 |
| Claude 4.5 Sonnet | `claude-sonnet-4-5-20250929` | 균형잡힌 성능 |
| Claude 4.5 Opus | `claude-opus-4-5-20251101` | 최고 성능 |

---

## 학습 체크리스트

- [ ] Buffer Memory로 전체 대화 저장 이해
- [ ] Window Memory로 최근 N개 유지 구현
- [ ] Summary Memory로 LLM 기반 요약 구현
- [ ] Hybrid Memory로 두 방식 결합
- [ ] LangGraph StateGraph 구조 이해
- [ ] SQLite 영구 저장 적용

---

## 참고 자료

- [LangChain 문서](https://python.langchain.com/)
- [LangGraph 문서](https://langchain-ai.github.io/langgraph/)
- [Anthropic Claude API](https://docs.anthropic.com/)
