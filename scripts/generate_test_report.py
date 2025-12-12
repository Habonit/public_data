#!/usr/bin/env python3
"""
테스트 결과 및 커버리지 마크다운 리포트 생성 스크립트

테스트를 실행하고 결과를 마크다운 리포트로 생성합니다.
리포트는 tests/result/{yyyy_mm_dd_HH_MM}/test_report.md 경로에 저장됩니다.

사용법:
    # 기본 실행 (API 테스트 제외)
    uv run python scripts/generate_test_report.py

    # 전체 테스트 실행
    uv run python scripts/generate_test_report.py --all

    # 특정 마커 필터
    uv run python scripts/generate_test_report.py --filter api
    uv run python scripts/generate_test_report.py --filter slow
    uv run python scripts/generate_test_report.py --filter "not api"
    uv run python scripts/generate_test_report.py --filter "not slow"
    uv run python scripts/generate_test_report.py --filter "not api and not slow"

출력 경로:
    tests/result/{yyyy_mm_dd_HH_MM}/test_report.md
    (예: tests/result/2025_12_12_18_30/test_report.md)
"""
import argparse
import subprocess
import sys
import json
import re
from datetime import datetime
from pathlib import Path


# 사전 정의된 필터 옵션
FILTER_PRESETS = {
    "all": None,  # 전체 테스트
    "api": "api",  # API 테스트만
    "slow": "slow",  # 느린 테스트만
    "not-api": "not api",  # API 제외 (기본값)
    "not-slow": "not slow",  # 느린 테스트 제외
    "quick": "not api and not slow",  # 빠른 테스트 (API, slow 제외)
    "integration": "integration",  # 통합 테스트만
}


