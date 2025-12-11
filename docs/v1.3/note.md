# version 1.3 에서는 현재 streamlit 앱을 streamlit community에 배포하는 절차를 밟을 예정입니다.

그래서 해당 준비에 맞게 아래 하위 항목들에 대한 정리를 진행해야 합니다.

## 안정적인 ML 모델 처리를 위한 전처리

train 데이터와 test 데이터에 대하여 사고일시, 라고 되어있는 칼럼에 대한 전처리 필요

- 현재 사고일시 데이터가 {yyyy-mm-dd HH} 이런 형태로 빠지고 있습니다.
- 이를 사고연, 사고월, 사고일, 사고시, 요일,  이렇게 5개로 분류되어어야 합니다.
- 예를 들어 "2022-01-01 01" 이었다면 사고연: 2022(int), 사고월: 1, 사고일: 1, 사고시: 1로 되어야 합니다.
- 그리고 사고시를 보고 시간대라는 범주형 컬럼도 만들어져야 합니다.
- 범주형 컬럼은 아래 규칙에 따라 만듭니다.
```python 
def hour_to_period(h):
    if 7 <= h <= 9:
        return "출근시간대"
    elif 17 <= h <= 19:
        return "퇴근시간대"
    elif 22 <= h or h <= 5:
        return "심야"
    else:
        return "일반시간대"
```

## 그 외 해당 ML 모델을 구동하기 위해 필요한 전처리가 있는지 확인하고 수행
- 참고 주피터 노트북: material/03-07/3_2_데이콘_데이터_제출해보기.ipynb
- 모델 추론을 위한 데이터: model/* 


## 프로젝트 개요 내용 추가

데이터 업로드하는 부분 위에 아래 내용이 자연스럽게 추가되어야 합니다. 


대구 지역 공공데이터를 탐색·분석하는 교육용 Streamlit 애플리케이션입니다.

데이터 출처: [DACON 대구 교통사고 피해 예측 AI 경진대회](https://dacon.io/competitions/official/236193/overview/description)

즉 데이터 원본을 위의 대회에서 불러와 업로드하면 된다고 안내하면 됩니다. 

## requirements.txt를 pyproject.toml과 싱크를 맞춘다. 

streamlit cloud는 github의 requirements.txt를 인식해서 배포가 되기 때문에 이를 toml 파일과 싱크를 맞춰야 합니다. 