# 경북 공공데이터 시각화 및 AI 챗봇 개발 과정

## 교육 개요

경북 공공데이터를 바탕으로 데이터 분석, 시각화를 수행하고 최신 개발 방법론인 **SDD(Spec-Driven Development, 스펙주도개발)**를 활용하여 Streamlit 기반 데이터 시각화 앱을 구현합니다. 나아가 **언어모델과 Tool Calling**을 통해 자연어 기반으로 인터랙티브하게 데이터를 분석하는 AI 챗봇까지 개발합니다.

- **교육 기간**: 20일
- **실습 환경**: Google Colab, VS Code
- **핵심 기술**: Python, Streamlit, Anthropic Claude API, LangChain, LangGraph, pytest

### 핵심 키워드

| 분류 | 키워드 |
|:-----|:-------|
| 데이터 분석 | 데이터 기반 의사 결정, EDA, 데이터 시각화 |
| 모델링 | 설명력 높은 모델, R², AutoML |
| 웹 앱 개발 | Streamlit, cache, session_state 관리 |
| AI/LLM | LangChain, LangGraph, Tool Calling, Memory 관리 |
| 개발 방법론 | SDD (Spec-Driven Development), TDD (Test-Driven Development), Speckit |

---

## 커리큘럼 전체 구조

