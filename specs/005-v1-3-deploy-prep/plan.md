# Implementation Plan: v1.3 Streamlit Community 배포 준비

**Branch**: `005-v1-3-deploy-prep` | **Date**: 2025-12-11 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/005-v1-3-deploy-prep/spec.md`

## Summary

v1.3은 Streamlit Community Cloud 배포를 위한 준비 단계로, 다음 3가지 핵심 목표를 달성한다:

1. **사고일시 전처리**: train/test 데이터의 "사고일시" 컬럼을 파싱하여 ML 모델 입력 피처(사고연, 사고월, 사고일, 사고시, 시간대) 자동 생성
2. **프로젝트 개요 보강**: 교육용 앱 설명, DACON 대회 링크, 데이터 업로드 안내 추가
3. **의존성 동기화**: requirements.txt에 누락된 scikit-learn, lightgbm 추가하여 배포 환경 안정화

## Technical Context

**Language/Version**: Python 3.10+ (현재 환경 Python 3.12 호환)
**Primary Dependencies**: Streamlit 1.28.0+, pandas 2.0.0+, scikit-learn 1.7.2+, lightgbm 4.6.0+
**Storage**: 파일 기반 (CSV 업로드, st.session_state 캐싱), model/ 디렉토리 (pkl 파일)
**Testing**: pytest (TDD 방법론 적용, constitution XII 참조)
**Target Platform**: Streamlit Community Cloud (웹 브라우저)
**Project Type**: Single project (Streamlit 앱)
**Performance Goals**: 전처리 3초 이내 완료 (SC-001)
**Constraints**: 원본 데이터 변경 금지, Graceful Degradation 필수
**Scale/Scope**: 교육용 단일 사용자 앱, train/test 데이터셋 처리

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| 원칙 | 상태 | 검증 |
|------|------|------|
| I. Data-First Exploration | ✅ Pass | 사고일시 전처리로 데이터 탐색 용이성 향상 |
| II. Simplicity & Accessibility | ✅ Pass | 단일 함수로 전처리, 복잡한 패턴 없음 |
| III. Educational Purpose | ✅ Pass | 학습자의 데이터 준비 및 ML 실습 지원 |
| IV. Streamlit-Based Visualization | ✅ Pass | Streamlit Community Cloud 배포 대상 |
| V. Scope Discipline | ✅ Pass | 전처리/UI/배포만 포함, ML 학습 제외 |
| XII. TDD | ✅ Required | 전처리 함수에 대한 테스트 코드 작성 필수 |
| XIII. Error Handling | ✅ Required | Graceful Degradation 적용 필수 |

**Gate Result**: ✅ PASS - 모든 원칙 준수, Phase 0 진행 가능

## Project Structure

### Documentation (this feature)

```text
specs/005-v1-3-deploy-prep/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (N/A - no API)
└── tasks.md             # Phase 2 output (/speckit.tasks)
```

### Source Code (repository root)

```text
# 기존 구조
app.py                   # Streamlit 메인 앱 (수정 대상)
utils/
├── __init__.py
├── loader.py            # 데이터 로딩 (수정 대상)
├── preprocessing.py     # 신규 생성 - 사고일시 전처리
├── chatbot.py
├── geo.py
├── graph.py
├── narration.py
├── predictor.py
├── prompts.py
├── tools.py
└── visualizer.py

# 신규 생성
tests/
├── __init__.py
├── test_preprocessing.py  # 전처리 단위 테스트 (TDD)
└── conftest.py            # pytest 설정

# 수정 대상
requirements.txt         # scikit-learn, lightgbm 추가
```

**Structure Decision**: 기존 Single project 구조 유지. utils/preprocessing.py 신규 생성, tests/ 디렉토리 신규 생성 (TDD 준수).

## Complexity Tracking

> **Constitution 위반 없음 - 이 섹션은 비어 있음**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |
