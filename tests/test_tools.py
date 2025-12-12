"""
Tests for data analysis tools.

대상: utils/tools.py
의도: LangGraph 기반 AI 챗봇의 22개 분석 도구 기능 검증
TDD approach: Tests written before implementation per Constitution XII.
"""
import pytest
import pandas as pd
import numpy as np
from utils.tools import (
    get_dataframe_from_config,
    get_dataframe_info,
    get_column_statistics,
    get_missing_values,
    get_value_counts,
    filter_dataframe,
    sort_dataframe,
    get_correlation,
    group_by_aggregate,
    get_unique_values,
    get_date_range,
    get_outliers,
    get_sample_rows,
    calculate_percentile,
    get_geo_bounds,
    cross_tabulation,
    analyze_missing_pattern,
    get_column_correlation_with_target,
    detect_data_types,
    get_temporal_pattern,
    summarize_categorical_distribution,
    get_all_tools,
)


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def sample_df():
    """기본 테스트용 DataFrame."""
    return pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'age': [25, 30, 35, 40, 45],
        'score': [90.5, 85.0, 92.3, 78.5, 88.0],
        'city': ['Seoul', 'Busan', 'Seoul', 'Daegu', 'Seoul'],
        'date': ['2022-01-01', '2022-02-15', '2022-03-20', '2022-04-10', '2022-05-05']
    })


@pytest.fixture
def sample_config(sample_df):
    """RunnableConfig 형식의 설정."""
    return {"configurable": {"dataframe": sample_df, "current_dataset": "test"}}


@pytest.fixture
def empty_config():
    """빈 DataFrame을 포함하는 설정."""
    return {"configurable": {"dataframe": pd.DataFrame(), "current_dataset": "empty"}}


@pytest.fixture
def no_df_config():
    """DataFrame이 없는 설정."""
    return {"configurable": {}}


@pytest.fixture
def geo_df():
    """위경도 데이터가 포함된 DataFrame."""
    return pd.DataFrame({
        '위도': [35.8714, 35.8682, 35.8701],
        '경도': [128.6014, 128.5961, 128.5988],
        'name': ['A', 'B', 'C']
    })


@pytest.fixture
def geo_config(geo_df):
    """위경도 DataFrame 설정."""
    return {"configurable": {"dataframe": geo_df, "current_dataset": "geo"}}


@pytest.fixture
def missing_df():
    """결측값이 포함된 DataFrame."""
    return pd.DataFrame({
        'col1': [1, 2, None, 4, None],
        'col2': [None, 'b', 'c', None, 'e'],
        'col3': [10.0, 20.0, 30.0, 40.0, 50.0]
    })


@pytest.fixture
def missing_config(missing_df):
    """결측값 DataFrame 설정."""
    return {"configurable": {"dataframe": missing_df, "current_dataset": "missing"}}


# ============================================================================
# Helper Function Tests
# ============================================================================

class TestGetDataframeFromConfig:
    """
    대상: utils/tools.py - get_dataframe_from_config()
    의도: RunnableConfig에서 DataFrame 추출 기능 검증
    """

    def test_get_dataframe_success(self, sample_config):
        """
        대상: utils/tools.py:26 - get_dataframe_from_config()
        의도: 정상 설정에서 DataFrame 추출 검증
        """
        df = get_dataframe_from_config(sample_config)
        assert len(df) == 5
        assert 'name' in df.columns

    def test_get_dataframe_missing_raises_error(self, no_df_config):
        """
        대상: utils/tools.py:26 - get_dataframe_from_config()
        의도: DataFrame 없을 때 KeyError 발생 검증
        """
        with pytest.raises(KeyError):
            get_dataframe_from_config(no_df_config)


# ============================================================================
# Data Analysis Tool Tests (20개)
# ============================================================================

