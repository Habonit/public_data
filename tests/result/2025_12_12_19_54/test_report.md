# 테스트 결과 리포트

**생성 시각**: 2025-12-12 20:08:00

**테스트 필터**: 전체 테스트

---

## 요약

| 지표 | 값 |
|:-----|:---|
| 테스트 성공률 | **100.0%** (320/320) |
| 코드 커버리지 | **83.7%** (1185/1416 statements) |
| 실행 시간 | 744.28s |

---

## 테스트 결과

| 상태 | 개수 |
|:-----|-----:|
| ✅ Passed | 320 |
| ❌ Failed | 0 |
| ⏭️ Skipped | 0 |
| ⚠️ Warnings | 3 |
| **Total** | **320** |

---

## 모듈별 커버리지

| 모듈 | 커버리지 | Statements | Missing | 상태 |
|:-----|--------:|-----------:|--------:|:----:|
| `__init__.py` | 100.0% | 8 | 0 | 🟢 |
| `prompts.py` | 100.0% | 26 | 0 | 🟢 |
| `geo.py` | 98.5% | 67 | 1 | 🟢 |
| `chatbot.py` | 95.3% | 215 | 10 | 🟢 |
| `preprocessing.py` | 93.3% | 30 | 2 | 🟢 |
| `visualizer.py` | 93.2% | 176 | 12 | 🟢 |
| `predictor.py` | 92.2% | 102 | 8 | 🟢 |
| `narration.py` | 88.5% | 87 | 10 | 🟡 |
| `graph.py` | 77.1% | 48 | 11 | 🟡 |
| `loader.py` | 75.6% | 78 | 19 | 🟡 |
| `tools.py` | 72.7% | 579 | 158 | 🟡 |
| **Total** | **83.7%** | **1416** | **231** | 🟡 |

---

## 테스트 마커 분류

| 마커 | 테스트 수 | 설명 |
|:-----|--------:|:-----|
| `@pytest.mark.api` | 24 | 외부 API 호출 필요 (ANTHROPIC_API_KEY) |
| `@pytest.mark.slow` | 4 | 실행 시간이 긴 테스트 (10초+) |
| `@pytest.mark.integration` | 41 | 여러 모듈 연결 통합 테스트 |
| (마커 없음) | 292 | 일반 단위 테스트 |
| **Total** | **320** | |

---

## 커버리지 기준

| 상태 | 범위 | 설명 |
|:----:|:-----|:-----|
| 🟢 | 90% 이상 | 우수 |
| 🟡 | 70-89% | 양호 |
| 🟠 | 50-69% | 개선 필요 |
| 🔴 | 50% 미만 | 주의 |

---

## 테스트 실행 방법

```bash
# 기본 실행 (API 테스트 제외)
uv run python scripts/generate_test_report.py

# 전체 테스트 실행
uv run python scripts/generate_test_report.py --all

# 특정 필터 옵션
uv run python scripts/generate_test_report.py --filter api             # API 테스트만
uv run python scripts/generate_test_report.py --filter slow            # 느린 테스트만
uv run python scripts/generate_test_report.py --filter "not api"       # API 제외
uv run python scripts/generate_test_report.py --filter "not slow"      # 느린 테스트 제외
uv run python scripts/generate_test_report.py --filter quick           # 빠른 테스트 (API, slow 제외)
uv run python scripts/generate_test_report.py --filter integration     # 통합 테스트만

# pytest 직접 실행
uv run pytest tests/ -v -m "not api"
uv run pytest tests/ --cov=utils --cov-report=term-missing
```

---

*이 리포트는 `scripts/generate_test_report.py`에 의해 자동 생성되었습니다.*
