"""
Tests for accident datetime preprocessing functions.

TDD approach: Tests written before implementation per Constitution XII.
"""
import pytest
import pandas as pd
from utils.preprocessing import hour_to_period, preprocess_accident_datetime


class TestHourToPeriod:
    """Test cases for hour_to_period function (TC1-TC5)."""

    def test_commute_morning_hour_8(self):
        """TC1: 08시 → 출근시간대"""
        assert hour_to_period(8) == "출근시간대"

    def test_commute_morning_hour_7(self):
        """경계값: 07시 → 출근시간대"""
        assert hour_to_period(7) == "출근시간대"

    def test_commute_morning_hour_9(self):
        """경계값: 09시 → 출근시간대"""
        assert hour_to_period(9) == "출근시간대"

    def test_commute_evening_hour_18(self):
        """TC2: 18시 → 퇴근시간대"""
        assert hour_to_period(18) == "퇴근시간대"

    def test_commute_evening_hour_17(self):
        """경계값: 17시 → 퇴근시간대"""
        assert hour_to_period(17) == "퇴근시간대"

    def test_commute_evening_hour_19(self):
        """경계값: 19시 → 퇴근시간대"""
        assert hour_to_period(19) == "퇴근시간대"

    def test_late_night_hour_23(self):
        """TC3: 23시 → 심야"""
        assert hour_to_period(23) == "심야"

    def test_late_night_hour_22(self):
        """경계값: 22시 → 심야"""
        assert hour_to_period(22) == "심야"

    def test_early_morning_hour_3(self):
        """TC4: 03시 → 심야"""
        assert hour_to_period(3) == "심야"

    def test_early_morning_hour_0(self):
        """경계값: 00시 → 심야"""
        assert hour_to_period(0) == "심야"

    def test_early_morning_hour_5(self):
        """경계값: 05시 → 심야"""
        assert hour_to_period(5) == "심야"

    def test_general_hour_14(self):
        """TC5: 14시 → 일반시간대"""
        assert hour_to_period(14) == "일반시간대"

    def test_general_hour_6(self):
        """경계값: 06시 → 일반시간대 (심야 끝난 직후)"""
        assert hour_to_period(6) == "일반시간대"

    def test_general_hour_10(self):
        """경계값: 10시 → 일반시간대 (출근 끝난 직후)"""
        assert hour_to_period(10) == "일반시간대"

    def test_general_hour_16(self):
        """경계값: 16시 → 일반시간대 (퇴근 시작 전)"""
        assert hour_to_period(16) == "일반시간대"

    def test_general_hour_20(self):
        """경계값: 20시 → 일반시간대 (퇴근 끝난 직후)"""
        assert hour_to_period(20) == "일반시간대"

    def test_general_hour_21(self):
        """경계값: 21시 → 일반시간대 (심야 시작 전)"""
        assert hour_to_period(21) == "일반시간대"


class TestPreprocessAccidentDatetime:
    """Test cases for preprocess_accident_datetime function (TC6-TC8)."""

    def test_normal_data_creates_5_columns(self, sample_accident_df):
        """TC6: 정상 데이터 → 5개 컬럼 생성 (사고연, 사고월, 사고일, 사고시, 시간대)"""
        result = preprocess_accident_datetime(sample_accident_df)

        # 5개 파생 컬럼 존재 확인
        assert '사고연' in result.columns
        assert '사고월' in result.columns
        assert '사고일' in result.columns
        assert '사고시' in result.columns
        assert '시간대' in result.columns

        # 첫 번째 행 검증: '2022-01-01 08'
        assert result.iloc[0]['사고연'] == 2022
        assert result.iloc[0]['사고월'] == 1
        assert result.iloc[0]['사고일'] == 1
        assert result.iloc[0]['사고시'] == 8
        assert result.iloc[0]['시간대'] == '출근시간대'

        # 두 번째 행 검증: '2022-06-15 18'
        assert result.iloc[1]['사고연'] == 2022
        assert result.iloc[1]['사고월'] == 6
        assert result.iloc[1]['사고일'] == 15
        assert result.iloc[1]['사고시'] == 18
        assert result.iloc[1]['시간대'] == '퇴근시간대'

        # 세 번째 행 검증: '2022-12-31 23'
        assert result.iloc[2]['시간대'] == '심야'

        # 네 번째 행 검증: '2022-03-10 03'
        assert result.iloc[3]['시간대'] == '심야'

        # 다섯 번째 행 검증: '2022-07-20 14'
        assert result.iloc[4]['시간대'] == '일반시간대'

    def test_missing_column_returns_original(self, sample_df_without_datetime):
        """TC7: 사고일시 컬럼 미존재 → 원본 반환"""
        result = preprocess_accident_datetime(sample_df_without_datetime)

        # 원본과 동일해야 함
        assert '사고연' not in result.columns
        assert '시간대' not in result.columns
        assert list(result.columns) == list(sample_df_without_datetime.columns)
        assert len(result) == len(sample_df_without_datetime)

    def test_invalid_datetime_rows_excluded(self, sample_df_with_invalid_datetime):
        """TC8: 파싱 실패 행 → 해당 행 제외"""
        result = preprocess_accident_datetime(sample_df_with_invalid_datetime)

        # 유효한 행만 남아야 함 (5개 중 3개)
        assert len(result) == 3
        # 파생 컬럼 존재 확인
        assert '시간대' in result.columns

    def test_original_data_not_modified(self, sample_accident_df):
        """FR-009: 원본 데이터 변경 금지 - DataFrame.copy() 사용 확인"""
        original_len = len(sample_accident_df)
        original_cols = list(sample_accident_df.columns)

        _ = preprocess_accident_datetime(sample_accident_df)

        # 원본 DataFrame 변경 없음 확인
        assert len(sample_accident_df) == original_len
        assert list(sample_accident_df.columns) == original_cols

    def test_derived_columns_have_correct_types(self, sample_accident_df):
        """파생 컬럼 데이터 타입 검증"""
        result = preprocess_accident_datetime(sample_accident_df)

        # 정수형 컬럼
        assert result['사고연'].dtype in ['int64', 'int32', 'Int64']
        assert result['사고월'].dtype in ['int64', 'int32', 'Int64']
        assert result['사고일'].dtype in ['int64', 'int32', 'Int64']
        assert result['사고시'].dtype in ['int64', 'int32', 'Int64']

        # 문자열 컬럼
        assert result['시간대'].dtype == 'object'

    def test_time_period_values_are_valid(self, sample_accident_df):
        """시간대 값이 유효한 범주인지 확인"""
        result = preprocess_accident_datetime(sample_accident_df)
        valid_periods = {'출근시간대', '퇴근시간대', '심야', '일반시간대'}

        for period in result['시간대']:
            assert period in valid_periods
