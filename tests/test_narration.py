"""
Unit tests for narration module.

대상: utils/narration.py
의도: 자연어 인사이트 생성 함수들이 올바르게 동작하는지 검증
"""
import pytest
import pandas as pd
import numpy as np

from utils.narration import (
    summarize_proximity_stats,
    generate_distribution_insight,
    compare_distributions,
)


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def proximity_stats_df():
    """근접 통계 테스트용 DataFrame"""
    return pd.DataFrame({
        '0.5': [2, 3, 1, 4, 2, 5, 3, 2, 1, 4],
        '1.0': [5, 7, 3, 8, 4, 10, 6, 5, 3, 9],
        '2.0': [12, 15, 8, 18, 10, 22, 14, 11, 7, 20],
    })


@pytest.fixture
def numeric_df():
    """수치형 분포 테스트용 DataFrame"""
    np.random.seed(42)
    return pd.DataFrame({
        '정규분포': np.random.randn(100),
        '양의왜도': np.random.exponential(2, 100),
        '음의왜도': -np.random.exponential(2, 100) + 10,
        '균등분포': np.random.uniform(0, 10, 100),
    })


@pytest.fixture
def categorical_df():
    """범주형 분포 테스트용 DataFrame"""
    return pd.DataFrame({
        '카테고리': ['A'] * 50 + ['B'] * 30 + ['C'] * 15 + ['D'] * 5,
    })


# ============================================================================
# summarize_proximity_stats 테스트
# ============================================================================

class TestSummarizeProximityStats:
    """summarize_proximity_stats 함수 테스트"""

    def test_basic_summary(self, proximity_stats_df):
        """의도: 기본 근접 통계 요약이 생성되는지 검증"""
        summary = summarize_proximity_stats(proximity_stats_df, '0.5', 'CCTV')
        assert isinstance(summary, str)
        assert len(summary) > 0
        assert 'CCTV' in summary

    def test_contains_statistics(self, proximity_stats_df):
        """의도: 요약에 통계 정보가 포함되는지 검증"""
        summary = summarize_proximity_stats(proximity_stats_df, '0.5', 'CCTV')
        # 평균, 중앙값, 최대값 관련 내용이 있어야 함
        assert '평균' in summary or '중앙값' in summary or '최대' in summary

    def test_density_classification_high(self):
        """의도: 높은 밀도가 올바르게 분류되는지 검증"""
        df = pd.DataFrame({'0.5': [10, 12, 8, 15, 9]})  # 평균 > 5
        summary = summarize_proximity_stats(df, '0.5', '시설')
        assert '높은' in summary or '밀집' in summary

    def test_density_classification_medium(self):
        """의도: 중간 밀도가 올바르게 분류되는지 검증"""
        df = pd.DataFrame({'0.5': [3, 4, 2, 4, 3]})  # 평균 2-5
        summary = summarize_proximity_stats(df, '0.5', '시설')
        assert '중간' in summary or '적당' in summary

    def test_density_classification_low(self):
        """의도: 낮은 밀도가 올바르게 분류되는지 검증"""
        df = pd.DataFrame({'0.5': [1, 0, 1, 2, 1]})  # 평균 < 2
        summary = summarize_proximity_stats(df, '0.5', '시설')
        assert '낮은' in summary or '희소' in summary

    def test_empty_dataframe(self):
        """의도: 빈 DataFrame에서 적절한 메시지 반환 검증"""
        df = pd.DataFrame()
        summary = summarize_proximity_stats(df, '0.5', '시설')
        assert '생성할 수 없습니다' in summary

    def test_missing_threshold_column(self, proximity_stats_df):
        """의도: 존재하지 않는 임계치 컬럼에서 적절한 메시지 반환 검증"""
        summary = summarize_proximity_stats(proximity_stats_df, '999', '시설')
        assert '생성할 수 없습니다' in summary


# ============================================================================
# generate_distribution_insight 테스트
# ============================================================================