```
┌─────────────────────────────────────────────────────────────────────┐
│  Phase 1: 데이터 분석 기초 (1~4일차)                                  │
│  - 공공데이터 수집, EDA, 예측 모델링, AutoML                          │
├─────────────────────────────────────────────────────────────────────┤
│  Phase 2: Streamlit 앱 개발 (5~10일차)                               │
│  - SDD 방법론, Version 1.0 구현, 시각화 검증, Streamlit 심화 학습      │
├─────────────────────────────────────────────────────────────────────┤
│  Phase 3: AI 챗봇 통합 (11~15일차)                                   │
│  - 앱 업그레이드, Tool Calling, 메모리 관리, AI 에이전트 구현          │
├─────────────────────────────────────────────────────────────────────┤
│  Phase 4: 고도화 및 TDD (16~20일차)                                  │
│  - LangGraph 전환, ECLO 예측, 배포, TDD 방법론 적용                   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: 데이터 분석 기초 (1~4일차)

### 1일차: 데이터 수집 및 기초 시각화

**학습 목표**: 공공데이터포털 API를 활용한 데이터 수집 및 기본 시각화

| 주제 | 내용 |
|:-----|:-----|
| 데이터 수집 | 공공데이터포털 API Key 발급, API 호출로 데이터 수집 |
| 기초 시각화 | matplotlib, seaborn을 활용한 기본 차트 |
| 통계량 분석 | describe(), info() 등 기본 통계량 확인 |

**사용 데이터**: 한국도로공사 고속도로 교통사고 데이터

**실습 노트북**:
- `1_1_한국도로공사_고속도로_교통사고_데이터_불러오기.ipynb`
- `1_2_데이터_시각화_및_기본적_통계량.ipynb`

---

### 2일차: EDA 및 사고심각도 예측 모델 구축

**학습 목표**: 탐색적 데이터 분석(EDA)과 분류 모델 구축

| 주제 | 내용 |
|:-----|:-----|
| EDA 심화 | 변수 간 관계 분석, 이상치 탐지 |
| 파생변수 설계 | 사고심각도 변수 생성 |
| 분류 모델 | 모델 학습 및 평가 |

**실습 노트북**:
- `2_1_EDA_및_시각화_심화.ipynb`
- `2_2_사고심각도_예측_모델_구축.ipynb`

---

### 3일차: 사고발생이정 예측 모델 및 Dacon 경진대회

**학습 목표**: 회귀 모델 구축 및 AI 경진대회 참여 경험

| 주제 | 내용 |
|:-----|:-----|
| 변수 탐색 | 주요 변수 선택 및 설명력 분석 |
| 회귀 모델 | LinearRegression, RandomForest, XGBoost, LightGBM |
| Dacon 참여 | 대구 교통사고 피해 예측 AI 경진대회 |
| 평가 지표 | RMSLE (Root Mean Squared Log Error) |

**핵심 개념**: ECLO (Equivalent Casualty Level of Object) - 사고 피해 심각도 수치화 지표

**실습 노트북**:
- `3_1_사고발생이정_예측_모델_구축.ipynb`
- `3_2_데이콘_데이터_제출해보기.ipynb`

---

### 4일차: AutoML을 통한 모델링과 한계 파악

**학습 목표**: AutoML(AutoGluon)의 활용과 한계 이해

| 주제 | 내용 |
|:-----|:-----|
| AutoGluon | TabularPredictor 기본 사용법 |
| Presets | best_quality, medium_quality_faster_train |
| Multi-target | 여러 타깃 변수 동시 예측 |
| 한계점 | 블랙박스 특성, 학습 시간, 도메인 지식 반영 제한 |

**실습 노트북**:
- `4_도입_automl_경험해보기pynb.ipynb`
- `4_2_automl_좀더_자세히.ipynb`

---

## Phase 2: Streamlit 앱 개발 (5~10일차)

### 5일차: Claude Code와 SDD를 통한 App Version 1.0 구현

**학습 목표**: AI 기반 개발 도구와 SDD 방법론 적용

| 주제 | 내용 |
|:-----|:-----|
| Claude Code | AI 기반 코드 작성 도구 |
| GitHub Speckit | SDD(Spec-Driven Development) 방법론 |
| Version 1.0 | Streamlit 대시보드 초기 버전 구현 |

**핵심 산출물**:
- `spec.md`: 기능 명세서
- `plan.md`: 구현 계획
- `tasks.md`: 작업 목록

**참고 자료**: [GitHub Speckit](https://github.com/github/spec-kit)

---

### 6일차: Version 1.0 시각화 검증 (1/2)

**학습 목표**: Streamlit 대시보드 데이터 정합성 검증

| 주제 | 내용 |
|:-----|:-----|
| 데이터 로드 | head(), info(), describe() |
| 컬럼 분리 | select_dtypes()로 수치형/범주형 자동 분리 |
| 수치형 시각화 | 히스토그램, 박스플롯 |
| 범주형 시각화 | Bar Chart (상위 20개 카테고리) |

**검증 데이터**:
| 데이터 | 행 수 | 컬럼 수 |
|:-------|:------|:--------|
| train.csv | 39,609 | 23 |
| test.csv | 10,963 | 8 |
| countrywide_accident.csv | 602,775 | 23 |

**실습 노트북**:
- `6_2_train_데이터_검증하기.ipynb`
- `6_2_test_csv_분석하기.ipynb`
- `6_2_전국_사고_데이터.ipynb`

---

### 7일차: Version 1.0 시각화 검증 (2/2)

**학습 목표**: 위치 기반 데이터 지도 시각화

| 주제 | 내용 |
|:-----|:-----|
| 위도/경도 감지 | 다양한 컬럼명 후보 탐색 |
| Folium | 지도 시각화 라이브러리 |
| MarkerCluster | 마커 클러스터링 |

**검증 데이터**: 대구 시설물 데이터 (CCTV, 보안등, 주차장, 어린이보호구역)

**실습 노트북**:
- `7_1_대구_cctv_데이터_검증.ipynb`
- `7_1_보안등_데이터_구조.ipynb`
- `7_1_주차장_검증.ipynb`

---

### 8일차: Streamlit 기초 (01~05)

**학습 목표**: Streamlit 핵심 컴포넌트 익히기

| 예제 | 주제 | 핵심 함수 |
|:-----|:-----|:---------|
| 01 | 기본 설정 및 텍스트 | `st.set_page_config`, `st.title`, `st.markdown` |
| 02 | 레이아웃과 컬럼 | `st.columns`, `st.metric` |
| 03 | 데이터 표시 및 캐싱 | `st.dataframe`, `@st.cache_data` |
| 04 | 사용자 입력 | `st.selectbox`, `st.multiselect`, `st.button` |
| 05 | 확장 가능한 섹션 | `st.expander` |

---

### 9일차: Streamlit 중급 (06)

**학습 목표**: 탭 기반 네비게이션 구현

| 예제 | 주제 | 핵심 함수 |
|:-----|:-----|:---------|
| 06 | 탭 네비게이션 | `st.tabs` |

---

### 10일차: Streamlit 중급~고급 (07~14)

**학습 목표**: 차트, 지도, 세션 상태, 앱 확장

| 예제 | 주제 | 핵심 내용 |
|:-----|:-----|:---------|
| 07 | 상태 메시지 | `st.success`, `st.warning`, `st.error`, `st.info` |
| 08 | 로딩 스피너 | `st.spinner` |
| 09 | Plotly 차트 | bar, line, scatter, pie, histogram |
| 10 | Folium 지도 | `folium.Map`, `MarkerCluster` |
| 11 | 고급 통합 | 필터링 + 탭 + 차트 + 지도 |
| 12 | 완전한 대시보드 | 전체 앱 구조 이해 |
| 13 | 세션 상태 | `st.session_state`, 파일 업로드/다운로드 |
| 14 | 앱 확장 가이드 | 새 탭/기능 추가 방법 |

---

## Phase 3: AI 챗봇 통합 (11~15일차)

### 11일차: App Version 1.1.0 ~ 1.1.1 업그레이드

**학습 목표**: AI 챗봇 기능 추가 및 Tool Calling 도입

| 버전 | 핵심 변경사항 |
|:-----|:-------------|
| v1.1.0 | CSV 파일 업로드, session_state + cache, AI 챗봇 추가 |
| v1.1.1 | Claude 4.5 시리즈, **Tool Calling (15개 분석 도구)**, 스트리밍 응답 |

**Tool Calling 분석 도구 (v1.1.1)**:
- 데이터 정보: `get_dataframe_info`, `get_column_statistics`, `get_missing_values`
- 데이터 조작: `filter_dataframe`, `sort_dataframe`, `group_by_aggregate`
- 통계 분석: `get_correlation`, `get_outliers`, `calculate_percentile`
- 기타: `get_value_counts`, `get_unique_values`, `get_date_range`, `get_sample_rows`, `get_geo_bounds`, `cross_tabulation`

---

### 12일차: App Version 1.1.2 ~ 1.1.3 업그레이드

**학습 목표**: UX 개선 및 버그 수정

| 버전 | 핵심 변경사항 |
|:-----|:-------------|
| v1.1.2 | st.status로 도구 피드백 개선, 토큰 사용량 실시간 추출, **5개 분석 도구 추가** |
| v1.1.3 | Tool Calling 피드백 UI 수정, 탭 간소화, 지도 설정 기능 |

**추가된 분석 도구 (v1.1.2)**:
- `analyze_missing_pattern`: 결측값 패턴 분석
- `get_column_correlation_with_target`: 타겟 컬럼 상관관계
- `detect_data_types`: 데이터 타입 추론
- `get_temporal_pattern`: 시간 패턴 분석
- `summarize_categorical_distribution`: 범주형 분포 요약

---

### 13일차: Anthropic Claude Tool Calling

**학습 목표**: Tool Calling의 원리와 구현 방법 이해

| 노트북 | 주제 | 핵심 개념 |
|:-------|:-----|:---------|
| 13_01 | API 기본 호출 | `client.messages.create()`, 응답 구조 |
| 13_02 | Tool 정의 | JSON Schema, description 중요성, enum |
| 13_03 | Tool 실행 | **Agentic Loop**, `tool_result` 메시지 |
| 13_04 | 다중 Tool | 병렬 호출, 연쇄 호출 |

**Agentic Loop 흐름**:
```
사용자 질문 → Claude 분석 → stop_reason: "tool_use"
                ↓
        도구 실행 (execute_tool)
                ↓
        tool_result 메시지 추가
                ↓
