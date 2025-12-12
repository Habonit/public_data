"""
Integration tests for data pipeline.

대상: INT-001 (CSV 업로드 → 전처리), INT-002 (전처리 → 도구 실행)
의도: loader → preprocessing → tools 연결 검증
"""
import io
import pytest
import pandas as pd
from utils.loader import read_uploaded_csv, get_dataset_info
from utils.preprocessing import preprocess_accident_datetime
from utils.tools import (
    get_dataframe_info,
    get_temporal_pattern,
    get_value_counts,
    group_by_aggregate,
)


# ============================================================================
# INT-001: CSV 업로드 → 전처리
# ============================================================================

class TestCsvUploadToPreprocessing:
    """
    INT-001: CSV 업로드 → 전처리 통합 테스트
    흐름: loader.read_uploaded_csv() → preprocessing.preprocess_accident_datetime()
    """

    @pytest.mark.integration
    def test_upload_csv_with_preprocessing_applied(self, sample_accident_csv_bytes):
        """
        의도: 업로드된 CSV가 전처리되어 시간대 컬럼이 생성되는지 검증
        """
        # Arrange - 파일 포인터 리셋
        sample_accident_csv_bytes.seek(0)

        # Act - read_uploaded_csv는 내부적으로 preprocess_accident_datetime 호출
        df = read_uploaded_csv(sample_accident_csv_bytes)

        # Assert - 전처리 결과 파생 컬럼 확인
        assert '사고연' in df.columns
        assert '사고월' in df.columns
        assert '사고일' in df.columns
        assert '사고시' in df.columns
        assert '시간대' in df.columns

        # 시간대 값 검증
        assert df['시간대'].isin(['출근시간대', '퇴근시간대', '심야', '일반시간대']).all()

    @pytest.mark.integration
    def test_upload_cp949_csv_with_preprocessing(self):
        """
        의도: CP949 인코딩 CSV도 전처리가 정상 적용되는지 검증
        """
        # Arrange - CP949 인코딩 CSV
        csv_content = "사고일시,기상상태\n2022-01-15 08,맑음\n2022-03-20 14,흐림"
        csv_bytes = io.BytesIO(csv_content.encode('cp949'))

        # Act
        df = read_uploaded_csv(csv_bytes)

        # Assert
        assert '시간대' in df.columns
        assert len(df) == 2

    @pytest.mark.integration
    def test_upload_csv_without_accident_datetime_column(self):
        """
        의도: 사고일시 컬럼이 없는 CSV 업로드 시 전처리 스킵되고 원본 반환
        """
        # Arrange - 사고일시 컬럼 없는 CSV
        csv_content = "이름,나이\n홍길동,30\n김철수,25"
        csv_bytes = io.BytesIO(csv_content.encode('utf-8'))

        # Act
        df = read_uploaded_csv(csv_bytes)

        # Assert - 전처리 스킵됨
        assert '시간대' not in df.columns
        assert '이름' in df.columns
        assert '나이' in df.columns

    @pytest.mark.integration
    def test_preprocessing_then_dataset_info(self, sample_accident_csv_bytes):
        """
        의도: 전처리 후 get_dataset_info가 파생 컬럼을 포함하여 반환하는지 검증
        """
        # Arrange
        sample_accident_csv_bytes.seek(0)
        df = read_uploaded_csv(sample_accident_csv_bytes)

        # Act
        info = get_dataset_info(df)

        # Assert
        assert info['column_count'] >= 6  # 원본 6 + 파생 5 = 11
        assert '시간대' in info['dtypes']
        assert '사고연' in info['dtypes']


# ============================================================================
# INT-002: 전처리 → 도구 실행
# ============================================================================

