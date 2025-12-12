"""
Unit tests for visualizer module.

대상: utils/visualizer.py
의도: Plotly 차트 및 Folium 지도 생성 함수들이 올바르게 동작하는지 검증
"""
import pytest
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import folium

from utils.visualizer import (
    check_missing_ratio,
    plot_numeric_distribution,
    plot_categorical_distribution,
    plot_boxplot,
    plot_kde,
    plot_scatter,
    plot_with_options,
    create_folium_map,
    create_overlay_map,
    PLOT_COLORS,
)


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def numeric_df():
    """수치형 데이터가 포함된 테스트 DataFrame"""
    np.random.seed(42)
    return pd.DataFrame({
        '값': np.random.randn(100),
        '점수': np.random.randint(0, 100, 100),
        '금액': np.random.uniform(1000, 10000, 100),
    })


@pytest.fixture
def categorical_df():
    """범주형 데이터가 포함된 테스트 DataFrame"""
    return pd.DataFrame({
        '카테고리': ['A', 'B', 'C', 'A', 'B', 'A', 'C', 'D', 'A', 'B'] * 10,
        '지역': ['서울', '부산', '대구', '서울', '부산'] * 20,
    })


@pytest.fixture
def geo_df():
    """지리 좌표가 포함된 테스트 DataFrame"""
    return pd.DataFrame({
        '위도': [35.87, 35.88, 35.86, 35.89, 35.85],
        '경도': [128.60, 128.61, 128.59, 128.62, 128.58],
        '이름': ['A', 'B', 'C', 'D', 'E'],
        '값': [10, 20, 30, 40, 50],
    })


@pytest.fixture
def missing_df():
    """결측값이 포함된 테스트 DataFrame"""
    return pd.DataFrame({
        '값': [1, 2, None, 4, None, 6, 7, None, 9, 10],
        '완전': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    })


# ============================================================================
# check_missing_ratio 테스트
# ============================================================================

class TestCheckMissingRatio:
    """check_missing_ratio 함수 테스트"""

    def test_no_missing_values(self, numeric_df):
        """의도: 결측값이 없는 경우 False 반환 검증"""
        is_above, ratio = check_missing_ratio(numeric_df, '값')
        assert is_above == False
        assert ratio == 0.0

    def test_above_threshold(self, missing_df):
        """의도: 결측값이 임계치 이상인 경우 True 반환 검증"""
        is_above, ratio = check_missing_ratio(missing_df, '값', threshold=0.2)
        assert is_above == True
        assert ratio == 0.3  # 3/10 = 30%

    def test_below_threshold(self, missing_df):
        """의도: 결측값이 임계치 미만인 경우 False 반환 검증"""
        is_above, ratio = check_missing_ratio(missing_df, '값', threshold=0.5)
        assert is_above == False
        assert ratio == 0.3

    def test_exact_threshold(self, missing_df):
        """의도: 결측값이 정확히 임계치인 경우 True 반환 검증"""
        is_above, ratio = check_missing_ratio(missing_df, '값', threshold=0.3)
        assert is_above == True

    def test_empty_dataframe(self):
        """의도: 빈 DataFrame에서 0.0 반환 검증"""
        df = pd.DataFrame({'값': []})
        is_above, ratio = check_missing_ratio(df, '값')
        assert is_above == False
        assert ratio == 0.0


# ============================================================================
# plot_numeric_distribution 테스트
# ============================================================================

class TestPlotNumericDistribution:
    """plot_numeric_distribution 함수 테스트"""

    def test_returns_figure(self, numeric_df):
        """의도: Plotly Figure 객체 반환 검증"""
        fig = plot_numeric_distribution(numeric_df, '값')
        assert isinstance(fig, go.Figure)

    def test_auto_generated_title(self, numeric_df):
        """의도: 타이틀이 자동 생성되는지 검증"""
        fig = plot_numeric_distribution(numeric_df, '값')
        assert '값' in fig.layout.title.text

    def test_custom_title(self, numeric_df):
        """의도: 커스텀 타이틀이 적용되는지 검증"""
        fig = plot_numeric_distribution(numeric_df, '값', title='커스텀 타이틀')
        assert fig.layout.title.text == '커스텀 타이틀'

    def test_missing_values_in_title(self, missing_df):
        """의도: 결측값 개수가 타이틀에 포함되는지 검증"""
        fig = plot_numeric_distribution(missing_df, '값')
        assert 'missing' in fig.layout.title.text.lower() or '3' in fig.layout.title.text


# ============================================================================
# plot_categorical_distribution 테스트
# ============================================================================

