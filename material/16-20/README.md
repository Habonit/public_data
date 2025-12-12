# 16-20일차: App 버전 업그레이드 및 TDD 적용 (v1.2 ~ v2.0.1)

## 개요

Claude Code를 활용하여 대구 공공데이터 시각화 앱을 v1.2에서 v2.0.1까지 업그레이드했습니다. LangGraph 기반 아키텍처 전환, ECLO 예측 기능 통합, Streamlit 배포 준비, 그리고 TDD 방법론 적용까지 진행했습니다.

- **사용 도구**: Claude Code
- **참고 문서**: `docs/v1.2*`, `docs/v1.3*`, `docs/v2.0*` 디렉토리

---

## 버전별 학습 내용

### v1.2: LangGraph 아키텍처 전환

**핵심 변경사항**

| 영역 | v1.1.3 | v1.2 |
|:-----|:-------|:-----|
| Tool Calling 방식 | Anthropic API 직접 호출 | LangChain + LangGraph |
| 도구 실행 노드 | 커스텀 루프 | LangGraph `ToolNode` |
| 상태 관리 | 수동 메시지 리스트 | `add_messages` Reducer |
| 패키지 관리 | pip | uv |
| ECLO 예측 | 미지원 | 대화형 예측 지원 |

**신규 파일 구조**

```
utils/
├── graph.py          # LangGraph 워크플로우 정의
├── predictor.py      # ECLO 예측 모듈
└── prompts.py        # 프롬프트 템플릿 분리
```

**ECLO 예측 필수 피처 (11개)**

| 피처 | 타입 | 설명 |
|:-----|:-----|:-----|
| 기상상태 | 범주형 | 맑음, 흐림, 비, 눈 등 |
| 노면상태 | 범주형 | 건조, 젖음, 적설 등 |
| 도로형태 | 범주형 | 직선, 곡선, 교차로 등 |
| 사고유형 | 범주형 | 차대차, 차대사람 등 |
| 시간대 | 범주형 | 새벽, 아침, 낮, 저녁 등 |
| 시군구 | 범주형 | 대구 시군구 |
| 요일 | 범주형 | 월~일 |
| 사고시 | 수치형 | 0-23 |
| 사고연 | 수치형 | 연도 |
| 사고월 | 수치형 | 1-12 |
| 사고일 | 수치형 | 1-31 |

**참고 문서**: `docs/v1.2/app_improvement_proposal.md`

---

### v1.2.1 ~ v1.2.7: 점진적 개선

**v1.2.1: 환경 설정 버그 수정**
- `uv run streamlit` 실행 오류 해결
- API Key 유효성 검증 개선
- Streamlit 경고 메시지 처리 (`use_container_width` → `width`)

**v1.2.3: 코드 품질 개선**
- 프롬프트를 `prompts.py`로 분리
- README에 도구 목록 상세 작성
- 다중 ECLO 예측 지원 (N개 데이터 추론)

**v1.2.5: 구조 정리**
- 테스트 데이터 헤더 표시 수정
- `material/` 디렉토리 넘버링 통일 (01-03, 03-07, ...)

**v1.2.7: UX 개선**
- 긴 표를 `st.expander`로 토글 처리
- 프로젝트 개요 도구 목록 UI 개선 (22개 도구)
- LangGraph 워크플로우 다이어그램 정교화

---

### v1.3: Streamlit Cloud 배포 준비

**핵심 변경사항**

| 영역 | v1.2.7 | v1.3 |
|:-----|:-------|:-----|
| 배포 환경 | 로컬 전용 | Streamlit Cloud |
| 데이터 전처리 | 부분 적용 | ML 모델용 전처리 완비 |
| 의존성 관리 | pyproject.toml | requirements.txt 동기화 |

**ML 모델 전처리 규칙**

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

- `사고일시` → `사고연`, `사고월`, `사고일`, `사고시`, `요일`, `시간대` 분리

**프로젝트 개요 업데이트**
- 데이터 출처: DACON 대구 교통사고 피해 예측 AI 경진대회
- 데이터 준비 방법 안내 추가

**참고 문서**: `docs/v1.3/app_improvement_proposal.md`

---

### v1.3.1 ~ v1.3.2: 배포 후 개선

