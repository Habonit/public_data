"""
Pytest configuration and fixtures for public_data tests.
"""
import pytest
import pandas as pd


@pytest.fixture
def sample_accident_df():
    """Sample DataFrame with 사고일시 column for testing."""
    return pd.DataFrame({
        '사고일시': [
            '2022-01-01 08',
            '2022-06-15 18',
            '2022-12-31 23',
            '2022-03-10 03',
            '2022-07-20 14'
        ],
        '기상상태': ['맑음', '흐림', '비', '맑음', '흐림'],
        '사고유형': ['차대차', '차대사람', '차대차', '차대차', '차대사람']
    })


@pytest.fixture
def sample_df_without_datetime():
    """Sample DataFrame without 사고일시 column."""
    return pd.DataFrame({
        '기상상태': ['맑음', '흐림', '비'],
        '사고유형': ['차대차', '차대사람', '차대차']
    })


@pytest.fixture
def sample_df_with_invalid_datetime():
    """Sample DataFrame with some invalid 사고일시 values."""
    return pd.DataFrame({
        '사고일시': [
            '2022-01-01 08',
            'invalid_date',
            '2022-06-15 18',
            'not_a_date',
            '2022-12-31 23'
        ],
        '기상상태': ['맑음', '흐림', '비', '눈', '맑음']
    })
