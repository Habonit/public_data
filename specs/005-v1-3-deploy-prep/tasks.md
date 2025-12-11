# Tasks: v1.3 Streamlit Community 배포 준비

**Branch**: `005-v1-3-deploy-prep` | **Date**: 2025-12-11 | **Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

## Summary

spec.md의 3개 User Story와 plan.md의 기술적 결정을 기반으로 TDD 방식의 구현 태스크를 정의합니다.

- **US1** (P1): 사고일시 데이터 자동 전처리
- **US2** (P2): 프로젝트 개요 정보 제공
- **US3** (P1): 안정적인 클라우드 배포

---

## Phase 0: Setup

프로젝트 구조 및 테스트 환경 설정

- [x] [T001] [P1] [Setup] tests/ 디렉토리 및 __init__.py 생성 (`tests/__init__.py`)
- [x] [T002] [P1] [Setup] pytest 설정 파일 생성 (`tests/conftest.py`)

---

## Phase 1: US3 - 의존성 동기화 (P1)

배포 환경 안정화를 위한 requirements.txt 업데이트 (선행 작업)

- [x] [T003] [P1] [US3] requirements.txt에 scikit-learn>=1.7.2 추가 (`requirements.txt`)
- [x] [T004] [P1] [US3] requirements.txt에 lightgbm>=4.6.0 추가 (`requirements.txt`)

**검증**: FR-007, SC-003, SC-004

---

## Phase 2: US1 - 사고일시 전처리 (P1)

TDD 방식으로 전처리 함수 구현

### 2.1 테스트 작성 (Red)

- [x] [T005] [P1] [US1] test_preprocessing.py 파일 생성 (`tests/test_preprocessing.py`)
- [x] [T006] [P1] [US1] hour_to_period() 테스트 케이스 작성 - 출근시간대 (TC1: 08시 → "출근시간대")
- [x] [T007] [P1] [US1] hour_to_period() 테스트 케이스 작성 - 퇴근시간대 (TC2: 18시 → "퇴근시간대")
- [x] [T008] [P1] [US1] hour_to_period() 테스트 케이스 작성 - 심야 (TC3: 23시 → "심야")
- [x] [T009] [P1] [US1] hour_to_period() 테스트 케이스 작성 - 심야 새벽 (TC4: 03시 → "심야")
- [x] [T010] [P1] [US1] hour_to_period() 테스트 케이스 작성 - 일반시간대 (TC5: 14시 → "일반시간대")
- [x] [T011] [P1] [US1] preprocess_accident_datetime() 테스트 케이스 작성 - 정상 데이터 (TC6: 5개 컬럼 생성)
- [x] [T012] [P1] [US1] preprocess_accident_datetime() 테스트 케이스 작성 - 컬럼 미존재 (TC7: 원본 반환)
- [x] [T013] [P1] [US1] preprocess_accident_datetime() 테스트 케이스 작성 - 파싱 실패 (TC8: 해당 행 제외)

### 2.2 구현 (Green)

- [x] [T014] [P1] [US1] preprocessing.py 파일 생성 (`utils/preprocessing.py`)
- [x] [T015] [P1] [US1] hour_to_period() 함수 구현 - 시간대 분류 로직
- [x] [T016] [P1] [US1] preprocess_accident_datetime() 함수 구현 - DataFrame.copy()로 복사본 생성 (FR-009)
- [x] [T017] [P1] [US1] preprocess_accident_datetime() 함수 구현 - "사고일시" 컬럼 존재 확인 (FR-003)
- [x] [T018] [P1] [US1] preprocess_accident_datetime() 함수 구현 - pd.to_datetime() 파싱 (errors='coerce')
- [x] [T019] [P1] [US1] preprocess_accident_datetime() 함수 구현 - 사고연/월/일/시 컬럼 추출 (FR-001)
- [x] [T020] [P1] [US1] preprocess_accident_datetime() 함수 구현 - 시간대 컬럼 생성 (FR-002)
- [x] [T021] [P1] [US1] preprocess_accident_datetime() 함수 구현 - NaT 행 제외 및 경고 메시지 (FR-010)

### 2.3 통합 (Refactor)

- [x] [T022] [P1] [US1] loader.py에서 preprocess_accident_datetime() 호출 추가 (`utils/loader.py`)
- [x] [T023] [P1] [US1] 전체 테스트 실행 및 통과 확인 (`pytest tests/ -v`)

**검증**: FR-001, FR-002, FR-003, FR-009, FR-010, SC-001, SC-002, SC-006

---

## Phase 3: US2 - 프로젝트 개요 (P2)

프로젝트 개요 탭 콘텐츠 추가

- [x] [T024] [P2] [US2] app.py 프로젝트 개요 탭에 교육용 앱 설명 추가 (st.info) (FR-004) (`app.py`)
- [x] [T025] [P2] [US2] app.py 프로젝트 개요 탭에 DACON 대회 링크 추가 (st.markdown) (FR-005) (`app.py`)
- [x] [T026] [P2] [US2] app.py 프로젝트 개요 탭에 데이터 다운로드/업로드 안내 추가 (FR-006) (`app.py`)

**검증**: FR-004, FR-005, FR-006, SC-005

---

## Phase 4: 최종 검증

배포 전 통합 테스트

- [x] [T027] [P1] [US3] 로컬 환경에서 streamlit run app.py 실행 및 전체 기능 테스트
- [x] [T028] [P1] [US3] train.csv 업로드 후 파생 피처 5개 생성 확인 (SC-001)
- [ ] [T029] [P1] [US3] AI 챗봇 ECLO 예측 기능 정상 동작 확인 (SC-004)
- [ ] [T030] [P1] [US3] Streamlit Community Cloud 배포 및 검증 (FR-008, SC-003)

---

## Task Summary

| Phase | Task Count | Priority |
|-------|------------|----------|
| Phase 0: Setup | 2 | P1 |
| Phase 1: US3 의존성 | 2 | P1 |
| Phase 2: US1 전처리 | 19 | P1 |
| Phase 3: US2 개요 | 3 | P2 |
| Phase 4: 검증 | 4 | P1 |
| **Total** | **30** | - |

## Dependencies

```
T001, T002 (Setup)
    ↓
T003, T004 (의존성)
    ↓
T005-T013 (테스트 작성)
    ↓
T014-T021 (구현)
    ↓
T022, T023 (통합)
    ↓
T024-T026 (프로젝트 개요) ← 독립적으로 병렬 가능
    ↓
T027-T030 (최종 검증)
```

## Checklist Reference

- [requirements.md](./checklists/requirements.md) - 기능 요구사항 체크리스트
