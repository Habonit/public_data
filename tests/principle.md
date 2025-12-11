# 테스트 원칙 및 방법론

**문서 버전**: v2.3
**작성일**: 2025-12-11
**목적**: 테스트 작성 시 따라야 하는 추상적 원칙과 방법론 정의

> **참고**: 이 프로젝트에서의 구체적인 테스트 대상, 실행 방법, 워크플로우는 `tests/README.md`를 참조한다.

---

## 개요

이 문서는 **TDD(Test-Driven Development)**를 실천하기 위한 완전한 방법론을 제공한다.

### 이 문서를 숙지하면 할 수 있는 것

| 역량 | 설명 | 관련 섹션 |
|:----|:-----|:---------|
| **Red-Green-Refactor 사이클 실천** | 실패하는 테스트 작성 → 통과하는 코드 구현 → 리팩토링의 반복 | Part 1, Section 1 |
| **효과적인 테스트 케이스 설계** | 경계값 분석, 동치 분할로 누락 없는 테스트 케이스 도출 | Part 1, Section 3 |
| **테스트 더블 활용** | Mock, Stub, Fake, Spy를 상황에 맞게 사용 | Part 1, Section 4 |
| **단위 테스트 작성** | AAA 패턴, 격리된 테스트, pytest fixture 활용 | Part 2 |
| **통합 테스트 작성** | 모듈 간 흐름 검증, 실제 의존성 테스트 | Part 3 |
| **E2E 테스트 설계** | 사용자 시나리오 기반 전체 흐름 검증 | Part 4 |

### Red → Green → Refactor 달성 경로

이 문서의 각 Part는 TDD 사이클의 각 단계를 지원한다:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          TDD 사이클 달성 경로                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   🔴 RED (실패하는 테스트 작성)                                               │
│   ├─ Part 1, Section 3: 테스트 케이스 설계 기법으로 "무엇을 테스트할지" 결정     │
│   ├─ Part 2: 단위 테스트 작성 규칙으로 "어떻게 테스트할지" 결정                 │
│   └─ Part 3, 4: 통합/E2E 테스트로 "전체 흐름을 어떻게 검증할지" 결정            │
│                                                                             │
│                              ▼                                              │
│                                                                             │
│   🟢 GREEN (테스트를 통과하는 최소한의 코드 작성)                               │
│   ├─ Part 1, Section 1.2: "최소한의 코드"란 테스트만 통과하는 코드              │
│   ├─ Part 1, Section 4: 테스트 더블로 외부 의존성 격리하며 구현                 │
│   └─ Part 2, Section 5.3: AAA 패턴으로 구현 결과 검증                         │
│                                                                             │
│                              ▼                                              │
│                                                                             │
│   🔵 REFACTOR (코드 개선, 테스트는 계속 통과)                                  │
│   ├─ Part 1, Section 2: pytest fixture로 중복 제거                           │
│   ├─ Part 2, Section 7: 테스트 우선순위로 중요한 것부터 개선                    │
│   └─ 모든 Part: 테스트가 통과하면 안전하게 리팩토링 가능                        │
│                                                                             │
│                              ▼                                              │
│                         (다음 기능으로 반복)                                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### TDD 숙련도 체크리스트

아래 항목을 모두 설명하고 실천할 수 있다면 TDD를 숙지했다고 볼 수 있다:

- [ ] Red-Green-Refactor 사이클을 설명하고 실천할 수 있다
- [ ] 테스트를 먼저 작성하고, 그 테스트를 통과하는 코드를 구현할 수 있다
- [ ] 경계값 분석과 동치 분할로 테스트 케이스를 설계할 수 있다
- [ ] Mock, Stub, Fake, Spy의 차이를 알고 적절히 사용할 수 있다
- [ ] AAA 패턴(Arrange-Act-Assert)으로 테스트를 구조화할 수 있다
- [ ] pytest fixture를 활용하여 테스트 간 중복을 제거할 수 있다
- [ ] 단위/통합/E2E 테스트의 차이를 알고 상황에 맞게 선택할 수 있다
- [ ] 테스트 피라미드 비율(Unit 70% : Integration 25% : E2E 5%)을 이해한다

---

## 목차

