"""
Integration tests for map visualization pipeline.

대상: INT-004 (지도 시각화 파이프라인)
의도: geo → visualizer 연결 검증 (좌표 감지 → folium 지도 생성)
"""
import pytest
import pandas as pd
from utils.geo import (
    detect_lat_lng_columns,
    haversine_distance,
    validate_coordinates,
    compute_proximity_stats,
)
from utils.tools import get_geo_bounds


# ============================================================================
# INT-004: 지도 시각화 파이프라인
# ============================================================================

class TestMapVisualizationPipeline:
    """
    INT-004: 지도 시각화 파이프라인 통합 테스트
    흐름: geo.detect_lat_lng_columns() → visualizer.create_folium_map()

    Note: visualizer.create_folium_map()은 Streamlit/Folium 의존성이 있어
          geo 모듈 레벨에서 통합 테스트를 진행함
    """

    @pytest.mark.integration
    def test_detect_columns_then_get_bounds(self, geo_df):
        """
        의도: 좌표 컬럼 자동 감지 후 지리적 범위 조회 파이프라인 검증
        """
        # Step 1: 좌표 컬럼 감지
        lat_col, lng_col = detect_lat_lng_columns(geo_df)
        assert lat_col == '위도'
        assert lng_col == '경도'

        # Step 2: 도구를 통한 지리적 범위 조회
        config = {"configurable": {"dataframe": geo_df, "current_dataset": "geo"}}
        result = get_geo_bounds.invoke({}, config=config)

        # Assert
        assert "지리적 범위" in result
        assert "위도" in result
        assert "경도" in result

    @pytest.mark.integration
    def test_coordinate_validation_pipeline(self, geo_df):
        """
        의도: 좌표 감지 → 좌표 유효성 검증 파이프라인 검증
        """
        # Step 1: 좌표 컬럼 감지
        lat_col, lng_col = detect_lat_lng_columns(geo_df)

        # Step 2: 각 좌표 유효성 검증
        for idx, row in geo_df.iterrows():
            lat = row[lat_col]
            lng = row[lng_col]

            # 대구 범위 내 좌표인지 검증
            is_valid = validate_coordinates(lat, lng)
            assert is_valid, f"({lat}, {lng})가 대구 범위 밖으로 판정됨"

    @pytest.mark.integration
    def test_distance_calculation_pipeline(self, geo_df):
        """
        의도: 좌표 감지 → 거리 계산 파이프라인 검증
        """
        # Step 1: 좌표 컬럼 감지
        lat_col, lng_col = detect_lat_lng_columns(geo_df)

        # Step 2: 첫 번째와 두 번째 포인트 간 거리 계산
        lat1, lng1 = geo_df.iloc[0][lat_col], geo_df.iloc[0][lng_col]
        lat2, lng2 = geo_df.iloc[1][lat_col], geo_df.iloc[1][lng_col]

        distance = haversine_distance(lat1, lng1, lat2, lng2)

        # Assert - 거리는 양수
        assert distance > 0
        # 같은 도시 내이므로 대략 0-10km 범위
        assert distance < 10

    @pytest.mark.integration
    def test_proximity_stats_pipeline(self, geo_df):
        """
        의도: 좌표 감지 → 근접성 통계 계산 파이프라인 검증
        """
        # Step 1: 좌표 컬럼 감지
        lat_col, lng_col = detect_lat_lng_columns(geo_df)

        # Step 2: 자기 자신과의 근접성 통계 (테스트용)
        proximity_df = compute_proximity_stats(
            geo_df, lat_col, lng_col,
            geo_df, lat_col, lng_col,
            thresholds=[0.5, 1.0]
        )

        # Assert
        assert len(proximity_df) == len(geo_df)
        assert '0.5' in proximity_df.columns
        assert '1.0' in proximity_df.columns

        # 자기 자신은 항상 포함되므로 최소 1 이상
        assert (proximity_df['1.0'] >= 1).all()

    @pytest.mark.integration
    def test_no_coords_pipeline(self):
        """
        의도: 좌표 컬럼 없는 DataFrame으로 파이프라인 실행 시 처리 검증
        """
        # Arrange - 좌표 없는 DataFrame
        no_geo_df = pd.DataFrame({
            'name': ['A', 'B', 'C'],
            'value': [1, 2, 3]
        })

        # Step 1: 좌표 컬럼 감지 실패
        lat_col, lng_col = detect_lat_lng_columns(no_geo_df)
        assert lat_col is None
        assert lng_col is None

        # Step 2: get_geo_bounds 도구는 에러 메시지 반환
        config = {"configurable": {"dataframe": no_geo_df, "current_dataset": "test"}}
        result = get_geo_bounds.invoke({}, config=config)

        assert "찾을 수 없습니다" in result


