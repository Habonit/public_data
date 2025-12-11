<!--
Sync Impact Report:
===================
Version: 1.2.0 → 1.3.0 (MINOR - TDD, Error Handling, AI/ML, 배포 환경 변경 등 다수 섹션 추가)
Ratification Date: 2025-11-21
Last Amended: 2025-12-11

Modified Principles:
- UNCHANGED: I. Data-First Exploration
- UNCHANGED: II. Simplicity & Accessibility
- UNCHANGED: III. Educational Purpose (NON-NEGOTIABLE)
- MODIFIED: IV. Streamlit-Based Visualization (로컬 실행 → Streamlit Community Cloud 배포)
- UNCHANGED: V. Scope Discipline

Added Sections:
- VIII. 3.4 전처리 파이프라인 (Data Handling Rules 하위)
- XI. 브랜치 전략 (Branch Strategy)
- XII. TDD (Test-Driven Development) 방법론
- XIII. Error Handling
- XIV. Environment & Configuration
- XV. Code Review Checklist
- XVI. AI/ML Guidelines

Modified Sections:
- VIII. Data Handling Rules: CSV 인코딩 순서 변경 (3개 → 4개)
- IX. Dependencies: 필수 패키지 확장 (7개 → 14개), 선택적 패키지 축소

Removed Sections:
- None

Templates Requiring Updates:
✅ spec-template.md - aligned (변경 불필요)
✅ plan-template.md - aligned (Constitution Check 섹션 유지)
✅ tasks-template.md - aligned (변경 불필요)

Follow-up TODOs:
- None (all placeholders filled)

Change Summary (한국어):
- v1.3 배포 준비: Streamlit Community Cloud 배포 환경 반영
- TDD 방법론, Error Handling, AI/ML Guidelines 등 개발 규칙 대폭 강화
- 의존성 패키지 14개로 확장 (langchain, scikit-learn, lightgbm 등)
- CSV 인코딩 순서 4개로 확장 (utf-8-sig 우선)
- 전처리 파이프라인, 브랜치 전략, 환경 설정, 코드 리뷰 체크리스트 추가
-->

# 대구 공공데이터 시각화 프로젝트 Constitution

## Core Principles (핵심 원칙)

### I. Data-First Exploration (데이터 우선 탐색)

**데이터는 단순히 제공되는 것이 아니라, 사고를 자극하는 도구이다.**

모든 기능은 복잡한 피처 엔지니어링이나 모델링보다 데이터 구조, 관계, 분포를 이해하는 것을 우선시해야 한다(MUST). 사용자는 여러 공공 데이터셋(CCTV, 보안등, 어린이 보호구역, 주차장, 사고 데이터, train/test 데이터셋)을 빠르게 이해할 수 있는 통합 환경에서 탐색할 수 있어야 한다(MUST).

**근거**: 이 프로젝트는 학습자가 독립적으로 인사이트를 발견하고 프로젝트 아이디어를 도출하도록 돕기 위해 존재한다. 데이터 시각화와 탐색이 이 목표를 달성하는 핵심 메커니즘이다.

### II. Simplicity & Accessibility (단순성 및 접근성)

**모든 코드는 Python 초보자도 이해할 수 있을 만큼 단순해야 한다(MUST).**

- 복잡한 아키텍처 패턴 금지 (repositories, factories, dependency injection)
- 고급 GIS 처리 금지 (좌표 변환, 공간 조인)
- 별도 백엔드 서버나 데이터베이스 구축 금지
- 코드 구조는 명확하고 일관되며 자명해야 함(MUST)
- 과도한 최적화 지양; 교육적 명확성이 성능보다 우선

**근거**: 대상 사용자는 데이터 분석 초보자 및 Python/Streamlit 학습자이다. 코드가 너무 복잡하면 교육 목적에 어긋나고 학습 장벽을 만든다.

### III. Educational Purpose (교육 목적) - NON-NEGOTIABLE

**모든 기능은 학습자가 독립적으로 문제를 정의하고 프로젝트를 기획하도록 지원해야 한다(MUST).**

- 분석적 사고를 촉발하는 통계 요약 및 시각화 제공
- 데이터셋 간 상관관계 발견 지원 (예: train/test 데이터, 사고 데이터, 대구 공공시설)
- 시각 정보를 통한 프로젝트 아이디어 생성 촉진
- Streamlit, 데이터 분석, 시각화 기초의 실습 학습 지원

**근거**: 최상위 목표는 학습자가 독립적으로 다음 프로젝트를 구상하고 기획하도록 역량을 강화하는 것이다. 이 목표에 기여하지 않는 기능은 거부되어야 한다(MUST).

