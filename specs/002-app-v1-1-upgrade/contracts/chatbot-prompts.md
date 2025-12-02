# Chatbot Prompts Contract: 데이터 질의응답

**Feature Branch**: `002-app-v1-1-upgrade`
**Created**: 2025-12-01
**Status**: Complete

## 1. 개요

AI 챗봇이 데이터셋에 대해 질의응답할 때 사용하는 프롬프트 계약을 정의한다.

---

## 2. System Prompt

### 2.1 기본 시스템 프롬프트

```python
SYSTEM_PROMPT = """
당신은 데이터 분석 도우미입니다. 사용자가 업로드한 데이터셋에 대해 질문하면
데이터의 구조, 통계, 특징을 기반으로 정확하고 도움이 되는 답변을 제공합니다.

## 역할
- 데이터셋의 구조와 컬럼을 설명합니다
- 기본 통계 정보를 해석합니다
- 데이터 분석 방법을 제안합니다
- 시각화 아이디어를 제공합니다
- 데이터 품질 이슈(결측치, 이상치)를 안내합니다

## 제약사항
- 제공된 데이터 컨텍스트 범위 내에서만 답변합니다
- 데이터에 없는 정보를 추측하지 않습니다
- 한국어로 답변합니다
- 기술 용어는 설명을 덧붙입니다

## 답변 형식
- 명확하고 구조화된 답변을 제공합니다
- 필요시 마크다운 형식을 사용합니다
- 숫자는 천 단위 구분자를 사용합니다 (예: 1,234)
"""
```

---

## 3. Data Context Template

### 3.1 데이터셋 컨텍스트 생성 함수

```python
def create_data_context(df: pd.DataFrame, dataset_name: str) -> str:
    """
    DataFrame을 기반으로 AI에게 전달할 컨텍스트 생성.

    Parameters:
        df (pd.DataFrame): 분석 대상 데이터셋
        dataset_name (str): 데이터셋 표시명

    Returns:
        str: 포맷된 데이터 컨텍스트
    """
    context = f"""
## 데이터셋 정보: {dataset_name}

### 기본 정보
- 행 수: {len(df):,}개
- 컬럼 수: {len(df.columns)}개

### 컬럼 목록
{_format_columns(df)}

### 숫자형 컬럼 통계
{_format_numeric_stats(df)}

### 결측치 현황
{_format_missing_info(df)}

### 샘플 데이터 (처음 5행)
{df.head().to_string()}
"""
    return context
```

### 3.2 헬퍼 함수들

```python
def _format_columns(df: pd.DataFrame) -> str:
    """컬럼 정보 포맷팅."""
    lines = []
    for col in df.columns:
        dtype = df[col].dtype
        non_null = df[col].count()
        lines.append(f"- {col}: {dtype} (비결측: {non_null:,}개)")
    return "\n".join(lines)


def _format_numeric_stats(df: pd.DataFrame) -> str:
    """숫자형 컬럼 통계 포맷팅."""
    numeric_df = df.select_dtypes(include=['number'])
    if numeric_df.empty:
        return "숫자형 컬럼이 없습니다."

    stats = numeric_df.describe()
    return stats.to_string()


def _format_missing_info(df: pd.DataFrame) -> str:
    """결측치 정보 포맷팅."""
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(1)

    lines = []
    for col in df.columns:
        if missing[col] > 0:
            lines.append(f"- {col}: {missing[col]:,}개 ({missing_pct[col]}%)")

    if not lines:
        return "결측치가 없습니다."
    return "\n".join(lines)
```

---

## 4. Message Format

### 4.1 사용자 메시지 형식

```python
def format_user_message(question: str, data_context: str) -> str:
    """
    사용자 질문과 데이터 컨텍스트를 결합.
    """
    return f"""
{data_context}

---

## 사용자 질문
{question}
"""
```

### 4.2 대화 이력 관리