class TestGetDataframeInfo:
    """
    대상: utils/tools.py - get_dataframe_info()
    의도: DataFrame 기본 정보 반환 기능 검증
    """

    def test_normal_dataframe_info(self, sample_config):
        """
        대상: utils/tools.py:46 - get_dataframe_info()
        의도: 정상 DataFrame 정보 반환 검증
        """
        result = get_dataframe_info.invoke({}, config=sample_config)
        assert "5" in result  # 행 수
        assert "5" in result  # 열 수
        assert "name" in result
        assert "age" in result

    def test_empty_dataframe_info(self, empty_config):
        """
        대상: utils/tools.py:46 - get_dataframe_info()
        의도: 빈 DataFrame 정보 반환 검증
        """
        result = get_dataframe_info.invoke({}, config=empty_config)
        assert "빈 DataFrame" in result

    def test_no_dataframe_error(self, no_df_config):
        """
        대상: utils/tools.py:46 - get_dataframe_info()
        의도: DataFrame 없을 때 에러 메시지 반환 검증
        """
        result = get_dataframe_info.invoke({}, config=no_df_config)
        assert "데이터셋이 없습니다" in result


class TestGetColumnStatistics:
    """
    대상: utils/tools.py - get_column_statistics()
    의도: 수치형 컬럼 통계 반환 기능 검증
    """

    def test_numeric_column_statistics(self, sample_config):
        """
        대상: utils/tools.py:73 - get_column_statistics()
        의도: 수치형 컬럼 통계 반환 검증
        """
        result = get_column_statistics.invoke({"column": "age"}, config=sample_config)
        assert "평균" in result
        assert "중앙값" in result
        assert "35" in result  # 중앙값

    def test_nonexistent_column(self, sample_config):
        """
        대상: utils/tools.py:73 - get_column_statistics()
        의도: 존재하지 않는 컬럼 에러 메시지 검증
        """
        result = get_column_statistics.invoke({"column": "nonexistent"}, config=sample_config)
        assert "찾을 수 없습니다" in result

    def test_non_numeric_column(self, sample_config):
        """
        대상: utils/tools.py:73 - get_column_statistics()
        의도: 비수치형 컬럼 에러 메시지 검증
        """
        result = get_column_statistics.invoke({"column": "name"}, config=sample_config)
        assert "수치형이 아닙니다" in result


class TestGetMissingValues:
    """
    대상: utils/tools.py - get_missing_values()
    의도: 결측값 정보 반환 기능 검증
    """

    def test_missing_values_analysis(self, missing_config):
        """
        대상: utils/tools.py:113 - get_missing_values()
        의도: 결측값 분석 결과 반환 검증
        """
        result = get_missing_values.invoke({}, config=missing_config)
        assert "결측치 현황" in result
        assert "col1" in result
        assert "col2" in result

    def test_no_missing_values(self, sample_config):
        """
        대상: utils/tools.py:113 - get_missing_values()
        의도: 결측값 없는 DataFrame 분석 검증
        """
        result = get_missing_values.invoke({}, config=sample_config)
        assert "0개" in result or "0%" in result


class TestGetValueCounts:
    """
    대상: utils/tools.py - get_value_counts()
    의도: 범주형 컬럼 값 분포 반환 기능 검증
    """

    def test_value_counts_normal(self, sample_config):
        """
        대상: utils/tools.py:140 - get_value_counts()
        의도: 범주형 컬럼 값 분포 반환 검증
        """
        result = get_value_counts.invoke({"column": "city"}, config=sample_config)
        assert "Seoul" in result
        assert "3" in result  # Seoul 개수

    def test_value_counts_with_top_n(self, sample_config):
        """
        대상: utils/tools.py:140 - get_value_counts()
        의도: top_n 파라미터 적용 검증
        """
        result = get_value_counts.invoke({"column": "city", "top_n": 2}, config=sample_config)
        assert "값 분포" in result

    def test_value_counts_nonexistent_column(self, sample_config):
        """
        대상: utils/tools.py:140 - get_value_counts()
        의도: 존재하지 않는 컬럼 에러 메시지 검증
        """
        result = get_value_counts.invoke({"column": "nonexistent"}, config=sample_config)
        assert "찾을 수 없습니다" in result


