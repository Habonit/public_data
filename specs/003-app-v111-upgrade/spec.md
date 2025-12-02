# Feature Specification: App v1.1.1 Upgrade

**Feature Branch**: `003-app-v111-upgrade`
**Created**: 2025-12-02
**Status**: Draft
**Input**: `docs/v1.1.1/app_improvement_proposal.md` 기반 spec 작성

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Tool Calling 기반 데이터 분석 질의 (Priority: P1)

사용자는 업로드한 CSV 데이터에 대해 자연어로 질문하고, AI 챗봇이 15개의 분석 도구를 활용하여 정확한 답변을 제공받는다.

**Why this priority**: 기존 샘플링 방식의 가장 큰 한계점인 "복잡한 질의 응답 불가" 문제를 해결하는 핵심 기능. 데이터 분석 앱의 핵심 가치 제안.

**Independent Test**: 데이터 업로드 후 "이 데이터의 평균값은?" 질문으로 정확한 통계 결과 확인 가능

**Acceptance Scenarios**:

1. **Given** 사용자가 CSV 파일을 업로드한 상태, **When** "CCTV 설치 연도별 개수를 알려줘"라고 질문, **Then** `group_by_aggregate` 도구가 호출되어 연도별 집계 결과가 표시됨
2. **Given** 챗봇이 질문을 분석 중, **When** 복잡한 질문에 여러 도구가 필요, **Then** 최대 3회까지 도구를 순차 호출하여 답변 생성
3. **Given** 질문에 적합한 도구가 없음, **When** 3회 iteration 후에도 도구 미발견, **Then** "현재 앱이 답변할 수 없는 질문입니다." 메시지 표시
4. **Given** 데이터와 무관한 질문 (예: "오늘 날씨 어때?"), **When** 사용자가 질문 제출, **Then** "데이터와 관련 없는 질문에 대해서는 대답할 수 없습니다." 메시지 표시

---

### User Story 2 - 데이터셋별 대화 컨텍스트 분리 (Priority: P1)

사용자는 각 데이터셋(CCTV, 보안등, 사고 등)에 대해 독립적인 대화 이력을 유지하며, 탭 전환 시 해당 데이터셋의 이전 대화만 표시된다.

**Why this priority**: 여러 데이터셋을 분석할 때 컨텍스트 혼란을 방지하고, 데이터셋별 분석 흐름을 유지하기 위한 필수 기능

**Independent Test**: CCTV 탭에서 질문 후 보안등 탭으로 전환, 다시 CCTV 탭으로 돌아왔을 때 이전 대화 이력 확인

**Acceptance Scenarios**:

1. **Given** CCTV 탭에서 대화 진행 중, **When** 보안등 탭으로 전환, **Then** 보안등 탭의 별도 대화 이력 표시 (빈 상태 또는 이전 보안등 대화)
2. **Given** 보안등 탭에서 대화 후 CCTV 탭으로 복귀, **When** 대화 목록 확인, **Then** CCTV 탭의 이전 대화 이력 그대로 유지
3. **Given** 특정 데이터셋 탭에서, **When** "대화 삭제" 버튼 클릭, **Then** 해당 데이터셋의 대화 이력만 삭제 (다른 데이터셋 이력 유지)

---

### User Story 3 - 버그 수정 및 안정성 개선 (Priority: P0)

사용자는 빈 DataFrame이나 결측치가 많은 데이터를 업로드해도 오류 없이 앱을 사용할 수 있다.

**Why this priority**: P0 - 앱의 기본 안정성 확보. 오류 발생 시 사용자 신뢰도 하락 및 앱 사용 불가

**Independent Test**: 빈 CSV 파일 업로드 시 오류 메시지 없이 정상 처리 확인

**Acceptance Scenarios**:

1. **Given** 빈 DataFrame (행 0개), **When** 결측치 비율 계산 시도, **Then** ZeroDivisionError 없이 0% 표시
2. **Given** 모든 좌표값이 NaN인 데이터, **When** 지도 시각화 시도, **Then** 오류 없이 대구 중심 좌표의 빈 지도 표시
3. **Given** 모든 수치 컬럼이 NaN인 데이터, **When** 통계 정보 표시, **Then** "모든 값이 결측치입니다" 메시지 표시

---

### User Story 4 - 최신 Claude 모델 선택 (Priority: P1)

사용자는 사이드바에서 최신 Claude 4.5 시리즈 모델을 선택하여 더 나은 분석 결과를 얻을 수 있다.

**Why this priority**: 최신 모델의 향상된 추론 능력 활용으로 데이터 분석 품질 향상

**Independent Test**: 사이드바 모델 드롭다운에서 Claude 4.5 Sonnet, Opus, Haiku 선택 가능 확인

**Acceptance Scenarios**:

1. **Given** 앱 실행 상태, **When** 사이드바 모델 선택 드롭다운 클릭, **Then** Claude Sonnet 4.5, Opus 4.5, Haiku 4.5 옵션 표시
2. **Given** 모델 선택 후, **When** 질문 제출, **Then** 선택된 모델로 API 호출 수행

---