- [Part 1: TDD 방법론](#part-1-tdd-방법론)
- [Part 2: 단위 테스트 규칙](#part-2-단위-테스트-규칙)
- [Part 3: 통합 테스트 규칙](#part-3-통합-테스트-규칙)
- [Part 4: E2E 테스트 규칙](#part-4-e2e-테스트-규칙)

---

# Part 1: TDD 방법론

## 1. TDD란?

**TDD(Test-Driven Development, 테스트 주도 개발)**는 테스트를 먼저 작성하고, 그 테스트를 통과하는 코드를 작성하는 개발 방법론이다.

### 1.1 핵심 철학

> "동작하는 깔끔한 코드(Clean code that works)"를 목표로 한다.

- **테스트가 개발을 이끈다**: 코드를 작성하기 전에 "이 코드가 무엇을 해야 하는가?"를 테스트로 먼저 정의
- **작은 단위로 반복**: 한 번에 하나의 기능만 테스트하고 구현
- **리팩토링 안전망**: 테스트가 있으면 코드를 안전하게 개선할 수 있음

### 1.2 Red-Green-Refactor 사이클

TDD의 핵심은 **3단계 사이클**을 반복하는 것이다:

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│    ┌─────────┐      ┌─────────┐      ┌───────────┐         │
│    │   Red   │ ───► │  Green  │ ───► │ Refactor  │ ──┐     │
│    │ (실패)  │      │ (통과)  │      │  (개선)   │   │     │
│    └─────────┘      └─────────┘      └───────────┘   │     │
│         ▲                                            │     │
│         └────────────────────────────────────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

| 단계 | 설명 | 예시 |
|:-----|:-----|:-----|
| **Red** | 실패하는 테스트 작성 | `test_add()` 작성 → 실행 → 실패 (함수가 없으니까) |
| **Green** | 테스트를 통과하는 최소한의 코드 작성 | `def add(a, b): return a + b` 구현 → 테스트 통과 |
| **Refactor** | 코드 개선 (테스트는 계속 통과해야 함) | 중복 제거, 네이밍 개선, 구조 정리 |

### 1.3 TDD 예시

```python
# 1단계: Red - 실패하는 테스트 작성
def test_calculate_discount_percent():
    """10% 할인이 적용되어야 한다."""
    assert calculate_discount(1000, 10) == 900
# → 실행하면 실패 (calculate_discount 함수가 없음)

# 2단계: Green - 테스트를 통과하는 최소한의 코드
def calculate_discount(price: int, percent: int) -> int:
    return price - (price * percent // 100)
# → 테스트 통과

# 3단계: Refactor - 코드 개선
def calculate_discount(price: int, percent: int) -> int:
    """가격에서 할인율만큼 차감한 금액을 반환."""
    if not 0 <= percent <= 100:
        raise ValueError("할인율은 0~100 사이여야 합니다")
    discount_amount = price * percent // 100
    return price - discount_amount
# → 테스트 여전히 통과, 코드는 더 견고해짐
```

---

## 2. TDD 적용 시나리오

### 2.1 현실적인 TDD

이미 코드가 존재하는 상태에서 테스트를 추가하는 경우에도 TDD 원칙을 적용할 수 있다:

| 상황 | 적용 방법 |
|:-----|:---------|
| **새 기능 추가** | 테스트 먼저 작성 → 기능 구현 → 리팩토링 |
| **버그 수정** | 버그를 재현하는 테스트 작성 → 수정 → 테스트 통과 확인 |
| **기존 코드** | 현재 동작을 검증하는 테스트 작성 (Characterization Test) |

### 2.2 회귀 테스트 (Regression Test)

코드 수정이 **다른 곳에 영향을 주는지** 확인하기 위해 전체 테스트를 실행한다.

```
예시:
1. module_a.py의 parse_data() 수정
2. 이 함수는 module_b.py에서도 사용됨
3. module_b.py를 사용하는 module_c.py에도 영향
4. → 전체 테스트를 돌려야 연쇄적 문제 발견 가능
```

### 2.3 테스트 격리 (Test Isolation)

각 테스트는 **다른 테스트에 영향을 주거나 받지 않아야** 한다.

```python
# Bad: 테스트 간 상태 공유
counter = 0

def test_increment():
    global counter
    counter += 1
    assert counter == 1  # 통과

def test_increment_again():
    global counter
    counter += 1
    assert counter == 1  # 실패! (counter가 이미 1이므로 2가 됨)

# Good: 각 테스트가 독립적
def test_increment():
    counter = 0
    counter += 1
    assert counter == 1

def test_increment_again():
    counter = 0
    counter += 1
    assert counter == 1  # 통과
```

**격리 원칙**:
- 테스트 실행 순서에 의존하지 않아야 함
- 하나의 테스트가 실패해도 다른 테스트에 영향 없음
- 테스트마다 깨끗한 상태에서 시작

---

## 3. 테스트 케이스 설계 기법

### 3.1 경계값 분석 (Boundary Value Analysis)

입력의 **경계에서 오류가 발생하기 쉽다**는 점을 활용한 설계 기법이다.

```python
# 예: 나이가 0~120 사이여야 유효한 경우
def is_valid_age(age: int) -> bool:
    return 0 <= age <= 120

# 경계값 테스트 케이스
def test_age_boundary():
    # 경계 안쪽 (유효)
    assert is_valid_age(0) == True      # 최소 경계
    assert is_valid_age(120) == True    # 최대 경계

    # 경계 바깥 (무효)
    assert is_valid_age(-1) == False    # 최소 경계 -1
    assert is_valid_age(121) == False   # 최대 경계 +1
```

**경계값 선택 가이드**:

| 조건 | 테스트할 값 |
|:-----|:-----------|
| `x >= min` | min-1, min, min+1 |
| `x <= max` | max-1, max, max+1 |
| `min <= x <= max` | min-1, min, max, max+1 |

### 3.2 동등 분할 (Equivalence Partitioning)

입력을 **동일하게 처리되는 그룹**으로 나누고, 각 그룹에서 대표값 하나만 테스트한다.

```python
# 예: 점수에 따른 등급 계산
def get_grade(score: int) -> str:
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    else:
        return 'F'

# 동등 분할 테스트
def test_grade_equivalence_partitions():
    # 각 파티션에서 대표값 하나씩 선택
    assert get_grade(95) == 'A'   # 90-100 파티션
    assert get_grade(85) == 'B'   # 80-89 파티션
    assert get_grade(75) == 'C'   # 70-79 파티션
    assert get_grade(50) == 'F'   # 0-69 파티션
```

**파티션 식별**:
- 유효한 입력 그룹 (정상 케이스)
- 무효한 입력 그룹 (에러 케이스)
- 특수한 입력 그룹 (빈 값, null, 극단값)

### 3.3 테스트 케이스 우선순위

모든 케이스를 테스트할 수 없을 때 우선순위를 정한다:

| 우선순위 | 케이스 유형 | 이유 |
|:---------|:-----------|:-----|
| P0 | 정상 케이스 (Happy Path) | 기본 기능이 동작해야 함 |
| P1 | 경계값 케이스 | 버그가 자주 발생하는 지점 |
| P2 | 에러 케이스 | 예외 상황 처리 검증 |
| P3 | 극단적 케이스 | 빈 입력, 매우 큰 입력 등 |

---

## 4. 테스트 더블 (Test Double)

### 4.1 테스트 더블이란?

**테스트 더블(Test Double)**은 영화 촬영의 **스턴트 더블(Stunt Double)**에서 유래한 용어다.

> 영화에서 위험한 장면을 촬영할 때, 실제 배우 대신 **스턴트 더블**이 대신 연기한다.
> 마찬가지로 테스트에서 실제 객체 대신 **테스트 더블**이 그 역할을 대신한다.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        테스트 더블의 개념                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   실제 시스템                           테스트 환경                       │
│   ┌─────────────┐                      ┌─────────────┐                  │
│   │   내 코드   │                      │   내 코드   │                  │
│   └──────┬──────┘                      └──────┬──────┘                  │
│          │ 호출                               │ 호출                     │
│          ▼                                    ▼                         │
│   ┌─────────────┐                      ┌─────────────┐                  │
│   │  실제 DB    │  ─────────────►      │  Fake DB    │  ← 테스트 더블   │
│   │  실제 API   │      대체            │  Mock API   │                  │
│   │  실제 서버  │                      │  Stub 서버  │                  │
│   └─────────────┘                      └─────────────┘                  │
│                                                                         │
│   • 느림 (네트워크 지연)                • 빠름 (메모리에서 실행)          │
│   • 비용 발생 (API 호출 비용)           • 무료                           │
│   • 불안정 (서버 다운 가능)             • 안정적 (항상 동일하게 동작)      │
│   • 테스트 어려움 (에러 재현 힘듦)       • 테스트 용이 (에러 상황 시뮬레이션)│
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 왜 필요한가?

실제 코드는 다양한 **외부 의존성**에 연결되어 있다:

```python
# 실제 코드 예시
def process_payment(user_id: int, amount: int) -> bool:
    user = database.get_user(user_id)      # 1. 데이터베이스 조회
    result = payment_api.charge(amount)     # 2. 외부 결제 API 호출
    email_service.send_receipt(user.email)  # 3. 이메일 발송
    return result.success
```

이 코드를 테스트하려면?

| 문제 | 설명 |
|:-----|:-----|
| **데이터베이스** | 테스트마다 실제 DB에 연결? 느리고, 테스트 데이터 관리 어려움 |
| **결제 API** | 테스트할 때마다 실제 결제? 돈이 나감! |
| **이메일 서비스** | 테스트마다 실제 이메일 발송? 스팸이 됨 |

**→ 테스트 더블로 이 의존성들을 "가짜"로 대체하면 안전하고 빠르게 테스트 가능**

```python
# 테스트 더블을 사용한 테스트
def test_process_payment():
    # 실제 의존성 대신 테스트 더블 사용
    fake_db = FakeDatabase()                    # Fake: 인메모리 DB
    mock_payment = Mock(return_value=Success()) # Mock: 가짜 결제 API
    stub_email = Mock()                         # Stub: 아무것도 안 하는 이메일

    result = process_payment(user_id=1, amount=1000)

    assert result == True
    mock_payment.charge.assert_called_once()  # 결제 API가 호출되었는지 검증
```

### 4.2 종류

| 종류 | 역할 | 비유 | 사용 시점 |
|:-----|:-----|:-----|:---------|
| **Stub** | 미리 정해진 값을 반환 | "대사만 읽는 대역 배우" | 외부 의존성의 반환값이 필요할 때 |
| **Mock** | 호출 여부/횟수/인자를 검증 | "CCTV로 감시하는 대역" | 특정 메서드가 호출되었는지 확인할 때 |
| **Fake** | 실제와 유사하게 동작하는 간단한 구현 | "진짜처럼 연기하는 대역" | 실제 DB 대신 인메모리 DB 사용 |
| **Spy** | 실제 객체를 감싸서 호출 기록 | "본인이 직접 + 기록 남김" | 실제 동작 + 호출 검증 둘 다 필요할 때 |

```
┌──────────────────────────────────────────────────────────────────────────┐
│                      테스트 더블 종류 비교                                 │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   Stub                              Mock                                 │
│   ┌─────────────────┐               ┌─────────────────┐                  │
│   │ "반환값 고정"    │               │ "호출 감시"      │                  │
│   │                 │               │                 │                  │
│   │ Q: 유저 정보?   │               │ Q: 알림 보냈어? │                  │
│   │ A: {"name":"A"} │               │ A: 네, 1번 호출 │                  │
│   └─────────────────┘               └─────────────────┘                  │
│   → 값만 반환, 검증 X                → 호출 여부/횟수 검증                 │
│                                                                          │
│   Fake                              Spy                                  │
│   ┌─────────────────┐               ┌─────────────────┐                  │
│   │ "간단한 구현체"  │               │ "실제 + 기록"    │                  │
│   │                 │               │                 │                  │
│   │ 실제 DB 대신    │               │ 실제 함수 호출  │                  │
│   │ dict로 저장/조회│               │ + 호출 기록 저장│                  │
│   └─────────────────┘               └─────────────────┘                  │
│   → 동작은 진짜처럼                  → 진짜 실행 + 검증 가능              │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

### 4.3 Stub 예시

```python
from unittest.mock import Mock

def test_user_service_with_stub():
    """
    대상: src/user_service.py - get_user_name()
    의도: 외부 API 호출 없이 사용자 이름 조회 로직 검증
    """
    # Arrange: API 클라이언트를 Stub으로 대체
    mock_api = Mock()
    mock_api.fetch_user.return_value = {"id": 1, "name": "Alice"}

    service = UserService(api_client=mock_api)

    # Act
    name = service.get_user_name(user_id=1)

    # Assert
    assert name == "Alice"
```

### 4.4 Mock 예시

```python
from unittest.mock import Mock

def test_notification_sent():
    """
    대상: src/order_service.py - complete_order()
    의도: 주문 완료 시 알림이 전송되는지 검증
    """
    # Arrange
    mock_notifier = Mock()
    service = OrderService(notifier=mock_notifier)

    # Act
    service.complete_order(order_id=123)

    # Assert: 알림 메서드가 호출되었는지 검증
    mock_notifier.send_notification.assert_called_once_with(
        message="주문 123이 완료되었습니다."
    )
```

### 4.5 언제 테스트 더블을 사용하나?

| 상황 | 사용 여부 | 이유 |
|:-----|:---------|:-----|
| 외부 API 호출 | O | 네트워크 의존성 제거, 비용 절감 |
| 데이터베이스 접근 | O 또는 X | 단위 테스트는 Mock, 통합 테스트는 실제 DB |
| 파일 시스템 접근 | O 또는 X | 임시 파일로 대체 가능 |
| 시간 의존 로직 | O | 현재 시간을 고정하여 테스트 |
| 내부 유틸 함수 | X | 실제 구현 사용 (과도한 Mock 지양) |

**주의**: Mock을 과도하게 사용하면 실제 동작과 테스트가 괴리될 수 있다.

---

## 5. 테스트 유형 선택 가이드

단위/통합/E2E 중 어떤 테스트를 작성해야 할지 모를 때 따르는 지침이다.

### 5.1 선택 플로우차트

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        테스트 유형 선택 플로우차트                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   시작: "무엇을 테스트하려고 하는가?"                                         │
│                     │                                                       │
│                     ▼                                                       │
│   ┌─────────────────────────────────────┐                                   │
│   │ Q1. 테스트 대상이 단일 함수/클래스인가? │                                   │
│   └─────────────────────────────────────┘                                   │
│            │                    │                                           │
│           Yes                  No                                           │
│            │                    │                                           │
│            ▼                    ▼                                           │
│   ┌────────────────┐   ┌─────────────────────────────────┐                  │
│   │ Q2. 외부 의존성 │   │ Q3. UI/사용자 시나리오를 검증하나? │                  │
│   │ 없이 테스트     │   └─────────────────────────────────┘                  │
│   │ 가능한가?      │            │                    │                      │
│   └────────────────┘           Yes                  No                      │
│       │        │                │                    │                      │
│      Yes      No                ▼                    ▼                      │
│       │        │        ┌────────────┐      ┌────────────────┐              │
│       ▼        │        │  E2E 테스트 │      │   통합 테스트   │              │
│ ┌───────────┐  │        └────────────┘      └────────────────┘              │
│ │ 단위 테스트 │  │                                                           │
│ └───────────┘  │                                                            │
│                ▼                                                            │
│   ┌────────────────────────────────────┐                                    │
│   │ 의존성을 Mock으로 대체할 수 있는가? │                                    │
│   └────────────────────────────────────┘                                    │
│            │                    │                                           │
│           Yes                  No                                           │
│            │                    │                                           │
│            ▼                    ▼                                           │
│   ┌───────────────┐    ┌────────────────┐                                   │
│   │ 단위 테스트    │    │   통합 테스트   │                                   │
│   │ (Mock 사용)   │    │ (실제 의존성)  │                                   │
│   └───────────────┘    └────────────────┘                                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.2 핵심 질문 체크리스트

테스트 유형을 결정할 때 아래 질문에 답해보자:

| 질문 | Yes → | No → |
|:-----|:------|:-----|
| 하나의 함수/메서드만 테스트하는가? | 단위 테스트 | 통합 또는 E2E |
| 외부 시스템(DB, API, 파일) 없이 테스트 가능한가? | 단위 테스트 | Mock 사용 또는 통합 테스트 |
| 여러 모듈이 함께 동작해야 검증 가능한가? | 통합 테스트 | 단위 테스트 |
| 실제 사용자 시나리오(클릭, 입력, 화면 전환)를 검증하는가? | E2E 테스트 | 단위 또는 통합 |
| 테스트 실패 시 "어디서 문제인지" 바로 알 수 있는가? | 단위 테스트 | 통합 또는 E2E |

### 5.3 테스트 유형별 특징 비교

| 특징 | 단위 테스트 | 통합 테스트 | E2E 테스트 |
|:-----|:-----------|:-----------|:-----------|
| **테스트 대상** | 함수, 메서드, 클래스 | 모듈 간 연결, 워크플로우 | 전체 시스템, 사용자 시나리오 |
| **실행 속도** | 매우 빠름 (ms) | 보통 (초) | 느림 (수십 초~분) |
| **실패 시 원인 파악** | 쉬움 (정확한 위치) | 보통 | 어려움 (어디서 문제인지 불명확) |
| **외부 의존성** | 없음 (Mock 사용) | 일부 실제 사용 | 전부 실제 사용 |
| **유지보수 비용** | 낮음 | 보통 | 높음 |
| **신뢰도** | 개별 로직 검증 | 연결 검증 | 실제 동작 검증 |

### 5.4 실전 예시로 판단하기

#### 예시 1: "CSV 파일 인코딩 감지 함수"
```
Q1. 단일 함수인가? → Yes
Q2. 외부 의존성 없이 테스트 가능? → Yes (임시 파일로 가능)
→ 단위 테스트
```

#### 예시 2: "사용자가 CSV 업로드 → 전처리 → 시간대 컬럼 생성"
```
Q1. 단일 함수인가? → No (loader → preprocessing 연결)
Q3. UI 시나리오인가? → No (백엔드 로직)
→ 통합 테스트
```

#### 예시 3: "LLM이 사용자 질문을 받아 적절한 도구를 선택하는가?"
```
Q1. 단일 함수인가? → No (chatbot → graph → tools 연결)
Q3. UI 시나리오인가? → No
→ 통합 테스트 (LLM이 올바른 도구를 선택하는 흐름 검증)
```

#### 예시 4: "API Key 입력 → 챗봇 활성화 → 질문 → 응답 표시"
```
Q1. 단일 함수인가? → No
Q3. UI 시나리오인가? → Yes (Streamlit 화면 조작)
→ E2E 테스트
```

### 5.5 애매할 때의 원칙

**"가장 작은 범위로 테스트하라"**

```
단위 테스트로 가능하면 → 단위 테스트
단위 테스트로 불가능하면 → 통합 테스트
통합 테스트로 불가능하면 → E2E 테스트
```

**이유**:
- 작은 범위일수록 실행이 빠르고 유지보수가 쉬움
- 실패 시 원인 파악이 빠름
- 테스트 피라미드(Unit 70% : Integration 25% : E2E 5%) 준수

### 5.6 잘못된 판단 예시

| 상황 | 잘못된 선택 | 올바른 선택 | 이유 |
|:-----|:-----------|:-----------|:-----|
| DB 저장 함수 테스트 | E2E 테스트 | 단위 테스트 (Mock DB) | DB 연결 없이도 로직 검증 가능 |
| 화면 버튼 클릭 동작 | 단위 테스트 | E2E 테스트 | UI 상호작용은 E2E로만 검증 가능 |
| A→B→C 모듈 연결 | 단위 테스트 3개 | 통합 테스트 1개 | 연결 자체를 검증해야 함 |
| 단일 유틸 함수 | 통합 테스트 | 단위 테스트 | 불필요하게 큰 범위 |

---

# Part 2: 단위 테스트 규칙

이 파트는 단위 테스트를 작성할 때 따라야 하는 **구체적인 규칙과 도구 사용법**을 설명한다.

---

## 6. 핵심 개념

### 6.1 Fixture란?

**Fixture**는 테스트 실행 전에 필요한 데이터나 환경을 미리 준비해주는 pytest의 기능이다.

#### 왜 필요한가?

테스트마다 동일한 데이터를 반복해서 만들면 코드 중복이 발생한다:

```python
# Bad: 매 테스트마다 데이터 생성 반복
def test_function_a():
    df = pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})
    result = function_a(df)
    assert result == expected

def test_function_b():
    df = pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})  # 중복!
    result = function_b(df)
    assert result == expected
