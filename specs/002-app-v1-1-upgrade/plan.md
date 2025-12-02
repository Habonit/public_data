# Implementation Plan: 대구 공공데이터 시각화 앱 v1.1 업그레이드

**Branch**: `002-app-v1-1-upgrade` | **Date**: 2025-12-01 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-app-v1-1-upgrade/spec.md`

## Summary

대구 공공데이터 시각화 앱을 v1.0에서 v1.1로 업그레이드한다. 핵심 변경 사항:
1. **데이터 로딩 방식 전환**: 파일 직접 읽기 → CSV 업로드 방식
2. **성능 최적화**: session_state와 cache 활용으로 재로딩 방지
3. **시각화 다양화**: 히스토그램, 박스플롯, KDE, 산점도 지원
4. **AI 챗봇 추가**: Anthropic API 기반 데이터 질의응답
5. **버그 수정**: ZeroDivisionError, deprecated API, mutable default 등

## Technical Context

**Language/Version**: Python 3.12 (현재 환경), Python 3.10+ 호환
**Primary Dependencies**: Streamlit 1.28.0+, pandas 2.0.0+, numpy 1.24.0+, plotly 5.17.0+, folium 0.14.0+, streamlit-folium 0.15.0+, anthropic (신규)
**Storage**: N/A (파일 기반, 사용자 업로드 CSV)
**Testing**: 수동 탐색적 테스트 (constitution에 따라 자동화 테스트 선택사항)
**Target Platform**: 로컬 환경 (Linux/Windows/macOS), localhost:8501
**Project Type**: Single project (Streamlit 웹 애플리케이션)
**Performance Goals**: CSV 업로드 후 3초 이내 미리보기 표시, 탭 전환 시 즉시 반응
**Constraints**: 지도 시각화 최대 5,000포인트, 파일 크기 50MB 제한 (Streamlit 기본)
**Scale/Scope**: 10개 탭, 7개 데이터셋, 로컬 단일 사용자

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| 원칙 | 상태 | 검증 내용 |
|------|------|----------|
| I. Data-First Exploration | ✅ PASS | 데이터 탐색과 시각화가 핵심, 복잡한 모델링 없음 |
| II. Simplicity & Accessibility | ✅ PASS | 복잡한 아키텍처 패턴 미사용, 초보자도 이해 가능한 코드 |
| III. Educational Purpose | ✅ PASS | 학습자의 프로젝트 기획 지원, 데이터 이해 촉진 |
| IV. Streamlit-Based Visualization | ✅ PASS | Streamlit + Plotly + Folium 유지 |
| V. Scope Discipline | ✅ PASS | 별도 백엔드/DB 없음, ML 모델 학습 없음 |
| VI. Git Commit Convention | ✅ PASS | type(scope): subject 형식 준수 |
| VII. Python Code Style | ✅ PASS | 타입 힌트, Google docstring, snake_case 사용 |
| VIII. Data Handling Rules | ✅ PASS | UTF-8/CP949 인코딩, 5000포인트 제한 준수 |
| IX. Dependencies | ✅ PASS | 필수 패키지 버전 명시, anthropic 추가 필요 |
| X. Documentation & Comments | ✅ PASS | 한글 우선, 기술 용어 영어 허용 |

**신규 의존성**: `anthropic` 패키지 추가 필요 (챗봇 기능)

## Project Structure

### Documentation (this feature)

```text
specs/002-app-v1-1-upgrade/
├── plan.md              # 이 파일
├── research.md          # Phase 0: 기술 리서치 결과
├── data-model.md        # Phase 1: 데이터 모델 정의
├── quickstart.md        # Phase 1: 빠른 시작 가이드
├── contracts/           # Phase 1: API 계약 (챗봇 프롬프트 등)
├── checklists/          # 체크리스트
│   └── requirements.md  # spec 품질 체크리스트
└── tasks.md             # Phase 2: 태스크 목록 (/speckit.tasks)
```

### Source Code (repository root)

```text
app.py                   # 메인 Streamlit 애플리케이션 (수정)
requirements.txt         # 의존성 목록 (수정: anthropic 추가)
utils/
├── __init__.py
├── loader.py            # 데이터 로딩 (수정: 업로드 지원)
├── visualizer.py        # 시각화 (수정: 다양한 차트 추가)
├── geo.py               # 지리 유틸 (수정: mutable default 수정)
├── narration.py         # 설명 텍스트
└── chatbot.py           # 신규: AI 챗봇 모듈
```

**Structure Decision**: 기존 Single project 구조 유지. utils/ 모듈 구조 활용, chatbot.py만 신규 추가.

## Complexity Tracking

> **Constitution Check 위반 없음 - 이 섹션은 비워둠**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| - | - | - |
