# Quickstart: v1.3 Streamlit Community 배포 준비

**Date**: 2025-12-11
**Feature**: 005-v1-3-deploy-prep

## 1. 개발 환경 설정

### 1.1 Python 환경

```bash
# Python 3.10+ 필요
python --version  # 3.10 이상 확인

# 의존성 설치
pip install -r requirements.txt
```

### 1.2 테스트 환경

```bash
# 개발 의존성 설치 (pytest)
pip install pytest

# 또는 uv 사용 시
uv sync
```

## 2. TDD 워크플로우

### 2.1 테스트 먼저 작성 (Red)

```bash
# 테스트 디렉토리 생성
mkdir -p tests

# 테스트 파일 생성
touch tests/__init__.py
touch tests/conftest.py
touch tests/test_preprocessing.py

# 테스트 실행 (실패 예상)
pytest tests/test_preprocessing.py -v
```

### 2.2 구현 (Green)

```bash
# 전처리 모듈 생성
touch utils/preprocessing.py

# 구현 후 테스트 재실행
pytest tests/test_preprocessing.py -v
```

### 2.3 리팩토링 (Refactor)

```bash
# 전체 테스트 실행
pytest tests/ -v

# 커버리지 확인 (선택)
pytest tests/ --cov=utils
```

## 3. 로컬 실행

### 3.1 앱 실행

```bash
streamlit run app.py
```

브라우저에서 `http://localhost:8501` 접속

### 3.2 전처리 기능 테스트

1. 프로젝트 개요 탭 접속
2. DACON 대회 링크에서 train.csv 다운로드
3. 훈련 데이터 업로드
4. 데이터 탭에서 "사고연", "사고월", "사고일", "사고시", "시간대" 컬럼 확인

## 4. Streamlit Community Cloud 배포

### 4.1 사전 준비

```bash
# requirements.txt 동기화 확인
cat requirements.txt | grep -E "(scikit-learn|lightgbm)"
# 출력: scikit-learn>=1.7.2, lightgbm>=4.6.0
```

### 4.2 배포 단계

1. GitHub 저장소에 코드 푸시
2. [share.streamlit.io](https://share.streamlit.io) 접속
3. 저장소 연결 및 app.py 지정
4. Deploy 클릭

### 4.3 배포 검증

1. 배포된 URL 접속
2. train.csv 업로드
3. AI 챗봇에서 ECLO 예측 요청
4. 예측 결과 정상 반환 확인

## 5. 파일 구조

```
project/
├── app.py                    # 메인 앱 (프로젝트 개요 탭 수정)
├── requirements.txt          # 의존성 (scikit-learn, lightgbm 추가)
├── pyproject.toml           # 개발 설정
├── utils/
│   ├── __init__.py
│   ├── loader.py            # 데이터 로딩 (전처리 호출 추가)
│   ├── preprocessing.py     # 신규 - 사고일시 전처리
│   └── ...
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # pytest 설정
│   └── test_preprocessing.py # 전처리 테스트
└── model/
    ├── accident_lgbm_model.pkl
    ├── label_encoders.pkl
    └── feature_config.json
```

## 6. 주요 함수 사용법

### 6.1 시간대 분류

```python
from utils.preprocessing import hour_to_period

# 사용 예시
hour_to_period(8)   # "출근시간대"
hour_to_period(18)  # "퇴근시간대"
hour_to_period(23)  # "심야"
hour_to_period(14)  # "일반시간대"
```

### 6.2 사고일시 전처리

```python
from utils.preprocessing import preprocess_accident_datetime
import pandas as pd

# 사용 예시
df = pd.read_csv("train.csv")
df_processed = preprocess_accident_datetime(df)

# 생성된 컬럼 확인
print(df_processed[['사고연', '사고월', '사고일', '사고시', '시간대']].head())
```

## 7. 트러블슈팅

### 7.1 배포 실패: ModuleNotFoundError

```
ModuleNotFoundError: No module named 'sklearn'
```

**해결**: requirements.txt에 `scikit-learn>=1.7.2` 추가 확인

### 7.2 배포 실패: lightgbm 설치 오류

```
ERROR: Could not build wheels for lightgbm
```

**해결**: Streamlit Cloud는 lightgbm 자동 빌드 지원. requirements.txt 버전 확인.

### 7.3 전처리 미적용

데이터 업로드 후 "시간대" 컬럼이 없는 경우:
- loader.py에서 `preprocess_accident_datetime()` 호출 확인
- "사고일시" 컬럼 존재 여부 확인
