# Tasks: 대구 공공데이터 시각화 앱 v1.1 업그레이드

**Input**: Design documents from `/specs/002-app-v1-1-upgrade/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**Tests**: 수동 탐색적 테스트 (constitution에 따라 자동화 테스트 선택사항으로 제외)

**Organization**: 태스크는 User Story별로 그룹화되어 독립적 구현 및 테스트 가능

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: 병렬 실행 가능 (다른 파일, 의존성 없음)
- **[Story]**: 해당 User Story (US0, US1, US2, US3)
- 설명에 정확한 파일 경로 포함

## Path Conventions

- **Project Type**: Single project (Streamlit 웹 애플리케이션)
- **Source**: `app.py`, `utils/`
- **Specs**: `specs/002-app-v1-1-upgrade/`

---

## Phase 1: Setup (공유 인프라)

**Purpose**: 의존성 업데이트 및 session_state 초기화 구조 설정

- [X] T001 requirements.txt에 anthropic>=0.39.0 추가
- [X] T002 app.py에 session_state 초기화 함수 추가 (init_session_state)
- [X] T003 [P] utils/에 DATASET_MAPPING 상수 정의 (utils/constants.py 또는 app.py 상단)

---

## Phase 2: Foundational (기반 - 모든 User Story 차단)

**Purpose**: 모든 User Story 구현 전 반드시 완료해야 하는 핵심 인프라

**⚠️ 중요**: 이 Phase 완료 전까지 어떤 User Story도 시작할 수 없음

- [X] T004 [US0] app.py:54 - ZeroDivisionError 수정 (빈 dict 체크)
- [X] T005 [P] [US0] app.py:59,70,75 - deprecated width='stretch' → use_container_width=True 수정 (st.dataframe)
- [X] T006 [P] [US0] app.py:119,135 - deprecated width='stretch' → use_container_width=True 수정 (st.plotly_chart)
- [X] T007 [P] [US0] utils/visualizer.py:96 - mutable default argument 수정 (popup_cols=[] → popup_cols=None)
- [X] T008 [P] [US0] utils/geo.py:126 - mutable default argument 수정 (thresholds=[] → thresholds=None)
- [X] T009 [US0] app.py:336 - 함수 내부 import를 파일 상단으로 이동 (plotly.express)
- [X] T010 [US0] app.py - 숫자형/범주형 컬럼이 없을 때 안내 메시지 추가

**Checkpoint**: 버그 수정 완료 - Warning/Error 없이 앱 실행 가능

---

## Phase 3: User Story 1 - CSV 파일 업로드 및 데이터 탐색 (Priority: P1) 🎯 MVP

**Goal**: 사용자가 CSV 파일을 업로드하여 데이터를 탐색하고 시각화할 수 있음

**Independent Test**: 앱 실행 → 프로젝트 개요 탭에서 CSV 업로드 → 해당 탭에서 데이터 미리보기 표시 확인

### 3.1 데이터 로딩 모듈 수정

- [X] T011 [US1] utils/loader.py - read_uploaded_csv() 함수 추가 (업로드된 파일 인코딩 자동 감지)
- [X] T012 [US1] utils/loader.py - 기존 load_dataset() 함수를 session_state 기반으로 수정

### 3.2 탭 구조 재구성

- [X] T013 [US1] app.py - 탭 순서 변경: 프로젝트 개요를 첫 번째 탭으로 이동
- [X] T014 [US1] app.py - 탭 명칭 수정: "🚂 기차" → "📊 훈련 데이터", "📝 테스트" → "📋 테스트 데이터"
- [X] T015 [US1] app.py - "💬 데이터 질의응답" 탭 추가 (총 10개 탭 구성)

### 3.3 프로젝트 개요 탭 (업로드 허브)

- [X] T016 [US1] app.py - render_overview_tab() 함수 생성
- [X] T017 [US1] app.py - 각 데이터셋별 st.file_uploader 위젯 추가 (7개)
- [X] T018 [US1] app.py - 업로드 시 session_state에 데이터 저장 및 upload_status 업데이트
- [X] T019 [US1] app.py - 업로드된 파일명, 파일 크기, 행/컬럼 수 표시

### 3.4 데이터셋 탭 조건부 렌더링

- [X] T020 [US1] app.py - render_dataset_tab() 수정: upload_status 체크 추가
- [X] T021 [US1] app.py - 미업로드 시 "데이터를 먼저 업로드해주세요" 안내 메시지 표시
- [X] T022 [US1] app.py - 업로드된 데이터셋에서만 시각화 렌더링

### 3.5 교차 데이터 분석 탭 수정

- [X] T023 [US1] app.py - 교차 분석에서 근접성 분석 섹션 제거
- [X] T024 [US1] app.py - 통합 지도 시각화만 유지

**Checkpoint**: User Story 1 완료 - CSV 업로드 및 탐색 가능, 탭 전환 시 재로딩 없음

---

## Phase 4: User Story 2 - 다양한 시각화로 데이터 분석 (Priority: P2)

**Goal**: 히스토그램 외에 박스플롯, KDE, 산점도 등 다양한 차트 제공

**Independent Test**: 숫자형 컬럼이 있는 데이터셋 업로드 → 시각화 유형 드롭다운에서 각 차트 선택 → 정상 렌더링 확인

### 4.1 시각화 함수 확장

- [X] T025 [P] [US2] utils/visualizer.py - plot_boxplot() 함수 추가
- [X] T026 [P] [US2] utils/visualizer.py - plot_kde() 함수 추가 (plotly.figure_factory 사용)
- [X] T027 [P] [US2] utils/visualizer.py - plot_scatter() 함수 추가 (X, Y 컬럼 선택)
- [X] T028 [US2] utils/visualizer.py - plot_with_options() 통합 함수 생성 (차트 유형 분기)

### 4.2 시각화 UI 개선

- [X] T029 [US2] app.py - 숫자형 시각화 섹션에 차트 유형 선택 드롭다운 추가
- [X] T030 [US2] app.py - 산점도 선택 시 X축/Y축 컬럼 선택 UI 추가
- [X] T031 [US2] app.py - 차트 유형에 따른 시각화 함수 호출

### 4.3 결측치 경고 기능

- [X] T032 [US2] utils/visualizer.py - check_missing_ratio() 함수 추가 (30% 기준)
- [X] T033 [US2] app.py - 결측치 30% 이상 컬럼 선택 시 st.warning 표시

### 4.4 스타일 개선

- [X] T034 [US2] utils/visualizer.py - Plotly 색상 테마 개선 (plot_categorical_distribution)
- [X] T035 [US2] utils/visualizer.py - plot_numeric_distribution 색상/스타일 개선

**Checkpoint**: User Story 2 완료 - 4가지 차트 유형 렌더링 가능, 결측치 경고 표시

---

## Phase 5: User Story 3 - AI 챗봇으로 데이터 질의응답 (Priority: P3)

**Goal**: 업로드한 데이터에 대해 자연어로 질문하고 AI 답변 수신

**Independent Test**: API Key 입력 → 데이터셋 선택 → "이 데이터의 주요 특징은?" 질문 → 응답 확인

### 5.1 챗봇 모듈 생성

- [X] T036 [US3] utils/chatbot.py - 신규 파일 생성
- [X] T037 [US3] utils/chatbot.py - SYSTEM_PROMPT 상수 정의
- [X] T038 [US3] utils/chatbot.py - create_data_context() 함수 구현
- [X] T039 [US3] utils/chatbot.py - create_chat_response() 함수 구현 (Anthropic API 호출)
- [X] T040 [US3] utils/chatbot.py - 에러 핸들링 추가 (API Key 오류, 네트워크 오류, 타임아웃)

### 5.2 사이드바 구현

- [X] T041 [US3] app.py - 사이드바에 API Key 입력 필드 추가 (st.text_input, type="password")
- [X] T042 [US3] app.py - 사이드바에 AI 모델 선택 드롭다운 추가
- [X] T043 [US3] app.py - 사이드바에 토큰 사용량 표시 (전체/입력/출력)
- [X] T044 [US3] app.py - 사이드바에 데이터 업로드 현황 표시

### 5.3 데이터 질의응답 탭 구현

- [X] T045 [US3] app.py - render_chatbot_tab() 함수 생성
- [X] T046 [US3] app.py - 업로드된 데이터셋 선택 드롭다운
- [X] T047 [US3] app.py - 질문 입력 텍스트 영역 (st.text_area)
- [X] T048 [US3] app.py - 전송 버튼 및 응답 표시 영역
- [X] T049 [US3] app.py - 대화 이력 표시 (st.chat_message 사용)
- [X] T050 [US3] app.py - API Key 미입력 시 안내 메시지 표시

**Checkpoint**: User Story 3 완료 - AI 챗봇으로 데이터 질의응답 가능

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: 전체 기능 통합 및 품질 개선

- [X] T051 [P] app.py - 코드 정리 및 불필요한 import 제거
- [X] T052 [P] utils/__init__.py - 모듈 export 업데이트
- [X] T053 app.py - 전체 탭 통합 테스트 (10개 탭 정상 동작 확인)
- [X] T054 app.py - 빈 데이터셋, 숫자형만/범주형만 데이터셋 엣지 케이스 테스트
- [X] T055 quickstart.md 검증 - 모든 가이드 단계 정상 동작 확인

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1: Setup
    ↓ (T001-T003 완료)
Phase 2: Foundational (P0 버그 수정) ⚠️ BLOCKS ALL
    ↓ (T004-T010 완료)
Phase 3: User Story 1 (P1 업로드)  ←──┐
    ↓                                  │ (Foundational 완료 후 병렬 가능)
Phase 4: User Story 2 (P2 시각화)  ←──┤
    ↓                                  │
Phase 5: User Story 3 (P3 챗봇)   ←───┘
    ↓
Phase 6: Polish
```