class TestProximityAnalysisPipeline:
    """근접성 분석 파이프라인 통합 테스트"""

    @pytest.mark.integration
    def test_proximity_between_two_datasets(self, geo_df):
        """
        의도: 두 데이터셋 간 근접성 분석 파이프라인 검증
        """
        # Arrange - 기준 데이터셋과 타겟 데이터셋 생성
        base_df = geo_df.head(2).copy()
        target_df = geo_df.tail(3).copy()

        lat_col, lng_col = detect_lat_lng_columns(geo_df)

        # Act
        proximity_df = compute_proximity_stats(
            base_df, lat_col, lng_col,
            target_df, lat_col, lng_col,
            thresholds=[0.5, 1.0, 2.0]
        )

        # Assert
        assert len(proximity_df) == 2  # base_df 행 수
        assert '0.5' in proximity_df.columns
        assert '1.0' in proximity_df.columns
        assert '2.0' in proximity_df.columns

        # 더 큰 threshold는 더 많은 count
        for idx in range(len(proximity_df)):
            assert proximity_df.loc[idx, '2.0'] >= proximity_df.loc[idx, '1.0']
            assert proximity_df.loc[idx, '1.0'] >= proximity_df.loc[idx, '0.5']

    @pytest.mark.integration
    def test_proximity_with_empty_target(self, geo_df):
        """
        의도: 빈 타겟 데이터셋으로 근접성 분석 시 모든 count가 0인지 검증
        """
        # Arrange
        lat_col, lng_col = detect_lat_lng_columns(geo_df)
        empty_target = pd.DataFrame({'위도': [], '경도': []})

        # Act
        proximity_df = compute_proximity_stats(
            geo_df, lat_col, lng_col,
            empty_target, lat_col, lng_col,
            thresholds=[0.5, 1.0]
        )

        # Assert - 모든 count가 0
        assert (proximity_df['0.5'] == 0).all()
        assert (proximity_df['1.0'] == 0).all()


class TestCoordinateDetectionVariants:
    """다양한 좌표 컬럼명 감지 통합 테스트"""

    @pytest.mark.integration
    def test_detect_lat_lng_variants(self):
        """
        의도: 다양한 좌표 컬럼명 형식이 감지되는지 검증
        """
        test_cases = [
            ({"lat": [35.87], "lng": [128.60]}, "lat", "lng"),
            ({"latitude": [35.87], "longitude": [128.60]}, "latitude", "longitude"),
            ({"위도": [35.87], "경도": [128.60]}, "위도", "경도"),
            ({"y": [35.87], "x": [128.60]}, "y", "x"),
            ({"Lat": [35.87], "Lng": [128.60]}, "Lat", "Lng"),
        ]

        for data, expected_lat, expected_lng in test_cases:
            df = pd.DataFrame(data)
            lat_col, lng_col = detect_lat_lng_columns(df)
            assert lat_col == expected_lat, f"Expected {expected_lat}, got {lat_col}"
            assert lng_col == expected_lng, f"Expected {expected_lng}, got {lng_col}"

    @pytest.mark.integration
    def test_detect_fails_with_partial_coords(self):
        """
        의도: 위도만 있고 경도가 없는 경우 감지 실패하는지 검증
        """
        partial_df = pd.DataFrame({"lat": [35.87], "name": ["A"]})
        lat_col, lng_col = detect_lat_lng_columns(partial_df)

        assert lat_col is None
        assert lng_col is None