Claude 최종 응답 → stop_reason: "end_turn"
```

---

### 14일차: LangChain & LangGraph 대화 메모리 관리

**학습 목표**: 4가지 메모리 관리 방식 이해 및 구현

| 노트북 | 메모리 방식 | 특징 |
|:-------|:-----------|:-----|
| 14_01 | Buffer Memory | 모든 대화 저장, 토큰 증가 |
| 14_02 | Window Memory | 최근 N개 유지, 오래된 정보 손실 |
| 14_03 | Summary Memory | LLM 요약 저장, 추가 호출 필요 |
| 14_04 | Hybrid Memory | Window + Summary 결합 |

**LangGraph 핵심 구성요소**:
- `StateGraph`: 상태 기반 그래프
- `add_messages`: 메시지 누적 Reducer
- `MemorySaver`: 메모리 체크포인터
- `SqliteSaver`: SQLite 영구 저장

---

### 15일차: LangGraph 메모리 관리 + Tool Calling 통합

**학습 목표**: 메모리 관리와 Tool Calling을 통합한 AI 에이전트 구현

| 노트북 | 메모리 + 도구 | 그래프 노드 |
|:-------|:-------------|:-----------|
| 15_01 | Buffer + Tool | chatbot, tools |
| 15_02 | Window + Tool | chatbot, tools, **window_memory** |
| 15_03 | Summary + Tool | chatbot, tools, **summarizer** |

**통합 도구 (5개)**:
- 커스텀: `get_current_time`, `calculator`, `random_number`
- 외부: `WikipediaQueryRun`, `DuckDuckGoSearchRun`

**그래프 구조 비교**:
```
Buffer:  START → chatbot ↔ tools → END
Window:  START → chatbot ↔ tools → window_memory → END
Summary: START → chatbot ↔ tools → summarizer → END
```

---

## Phase 4: 고도화 및 TDD (16~20일차)

### 16일차: App Version 1.2 - LangGraph 아키텍처 전환

**학습 목표**: LangGraph 기반 Tool Calling 아키텍처 전환 및 ECLO 예측 기능 통합

| 구분 | v1.1.3 | v1.2 |
|:-----|:-------|:-----|
| Tool Calling 방식 | Anthropic API 직접 호출 | LangChain + LangGraph |
| 도구 실행 노드 | 커스텀 루프 | LangGraph `ToolNode` |
| 상태 관리 | 수동 메시지 리스트 | `add_messages` Reducer |
| 패키지 관리 | pip | uv |
| ECLO 예측 | 미지원 | 대화형 예측 지원 |

**신규 모듈**:
- `utils/graph.py`: LangGraph 워크플로우 정의
- `utils/predictor.py`: ECLO 예측 모듈
- `utils/prompts.py`: 프롬프트 템플릿 분리

**ECLO 예측 필수 피처 (11개)**:
- 범주형: 기상상태, 노면상태, 도로형태, 사고유형, 시간대, 시군구, 요일
- 수치형: 사고시, 사고연, 사고월, 사고일

---

### 17일차: App Version 1.2.x - 점진적 개선

**학습 목표**: 버그 수정, 코드 품질 개선, UX 향상

| 버전 | 핵심 변경사항 |
|:-----|:-------------|
| v1.2.1 | uv 실행 오류 해결, API Key 검증, Streamlit 경고 처리 |
| v1.2.3 | 프롬프트 분리, README 도구 목록 상세화, 다중 ECLO 예측 |
| v1.2.5 | 테스트 데이터 헤더 수정, material 넘버링 통일 |
| v1.2.7 | 긴 표 expander 처리, 도구 목록 UI 개선 (22개) |

**핵심 개선 사항**:
- `use_container_width` → `width` 마이그레이션
- 다중 행 ECLO 예측 지원
- LangGraph 워크플로우 다이어그램 정교화

---

### 18일차: App Version 1.3 - Streamlit Cloud 배포

**학습 목표**: Streamlit Community Cloud 배포 준비 및 실행

| 구분 | v1.2.7 | v1.3 |
|:-----|:-------|:-----|
| 배포 환경 | 로컬 전용 | Streamlit Cloud |
| 데이터 전처리 | 부분 적용 | ML 모델용 전처리 완비 |
| 의존성 관리 | pyproject.toml | requirements.txt 동기화 |

**ML 모델 전처리 규칙**:
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

**v1.3.1 ~ v1.3.2 추가 개선**:
- 프로젝트 개요 문구 수정
- AI 응답 복사 버튼 추가 (마크다운 형태)
- 파일 위치 정리 (`syllabus.md`, `error_explanation.md`)

---

### 19일차: App Version 2.0 - TDD 방법론 문서화

**학습 목표**: 테스트 주도 개발(TDD) 방법론 이해 및 문서 작성

| 파일 | 설명 |
|:-----|:-----|
| `tests/principle.md` | TDD 방법론 원칙 |
| `tests/TEST_README_TEMPLATE.md` | 프로젝트별 TDD 룰 템플릿 |
| `tests/README.md` | 해당 프로젝트 TDD 룰 |
| `tests/workflow_template.yaml` | GitHub Actions CI/CD 템플릿 |

**TDD 핵심 원칙**:
1. Red: 실패하는 테스트 작성
2. Green: 테스트 통과하는 최소 코드 작성
3. Refactor: 코드 개선

---

### 20일차: App Version 2.0.1 - TDD 실제 적용

**학습 목표**: pytest 기반 테스트 코드 작성 및 커버리지 관리

**테스트 현황**:

| 지표 | 값 |
|:-----|:---|
| 총 테스트 | 320개 |
| 성공률 | 100% |
| 코드 커버리지 | 83.7% |

**pytest 마커 분류**:

| 마커 | 테스트 수 | 설명 |
|:-----|--------:|:-----|
| `@pytest.mark.api` | 24개 | 외부 API 호출 필요 |
| `@pytest.mark.slow` | 4개 | 실행 시간 10초+ |
| `@pytest.mark.integration` | 41개 | 모듈 간 통합 테스트 |

**테스트 파일 구조**:
```
tests/
├── test_preprocessing.py   # 전처리 모듈
├── test_loader.py          # 데이터 로더
├── test_tools.py           # 22개 분석 도구
├── test_predictor.py       # ECLO 예측
├── test_geo.py             # 지리 분석
├── test_visualizer.py      # 시각화
├── test_narration.py       # 내러티브 생성
├── test_graph.py           # LangGraph 워크플로우
├── test_prompts.py         # 프롬프트 검증
├── test_chatbot.py         # 챗봇 기능
└── integration/            # 통합 테스트
```

**테스트 실행 명령어**:
```bash
# 전체 테스트 (API 제외)
uv run pytest tests/ -v -m "not api"