### IV. Streamlit-Based Visualization (Streamlit 기반 시각화)

**애플리케이션은 Streamlit 기반 반응형 웹 시각화 도구여야 한다(MUST).**

- 각 데이터셋에 대한 탭 기반 네비게이션
- Plotly 또는 유사 라이브러리를 사용한 대화형 그래프
- Folium, Pydeck 또는 동등한 도구를 사용한 지도 기반 시각화
- 다양한 화면 크기(모바일, 태블릿, 데스크톱)에 적응하는 반응형 UI
- **배포 환경**: Streamlit Community Cloud 기준

**근거**: Streamlit은 빠른 프로토타이핑을 가능하게 하고 학습자가 대화형 데이터 애플리케이션을 구축하는 데 낮은 진입 장벽을 제공한다.

### V. Scope Discipline (범위 규율)

**정의된 범위 외의 기능은 명시적으로 제외되어야 한다(MUST).**

**포함 범위**:
- Streamlit 기반 반응형 웹 UI
- CSV 데이터 업로드 및 기본 통계
- 그래프 시각화 (Plotly 등)
- 지도 기반 시각화 (Folium, Pydeck 등)
- 데이터셋 간 관계 탐색
- 경량 탐색적 분석 기능
- AI 기반 데이터 질의응답 (챗봇)
- ECLO 예측 모델 추론 (LightGBM)

**제외 범위**:
- 별도 백엔드 API 개발
- 데이터베이스 구축
- 머신러닝/딥러닝 모델 학습 (추론만 허용)
- 고급 GIS 작업 (복잡한 공간 처리)

**근거**: 명확한 경계는 범위 확장을 방지하고 교육 미션에 집중을 유지한다. 제외된 기능을 추가하면 교육적 가치에 상응하지 않는 복잡성과 유지보수 부담이 증가한다.

---

## VI. Git Commit Convention (Git 커밋 규칙)

### 커밋 메시지 형식

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type (유형)

| Type | 설명 |
|------|------|
| `feat` | 새로운 기능 추가 |
| `fix` | 버그 수정 |
| `docs` | 문서 수정 |
| `style` | 코드 포맷팅, 세미콜론 누락 등 (코드 변경 없음) |
| `refactor` | 코드 리팩토링 |
| `test` | 테스트 코드 추가/수정 |
| `chore` | 빌드, 설정 파일 수정 |

### 예시

```
feat: 히트맵 시각화 기능 추가

- plotly heatmap 차트 생성 함수 구현
- 숫자형 컬럼 간 상관관계 시각화
```

---

## VII. Python Code Style (Python 코드 스타일)

### 7.1 일반 규칙

- **Python 버전**: 3.10+
- **타입 힌트**: 모든 함수에 타입 힌트 사용 (예: `def func(arg: str) -> int:`)
- **Docstring**: Google 스타일 docstring 사용
- **라인 길이**: 최대 100자
- **들여쓰기**: 스페이스 4칸

### 7.2 임포트 순서

```python
# 1. 표준 라이브러리
import os
from math import sqrt

# 2. 서드파티 라이브러리
import pandas as pd
import streamlit as st

# 3. 로컬 모듈
from utils.loader import load_dataset
```

### 7.3 함수/변수 네이밍

| 대상 | 규칙 | 예시 |
|------|------|------|
| 함수명 | snake_case | `load_dataset`, `create_folium_map` |
| 변수명 | snake_case | `df_clean`, `lat_col` |
| 상수 | UPPER_SNAKE_CASE | `MAX_POINTS = 5000` |
| 클래스 | PascalCase | `DataLoader` |

### 7.4 Docstring 형식

```python
def function_name(param1: str, param2: int) -> dict:
    """
    함수에 대한 간략한 설명.

    Parameters:
        param1 (str): 첫 번째 파라미터 설명
        param2 (int): 두 번째 파라미터 설명

    Returns:
        dict: 반환값 설명

    Raises:
        ValueError: 에러 상황 설명
    """
```

---

## VIII. Data Handling Rules (데이터 처리 규칙)

### 8.1 CSV 인코딩

인코딩 시도 순서: `UTF-8-SIG` → `UTF-8` → `CP949` → `EUC-KR`

한글 파일명 지원 필수(MUST)

### 8.2 데이터 로딩 방식

**v1.1 이후**: 사용자가 CSV 파일을 직접 업로드하는 방식

