# 13일차: Anthropic Claude Tool Calling

## 개요

Anthropic Claude API를 활용한 Tool Calling(Function Calling) 개념을 학습합니다.

- **최종 목표**: 연쇄적인 Tool Calling으로 언어모델이 더 나은 답변을 생성하도록 구현
- **학습 환경**: Google Colab
- **사용 모델**: Claude 4.5 시리즈 (Haiku, Sonnet, Opus)

---

## 학습 순서

노트북은 개념을 점진적으로 확장하며 구성되어 있습니다:

```
01_basic_api_call     →  02_tool_definition  →  03_tool_execution  →  04_multiple_tools
(API 기초)               (도구 정의)             (도구 실행)            (다중 도구)
```

---

## 노트북별 학습 내용

### 01. Basic API Call

**파일**: `13_01_basic_api_call.ipynb`

| 주제 | 내용 |
|:-----|:-----|
| API 설정 | `anthropic` 패키지 설치, API Key 설정 |
| 기본 호출 | `client.messages.create()` 사용법 |
| 응답 구조 | `id`, `content`, `stop_reason`, `usage` 분석 |
| 시스템 프롬프트 | 역할 지정 및 응답 스타일 제어 |

**핵심 코드 패턴**:
```python
from anthropic import Anthropic
client = Anthropic(api_key="YOUR_API_KEY")

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    messages=[{"role": "user", "content": "질문"}]
)
```

---

### 02. Tool Definition

**파일**: `13_02_tool_definition.ipynb`

| 주제 | 내용 |
|:-----|:-----|
| JSON Schema | 도구 정의 형식 (`name`, `description`, `input_schema`) |
| 단순 도구 | 파라미터 없는 도구 (`get_current_time`) |
| 파라미터 도구 | 필수 파라미터 사용 (`get_weather`) |
| enum 제한 | 파라미터 값 제한 (`calculator`) |
| description 중요성 | 좋은 설명 vs 나쁜 설명 비교 |

**도구 정의 형식**:
```python
tools = [{
    "name": "tool_name",
    "description": "도구에 대한 상세 설명",
    "input_schema": {
        "type": "object",
        "properties": {
            "param": {"type": "string", "description": "파라미터 설명"}
        },
        "required": ["param"]
    }
}]
```

---

### 03. Tool Execution

**파일**: `13_03_tool_execution.ipynb`

| 주제 | 내용 |
|:-----|:-----|
| Agentic Loop | 사용자 → AI 도구 요청 → 실행 → 결과 반환 → AI 최종 응답 |
| execute_tool() | 도구 이름으로 실제 함수 호출 |
| tool_result | `tool_use_id`를 포함한 결과 메시지 형식 |
| 루프 종료 조건 | `stop_reason == "end_turn"` 확인 |

**Agentic Loop 흐름**:
```
┌─────────────────────────────────────────────────────────┐
│  사용자 질문                                              │
│       ↓                                                  │
│  Claude 분석 → stop_reason: "tool_use"                   │
│       ↓                                                  │
│  도구 실행 (execute_tool)                                 │
│       ↓                                                  │
│  tool_result 메시지 추가                                  │
│       ↓                                                  │
│  Claude 최종 응답 → stop_reason: "end_turn"              │
└─────────────────────────────────────────────────────────┘
```

---

### 04. Multiple Tools

**파일**: `13_04_multiple_tools.ipynb`

| 주제 | 내용 |
|:-----|:-----|
| 다중 도구 등록 | 4개 도구 동시 사용 (time, calculator, weather, random) |
| 병렬 호출 | 하나의 응답에서 여러 도구 동시 요청 |
| 연쇄 호출 | 이전 도구 결과를 다음 도구 입력으로 사용 |
| DEBUG 모드 | 도구 호출 과정 상세 로깅 |

**호출 유형 비교**:

| 유형 | 설명 | 예시 |
|:-----|:-----|:-----|
| 병렬 (Parallel) | 독립적인 여러 도구 동시 호출 | "서울과 부산 날씨 알려줘" |
| 연쇄 (Chained) | 이전 결과를 다음 입력으로 사용 | "현재 시간의 분을 2배로 계산해줘" |

---

## 핵심 개념 요약

| 개념 | 설명 |
|:-----|:-----|
| Tool Calling | AI가 외부 함수를 호출하여 실시간 정보를 얻는 기능 |
| JSON Schema | 도구의 파라미터 구조를 정의하는 표준 형식 |
| Agentic Loop | 도구 호출 → 실행 → 결과 반환의 반복 패턴 |
| stop_reason | `tool_use` (도구 요청) vs `end_turn` (대화 종료) |
| tool_result | 도구 실행 결과를 AI에게 전달하는 메시지 형식 |

---

## 사용된 모델

| 모델 | ID | 용도 |
|:-----|:---|:-----|
| Claude 4.5 Haiku | `claude-haiku-4-5-20251001` | 빠른 응답, 테스트용 |
| Claude 4.5 Sonnet | `claude-sonnet-4-5-20250929` | 균형잡힌 성능 |
| Claude 4.5 Opus | `claude-opus-4-5-20251101` | 최고 성능 |

---

## 학습 체크리스트

- [ ] API Key 설정 및 기본 호출 이해
- [ ] JSON Schema로 도구 정의하기
- [ ] Agentic Loop 패턴 구현
- [ ] 다중 도구 병렬/연쇄 호출 이해
- [ ] 실제 프로젝트에 Tool Calling 적용

---

## 참고 자료

- [Anthropic API 문서](https://docs.anthropic.com/)
- [Tool Use 가이드](https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview)
- [JSON Schema 스펙](https://json-schema.org/)