```

Fixture를 사용하면 한 번 정의하고 여러 테스트에서 재사용할 수 있다:

```python
# Good: conftest.py에 fixture 정의
@pytest.fixture
def sample_df():
    """여러 테스트에서 재사용할 샘플 DataFrame."""
    return pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})

# 테스트 함수에서 fixture 이름을 파라미터로 받으면 자동 주입됨
def test_function_a(sample_df):
    result = function_a(sample_df)
    assert result == expected

def test_function_b(sample_df):  # 같은 fixture 재사용
    result = function_b(sample_df)
    assert result == expected
```

#### Fixture의 동작 원리

1. `conftest.py`에 `@pytest.fixture` 데코레이터가 붙은 함수를 정의
2. 테스트 함수의 파라미터에 fixture 함수 이름을 넣음
3. pytest가 테스트 실행 전에 자동으로 fixture 함수를 호출하여 반환값을 주입

#### Fixture Scope (범위)

Fixture는 생성 빈도를 조절할 수 있다. **Scope**는 "이 fixture를 얼마나 자주 새로 만들 것인가"를 결정한다.

```python
@pytest.fixture(scope="function")  # 기본값: 매 테스트마다 새로 생성
def fresh_data():
    return create_data()

@pytest.fixture(scope="module")  # 모듈(파일)당 한 번만 생성
def expensive_resource():
    return load_heavy_file()