class TestFilterDataframe:
    """
    대상: utils/tools.py - filter_dataframe()
    의도: DataFrame 필터링 기능 검증
    """

    def test_filter_equal(self, sample_config):
        """
        대상: utils/tools.py:166 - filter_dataframe()
        의도: == 연산자 필터링 검증
        """
        result = filter_dataframe.invoke({
            "column": "city",
            "operator": "==",
            "value": "Seoul"
        }, config=sample_config)
        assert "필터링 후 행 수: 3" in result

    def test_filter_greater_than(self, sample_config):
        """
        대상: utils/tools.py:166 - filter_dataframe()
        의도: > 연산자 필터링 검증
        """
        result = filter_dataframe.invoke({
            "column": "age",
            "operator": ">",
            "value": 30
        }, config=sample_config)
        assert "필터링 결과" in result

    def test_filter_contains(self, sample_config):
        """
        대상: utils/tools.py:166 - filter_dataframe()
        의도: contains 연산자 필터링 검증
        """
        result = filter_dataframe.invoke({
            "column": "name",
            "operator": "contains",
            "value": "e"
        }, config=sample_config)
        assert "필터링 결과" in result


class TestSortDataframe:
    """
    대상: utils/tools.py - sort_dataframe()
    의도: DataFrame 정렬 기능 검증
    """

    def test_sort_ascending(self, sample_config):
        """
        대상: utils/tools.py:215 - sort_dataframe()
        의도: 오름차순 정렬 검증
        """
        result = sort_dataframe.invoke({
            "column": "age",
            "ascending": True,
            "top_n": 3
        }, config=sample_config)
        assert "오름차순" in result

    def test_sort_descending(self, sample_config):
        """
        대상: utils/tools.py:215 - sort_dataframe()
        의도: 내림차순 정렬 검증
        """
        result = sort_dataframe.invoke({
            "column": "score",
            "ascending": False,
            "top_n": 3
        }, config=sample_config)
        assert "내림차순" in result


class TestGetCorrelation:
    """
    대상: utils/tools.py - get_correlation()
    의도: 상관관계 분석 기능 검증
    """

    def test_correlation_all_numeric(self, sample_config):
        """
        대상: utils/tools.py:248 - get_correlation()
        의도: 모든 수치형 컬럼 상관관계 분석 검증
        """
        result = get_correlation.invoke({}, config=sample_config)
        assert "상관계수 행렬" in result
        assert "age" in result
        assert "score" in result

    def test_correlation_specific_columns(self, sample_config):
        """
        대상: utils/tools.py:248 - get_correlation()
        의도: 특정 컬럼 상관관계 분석 검증
        """
        result = get_correlation.invoke({"columns": ["age", "score"]}, config=sample_config)
        assert "상관계수 행렬" in result


class TestGroupByAggregate:
    """
    대상: utils/tools.py - group_by_aggregate()
    의도: 그룹별 집계 기능 검증
    """

    def test_group_by_mean(self, sample_config):
        """
        대상: utils/tools.py:281 - group_by_aggregate()
        의도: 그룹별 평균 집계 검증
        """
        result = group_by_aggregate.invoke({
            "group_column": "city",
            "agg_column": "age",
            "operation": "mean"
        }, config=sample_config)
        assert "그룹별 집계" in result
        assert "평균" in result

    def test_group_by_count(self, sample_config):
        """
        대상: utils/tools.py:281 - group_by_aggregate()
        의도: 그룹별 개수 집계 검증
        """
        result = group_by_aggregate.invoke({
            "group_column": "city",
            "agg_column": "name",
            "operation": "count"
        }, config=sample_config)
        assert "개수" in result


