# Project Constitution

대구 공공데이터 시각화 프로젝트의 개발 규칙과 컨벤션을 정의합니다.

---

## 1. Git Commit Convention

### 커밋 메시지 형식
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type
- `feat`: 새로운 기능 추가
- `fix`: 버그 수정
- `docs`: 문서 수정
- `style`: 코드 포맷팅, 세미콜론 누락 등 (코드 변경 없음)
- `refactor`: 코드 리팩토링
- `test`: 테스트 코드 추가/수정
- `chore`: 빌드, 설정 파일 수정

### 예시
```
feat: 히트맵 시각화 기능 추가

- plotly heatmap 차트 생성 함수 구현
- 숫자형 컬럼 간 상관관계 시각화

```

---

## 2. Python Code Style

### 2.1 일반 규칙
- **Python 버전**: 3.10+
- **타입 힌트**: 모든 함수에 타입 힌트 사용 (예: `def func(arg: str) -> int:`)
- **Docstring**: Google 스타일 docstring 사용
- **라인 길이**: 최대 100자
- **들여쓰기**: 스페이스 4칸

### 2.2 임포트 순서
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

### 2.3 함수/변수 네이밍
- **함수명**: snake_case (예: `load_dataset`, `create_folium_map`)
- **변수명**: snake_case (예: `df_clean`, `lat_col`)
- **상수**: UPPER_SNAKE_CASE (예: `MAX_POINTS = 5000`)
- **클래스**: PascalCase (예: `DataLoader`)

### 2.4 Docstring 형식
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

## 3. Data Handling Rules

### 3.1 CSV 인코딩
- 기본 인코딩 시도 순서: ['utf-8-sig', 'utf-8', 'cp949', 'euc-kr']
- 한글 파일명 지원 필수

### 3.2 좌표 컬럼 감지
위도/경도 컬럼명 후보:
  위도: `lat`, `latitude`, `위도`, `y좌표`, `y`, `Lat`, `Latitude`
  경도: `lng`, `lon`, `longitude`, `경도`, `x좌표`, `x`, `Lng`, `Lon`, `Longitude`


### 3.3 성능 제한
- 지도 시각화 최대 포인트: **5,000개** (초과 시 샘플링)
- 근접성 분석 최대 행: **5,000행** (초과 시 샘플링)
- 범주형 컬럼 상위 표시: **20개**

### 3.4 전처리 파이프라인
- 전처리 함수는 `utils/preprocessing.py`에 모듈화
- 원본 데이터 변경 금지 (복사본 사용)
- 전처리 결과는 session_state에 캐싱

---

## 4. Dependencies

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

---

## 5. Development Philosophy

1. **단순성 우선**: 복잡한 로직보다 이해하기 쉬운 코드
2. **교육 목적 중심**: 초보자도 읽고 이해할 수 있어야 함
3. **과한 최적화 지양**: 교육적 가치 > 성능 최적화
4. **명확한 구조**: 코드 구조는 일관되고 예측 가능해야 함
5. **데이터 탐색 중심**: 모델링보다 데이터 이해와 시각화에 집중

---

## 6. Documentation & Comments

### 6.1 언어 규칙
- **기본 언어**: 한글로 작성
- **영어 사용 허용**: 한글로 전달이 어려운 기술 용어 (예: DataFrame, API, cache 등)
- **불필요한 영어 지양**: 영어로 쓸 이유가 없으면 한글로 작성

### 6.2 주석 작성
```python
# 좋은 예
# 좌표 결측값이 있는 행 제거
df_clean = df.dropna(subset=[lat_col, lng_col])

# 나쁜 예
# Drop rows with missing coordinates  ← 불필요한 영어
df_clean = df.dropna(subset=[lat_col, lng_col])
```

### 6.3 Docstring 작성
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

### 6.4 마크다운 문서
- 제목, 설명, 내용: 한글
- 코드 예시: 원본 유지
- 기술 용어 및 명령어: 원문 (예: `streamlit run`, `git commit`)

---

## 7. 브랜치 전략

### 7.1 브랜치 네이밍
- spec 문서를 만들 때의 이름으로 브랜치를 쓰지 않는다
- 무조건 버전 이름으로만 브랜치를 딴다
- 형태: `version/{실제 버전}` (예: `version/1.3`)

### 7.2 버전 번호 규칙
- **Major (x.0.0)**: 대규모 기능 추가 또는 Breaking Change
- **Minor (1.x.0)**: 신규 기능 추가
- **Patch (1.2.x)**: 버그 수정 및 소규모 개선