**v1.3.1: UI 문구 수정**
- 프로젝트 개요 탭 문구 개선
- AI 응답 복사 버튼 추가 (마크다운 형태)
- Streamlit 경고 메시지 제거
- 버전 히스토리 v1.3 반영

**v1.3.2: 프로젝트 구조 정리**
- `syllabus.md` → `material/syllabus.md` 이동
- `docs/error_explanation.md` → `tests/error_explanation.md` 이동
- 경로 참조 전체 업데이트

---

### v2.0: TDD 방법론 문서화

**핵심 목표**

| 영역 | 이전 | v2.0 |
|:-----|:-----|:-----|
| 테스트 코드 | 없음 | TDD 방법론 문서 작성 |
| 코드 변경 관리 | Side effect 예측 불가 | 테스트 기반 검증 |

**생성된 TDD 문서**

| 파일 | 설명 |
|:-----|:-----|
| `tests/principle.md` | TDD 방법론 원칙 |
| `tests/TEST_README_TEMPLATE.md` | 프로젝트별 TDD 룰 템플릿 |
| `tests/README.md` | 해당 프로젝트 TDD 룰 |
| `tests/workflow_template.yaml` | GitHub Actions CI/CD 템플릿 |

**참고 문서**: `docs/v2.0/app_improvement_proposal.md`

---

### v2.0.1: TDD 실제 적용

**핵심 작업**

테스트 코드 작성 및 검증:
1. P0 모듈 단위 테스트 (preprocessing, loader, tools, predictor, geo)
2. P1 모듈 단위 테스트 (visualizer, narration, graph, prompts, chatbot)
3. 통합 테스트 (INT-001 ~ INT-005)
4. 테스트 커버리지 리포트 자동 생성

**테스트 현황**

| 지표 | 값 |
|:-----|:---|
| 총 테스트 | 320개 |
| 성공률 | 100% |
| 코드 커버리지 | 83.7% |

**pytest 마커 분류**

| 마커 | 테스트 수 | 설명 |
|:-----|--------:|:-----|
| `@pytest.mark.api` | 24개 | 외부 API 호출 필요 |
| `@pytest.mark.slow` | 4개 | 실행 시간 10초+ |
| `@pytest.mark.integration` | 41개 | 모듈 간 통합 테스트 |

**생성된 테스트 파일**

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

**테스트 리포트 생성**

```bash
# 테스트 실행 (API 테스트 제외)
uv run pytest tests/ -v -m "not api"

# 커버리지 포함 실행
uv run pytest tests/ --cov=utils --cov-report=term-missing

# 마크다운 리포트 생성
uv run python scripts/generate_test_report.py
```

**참고 문서**: `docs/v2.0.1/app_improvement_proposal.md`

---

## 학습 포인트 요약

| 버전 | 핵심 키워드 | 배운 것 |
|------|------------|---------|
| v1.2 | LangGraph, ECLO, uv | StateGraph, ToolNode, 대화형 예측 |
| v1.2.x | 점진적 개선 | 프롬프트 분리, UX 개선, 다중 예측 |
| v1.3 | 배포 준비 | Streamlit Cloud, 전처리, requirements.txt |
| v1.3.x | 배포 후 개선 | UI 문구, 프로젝트 구조 정리 |
| v2.0 | TDD 문서화 | 테스트 방법론, CI/CD 템플릿 |
| v2.0.1 | TDD 적용 | pytest, 커버리지, 마커 분류 |

---

## 주요 기술 스택 변화

| 영역 | v1.1.3 | v2.0.1 |
|:-----|:-------|:-------|
| Tool Calling | Anthropic API | LangChain + LangGraph |
| 패키지 관리 | pip | uv |
| 테스트 | 없음 | pytest + coverage |
| 배포 | 로컬 | Streamlit Cloud |
| 문서화 | README만 | TDD 방법론 포함 |

---

## 참고 자료

- 프로젝트 README: `/README.md`
- v1.2 ~ v1.2.7 문서: `docs/v1.2*/`
- v1.3 ~ v1.3.2 문서: `docs/v1.3*/`
- v2.0 ~ v2.0.1 문서: `docs/v2.0*/`
- TDD 방법론: `tests/principle.md`
- 테스트 리포트: `tests/result/{yyyy_mm_dd_HH_MM}/test_report.md`
- LangGraph 문서: https://langchain-ai.github.io/langgraph/
- uv 문서: https://docs.astral.sh/uv/