```python
def build_messages(
    question: str,
    data_context: str,
    history: list[dict]
) -> list[dict]:
    """
    API 호출용 메시지 목록 구성.

    Parameters:
        question: 현재 질문
        data_context: 데이터셋 컨텍스트
        history: 이전 대화 이력

    Returns:
        list[dict]: API 메시지 형식
    """
    messages = []

    # 이전 대화 이력 추가 (최근 10개까지)
    for msg in history[-10:]:
        messages.append(msg)

    # 현재 질문 추가
    user_content = format_user_message(question, data_context)
    messages.append({
        'role': 'user',
        'content': user_content
    })

    return messages
```

---

## 5. API Call Contract

### 5.1 요청 형식

```python
{
    "model": "claude-sonnet-4-20250514",  # 또는 다른 지원 모델
    "max_tokens": 1024,
    "system": SYSTEM_PROMPT,
    "messages": [
        {"role": "user", "content": "데이터 컨텍스트 + 질문"},
        {"role": "assistant", "content": "이전 응답"},
        {"role": "user", "content": "데이터 컨텍스트 + 후속 질문"},
        ...
    ]
}
```

### 5.2 응답 형식

```python
{
    "content": [
        {"type": "text", "text": "응답 내용"}
    ],
    "usage": {
        "input_tokens": 1234,
        "output_tokens": 567
    }
}
```

### 5.3 에러 처리

| 에러 유형 | HTTP 코드 | 사용자 메시지 |
|----------|----------|--------------|
| Invalid API Key | 401 | "API Key를 확인해주세요." |
| Rate Limit | 429 | "요청이 너무 많습니다. 잠시 후 다시 시도해주세요." |
| Network Error | - | "네트워크 오류가 발생했습니다. 인터넷 연결을 확인해주세요." |
| Timeout | - | "응답 시간이 초과되었습니다. 다시 시도해주세요." |

---

## 6. 예시 대화

### 6.1 데이터 구조 질문

**사용자**: "이 데이터셋에는 어떤 정보가 있나요?"

**예상 응답**:
```
이 CCTV 데이터셋에는 대구시 CCTV 설치 현황 정보가 포함되어 있습니다.

## 주요 컬럼
- **설치위치**: CCTV가 설치된 주소
- **위도/경도**: 정확한 좌표 정보
- **관리기관**: CCTV를 관리하는 기관명
- **설치일자**: CCTV 설치 날짜

## 기본 통계
- 총 1,234개의 CCTV 정보가 있습니다
- 결측치가 있는 컬럼: 설치일자 (15개, 1.2%)

지도 시각화를 통해 CCTV 분포를 확인하시거나,
관리기관별 설치 현황을 분석해보시는 것을 추천드립니다.
```

### 6.2 통계 분석 질문

**사용자**: "데이터에서 이상한 점이 있나요?"

**예상 응답**:
```
데이터를 분석한 결과, 다음과 같은 점이 발견되었습니다:

## 결측치 현황
- 설치일자: 15개 (1.2%) - 일부 CCTV의 설치 날짜가 누락됨

## 좌표 이상치
- 경도가 0인 데이터: 3개 - 좌표가 정상적으로 기록되지 않은 것으로 보임
- 위도 범위 이상: 없음 (모두 35.7~36.1° 범위 내)

## 데이터 품질
- 전반적으로 양호한 상태입니다
- 지도 시각화 시 좌표가 0인 3개 데이터는 제외됩니다

분석 시 결측치가 있는 행을 어떻게 처리할지 결정해주세요.
```

---

## 7. 토큰 최적화

### 7.1 컨텍스트 크기 제한

```python
MAX_CONTEXT_ROWS = 1000  # 통계 계산용 최대 행 수
MAX_SAMPLE_ROWS = 5      # 샘플 데이터 표시 행 수
MAX_HISTORY_MESSAGES = 10  # 대화 이력 유지 개수
```

### 7.2 컨텍스트 압축

대용량 데이터셋의 경우:
- 전체 통계는 샘플링된 데이터 기반
- 샘플 데이터는 처음 5행만 포함
- 컬럼이 20개 초과 시 주요 컬럼만 표시
