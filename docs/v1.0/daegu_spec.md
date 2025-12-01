# daegu_spec.md  
대구 공공데이터 시각화 프로젝트 기능 명세(Spec)

본 문서는 Constitution을 기반으로 Streamlit 기반 대구 공공데이터 시각화 웹 앱의  
전체 기능을 정량적으로 정의한 공식 명세이다.  
문서에 정의되지 않은 기능은 구현하지 않는다.

---

# 1. 시스템 개요

본 시스템은 다음 데이터를 기반으로 한다:

- 대구 CCTV 정보  
- 대구 보안등 정보  
- 대구 어린이 보호 구역 정보  
- 대구 주차장 정보  
- countrywide_accident.csv  
- train.csv  
- test.csv  

이 데이터들을 Streamlit UI로 시각화하며,  
데이터 간의 상관성·분포·위치 관계를 분석하여  
교육생이 프로젝트 아이디어를 도출하도록 돕는 탐색형 시각화 시스템이다.

---

# 2. 기능 요구사항(Functional Requirements)

## 2.1 페이지 구조

앱은 다음 탭(Tabs)을 제공한다.

1. 대구 CCTV  
2. 대구 보안등  
3. 대구 어린이 보호 구역  
4. 대구 주차장  
5. Accident(전국 사고 데이터)  
6. train.csv  
7. test.csv  
8. **Cross-Data Analysis (데이터 간 관계 분석)**  
9. **Project Overview (프로젝트 소개 + 구조 다이어그램) — README 통합 텝**

---

# 3. 공통 기능 명세

## 3.1 데이터 로딩
- /data 폴더에서 CSV 자동 로드
- 인코딩 자동 시도(UTF-8 → UTF-8-SIG → CP949)
- 파일 누락 시 Streamlit warning 표시
- 파일명 변경 시 허용하지 않음

---

## 3.2 기초 통계량
각 탭은 다음을 포함해야 한다:

- 데이터프레임 preview (head)
- 행/열 개수
- 데이터 타입
- 결측치 비율 테이블
- describe() 통계량

UI 형식:
- expander 안에 테이블 형태로 표시
- sorting 가능하도록 dataframe() 사용

---

## 3.3 시각화 기능
모든 데이터 탭은 다음 중 가능한 항목을 제공한다.

- 숫자형 컬럼 히스토그램
- 범주형 bar chart
- 산점도(가능한 경우)
- 지도 기반 시각화(위도/경도 존재 시)
- 지도 포인트 클릭 → 세부 정보 팝업

지도 처리 규칙:
- latitude/longitude 컬럼 자동 인식  
  예: ['lat', 'Lat', '위도', 'Y좌표'], ['lng', 'Lon', '경도', 'X좌표']

---

# 4. Cross-Data Analysis 기능 명세

Cross-Data Analysis는 본 프로젝트의 핵심 기능으로,  
다음 세부 기능을 반드시 포함한다.

---

## 4.1 **train.csv와 다른 모든 공공데이터 간 관계 분석**

train.csv와 다음 데이터 간 관계를 필수 제공한다:

- train ↔ CCTV  
- train ↔ 보안등  
- train ↔ 어린이 보호구역  
- train ↔ 주차장  
- train ↔ accident  
- train ↔ test (가능한 경우 단순 분포 비교)

관계 분석의 구성:

### 4.1.1 위치 기반 근접성 분석
- train 좌표가 있는 경우 각 공공데이터와의 거리 계산
- 거리 임계값 예시: 500m / 1km / 2km  
- 가까운 항목 개수의 통계 요약 제공

### 4.1.2 지도 겹쳐보기 Overlay
- train 포인트와 CCTV/보안등 등의 위치를 한 지도 위에 중첩 표시
- 색상/레이어 구분

### 4.1.3 분포 비교
- train 특정 수치 컬럼과 공공데이터의 count 분포 비교
- bar chart, line chart 등

### 4.1.4 텍스트 기반 인사이트 제공
모든 분석 결과는 자연어로 요약해야 한다.

