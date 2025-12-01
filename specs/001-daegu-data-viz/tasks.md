# Tasks: Daegu Public Data Visualization

**Feature**: 001-daegu-data-viz
**Input**: Design documents from `/specs/001-daegu-data-viz/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Manual exploratory testing per constitution. No automated tests required.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Single Streamlit application structure
- Root: `app.py`, `utils/`, `data/`, `requirements.txt`
- Paths assume repository root as working directory

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project directory structure (utils/, data/, docs/, specs/001-daegu-data-viz/)
- [X] T002 Create requirements.txt with dependencies (streamlit>=1.28.0, pandas>=2.0.0, numpy>=1.24.0, plotly>=5.17.0, folium>=0.14.0, streamlit-folium>=0.15.0)
- [X] T003 [P] Create empty utility module files (utils/loader.py, utils/geo.py, utils/visualizer.py, utils/narration.py)
- [X] T004 [P] Create __init__.py files for utils package (utils/__init__.py)

**Checkpoint**: Project structure ready for implementation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Implement read_csv_safe() function with encoding fallback (UTF-8 → UTF-8-SIG → CP949) in utils/loader.py
- [X] T006 Implement load_dataset() function with @st.cache_data decorator and dataset name mapping in utils/loader.py
- [X] T007 Implement get_dataset_info() function for statistical summary generation in utils/loader.py
- [X] T008 [P] Implement detect_lat_lng_columns() function for coordinate auto-detection in utils/geo.py
- [X] T009 [P] Implement haversine_distance() function with Earth radius 6371km in utils/geo.py
- [X] T010 [P] Implement validate_coordinates() function with Daegu bounds validation in utils/geo.py
- [X] T011 Create app.py with basic Streamlit configuration (page title, layout, initial imports)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Explore Individual Dataset (Priority: P1) 🎯 MVP

**Goal**: Enable learners to view and understand each public dataset individually with statistics, visualizations, and maps

**Independent Test**: Load application, select any dataset tab (CCTV, Security Lights, Child Protection Zones, Parking Lots, Accident, Train, or Test), verify that basic statistics, visualizations, and geographic data display without errors

### Implementation for User Story 1

- [X] T012 [P] [US1] Implement plot_numeric_distribution() function for histogram generation in utils/visualizer.py
- [X] T013 [P] [US1] Implement plot_categorical_distribution() function for bar chart generation with top_n limiting in utils/visualizer.py
- [X] T014 [P] [US1] Implement create_folium_map() function with MarkerCluster for single dataset visualization in utils/visualizer.py
- [X] T015 [US1] Create main tab structure in app.py with st.tabs() for 9 tabs (CCTV, Security Lights, Child Protection Zones, Parking Lots, Accident, Train, Test, Cross-Data Analysis, Project Overview)
- [X] T016 [US1] Implement CCTV tab rendering logic with data loading, statistics display, and visualizations in app.py
- [X] T017 [US1] Implement Security Lights tab rendering logic with data loading, statistics display, and visualizations in app.py
- [X] T018 [US1] Implement Child Protection Zones tab rendering logic with data loading, statistics display, and visualizations in app.py
- [X] T019 [US1] Implement Parking Lots tab rendering logic with data loading, statistics display, and visualizations in app.py
- [X] T020 [US1] Implement Accident tab rendering logic with data loading, statistics display, and visualizations in app.py
- [X] T021 [US1] Implement Train tab rendering logic with data loading, statistics display, and visualizations in app.py
- [X] T022 [US1] Implement Test tab rendering logic with data loading, statistics display, and visualizations in app.py
- [X] T023 [US1] Add data preview (first N rows) with st.dataframe() in each dataset tab
- [X] T024 [US1] Add descriptive statistics tables using st.expander() for better UI organization in each dataset tab
- [X] T025 [US1] Add sorting capability to displayed data tables with st.dataframe() in each dataset tab
- [X] T026 [US1] Add error handling for missing CSV files with st.warning() messages in app.py
- [X] T027 [US1] Add error handling for missing coordinates with st.info() messages when map visualization skipped in app.py

**Checkpoint**: At this point, User Story 1 should be fully functional - all 7 dataset tabs should display statistics, charts, and maps (where coordinates exist)

**Manual Test Checklist for US1**:
- [ ] Application starts without errors (`streamlit run app.py`)
- [ ] All 7 dataset tabs (CCTV through Test) are visible
- [ ] Each tab displays row count, column count, data types, missing value ratios
- [ ] Numeric columns show histograms with proper binning
- [ ] Categorical columns show bar charts with frequency distributions
- [ ] Datasets with coordinates display interactive Folium maps
- [ ] Map markers are clickable and show detail popups
- [ ] Missing CSV files trigger clear warning messages
- [ ] Datasets without coordinates skip map visualization gracefully
- [ ] Data tables are sortable by clicking column headers
- [ ] Statistics sections are collapsible using expanders

---

## Phase 4: User Story 2 - Analyze Cross-Dataset Relationships (Priority: P2)

**Goal**: Enable learners to explore relationships between train.csv and public facility datasets through spatial proximity analysis, overlay maps, and distribution comparisons

**Independent Test**: Navigate to "Cross-Data Analysis" tab, select train.csv and any public dataset (e.g., CCTV), verify that proximity analysis, overlay maps, distribution comparisons, and textual insights are generated and displayed

### Implementation for User Story 2

- [ ] T028 [P] [US2] Implement compute_proximity_stats() function with thresholds [0.5, 1.0, 2.0]km and 5000 point sampling in utils/geo.py
- [ ] T029 [P] [US2] Implement create_overlay_map() function for multi-dataset layer visualization in utils/visualizer.py
- [ ] T030 [P] [US2] Implement summarize_proximity_stats() function with density classification (high/moderate/low) in utils/narration.py
- [ ] T031 [P] [US2] Implement generate_distribution_insight() function for single column analysis in utils/narration.py
- [ ] T032 [P] [US2] Implement compare_distributions() function for train vs test comparison in utils/narration.py
- [ ] T033 [US2] Create Cross-Data Analysis tab UI with dual dataset selection dropdowns in app.py
- [ ] T034 [US2] Implement proximity analysis calculation and results display (500m, 1km, 2km statistics table) in app.py
- [ ] T035 [US2] Implement overlay map rendering with distinct colors for each dataset and layer toggle controls in app.py
- [ ] T036 [US2] Implement distribution comparison charts (bar/line charts) for numeric features between selected datasets in app.py
- [ ] T037 [US2] Integrate natural language insights generation and display for spatial relationships in app.py
- [ ] T038 [US2] Add support for train.csv comparisons with all public datasets (CCTV, Security Lights, Child Protection Zones, Parking Lots, Accident) in app.py
- [ ] T039 [US2] Add support for facility-to-facility comparisons (CCTV ↔ Security Lights, CCTV ↔ Child Protection Zones, etc.) in app.py
- [ ] T040 [US2] Add error handling for missing coordinates in cross-analysis with informative st.error() messages in app.py
- [ ] T041 [US2] Add performance optimization to ensure proximity analysis completes within 10 seconds in app.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - individual dataset exploration AND cross-dataset analysis should be fully functional

**Manual Test Checklist for US2**:
- [ ] Cross-Data Analysis tab is accessible and loads without errors
- [ ] Dataset selection dropdowns show all 7 datasets
- [ ] Selecting train.csv + CCTV calculates proximity statistics (500m, 1km, 2km)
- [ ] Proximity analysis completes within 10 seconds for datasets up to 5000 points
- [ ] Overlay map displays both datasets with distinct colors (e.g., blue for train, red for CCTV)
- [ ] Layer toggle controls allow showing/hiding each dataset independently
- [ ] Distribution comparison charts display for numeric columns between datasets
- [ ] Natural language insights generate meaningful summaries (e.g., "high spatial correlation")
- [ ] Facility-to-facility comparisons work (e.g., CCTV ↔ Security Lights)
- [ ] Missing coordinates trigger clear error message explaining spatial analysis requires location data
- [ ] Non-spatial analyses (distribution comparisons) proceed even when coordinates missing

---

## Phase 5: User Story 3 - Understand Project Context and Data Concepts (Priority: P3)

**Goal**: Provide learners with project documentation and foundational data analysis concepts within the application to enable independent learning without external resources

**Independent Test**: Navigate to "Project Overview" tab, verify that project introduction, system architecture diagram, dataset descriptions, and educational concept explanations are clearly presented

### Implementation for User Story 3

- [ ] T042 [US3] Create Project Overview tab structure with markdown sections in app.py
- [ ] T043 [US3] Add project purpose and learning objectives section with st.markdown() in app.py
- [ ] T044 [US3] Add dataset list with descriptions (CCTV, Security Lights, Child Protection Zones, Parking Lots, Accident, Train, Test) in app.py
- [ ] T045 [US3] Add technology stack explanation (Python 3.10+, Streamlit, pandas, numpy, plotly, folium) in app.py
- [ ] T046 [US3] Add system architecture diagram showing tab structure and data flow (using st.mermaid() or image) in app.py
- [ ] T047 [US3] Add educational concepts section explaining data types (numerical, categorical, datetime) in app.py
- [ ] T048 [US3] Add educational concepts section explaining basic statistics (mean, std, min, max, median, percentiles) in app.py
- [ ] T049 [US3] Add educational concepts section explaining missing values and outliers in app.py
- [ ] T050 [US3] Add educational concepts section explaining distributions and geospatial coordinates in app.py
- [ ] T051 [US3] Add educational concepts section explaining correlation and spatial patterns (clustering, density) in app.py
- [ ] T052 [US3] Add educational concepts section explaining insight derivation methods in app.py
- [ ] T053 [US3] Add example questions to guide learners (e.g., "Which areas have concentrated facilities?", "What spatial patterns exist?") in app.py
- [ ] T054 [US3] Add explanation of cross-dataset analysis importance and spatial visualization interpretation in app.py

**Checkpoint**: All user stories should now be independently functional - individual exploration (US1), cross-analysis (US2), and educational content (US3) complete

**Manual Test Checklist for US3**:
- [ ] Project Overview tab loads without errors
- [ ] Project purpose section clearly explains application goals
- [ ] Dataset list includes all 7 datasets with brief descriptions
- [ ] Technology stack section lists Python 3.10+, Streamlit, pandas, numpy, plotly, folium, streamlit-folium
- [ ] System architecture diagram renders correctly (Mermaid or image)
- [ ] Educational concepts cover data types, basic statistics, missing values, outliers
- [ ] Educational concepts cover distributions, geospatial basics, correlation
- [ ] Educational concepts cover spatial visualization patterns (clustering, density)
- [ ] Example questions are provided to guide analytical thinking
- [ ] Cross-analysis importance explanation helps learners understand why it matters
- [ ] All markdown formatting renders correctly and is readable

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T055 [P] Add application title and header with st.title() and st.header() in app.py
- [ ] T056 [P] Add sidebar with usage instructions or navigation guidance in app.py
- [ ] T057 [P] Optimize caching to ensure initial load <3 seconds by verifying @st.cache_data usage in utils/loader.py
- [ ] T058 [P] Add performance monitoring to ensure tab switching <1 second in app.py
- [ ] T059 [P] Add performance optimization to ensure map rendering smooth for up to 5000 points in utils/visualizer.py
- [ ] T060 Verify application works on Windows, macOS, and Linux per quickstart.md instructions
- [ ] T061 Test with large datasets (>5000 rows) to verify sampling triggers correctly in utils/geo.py and utils/visualizer.py
- [ ] T062 Test with missing CSV files to verify error messages are user-friendly and actionable
- [ ] T063 Test with datasets missing coordinate columns to verify graceful degradation
- [ ] T064 Test with Korean character encoding variations (UTF-8, UTF-8-SIG, CP949) to verify read_csv_safe() handles all cases
- [ ] T065 [P] Add code comments explaining key algorithms (Haversine, proximity analysis) for educational transparency
- [ ] T066 Validate quickstart.md instructions by following setup steps on clean environment
- [ ] T067 Verify all constitutional principles are satisfied (Data-First, Simplicity, Educational Purpose, Streamlit-Based, Scope Discipline)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User stories can proceed in parallel (if staffed) after Foundational complete
  - Or sequentially in priority order: US1 (P1) → US2 (P2) → US3 (P3)
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent of US1 but may reuse loader/visualizer functions
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Independent of US1/US2 (pure documentation)

### Within Each User Story

**User Story 1**:
- T012-T014 (visualizer functions) can run in parallel
- T015 (tab structure) must complete before T016-T022 (individual tabs)
- T016-T022 (individual tab implementations) can run in parallel after T015
- T023-T025 (enhancements) apply to all tabs, run after T016-T022
- T026-T027 (error handling) run last

**User Story 2**:
- T028-T032 (utility functions) can all run in parallel
- T033 (UI structure) must complete before T034-T041
- T034-T039 (feature implementations) can run in parallel after T033
- T040-T041 (error handling, optimization) run last

**User Story 3**:
- All tasks (T042-T054) are sequential markdown content additions to same tab
- Could be parallelized by having different developers write different sections

### Parallel Opportunities

**Setup Phase (Phase 1)**:
- T003 and T004 can run in parallel (different files)

**Foundational Phase (Phase 2)**:
- T008, T009, T010 can run in parallel (different functions in utils/geo.py)
- T005, T006, T007 must run sequentially (same file, interdependent)

**User Story 1 (Phase 3)**:
- T012, T013, T014 can run in parallel (different functions)
- T016, T017, T018, T019, T020, T021, T022 can run in parallel (different tabs)

**User Story 2 (Phase 4)**:
- T028, T029, T030, T031, T032 can run in parallel (different functions, different files)
- T034, T035, T036, T037, T038, T039 can run in parallel after T033 (different features)

**Polish Phase (Phase 6)**:
- T055, T056, T057, T058, T059, T065 can run in parallel (different concerns)

---

## Parallel Example: User Story 1

```bash
# Parallel batch 1: Visualizer functions
Task T012: "Implement plot_numeric_distribution() in utils/visualizer.py"
Task T013: "Implement plot_categorical_distribution() in utils/visualizer.py"
Task T014: "Implement create_folium_map() in utils/visualizer.py"

