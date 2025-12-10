# 3일차~7일차 교육 커리큘럼

## 개요

이 문서는 3일차부터 7일차까지의 교육 내용을 정리한 것입니다.
교육생이 해당 주피터 노트북을 각자 환경(Colab)에서 재현해볼 수 있도록 구성되어 있습니다.

- **실습 환경**: Google Colab
- **사용 데이터 경로**: `material/3-7/data`
- **데이터 출처**: [Dacon 대구 교통사고 피해 예측 AI 경진대회](https://dacon.io/competitions/official/236193/overview/description)

---

## 3일차: 대구 교통사고 피해 예측 AI 경진대회

### 학습 목표
- Dacon 플랫폼 가입 및 API Key 발급
- 대회 데이터를 API로 불러오기
- 기본적인 모델링을 통해 Dacon에 직접 제출해보기

### 주요 내용
1. **ECLO (Equivalent Casualty Level of Object)**: 사고 피해 심각도를 수치화한 지표
2. **Feature Engineering**: 날짜/시간 파생 변수 생성, 시간대 분류
3. **모델 비교**: LinearRegression, RandomForest, XGBoost, LightGBM
4. **평가 지표**: RMSLE (Root Mean Squared Log Error)

### 참고 노트북
| 파일명 | 설명 |
|--------|------|
| `3_2_데이콘_데이터_제출해보기.ipynb` | Dacon 대회 데이터 로드, EDA, 모델링, 제출 파일 생성 |

### 사용 데이터
- `train.csv`: 학습 데이터 (39,609건, 23개 컬럼, ECLO 포함)
- `test.csv`: 제출용 예측 대상 (10,963건, 8개 컬럼)
- `sample_submission.csv`: 제출 포맷

---

## 4일차: AutoML을 통한 모델링과 그 한계 파악

### 학습 목표
- AutoML(AutoGluon)의 기본 사용법 익히기
- AutoML의 장점과 한계 이해하기
- 수동 모델링과 AutoML 결과 비교

### 주요 내용
1. **AutoGluon 설치 및 기본 사용법**
2. **TabularPredictor**: 테이블 데이터용 예측기
3. **Presets**: `best_quality`, `medium_quality_faster_train` 등
4. **Multi-target Regression**: 여러 타깃 변수 동시 예측

### 참고 노트북
| 파일명 | 설명 |
|--------|------|
| `4_도입_automl_경험해보기pynb.ipynb` | AutoGluon 설치 및 자율주행 데이터로 실습 |
| `4_2_automl_좀더_자세히.ipynb` | 사고 데이터셋에 AutoGluon 적용, RMSLE 검증 |

### AutoML 한계점
- 블랙박스 특성으로 해석이 어려움
- 학습 시간이 오래 걸릴 수 있음
- 도메인 지식 반영이 제한적

---

## 5일차: Claude Code와 GitHub Speckit을 통한 App Version 1.0 구현

### 학습 목표
- Claude Code를 활용한 AI 기반 개발 경험
- GitHub Speckit 방법론 이해
- Streamlit 대시보드 Version 1.0 구현

### 주요 내용
- 주피터 노트북으로 공부한 내용은 없음
- Version 1.0 구현에 집중

### 참고 자료
- **GitHub 저장소**: https://github.com/Habonit/public_data.git (version/1.0 브랜치 참조)
- **Speckit 링크**: https://github.com/github/spec-kit

---

## 6일차: Version 1.0으로 구현한 데이터 시각화 검증 (1/2)

### 학습 목표
- Streamlit 대시보드에서 시각화한 결과를 Colab에서 검증
- train, test, countrywide_accident 데이터의 시각화 정확성 확인

### 주요 내용
1. **데이터 로드 및 기본 정보 확인**: head(), info(), describe()
2. **수치형/범주형 컬럼 자동 분리**: `select_dtypes()` 활용
3. **수치형 컬럼 시각화**: 히스토그램, 박스플롯
4. **범주형 컬럼 시각화**: Bar Chart (상위 20개 카테고리)

### 참고 노트북
| 파일명 | 설명 |
|--------|------|
| `6_2_train_데이터_검증하기.ipynb` | train.csv EDA 및 시각화 검증 |
| `6_2_test_csv_분석하기.ipynb` | test.csv EDA 및 시각화 검증 |
| `6_2_전국_사고_데이터.ipynb` | countrywide_accident.csv EDA 및 시각화 검증 |

### 사용 데이터
| 파일명 | 행 수 | 컬럼 수 | 특징 |
|--------|-------|---------|------|
| train.csv | 39,609 | 23 | 수치형 5개, 범주형 18개 |
| test.csv | 10,963 | 8 | 전부 범주형 |
| countrywide_accident.csv | 602,775 | 23 | 전국 사고 데이터 |

---

## 7일차: Version 1.0으로 구현한 데이터 시각화 검증 (2/2)

### 학습 목표
- 대구 지역 시설물 데이터(CCTV, 보안등, 주차장) 시각화 검증
- 위도/경도 기반 지도 시각화 (Folium + MarkerCluster)

### 주요 내용
1. **위도/경도 컬럼 자동 감지**: 다양한 컬럼명 후보 탐색
2. **Folium 지도 시각화**: MarkerCluster를 활용한 클러스터링
3. **수치형/범주형 컬럼 분석**: 히스토그램, 박스플롯, Bar Chart

### 참고 노트북
| 파일명 | 설명 |
|--------|------|
| `7_1_대구_cctv_데이터_검증.ipynb` | 대구 CCTV 데이터 EDA 및 지도 시각화 |
| `7_1_보안등_데이터_구조.ipynb` | 대구 보안등 데이터 EDA 및 지도 시각화 |
| `7_1_주차장_검증.ipynb` | 대구 주차장 데이터 EDA 및 지도 시각화 |

### 사용 데이터
| 파일명 | 행 수 | 컬럼 수 | 평균 결측률 |
|--------|-------|---------|------------|
| 대구 CCTV 정보.csv | 1,065 | 18 | 16.49% |
| 대구 보안등 정보.csv | 71,913 | 8 | 30.06% |
| 대구 주차장 정보.csv | - | - | - |
| 대구 어린이 보호 구역 정보.csv | - | - | (노트북 없음, 반복 패턴으로 생략) |

---

## 공통 코드 패턴

### 한글 폰트 설정 (Colab)
```python
!apt-get update -qq
!apt-get install -y fonts-nanum

import shutil
import matplotlib as mpl

root = mpl.matplotlib_fname().replace("matplotlibrc", "")
target_font = root + "fonts/ttf/DejaVuSans.ttf"
nanum_font = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"
shutil.copyfile(nanum_font, target_font)

!rm -rf ~/.cache/matplotlib
```

### CSV 안전 로드 함수
```python
def read_csv_safe(path, encodings=["utf-8", "utf-8-sig", "cp949"]):
    """여러 인코딩을 시도하면서 CSV 파일을 안전하게 읽는 함수"""
    for enc in encodings:
        try:
            return pd.read_csv(path, encoding=enc)
        except Exception as e:
            print(f"[경고] 인코딩 {enc} 로 읽기 실패: {e}")
            continue
    raise ValueError("CSV를 어떤 인코딩으로도 읽을 수 없습니다.")
```

### 수치형/범주형 컬럼 분리
```python
numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
```

---

## 필수 라이브러리

```python
# 기본 라이브러리
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 지도 시각화
import folium
from folium.plugins import MarkerCluster

# 머신러닝
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_log_error
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor

# AutoML
from autogluon.tabular import TabularPredictor
```

---

## 학습 포인트 요약

| 일차 | 핵심 키워드 | 배운 것 |
|------|------------|---------|
| 3일차 | Dacon, ECLO, RMSLE | AI 경진대회 참여 방법, 기본 모델링 파이프라인 |
| 4일차 | AutoML, AutoGluon | 자동화된 머신러닝의 장단점 |
| 5일차 | Claude Code, Speckit | AI 기반 개발 도구 활용 |
| 6일차 | EDA, 시각화 검증 | Streamlit 대시보드 데이터 정합성 확인 |
| 7일차 | Folium, 지도 시각화 | 위치 기반 데이터 시각화 |