### User Story Dependencies

| User Story | 의존성 | 독립 테스트 가능 |
|------------|--------|----------------|
| US0 (P0) | Setup 완료 | ✅ 앱 실행 시 Warning 없음 |
| US1 (P1) | Foundational 완료 | ✅ CSV 업로드 후 탐색 |
| US2 (P2) | Foundational 완료 + US1 권장 | ✅ 차트 유형 선택 후 렌더링 |
| US3 (P3) | Foundational 완료 + US1 필수 | ✅ API Key 입력 후 질의응답 |

### Within Each User Story

1. 모델/유틸 함수 먼저
2. 서비스 로직 다음
3. UI 컴포넌트 마지막
4. 스토리 완료 후 다음 우선순위로

### Parallel Opportunities

**Phase 2 (Foundational) 내 병렬:**
```
T005, T006, T007, T008 → 모두 다른 파일/라인, 동시 실행 가능
```

**Phase 4 (US2) 내 병렬:**
```
T025, T026, T027 → 모두 다른 함수, 동시 실행 가능
```

**Phase 5 (US3) 내 병렬:**
```
T041, T042, T043, T044 → 사이드바 요소, 순서 무관
```

---

## Parallel Example: Phase 2 (Foundational)

```bash
# 병렬 실행 가능한 버그 수정:
Task: "T005 - deprecated width='stretch' 수정 (st.dataframe)"
Task: "T006 - deprecated width='stretch' 수정 (st.plotly_chart)"
Task: "T007 - mutable default 수정 (visualizer.py)"
Task: "T008 - mutable default 수정 (geo.py)"
```