- 프로젝트 개요 탭에서 데이터셋별 업로드 UI 제공
- 업로드된 데이터는 `st.session_state`에 캐싱
- 데이터 미업로드 시 해당 탭에서 안내 메시지 표시

### 8.3 좌표 컬럼 감지

자동 감지 대상 컬럼명:

| 좌표 | 후보 컬럼명 |
|------|------------|
| 위도 | `lat`, `latitude`, `위도`, `y좌표`, `y`, `Lat`, `Latitude` |
| 경도 | `lng`, `lon`, `longitude`, `경도`, `x좌표`, `x`, `Lng`, `Lon`, `Longitude` |

### 8.4 성능 제한

| 항목 | 제한 | 초과 시 처리 |
|------|------|-------------|
| 지도 시각화 최대 포인트 | 5,000개 | 샘플링 |
| 근접성 분석 최대 행 | 5,000행 | 샘플링 |
| 범주형 컬럼 상위 표시 | 20개 | 상위 N개만 표시 |

### 8.5 전처리 파이프라인

- 전처리 함수는 `utils/preprocessing.py`에 모듈화
- 원본 데이터 변경 금지 (복사본 사용)
- 전처리 결과는 session_state에 캐싱

### 8.6 지원 데이터셋

다음 형식의 CSV 파일 업로드를 지원한다:

- CCTV 정보 (대구 CCTV 정보.csv)
- 보안등 정보 (대구 보안등 정보.csv)
- 어린이 보호구역 정보 (대구 어린이 보호 구역 정보.csv)
- 주차장 정보 (대구 주차장 정보.csv)
- 사고 데이터 (countrywide_accident.csv)
- 훈련 데이터 (train.csv)
- 테스트 데이터 (test.csv)

---

## IX. Dependencies (의존성)

### 필수 패키지

| 패키지 | 최소 버전 | 용도 |
|--------|----------|------|
| streamlit | 1.28.0 | 웹 프레임워크 |
| pandas | 2.0.0 | 데이터 처리 |
| numpy | 1.24.0 | 수치 연산 |
| plotly | 5.17.0 | 대화형 차트 |
| folium | 0.14.0 | 지도 시각화 |
| streamlit-folium | 0.15.0 | Folium-Streamlit 통합 |
| matplotlib | 3.8.0 | 추가 시각화 |
| openpyxl | 3.1.5 | Excel 파일 지원 |
| anthropic | 0.39.0 | AI 챗봇 API |
| langchain | 0.3.0 | LLM 프레임워크 |
| langchain-anthropic | 0.3.0 | Anthropic 연동 |
| langgraph | 0.2.0 | Tool Calling 워크플로우 |
| scikit-learn | 1.7.2 | ML 유틸리티 |
| lightgbm | 4.6.0 | ECLO 예측 모델 |

### 선택적 패키지

| 패키지 | 용도 |
|--------|------|
| geopandas | 지도 렌더링 (선택) |
| pydeck | 지도 시각화 대안 (선택) |
| leafmap | 지도 시각화 대안 (선택) |

---

## X. Documentation & Comments (문서화 및 주석)

### 10.1 언어 규칙

- **기본 언어**: 한글로 작성
- **영어 사용 허용**: 한글로 전달이 어려운 기술 용어 (예: DataFrame, API, cache 등)
- **불필요한 영어 지양**: 영어로 쓸 이유가 없으면 한글로 작성

### 10.2 주석 작성

```python
# 좋은 예
# 좌표 결측값이 있는 행 제거
df_clean = df.dropna(subset=[lat_col, lng_col])

# 나쁜 예
# Drop rows with missing coordinates  ← 불필요한 영어
df_clean = df.dropna(subset=[lat_col, lng_col])
```

### 10.3 Docstring 작성

- 함수 설명: 한글로 간결하게
- Parameters/Returns: 타입은 영어, 설명은 한글
- 기술 용어(DataFrame, str, dict 등): 원문 유지

```python
def load_dataset(dataset_name: str) -> pd.DataFrame:
    """
    이름으로 사전 정의된 데이터셋 로드 (캐싱 적용).

    Parameters:
        dataset_name (str): 데이터셋 이름

    Returns:
        pd.DataFrame: 캐시된 데이터셋
    """
```

### 10.4 마크다운 문서

- 제목, 설명, 내용: 한글
- 코드 예시: 원본 유지
- 기술 용어 및 명령어: 원문 (예: `streamlit run`, `git commit`)

---

## XI. Branch Strategy (브랜치 전략)

### 11.1 브랜치 네이밍

