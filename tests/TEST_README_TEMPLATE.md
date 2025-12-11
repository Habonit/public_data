# 테스트 실행 가이드 (템플릿)

이 문서는 **{프로젝트명}**의 테스트를 실행하고 활용하는 방법을 설명한다.

> **방법론 참고**: 테스트 작성 원칙과 규칙은 [principle.md](./principle.md) 참조

---

## 목차

1. [왜 TDD가 필요한가?](#1-왜-tdd가-필요한가)
2. [테스트 범위](#2-테스트-범위)
3. [테스트 실행 방법](#3-테스트-실행-방법)
4. [개발 워크플로우](#4-개발-워크플로우)
5. [CI/CD 연동](#5-cicd-연동)
6. [디렉토리 구조](#6-디렉토리-구조)
7. [Fixture 목록](#7-fixture-목록)
8. [FAQ](#8-faq)

---

## 1. 왜 TDD가 필요한가?

이 프로젝트에서 TDD가 중요한 이유:

### 1.1 {핵심 이유 1}

```
{프로젝트의 핵심 데이터 흐름 또는 파이프라인}
```

{구체적인 이유 설명}

**→ 테스트로 {무엇}의 정확성을 보장**

### 1.2 {핵심 이유 2}

{이유 설명}

**→ {테스트로 얻는 이점}**

### 1.3 안전한 리팩토링

코드 수정 시:
- "이거 고치면 다른 데 영향 없겠지?" 걱정 없이 수정
- 테스트가 통과하면 기존 기능이 정상 동작함을 확인

---

## 2. 테스트 범위

### 2.1 단위 테스트 (Unit Test)

개별 함수의 정확성을 검증한다. 각 모듈별 테스트 대상 함수와 우선순위는 다음과 같다.

---

#### 2.1.1 `{소스경로}/{모듈명}.py` (P0)

| 함수 | 설명 | 테스트 케이스 |
|:-----|:-----|:-------------|
| `{함수명}({파라미터})` | {함수 설명} | {테스트 케이스 예시} |
| `{함수명}({파라미터})` | {함수 설명} | {테스트 케이스 예시} |

---

#### 2.1.2 `{소스경로}/{모듈명}.py` (P0)

| 함수 | 설명 | 테스트 케이스 |
|:-----|:-----|:-------------|
| `{함수명}({파라미터})` | {함수 설명} | {테스트 케이스 예시} |

---

<!-- 필요한 만큼 모듈 섹션 추가 -->

#### 2.1.N `{소스경로}/{모듈명}.py` (테스트 불필요)

{테스트가 불필요한 이유 설명}

---

### 2.2 통합 테스트 (Integration Test)

여러 모듈이 함께 동작하는 흐름을 검증한다. 단위 테스트로는 검증할 수 없는 **모듈 간 연결**을 테스트한다.

---

#### 2.2.1 통합 테스트 목록

| ID | 흐름 | 관련 모듈 | 검증 내용 |
|:---|:-----|:---------|:---------|
| INT-001 | {흐름 설명} | {모듈A} → {모듈B} | {검증 내용} |
| INT-002 | {흐름 설명} | {모듈B} → {모듈C} | {검증 내용} |

---

#### 2.2.2 통합 테스트 상세

##### INT-001: {흐름 제목}

```
{모듈A.함수}() → {모듈B.함수}()
```

| 테스트 케이스 | 검증 내용 |
|:-------------|:---------|
| {케이스 설명} | {검증 내용} |
| {케이스 설명} | {검증 내용} |

##### INT-002: {흐름 제목}

```
{모듈B.함수}() → {모듈C.함수}()
```

| 테스트 케이스 | 검증 내용 |
|:-------------|:---------|
| {케이스 설명} | {검증 내용} |

---

### 2.3 E2E 테스트 (End-to-End)

전체 사용자 시나리오를 검증한다.

| 시나리오 | 검증 방법 |
|:---------|:---------|
| {시나리오 설명} | {자동화/수동} |
| {시나리오 설명} | {자동화/수동} |

---

## 3. 테스트 실행 방법

### 3.1 전체 테스트 실행

```bash
# {특정 마커} 테스트 제외
{패키지 매니저} run pytest tests/ -m "not {마커}" -v

# 전체 테스트
{패키지 매니저} run pytest tests/ -v
```

### 3.2 특정 테스트만 실행

```bash
# 특정 파일
{패키지 매니저} run pytest tests/test_{모듈명}.py -v

# 특정 함수
{패키지 매니저} run pytest tests/test_{모듈명}.py::test_{함수명}_{시나리오} -v

# 특정 클래스
{패키지 매니저} run pytest tests/test_{모듈명}.py::Test{클래스명} -v
```

### 3.3 마커로 필터링

```bash
# {마커} 테스트만
{패키지 매니저} run pytest -m {마커} -v

# 통합 테스트만
{패키지 매니저} run pytest -m integration -v

# 느린 테스트 제외
{패키지 매니저} run pytest -m "not slow" -v
```

### 3.4 커버리지 측정

```bash
# 터미널 출력
{패키지 매니저} run pytest tests/ --cov={소스디렉토리} --cov-report=term-missing

# HTML 리포트 생성
{패키지 매니저} run pytest tests/ --cov={소스디렉토리} --cov-report=html
# → htmlcov/index.html 열어서 확인
```

---

## 4. 개발 워크플로우

### 4.1 새 기능 개발 시 (TDD)

```
1. 테스트 먼저 작성
   └─► tests/test_xxx.py에 실패하는 테스트 작성

2. 최소한의 구현
   └─► 테스트가 통과하도록 코드 작성

3. 리팩토링
   └─► 코드 개선 (테스트는 계속 통과해야 함)

4. 로컬 테스트 실행
   └─► {패키지 매니저} run pytest tests/test_xxx.py -v
```

### 4.2 버그 수정 시

```
1. 버그 재현 테스트 작성
   └─► 버그를 발생시키는 테스트 케이스 작성

2. 테스트 실패 확인
   └─► 테스트가 실패하는지 확인 (버그 재현)

3. 버그 수정
   └─► 코드 수정

4. 테스트 통과 확인
   └─► 수정 후 테스트 통과 확인
```

### 4.3 Commit 전 체크리스트

```bash
# 1. 관련 테스트 실행
{패키지 매니저} run pytest tests/test_xxx.py -v

# 2. 전체 테스트 실행 (권장)
{패키지 매니저} run pytest tests/ -m "not {제외할 마커}" -v

# 3. 테스트 통과 확인 후 commit
git add .
git commit -m "feat: xxx 기능 추가"
```

### 4.4 Push 전 체크리스트

```bash
# 1. 전체 테스트 실행 (모든 마커 포함)
{환경변수 설정 명령}
{패키지 매니저} run pytest tests/ -v

# 2. 커버리지 확인 (선택)
{패키지 매니저} run pytest tests/ --cov={소스디렉토리}

# 3. 모든 테스트 통과 후 push
git push origin {브랜치명}
```

---

## 5. CI/CD 연동

### 5.1 GitHub Actions 워크플로우

PR 생성 시 자동으로 테스트가 실행된다:

```yaml
# .github/workflows/test.yml
name: Test

on:
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: {패키지 매니저 setup action}

      - name: Run unit tests (without {마커})
        run: {패키지 매니저} run pytest tests/ --ignore=tests/integration/ -m "not {마커}" --cov={소스디렉토리}

      - name: Run integration tests (without {마커})
        run: {패키지 매니저} run pytest tests/integration/ -m "not {마커}"

      - name: Run {마커} tests
        env:
          {환경변수명}: ${{ secrets.{시크릿명} }}
        run: {패키지 매니저} run pytest -m {마커}
```

### 5.2 머지 규칙

- **모든 테스트 통과** 필수
- {추가 규칙}
- 테스트 실패 시 PR 머지 불가

### 5.3 왜 PR마다 전체 테스트를 실행하나?

**회귀 테스트(Regression Test)** 때문이다.

```
예시:
1. {모듈A}의 {함수}() 수정
2. 이 함수는 {모듈B}에서도 사용됨
3. {모듈B}를 사용하는 {모듈C}에도 영향
4. → {모듈A}만 테스트하면 {모듈C}의 문제를 발견 못함
5. → 전체 테스트를 돌려야 연쇄적인 문제 발견 가능
```

---

## 6. 디렉토리 구조

```
tests/
├── conftest.py                 # 공통 fixture 정의
├── principle.md                # 테스트 원칙 및 방법론 (추상적)
├── README.md                   # 본 문서 (실천적 가이드)
├── error_explanation.md        # 에러 케이스 설명
│
├── test_{모듈1}.py             # {소스경로}/{모듈1}.py 테스트
├── test_{모듈2}.py             # {소스경로}/{모듈2}.py 테스트
├── test_{모듈3}.py             # {소스경로}/{모듈3}.py 테스트
│
└── integration/                # 통합 테스트
    ├── conftest.py             # 통합 테스트 전용 fixture
    ├── test_{워크플로우1}.py   # INT-001, INT-002
    └── test_{워크플로우2}.py   # INT-003
```

---

## 7. Fixture 목록

### 7.1 공통 Fixture (conftest.py)

| Fixture | Scope | 설명 |
|:--------|:------|:-----|
| `{fixture명}` | function | {설명} |
| `{fixture명}` | module | {설명} |
| `{fixture명}` | session | {설명} |

### 7.2 통합 테스트 Fixture (integration/conftest.py)

| Fixture | Scope | 설명 |
|:--------|:------|:-----|
| `{fixture명}` | module | {설명} |
| `{fixture명}` | module | {설명} |

---

## 8. FAQ

### Q: {마커} 테스트 없이 테스트할 수 있나요?

네, `-m "not {마커}"` 옵션으로 해당 테스트를 제외하고 실행할 수 있습니다:

```bash
{패키지 매니저} run pytest tests/ -m "not {마커}" -v
```

### Q: 테스트가 너무 느린데요?

느린 테스트에는 `@pytest.mark.slow` 마커를 붙이고, 제외하고 실행할 수 있습니다:

```bash
{패키지 매니저} run pytest tests/ -m "not slow" -v
```

### Q: 새 테스트 파일은 어디에 만드나요?

- 단위 테스트: `tests/test_{모듈명}.py`
- 통합 테스트: `tests/integration/test_{워크플로우명}.py`

### Q: conftest.py에 fixture를 추가해도 되나요?

네, 여러 테스트 파일에서 공통으로 사용하는 데이터는 `conftest.py`에 fixture로 정의하세요.

### Q: 테스트 실패 시 어떻게 디버깅하나요?

```bash
# 실패한 테스트만 재실행
{패키지 매니저} run pytest tests/ --lf -v

# 첫 번째 실패에서 멈춤
{패키지 매니저} run pytest tests/ -x -v

# 상세 출력
{패키지 매니저} run pytest tests/ -v --tb=long
```

### Q: 커버리지가 낮으면 어떻게 하나요?

1. `--cov-report=html`로 HTML 리포트 생성
2. `htmlcov/index.html` 열어서 테스트되지 않은 라인 확인
3. 해당 라인을 커버하는 테스트 케이스 추가

---

## 관련 문서

- [principle.md](./principle.md) - 테스트 원칙 및 방법론
- [error_explanation.md](./error_explanation.md) - 에러 케이스 설명
- {프로젝트별 추가 문서 링크}