### 7.3 릴리스 절차
1. `app_improvement_proposal.md` 작성
2. 테스트 코드 작성 (TDD)
3. 구현 및 테스트 통과 확인
4. README.md 버전 히스토리 업데이트

---

## 8. TDD (Test-Driven Development) 방법론

### 8.1 개발 프로세스
1. **제안서 작성**: `docs/v{버전}/app_improvement_proposal.md` 작성
2. **테스트 코드 작성**: 구현 전에 테스트 코드를 먼저 작성
3. **구현**: 테스트를 통과하도록 기능 구현
4. **검증**: 모든 테스트 통과 확인

### 8.2 테스트 코드 규칙
- **테스트 위치**: `tests/` 디렉토리
- **테스트 파일명**: `test_<모듈명>.py`
- **테스트 함수명**: `test_<기능명>_<상황>` (예: `test_preprocess_datetime_valid_input`)
- **테스트 프레임워크**: pytest

### 8.3 테스트 작성 순서
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

### 8.4 테스트 실행
```bash
# 전체 테스트 실행
pytest tests/

# 특정 테스트 파일 실행
pytest tests/test_preprocessing.py

# 커버리지 포함 실행
pytest tests/ --cov=utils
```

### 8.5 TDD 적용 대상
- `app_improvement_proposal.md`에 정의된 모든 신규 기능
- 전처리 함수 및 유틸리티 함수
- ML 모델 추론 관련 함수

---

## 9. Error Handling

### 9.1 예외 처리 원칙
- 사용자에게 친절한 한글 에러 메시지 제공
- 내부 에러 로깅과 사용자 메시지 분리
- 복구 가능한 에러는 Graceful Degradation 적용

### 9.2 Graceful Degradation (우아한 성능 저하)
시스템의 일부 기능이 실패하더라도 전체 시스템이 중단되지 않고,
가능한 범위 내에서 서비스를 계속 제공하는 설계 원칙.

**예시:**
- ML 모델 로딩 실패 → ECLO 예측 기능만 비활성화, 나머지 앱은 정상 동작
- API Key 미입력 → 챗봇 탭에서 안내 메시지 표시, 다른 탭은 정상 동작
- 좌표 컬럼 미감지 → 지도 시각화만 비활성화, 통계/차트는 정상 표시

### 9.3 예외 처리 패턴
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

### 9.4 에러 명세서
상세 에러 케이스는 `tests/error_explanation.md` 참조

---

## 10. Environment & Configuration

### 10.1 환경 변수
- API Key 등 민감 정보: `.env` 파일에 보관
- `.env` 파일은 `.gitignore`에 포함하여 버전 관리에서 제외
- 하드코딩 금지

### 10.2 Streamlit 설정
- 앱 설정: `.streamlit/config.toml`
- 배포 환경 secrets: `.streamlit/secrets.toml` (Streamlit Community Cloud 전용)

### 10.3 배포 환경
- Streamlit Community Cloud 기준
- `requirements.txt` 최신 유지 (pyproject.toml과 동기화 필수)
- Python 버전 명시 (runtime.txt 또는 pyproject.toml)

---

## 11. Code Review Checklist

- [ ] 타입 힌트 적용 여부
- [ ] Docstring 작성 여부
- [ ] 테스트 코드 존재 여부
- [ ] 한글 주석/문서 규칙 준수
- [ ] 구체적 예외 타입 명시 (bare except 금지)

---

## 12. AI/ML Guidelines

### 12.1 모델 파일 관리
- 모델 파일 위치: `model/` 디렉토리
- 필수 파일: 모델(.pkl), 인코더(.pkl), 피처 설정(.json)

### 12.2 추론 함수 규칙
- 입력 검증 필수 (필수 컬럼, 데이터 타입)
- 예측 실패 시 명확한 에러 메시지
- 배치 예측 지원

---

## Document History

| 버전 | 문서 위치 | 설명 |
|------|----------|------|
| v1.0 | `docs/v1.0/daegu_constitution.md` | Spec 주도 개발(SDD)에서 최초 생성된 Constitution |
| v1.1 | `docs/constitution.md` | #1 ~ #6까지 constitution에 반영 |
| v1.2.4 | `docs/constitution.md` | #7까지 constitution에 반영 |
| v1.3 | `docs/constitution.md` | #3, #4, #7 수정, #8, #9, #10, #11, #12 추가하여 constitution에 반영 | 

