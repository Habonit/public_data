"""
Tests for geospatial utilities.

대상: utils/geo.py
의도: 좌표 감지, 거리 계산, 근접성 통계 기능 검증
TDD approach: Tests written before implementation per Constitution XII.
"""
import pytest
import pandas as pd
from utils.geo import (
    detect_lat_lng_columns,
    haversine_distance,
    validate_coordinates,
    compute_proximity_stats,
)


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def df_with_korean_coords():
    """한글 위경도 컬럼명을 가진 DataFrame."""
    return pd.DataFrame({
        '위도': [35.8714, 35.8682, 35.8701],
        '경도': [128.6014, 128.5961, 128.5988],
        'name': ['A', 'B', 'C']
    })


@pytest.fixture
def df_with_english_coords():
    """영문 위경도 컬럼명을 가진 DataFrame."""
    return pd.DataFrame({
        'lat': [35.8714, 35.8682],
        'lng': [128.6014, 128.5961],
        'name': ['A', 'B']
    })


@pytest.fixture
def df_with_no_coords():
    """좌표 컬럼이 없는 DataFrame."""
    return pd.DataFrame({
        'name': ['Alice', 'Bob'],
        'age': [25, 30]
    })


@pytest.fixture
def df_base():
    """근접성 분석 기준 DataFrame."""
    return pd.DataFrame({
        'lat': [35.8714, 35.8750],
        'lng': [128.6014, 128.6050],
    })


@pytest.fixture
def df_target():
    """근접성 분석 대상 DataFrame."""
    return pd.DataFrame({
        'latitude': [35.8720, 35.8730, 35.8800],
        'longitude': [128.6020, 128.6030, 128.6100],
    })


# ============================================================================
# detect_lat_lng_columns Tests
# ============================================================================

class TestDetectLatLngColumns:
    """
    대상: utils/geo.py - detect_lat_lng_columns()
    의도: 위경도 컬럼 자동 감지 기능 검증
    """

    def test_detect_korean_columns(self, df_with_korean_coords):
        """
        대상: utils/geo.py:8 - detect_lat_lng_columns()
        의도: 한글 컬럼명 (위도, 경도) 감지 검증
        """
        lat_col, lng_col = detect_lat_lng_columns(df_with_korean_coords)
        assert lat_col == '위도'
        assert lng_col == '경도'

    def test_detect_english_columns(self, df_with_english_coords):
        """
        대상: utils/geo.py:8 - detect_lat_lng_columns()
        의도: 영문 컬럼명 (lat, lng) 감지 검증
        """
        lat_col, lng_col = detect_lat_lng_columns(df_with_english_coords)
        assert lat_col == 'lat'
        assert lng_col == 'lng'

    def test_detect_latitude_longitude_columns(self):
        """
        대상: utils/geo.py:8 - detect_lat_lng_columns()
        의도: 전체 영문 컬럼명 (latitude, longitude) 감지 검증
        """
        df = pd.DataFrame({
            'latitude': [35.8714],
            'longitude': [128.6014]
        })
        lat_col, lng_col = detect_lat_lng_columns(df)
        assert lat_col == 'latitude'
        assert lng_col == 'longitude'

    def test_detect_xy_columns(self):
        """
        대상: utils/geo.py:8 - detect_lat_lng_columns()
        의도: x, y 컬럼명 감지 검증
        """
        df = pd.DataFrame({
            'y': [35.8714],  # latitude
            'x': [128.6014]  # longitude
        })
        lat_col, lng_col = detect_lat_lng_columns(df)
        assert lat_col == 'y'
        assert lng_col == 'x'

    def test_detect_no_coords_returns_none(self, df_with_no_coords):
        """
        대상: utils/geo.py:8 - detect_lat_lng_columns()
        의도: 좌표 컬럼 없을 때 (None, None) 반환 검증
        """
        lat_col, lng_col = detect_lat_lng_columns(df_with_no_coords)
        assert lat_col is None
        assert lng_col is None

    def test_detect_partial_coords_returns_none(self):
        """
        대상: utils/geo.py:8 - detect_lat_lng_columns()
        의도: 위도만 있고 경도 없을 때 (None, None) 반환 검증
        """
        df = pd.DataFrame({
            'lat': [35.8714],
            'name': ['A']  # lng 없음
        })
        lat_col, lng_col = detect_lat_lng_columns(df)
        assert lat_col is None
        assert lng_col is None


