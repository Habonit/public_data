# 대구 공공데이터 시각화 앱 개선 제안서 (v1.3.1 → v2.0)

**문서 버전**: v2.0
**작성일**: 2025-12-11
**참고 문서**: `docs/v2.0/note.md`

---

## 1. 개요

본 문서는 대구 공공데이터 시각화 앱 v1.3.1의 현재 상태(AS-IS)와 v2.0에서 목표하는 개선 상태(TO-BE)를 비교 분석한다.

v2.0의 핵심 목표는 **TDD(Test-Driven Development) 방법론의 사후적 적용**이다. 현재 프로젝트는 테스트 코드가 없어 코드 변경 시 side effect를 예측할 수 없는 상황이다. 이를 해결하기 위해 TDD 문서 체계를 먼저 구축하여, 추후 개발 시 기존 코드에 영향을 주는 일이 없도록 한다.

---

## 2. 기능별 AS-IS / TO-BE 비교

### 2.1 TDD 방법론 문서

| 구분 | AS-IS (v1.3.1) | TO-BE (v2.0) |
|:-----|:---------------|:-------------|
| TDD 방법론 가이드 | 없음 | `tests/principle.md` 추가 |
| 테스트 작성 원칙 | 없음 | Red-Green-Refactor 사이클 문서화 |
| 테스트 유형 선택 가이드 | 없음 | 단위/통합/E2E 선택 플로우차트 제공 |
| 테스트 더블 설명 | 없음 | Mock, Stub, Fake, Spy 개념 정리 |

#### 2.1.1 `tests/principle.md` 주요 내용

- Part 1: TDD 기초 (Red-Green-Refactor, AAA 패턴)
- Part 2: 테스트 케이스 설계 (경계값 분석, 동치 분할)
- Part 3: pytest 활용 (fixture, marker, parametrize)
- Part 4: E2E 테스트 방법론

---

### 2.2 프로젝트별 실천 가이드

| 구분 | AS-IS (v1.3.1) | TO-BE (v2.0) |
|:-----|:---------------|:-------------|
| 테스트 실행 가이드 | 없음 | `tests/README.md` 추가 |
| 모듈별 테스트 범위 | 정의 안됨 | 60+ 함수에 대한 테스트 케이스 명세 |
| 통합 테스트 정의 | 없음 | 6개 통합 테스트 흐름 정의 (INT-001 ~ INT-006) |
| 테스트 README 템플릿 | 없음 | `tests/TEST_README_TEMPLATE.md` 추가 |

#### 2.2.1 테스트 범위 정의

| 모듈 | 함수 수 | 우선순위 |
|:-----|:--------|:---------|
| `utils/preprocessing.py` | 2 | P0 |
| `utils/loader.py` | 5 | P0 |
| `utils/tools.py` | 22 | P0 |
| `utils/predictor.py` | 9 | P0 |
| `utils/geo.py` | 4 | P0 |
| `utils/narration.py` | 3 | P1 |
| `utils/graph.py` | 3 | P1 |
| `utils/chatbot.py` | 10 | P1 |
| `utils/visualizer.py` | 9 | P1 |
| `utils/prompts.py` | - | 테스트 불필요 |

---

### 2.3 CI/CD 워크플로우 템플릿

| 구분 | AS-IS (v1.3.1) | TO-BE (v2.0) |
|:-----|:---------------|:-------------|
| GitHub Actions 워크플로우 | 없음 | `tests/workflow_template.yaml` 추가 |
| 자동 테스트 실행 | 수동 실행만 | PR 시 자동 테스트 실행 가이드 |
| Runner 선택 가이드 | 없음 | GitHub-hosted vs Self-hosted 비교 문서 |
| 테스트 피라미드 | 개념 없음 | 단위 70% / 통합 25% / E2E 5% 가이드 |

---

## 3. 변경 요약표

| 영역 | 변경 유형 | 내용 |
|:-----|:---------|:-----|
| `tests/principle.md` | ➕ 추가 | 범용 TDD 방법론 문서 (v2.3) |
| `tests/README.md` | ➕ 추가 | 프로젝트별 테스트 실행 가이드 |
| `tests/TEST_README_TEMPLATE.md` | ➕ 추가 | 다른 프로젝트에서 재사용 가능한 템플릿 |
| `tests/workflow_template.yaml` | ➕ 추가 | GitHub Actions CI/CD 템플릿 |
| `tests/error_explanation.md` | 🔄 변경 | 에러 케이스 설명 보완 (기존 문서) |