class TestPlotCategoricalDistribution:
    """plot_categorical_distribution 함수 테스트"""

    def test_returns_figure(self, categorical_df):
        """의도: Plotly Figure 객체 반환 검증"""
        fig = plot_categorical_distribution(categorical_df, '카테고리')
        assert isinstance(fig, go.Figure)

    def test_top_n_categories(self, categorical_df):
        """의도: top_n 파라미터가 적용되는지 검증"""
        fig = plot_categorical_distribution(categorical_df, '카테고리', top_n=2)
        # 2개 카테고리만 표시되어야 함
        assert fig is not None

    def test_auto_title_with_total(self, categorical_df):
        """의도: 전체 카테고리 수가 타이틀에 포함되는지 검증"""
        fig = plot_categorical_distribution(categorical_df, '카테고리', top_n=2)
        title = fig.layout.title.text
        assert 'Top' in title or '카테고리' in title


# ============================================================================
# plot_boxplot 테스트
# ============================================================================

class TestPlotBoxplot:
    """plot_boxplot 함수 테스트"""

    def test_returns_figure(self, numeric_df):
        """의도: Plotly Figure 객체 반환 검증"""
        fig = plot_boxplot(numeric_df, '값')
        assert isinstance(fig, go.Figure)

    def test_custom_title(self, numeric_df):
        """의도: 커스텀 타이틀이 적용되는지 검증"""
        fig = plot_boxplot(numeric_df, '값', title='박스플롯 테스트')
        assert fig.layout.title.text == '박스플롯 테스트'

    def test_missing_values_handled(self, missing_df):
        """의도: 결측값이 있어도 정상 동작하는지 검증"""
        fig = plot_boxplot(missing_df, '값')
        assert isinstance(fig, go.Figure)


# ============================================================================
# plot_kde 테스트
# ============================================================================

class TestPlotKde:
    """plot_kde 함수 테스트"""

    def test_returns_figure(self, numeric_df):
        """의도: Plotly Figure 객체 반환 검증"""
        fig = plot_kde(numeric_df, '값')
        assert isinstance(fig, go.Figure)

    def test_insufficient_data(self):
        """의도: 데이터가 부족한 경우 빈 Figure 반환 검증"""
        df = pd.DataFrame({'값': [1]})
        fig = plot_kde(df, '값')
        assert isinstance(fig, go.Figure)

    def test_all_missing_data(self):
        """의도: 모든 값이 결측인 경우 처리 검증"""
        df = pd.DataFrame({'값': [None, None, None]})
        fig = plot_kde(df, '값')
        assert isinstance(fig, go.Figure)


# ============================================================================
# plot_scatter 테스트
# ============================================================================

class TestPlotScatter:
    """plot_scatter 함수 테스트"""

    def test_returns_figure(self, numeric_df):
        """의도: Plotly Figure 객체 반환 검증"""
        fig = plot_scatter(numeric_df, '값', '점수')
        assert isinstance(fig, go.Figure)

    def test_auto_title(self, numeric_df):
        """의도: 자동 생성 타이틀이 두 컬럼명을 포함하는지 검증"""
        fig = plot_scatter(numeric_df, '값', '점수')
        title = fig.layout.title.text
        assert '값' in title and '점수' in title

    def test_custom_title(self, numeric_df):
        """의도: 커스텀 타이틀이 적용되는지 검증"""
        fig = plot_scatter(numeric_df, '값', '점수', title='산점도 테스트')
        assert fig.layout.title.text == '산점도 테스트'


# ============================================================================
# plot_with_options 테스트
# ============================================================================

class TestPlotWithOptions:
    """plot_with_options 함수 테스트"""

    def test_histogram_option(self, numeric_df):
        """의도: histogram 옵션이 정상 동작하는지 검증"""
        fig = plot_with_options(numeric_df, '값', chart_type='histogram')
        assert isinstance(fig, go.Figure)

    def test_boxplot_option(self, numeric_df):
        """의도: boxplot 옵션이 정상 동작하는지 검증"""
        fig = plot_with_options(numeric_df, '값', chart_type='boxplot')
        assert isinstance(fig, go.Figure)

    def test_kde_option(self, numeric_df):
        """의도: kde 옵션이 정상 동작하는지 검증"""
        fig = plot_with_options(numeric_df, '값', chart_type='kde')
        assert isinstance(fig, go.Figure)

    def test_scatter_option(self, numeric_df):
        """의도: scatter 옵션이 정상 동작하는지 검증"""
        fig = plot_with_options(numeric_df, '값', chart_type='scatter', y_column='점수')
        assert isinstance(fig, go.Figure)

    def test_scatter_without_y_column_raises(self, numeric_df):
        """의도: scatter에서 y_column 없이 호출 시 ValueError 발생 검증"""
        with pytest.raises(ValueError, match="y_column"):
            plot_with_options(numeric_df, '값', chart_type='scatter')

    def test_unknown_chart_type_raises(self, numeric_df):
        """의도: 알 수 없는 차트 타입에서 ValueError 발생 검증"""
        with pytest.raises(ValueError, match="Unknown chart type"):
            plot_with_options(numeric_df, '값', chart_type='unknown')