class TestGetUniqueValues:
    """
    대상: utils/tools.py - get_unique_values()
    의도: 고유값 조회 기능 검증
    """

    def test_unique_values(self, sample_config):
        """
        대상: utils/tools.py:327 - get_unique_values()
        의도: 고유값 목록 반환 검증
        """
        result = get_unique_values.invoke({"column": "city"}, config=sample_config)
        assert "고유값" in result
        assert "Seoul" in result
        assert "Busan" in result
        assert "Daegu" in result


class TestGetDateRange:
    """
    대상: utils/tools.py - get_date_range()
    의도: 날짜 범위 분석 기능 검증
    """

    def test_date_range_analysis(self, sample_config):
        """
        대상: utils/tools.py:355 - get_date_range()
        의도: 날짜 범위 분석 결과 검증
        """
        result = get_date_range.invoke({"column": "date"}, config=sample_config)
        assert "날짜 범위" in result
        assert "시작 날짜" in result
        assert "종료 날짜" in result


class TestGetOutliers:
    """
    대상: utils/tools.py - get_outliers()
    의도: IQR 기반 이상치 탐지 기능 검증
    """

    def test_outlier_detection(self, sample_config):
        """
        대상: utils/tools.py:392 - get_outliers()
        의도: 이상치 탐지 결과 검증
        """
        result = get_outliers.invoke({"column": "age"}, config=sample_config)
        assert "이상치 분석" in result
        assert "Q1" in result
        assert "Q3" in result
        assert "IQR" in result


class TestGetSampleRows:
    """
    대상: utils/tools.py - get_sample_rows()
    의도: 샘플 행 추출 기능 검증
    """

    def test_sample_rows_default(self, sample_config):
        """
        대상: utils/tools.py:441 - get_sample_rows()
        의도: 기본 샘플 추출 검증
        """
        result = get_sample_rows.invoke({"n": 3}, config=sample_config)
        assert "샘플 데이터" in result

    def test_sample_rows_with_condition(self, sample_config):
        """
        대상: utils/tools.py:441 - get_sample_rows()
        의도: 조건부 샘플 추출 검증
        """
        result = get_sample_rows.invoke({
            "n": 2,
            "column": "city",
            "value": "Seoul"
        }, config=sample_config)
        assert "Seoul" in result


class TestCalculatePercentile:
    """
    대상: utils/tools.py - calculate_percentile()
    의도: 백분위수 계산 기능 검증
    """

    def test_percentile_50(self, sample_config):
        """
        대상: utils/tools.py:481 - calculate_percentile()
        의도: 50번째 백분위수(중앙값) 계산 검증
        """
        result = calculate_percentile.invoke({
            "column": "age",
            "percentile": 50
        }, config=sample_config)
        assert "백분위수" in result
        assert "35" in result  # 중앙값

    def test_percentile_invalid_range(self, sample_config):
        """
        대상: utils/tools.py:481 - calculate_percentile()
        의도: 잘못된 백분위수 범위 에러 검증
        """
        result = calculate_percentile.invoke({
            "column": "age",
            "percentile": 150
        }, config=sample_config)
        assert "0-100 사이" in result


class TestGetGeoBounds:
    """
    대상: utils/tools.py - get_geo_bounds()
    의도: 지리적 범위 반환 기능 검증
    """

    def test_geo_bounds(self, geo_config):
        """
        대상: utils/tools.py:514 - get_geo_bounds()
        의도: 위경도 범위 반환 검증
        """
        result = get_geo_bounds.invoke({}, config=geo_config)
        assert "지리적 범위" in result
        assert "위도" in result
        assert "경도" in result

    def test_geo_bounds_no_coordinates(self, sample_config):
        """
        대상: utils/tools.py:514 - get_geo_bounds()
        의도: 좌표 컬럼 없을 때 에러 메시지 검증
        """
        result = get_geo_bounds.invoke({}, config=sample_config)
        assert "찾을 수 없습니다" in result