---

## 4. 구현 우선순위

### 🔴 P0 - 핵심 문서 (필수)

| 순위 | 항목 | 설명 |
|:-----|:-----|:-----|
| 1 | `tests/principle.md` | 모든 TDD에서 지켜야 할 방법론 제시 |
| 2 | `tests/README.md` | 본 프로젝트의 테스트 실행 가이드 |

### 🟡 P1 - 템플릿 문서

| 순위 | 항목 | 설명 |
|:-----|:-----|:-----|
| 3 | `tests/TEST_README_TEMPLATE.md` | 다른 프로젝트 적용을 위한 README 템플릿 |
| 4 | `tests/workflow_template.yaml` | GitHub Actions CI/CD 템플릿 |

### 🟢 P2 - 향후 과제 (v2.1+)

| 순위 | 항목 | 설명 |
|:-----|:-----|:-----|
| 5 | 실제 테스트 코드 작성 | `tests/test_*.py` 파일 구현 |
| 6 | CI/CD 실제 적용 | `.github/workflows/test.yml` 생성 |
| 7 | 커버리지 목표 설정 | 최소 80% 커버리지 달성 |

---

## 5. 예상 구조

```
tests/
├── principle.md                 # [P0] 범용 TDD 방법론 (모든 프로젝트 공통)
├── README.md                    # [P0] 본 프로젝트 테스트 실행 가이드
├── TEST_README_TEMPLATE.md      # [P1] 테스트 README 작성 템플릿
├── workflow_template.yaml       # [P1] GitHub Actions CI/CD 템플릿
├── error_explanation.md         # 에러 케이스 설명
├── conftest.py                  # (v2.1+) 공통 fixture 정의
│
├── test_preprocessing.py        # (v2.1+) preprocessing.py 테스트
├── test_loader.py               # (v2.1+) loader.py 테스트
├── test_tools.py                # (v2.1+) tools.py 테스트
├── test_predictor.py            # (v2.1+) predictor.py 테스트
├── test_geo.py                  # (v2.1+) geo.py 테스트
│
└── integration/                 # (v2.1+) 통합 테스트
    ├── conftest.py
    ├── test_data_pipeline.py    # INT-001, INT-002
    ├── test_tool_calling.py     # INT-003
    └── test_eclo_pipeline.py    # INT-005
```

---

## 6. 다음 단계

1. **P0 구현**: `principle.md`, `README.md` 완성 및 검토
2. **P1 구현**: `TEST_README_TEMPLATE.md`, `workflow_template.yaml` 완성
3. **v2.0 릴리스**: TDD 문서 체계 프로젝트 포함
4. **v2.1 계획**: 실제 테스트 코드 작성 시작 (P0 모듈부터)
5. **v2.2 계획**: CI/CD 실제 적용 및 커버리지 측정

---

## 7. 버전 릴리스 기준

v2.0 릴리스 조건:
- [x] `tests/principle.md` 완성 (v2.3)
- [x] `tests/README.md` 완성
- [x] `tests/TEST_README_TEMPLATE.md` 완성
- [x] `tests/workflow_template.yaml` 완성
- [ ] 문서 리뷰 및 최종 확인

---

## 참고: TDD 사후 적용 전략

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      TDD 사후 적용 로드맵                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   v2.0: 문서 체계 구축                                                   │
│   ├─ principle.md (방법론)                                              │
│   ├─ README.md (실천 가이드)                                            │
│   ├─ TEST_README_TEMPLATE.md (템플릿)                                   │
│   └─ workflow_template.yaml (CI/CD)                                     │
│                                                                         │
│   v2.1: 핵심 모듈 테스트 작성                                            │
│   ├─ test_preprocessing.py                                              │
│   ├─ test_loader.py                                                     │
│   ├─ test_tools.py                                                      │
│   └─ test_predictor.py                                                  │
│                                                                         │
│   v2.2: 통합 테스트 + CI/CD 적용                                         │
│   ├─ integration/ 디렉토리                                              │
│   ├─ .github/workflows/test.yml                                         │
│   └─ 커버리지 80% 목표                                                  │
│                                                                         │
│   v2.3+: E2E 테스트 + 자동화 확대                                        │
│   └─ 수동 E2E → 자동화 E2E 전환 검토                                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

이 전략의 핵심은 **문서 먼저, 코드 나중**이다. 테스트 작성 방법을 명확히 정의한 후에 실제 테스트 코드를 작성함으로써, 일관된 품질의 테스트 코드를 작성할 수 있다.
