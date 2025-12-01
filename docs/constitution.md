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

---

## 3. Data Handling Rules

### 3.1 CSV 인코딩
- 기본 인코딩 시도 순서: `UTF-8` → `UTF-8-SIG` → `CP949`
- 한글 파일명 지원 필수

### 3.2 좌표 컬럼 감지
위도/경도 컬럼명 후보:
- 위도: `lat`, `latitude`, `위도`, `y좌표`, `y`
- 경도: `lng`, `lon`, `longitude`, `경도`, `x좌표`, `x`

### 3.3 성능 제한
- 지도 시각화 최대 포인트: **5,000개** (초과 시 샘플링)
- 근접성 분석 최대 행: **5,000행** (초과 시 샘플링)
- 범주형 컬럼 상위 표시: **20개**

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

## Document History

| 버전 | 문서 위치 | 설명 |
|------|----------|------|
| v1.0 | `docs/v1.0/daegu_constitution.md` | Spec 주도 개발(SDD)에서 최초 생성된 Constitution |

