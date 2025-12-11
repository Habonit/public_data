# 테스트 실행 가이드

이 문서는 **대구 공공데이터 시각화 앱**의 테스트를 실행하고 활용하는 방법을 설명한다.

> **방법론 참고**: 테스트 작성 원칙과 규칙은 [principle.md](./principle.md) 참조

---

## 목차

1. [왜 TDD가 필요한가?](#1-왜-tdd가-필요한가)
2. [테스트 범위](#2-테스트-범위)
3. [테스트 실행 방법](#3-테스트-실행-방법)
4. [개발 워크플로우](#4-개발-워크플로우)
5. [CI/CD 연동](#5-cicd-연동)
6. [디렉토리 구조](#6-디렉토리-구조)
7. [Fixture 목록](#7-fixture-목록)
8. [FAQ](#8-faq)

---

## 1. 왜 TDD가 필요한가?

이 프로젝트에서 TDD가 중요한 이유:

### 1.1 데이터 파이프라인 신뢰성

```
CSV 업로드 → 전처리 → 분석 → 시각화
```

데이터 전처리 함수(`preprocess_accident_data`)가 잘못되면:
- 사고일시 파싱 오류 → 시간대 분석 실패
- 좌표 변환 오류 → 지도 시각화 실패
- 숫자 컬럼 인식 오류 → 통계 계산 실패

**→ 테스트로 전처리 함수의 정확성을 보장**

### 1.2 Tool Calling 안정성

22개의 도구가 AI와 연동되어 실행된다:
- 도구 하나가 잘못된 형식을 반환하면 전체 대화가 깨짐
- 도구 간 데이터 전달이 실패하면 연쇄 오류 발생

**→ 각 도구와 연결 흐름을 테스트로 검증**

### 1.3 안전한 리팩토링

코드 수정 시:
- "이거 고치면 다른 데 영향 없겠지?" 걱정 없이 수정
- 테스트가 통과하면 기존 기능이 정상 동작함을 확인

---

## 2. 테스트 범위

### 2.1 단위 테스트 (Unit Test)

개별 함수의 정확성을 검증한다. 각 모듈별 테스트 대상 함수와 우선순위는 다음과 같다.

---

#### 2.1.1 `utils/preprocessing.py` (P0)

| 함수 | 설명 | 테스트 케이스 |
|:-----|:-----|:-------------|
| `hour_to_period(hour)` | 시간을 시간대로 변환 | 출근(7-9), 점심(11-13), 퇴근(17-19), 심야(0-5) 등 |
| `preprocess_accident_datetime(df)` | 사고일시 컬럼 전처리 | 정상 파싱, 결측값 처리, 잘못된 형식 처리 |

---

#### 2.1.2 `utils/loader.py` (P0)

| 함수 | 설명 | 테스트 케이스 |
|:-----|:-----|:-------------|
| `read_csv_safe(file_path)` | 다양한 인코딩 CSV 읽기 | UTF-8, CP949, EUC-KR 인코딩 |
| `read_uploaded_csv(uploaded_file)` | 업로드된 파일 읽기 | 정상 파일, 빈 파일, 잘못된 형식 |
| `load_dataset_from_session(name)` | 세션에서 데이터셋 로드 | 존재하는 데이터셋, 없는 데이터셋 |
| `load_dataset(dataset_name)` | 이름으로 데이터셋 로드 | 유효한 이름, 잘못된 이름 |
| `get_dataset_info(df)` | DataFrame 메타정보 반환 | 정상 DataFrame, 빈 DataFrame |

---

#### 2.1.3 `utils/tools.py` (P0) - 22개 도구 함수

모든 도구는 개별적으로 단위 테스트해야 한다. 하나라도 잘못된 형식을 반환하면 전체 Tool Calling이 실패한다.

| # | 도구 함수 | 설명 | 테스트 케이스 |
|:--|:---------|:-----|:-------------|
| 1 | `get_dataframe_info` | DataFrame 기본 정보 | 정상 df, 빈 df |
| 2 | `get_column_statistics` | 컬럼 통계 | 숫자형, 문자형, 없는 컬럼 |
| 3 | `get_missing_values` | 결측값 정보 | 결측 있음/없음 |
| 4 | `get_value_counts` | 값 빈도수 | 범주형, top_n 파라미터 |
| 5 | `filter_dataframe` | 조건 필터링 | 유효 조건, 잘못된 조건 |
| 6 | `sort_dataframe` | 정렬 | 오름차순, 내림차순 |
| 7 | `get_correlation` | 상관관계 | 숫자형 컬럼, 없는 컬럼 |
| 8 | `group_by_aggregate` | 그룹별 집계 | sum, mean, count |
| 9 | `get_unique_values` | 고유값 조회 | 범주형, 없는 컬럼 |
| 10 | `get_date_range` | 날짜 범위 | 날짜형, 비날짜형 |
| 11 | `get_outliers` | 이상치 탐지 | 이상치 있음/없음 |
| 12 | `get_sample_rows` | 샘플 행 조회 | n개 샘플, 빈 df |
| 13 | `calculate_percentile` | 백분위수 계산 | 0-100 범위, 숫자형 |
| 14 | `get_geo_bounds` | 지리적 경계 | 좌표 있음/없음 |
| 15 | `cross_tabulation` | 교차표 | 두 범주형 컬럼 |
| 16 | `analyze_missing_pattern` | 결측 패턴 분석 | 결측 있음/없음 |
| 17 | `get_column_correlation_with_target` | 타겟 상관관계 | 유효 타겟, 없는 타겟 |
| 18 | `detect_data_types` | 데이터 타입 감지 | 다양한 타입 df |
| 19 | `get_temporal_pattern` | 시계열 패턴 | 시간대 컬럼 있음/없음 |
| 20 | `summarize_categorical_distribution` | 범주형 분포 요약 | 범주형, 숫자형 |
| 21 | `predict_eclo` | 단일 ECLO 예측 | 유효 입력, 잘못된 입력 |
| 22 | `predict_eclo_batch` | 배치 ECLO 예측 | 복수 건, 빈 리스트 |

---

#### 2.1.4 `utils/predictor.py` (P0)

| 함수 | 설명 | 테스트 케이스 |
|:-----|:-----|:-------------|
| `load_model()` | LightGBM 모델 로드 | 모델 파일 존재/미존재 |
| `load_encoders()` | 라벨 인코더 로드 | 인코더 파일 존재/미존재 |
| `load_feature_config()` | 피처 설정 로드 | 설정 파일 존재/미존재 |
| `get_valid_values(feature_name)` | 유효값 목록 반환 | 유효 피처명, 잘못된 피처명 |
| `encode_features(features)` | 피처 인코딩 | 모든 필드 유효, 일부 누락 |
| `predict_eclo_value(features)` | ECLO 값 예측 | 정상 입력, 결측 입력 |
| `interpret_eclo(eclo_value)` | ECLO 해석 (간단) | 0-1, 1-3, 3-5, 5+ 범위 |
| `interpret_eclo_detail(eclo_value)` | ECLO 해석 (상세) | 각 범위별 상세 설명 |
| `predict_eclo_batch(accidents)` | 배치 ECLO 예측 | 여러 건, 빈 리스트 |

---

#### 2.1.5 `utils/geo.py` (P1)

| 함수 | 설명 | 테스트 케이스 |
|:-----|:-----|:-------------|
| `detect_lat_lng_columns(df)` | 위도/경도 컬럼 자동 감지 | lat/lng, 위도/경도, y/x 등 |
| `haversine_distance(lat1, lon1, lat2, lon2)` | 두 좌표 간 거리 계산 | 같은 위치, 다른 위치 |
| `validate_coordinates(lat, lng, bounds)` | 좌표 유효성 검증 | 유효 좌표, 범위 밖 좌표 |
| `compute_proximity_stats(df, ...)` | 근접성 통계 계산 | 좌표 있음/없음, 빈 df |

---

#### 2.1.6 `utils/narration.py` (P1)

| 함수 | 설명 | 테스트 케이스 |
|:-----|:-----|:-------------|
| `summarize_proximity_stats(stats_df, ...)` | 근접성 통계 요약 내레이션 | 정상 통계, 빈 통계 |
| `generate_distribution_insight(df, column)` | 분포 인사이트 생성 | 숫자형, 범주형 |
| `compare_distributions(df1, df2, column)` | 두 분포 비교 | 같은 컬럼, 다른 컬럼 |

---

#### 2.1.7 `utils/graph.py` (P1)

| 함수 | 설명 | 테스트 케이스 |
|:-----|:-----|:-------------|
| `route_tools(state)` | 조건부 라우팅 결정 | tool_calls 있음/없음 |
| `build_graph(model, tools, system_prompt)` | StateGraph 생성 | 도구 있음/없음 |
| `astream_graph_events(graph, state, config)` | 이벤트 스트리밍 | (통합 테스트로 검증 권장) |

---

#### 2.1.8 `utils/chatbot.py` (P2)

| 함수 | 설명 | 테스트 케이스 |
|:-----|:-----|:-------------|
| `create_data_context(df, dataset_name)` | 데이터 컨텍스트 생성 | 정상 df, 빈 df |
| `handle_chat_error(error)` | 에러 메시지 생성 | 각종 예외 타입 |
| `validate_api_key(api_key)` | API Key 유효성 검증 | 유효 키, 잘못된 형식, 빈 문자열 |
| `create_langgraph_model(api_key, model)` | ChatAnthropic 생성 | (API 마커 필요) |
| `run_langgraph_chat(...)` | 동기 채팅 실행 | (통합 테스트로 검증) |
| `stream_langgraph_chat(...)` | 스트리밍 채팅 실행 | (통합 테스트로 검증) |
| `create_chat_response(...)` | 채팅 응답 생성 | (통합 테스트로 검증) |
| `run_tool_calling(...)` | Tool Calling 실행 | (통합 테스트로 검증) |
| `create_chat_response_with_tools(...)` | 도구 응답 생성 | (통합 테스트로 검증) |
| `stream_chat_response_with_tools(...)` | 도구 스트리밍 응답 | (통합 테스트로 검증) |

---

#### 2.1.9 `utils/visualizer.py` (P2)

| 함수 | 설명 | 테스트 케이스 |
|:-----|:-----|:-------------|
| `check_missing_ratio(df, column, threshold)` | 결측 비율 확인 | 임계값 이상/이하 |
| `plot_numeric_distribution(df, column)` | 숫자형 분포 차트 | 정상 숫자형, 결측 많음 |
| `plot_categorical_distribution(df, column)` | 범주형 분포 차트 | 범주형, top_n |
| `plot_boxplot(df, column)` | 박스플롯 생성 | 숫자형, 이상치 있음 |
| `plot_kde(df, column)` | KDE 플롯 생성 | 숫자형, 샘플 적음 |
| `plot_scatter(df, x, y)` | 산점도 생성 | 두 숫자형 컬럼 |
| `plot_with_options(df, column, plot_type)` | 옵션별 차트 생성 | 각 plot_type |
| `create_folium_map(df, lat_col, lng_col)` | Folium 지도 생성 | 좌표 있음, 샘플링 |
| `create_overlay_map(datasets, max_points)` | 오버레이 지도 생성 | 다중 데이터셋 |

---

#### 2.1.10 `utils/prompts.py` (테스트 불필요)

상수 정의만 있는 모듈로, 별도 테스트가 필요하지 않다.
- `SYSTEM_PROMPT_BASE`: 기본 시스템 프롬프트
- `ECLO_PREDICTION_PROMPT`: ECLO 예측 안내 프롬프트

### 2.2 통합 테스트 (Integration Test)

여러 모듈이 함께 동작하는 흐름을 검증한다. 단위 테스트로는 검증할 수 없는 **모듈 간 연결**을 테스트한다.

---

#### 2.2.1 통합 테스트 목록

| ID | 흐름 | 관련 모듈 | 검증 내용 |
|:---|:-----|:---------|:---------|
| INT-001 | CSV 업로드 → 전처리 | loader → preprocessing | 업로드된 CSV가 전처리되어 시간대 컬럼이 생성되는지 |
| INT-002 | 전처리 → 도구 실행 | preprocessing → tools | 전처리된 데이터로 분석 도구가 정상 동작하는지 |
| INT-003 | Tool Calling 워크플로우 | chatbot → graph → tools | LangGraph가 도구를 호출하고 결과를 반환하는지 |
| INT-004 | 지도 시각화 파이프라인 | geo → visualizer | 좌표 감지 → folium 지도 생성까지 |
| INT-005 | ECLO 예측 파이프라인 | predictor → tools | predictor 모듈 로드 → 입력 검증 → 예측 반환 |
| INT-006 | 내레이션 생성 파이프라인 | geo → narration | 근접성 통계 → 자연어 요약 생성 |

---

#### 2.2.2 통합 테스트 상세

##### INT-001: CSV 업로드 → 전처리

```
loader.read_uploaded_csv() → preprocessing.preprocess_accident_datetime()
```

| 테스트 케이스 | 검증 내용 |
|:-------------|:---------|
| 정상 CSV 업로드 | 사고일시 컬럼이 파싱되어 시간대 컬럼 생성 |
| 인코딩이 다른 CSV | CP949 → UTF-8 변환 후 전처리 성공 |
| 사고일시 컬럼 누락 | 전처리 스킵, 원본 반환 |

##### INT-002: 전처리 → 도구 실행

```
preprocessing.preprocess_accident_datetime() → tools.get_temporal_pattern()
```

| 테스트 케이스 | 검증 내용 |
|:-------------|:---------|
| 전처리된 데이터 | 시간대 컬럼으로 패턴 분석 가능 |
| 전처리 안 된 데이터 | 시간대 컬럼 없음 오류 처리 |

##### INT-003: Tool Calling 워크플로우 (@pytest.mark.api)

```
사용자 질문 → chatbot → graph.build_graph() → tools 실행 → 응답
```

| 테스트 케이스 | 검증 내용 |
|:-------------|:---------|
| "데이터 정보 알려줘" | get_dataframe_info 도구 호출 |
| "나이 통계 보여줘" | get_column_statistics 도구 호출 |
| "ECLO 예측해줘" | predict_eclo 도구 호출 |
| 도구 필요 없는 질문 | 도구 호출 없이 직접 응답 |

##### INT-004: 지도 시각화 파이프라인

```
geo.detect_lat_lng_columns() → visualizer.create_folium_map()
```

| 테스트 케이스 | 검증 내용 |
|:-------------|:---------|
| 좌표 컬럼 자동 감지 | lat/lng 감지 → 지도 생성 |
| 좌표 컬럼 없음 | 지도 생성 불가 메시지 |
| 5000개 초과 데이터 | 샘플링 후 지도 생성 |

##### INT-005: ECLO 예측 파이프라인

```
predictor.load_model() → predictor.encode_features() → predictor.predict_eclo_value()
```

| 테스트 케이스 | 검증 내용 |
|:-------------|:---------|
| 유효한 사고 데이터 | ECLO 값 + 해석 반환 |
| 일부 피처 누락 | 오류 메시지 반환 |
| 배치 예측 | 여러 건 동시 예측 |

##### INT-006: 내레이션 생성 파이프라인

```
geo.compute_proximity_stats() → narration.summarize_proximity_stats()
```

| 테스트 케이스 | 검증 내용 |
|:-------------|:---------|
| 정상 근접성 통계 | 자연어 요약 생성 |
| 빈 통계 결과 | 적절한 빈 메시지 |

#### Q: Tool Calling 테스트는 단위 테스트인가 통합 테스트인가?

**통합 테스트(INT-003)이다.**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      Tool Calling 테스트 구분                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   단위 테스트 (test_tools.py)                                            │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │ • 개별 도구 함수가 올바른 결과를 반환하는지                         │   │
│   │ • 예: get_column_statistics("나이", config) → "평균: 35.2..."     │   │
│   │ • LLM 호출 없음, 도구 함수만 직접 테스트                           │   │
│   └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│   통합 테스트 (integration/test_tool_calling.py)                         │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │ • 사용자 질문 → LLM → 도구 선택 → 도구 실행 → 결과 반환 전체 흐름   │   │
│   │ • 예: "나이 통계 알려줘" → LLM이 get_column_statistics 선택        │   │
│   │     → 도구 실행 → 결과를 LLM이 자연어로 변환                       │   │
│   │ • LangGraph 워크플로우 전체 검증                                   │   │
│   │ • API Key 필요 (@pytest.mark.api)                                 │   │
│   └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**왜 통합 테스트인가?**
- 단위 테스트: "이 함수가 올바른 값을 반환하는가?"
- 통합 테스트: "LLM이 올바른 도구를 선택하고, 결과를 사용자에게 잘 전달하는가?"

Tool Calling이 "잘 되는지"는 여러 모듈(chatbot, graph, tools)이 협력해야 검증 가능하므로 **통합 테스트**다.

### 2.3 E2E 테스트 (End-to-End)

전체 사용자 시나리오를 검증한다. **Streamlit 특성상 수동 테스트로 진행한다.**

| 시나리오 | 검증 방법 |
|:---------|:---------|
| API Key 입력 → 챗봇 활성화 | 수동 (Streamlit 실행 후 확인) |
| 데이터 업로드 → 시각화 탭 전환 | 수동 |
| 챗봇 질문 → Tool Calling → 응답 | 수동 |

---

## 3. 테스트 실행 방법

### 3.1 전체 테스트 실행

```bash
# API 테스트 제외 (API Key 없을 때)
uv run pytest tests/ -m "not api" -v

# 전체 테스트 (API Key 필요)
uv run pytest tests/ -v
```

### 3.2 특정 테스트만 실행

```bash
# 특정 파일
uv run pytest tests/test_preprocessing.py -v

# 특정 함수
uv run pytest tests/test_preprocessing.py::test_hour_to_period_commute_morning -v

# 특정 클래스
uv run pytest tests/test_preprocessing.py::TestHourToPeriod -v
```

### 3.3 마커로 필터링

```bash
# API 테스트만
uv run pytest -m api -v

# 통합 테스트만
uv run pytest -m integration -v

# 느린 테스트 제외
uv run pytest -m "not slow" -v
```

### 3.4 커버리지 측정

```bash
# 터미널 출력
uv run pytest tests/ --cov=utils --cov-report=term-missing

# HTML 리포트 생성
uv run pytest tests/ --cov=utils --cov-report=html
# → htmlcov/index.html 열어서 확인
```

---

## 4. 개발 워크플로우

### 4.1 새 기능 개발 시 (TDD)

```
1. 테스트 먼저 작성
   └─► tests/test_xxx.py에 실패하는 테스트 작성

2. 최소한의 구현
   └─► 테스트가 통과하도록 코드 작성

3. 리팩토링
   └─► 코드 개선 (테스트는 계속 통과해야 함)

4. 로컬 테스트 실행
   └─► uv run pytest tests/test_xxx.py -v
```

### 4.2 버그 수정 시

```
1. 버그 재현 테스트 작성
   └─► 버그를 발생시키는 테스트 케이스 작성

2. 테스트 실패 확인
   └─► 테스트가 실패하는지 확인 (버그 재현)

3. 버그 수정
   └─► 코드 수정

4. 테스트 통과 확인
   └─► 수정 후 테스트 통과 확인
```

### 4.3 Commit 전 체크리스트

```bash
# 1. 관련 테스트 실행
uv run pytest tests/test_xxx.py -v

# 2. 전체 테스트 실행 (권장)
uv run pytest tests/ -m "not api" -v

# 3. 테스트 통과 확인 후 commit
git add .
git commit -m "feat: xxx 기능 추가"
```

### 4.4 Push 전 체크리스트

```bash
# 1. 전체 테스트 실행 (API 포함)
export ANTHROPIC_API_KEY=sk-ant-xxxxx
uv run pytest tests/ -v

# 2. 커버리지 확인 (선택)
uv run pytest tests/ --cov=utils

# 3. 모든 테스트 통과 후 push
git push origin feature/xxx
```

---

## 5. CI/CD 연동

### 5.1 GitHub Actions 워크플로우

PR 생성 시 자동으로 테스트가 실행된다:

```yaml
# .github/workflows/test.yml
name: Test

on:
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4

      - name: Run unit tests (without API)
        run: uv run pytest tests/ --ignore=tests/integration/ -m "not api" --cov=utils

      - name: Run integration tests (without API)
        run: uv run pytest tests/integration/ -m "not api"

      - name: Run API tests
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: uv run pytest -m api
```

### 5.2 머지 규칙

- **모든 테스트 통과** 필수
- API 테스트도 통과해야 머지 가능
- 테스트 실패 시 PR 머지 불가

### 5.3 왜 PR마다 전체 테스트를 실행하나?

**회귀 테스트(Regression Test)** 때문이다.

```
예시:
1. utils/loader.py의 read_csv_safe() 수정
2. 이 함수는 preprocessing.py에서도 사용됨
3. preprocessing.py를 사용하는 tools.py에도 영향
4. → loader.py만 테스트하면 tools.py의 문제를 발견 못함
5. → 전체 테스트를 돌려야 연쇄적인 문제 발견 가능
```

---

## 6. 디렉토리 구조

```
tests/
├── conftest.py                 # 공통 fixture 정의
├── principle.md                # 테스트 원칙 및 방법론 (추상적)
├── README.md                   # 본 문서 (실천적 가이드)
├── error_explanation.md        # 에러 케이스 설명
│
├── test_preprocessing.py       # utils/preprocessing.py 테스트
├── test_loader.py              # utils/loader.py 테스트
├── test_tools.py               # utils/tools.py 테스트 (22개 도구 전체)
├── test_predictor.py           # utils/predictor.py 테스트 (ECLO 예측)
├── test_geo.py                 # utils/geo.py 테스트
├── test_narration.py           # utils/narration.py 테스트
├── test_graph.py               # utils/graph.py 테스트 (라우팅 로직)
├── test_chatbot.py             # utils/chatbot.py 테스트 (@pytest.mark.api)
├── test_visualizer.py          # utils/visualizer.py 테스트 (선택)
│
└── integration/                # 통합 테스트
    ├── conftest.py             # 통합 테스트 전용 fixture
    ├── test_data_pipeline.py   # INT-001, INT-002
    ├── test_tool_calling.py    # INT-003 (@pytest.mark.api)
    ├── test_map_visualization.py  # INT-004
    ├── test_eclo_pipeline.py   # INT-005 (ECLO 예측 파이프라인)
    └── test_narration_pipeline.py  # INT-006 (내레이션 생성)
```

---

## 7. Fixture 목록

### 7.1 공통 Fixture (conftest.py)

| Fixture | Scope | 설명 |
|:--------|:------|:-----|
| `sample_accident_df` | function | 교통사고 샘플 DataFrame |
| `sample_csv_path` | module | 임시 CSV 파일 경로 |
| `api_key` | session | ANTHROPIC_API_KEY (없으면 skip) |
| `anthropic_client` | session | Anthropic 클라이언트 인스턴스 |

### 7.2 통합 테스트 Fixture (integration/conftest.py)

| Fixture | Scope | 설명 |
|:--------|:------|:-----|
| `preprocessed_accident_df` | module | 전처리 완료된 DataFrame |
| `sample_accident_csv` | module | 교통사고 CSV 파일 (임시) |

---

## 8. FAQ

### Q: API Key 없이 테스트할 수 있나요?

네, `-m "not api"` 옵션으로 API 테스트를 제외하고 실행할 수 있습니다:

```bash
uv run pytest tests/ -m "not api" -v
```

### Q: 테스트가 너무 느린데요?

느린 테스트에는 `@pytest.mark.slow` 마커를 붙이고, 제외하고 실행할 수 있습니다:

```bash
uv run pytest tests/ -m "not slow" -v
```

### Q: 새 테스트 파일은 어디에 만드나요?

- 단위 테스트: `tests/test_{모듈명}.py`
- 통합 테스트: `tests/integration/test_{워크플로우명}.py`

### Q: conftest.py에 fixture를 추가해도 되나요?

네, 여러 테스트 파일에서 공통으로 사용하는 데이터는 `conftest.py`에 fixture로 정의하세요.

### Q: 테스트 실패 시 어떻게 디버깅하나요?

```bash
# 실패한 테스트만 재실행
uv run pytest tests/ --lf -v

# 첫 번째 실패에서 멈춤
uv run pytest tests/ -x -v

# 상세 출력
uv run pytest tests/ -v --tb=long
```

### Q: 커버리지가 낮으면 어떻게 하나요?

1. `--cov-report=html`로 HTML 리포트 생성
2. `htmlcov/index.html` 열어서 테스트되지 않은 라인 확인
3. 해당 라인을 커버하는 테스트 케이스 추가

---

## 관련 문서

- [principle.md](./principle.md) - 테스트 원칙 및 방법론
- [error_explanation.md](./error_explanation.md) - 에러 케이스 설명
- [workflow_template.yaml](./workflow_template.yaml) - GitHub Actions 워크플로우 템플릿
- [TEST_README_TEMPLATE.md](./TEST_README_TEMPLATE.md) - 테스트 README 작성 템플릿
- [docs/constitution.md](../docs/constitution.md) - 프로젝트 개발 규칙