class TestPreprocessingToTools:
    """
    INT-002: 전처리 → 도구 실행 통합 테스트
    흐름: preprocessing.preprocess_accident_datetime() → tools.*
    """

    @pytest.mark.integration
    def test_preprocessed_data_with_get_dataframe_info(self, preprocessed_accident_df):
        """
        의도: 전처리된 데이터로 get_dataframe_info 도구가 정상 동작하는지 검증
        """
        # Arrange
        config = {"configurable": {"dataframe": preprocessed_accident_df, "current_dataset": "test"}}

        # Act
        result = get_dataframe_info.invoke({}, config=config)

        # Assert
        assert "시간대" in result
        assert "사고연" in result
        assert "5" in result  # 5행

    @pytest.mark.integration
    def test_preprocessed_data_with_temporal_pattern(self, preprocessed_accident_df):
        """
        의도: 전처리된 데이터로 시간 패턴 분석(get_temporal_pattern)이 동작하는지 검증
        """
        # Arrange
        config = {"configurable": {"dataframe": preprocessed_accident_df, "current_dataset": "test"}}

        # Act - 파싱된 사고일시로 시간 패턴 분석
        result = get_temporal_pattern.invoke({"column": "사고일시"}, config=config)

        # Assert
        assert "시간 패턴 분석" in result
        assert "월별 분포" in result

    @pytest.mark.integration
    def test_preprocessed_data_with_value_counts_time_period(self, preprocessed_accident_df):
        """
        의도: 전처리된 시간대 컬럼으로 value_counts가 정상 동작하는지 검증
        """
        # Arrange
        config = {"configurable": {"dataframe": preprocessed_accident_df, "current_dataset": "test"}}

        # Act
        result = get_value_counts.invoke({"column": "시간대"}, config=config)

        # Assert
        assert "시간대" in result
        assert any(period in result for period in ['출근시간대', '퇴근시간대', '심야', '일반시간대'])

    @pytest.mark.integration
    def test_preprocessed_data_with_group_by_time_period(self, preprocessed_accident_df):
        """
        의도: 시간대별 그룹 집계가 정상 동작하는지 검증
        """
        # Arrange
        config = {"configurable": {"dataframe": preprocessed_accident_df, "current_dataset": "test"}}

        # Act
        result = group_by_aggregate.invoke({
            "group_column": "시간대",
            "agg_column": "사고월",
            "operation": "count"
        }, config=config)

        # Assert
        assert "그룹별 집계" in result

    @pytest.mark.integration
    def test_unpreprocessed_data_temporal_column_missing(self, sample_accident_df):
        """
        의도: 전처리 안 된 데이터로 시간대 컬럼 조회 시 에러 처리
        """
        # Arrange - 원본 데이터 (전처리 안 됨)
        config = {"configurable": {"dataframe": sample_accident_df, "current_dataset": "test"}}

        # Act
        result = get_value_counts.invoke({"column": "시간대"}, config=config)

        # Assert - 컬럼 없음 에러 메시지
        assert "찾을 수 없습니다" in result

    @pytest.mark.integration
    def test_full_pipeline_upload_to_analysis(self, sample_accident_csv_bytes):
        """
        의도: CSV 업로드 → 전처리 → 분석 도구 실행 전체 파이프라인 검증
        """
        # Step 1: CSV 업로드 및 전처리
        sample_accident_csv_bytes.seek(0)
        df = read_uploaded_csv(sample_accident_csv_bytes)

        # Step 2: 데이터셋 정보 확인
        info = get_dataset_info(df)
        assert info['row_count'] == 5

        # Step 3: 분석 도구 실행
        config = {"configurable": {"dataframe": df, "current_dataset": "accident"}}

        # 3-1. 기본 정보
        info_result = get_dataframe_info.invoke({}, config=config)
        assert "행 수: 5" in info_result

        # 3-2. 시간대 분포
        time_result = get_value_counts.invoke({"column": "시간대"}, config=config)
        assert "시간대" in time_result

        # 3-3. 기상상태별 집계
        weather_result = group_by_aggregate.invoke({
            "group_column": "기상상태",
            "agg_column": "사고유형",
            "operation": "count"
        }, config=config)
        assert "기상상태" in weather_result