# ============================================================================
# create_folium_map 테스트
# ============================================================================

class TestCreateFoliumMap:
    """create_folium_map 함수 테스트"""

    def test_returns_folium_map(self, geo_df):
        """의도: folium.Map 객체 반환 검증"""
        m = create_folium_map(geo_df, '위도', '경도')
        assert isinstance(m, folium.Map)

    def test_empty_dataframe(self):
        """의도: 빈 DataFrame에서 기본 대구 중심 지도 반환 검증"""
        df = pd.DataFrame({'위도': [], '경도': []})
        m = create_folium_map(df, '위도', '경도')
        assert isinstance(m, folium.Map)

    def test_with_popup_cols(self, geo_df):
        """의도: popup_cols 파라미터가 적용되는지 검증"""
        m = create_folium_map(geo_df, '위도', '경도', popup_cols=['이름', '값'])
        assert isinstance(m, folium.Map)

    def test_custom_color(self, geo_df):
        """의도: 커스텀 색상이 적용되는지 검증"""
        m = create_folium_map(geo_df, '위도', '경도', color='red')
        assert isinstance(m, folium.Map)

    def test_max_points_sampling(self):
        """의도: max_points 초과 시 샘플링이 적용되는지 검증"""
        # 1000개 포인트 생성
        df = pd.DataFrame({
            '위도': np.random.uniform(35.8, 35.9, 1000),
            '경도': np.random.uniform(128.5, 128.7, 1000),
        })
        m = create_folium_map(df, '위도', '경도', max_points=100)
        assert isinstance(m, folium.Map)

    def test_missing_coordinates_dropped(self):
        """의도: 결측 좌표가 제거되는지 검증"""
        df = pd.DataFrame({
            '위도': [35.87, None, 35.86],
            '경도': [128.60, 128.61, None],
        })
        m = create_folium_map(df, '위도', '경도')
        assert isinstance(m, folium.Map)

    @pytest.mark.slow
    def test_large_dataset_performance(self):
        """의도: 대용량 데이터셋에서도 정상 동작하는지 검증"""
        df = pd.DataFrame({
            '위도': np.random.uniform(35.8, 35.9, 5000),
            '경도': np.random.uniform(128.5, 128.7, 5000),
        })
        m = create_folium_map(df, '위도', '경도', max_points=5000)
        assert isinstance(m, folium.Map)


# ============================================================================
# create_overlay_map 테스트
# ============================================================================

class TestCreateOverlayMap:
    """create_overlay_map 함수 테스트"""

    def test_empty_datasets(self):
        """의도: 빈 datasets 리스트에서 기본 지도 반환 검증"""
        m = create_overlay_map([])
        assert isinstance(m, folium.Map)

    def test_single_dataset(self, geo_df):
        """의도: 단일 데이터셋으로 지도 생성 검증"""
        datasets = [{
            'df': geo_df,
            'lat_col': '위도',
            'lng_col': '경도',
            'name': 'Test Layer',
            'color': 'blue',
        }]
        m = create_overlay_map(datasets)
        assert isinstance(m, folium.Map)

    def test_multiple_datasets(self, geo_df):
        """의도: 여러 데이터셋 오버레이 검증"""
        geo_df2 = geo_df.copy()
        geo_df2['위도'] = geo_df2['위도'] + 0.01

        datasets = [
            {
                'df': geo_df,
                'lat_col': '위도',
                'lng_col': '경도',
                'name': 'Layer 1',
                'color': 'blue',
            },
            {
                'df': geo_df2,
                'lat_col': '위도',
                'lng_col': '경도',
                'name': 'Layer 2',
                'color': 'red',
            },
        ]
        m = create_overlay_map(datasets)
        assert isinstance(m, folium.Map)

    def test_with_popup_cols(self, geo_df):
        """의도: popup_cols가 포함된 오버레이 검증"""
        datasets = [{
            'df': geo_df,
            'lat_col': '위도',
            'lng_col': '경도',
            'popup_cols': ['이름', '값'],
            'name': 'Test',
        }]
        m = create_overlay_map(datasets)
        assert isinstance(m, folium.Map)


# ============================================================================
# PLOT_COLORS 상수 테스트
# ============================================================================

class TestPlotColors:
    """PLOT_COLORS 상수 테스트"""

    def test_required_keys_exist(self):
        """의도: 필수 색상 키가 존재하는지 검증"""
        required_keys = ['primary', 'secondary', 'histogram', 'boxplot', 'kde', 'scatter']
        for key in required_keys:
            assert key in PLOT_COLORS

    def test_valid_hex_colors(self):
        """의도: 모든 색상이 유효한 hex 형식인지 검증"""
        for key, color in PLOT_COLORS.items():
            assert color.startswith('#'), f"{key} color should be hex format"
            assert len(color) == 7, f"{key} color should be #RRGGBB format"