@pytest.fixture(scope="session")  # 전체 테스트 세션당 한 번만 생성
def database_connection():
    return connect_to_db()
```

**Scope별 동작 예시**:

```
pytest tests/ 실행 시 (test_a.py에 3개, test_b.py에 2개 테스트가 있다고 가정)

scope="function" (기본값):
  test_a.py::test_1 → fixture 생성 (1번째)
  test_a.py::test_2 → fixture 생성 (2번째)
  test_a.py::test_3 → fixture 생성 (3번째)
  test_b.py::test_1 → fixture 생성 (4번째)
  test_b.py::test_2 → fixture 생성 (5번째)
  → 총 5번 생성

scope="module":
  test_a.py::test_1 → fixture 생성 (1번째)
  test_a.py::test_2 → 재사용
  test_a.py::test_3 → 재사용
  test_b.py::test_1 → fixture 생성 (2번째, 파일이 바뀜)
  test_b.py::test_2 → 재사용
  → 총 2번 생성

scope="session":
  test_a.py::test_1 → fixture 생성 (1번째)
  test_a.py::test_2 → 재사용
  test_a.py::test_3 → 재사용
  test_b.py::test_1 → 재사용
  test_b.py::test_2 → 재사용
  → 총 1번 생성
```

**언제 어떤 scope를 사용하나?**

| Scope | 생성 횟수 | 사용 사례 |
|:------|:---------|:---------|
| `function` | 매 테스트마다 | 테스트 간 독립성이 중요할 때, 데이터가 변경되는 경우 |
| `module` | 파일당 한 번 | 생성 비용이 크지만 파일 내 공유 가능할 때 |
| `session` | 전체 테스트당 한 번 | 생성 비용이 매우 크고 변경되지 않을 때 |

**주의**: scope가 넓을수록 테스트 간 상태 공유로 인한 부작용이 발생할 수 있음. 기본값 `function`을 권장.

#### Fixture 네이밍 규칙

| 접두사 | 의미 | 예시 |
|:-------|:-----|:-----|
| `sample_*` | 테스트용 샘플 데이터 | `sample_user_df` |
| `valid_*` | 정상 케이스용 데이터 | `valid_config` |
| `invalid_*` | 에러 케이스용 데이터 | `invalid_input` |
| `mock_*` | Mock 객체 | `mock_api_response` |

---

### 6.2 테스트 마킹(Marking)이란?

**테스트 마킹**은 테스트에 라벨(태그)을 붙여서 특정 조건의 테스트만 선택적으로 실행하는 pytest 기능이다.

#### 왜 필요한가?

프로젝트에는 다양한 종류의 테스트가 있다:
- 빠른 단위 테스트 (< 1초)
- 느린 통합 테스트 (> 10초)
- API 호출이 필요한 테스트 (비용 발생)
- 특정 환경에서만 실행 가능한 테스트

마킹을 사용하면 **상황에 따라 원하는 테스트만 실행**할 수 있다.

#### 마킹 정의 및 사용법

**1단계: pyproject.toml에 마커 등록 (선택사항)**

```toml
[tool.pytest.ini_options]
markers = [
    "api: 외부 API 호출이 필요한 테스트",
    "slow: 실행 시간이 긴 테스트 (10초 이상)",
    "integration: 여러 모듈을 연결하는 통합 테스트",
]
```

> **pyproject.toml이란?**
>
> Python 프로젝트의 여러 설정을 한 파일에 모아놓는 표준 설정 파일이다.
> 예전에는 `setup.py`, `pytest.ini`, `requirements.txt` 등 여러 파일에 흩어져 있던 설정을
> `pyproject.toml` 하나에 모을 수 있다.

> **마커 등록은 필수인가?**
>
> **아니오, 선택사항이다.** 등록하지 않아도 `pytest -m api`는 정상 동작한다.
> 다만 등록하지 않으면 pytest 실행 시 경고가 뜬다.
> 등록하면 경고가 뜨지 않고, `pytest --markers`로 사용 가능한 마커 목록을 확인할 수 있다.

**2단계: 테스트에 마커 적용**
```python
import pytest

