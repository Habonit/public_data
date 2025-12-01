# daegu_plan.md  
대구 공공데이터 시각화 프로젝트 구현 계획(Plan)

본 문서는 `daegu_constitution.md`, `daegu_spec.md`를 기반으로  
Streamlit 앱을 **어떤 단계와 구조로 구현할 것인지**를 정의하는 구현 계획서이다.

코드 구현 전·중·후에 이 Plan을 계속 참조하며,  
Plan과 실제 코드가 괴리되지 않도록 유지한다.

---

## 1. 구현 목표 정리

- Streamlit 기반 단일 프로젝트에서
  - 각 CSV 데이터에 대한 **탭별 시각화 화면**
  - `train.csv`와 다른 공공데이터 간 **Cross-Data Analysis**
  - **Project Overview(README 탭)** 에서
    - 프로젝트 소개
    - 시스템 구조 다이어그램 (Mermaid)
    - 교육생 필수 개념(통계·데이터 분석 기본 개념)
  를 제공하는 애플리케이션을 구현한다.

- 지도 라이브러리: **folium** 사용
  - 교육용·직관적인 지도 표현을 목표로 선택
- 거리 계산 방식: **Haversine 공식** 사용
  - 위도·경도 기반 실제 거리(km) 단위 제공
- Overlay 지도: **레이어 ON/OFF 토글 제공**
  - train + 공공데이터를 같은 지도에 올리고, 체크박스로 표시/비표시 제어

---

## 2. 개발 단계(Phase) 계획

### Phase 0. 환경 세팅 및 데이터 확인
- Python 버전 및 가상환경 세팅
- `requirements.txt` 정의
- 업로드된 CSV들이 `/data` 폴더에 잘 들어오는지 확인
- 인코딩 문제(UTF-8/CP949) 테스트

### Phase 1. 프로젝트 스캐폴딩
- 디렉터리/파일 구조 생성
- `app.py` 기본 골격 및 Streamlit 탭/페이지 설정
- `utils/loader.py`, `utils/geo.py`, `utils/visualizer.py` 기본 함수 뼈대 구현

### Phase 2. 각 데이터 탭 기본 기능 구현
- CCTV, 보안등, 어린이 보호구역, 주차장, accident, train, test 탭
- 공통: 데이터 로딩, 기초 통계량, 기본 그래프, 지도 시각화

### Phase 3. Cross-Data Analysis 구현
- train ↔ 공공데이터/accident 관계 분석
- 근접성 계산(Haversine)
- Overlay 지도 및 레이어 토글
- 텍스트 기반 인사이트 출력

### Phase 4. Project Overview(README 탭) 구현
- 프로젝트 소개
- 시스템 구조 다이어그램(Mermaid)
- 교육생 필수 개념(통계/데이터 분석) 정리
- 전체 UI에서 한 번에 접근 가능하게 배치

### Phase 5. 리팩토링 및 검증
- 코드 모듈화·정리
- 캐싱 적용 및 성능 체크
- 간단한 테스트 시나리오 수행
- Spec/Constitution과의 일치 여부 점검

---

## 3. 기술 스택 및 라이브러리

- Python 3.10+
- Streamlit
- pandas, numpy
- plotly (기본 그래프)
- folium (지도 시각화)
- geopy 또는 Haversine 직접 구현(수학식)  
- (선택) geopandas: 향후 확장 고려용

---

## 4. 디렉터리 및 파일 구조 설계