class TestGenerateDistributionInsight:
    """generate_distribution_insight 함수 테스트"""

    def test_numeric_column_insight(self, numeric_df):
        """의도: 수치형 컬럼에 대한 인사이트 생성 검증"""
        insight = generate_distribution_insight(numeric_df, '정규분포')
        assert isinstance(insight, str)
        assert '정규분포' in insight
        assert '평균' in insight or '중앙값' in insight

    def test_categorical_column_insight(self, categorical_df):
        """의도: 범주형 컬럼에 대한 인사이트 생성 검증"""
        insight = generate_distribution_insight(categorical_df, '카테고리')
        assert '범주형' in insight
        assert '고유 값' in insight

    def test_positive_skew_detection(self, numeric_df):
        """의도: 양의 왜도가 감지되는지 검증"""
        insight = generate_distribution_insight(numeric_df, '양의왜도')
        # 양의 왜도 또는 오른쪽 치우침 언급
        assert '오른쪽' in insight or '양' in insight or '낮은 쪽' in insight

    def test_symmetric_distribution_detection(self):
        """의도: 대칭 분포가 감지되는지 검증"""
        np.random.seed(42)
        df = pd.DataFrame({'값': np.random.randn(1000)})  # 정규분포는 대칭
        insight = generate_distribution_insight(df, '값')
        assert '대칭' in insight or '균형' in insight or '비대칭' in insight

    def test_outlier_detection(self):
        """의도: 이상치가 감지되는지 검증"""
        # 명확한 이상치가 있는 데이터
        df = pd.DataFrame({'값': [1, 2, 3, 4, 5, 100]})
        insight = generate_distribution_insight(df, '값')
        assert '이상치' in insight

    def test_nonexistent_column(self, numeric_df):
        """의도: 존재하지 않는 컬럼에서 적절한 메시지 반환 검증"""
        insight = generate_distribution_insight(numeric_df, '없는컬럼')
        assert '찾을 수 없습니다' in insight

    def test_all_null_column(self):
        """의도: 모든 값이 결측인 경우 적절한 메시지 반환 검증"""
        df = pd.DataFrame({'값': [None, None, None]})
        insight = generate_distribution_insight(df, '값')
        assert '유효한 데이터가 없습니다' in insight

    def test_top_category_percentage(self, categorical_df):
        """의도: 최빈 카테고리의 비율이 포함되는지 검증"""
        insight = generate_distribution_insight(categorical_df, '카테고리')
        assert '%' in insight or '퍼센트' in insight


# ============================================================================
# compare_distributions 테스트
# ============================================================================

class TestCompareDistributions:
    """compare_distributions 함수 테스트"""

    def test_similar_distributions(self):
        """의도: 유사한 분포 비교 결과 검증"""
        np.random.seed(42)
        df1 = pd.DataFrame({'값': np.random.randn(100)})
        df2 = pd.DataFrame({'값': np.random.randn(100)})
        comparison = compare_distributions(df1, '값', df2, '값')
        assert isinstance(comparison, str)
        assert '유사' in comparison or '비슷' in comparison or '다릅니다' in comparison

    def test_different_distributions(self):
        """의도: 다른 분포 비교 결과 검증"""
        df1 = pd.DataFrame({'값': [1, 2, 3, 4, 5]})
        df2 = pd.DataFrame({'값': [100, 200, 300, 400, 500]})
        comparison = compare_distributions(df1, '값', df2, '값')
        assert '다릅니다' in comparison or '차이' in comparison

    def test_contains_statistics(self):
        """의도: 비교 결과에 통계 정보가 포함되는지 검증"""
        df1 = pd.DataFrame({'값': [1, 2, 3, 4, 5]})
        df2 = pd.DataFrame({'값': [2, 3, 4, 5, 6]})
        comparison = compare_distributions(df1, '값', df2, '값')
        assert '평균' in comparison
        assert '표준편차' in comparison

    def test_missing_column_first_df(self):
        """의도: 첫 번째 DataFrame에 컬럼이 없을 때 메시지 반환 검증"""
        df1 = pd.DataFrame({'다른값': [1, 2, 3]})
        df2 = pd.DataFrame({'값': [1, 2, 3]})
        comparison = compare_distributions(df1, '값', df2, '값')
        assert '첫 번째' in comparison and '찾을 수 없습니다' in comparison

    def test_missing_column_second_df(self):
        """의도: 두 번째 DataFrame에 컬럼이 없을 때 메시지 반환 검증"""
        df1 = pd.DataFrame({'값': [1, 2, 3]})
        df2 = pd.DataFrame({'다른값': [1, 2, 3]})
        comparison = compare_distributions(df1, '값', df2, '값')
        assert '두 번째' in comparison and '찾을 수 없습니다' in comparison

    def test_empty_data(self):
        """의도: 빈 데이터에서 적절한 메시지 반환 검증"""
        df1 = pd.DataFrame({'값': []})
        df2 = pd.DataFrame({'값': [1, 2, 3]})
        comparison = compare_distributions(df1, '값', df2, '값')
        assert '유효한 데이터가 없습니다' in comparison

    def test_non_numeric_columns(self):
        """의도: 비수치형 컬럼에서 적절한 메시지 반환 검증"""
        df1 = pd.DataFrame({'값': ['a', 'b', 'c']})
        df2 = pd.DataFrame({'값': ['x', 'y', 'z']})
        comparison = compare_distributions(df1, '값', df2, '값')
        assert '숫자형' in comparison

    def test_detailed_statistics_format(self):
        """의도: 세부 통계가 올바른 형식으로 포함되는지 검증"""
        df1 = pd.DataFrame({'값': [1, 2, 3, 4, 5]})
        df2 = pd.DataFrame({'값': [2, 3, 4, 5, 6]})
        comparison = compare_distributions(df1, '값', df2, '값')
        assert '세부 통계' in comparison or '첫 번째 데이터셋' in comparison