# 커버리지 포함
uv run pytest tests/ --cov=utils --cov-report=term-missing

# 리포트 생성
uv run python scripts/generate_test_report.py
```

---

## 기술 스택 요약

### 데이터 분석
- pandas, numpy, matplotlib, seaborn
- scikit-learn, XGBoost, LightGBM, AutoGluon

### 시각화
- Plotly, Folium, streamlit-folium

### 웹 앱
- Streamlit (st.set_page_config, st.tabs, st.session_state, @st.cache_data)

### AI/LLM
- Anthropic Claude API (claude-haiku-4-5, claude-sonnet-4-5, claude-opus-4-5)
- LangChain (ChatAnthropic, @tool, InMemoryChatMessageHistory)
- LangGraph (StateGraph, ToolNode, MemorySaver, SqliteSaver)

### 개발 방법론
- SDD (Spec-Driven Development)
- GitHub Speckit (spec.md, plan.md, tasks.md)
- TDD (Test-Driven Development)
- Claude Code

### 테스트
- pytest, pytest-cov
- pytest 마커 (@pytest.mark.api, slow, integration)

---

## 최종 산출물

1. **Streamlit 데이터 시각화 앱 (v2.0.1)**
   - CSV 파일 업로드 지원
   - 수치형/범주형 자동 분류 및 시각화
   - Folium 지도 시각화
   - AI 챗봇 (LangGraph 기반 22개 분석 도구)
   - ECLO 예측 기능 (대화형 모델 실행)
   - Streamlit Cloud 배포

2. **AI 에이전트 프로토타입**
   - 메모리 관리 (Buffer, Window, Summary)
   - Tool Calling 통합
   - 자연어 기반 데이터 분석

3. **테스트 코드 및 TDD 체계**
   - pytest 마커 기반 테스트 분류
   - 테스트 리포트 자동 생성

---

## 학습 자료 경로

| 일차 | 경로 |
|:-----|:-----|
| 1~3일차 | `material/01-03/` |
| 3~7일차 | `material/03-07/` |
| 8~10일차 | `material/08-10/` |
| 11~12일차 | `material/11-12/` |
| 13일차 | `material/13/` |
| 14일차 | `material/14/` |
| 15일차 | `material/15/` |
| 16~20일차 | `material/16-20/` |

---

## 참고 자료

- [공공데이터포털](https://www.data.go.kr/)
- [Dacon](https://dacon.io/)
- [Streamlit 공식 문서](https://docs.streamlit.io/)
- [Anthropic Claude API](https://docs.anthropic.com/)
- [LangChain 문서](https://python.langchain.com/)
- [LangGraph 문서](https://langchain-ai.github.io/langgraph/)
- [GitHub Speckit](https://github.com/github/spec-kit)
- [uv 문서](https://docs.astral.sh/uv/)
- [pytest 문서](https://docs.pytest.org/)