- spec 문서를 만들 때의 이름으로 브랜치를 쓰지 않는다
- 무조건 버전 이름으로만 브랜치를 딴다
- 형태: `version/{실제 버전}` (예: `version/1.3`)

### 11.2 버전 번호 규칙

- **Major (x.0.0)**: 대규모 기능 추가 또는 Breaking Change
- **Minor (1.x.0)**: 신규 기능 추가
- **Patch (1.2.x)**: 버그 수정 및 소규모 개선

### 11.3 릴리스 절차

1. `app_improvement_proposal.md` 작성
2. 테스트 코드 작성 (TDD)
3. 구현 및 테스트 통과 확인
4. README.md 버전 히스토리 업데이트

---

## XII. TDD (Test-Driven Development) 방법론

### 12.1 개발 프로세스

1. **제안서 작성**: `docs/v{버전}/app_improvement_proposal.md` 작성
2. **테스트 코드 작성**: 구현 전에 테스트 코드를 먼저 작성
3. **구현**: 테스트를 통과하도록 기능 구현
4. **검증**: 모든 테스트 통과 확인

### 12.2 테스트 코드 규칙

- **테스트 위치**: `tests/` 디렉토리
- **테스트 파일명**: `test_<모듈명>.py`
- **테스트 함수명**: `test_<기능명>_<상황>` (예: `test_preprocess_datetime_valid_input`)
- **테스트 프레임워크**: pytest

### 12.3 테스트 작성 순서

```python
# 1. 정상 케이스 (Happy Path)
def test_preprocess_datetime_valid_input():
    ...

# 2. 경계 케이스 (Edge Case)
def test_preprocess_datetime_midnight():
    ...

# 3. 예외 케이스 (Error Case)
def test_preprocess_datetime_missing_column():
    ...
```

### 12.4 테스트 실행

```bash
# 전체 테스트 실행
pytest tests/

# 특정 테스트 파일 실행
pytest tests/test_preprocessing.py

# 커버리지 포함 실행
pytest tests/ --cov=utils
```

### 12.5 TDD 적용 대상

- `app_improvement_proposal.md`에 정의된 모든 신규 기능
- 전처리 함수 및 유틸리티 함수
- ML 모델 추론 관련 함수

---

## XIII. Error Handling

### 13.1 예외 처리 원칙

- 사용자에게 친절한 한글 에러 메시지 제공
- 내부 에러 로깅과 사용자 메시지 분리
- 복구 가능한 에러는 Graceful Degradation 적용

### 13.2 Graceful Degradation (우아한 성능 저하)

시스템의 일부 기능이 실패하더라도 전체 시스템이 중단되지 않고,
가능한 범위 내에서 서비스를 계속 제공하는 설계 원칙.

**예시:**
- ML 모델 로딩 실패 → ECLO 예측 기능만 비활성화, 나머지 앱은 정상 동작
- API Key 미입력 → 챗봇 탭에서 안내 메시지 표시, 다른 탭은 정상 동작
- 좌표 컬럼 미감지 → 지도 시각화만 비활성화, 통계/차트는 정상 표시

### 13.3 예외 처리 패턴

- try-except 블록에서 구체적인 예외 타입 명시
- **bare except 사용 금지**

**bare except란?**
예외 타입을 명시하지 않고 모든 예외를 포괄적으로 잡는 패턴.
디버깅을 어렵게 하고 예상치 못한 에러를 숨길 수 있어 금지.

```python
# 나쁜 예 (bare except)
try:
    result = process_data(df)
except:  # ← 어떤 에러인지 알 수 없음
    pass

# 좋은 예 (구체적 예외 타입 명시)
try:
    result = process_data(df)
except ValueError as e:
    st.error(f"데이터 형식 오류: {e}")
except KeyError as e:
    st.error(f"필수 컬럼 누락: {e}")
except Exception as e:
    st.error(f"예상치 못한 오류: {e}")
    logging.exception("process_data 실패")
```

### 13.4 에러 명세서

상세 에러 케이스는 `docs/error_explanation.md` 참조

---

## XIV. Environment & Configuration

### 14.1 환경 변수

- API Key 등 민감 정보: `.env` 파일에 보관
- `.env` 파일은 `.gitignore`에 포함하여 버전 관리에서 제외
- 하드코딩 금지

### 14.2 Streamlit 설정

- 앱 설정: `.streamlit/config.toml`
- 배포 환경 secrets: `.streamlit/secrets.toml` (Streamlit Community Cloud 전용)

### 14.3 배포 환경

