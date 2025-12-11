# 대구 공공데이터 시각화 앱 개선 제안서 (v1.3.1 → v1.3.2)

**문서 버전**: v1.3.2
**작성일**: 2025-12-11
**참고 문서**: `docs/v1.3.2/note.md`

---

## 1. 개요

본 문서는 대구 공공데이터 시각화 앱 v1.3.1의 현재 상태(AS-IS)와 v1.3.2에서 목표하는 개선 상태(TO-BE)를 비교 분석한다.

v1.3.2는 프로젝트 파일 구조 정리를 목표로 하며, 문서 파일 위치 변경 및 관련 참조 업데이트를 수행한다.

---

## 2. 기능별 AS-IS / TO-BE 비교

### 2.1 syllabus.md 파일 위치

| 구분 | AS-IS (v1.3.1) | TO-BE (v1.3.2) |
|:-----|:---------------|:---------------|
| 파일 경로 | `syllabus.md` (프로젝트 루트) | `material/syllabus.md` |
| 관련 참조 | 루트 경로 참조 | material/ 경로 참조로 업데이트 |
| 구조적 의미 | 루트에 혼재 | 교육 자료는 material/ 디렉토리로 분류 |

#### 2.1.1 변경이 필요한 참조 위치

| 파일 | 참조 유형 | 변경 내용 |
|:-----|:---------|:---------|
| `README.md` | 문서 링크/설명 | `syllabus.md` → `material/syllabus.md` |
| `app.py` | 주석/docstring | 경로 참조 업데이트 (있는 경우) |
| 기타 문서 | 경로 참조 | 전체 검색 후 업데이트 |

---

### 2.2 error_explanation.md 파일 위치

| 구분 | AS-IS (v1.3.1) | TO-BE (v1.3.2) |
|:-----|:---------------|:---------------|
| 파일 경로 | `docs/error_explanation.md` | `tests/error_explanation.md` |
| 관련 참조 | docs/ 경로 참조 | tests/ 경로 참조로 업데이트 |
| 구조적 의미 | 일반 문서로 분류 | 테스트 관련 문서로 재분류 |

#### 2.2.1 변경이 필요한 참조 위치

| 파일 | 참조 유형 | 변경 내용 |
|:-----|:---------|:---------|
| `README.md` | 문서 링크/설명 | `docs/error_explanation.md` → `tests/error_explanation.md` |
| `tests/conftest.py` | 주석 참조 | 경로 업데이트 (있는 경우) |
| 기타 테스트 파일 | 경로 참조 | 전체 검색 후 업데이트 |

---

### 2.3 README.md 업데이트

| 구분 | AS-IS (v1.3.1) | TO-BE (v1.3.2) |
|:-----|:---------------|:---------------|
| 버전 표기 | v1.3.1 | v1.3.2 |
| 파일 구조 섹션 | 기존 구조 반영 | 변경된 파일 위치 반영 |
| 문서 참조 링크 | 기존 경로 | 새 경로로 업데이트 |

---

## 3. 변경 요약표

| 영역 | 변경 유형 | 내용 |
|:-----|:---------|:-----|
| `syllabus.md` | 🔄 변경 | 루트 → `material/syllabus.md`로 이동 |
| `error_explanation.md` | 🔄 변경 | `docs/` → `tests/`로 이동 |
| `README.md` | 🔧 개선 | 파일 구조 및 참조 경로 업데이트 |
| 코드 주석 | 🔧 개선 | 관련 경로 참조 전체 업데이트 |
| docstring | 🔧 개선 | 관련 경로 참조 전체 업데이트 |

---

## 4. 구현 우선순위

### 🔴 P0 - 파일 이동 (필수)

| 순위 | 항목 | 설명 |
|:-----|:-----|:-----|
| 1 | syllabus.md 이동 | `syllabus.md` → `material/syllabus.md` |
| 2 | error_explanation.md 이동 | `docs/error_explanation.md` → `tests/error_explanation.md` |

### 🟡 P1 - 참조 업데이트 (중요)

| 순위 | 항목 | 설명 |
|:-----|:-----|:-----|
| 3 | syllabus.md 참조 검색 | 프로젝트 전체에서 `syllabus.md` 참조 검색 |
| 4 | syllabus.md 참조 업데이트 | 발견된 모든 참조를 새 경로로 변경 |
| 5 | error_explanation.md 참조 검색 | 프로젝트 전체에서 `error_explanation.md` 참조 검색 |
| 6 | error_explanation.md 참조 업데이트 | 발견된 모든 참조를 새 경로로 변경 |

### 🟢 P2 - 문서화 (개선)

| 순위 | 항목 | 설명 |
|:-----|:-----|:-----|
| 7 | README.md 업데이트 | 버전, 파일 구조, 참조 링크 반영 |
| 8 | 변경 사항 검증 | 모든 참조가 정상 동작하는지 확인 |

---

## 5. 예상 구조

```
public_data/
├── material/
│   ├── 01-03/
│   ├── 03-07/
│   ├── ...
│   └── syllabus.md          ← 이동됨 (루트에서)
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_preprocessing.py
│   └── error_explanation.md  ← 이동됨 (docs/에서)
├── docs/
│   ├── constitution.md
│   ├── proposal_template.md
│   ├── v1.3.2/
│   │   ├── note.md
│   │   └── app_improvement_proposal.md
│   └── ...
├── utils/
├── app.py
├── README.md
└── ...
```

---

## 6. 다음 단계

1. **P0 구현**: syllabus.md, error_explanation.md 파일 이동
2. **P1 구현**: 프로젝트 전체 참조 검색 및 업데이트
3. **P2 구현**: README.md 반영
4. **테스트**: 앱 실행 및 문서 링크 정상 동작 확인
5. **문서화**: 버전 히스토리 업데이트

---
