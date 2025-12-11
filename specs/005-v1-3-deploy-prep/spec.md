# Feature Specification: v1.3 Streamlit Community 배포 준비

**Feature Branch**: `005-v1-3-deploy-prep`
**Created**: 2025-12-11
**Status**: Draft
**Input**: docs/v1.3/app_improvement_proposal.md 기반 - ML 전처리 개선, 프로젝트 개요 보강, 의존성 동기화

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 사고일시 데이터 자동 전처리 (Priority: P1)

학습자가 train 또는 test CSV 데이터를 업로드하면, 시스템이 자동으로 "사고일시" 컬럼을 파싱하여 연/월/일/시 및 시간대 분류 컬럼을 생성한다. 이를 통해 ML 모델이 필요로 하는 피처를 자동으로 준비할 수 있다.

**Why this priority**: ML 모델 추론의 핵심 입력 피처를 생성하는 기능으로, ECLO 예측 기능이 정상 동작하기 위한 필수 전처리이다.

**Independent Test**: train.csv를 업로드하고 "사고연", "사고월", "사고일", "사고시", "시간대" 컬럼이 자동 생성되는지 확인하면 독립적으로 검증 가능하다.

**Acceptance Scenarios**:

1. **Given** "사고일시" 컬럼이 포함된 train.csv가 있을 때, **When** 사용자가 훈련 데이터를 업로드하면, **Then** 시스템이 "사고연(int)", "사고월(int)", "사고일(int)", "사고시(int)", "시간대(str)" 5개 컬럼을 자동 생성한다.

2. **Given** "2022-01-01 08" 형식의 사고일시 값이 있을 때, **When** 전처리가 수행되면, **Then** 시간대가 "출근시간대"로 분류된다.

3. **Given** "2022-06-15 23" 형식의 사고일시 값이 있을 때, **When** 전처리가 수행되면, **Then** 시간대가 "심야"로 분류된다.

4. **Given** "사고일시" 컬럼이 없는 CSV가 있을 때, **When** 사용자가 데이터를 업로드하면, **Then** 시스템이 원본 데이터를 그대로 유지하고 에러 없이 처리한다.

---

### User Story 2 - 프로젝트 개요 정보 제공 (Priority: P2)

학습자가 앱에 처음 접속했을 때, 프로젝트의 교육 목적과 데이터 출처를 명확히 이해할 수 있도록 안내 정보를 제공한다. 데이터 다운로드 방법도 안내하여 학습자가 쉽게 데이터를 준비할 수 있도록 한다.

**Why this priority**: 사용자 온보딩과 데이터 준비를 돕는 기능으로, 핵심 기능은 아니지만 사용자 경험에 중요하다.

**Independent Test**: 앱 프로젝트 개요 탭에서 교육용 앱 설명, DACON 대회 링크, 데이터 업로드 안내가 표시되는지 확인하면 독립적으로 검증 가능하다.

**Acceptance Scenarios**:

1. **Given** 사용자가 앱에 접속했을 때, **When** 프로젝트 개요 탭을 볼 때, **Then** "교육용 Streamlit 애플리케이션" 설명이 표시된다.

2. **Given** 사용자가 프로젝트 개요 탭에 있을 때, **When** 데이터 출처 영역을 볼 때, **Then** DACON 대구 교통사고 피해 예측 AI 경진대회 링크가 표시된다.

3. **Given** 사용자가 데이터 업로드 영역을 볼 때, **When** 안내 문구를 읽을 때, **Then** 대회 페이지에서 데이터를 다운로드하여 업로드하라는 안내가 표시된다.

---

### User Story 3 - 안정적인 클라우드 배포 (Priority: P1)

앱이 Streamlit Community Cloud에서 모든 기능이 정상 동작하도록 의존성 패키지를 완전히 동기화한다. 특히 ML 관련 패키지(scikit-learn, lightgbm)가 누락되어 ECLO 예측 기능이 실패하는 문제를 해결한다.

**Why this priority**: 배포 환경에서 앱이 정상 동작해야 학습자들이 실제로 사용할 수 있으므로 핵심 우선순위이다.

**Independent Test**: Streamlit Community Cloud에 배포한 후 ECLO 예측 기능(AI 챗봇의 predict_eclo 도구)이 정상 동작하는지 확인하면 독립적으로 검증 가능하다.

**Acceptance Scenarios**:

1. **Given** 앱이 Streamlit Community Cloud에 배포되었을 때, **When** 사용자가 앱에 접속하면, **Then** 앱이 에러 없이 정상 로딩된다.

2. **Given** 배포된 앱에서 train 데이터가 업로드된 상태일 때, **When** AI 챗봇에 ECLO 예측을 요청하면, **Then** 예측 결과가 정상적으로 반환된다.