- Streamlit Community Cloud 기준
- `requirements.txt` 최신 유지 (pyproject.toml과 동기화 필수)
- Python 버전 명시 (runtime.txt 또는 pyproject.toml)

---

## XV. Code Review Checklist

- [ ] 타입 힌트 적용 여부
- [ ] Docstring 작성 여부
- [ ] 테스트 코드 존재 여부
- [ ] 한글 주석/문서 규칙 준수
- [ ] 구체적 예외 타입 명시 (bare except 금지)

---

## XVI. AI/ML Guidelines

### 16.1 모델 파일 관리

- 모델 파일 위치: `model/` 디렉토리
- 필수 파일: 모델(.pkl), 인코더(.pkl), 피처 설정(.json)

### 16.2 추론 함수 규칙

- 입력 검증 필수 (필수 컬럼, 데이터 타입)
- 예측 실패 시 명확한 에러 메시지
- 배치 예측 지원

---

## Development Workflow (개발 워크플로우)

**환경 요구사항**:
- Python 3.10 이상
- pip 또는 conda 패키지 관리
- 크로스 플랫폼 지원 (Windows, macOS, Linux)

**설치 프로세스**:
1. 저장소 클론
2. `requirements.txt`에서 의존성 설치

**실행**:
```bash
streamlit run app.py
```
애플리케이션은 기본적으로 `http://localhost:8501`에서 실행된다.

**품질 표준**:
- 코드 단순성이 교묘함보다 우선되어야 한다(MUST)
- 모든 기능은 복잡한 설정 없이 누구나 실행 가능해야 한다(MUST)
- 데이터 탐색과 시각화가 핵심 초점이어야 한다(MUST)
- 코드 구조는 명확하고 일관되어야 한다(MUST)
- 과도한 최적화를 피하고 교육적 초점을 유지해야 한다(MUST)
- Python Code Style (섹션 VII) 준수 필수

**테스트 전략**:
- TDD 방법론 적용 (섹션 XII 참조)
- 검증 초점: 데이터 로딩, 전처리, 시각화 렌더링, ML 추론

---

## Governance (거버넌스)

**Constitution 권한**: 이 constitution은 모든 다른 개발 관행 및 결정보다 우선한다. 모든 명세(spec.md), 계획(plan.md), 작업(tasks.md)은 여기에 정의된 원칙을 준수해야 한다(MUST).

**수정 프로세스**:
1. 제안된 수정 사항은 명확한 근거와 함께 문서화되어야 한다(MUST)
2. 기존 기능에 대한 영향을 평가해야 한다(MUST)
3. 템플릿 업데이트 (spec-template.md, plan-template.md, tasks-template.md)를 동기화해야 한다(MUST)
4. 버전 번호는 시맨틱 버저닝에 따라 증가해야 한다(MUST):
   - MAJOR: 이전 버전과 호환되지 않는 원칙 제거 또는 재정의
   - MINOR: 새 원칙 추가 또는 실질적 확장
   - PATCH: 설명, 문구 수정, 비시맨틱 개선

**준수 검증**:
- 모든 기능 명세는 정렬을 검증하는 "Constitution Check" 섹션을 포함해야 한다(MUST)
- 코드 리뷰는 단순성 및 접근성 원칙 준수를 검증해야 한다(MUST)
- 복잡성 추가는 plan.md의 "Complexity Tracking" 섹션에서 정당화되어야 한다(MUST)
- 교육적 가치가 모든 기능의 주요 결정 기준이어야 한다(MUST)

**버저닝 정책**: 시맨틱 버저닝 (MAJOR.MINOR.PATCH)을 사용하여 constitution 변경을 추적한다. 모든 변경 사항은 이 파일 상단의 Sync Impact Report에 문서화한다.

---

## Document History (문서 이력)

| 버전 | 날짜 | 설명 |
|------|------|------|
| v1.0.0 | 2025-11-21 | 최초 제정 - 5개 핵심 원칙 정의 |
| v1.1.0 | 2025-12-01 | docs/constitution.md 통합 - Git 규칙, 코드 스타일, 데이터 처리, 의존성, 문서화 규칙 추가 |
| v1.2.0 | 2025-12-02 | v1.1 앱 개선사항 반영 - anthropic 패키지 추가, CSV 업로드 방식, AI 챗봇 범위 추가 |
| v1.3.0 | 2025-12-11 | v1.3 배포 준비 - TDD, Error Handling, AI/ML Guidelines, 브랜치 전략, 환경 설정 추가; 의존성 14개로 확장 |

---

**Version**: 1.3.0 | **Ratified**: 2025-11-21 | **Last Amended**: 2025-12-11