# Sequential: Create tab structure
Task T015: "Create main tab structure in app.py"

# Parallel batch 2: Individual tab implementations
Task T016: "Implement CCTV tab in app.py"
Task T017: "Implement Security Lights tab in app.py"
Task T018: "Implement Child Protection Zones tab in app.py"
Task T019: "Implement Parking Lots tab in app.py"
Task T020: "Implement Accident tab in app.py"
Task T021: "Implement Train tab in app.py"
Task T022: "Implement Test tab in app.py"
```

---

## Parallel Example: User Story 2

```bash
# Parallel batch 1: All utility functions (different files)
Task T028: "Implement compute_proximity_stats() in utils/geo.py"
Task T029: "Implement create_overlay_map() in utils/visualizer.py"
Task T030: "Implement summarize_proximity_stats() in utils/narration.py"
Task T031: "Implement generate_distribution_insight() in utils/narration.py"
Task T032: "Implement compare_distributions() in utils/narration.py"

# Sequential: Create UI structure
Task T033: "Create Cross-Data Analysis tab UI in app.py"

# Parallel batch 2: Feature implementations
Task T034: "Implement proximity analysis calculation in app.py"
Task T035: "Implement overlay map rendering in app.py"
Task T036: "Implement distribution comparison charts in app.py"
Task T037: "Integrate insights generation in app.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T004) → ~15 minutes
2. Complete Phase 2: Foundational (T005-T011) → ~2 hours (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (T012-T027) → ~6-8 hours
4. **STOP and VALIDATE**: Test User Story 1 independently with manual checklist
5. You now have a working MVP that allows exploration of all 7 datasets!

**Estimated MVP time**: 8-10 hours of focused development

### Incremental Delivery

1. **Foundation** (Phases 1-2): Setup + Foundational → Foundation ready (~2-3 hours)
2. **MVP** (Phase 3): User Story 1 → Individual dataset exploration working (~6-8 hours)
   - STOP, TEST, DEMO
3. **Enhanced** (Phase 4): Add User Story 2 → Cross-dataset analysis working (~4-6 hours)
   - STOP, TEST, DEMO
4. **Complete** (Phase 5): Add User Story 3 → Educational content complete (~2-3 hours)
   - STOP, TEST, DEMO
5. **Polished** (Phase 6): Polish & validation → Production-ready (~2-3 hours)

**Total estimated time**: 16-23 hours

### Parallel Team Strategy

With 3 developers after Foundational phase completes:

1. **Team completes Phases 1-2 together** (~2-3 hours)
2. **Once Foundational done**:
   - Developer A: User Story 1 (T012-T027) → Individual datasets
   - Developer B: User Story 2 (T028-T041) → Cross-analysis
   - Developer C: User Story 3 (T042-T054) → Educational content
3. Stories complete independently, integrate naturally through shared utils/

**Parallel completion time**: ~6-8 hours after foundation (vs ~12-17 hours sequential)

---

## Notes

- **[P] tasks** = different files/functions, no dependencies, can run in parallel
- **[Story] labels** = maps task to specific user story (US1, US2, US3) for traceability
- **Each user story is independently completable and testable** - can stop after any story phase
- **No automated tests** per constitutional guidance - manual exploratory testing only
- **Commit strategy**: Commit after each task or logical group (e.g., all T012-T014 visualizer functions)
- **Stop at any checkpoint** to validate story independently before proceeding
- **Path assumptions**: All paths assume repository root as working directory
- **File conflicts**: Carefully manage app.py edits when parallelizing - consider using feature branches per user story

---

## Success Metrics

**After MVP (User Story 1 complete)**:
- [ ] Application loads within 3 seconds on local machine
- [ ] All 7 dataset tabs display statistics and visualizations
- [ ] Maps render smoothly for datasets with coordinates
- [ ] Clear error messages for missing files or data issues

**After User Story 2 complete**:
- [ ] Cross-dataset proximity analysis completes within 10 seconds
- [ ] Overlay maps show multiple datasets with distinct colors
- [ ] Natural language insights provide meaningful spatial pattern summaries

**After User Story 3 complete**:
- [ ] Learners can understand all foundational concepts from Project Overview tab
- [ ] No external documentation required to use the application effectively

**After Polish phase**:
- [ ] Application satisfies all constitutional principles
- [ ] Quickstart.md instructions work on clean environment
- [ ] Code is simple enough for Python beginners to understand
- [ ] 90% of learners can identify spatial patterns within 15 minutes of exploration