@pytest.mark.api
def test_external_api_call():
    """API 호출이 필요한 테스트."""
    ...

@pytest.mark.slow
def test_large_dataset_processing():
    """대용량 데이터 처리 테스트."""
    ...

@pytest.mark.api
@pytest.mark.slow
def test_streaming_large_response():
    """마커는 여러 개 붙일 수 있음."""
    ...
```

**3단계: 마커로 테스트 필터링 실행**
```bash
# api 마커가 붙은 테스트만 실행
pytest -m api

# api 마커가 붙지 않은 테스트만 실행
pytest -m "not api"

# api 또는 slow 마커가 붙은 테스트 실행
pytest -m "api or slow"

# api이면서 slow인 테스트만 실행
pytest -m "api and slow"
```

---

### 6.3 테스트 커버리지(Coverage)란?

**커버리지**는 테스트가 소스 코드의 얼마나 많은 부분을 실행했는지 측정하는 지표다.

#### 커버리지 종류

```python
# 예시 함수
def calculate_grade(score):          # Line 1
    if score >= 90:                   # Line 2 (분기 A)
        return 'A'                    # Line 3
    elif score >= 80:                 # Line 4 (분기 B)
        return 'B'                    # Line 5
    else:                             # Line 6 (분기 C)
        return 'C'                    # Line 7
```

| 커버리지 종류 | 측정 대상 | 설명 |
|:-------------|:---------|:-----|
| **Line Coverage** | 실행된 라인 수 / 전체 라인 수 | 가장 기본적인 지표 |
| **Branch Coverage** | 실행된 분기 수 / 전체 분기 수 | if/else 모든 경로 테스트 여부 |
| **Function Coverage** | 호출된 함수 수 / 전체 함수 수 | 함수 단위 테스트 여부 |

#### 커버리지 측정 방법

```bash
# 기본 커버리지 측정
pytest --cov=src

# HTML 리포트 생성 (브라우저에서 확인 가능)
pytest --cov=src --cov-report=html
# → htmlcov/index.html 파일 생성됨

# 터미널에 상세 출력
pytest --cov=src --cov-report=term-missing
```

#### 커버리지 리포트 읽는 법

```
Name                      Stmts   Miss  Cover   Missing
-------------------------------------------------------
src/module_a.py              45      5    89%   23-25, 40-41
src/module_b.py              80     20    75%   45-50, 67-80
-------------------------------------------------------
TOTAL                       125     25    80%
```

| 컬럼 | 의미 |
|:-----|:-----|
| Stmts | 전체 실행 가능한 문장(statement) 수 |
| Miss | 테스트에서 실행되지 않은 문장 수 |
| Cover | 커버리지 비율 (%) |
| Missing | 실행되지 않은 라인 번호 |

#### 주의사항

- **100% 커버리지 ≠ 버그 없음**: 커버리지는 "실행 여부"만 측정하지, "올바른 결과"는 검증하지 않음
- **커버리지 숫자에 집착하지 말 것**: 의미 있는 테스트가 더 중요
- **핵심 로직 우선**: 모든 코드를 동일하게 테스트할 필요 없음

---

## 7. 테스트 작성 규칙

### 7.1 양방향 추적성 (Bidirectional Traceability)

테스트와 소스 코드 간에 **양방향으로 참조**가 가능해야 한다.

#### 테스트 → 소스 코드 (테스트 파일에 명시)

```python
# tests/test_calculator.py
def test_add_positive_numbers():
    """
    대상: src/calculator.py:45 - add()
    의도: 양수 두 개를 더했을 때 올바른 결과 반환 검증
    """
```

#### 소스 코드 → 테스트 (소스 파일에 주석)

```python
# src/calculator.py
def add(a: int, b: int) -> int:
    """두 숫자를 더한 결과를 반환.

    # Test: tests/test_calculator.py::TestAdd
    """
    return a + b
```

**형식**:
- 테스트 docstring: `대상: {파일경로}:{라인번호} - {함수명}()`
- 소스 주석: `# Test: tests/{테스트파일}::{클래스명 또는 함수명}`

---

### 7.2 의도 명시 (Docstring)

모든 테스트 함수에는 **반드시 docstring**을 작성하여 테스트의 목적을 명확히 한다.

**필수 포함 항목**:
1. **대상**: 테스트 대상 파일 및 함수
2. **의도**: 무엇을 검증하는지

**선택 포함 항목**:
- 테스트 케이스 ID (예: TC1, TC2)
- 경계값 설명
- 관련 요구사항 ID (예: FR-009)

```python
def test_discount_boundary_value():
    """
    대상: src/pricing.py:12 - calculate_discount()
    의도: 할인율 경계값(0%, 100%) 입력 시 올바른 결과 반환 검증

    TC1: 0% 할인 → 원가 그대로
    TC2: 100% 할인 → 0원
    """
```

