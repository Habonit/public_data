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

### v1.1 (현재)

**사용자 중심 개선** - CSV 업로드 방식 전환 및 AI 챗봇 도입

#### 주요 변경사항

| 영역 | v1.0 | v1.1 |
|:-----|:-----|:-----|
| **데이터 로딩** | 서버 내 고정 파일 경로 | CSV 파일 업로드 방식 |
| **성능** | 상호작용마다 재로딩 | `session_state` + `cache` 적용 |
| **시각화** | 히스토그램, bar chart | 박스플롯, KDE, 산점도 추가 |
| **시각화 스타일** | 기본 스타일 | Plotly 색상/스타일 개선 |
| **결측치 처리** | 테이블 표시만 | 30% 이상 시 warning 알림 |
| **탭 명칭** | "기차", "테스트" | "훈련 데이터", "테스트 데이터" |
| **교차 분석** | 근접성 분석 포함 | 통합 지도 시각화만 유지 |
| **프로젝트 개요** | 소개 페이지 | 데이터 업로드 허브 |

#### 신규 기능

- **AI 데이터 질의응답**: Anthropic Claude 기반 챗봇으로 데이터 분석 질문
- **사이드바**: API Key 입력, 모델 선택, 토큰 사용량, 업로드 현황 표시

#### 코드 품질 개선

- Deprecated API 수정 (`width='stretch'` → `use_container_width=True`)
- Mutable default argument 수정 (`[]` → `None`)
- ZeroDivisionError 방지 로직 추가

기준 문서: `docs/v1.1/app_improvement_proposal.md`
스펙 문서: `specs/002-app-v1-1-upgrade/`

---

### v1.0

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
| **시각화** | Plotly, Folium |
| **지도 연동** | streamlit-folium |
| **AI** | Anthropic Claude |
| **스펙 관리** | GitHub SpecKit |
| **개발 도구** | Claude Code |

---

## 문서

| 문서 | 설명 |
|------|------|
| `docs/v1.0/*.md` | v1.0 스펙 결정을 위한 최초 참고 문서 |
| `docs/v1.1/*.md` | v1.1 개선 제안서 및 노트 |
| `specs/001-daegu-data-viz/` | v1.0 스펙 산출물 (spec, plan, tasks) |
| `specs/002-app-v1-1-upgrade/` | v1.1 스펙 산출물 |
| `streamlit_study/` | Streamlit 학습 예제 (01~14번) |