예:
```

train 데이터의 점들이 밀집한 지역은 보안등 역시 밀집되어 있으며,
이는 해당 지역이 상대적으로 야간 안전 장치가 많은 지역일 가능성을 시사합니다.

````

---

## 4.2 공공데이터 간 Cross Analysis

대구의 모든 데이터셋 간 관계도 분석해야 한다.

- CCTV ↔ 보안등  
- CCTV ↔ 보호구역  
- 보호구역 ↔ 주차장  
- 보안등 ↔ accident  
- CCTV ↔ accident  

위 구조는 선택형 UI로 제공한다.

---

# 5. Project Overview (README) 탭 스펙  
**(Constitution에 포함된 README를 실제 Streamlit UI에서도 별도 탭으로 노출)**

이 탭은 다음을 포함한다.

## 5.1 프로젝트 소개
다음 내용을 markdown 형태로 표시:

- 프로젝트 목적  
- 사용 데이터 목록  
- 사용 기술(파이썬, Streamlit, pandas, folium 등)  
- 학습 목표(탐색적 분석, 지도 시각화, 데이터 관계 파악)

---

## 5.2 시스템 구조 다이어그램(필수)

다음 구조를 다이어그램(mermaid 또는 png 파일)로 표시해야 한다.

### 예시 Mermaid 다이어그램

```mermaid
flowchart TD

A[사용자 브라우저] --> B[Streamlit App]

B --> C1[대구 CCTV 탭]
B --> C2[보안등 탭]
B --> C3[어린이 보호구역 탭]
B --> C4[주차장 탭]
B --> C5[Accident 탭]
B --> C6[Train 탭]
B --> C7[Test 탭]
B --> C8[Cross-Data Analysis]
B --> C9[Project Overview]

subgraph Data
D1[대구 CCTV CSV]
D2[보안등 CSV]
D3[보호구역 CSV]
D4[주차장 CSV]
D5[accident CSV]
D6[train CSV]
D7[test CSV]
end

C1 --> D1
C2 --> D2
C3 --> D3
C4 --> D4
C5 --> D5
C6 --> D6
C7 --> D7
C8 --> D1 & D2 & D3 & D4 & D5 & D6
````

요구사항:

* 다이어그램은 mermaid 또는 이미지 모두 허용
* README 탭에서 가독성 있게 표시
* 프로젝트 흐름을 직관적으로 이해할 수 있어야 함

---

# 5.3 데이터 분석 및 통계 기본 개념(교육생 필수 이해 요소)

Project Overview(README) 탭에서는 단순한 프로젝트 소개 외에도  
다음의 “기초 데이터 분석 개념”을 반드시 포함해야 한다.

이 개념들은 교육생이 데이터 시각화와 Cross-Analysis를 이해하는 데 필수이다.

---

## (1) 데이터 타입(Data Types)
- **수치형 데이터(numerical)**: 거리, 수량, 속도 등 숫자로 계산 가능한 값  
- **범주형 데이터(categorical)**: CCTV 종류, 구역명 등 그룹/라벨 형태의 값  
- **날짜/시간 데이터(datetime)**: 사고 발생 시간 등  
- 데이터 타입에 따라 사용 가능한 시각화 종류가 다르다는 점을 설명해야 한다.

---

## (2) 기초 통계량(Basic Statistics)
다음 항목의 의미를 명확히 설명한다.
- **평균(mean)**: 대표값을 이해하기 위한 중심  
- **표준편차(std)**: 값들이 평균에서 얼마나 퍼져있는지  
- **최솟값/최댓값(min/max)**  
- **중앙값(median)**  
- **분위수(25%, 50%, 75%)**  

교육생은 describe() 결과를 보고 데이터의 분포와 안정성을 판단할 수 있어야 한다.

---

## (3) 결측치(Missing Values)
- 결측치가 왜 생기는지  
- 결측치가 많은 컬럼을 어떻게 해석해야 하는지  
- 시각화/분석 시 결측치가 많을 때 발생하는 문제점