---

### 7.3 AAA 패턴 (Arrange-Act-Assert)

모든 테스트는 **AAA 패턴**을 따라 구조화한다.

```python
def test_filter_list_by_condition():
    """
    대상: src/utils.py:234 - filter_list()
    의도: 조건에 맞는 항목만 필터링되는지 검증
    """
    # Arrange: 테스트 데이터 및 환경 준비
    items = [1, 2, 3, 4, 5]
    threshold = 3

    # Act: 테스트 대상 함수 실행
    result = filter_list(items, lambda x: x >= threshold)

    # Assert: 결과 검증
    assert result == [3, 4, 5]
```

| 섹션 | 역할 | 예시 |
|:-----|:-----|:-----|
| **Arrange** | 테스트에 필요한 데이터, 객체, 환경 준비 | 데이터 생성, fixture 주입 |
| **Act** | 테스트 대상 함수/메서드 실행 | `result = func(args)` |
| **Assert** | 결과 검증 | `assert result == expected` |

---

### 7.4 에러 케이스 문서화

테스트에서 **의도적으로 발생시키는 실패나 오류**(예: 잘못된 입력, 예외 상황)는 별도 문서에 기록한다.

```python
def test_divide_by_zero():
    """
    대상: src/calculator.py:78 - divide()
    의도: 0으로 나눌 때 ZeroDivisionError 발생 검증

    에러 케이스: tests/error_explanation.md#ERR-CALC-001
    """
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
```

---

## 8. 테스트 구조 규칙

### 8.1 네이밍 규칙

**파일**: `test_{모듈명}.py`

**함수**: `test_{함수명}_{시나리오}`
- `test_add_positive_numbers`
- `test_parse_invalid_input`
- `test_filter_empty_result`

**클래스**: `Test{함수명PascalCase}`
- `TestAdd`
- `TestParse`

### 8.2 테스트 클래스 구성

관련 테스트는 **클래스로 그룹화**하여 가독성을 높인다.

```python
class TestCalculateDiscount:
    """
    대상: src/pricing.py:12 - calculate_discount()
    """

    def test_zero_percent(self):
        """의도: 0% 할인 시 원가 반환 검증."""
        assert calculate_discount(1000, 0) == 1000

    def test_fifty_percent(self):
        """의도: 50% 할인 검증."""
        assert calculate_discount(1000, 50) == 500

    def test_hundred_percent(self):
        """의도: 100% 할인 시 0원 반환 검증."""
        assert calculate_discount(1000, 100) == 0
```

---

## 9. 단위 테스트 체크리스트

새 테스트 작성 시 다음 항목을 확인한다:

- [ ] docstring에 **대상**(파일:라인 - 함수명)이 명시되어 있는가?
- [ ] docstring에 **의도**(무엇을 검증하는지)가 명시되어 있는가?
- [ ] 소스 코드에 **테스트 위치 주석**(`# Test: ...`)이 추가되었는가?
- [ ] **AAA 패턴**(Arrange-Act-Assert)을 따르고 있는가?
- [ ] 재사용 데이터는 **fixture**로 분리되어 있는가?
- [ ] 함수명이 `test_{함수명}_{시나리오}` 형식인가?
- [ ] 의도된 에러/예외 테스트는 별도 문서에 기록되었는가?

---

# Part 3: 통합 테스트 규칙

이 파트는 여러 모듈이 함께 동작하는 **통합 테스트**를 작성할 때 따라야 하는 규칙을 설명한다.

---

## 10. 통합 테스트란?

### 10.1 단위 테스트 vs 통합 테스트

| 구분 | 단위 테스트 (Unit Test) | 통합 테스트 (Integration Test) |
|:-----|:----------------------|:-----------------------------|
| **범위** | 함수/메서드 하나 | 여러 모듈/컴포넌트 조합 |
| **목적** | 개별 함수가 올바르게 동작하는지 | 모듈 간 연결이 올바른지 |
| **의존성** | 격리 (필요시 Mock) | 실제 의존성 사용 |
| **속도** | 빠름 (< 1초) | 느림 (수 초 ~ 수십 초) |
| **실패 원인** | 함수 로직 오류 | 인터페이스 불일치, 데이터 흐름 오류 |

```
단위 테스트:
┌─────────────┐
│  함수 A     │  ← 이것만 테스트
└─────────────┘

통합 테스트:
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  함수 A     │ ──► │  함수 B     │ ──► │  함수 C     │
└─────────────┘     └─────────────┘     └─────────────┘
       ↑                                       ↑
       └───────── 이 전체 흐름을 테스트 ─────────┘
```

### 10.2 왜 통합 테스트가 필요한가?

단위 테스트만으로는 발견할 수 없는 문제들이 있다:

```python
# 예시: 두 함수가 각각은 잘 동작하지만, 함께 사용하면 문제 발생

# module_a.py
def parse_data(raw: str) -> dict:
    """JSON 문자열을 파싱."""
    return json.loads(raw)  # {'name': 'Alice'} 반환

# module_b.py
def process_user(data: dict) -> str:
    """사용자 데이터 처리."""
    return data['username']  # 'username' 키를 기대하지만 'name'이 옴!

# 단위 테스트: 각각 통과
# 통합 테스트: 실제로 연결하면 KeyError 발생
```

**통합 테스트가 잡아내는 문제**:
- 모듈 간 인터페이스 불일치 (키 이름, 데이터 타입)
- 데이터 흐름에서 발생하는 결측값, 형변환 오류
- 순서 의존성 (A가 B보다 먼저 실행되어야 하는 경우)
- 실제 환경에서의 성능 문제

---

## 11. 통합 테스트 대상 선정 기준

모든 모듈 조합을 테스트할 필요는 없다. **다음 기준**에 해당하는 경우 통합 테스트를 작성한다:

| 기준 | 예시 |
|:-----|:-----|
| **핵심 데이터 파이프라인** | 파일 로드 → 전처리 → 분석 |
| **여러 모듈을 거치는 워크플로우** | 사용자 입력 → 처리 → 출력 |
| **외부 시스템 연동** | API 호출 + 응답 파싱 |
| **사용자 시나리오** | 실제 사용 흐름 전체 |

---

## 12. 통합 테스트 작성 규칙

### 12.1 파일 구조

통합 테스트는 **별도 디렉토리**로 분리한다:

```
tests/
├── conftest.py                    # 공통 fixture
├── test_module_a.py               # 단위 테스트
├── test_module_b.py               # 단위 테스트
│
├── integration/                   # 통합 테스트 디렉토리
│   ├── conftest.py               # 통합 테스트 전용 fixture
│   ├── test_data_pipeline.py     # 데이터 파이프라인 통합
│   └── test_api_workflow.py      # API 워크플로우 통합
```

### 12.2 네이밍 규칙

**파일명**: `test_{워크플로우명}.py`
- `test_data_pipeline.py`
- `test_user_workflow.py`

**함수명**: `test_{시작모듈}_to_{끝모듈}_{시나리오}`
- `test_parser_to_processor_valid_input`
- `test_api_to_storage_success`

