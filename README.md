# 대구 공공데이터 시각화

대구 지역 공공데이터를 탐색·분석하는 교육용 Streamlit 애플리케이션입니다.

데이터 출처: [DACON 대구 교통사고 피해 예측 AI 경진대회](https://dacon.io/competitions/official/236193/overview/description)

---

## 빠른 시작

```bash
# 1. 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. 의존성 설치
pip install -r requirements.txt

# 3. 앱 실행
streamlit run app.py
```

---

## 버전 히스토리

### v1.0 (현재) 

**기초 컨셉 구현** - 7개 공공데이터셋 개별 탐색 기능

- 데이터셋별 탭 구성 (CCTV, 보안등, 어린이보호구역, 주차장, 사고, train, test)
- 기본 통계 및 데이터 미리보기
- 숫자형/범주형 컬럼 히스토그램
- 좌표 기반 Folium 지도 시각화
- 교차 데이터 분석 (근접성 분석)
- 프로젝트 개요 탭

기준 문서: `docs/v1.0/*.md`
스펙 문서: `specs/001-daegu-data-viz/`

---

## Stack

이 프로젝트는 [GitHub SpecKit](https://github.com/github/spec-kit)을 활용한 스펙 기반 개발 연습과 데이터 시각화를 학습하기 위해 만들어졌습니다.

| 분류 | 기술 |
|------|------|
| **언어** | Python 3.10+ |
| **웹 프레임워크** | Streamlit |
| **데이터 처리** | pandas, numpy |
| **시각화** | Plotly, Matplotlib, Folium |
| **지도 연동** | streamlit-folium |
| **스펙 관리** | GitHub SpecKit |
| **개발 도구** | Claude Code |

---

## 문서

| 문서 | 설명 |
|------|------|
| `docs/v1.0/*.md` | v1.0 스펙 결정을 위한 최초 참고 문서 |
| `specs/001-daegu-data-viz/` | v1.0 스펙 산출물 (spec, plan, tasks) |
| `streamlit_study/` | Streamlit 학습 예제 (01~14번) |