3. **Given** 앱이 배포된 상태에서, **When** 모든 데이터셋(CCTV, 보안등, 어린이보호구역, 주차장, 사고데이터, train, test)을 업로드하면, **Then** 각 탭의 시각화 기능이 정상 동작한다.

---

### Edge Cases

- **사고일시 형식 오류**: "사고일시" 컬럼 값이 예상 형식("yyyy-mm-dd HH")이 아닌 경우, 해당 행만 제외하고 나머지 데이터를 처리한다.
- **빈 데이터 업로드**: 빈 CSV 파일이 업로드된 경우, 친절한 에러 메시지를 표시한다.
- **시간대 경계값**: 시간 06:00, 10:00, 16:00, 20:00, 21:00 등 경계값에서 올바른 시간대로 분류되는지 확인한다.
- **ML 모델 파일 누락**: 모델 파일이 없는 경우 ECLO 예측 기능만 비활성화하고 다른 기능은 정상 동작한다 (Graceful Degradation).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: 시스템은 "사고일시" 컬럼이 포함된 CSV 업로드 시 자동으로 연/월/일/시 4개의 정수 컬럼을 생성해야 한다(MUST).
- **FR-002**: 시스템은 사고시 값을 기반으로 "시간대" 범주형 컬럼을 생성해야 한다(MUST). 분류 기준: 07-09시=출근시간대, 17-19시=퇴근시간대, 22-05시=심야, 그 외=일반시간대.
- **FR-003**: 시스템은 "사고일시" 컬럼이 없는 데이터에 대해 원본을 그대로 유지하고 에러 없이 처리해야 한다(MUST).
- **FR-004**: 프로젝트 개요 탭은 앱의 교육 목적을 설명하는 안내 문구를 표시해야 한다(MUST).
- **FR-005**: 프로젝트 개요 탭은 DACON 대회 페이지 링크를 포함한 데이터 출처 정보를 표시해야 한다(MUST).
- **FR-006**: 프로젝트 개요 탭은 데이터 다운로드 및 업로드 방법을 안내해야 한다(MUST).
- **FR-007**: requirements.txt는 pyproject.toml의 모든 의존성 패키지와 동기화되어야 한다(MUST). 특히 scikit-learn과 lightgbm이 포함되어야 한다.
- **FR-008**: 앱은 Streamlit Community Cloud 환경에서 모든 기능이 정상 동작해야 한다(MUST).
- **FR-009**: 전처리 함수는 원본 데이터를 변경하지 않고 복사본에서 작업해야 한다(MUST).
- **FR-010**: 날짜 파싱에 실패한 행은 적절한 경고 메시지와 함께 제외하고 나머지 데이터를 처리해야 한다(MUST).

### Key Entities

- **사고일시 원본**: "yyyy-mm-dd HH" 형식의 문자열 데이터. train/test CSV에 포함된 원본 컬럼.
- **파생 피처**: 사고일시에서 추출된 5개 컬럼 (사고연, 사고월, 사고일, 사고시, 시간대). ML 모델 입력으로 사용.
- **시간대 분류**: 4개 범주 (출근시간대, 퇴근시간대, 심야, 일반시간대). 사고시 값에 따라 결정.
- **의존성 패키지**: requirements.txt와 pyproject.toml에 정의된 패키지 목록. 배포 환경 동작에 필수.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: train/test 데이터 업로드 후 3초 이내에 전처리가 완료되어 파생 피처 5개가 생성된다.
- **SC-002**: 시간대 분류 정확도 100% - 모든 시간값이 정의된 규칙에 따라 올바르게 분류된다.
- **SC-003**: Streamlit Community Cloud 배포 후 앱의 모든 탭이 에러 없이 로딩된다.
- **SC-004**: 배포 환경에서 AI 챗봇의 ECLO 예측 도구가 정상적으로 예측 결과를 반환한다.
- **SC-005**: 프로젝트 개요 탭에서 DACON 링크 클릭 시 대회 페이지로 정상 이동한다.
- **SC-006**: 잘못된 형식의 사고일시 데이터가 포함된 경우에도 앱이 중단되지 않고 정상 동작한다 (Graceful Degradation).

## Assumptions

- 사고일시 데이터 형식은 "yyyy-mm-dd HH" (예: "2022-01-01 08")로 고정되어 있다.
- Streamlit Community Cloud는 requirements.txt를 기반으로 의존성을 설치한다.
- ML 모델 파일(model/*.pkl)은 이미 저장소에 포함되어 있다.
- DACON 대회 페이지 URL은 안정적으로 유지된다.