**클래스명**: `TestIntegration{워크플로우명}`
- `TestIntegrationDataPipeline`
- `TestIntegrationUserWorkflow`

### 12.3 마킹

모든 통합 테스트에는 `@pytest.mark.integration` 마커를 붙인다:

```python
import pytest

@pytest.mark.integration
def test_parser_to_processor_pipeline():
    """통합: 파서 출력이 프로세서 입력으로 정상 전달되는지 검증."""
    ...
```

### 12.4 Docstring 형식

통합 테스트의 docstring은 **흐름 전체**를 설명한다:

```python
@pytest.mark.integration
def test_file_to_report_pipeline(sample_file_path):
    """
    통합 테스트 ID: INT-001
    대상 흐름: loader.py → processor.py → reporter.py

    검증 내용:
    1. 파일을 정상적으로 로드
    2. 데이터 처리가 올바르게 수행됨
    3. 리포트가 정상 생성됨

    시나리오: 사용자가 파일을 업로드하고 리포트를 요청
    """
```

---

## 13. 단위 테스트 vs 통합 테스트 선택 가이드

| 상황 | 작성할 테스트 | 이유 |
|:-----|:------------|:-----|
| 새 유틸리티 함수 추가 | 단위 테스트 | 함수 로직만 검증하면 됨 |
| 기존 함수 버그 수정 | 단위 테스트 | 해당 함수만 검증 |
| 새 데이터 흐름 추가 | 단위 + 통합 | 개별 함수 + 연결 모두 검증 |
| 외부 API 연동 기능 | 통합 테스트 | 실제 호출 흐름 검증 필요 |
| 사용자 시나리오 검증 | 통합 테스트 | 전체 워크플로우 검증 |

### 테스트 피라미드

```
                    ┌───────┐
                    │  E2E  │  ← 최소한으로 (수동 또는 자동화)
                   ─┴───────┴─
                  ┌───────────┐
                  │   통합    │  ← 핵심 워크플로우만
                 ─┴───────────┴─
                ┌───────────────┐
                │    단위       │  ← 대부분의 테스트
                └───────────────┘
```

**권장 비율**: 단위 테스트 70% : 통합 테스트 25% : E2E 5%

---

## 14. 통합 테스트 체크리스트

새 통합 테스트 작성 시 다음 항목을 확인한다:

- [ ] `@pytest.mark.integration` 마커가 붙어 있는가?
- [ ] docstring에 **통합 테스트 ID** (INT-XXX)가 명시되어 있는가?
- [ ] docstring에 **대상 흐름** (모듈 → 모듈)이 명시되어 있는가?
- [ ] docstring에 **검증 내용**이 단계별로 명시되어 있는가?
- [ ] `tests/integration/` 디렉토리에 위치해 있는가?
- [ ] 파일명이 `test_{워크플로우명}.py` 형식인가?
- [ ] 테스트 간 독립성이 보장되는가? (다른 테스트에 영향 없음)

---

# Part 4: E2E 테스트 규칙

이 파트는 **사용자 관점에서 전체 시스템**을 검증하는 E2E(End-to-End) 테스트 작성 규칙을 설명한다.

---

## 15. E2E 테스트란?

### 15.1 테스트 레벨 비교

| 구분 | 단위 테스트 | 통합 테스트 | E2E 테스트 |
|:-----|:-----------|:-----------|:----------|
| **범위** | 함수 하나 | 모듈 간 연결 | 전체 시스템 |
| **관점** | 개발자 | 개발자 | 사용자 |
| **검증 대상** | 함수 로직 | 모듈 인터페이스 | 사용자 시나리오 |
| **실행 환경** | 격리된 환경 | 부분적 실제 환경 | 실제와 동일한 환경 |
| **속도** | 매우 빠름 | 보통 | 느림 |
| **비용** | 낮음 | 보통 | 높음 |

```
┌──────────────────────────────────────────────────────────────────┐
│                         E2E 테스트                                │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                      통합 테스트                          │   │
│  │  ┌────────────────────────────────────────────────────┐ │   │
│  │  │                   단위 테스트                       │ │   │
│  │  │                                                    │ │   │
│  │  │   함수 A    함수 B    함수 C    함수 D            │ │   │
│  │  └────────────────────────────────────────────────────┘ │   │
│  │                                                          │   │
│  │          모듈 간 연결, 데이터 흐름                        │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│   UI, API, DB, 외부 서비스 등 전체 시스템을 사용자 관점에서 검증   │
└──────────────────────────────────────────────────────────────────┘
```

### 15.2 왜 E2E 테스트가 필요한가?

단위 테스트와 통합 테스트만으로는 발견할 수 없는 문제들이 있다:

- **UI 렌더링 문제**: 데이터는 올바르지만 화면에 잘못 표시됨
- **사용자 플로우 오류**: 개별 기능은 동작하지만 순서대로 사용하면 실패
- **환경 설정 문제**: 로컬에서는 동작하지만 배포 환경에서 실패
- **전체 성능 문제**: 개별 모듈은 빠르지만 조합하면 느려짐

### 15.3 E2E 테스트의 특징

**장점**:
- 실제 사용자 경험을 검증
- 통합 환경에서의 문제 발견
- 회귀 방지에 효과적

**단점**:
- 실행 시간이 오래 걸림
- 설정 및 유지보수 비용이 높음
- 실패 원인 파악이 어려움 (어디서 문제인지 모호)
- 불안정할 수 있음 (Flaky Test)

---

## 16. E2E 테스트 대상 선정 기준

E2E 테스트는 비용이 높으므로 **핵심 사용자 시나리오만** 선별한다.

### 16.1 테스트 대상 기준

| 기준 | 예시 | 우선순위 |
|:-----|:-----|:---------|
| **핵심 비즈니스 흐름** | 회원가입 → 로그인 → 주문 | P0 |
| **수익에 영향을 주는 기능** | 결제 프로세스 | P0 |
| **사용 빈도가 높은 기능** | 메인 페이지 로드, 검색 | P1 |
| **과거에 장애가 발생한 기능** | 이전에 버그가 있던 플로우 | P1 |
| **복잡한 사용자 플로우** | 여러 단계를 거치는 프로세스 | P2 |

### 16.2 테스트하지 않아도 되는 것

- 단위 테스트로 충분히 검증 가능한 로직
- 거의 사용되지 않는 기능
- 외부 서비스 장애 시나리오 (Mock으로 대체)

---

## 17. E2E 테스트 방법

### 17.1 자동화 E2E vs 수동 E2E

| 구분 | 자동화 E2E | 수동 E2E |
|:-----|:----------|:---------|
| **도구** | Selenium, Playwright, Cypress | 사람이 직접 실행 |
| **비용** | 초기 설정 비용 높음, 유지보수 필요 | 매번 시간 소요 |
| **적합한 경우** | CI/CD에서 반복 실행 | 탐색적 테스트, UI 변경이 잦을 때 |
| **장점** | 일관된 반복 실행 | 유연한 탐색, 즉각적 피드백 |
| **단점** | UI 변경 시 테스트 수정 필요 | 시간 소요, 일관성 부족 |