# ============================================================================
# haversine_distance Tests
# ============================================================================

class TestHaversineDistance:
    """
    대상: utils/geo.py - haversine_distance()
    의도: Haversine 공식 기반 거리 계산 기능 검증
    """

    def test_same_point_returns_zero(self):
        """
        대상: utils/geo.py:53 - haversine_distance()
        의도: 동일 좌표 입력 시 0 반환 검증
        """
        dist = haversine_distance(35.8714, 128.6014, 35.8714, 128.6014)
        assert dist == 0.0

    def test_known_distance(self):
        """
        대상: utils/geo.py:53 - haversine_distance()
        의도: 알려진 거리 계산 정확성 검증

        Note: 대구역(35.8771, 128.5927) ~ 동대구역(35.8797, 128.6277) 약 3.3km
        """
        daegu_station = (35.8771, 128.5927)
        dongdaegu_station = (35.8797, 128.6277)

        dist = haversine_distance(
            daegu_station[0], daegu_station[1],
            dongdaegu_station[0], dongdaegu_station[1]
        )
        # 약 3.1~3.5km 범위
        assert 3.0 < dist < 3.6

    def test_distance_is_positive(self):
        """
        대상: utils/geo.py:53 - haversine_distance()
        의도: 거리 계산 결과가 항상 양수인지 검증
        """
        dist = haversine_distance(35.8714, 128.6014, 35.8800, 128.6100)
        assert dist > 0

    def test_distance_symmetry(self):
        """
        대상: utils/geo.py:53 - haversine_distance()
        의도: A→B 거리와 B→A 거리가 동일한지 검증
        """
        dist_ab = haversine_distance(35.8714, 128.6014, 35.8800, 128.6100)
        dist_ba = haversine_distance(35.8800, 128.6100, 35.8714, 128.6014)
        assert dist_ab == dist_ba

    def test_short_distance(self):
        """
        대상: utils/geo.py:53 - haversine_distance()
        의도: 짧은 거리 (약 100m) 계산 검증
        """
        # 약 0.001도 차이 ≈ 100m
        dist = haversine_distance(35.8714, 128.6014, 35.8724, 128.6014)
        assert 0.1 < dist < 0.15  # 약 100-150m


# ============================================================================
# validate_coordinates Tests
# ============================================================================

class TestValidateCoordinates:
    """
    대상: utils/geo.py - validate_coordinates()
    의도: 좌표 유효성 검증 기능 테스트
    """

    def test_valid_daegu_coordinates(self):
        """
        대상: utils/geo.py:97 - validate_coordinates()
        의도: 대구 범위 내 유효 좌표 검증
        """
        result = validate_coordinates(35.8714, 128.6014)
        assert result is True

    def test_zero_coordinates_invalid(self):
        """
        대상: utils/geo.py:97 - validate_coordinates()
        의도: (0, 0) 좌표 무효 판정 검증
        """
        result = validate_coordinates(0.0, 0.0)
        assert result is False

    def test_out_of_bounds_latitude(self):
        """
        대상: utils/geo.py:97 - validate_coordinates()
        의도: 범위 밖 위도 무효 판정 검증
        """
        # 대구 기본 bounds: lat 35.7-36.1
        result = validate_coordinates(37.0, 128.6014)  # 서울 위도
        assert result is False

    def test_out_of_bounds_longitude(self):
        """
        대상: utils/geo.py:97 - validate_coordinates()
        의도: 범위 밖 경도 무효 판정 검증
        """
        # 대구 기본 bounds: lng 128.4-128.8
        result = validate_coordinates(35.8714, 127.0)  # 서울 경도
        assert result is False

    def test_custom_bounds(self):
        """
        대상: utils/geo.py:97 - validate_coordinates()
        의도: 사용자 정의 bounds 적용 검증
        """
        seoul_bounds = {
            'lat_min': 37.4,
            'lat_max': 37.7,
            'lng_min': 126.8,
            'lng_max': 127.2
        }
        # 서울 좌표
        result = validate_coordinates(37.5665, 126.9780, bounds=seoul_bounds)
        assert result is True

    def test_invalid_latitude_range(self):
        """
        대상: utils/geo.py:97 - validate_coordinates()
        의도: 전역 위도 범위 (-90~90) 벗어남 검증
        """
        result = validate_coordinates(100.0, 128.6014)
        assert result is False

    def test_invalid_longitude_range(self):
        """
        대상: utils/geo.py:97 - validate_coordinates()
        의도: 전역 경도 범위 (-180~180) 벗어남 검증
        """
        result = validate_coordinates(35.8714, 200.0)
        assert result is False