## Parallel Example: Phase 4 (User Story 2)

```bash
# 병렬 실행 가능한 시각화 함수:
Task: "T025 - plot_boxplot() 함수 추가"
Task: "T026 - plot_kde() 함수 추가"
Task: "T027 - plot_scatter() 함수 추가"
```

---

## Implementation Strategy

### MVP First (User Story 1만)

1. Phase 1: Setup 완료
2. Phase 2: Foundational (버그 수정) 완료 - **반드시 먼저!**
3. Phase 3: User Story 1 완료
4. **중단 및 검증**: CSV 업로드 및 탐색 독립 테스트
5. 배포/데모 준비 완료

### Incremental Delivery

1. Setup + Foundational → 안정적인 기반 확보
2. User Story 1 추가 → 독립 테스트 → **MVP 완성!**
3. User Story 2 추가 → 독립 테스트 → 시각화 다양화
4. User Story 3 추가 → 독립 테스트 → AI 챗봇 기능

### 권장 실행 순서

```
Day 1: T001 → T010 (Setup + Foundational)
Day 2: T011 → T024 (User Story 1)
Day 3: T025 → T035 (User Story 2)
Day 4: T036 → T050 (User Story 3)
Day 5: T051 → T055 (Polish)
```

---

## Summary

| 구분 | 태스크 수 |
|------|----------|
| Phase 1: Setup | 3 |
| Phase 2: Foundational (US0) | 7 |
| Phase 3: User Story 1 | 14 |
| Phase 4: User Story 2 | 11 |
| Phase 5: User Story 3 | 15 |
| Phase 6: Polish | 5 |
| **총계** | **55** |

**병렬 실행 기회**: 19개 태스크 ([P] 마커)

**MVP 범위**: Phase 1-3 완료 시 (24개 태스크)

---

## Notes

- [P] 태스크 = 다른 파일, 의존성 없음, 병렬 가능
- [USX] 레이블 = 해당 User Story 추적용
- 각 User Story는 독립적으로 완료 및 테스트 가능
- 태스크 완료 또는 논리적 그룹 완료 후 커밋
- 체크포인트에서 중단하여 스토리 독립 검증 가능
- 테스트는 constitution에 따라 수동 탐색적 테스트로 수행