```text
project-directory/
 ├─ app.py                      # 메인 엔트리, 탭 구성
 ├─ pages/                      # (선택) 다중 페이지 구조를 쓸 경우
 │    ├─ CCTV.py
 │    ├─ Lights.py
 │    ├─ SchoolZone.py
 │    ├─ Parking.py
 │    ├─ Accident.py
 │    ├─ Train.py
 │    ├─ Test.py
 │    └─ Cross_Analysis.py
 ├─ utils/
 │    ├─ loader.py             # 데이터 로딩/캐싱
 │    ├─ geo.py                # Haversine 거리 계산 및 좌표 관련 유틸
 │    ├─ visualizer.py         # 공통 그래프/지도 생성 함수
 │    └─ narration.py          # 텍스트 인사이트 생성용(간단 룰 기반)
 ├─ data/
 │    ├─ 대구 CCTV 정보.csv
 │    ├─ 대구 보안등 정보.csv
 │    ├─ 대구 어린이 보호 구역 정보.csv
 │    ├─ 대구 주차장 정보.csv
 │    ├─ countrywide_accident.csv
 │    ├─ train.csv
 │    └─ test.csv
 ├─ requirements.txt
 └─ docs/
      ├─ daegu_constitution.md
      ├─ daegu_spec.md
      └─ daegu_plan.md
````

> 단순화를 위해 초기에는 `app.py` 하나에 모든 탭을 구성하고,
> 필요 시 `pages/` 구조로 분리하는 방향으로 진행한다.

---

## 5. 모듈별 책임 정의

### 5.1 `utils/loader.py`

**목표:** CSV 로딩과 캐싱을 담당

주요 함수:

* `read_csv_safe(path: str) -> pd.DataFrame`

  * 인코딩 후보(utf-8, utf-8-sig, cp949) 순차 시도
  * 실패 시 예외 발생
* `load_dataset(name: str) -> pd.DataFrame`

  * `"cctv"`, `"lights"`, `"schoolzone"`, `"parking"`, `"accident"`, `"train"`, `"test"` 등의 키로 분기
  * `@st.cache_data` 적용

### 5.2 `utils/geo.py`

**목표:** 좌표 처리 및 거리 계산 담당

주요 함수:

* `detect_lat_lng_columns(df: pd.DataFrame) -> tuple[str|None, str|None]`

  * 컬럼명 후보 리스트 기반 자동 탐지
* `haversine_distance(lat1, lon1, lat2, lon2) -> float`

  * km 단위 Haversine 거리 계산
* `compute_nearest_counts(df_base, df_target, thresholds=[0.5, 1.0, 2.0])`

  * base 각 포인트에 대해 target과의 거리 계산
  * threshold 별로 카운트/요약 통계 반환

### 5.3 `utils/visualizer.py`

**목표:** 공통 그래프 및 지도 렌더링

주요 함수:

* `plot_numeric_distribution(df, col)`
* `plot_categorical_distribution(df, col)`
* `create_folium_map(points: pd.DataFrame, lat_col, lng_col, color, popup_cols=[])`
* `create_overlay_map(base_points, overlay_points_list, layer_names)`

### 5.4 `utils/narration.py`

**목표:** 간단한 규칙 기반 인사이트 문장 생성

주요 함수:

* `summarize_proximity_stats(stats_dict) -> str`

  * 예: “500m 이내 CCTV가 평균 3개 이상 존재합니다.”
* `summarize_distribution_diff(df1, df2, col) -> str`

  * 히스토그램 결과를 요약

---

## 6. 탭별 구현 계획

### 6.1 공통 UI 패턴

각 탭의 상단:

* 제목 + 설명 문구
* 데이터 선택/필터 옵션(필요 시)
* `st.expander("데이터 개요")` 안에

  * head()
  * shape, dtypes
  * 결측치 비율 테이블
  * describe() 결과

중간:

* 수치형/범주형 컬럼 선택용 `selectbox` 또는 `multiselect`
* 선택된 컬럼에 따라 히스토그램/막대 그래프 출력

하단:

* 지도 시각화 (좌표 존재 시)

  * `folium.Map` + MarkerCluster 또는 CircleMarker
  * `st_folium` 등을 활용해 Streamlit에 렌더링

---

### 6.2 CCTV 탭

데이터:

* `대구 CCTV 정보.csv`

구현 항목:

* CCTV 위치 지도
* 행정동별 CCTV 개수 bar chart
* 설치 용도/유형별 분포

---

### 6.3 보안등 탭

데이터:

* `대구 보안등 정보.csv`

구현 항목:

* 보안등 위치 지도
* 도로 구분/구역별 보안등 개수
* 야간 안전장치로서의 분포 해석용 그래프

---

### 6.4 어린이 보호구역 탭

데이터:

* `대구 어린이 보호 구역 정보.csv`

구현 항목:

* 보호구역 위치 지도
* 학교/유형별 분포
* 면적/길이(존재 시) 관련 히스토그램

---

### 6.5 주차장 탭

데이터:

* `대구 주차장 정보.csv`

구현 항목:

* 주차장 위치 지도
* 공영/민영, 지상/지하 등 분류별 분포
* 주차면 수 분포 히스토그램

---

### 6.6 Accident 탭

데이터:

* `countrywide_accident.csv`

구현 항목:

* 사고 위치 지도(필요 시 대구 지역만 필터)
* 사고 유형·시간대·요일 분포 그래프
* train 데이터와의 연계를 염두에 둔 기본 통계

---

### 6.7 train / test 탭

데이터:

* `train.csv`, `test.csv`

구현 항목:

* 주요 feature 분포 확인(수치형/범주형)
* 특정 위치/시간 정보를 포함한다면 지도 또는 시간대별 그래프
* test는 train의 분포와 비교하는 시각화(겹친 히스토그램 등)

---

## 7. Cross-Data Analysis 구현 계획

### 7.1 UI 구성

* 상단: 설명 문구

  * "train 데이터와 다른 공공데이터 간의 공간적 관계를 분석합니다."
* 좌측 또는 상단 컨트롤:

  * **중심 데이터 선택**: 기본값 `train`
  * **비교 데이터 선택**: CCTV / 보안등 / 보호구역 / 주차장 / accident
  * 거리 임계값 선택: 0.5km / 1km / 2km (multiselect 또는 slider)
* 레이아웃:

  * 좌: 지도(Overlay)
  * 우: 통계 요약 + 인사이트 텍스트

### 7.2 알고리즘(로직) 단계

1. 중심 데이터셋(df_base = train) 로드
2. 비교 대상 데이터셋(df_target) 로드
3. 각 데이터에서 위도·경도 컬럼 자동 감지
4. 좌표가 없으면 경고 메시지 출력 후 종료
5. Haversine 거리 계산

   * 간단한 샘플링(예: train 1000건 이하로 제한) 적용 가능
6. threshold 별:

   * 각 train 포인트 기준, target 포인트가 반경 내 몇 개 있는지 카운트
   * 전체 평균/중앙값/최댓값 계산
7. Folium 지도 생성:

   * 레이어 1: train 포인트(예: 파란색)
   * 레이어 2: target 포인트(예: 빨간색)
   * LayerControl 추가 → 사용자가 ON/OFF 할 수 있도록 구현
8. Narration:

   * 통계 결과를 `narration.summarize_proximity_stats`로 요약
   * README에서 설명한 개념(분포, 상관성 등)을 연결한 문장 제공

### 7.3 확대 계획 (선택)

* heatmap 추가 (Folium HeatMap)
* 시간대별 사고 heatmap (accident 데이터)

---

## 8. Project Overview(README) 탭 구현 계획

### 8.1 섹션 구성

1. 프로젝트 소개

   * 목적, 사용 데이터, 사용 기술, 학습 목표
2. 시스템 구조 다이어그램

   * mermaid 문법 그대로 `st.markdown("""```mermaid ...```""")` 로 렌더링
3. 교육생 필수 개념

   * 데이터 타입, 기초 통계량, 결측치, 이상치, 분포, 좌표, 상관성 등
   * 개념별로 소제목과 짧은 설명
4. 사용 방법 요약

   * “탭을 이렇게 이동하면서 이런 질문을 던져보라”는 가이드

### 8.2 예시 구현 흐름

````python
def render_project_overview():
    st.title("대구 공공데이터 시각화 프로젝트 개요")
    st.markdown("프로젝트 목적 …")

    with st.expander("시스템 구조 다이어그램 보기"):
        st.markdown(\"\"\"```mermaid
        (mermaid 코드)
        ```\"\"\")

    st.header("데이터 분석 기초 개념")
    # (필수 개념들 bullet 형식으로)
````

---

## 9. 테스트 및 검증 계획

### 9.1 기본 동작 테스트

* [ ] 각 탭에서 데이터 로딩 시 에러 없는지
* [ ] describe, 결측치 테이블 정상 출력
* [ ] 그래프/지도 렌더링 확인

### 9.2 Cross-Analysis 테스트

* [ ] train ↔ CCTV 근접성 계산 시 결과 표/텍스트 출력
* [ ] 레이어 토글 동작 확인
* [ ] train ↔ 보안등 / 보호구역 / 주차장 / accident 모두 시나리오별 테스트

### 9.3 교육 관점 검증

* [ ] README 탭에서 개념 설명이 지나치게 어렵지 않은지
* [ ] 데이터 초보자가 “어디를 먼저 눌러야 할지” 직관적으로 알 수 있는지
* [ ] 최소 1~2개의 “프로젝트 아이디어 예시”를 말로 설명해 줄 수 있을 정도로 인사이트가 나오는지

---

## 10. Definition of Done 재확인

이 Plan의 구현이 완료되었다고 판단할 기준:

1. Constitution / Spec에 정의된 모든 탭과 기능이 동작한다.
2. `train ↔ 공공데이터` 관계 분석이 지도·통계·텍스트로 모두 표현된다.
3. Project Overview 탭에서

   * 프로젝트 소개
   * 구조 다이어그램
   * 데이터 분석 기초 개념
     이 모두 확인 가능하다.
4. 교육생이 별도 세팅 지식 없이 README(Constitution)대로 따라 했을 때
   Streamlit 앱 실행 및 전 탭 탐색이 가능하다.

---