def parse_args() -> argparse.Namespace:
    """커맨드라인 인자 파싱"""
    parser = argparse.ArgumentParser(
        description="테스트 결과 및 커버리지 마크다운 리포트 생성",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예제:
  %(prog)s                          # 기본 (API 테스트 제외)
  %(prog)s --all                    # 전체 테스트
  %(prog)s --filter api             # API 테스트만
  %(prog)s --filter slow            # 느린 테스트만
  %(prog)s --filter "not api"       # API 제외
  %(prog)s --filter "not slow"      # 느린 테스트 제외
  %(prog)s --filter quick           # 빠른 테스트 (API, slow 제외)
  %(prog)s --filter integration     # 통합 테스트만
  %(prog)s --filter "api or slow"   # 커스텀 pytest 마커 표현식
        """
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--all", "-a",
        action="store_true",
        help="전체 테스트 실행 (필터 없음)"
    )
    group.add_argument(
        "--filter", "-f",
        type=str,
        metavar="MARKER",
        help="pytest 마커 필터 (예: api, slow, 'not api', quick)"
    )

    return parser.parse_args()


def get_marker_filter(args: argparse.Namespace) -> tuple[str | None, str]:
    """인자에서 마커 필터와 설명 추출

    Returns:
        (marker_expression, description) 튜플
    """
    if args.all:
        return None, "전체 테스트"

    if args.filter:
        # 사전 정의된 프리셋 확인
        if args.filter in FILTER_PRESETS:
            marker = FILTER_PRESETS[args.filter]
            if marker is None:
                return None, "전체 테스트"
            return marker, f"`-m \"{marker}\"`"
        # 커스텀 마커 표현식
        return args.filter, f"`-m \"{args.filter}\"`"

    # 기본값: not api
    return "not api", "`-m \"not api\"` (기본값)"


def run_pytest_with_coverage(marker_filter: str | None = None) -> tuple[str, str]:
    """pytest를 실행하고 결과를 반환

    Args:
        marker_filter: pytest 마커 필터 표현식 (None이면 필터 없음)
    """
    cmd = [
        sys.executable, "-m", "pytest", "tests/",
        "--cov=utils",
        "--cov-report=json:coverage.json",
        "--tb=no",
        "-q",
        "--no-header"
    ]
    if marker_filter:
        cmd.extend(["-m", marker_filter])

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent
    )
    return result.stdout, result.stderr


def count_tests_by_marker() -> dict:
    """마커별 테스트 수 계산"""
    markers = {}
    base_cmd = [sys.executable, "-m", "pytest", "tests/", "--collect-only", "-q"]

    # 전체 테스트 수
    result = subprocess.run(base_cmd, capture_output=True, text=True, cwd=Path(__file__).parent.parent)
    total_match = re.search(r'(\d+)\s+tests?\s+collected', result.stdout + result.stderr)
    markers["total"] = int(total_match.group(1)) if total_match else 0

    # 마커별 테스트 수
    for marker in ["api", "slow", "integration"]:
        result = subprocess.run(
            base_cmd + ["-m", marker],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        match = re.search(r'(\d+)/\d+\s+tests?\s+collected', result.stdout + result.stderr)
        markers[marker] = int(match.group(1)) if match else 0

    return markers


def parse_test_results(output: str) -> dict:
    """테스트 결과 파싱"""
    results = {
        "passed": 0,
        "failed": 0,
        "skipped": 0,
        "errors": 0,
        "warnings": 0,
        "total": 0,
        "duration": "0s"
    }

    # 결과 라인 파싱 (예: "170 passed, 3 warnings in 141.17s")
    match = re.search(
        r'(\d+)\s+passed(?:,\s*(\d+)\s+failed)?(?:,\s*(\d+)\s+skipped)?(?:,\s*(\d+)\s+error)?(?:,\s*(\d+)\s+warning)?.*?in\s+([\d.]+s)',
        output
    )
    if match:
        results["passed"] = int(match.group(1)) if match.group(1) else 0
        results["failed"] = int(match.group(2)) if match.group(2) else 0
        results["skipped"] = int(match.group(3)) if match.group(3) else 0
        results["errors"] = int(match.group(4)) if match.group(4) else 0
        results["warnings"] = int(match.group(5)) if match.group(5) else 0
        results["duration"] = match.group(6) if match.group(6) else "0s"

    results["total"] = results["passed"] + results["failed"] + results["skipped"] + results["errors"]

    return results


def load_coverage_json() -> dict:
    """coverage.json 파일 로드"""
    coverage_file = Path(__file__).parent.parent / "coverage.json"
    if coverage_file.exists():
        with open(coverage_file, "r") as f:
            return json.load(f)
    return {}


def get_module_coverage(coverage_data: dict) -> list[dict]:
    """모듈별 커버리지 정보 추출"""
    modules = []
    files = coverage_data.get("files", {})

    for filepath, data in files.items():
        if "utils/" in filepath:
            module_name = Path(filepath).name
            summary = data.get("summary", {})
            modules.append({
                "name": module_name,
                "statements": summary.get("num_statements", 0),
                "missing": summary.get("missing_lines", 0),
                "covered": summary.get("covered_lines", 0),
                "coverage": summary.get("percent_covered", 0),
            })

    # 커버리지 순으로 정렬
    modules.sort(key=lambda x: x["coverage"], reverse=True)
    return modules


def get_coverage_badge(percent: float) -> str:
    """커버리지 퍼센트에 따른 뱃지 이모지 반환"""
    if percent >= 90:
        return "🟢"
    elif percent >= 70:
        return "🟡"
    elif percent >= 50:
        return "🟠"
    else:
        return "🔴"


def generate_markdown_report(
    test_results: dict,
    coverage_data: dict,
    marker_counts: dict | None = None,
    filter_description: str = ""
) -> str:
    """마크다운 리포트 생성

    Args:
        test_results: 테스트 결과 딕셔너리
        coverage_data: 커버리지 데이터
        marker_counts: 마커별 테스트 수
        filter_description: 적용된 필터 설명
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 전체 커버리지
    totals = coverage_data.get("totals", {})
    total_coverage = totals.get("percent_covered", 0)
    total_statements = totals.get("num_statements", 0)
    total_missing = totals.get("missing_lines", 0)

    # 성공률 계산
    if test_results["total"] > 0:
        success_rate = (test_results["passed"] / test_results["total"]) * 100
    else:
        success_rate = 0

    # 마커 정보 (기본값)
    if marker_counts is None:
        marker_counts = {"total": 0, "api": 0, "slow": 0, "integration": 0}

    # 모듈별 커버리지
    modules = get_module_coverage(coverage_data)

    # 필터 정보 표시
    filter_info = f"\n**테스트 필터**: {filter_description}\n" if filter_description else ""

    report = f"""# 테스트 결과 리포트

**생성 시각**: {now}
{filter_info}
---

## 요약

| 지표 | 값 |
|:-----|:---|
| 테스트 성공률 | **{success_rate:.1f}%** ({test_results["passed"]}/{test_results["total"]}) |
| 코드 커버리지 | **{total_coverage:.1f}%** ({total_statements - total_missing}/{total_statements} statements) |
| 실행 시간 | {test_results["duration"]} |

---

## 테스트 결과

| 상태 | 개수 |
|:-----|-----:|
| ✅ Passed | {test_results["passed"]} |
| ❌ Failed | {test_results["failed"]} |
| ⏭️ Skipped | {test_results["skipped"]} |
| ⚠️ Warnings | {test_results["warnings"]} |
| **Total** | **{test_results["total"]}** |

---

## 모듈별 커버리지

| 모듈 | 커버리지 | Statements | Missing | 상태 |
|:-----|--------:|-----------:|--------:|:----:|
"""

    for module in modules:
        badge = get_coverage_badge(module["coverage"])
        report += f"| `{module['name']}` | {module['coverage']:.1f}% | {module['statements']} | {module['missing']} | {badge} |\n"

    report += f"| **Total** | **{total_coverage:.1f}%** | **{total_statements}** | **{total_missing}** | {get_coverage_badge(total_coverage)} |\n"

    report += f"""
---

## 테스트 마커 분류

| 마커 | 테스트 수 | 설명 |
|:-----|--------:|:-----|
| `@pytest.mark.api` | {marker_counts.get('api', 0)} | 외부 API 호출 필요 (ANTHROPIC_API_KEY) |
| `@pytest.mark.slow` | {marker_counts.get('slow', 0)} | 실행 시간이 긴 테스트 (10초+) |
| `@pytest.mark.integration` | {marker_counts.get('integration', 0)} | 여러 모듈 연결 통합 테스트 |
| (마커 없음) | {marker_counts.get('total', 0) - marker_counts.get('api', 0) - marker_counts.get('slow', 0)} | 일반 단위 테스트 |
| **Total** | **{marker_counts.get('total', 0)}** | |

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
"""

    return report


def get_output_path() -> Path:
    """테스트 시작 시각 기반 출력 경로 생성

    Returns:
        tests/result/{yyyy_mm_dd_HH_MM}/test_report.md 경로
    """
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
    return Path(__file__).parent.parent / "tests" / "result" / timestamp / "test_report.md"


def main():
    """테스트 실행 및 리포트 생성 메인 함수"""
    args = parse_args()
    marker_filter, filter_description = get_marker_filter(args)

    # 테스트 시작 시각 기록 (출력 경로용)
    output_path = get_output_path()

    print(f"🧪 테스트 실행 중... (필터: {filter_description})")
    stdout, stderr = run_pytest_with_coverage(marker_filter)

    print("📊 결과 분석 중...")
    test_results = parse_test_results(stdout + stderr)
    coverage_data = load_coverage_json()

    print("🏷️ 마커별 테스트 수 집계 중...")
    marker_counts = count_tests_by_marker()

    print("📝 리포트 생성 중...")
    report = generate_markdown_report(test_results, coverage_data, marker_counts, filter_description)

    # 출력 디렉토리 생성 및 파일 저장
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")

    print(f"✅ 리포트 생성 완료: {output_path}")

    # 요약 출력
    totals = coverage_data.get("totals", {})
    print(f"\n📈 요약:")
    print(f"   - 테스트: {test_results['passed']}/{test_results['total']} passed")
    print(f"   - 커버리지: {totals.get('percent_covered', 0):.1f}%")

    # coverage.json 정리
    coverage_file = Path(__file__).parent.parent / "coverage.json"
    if coverage_file.exists():
        coverage_file.unlink()


if __name__ == "__main__":
    main()
