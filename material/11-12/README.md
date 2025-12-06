# 11-12일차: App 버전 업그레이드 (v1.1.0 ~ v1.1.3)

## 개요

Claude Code와 GitHub SpecKit을 활용하여 대구 공공데이터 시각화 앱의 버전을 v1.1.0에서 v1.1.3까지 업그레이드했습니다.

- **사용 도구**: Claude Code, GitHub SpecKit
- **참고 문서**: 프로젝트 루트 `README.md`, `docs/v1.1*` 디렉토리

---

## 버전별 학습 내용

### v1.1.0: 사용자 중심 개선

**핵심 변경사항**

| 영역 | v1.0 | v1.1 |
|:-----|:-----|:-----|
| 데이터 로딩 | 서버 내 고정 파일 경로 | CSV 파일 업로드 방식 |
| 성능 | 상호작용마다 재로딩 | `session_state` + `cache` 적용 |
| 시각화 | 히스토그램, bar chart | 박스플롯, KDE, 산점도 추가 |

**신규 기능**
- AI 데이터 질의응답: Anthropic Claude 기반 챗봇
- 사이드바: API Key 입력, 모델 선택, 토큰 사용량 표시

**참고 문서**: `docs/v1.1/app_improvement_proposal.md`

---

### v1.1.1: AI 분석 고도화

**핵심 변경사항**

| 영역 | v1.1 | v1.1.1 |
|:-----|:-----|:-------|
| AI 모델 | Claude 4 시리즈 | Claude 4.5 시리즈 |
| 챗봇 분석 | 샘플링 데이터 기반 | Tool Calling (15개 분석 도구) |
| 응답 출력 | 전체 완료 후 표시 | 스트리밍 실시간 출력 |
| 지도 렌더링 | 매번 새로 생성 | session_state 캐싱 |

**Tool Calling 분석 도구 (15개)**

| 도구 | 설명 |
|:-----|:-----|
| `get_dataframe_info` | DataFrame 기본 정보 |
| `get_column_statistics` | 컬럼별 통계 |
| `get_missing_values` | 결측치 현황 |
| `get_value_counts` | 값 분포 |
| `filter_dataframe` | 조건 필터링 |
| `sort_dataframe` | 정렬 |
| `get_correlation` | 상관관계 |
| `group_by_aggregate` | 그룹별 집계 |
| `get_unique_values` | 고유값 목록 |
| `get_date_range` | 날짜 범위 |
| `get_outliers` | 이상치 탐지 |
| `get_sample_rows` | 샘플 추출 |
| `calculate_percentile` | 백분위수 |
| `get_geo_bounds` | 지리적 범위 |
| `cross_tabulation` | 교차표 |

**참고 문서**: `docs/v1.1.1/app_improvement_proposal.md`

---

### v1.1.2: 사용자 경험 개선

**핵심 변경사항**

| 영역 | v1.1.1 | v1.1.2 |
|:-----|:-------|:-------|
| Tool Calling 피드백 | "도구 실행 중..." 단순 텍스트 | st.status로 도구명, 순번, 경과시간 표시 |
| 토큰 사용량 | 표시만 됨 | API 응답에서 실시간 추출 |
| 분석 도구 | 15개 | 20개 (+5개 추가) |

**추가된 분석 도구 (5개)**

| 도구 | 설명 |
|:-----|:-----|
| `analyze_missing_pattern` | 결측값 패턴 분석 (MCAR, MAR, MNAR 추정) |
| `get_column_correlation_with_target` | 타겟 컬럼과의 상관관계 분석 |
| `detect_data_types` | 컬럼별 실제 데이터 타입 추론 |
| `get_temporal_pattern` | 시간 관련 컬럼의 패턴 분석 |
| `summarize_categorical_distribution` | 범주형 컬럼 분포 요약 |

**참고 문서**: `docs/v1.1.2/app_improvement_proposal.md`

---

### v1.1.3: UI 간소화 및 버그 수정

**핵심 변경사항**

| 영역 | v1.1.2 | v1.1.3 |
|:-----|:-------|:-------|
| Tool Calling 피드백 | 응답 텍스트 위에 표시 (밀림 현상) | 응답 완료 후 expander로 요약 표시 |
| 탭 개수 | 10개 | 9개 (교차 데이터 분석 탭 삭제) |
| 지도 설정 | 없음 | 사이드바에서 최대 포인트 수 설정 |

**삭제된 섹션** (프로젝트 개요 탭)
- 주요 기능, 사용 방법, 시스템 구조
- 데이터 분석 기초 개념 (6개 expander)
- 분석 가이드 질문, 교차 데이터 분석의 중요성

**버그 수정**
- Tool Calling 피드백 위치 오류 수정

**참고 문서**: `docs/v1.1.3/app_improvement_proposal.md`

---

## 개발 도구 활용

### Claude Code

AI 기반 코드 작성 및 리팩토링 도구로, 다음 작업에 활용:
- 기능 요구사항 분석 및 구현
- 버그 수정 및 코드 최적화
- 문서 작성

### GitHub SpecKit

스펙 기반 개발 방법론으로, 다음 산출물 관리:
- `spec.md`: 기능 명세서
- `plan.md`: 구현 계획
- `tasks.md`: 작업 목록

**스펙 문서 위치**
- v1.1: `specs/002-app-v1-1-upgrade/`
- v1.1.1: `specs/003-app-v111-upgrade/`

---

## 학습 포인트 요약

| 버전 | 핵심 키워드 | 배운 것 |
|------|------------|---------|
| v1.1.0 | CSV 업로드, 캐싱, AI 챗봇 | Streamlit session_state, cache, Anthropic API |
| v1.1.1 | Tool Calling, 스트리밍 | Claude Function Calling, 실시간 응답 처리 |
| v1.1.2 | UX 개선, 도구 확장 | st.status, 토큰 사용량 추적 |
| v1.1.3 | UI 간소화, 버그 수정 | 사용자 피드백 반영, 코드 정리 |

---

## 참고 자료

- 프로젝트 README: `/README.md`
- v1.1 문서: `docs/v1.1/`
- v1.1.1 문서: `docs/v1.1.1/`
- v1.1.2 문서: `docs/v1.1.2/`
- v1.1.3 문서: `docs/v1.1.3/`
- GitHub SpecKit: https://github.com/github/spec-kit
