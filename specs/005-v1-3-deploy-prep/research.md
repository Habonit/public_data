# Research: v1.3 Streamlit Community 배포 준비

**Date**: 2025-12-11
**Feature**: 005-v1-3-deploy-prep

## 1. 사고일시 전처리 설계

### 1.1 Decision: 전처리 함수 위치
- **선택**: `utils/preprocessing.py` 신규 파일 생성
- **근거**: constitution 3.4에서 "전처리 함수는 utils/preprocessing.py에 모듈화" 명시
- **대안 고려**: loader.py에 추가 - 파일 책임 분리 원칙 위반으로 기각

### 1.2 Decision: 전처리 적용 시점
- **선택**: 데이터 업로드 직후 (loader.py에서 호출)
- **근거**: session_state 캐싱 전에 전처리하여 일관된 데이터 구조 보장
- **대안 고려**: 시각화 탭에서 필요 시 호출 - 중복 처리 위험으로 기각

### 1.3 Decision: 시간대 분류 로직
- **선택**: note.md에서 제공된 `hour_to_period()` 함수 그대로 사용
- **근거**: 제안서에 명시된 비즈니스 규칙 준수
- **분류 기준**:
  - 07-09시: 출근시간대
  - 17-19시: 퇴근시간대
  - 22-05시: 심야 (22~24 또는 0~5)
  - 그 외: 일반시간대

### 1.4 Decision: 원본 데이터 보존
- **선택**: DataFrame.copy()로 복사본 생성 후 전처리
- **근거**: constitution FR-009 "원본 데이터를 변경하지 않고 복사본에서 작업"
- **대안 고려**: 원본 수정 - constitution 위반으로 기각

## 2. 에러 처리 전략

### 2.1 Decision: 날짜 파싱 실패 처리
- **선택**: `errors='coerce'`로 파싱 실패 시 NaT 반환, 해당 행 제외
- **근거**: constitution XIII.2 Graceful Degradation - 일부 실패해도 나머지 정상 처리
- **대안 고려**: 전체 실패 - 사용자 경험 저하로 기각

### 2.2 Decision: 컬럼 미존재 처리
- **선택**: "사고일시" 컬럼 없으면 원본 그대로 반환 (전처리 건너뜀)
- **근거**: spec FR-003 "에러 없이 처리해야 한다"
- **대안 고려**: 에러 발생 - 다른 데이터셋(CCTV, 보안등 등) 업로드 시 실패로 기각

## 3. 의존성 동기화

### 3.1 Decision: requirements.txt 업데이트 방식
- **선택**: pyproject.toml과 동일한 패키지 목록으로 수동 동기화
- **근거**: Streamlit Community Cloud는 requirements.txt만 인식
- **추가 패키지**:
  - `scikit-learn>=1.7.2` - ML 유틸리티
  - `lightgbm>=4.6.0` - ECLO 예측 모델

### 3.2 현재 상태 분석
- **pyproject.toml**: 14개 패키지 (scikit-learn, lightgbm 포함)
- **requirements.txt**: 12개 패키지 (scikit-learn, lightgbm 누락)
- **영향**: 배포 환경에서 ECLO 예측 기능 실패

## 4. 프로젝트 개요 UI

### 4.1 Decision: 콘텐츠 배치
- **선택**: 데이터 업로드 섹션 위에 앱 소개 및 데이터 출처 표시
- **근거**: 사용자가 데이터 업로드 전에 맥락 파악 필요
- **콘텐츠**:
  1. 교육용 앱 설명 (st.info)
  2. DACON 대회 링크 (st.markdown)
  3. 데이터 다운로드/업로드 안내

### 4.2 Decision: DACON 링크 형식
- **선택**: 클릭 가능한 마크다운 하이퍼링크
- **URL**: `https://dacon.io/competitions/official/236193/overview/description`
- **근거**: 사용자가 직접 대회 페이지에서 데이터 다운로드

## 5. 테스트 전략 (TDD)

### 5.1 Decision: 테스트 프레임워크
- **선택**: pytest (constitution XII.2 명시)
- **구조**: `tests/test_preprocessing.py`

### 5.2 테스트 케이스 설계
| TC# | 함수 | 시나리오 | 예상 결과 |
|-----|------|---------|----------|
| TC1 | `hour_to_period` | 08시 입력 | "출근시간대" |
| TC2 | `hour_to_period` | 18시 입력 | "퇴근시간대" |
| TC3 | `hour_to_period` | 23시 입력 | "심야" |
| TC4 | `hour_to_period` | 03시 입력 | "심야" |
| TC5 | `hour_to_period` | 14시 입력 | "일반시간대" |
| TC6 | `preprocess_accident_datetime` | 정상 데이터 | 5개 컬럼 생성 |
| TC7 | `preprocess_accident_datetime` | 컬럼 미존재 | 원본 반환 |
| TC8 | `preprocess_accident_datetime` | 파싱 실패 행 | 해당 행 제외 |

## 6. 기존 코드 분석

### 6.1 utils/loader.py
- `read_uploaded_csv()`: 이미 4개 인코딩 지원 (utf-8-sig, utf-8, cp949, euc-kr)
- 수정 필요: 전처리 함수 호출 추가

### 6.2 app.py 프로젝트 개요 탭
- 현재: 데이터 업로드 UI만 존재
- 수정 필요: 앱 소개 및 데이터 출처 추가

## 7. 결론

모든 기술적 결정이 완료되었으며 NEEDS CLARIFICATION 항목 없음.
Phase 1 설계 단계로 진행 가능.