class TestCrossTabulation:
    """
    대상: utils/tools.py - cross_tabulation()
    의도: 교차표 생성 기능 검증
    """

    def test_cross_tab_normal(self, sample_config):
        """
        대상: utils/tools.py:554 - cross_tabulation()
        의도: 교차표 생성 검증
        """
        # city와 name의 교차표는 의미 없지만 기능 테스트 용도
        result = cross_tabulation.invoke({
            "row_column": "city",
            "col_column": "name"
        }, config=sample_config)
        assert "교차표" in result


class TestAnalyzeMissingPattern:
    """
    대상: utils/tools.py - analyze_missing_pattern()
    의도: 결측값 패턴 분석 기능 검증
    """

    def test_missing_pattern_analysis(self, missing_config):
        """
        대상: utils/tools.py:594 - analyze_missing_pattern()
        의도: 결측값 패턴 분석 결과 검증
        """
        result = analyze_missing_pattern.invoke({"column": "col1"}, config=missing_config)
        assert "결측값 패턴 분석" in result


class TestGetColumnCorrelationWithTarget:
    """
    대상: utils/tools.py - get_column_correlation_with_target()
    의도: 타겟 컬럼 상관관계 분석 기능 검증
    """

    def test_target_correlation(self, sample_config):
        """
        대상: utils/tools.py:664 - get_column_correlation_with_target()
        의도: 타겟 컬럼과의 상관관계 분석 검증
        """
        result = get_column_correlation_with_target.invoke({
            "target_column": "age"
        }, config=sample_config)
        assert "상관관계 분석" in result


class TestDetectDataTypes:
    """
    대상: utils/tools.py - detect_data_types()
    의도: 데이터 타입 추론 기능 검증
    """

    def test_data_type_detection(self, sample_config):
        """
        대상: utils/tools.py:717 - detect_data_types()
        의도: 컬럼별 데이터 타입 추론 검증
        """
        result = detect_data_types.invoke({}, config=sample_config)
        assert "데이터 타입 분석" in result
        assert "name" in result
        assert "age" in result


class TestGetTemporalPattern:
    """
    대상: utils/tools.py - get_temporal_pattern()
    의도: 시간 패턴 분석 기능 검증
    """

    def test_temporal_pattern_analysis(self, sample_config):
        """
        대상: utils/tools.py:794 - get_temporal_pattern()
        의도: 시간 패턴 분석 결과 검증
        """
        result = get_temporal_pattern.invoke({"column": "date"}, config=sample_config)
        assert "시간 패턴 분석" in result


class TestSummarizeCategoricalDistribution:
    """
    대상: utils/tools.py - summarize_categorical_distribution()
    의도: 범주형 컬럼 분포 요약 기능 검증
    """

    def test_categorical_summary(self, sample_config):
        """
        대상: utils/tools.py:854 - summarize_categorical_distribution()
        의도: 범주형 컬럼 분포 요약 검증
        """
        result = summarize_categorical_distribution.invoke({
            "column": "city"
        }, config=sample_config)
        assert "범주형 분포 분석" in result
        assert "고유 카테고리 수" in result


# ============================================================================
# Tool Export Tests
# ============================================================================

class TestGetAllTools:
    """
    대상: utils/tools.py - get_all_tools()
    의도: 전체 도구 리스트 반환 기능 검증
    """

    def test_all_tools_count(self):
        """
        대상: utils/tools.py:1116 - get_all_tools()
        의도: 전체 도구 개수(22개) 확인
        """
        tools = get_all_tools()
        assert len(tools) == 22

    def test_all_tools_have_name(self):
        """
        대상: utils/tools.py:1116 - get_all_tools()
        의도: 모든 도구가 name 속성을 가지는지 확인
        """
        tools = get_all_tools()
        for tool in tools:
            assert hasattr(tool, 'name')
            assert tool.name is not None

    def test_all_tools_have_description(self):
        """
        대상: utils/tools.py:1116 - get_all_tools()
        의도: 모든 도구가 description 속성을 가지는지 확인
        """
        tools = get_all_tools()
        for tool in tools:
            assert hasattr(tool, 'description')
            assert tool.description is not None