# ============================================================================
# compute_proximity_stats Tests
# ============================================================================

class TestComputeProximityStats:
    """
    대상: utils/geo.py - compute_proximity_stats()
    의도: 근접성 통계 계산 기능 검증
    """

    def test_proximity_stats_returns_dataframe(self, df_base, df_target):
        """
        대상: utils/geo.py:138 - compute_proximity_stats()
        의도: DataFrame 반환 검증
        """
        result = compute_proximity_stats(
            df_base, 'lat', 'lng',
            df_target, 'latitude', 'longitude'
        )
        assert isinstance(result, pd.DataFrame)

    def test_proximity_stats_default_thresholds(self, df_base, df_target):
        """
        대상: utils/geo.py:138 - compute_proximity_stats()
        의도: 기본 threshold (0.5, 1.0, 2.0) 컬럼 존재 검증
        """
        result = compute_proximity_stats(
            df_base, 'lat', 'lng',
            df_target, 'latitude', 'longitude'
        )
        assert '0.5' in result.columns
        assert '1.0' in result.columns
        assert '2.0' in result.columns

    def test_proximity_stats_custom_thresholds(self, df_base, df_target):
        """
        대상: utils/geo.py:138 - compute_proximity_stats()
        의도: 사용자 정의 threshold 적용 검증
        """
        result = compute_proximity_stats(
            df_base, 'lat', 'lng',
            df_target, 'latitude', 'longitude',
            thresholds=[0.3, 0.7]
        )
        assert '0.3' in result.columns
        assert '0.7' in result.columns
        assert '0.5' not in result.columns  # 기본 threshold는 없어야 함

    def test_proximity_stats_row_count(self, df_base, df_target):
        """
        대상: utils/geo.py:138 - compute_proximity_stats()
        의도: 결과 행 수가 기준 DataFrame 행 수와 일치 검증
        """
        result = compute_proximity_stats(
            df_base, 'lat', 'lng',
            df_target, 'latitude', 'longitude'
        )
        assert len(result) == len(df_base)

    def test_proximity_stats_counts_are_non_negative(self, df_base, df_target):
        """
        대상: utils/geo.py:138 - compute_proximity_stats()
        의도: 모든 count 값이 0 이상인지 검증
        """
        result = compute_proximity_stats(
            df_base, 'lat', 'lng',
            df_target, 'latitude', 'longitude'
        )
        for col in result.columns:
            assert (result[col] >= 0).all()

    def test_proximity_stats_larger_threshold_more_counts(self, df_base, df_target):
        """
        대상: utils/geo.py:138 - compute_proximity_stats()
        의도: 더 큰 threshold에서 count가 더 크거나 같음 검증
        """
        result = compute_proximity_stats(
            df_base, 'lat', 'lng',
            df_target, 'latitude', 'longitude',
            thresholds=[0.5, 1.0, 2.0]
        )
        # 2.0 threshold count >= 1.0 threshold count >= 0.5 threshold count
        for idx in range(len(result)):
            assert result.loc[idx, '2.0'] >= result.loc[idx, '1.0']
            assert result.loc[idx, '1.0'] >= result.loc[idx, '0.5']

    def test_proximity_stats_empty_target(self, df_base):
        """
        대상: utils/geo.py:138 - compute_proximity_stats()
        의도: 빈 타겟 DataFrame 시 모든 count가 0인지 검증
        """
        empty_target = pd.DataFrame({
            'latitude': [],
            'longitude': []
        })
        result = compute_proximity_stats(
            df_base, 'lat', 'lng',
            empty_target, 'latitude', 'longitude'
        )
        # 모든 count가 0이어야 함
        for col in result.columns:
            assert (result[col] == 0).all()
