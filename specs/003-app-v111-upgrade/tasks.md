# Tasks: App v1.1.1 Upgrade

**Input**: Design documents from `/specs/003-app-v111-upgrade/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/tools.json

**Tests**: Manual testing only (Streamlit 앱 실행). 자동화된 테스트는 이 프로젝트에서 요구되지 않음 (Constitution 참조).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Project**: Repository root (Streamlit single application)
- Main: `app.py`
- Utils: `utils/chatbot.py`, `utils/visualizer.py`, `utils/tools.py` (신규)

---

## Phase 1: Setup

**Purpose**: 신규 파일 생성 및 기존 코드 확인

- [ ] T001 Create utils/tools.py skeleton file with module docstring and imports
- [ ] T002 [P] Verify anthropic>=0.39.0 in requirements.txt

---

## Phase 2: Foundational (P0 Bug Fixes)

**Purpose**: 앱의 기본 안정성 확보 - 모든 User Story 전에 반드시 완료

**⚠️ CRITICAL**: 이 Phase가 완료되어야 다른 기능 개발이 가능합니다.

### User Story 3 - 버그 수정 및 안정성 개선 (Priority: P0)

**Goal**: 빈 DataFrame이나 결측치가 많은 데이터를 업로드해도 오류 없이 앱을 사용할 수 있다.

**Independent Test**: 빈 CSV 파일 업로드 시 오류 메시지 없이 정상 처리 확인

- [ ] T003 [US3] Fix ZeroDivisionError in app.py:645 - add empty DataFrame check before division
- [ ] T004 [US3] Fix empty map rendering in utils/visualizer.py:321 - add early return with default Daegu center map
- [ ] T005 [US3] Fix NaN formatting error in utils/chatbot.py:51 - add NaN check before numeric formatting
- [ ] T006 [US3] Test bug fixes manually: upload empty CSV, CSV with all NaN coordinates

**Checkpoint**: 빈 데이터/NaN 데이터 업로드 시 오류 없이 동작해야 함

---

## Phase 3: User Story 4 - 최신 Claude 모델 선택 (Priority: P1)

**Goal**: 사이드바에서 최신 Claude 4.5 시리즈 모델을 선택 가능

**Independent Test**: 사이드바 모델 드롭다운에서 Claude 4.5 Sonnet, Opus, Haiku 선택 가능 확인

- [ ] T007 [US4] Update AI_MODEL_OPTIONS in app.py with Claude 4.5 series (Sonnet, Opus, Haiku)
- [ ] T008 [US4] Verify model selection in sidebar works correctly with new model IDs
- [ ] T009 [US4] Test model selection manually: select each model and verify in API call

**Checkpoint**: 사이드바에서 Claude 4.5 모델들이 표시되고 선택 가능해야 함

---

## Phase 4: User Story 1 - Tool Calling 기반 데이터 분석 질의 (Priority: P1) 🎯 MVP

**Goal**: AI 챗봇이 15개의 분석 도구를 활용하여 정확한 답변을 제공

**Independent Test**: 데이터 업로드 후 "이 데이터의 평균값은?" 질문으로 정확한 통계 결과 확인

### Implementation for User Story 1

#### Tool Definitions (utils/tools.py)

- [ ] T010 [P] [US1] Define TOOLS list with 15 tool schemas in utils/tools.py based on contracts/tools.json
- [ ] T011 [P] [US1] Implement get_dataframe_info handler in utils/tools.py
- [ ] T012 [P] [US1] Implement get_column_statistics handler in utils/tools.py
- [ ] T013 [P] [US1] Implement get_missing_values handler in utils/tools.py
- [ ] T014 [P] [US1] Implement get_value_counts handler in utils/tools.py
- [ ] T015 [P] [US1] Implement filter_dataframe handler in utils/tools.py
- [ ] T016 [P] [US1] Implement sort_dataframe handler in utils/tools.py
- [ ] T017 [P] [US1] Implement get_correlation handler in utils/tools.py
- [ ] T018 [P] [US1] Implement group_by_aggregate handler in utils/tools.py
- [ ] T019 [P] [US1] Implement get_unique_values handler in utils/tools.py
- [ ] T020 [P] [US1] Implement get_date_range handler in utils/tools.py
- [ ] T021 [P] [US1] Implement get_outliers handler in utils/tools.py
- [ ] T022 [P] [US1] Implement get_sample_rows handler in utils/tools.py
- [ ] T023 [P] [US1] Implement calculate_percentile handler in utils/tools.py
- [ ] T024 [P] [US1] Implement get_geo_bounds handler in utils/tools.py
- [ ] T025 [P] [US1] Implement cross_tabulation handler in utils/tools.py
- [ ] T026 [US1] Implement execute_tool dispatcher function in utils/tools.py

#### Tool Calling Logic (utils/chatbot.py)

- [ ] T027 [US1] Import TOOLS and execute_tool from utils/tools in utils/chatbot.py
- [ ] T028 [US1] Implement run_tool_calling function with max 3 iterations in utils/chatbot.py
- [ ] T029 [US1] Update create_chat_response to use tools parameter in utils/chatbot.py
- [ ] T030 [US1] Add tool_use detection and tool_result handling in utils/chatbot.py
- [ ] T031 [US1] Add error response for "현재 앱이 답변할 수 없는 질문입니다" in utils/chatbot.py
- [ ] T032 [US1] Add error response for "데이터와 관련 없는 질문" detection in utils/chatbot.py

#### App Integration (app.py)

- [ ] T033 [US1] Update render_chatbot_tab to use new Tool Calling chatbot in app.py
- [ ] T034 [US1] Test Tool Calling manually: ask "평균값", "그룹별 합계", "결측치 개수" questions

**Checkpoint**: Tool Calling으로 복잡한 질문에 정확한 답변 제공 (90% 이상 정확도)

---

## Phase 5: User Story 2 - 데이터셋별 대화 컨텍스트 분리 (Priority: P1)

**Goal**: 각 데이터셋에 대해 독립적인 대화 이력을 유지

**Independent Test**: CCTV 탭에서 질문 후 보안등 탭으로 전환, 다시 CCTV 탭으로 돌아왔을 때 이전 대화 이력 확인

### Implementation for User Story 2

- [ ] T035 [US2] Change chat_history structure from list to dict in init_session_state() in app.py
- [ ] T036 [US2] Add get_chat_history(dataset_name) helper function in app.py
- [ ] T037 [US2] Add clear_chat_history(dataset_name) helper function in app.py
- [ ] T038 [US2] Update render_chatbot_tab to use dataset-specific chat history in app.py
- [ ] T039 [US2] Update "대화 삭제" button to only clear current dataset history in app.py
- [ ] T040 [US2] Test context separation manually: chat in CCTV tab, switch to lights tab, return to CCTV

**Checkpoint**: 탭 전환 시 각 데이터셋의 대화 이력이 독립적으로 유지되어야 함

---

## Phase 6: User Story 6 - 지도 및 차트 캐싱 최적화 (Priority: P2)

**Goal**: 탭 전환이나 지도 인터랙션 시 불필요한 재렌더링 없이 빠른 응답

**Independent Test**: 지도 줌 인/아웃 시 전체 페이지 리렌더링 없음 확인

### Implementation for User Story 6

- [ ] T041 [P] [US6] Add map caching logic in render_dataset_tab with session_state key pattern in app.py
- [ ] T042 [P] [US6] Add returned_objects=[] parameter to st_folium calls in app.py
- [ ] T043 [P] [US6] Optimize iterrows to itertuples in create_folium_map in utils/visualizer.py:357
- [ ] T044 [P] [US6] Optimize iterrows to itertuples in create_overlay_map in utils/visualizer.py:475
- [ ] T045 [US6] Test caching manually: switch tabs and verify maps load instantly on return

**Checkpoint**: 탭 전환 시 지도 재렌더링 시간 1초 이내

---

## Phase 7: User Story 5 - 스트리밍 응답 출력 (Priority: P3)

**Goal**: 챗봇 응답이 실시간으로 스트리밍되어 긴 대기 시간 없이 응답 생성 과정을 확인

**Independent Test**: 질문 제출 후 응답 텍스트가 한 글자씩 나타나는 것 확인

### Implementation for User Story 5

- [ ] T046 [US5] Implement streaming response using client.messages.stream() in utils/chatbot.py
- [ ] T047 [US5] Add st.write_stream integration for text_stream in app.py render_chatbot_tab
- [ ] T048 [US5] Handle tool_use detection after streaming with get_final_message() in utils/chatbot.py
- [ ] T049 [US5] Test streaming manually: ask question and verify text appears character by character

**Checkpoint**: 스트리밍 응답의 첫 토큰 표시까지 지연 시간 500ms 이내

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: 최종 검증 및 정리

- [ ] T050 Update utils/__init__.py to export new tools module
- [ ] T051 Run full manual test: upload all 7 datasets, test chatbot with each
- [ ] T052 Verify all acceptance scenarios from spec.md pass
- [ ] T053 Code cleanup: remove unused imports, add missing docstrings

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - can start immediately
- **Phase 2 (P0 Bug Fixes)**: Depends on Setup - **BLOCKS all user stories**
- **Phase 3 (US4 Model Update)**: Depends on Phase 2 - Can run parallel with other P1 stories
- **Phase 4 (US1 Tool Calling)**: Depends on Phase 2 - Core feature, recommended first
- **Phase 5 (US2 Context Separation)**: Depends on Phase 2 - Can run parallel with US1
- **Phase 6 (US6 Caching)**: Depends on Phase 2 - Can run parallel with P1 stories
- **Phase 7 (US5 Streaming)**: Depends on Phase 4 (needs Tool Calling chatbot)
- **Phase 8 (Polish)**: Depends on all user stories

### User Story Dependencies

| User Story | Priority | Dependencies | Can Parallelize? |
|:-----------|:---------|:-------------|:-----------------|
| US3 (Bug Fix) | P0 | None | N/A (Foundational) |
| US4 (Model Update) | P1 | US3 | Yes |
| US1 (Tool Calling) | P1 | US3 | Yes |
| US2 (Context Separation) | P1 | US3 | Yes |
| US6 (Caching) | P2 | US3 | Yes |
| US5 (Streaming) | P3 | US1 | No (needs Tool Calling) |

### Within Each User Story

- Tool definitions [P] before dispatcher
- Chatbot changes before app.py integration
- Core implementation before optimization

### Parallel Opportunities

**Phase 4 (Tool Definitions)**:
```
# All 15 tool handlers can be implemented in parallel (T011-T025)
Task: T011 [P] [US1] Implement get_dataframe_info handler
Task: T012 [P] [US1] Implement get_column_statistics handler
Task: T013 [P] [US1] Implement get_missing_values handler
... (all handlers are independent)
```

**Phase 6 (Caching)**:
```
# All caching tasks are in different locations
Task: T041 [P] [US6] Add map caching in app.py
Task: T043 [P] [US6] Optimize iterrows in visualizer.py:357
Task: T044 [P] [US6] Optimize iterrows in visualizer.py:475
```

---

## Implementation Strategy

### MVP First (P0 + US1)

1. Complete Phase 1: Setup (T001-T002)
2. Complete Phase 2: Bug Fixes - US3 (T003-T006)
3. Complete Phase 4: Tool Calling - US1 (T010-T034)
4. **STOP and VALIDATE**: Tool Calling should work with basic queries
5. Deploy/demo if ready

### Incremental Delivery

1. Setup + Bug Fixes (P0) → Foundation ready
2. Add Model Update (US4) → Latest models available
3. Add Tool Calling (US1) → MVP! Core feature complete
4. Add Context Separation (US2) → Better UX for multi-dataset analysis
5. Add Caching (US6) → Performance improvement
6. Add Streaming (US5) → Final UX polish

---

## Summary

| Phase | User Story | Priority | Tasks | Parallel Tasks |
|:------|:-----------|:---------|:------|:---------------|
| 1 | Setup | - | 2 | 1 |
| 2 | US3 (Bug Fix) | P0 | 4 | 0 |
| 3 | US4 (Model Update) | P1 | 3 | 0 |
| 4 | US1 (Tool Calling) | P1 | 25 | 16 |
| 5 | US2 (Context Sep.) | P1 | 6 | 0 |
| 6 | US6 (Caching) | P2 | 5 | 4 |
| 7 | US5 (Streaming) | P3 | 4 | 0 |
| 8 | Polish | - | 4 | 0 |

**Total Tasks**: 53
**Parallel Opportunities**: 21 tasks (40%)
**MVP Scope**: Phase 1-2 + Phase 4 (US1) = 31 tasks

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Manual testing은 Constitution에 따라 수동 탐색적 테스트로 충분
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