### 17.2 자동화 E2E 테스트 구조

```python
# tests/e2e/test_user_journey.py
import pytest
from playwright.sync_api import Page

@pytest.mark.e2e
class TestUserJourney:
    """
    E2E: 사용자 여정 테스트
    시나리오: 신규 사용자가 가입 후 첫 주문을 완료한다
    """

    def test_signup_to_first_order(self, page: Page):
        """
        E2E 테스트 ID: E2E-001
        시나리오: 회원가입 → 로그인 → 상품 검색 → 장바구니 → 주문

        검증 단계:
        1. 회원가입 폼 입력 및 제출
        2. 로그인 성공 확인
        3. 상품 검색 및 선택
        4. 장바구니 추가
        5. 주문 완료 메시지 확인
        """
        # 1. 회원가입
        page.goto("/signup")
        page.fill("#email", "test@example.com")
        page.fill("#password", "password123")
        page.click("#submit")

        # 2. 로그인 확인
        assert page.locator("#welcome-message").is_visible()

        # 3. 상품 검색
        page.fill("#search", "테스트 상품")
        page.click("#search-button")

        # 4. 장바구니 추가
        page.click("#add-to-cart")

        # 5. 주문 완료
        page.click("#checkout")
        page.click("#confirm-order")
        assert page.locator("#order-success").is_visible()
```

### 17.3 수동 E2E 테스트 체크리스트

자동화가 어렵거나 비용 대비 효과가 낮은 경우 수동 테스트를 진행한다.

```markdown
## 수동 E2E 테스트 체크리스트

### E2E-001: 신규 사용자 가입 및 첫 주문

**사전 조건**:
- 테스트 환경에 접속 가능
- 테스트용 이메일 준비

**테스트 단계**:
- [ ] 1. /signup 페이지 접속
- [ ] 2. 이메일, 비밀번호 입력 후 가입 버튼 클릭
- [ ] 3. 환영 메시지 표시 확인
- [ ] 4. 상품 검색 후 결과 표시 확인
- [ ] 5. 장바구니 추가 후 수량 표시 확인
- [ ] 6. 주문 완료 후 성공 메시지 확인

**예상 결과**: 주문 완료 페이지에 "주문이 완료되었습니다" 메시지 표시

**테스트 일자**: ____
**테스트 결과**: [ ] 통과 / [ ] 실패
**실패 시 내용**: ____________________
```

---

## 18. E2E 테스트 작성 규칙

### 18.1 파일 구조

```
tests/
├── conftest.py
├── test_unit_*.py           # 단위 테스트
├── integration/             # 통합 테스트
│
└── e2e/                     # E2E 테스트
    ├── conftest.py          # E2E 전용 fixture (브라우저 설정 등)
    ├── test_user_journey.py # 사용자 여정 테스트
    ├── test_admin_flow.py   # 관리자 플로우 테스트
    └── manual/              # 수동 테스트 체크리스트
        └── checklist.md
```

### 18.2 네이밍 규칙

**파일명**: `test_{사용자유형}_{시나리오}.py`
- `test_user_journey.py`
- `test_admin_dashboard.py`

**함수명**: `test_{시나리오}_{결과}`
- `test_signup_to_first_order_success`
- `test_checkout_with_invalid_card_shows_error`

**클래스명**: `TestE2E{시나리오}`
- `TestE2EUserJourney`
- `TestE2EAdminFlow`

### 18.3 마킹

```python
import pytest

@pytest.mark.e2e
def test_user_login_flow():
    """E2E: 사용자 로그인 플로우"""
    ...

@pytest.mark.e2e
@pytest.mark.slow
def test_full_order_process():
    """E2E: 전체 주문 프로세스 (느림)"""
    ...
```

### 18.4 Docstring 형식

```python
@pytest.mark.e2e
def test_data_upload_to_visualization(page: Page):
    """
    E2E 테스트 ID: E2E-002
    시나리오: 데이터 업로드 → 전처리 → 시각화 확인

    검증 단계:
    1. CSV 파일 업로드
    2. 전처리 완료 메시지 확인
    3. 차트 렌더링 확인
    4. 지도 시각화 확인

    사전 조건:
    - 테스트용 CSV 파일 (test_data.csv)

    예상 결과:
    - 차트와 지도가 정상적으로 렌더링됨
    """
```

---

## 19. E2E 테스트 실행

### 19.1 실행 명령어

```bash
# E2E 테스트만 실행
pytest tests/e2e/ -v

# 마커로 필터링
pytest -m e2e -v

# 헤드리스 모드로 실행 (CI용)
pytest tests/e2e/ --headless -v

# E2E 제외하고 실행 (빠른 피드백)
pytest tests/ --ignore=tests/e2e/ -v
```

### 19.2 CI/CD에서의 E2E 테스트

E2E 테스트는 비용이 높으므로 **조건부 실행**을 권장한다:

```yaml
# .github/workflows/test.yml
jobs:
  unit-test:
    runs-on: ubuntu-latest
    steps:
      - name: Run unit and integration tests
        run: pytest tests/ --ignore=tests/e2e/ -v

  e2e-test:
    runs-on: ubuntu-latest
    # main 브랜치 또는 release 태그에서만 실행
    if: github.ref == 'refs/heads/main' || startsWith(github.ref, 'refs/tags/')
    steps:
      - name: Run E2E tests
        run: pytest tests/e2e/ -v --headless
```

---

## 20. 테스트 레벨별 권장 비율

```
                    ┌───────┐
                    │  E2E  │  ← 5-10% (핵심 시나리오만)
                   ─┴───────┴─
                  ┌───────────┐
                  │   통합    │  ← 20-25% (주요 워크플로우)
                 ─┴───────────┴─
                ┌───────────────┐
                │    단위       │  ← 70% (대부분의 테스트)
                └───────────────┘
```

| 테스트 레벨 | 비율 | 실행 시점 | 목적 |
|:-----------|:----|:---------|:-----|
| 단위 테스트 | 70% | 모든 commit, PR | 빠른 피드백 |
| 통합 테스트 | 20-25% | PR, merge | 모듈 연결 검증 |
| E2E 테스트 | 5-10% | merge, release | 사용자 시나리오 검증 |

---

## 21. E2E 테스트 체크리스트

새 E2E 테스트 작성 시 다음 항목을 확인한다:

- [ ] `@pytest.mark.e2e` 마커가 붙어 있는가?
- [ ] docstring에 **E2E 테스트 ID** (E2E-XXX)가 명시되어 있는가?
- [ ] docstring에 **시나리오**가 사용자 관점으로 작성되어 있는가?
- [ ] docstring에 **검증 단계**가 순서대로 명시되어 있는가?
- [ ] docstring에 **사전 조건**과 **예상 결과**가 명시되어 있는가?
- [ ] `tests/e2e/` 디렉토리에 위치해 있는가?
- [ ] 테스트가 **독립적으로 실행 가능**한가? (다른 테스트에 의존하지 않음)
- [ ] 테스트 실패 시 **원인 파악이 용이**하도록 단계별 assertion이 있는가?

---