시각화 탭에서는 결측치 비율을 표시하고, README 탭에는 개념적 설명을 포함해야 한다.

---

## (4) 이상치(Outliers)
- 극단값이 발생하는 원인 (수집 오류, 실제 특이 케이스 등)  
- 히스토그램/박스플롯에서 이상치가 어떻게 보이는지  
- 왜 이상치를 확인해야 하는지(왜곡 방지)  

---

## (5) 데이터 분포(Distribution)
- 정규분포, 치우친 분포(skew), 긴 꼬리(long tail) 등  
- 분포에 따라 해석이나 모델링 전략이 달라짐  
- 히스토그램과 KDE(밀도 그래프)의 역할  

Cross Analysis에서 train 데이터 분포와 다른 데이터 분포를 비교할 때 사용됨.

---

## (6) 좌표 데이터(Geospatial Basics)
- 위도(latitude) / 경도(longitude)의 의미  
- 지도 시각화 시 좌표의 중요성  
- 가까움(근접성)의 정의  
- 거리 계산 방식(Haversine vs Euclidean)

이 내용은 Cross Analysis의 거리 기반 분석 기능과 직접 연관된다.

---

## (7) 상관성(Correlation)
- 두 변수 또는 두 데이터셋 간의 관계를 의미  
- 양의 상관, 음의 상관, 무상관  
- 지도에서 “근접도”가 일종의 공간적 상관성(spatial correlation) 역할을 한다는 점  

교육생이 "왜 train 데이터와 CCTV 위치를 비교하는지" 이해하도록 한다.

---

## (8) 지도 기반 분포 해석(Spatial Visualization)
- 클러스터링처럼 보이는 위치 패턴의 의미  
- 밀집(high density) ↔ 희박(low density)  
- 지도에 포인트가 겹쳐 보일 때 어떻게 해석해야 하는지  
- 사고 위치와 시설물 위치의 상관성 분석 기본 개념  

---

## (9) Feature의 개념(기본 수준)
- train.csv의 컬럼들은 “특징(feature)”으로 해석될 수 있음  
- 각 feature의 분포를 이해해야 사고 위치/패턴/시설과의 관계를 추론 가능  

---

## (10) 데이터 기반 인사이트 도출법
교육생이 스스로 해석할 수 있도록 기본 질문 예시 포함:

- 어느 지역에 시설물이 많이 분포하는가?  
- 사고는 특정 장소·시간대에 집중되는가?  
- train 데이터가 공공데이터와 어떤 공간적 패턴을 가지는가?  
- 특정 데이터 조합으로 새로운 프로젝트 아이디어를 만들 수 있는가?

이 섹션은 README 탭에 필수 포함된다.

---

# 포함 규칙
- 이 개념 설명은 Project Overview 내에서 **하나의 대시보드 섹션으로 정리**되어야 한다.
- Streamlit markdown 또는 expandable 영역으로 구성 가능.
- 예제 그래프나 샘플 출력이 포함되면 더욱 좋음.

---

---

# 6. UI 요구사항

* Streamlit tabs 또는 sidebar를 사용하되, Constitution에서 정한 구조 우선
* 모든 그래프는 반응형
* 오류 발생 시 사용자 친화적 메시지 제공

---

# 7. 비기능 요구사항

* 로컬 기준 3초 이내 초기 로드
* 지도 렌더링은 5000 포인트까지 원활히 동작
* 캐싱(st.cache_data) 필수 적용
* 코드 모듈화 필수 (loader / visualizer / analysis 분리)

---

# 8. 성공 기준 (Definition of Done)

* 모든 데이터가 정상 로드
* train ↔ 다른 공공데이터 관계 시각화 정상 동작
* Cross-Analysis 탭에서 최소 3종 이상의 관계 분석 제공
* README 탭에서 구조 다이어그램이 시각적으로 표시
* 모든 시각화가 오류 없이 실행
* 교육생이 UI만으로 전체 데이터를 탐색 가능

---