### User Story 5 - 스트리밍 응답 출력 (Priority: P3)

사용자는 챗봇 응답이 실시간으로 스트리밍되어 긴 대기 시간 없이 응답 생성 과정을 확인할 수 있다.

**Why this priority**: 사용자 경험 개선 - 체감 응답 속도 향상. 기능적 필수는 아니지만 UX 품질 향상

**Independent Test**: 질문 제출 후 응답 텍스트가 한 글자씩 나타나는 것 확인

**Acceptance Scenarios**:

1. **Given** 사용자가 질문 제출, **When** AI가 응답 생성 시작, **Then** 첫 토큰부터 실시간으로 화면에 표시
2. **Given** 스트리밍 응답 중, **When** 전체 응답 완료, **Then** 완성된 응답이 대화 이력에 저장

---

### User Story 6 - 지도 및 차트 캐싱 최적화 (Priority: P2)

사용자는 탭 전환이나 지도 인터랙션 시 불필요한 재렌더링 없이 빠른 응답을 경험한다.

**Why this priority**: 성능 개선 - 지도 마커가 많은 경우 체감 속도 저하 해결

**Independent Test**: 지도 줌 인/아웃 시 전체 페이지 리렌더링 없음 확인

**Acceptance Scenarios**:

1. **Given** 지도가 표시된 탭, **When** 줌 인/아웃 수행, **Then** 지도만 변경되고 페이지 리렌더링 없음
2. **Given** 데이터셋 탭 간 전환, **When** 이전에 본 탭으로 복귀, **Then** 캐싱된 지도 객체 사용으로 즉시 표시
3. **Given** 동일 조건의 차트 요청, **When** 차트 생성 시도, **Then** `@st.cache_data` 캐시 활용

---

### Edge Cases

- 빈 CSV 파일 업로드 시 어떻게 처리하나? -> ZeroDivisionError 방지 로직으로 안전 처리
- 모든 값이 NaN인 컬럼의 통계 요청 시? -> "모든 값이 결측치입니다" 메시지 표시
- Tool Calling 3회 iteration 후에도 답변 불가 시? -> "현재 앱이 답변할 수 없는 질문입니다." 메시지
- 데이터와 전혀 무관한 질문 시? -> "데이터와 관련 없는 질문에 대해서는 대답할 수 없습니다." 메시지
- 매우 큰 DataFrame (10만 행 이상)에서 Tool Calling 시? -> 도구별 적절한 샘플링/제한 로직 필요

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST 사이드바에서 Claude 4.5 시리즈 모델(Sonnet, Opus, Haiku) 선택 기능 제공
- **FR-002**: System MUST 15개의 데이터 분석 Tool Calling 도구 구현
  - `get_dataframe_info`, `get_column_statistics`, `get_missing_values`, `get_value_counts`, `filter_dataframe`, `sort_dataframe`, `get_correlation`, `group_by_aggregate`, `get_unique_values`, `get_date_range`, `get_outliers`, `get_sample_rows`, `calculate_percentile`, `get_geo_bounds`, `cross_tabulation`
- **FR-003**: System MUST 하나의 쿼리에서 최대 3회까지 Tool Calling iteration 수행
- **FR-004**: System MUST 도구 미발견 시 "현재 앱이 답변할 수 없는 질문입니다." 메시지 반환
- **FR-005**: System MUST 데이터 무관 질문 시 "데이터와 관련 없는 질문에 대해서는 대답할 수 없습니다." 메시지 반환
- **FR-006**: System MUST 데이터셋별로 독립적인 대화 이력 유지
- **FR-007**: System MUST 스트리밍 방식으로 챗봇 응답 출력
- **FR-008**: System MUST 빈 DataFrame에서 ZeroDivisionError 방지
- **FR-009**: System MUST 빈 좌표 데이터에서 기본 대구 중심 좌표로 빈 지도 표시
- **FR-010**: System MUST NaN 값에 대해 안전한 포맷팅 처리
- **FR-011**: System MUST 지도 객체를 `session_state`에 캐싱
- **FR-012**: System MUST `st_folium`에 `returned_objects=[]` 설정으로 리렌더링 방지

### Key Entities

- **Tool**: 15개 분석 도구 각각의 정의 (이름, 설명, 파라미터, 반환값)
- **ChatHistory**: 데이터셋별 대화 이력 딕셔너리 (`{dataset_name: [messages]}`)
- **MapCache**: 데이터셋별 캐싱된 Folium 지도 객체 (`{cache_key: folium.Map}`)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Tool Calling으로 "평균값", "그룹별 합계" 등 복잡한 질문에 정확한 답변 제공율 90% 이상
- **SC-002**: 빈 DataFrame 또는 전체 NaN 데이터 업로드 시 오류 발생율 0%
- **SC-003**: 탭 전환 시 지도 재렌더링 시간 1초 이내 (캐싱 적용 효과)
- **SC-004**: 스트리밍 응답의 첫 토큰 표시까지 지연 시간 500ms 이내
- **SC-005**: 데이터 무관 질문에 대해 100% 적절한 안내 메시지 표시
