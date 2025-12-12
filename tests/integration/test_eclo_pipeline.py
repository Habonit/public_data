"""
Integration tests for ECLO prediction pipeline.

대상: INT-005 (ECLO 예측 파이프라인)
의도: predictor 모듈 로드 → 입력 검증 → 예측 반환 연결 검증
"""
import pytest
from utils.predictor import (
    load_model,
    load_encoders,
    load_feature_config,
    encode_features,
    predict_eclo_value,
    interpret_eclo,
    predict_eclo_batch,
)
from utils.tools import predict_eclo, predict_eclo_batch as tool_predict_batch


# ============================================================================
# INT-005: ECLO 예측 파이프라인
# ============================================================================

class TestEcloPredictionPipeline:
    """
    INT-005: ECLO 예측 파이프라인 통합 테스트
    흐름: predictor.load_model() → predictor.encode_features() → predictor.predict_eclo_value()
    """

    @pytest.mark.integration
    def test_full_prediction_pipeline(self, valid_eclo_features):
        """
        의도: 모델 로드 → 피처 인코딩 → 예측 → 해석 전체 파이프라인 검증
        """
        # Step 1: 모델 로드
        model = load_model()
        assert model is not None

        # Step 2: 인코더 로드
        encoders = load_encoders()
        assert encoders is not None

        # Step 3: 설정 로드
        config = load_feature_config()
        assert config is not None
        assert "feature_cols" in config

        # Step 4: 피처 인코딩
        encoded = encode_features(valid_eclo_features)
        assert encoded is not None
        assert len(encoded) == 1

        # Step 5: 예측
        eclo_value = predict_eclo_value(valid_eclo_features)
        assert isinstance(eclo_value, float)
        assert eclo_value >= 0

        # Step 6: 해석
        interpretation = interpret_eclo(eclo_value)
        assert interpretation in ["경미", "일반", "심각", "매우 심각"]

    @pytest.mark.integration
    def test_prediction_with_missing_feature(self, valid_eclo_features):
        """
        의도: 일부 피처 누락 시 적절한 에러 메시지 반환 검증
        """
        # Arrange - 피처 하나 제거
        incomplete_features = valid_eclo_features.copy()
        del incomplete_features["기상상태"]

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            predict_eclo_value(incomplete_features)

        assert "누락" in str(exc_info.value)

    @pytest.mark.integration
    def test_prediction_with_invalid_feature_value(self, valid_eclo_features):
        """
        의도: 잘못된 피처 값 입력 시 적절한 에러 메시지 반환 검증
        """
        # Arrange - 잘못된 값 입력
        invalid_features = valid_eclo_features.copy()
        invalid_features["기상상태"] = "존재하지않는날씨"

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            predict_eclo_value(invalid_features)

        assert "유효한 값이 아닙니다" in str(exc_info.value)

    @pytest.mark.integration
    def test_batch_prediction_pipeline(self, valid_eclo_features):
        """
        의도: 여러 건 동시 예측 파이프라인 검증
        """
        # Arrange - 여러 건의 피처
        accidents = [
            valid_eclo_features,
            valid_eclo_features.copy(),  # 동일한 피처로 두 번째 건
        ]

        # Act
        results = predict_eclo_batch(accidents)

        # Assert
        assert len(results) == 2
        for result in results:
            assert result["eclo"] is not None
            assert result["interpretation"] is not None
            assert result["error"] is None

    @pytest.mark.integration
    def test_batch_prediction_with_partial_errors(self, valid_eclo_features):
        """
        의도: 배치 예측 중 일부 에러 발생 시 에러 건만 실패하고 나머지는 성공하는지 검증
        """
        # Arrange
        invalid_features = valid_eclo_features.copy()
        invalid_features["기상상태"] = "존재하지않는날씨"

        accidents = [
            valid_eclo_features,  # 성공
            invalid_features,     # 실패
        ]

        # Act
        results = predict_eclo_batch(accidents)

        # Assert
        assert len(results) == 2
        assert results[0]["eclo"] is not None
        assert results[0]["error"] is None
        assert results[1]["eclo"] is None
        assert results[1]["error"] is not None


class TestEcloToolIntegration:
    """
    ECLO 예측 도구 통합 테스트
    흐름: tools.predict_eclo → predictor 모듈
    """

    @pytest.mark.integration
    def test_predict_eclo_tool(self, valid_eclo_features, preprocessed_accident_df):
        """
        의도: predict_eclo 도구가 predictor 모듈을 통해 예측을 수행하는지 검증
        """
        # Arrange
        config = {"configurable": {"dataframe": preprocessed_accident_df, "current_dataset": "test"}}

        # Act
        result = predict_eclo.invoke({
            "weather": valid_eclo_features["기상상태"],
            "road_surface": valid_eclo_features["노면상태"],
            "road_type": valid_eclo_features["도로형태"],
            "accident_type": valid_eclo_features["사고유형"],
            "time_period": valid_eclo_features["시간대"],
            "district": valid_eclo_features["시군구"],
            "day_of_week": valid_eclo_features["요일"],
            "accident_hour": valid_eclo_features["사고시"],
            "accident_year": valid_eclo_features["사고연"],
            "accident_month": valid_eclo_features["사고월"],
            "accident_day": valid_eclo_features["사고일"],
        }, config=config)

        # Assert
        assert "ECLO 예측 결과" in result
        assert "예측된 ECLO 값" in result

    @pytest.mark.integration
    def test_predict_eclo_tool_with_invalid_input(self, valid_eclo_features, preprocessed_accident_df):
        """
        의도: 잘못된 입력으로 predict_eclo 도구 호출 시 에러 메시지 반환 검증
        """
        # Arrange
        config = {"configurable": {"dataframe": preprocessed_accident_df, "current_dataset": "test"}}

        # Act - 잘못된 기상상태 값
        result = predict_eclo.invoke({
            "weather": "존재하지않는날씨",
            "road_surface": valid_eclo_features["노면상태"],
            "road_type": valid_eclo_features["도로형태"],
            "accident_type": valid_eclo_features["사고유형"],
            "time_period": valid_eclo_features["시간대"],
            "district": valid_eclo_features["시군구"],
            "day_of_week": valid_eclo_features["요일"],
            "accident_hour": valid_eclo_features["사고시"],
            "accident_year": valid_eclo_features["사고연"],
            "accident_month": valid_eclo_features["사고월"],
            "accident_day": valid_eclo_features["사고일"],
        }, config=config)

        # Assert - 에러 메시지 포함
        assert "오류" in result or "유효" in result

    @pytest.mark.integration
    def test_predict_eclo_batch_tool(self, valid_eclo_features, preprocessed_accident_df):
        """
        의도: predict_eclo_batch 도구가 여러 건 예측을 수행하는지 검증
        """
        # Arrange
        config = {"configurable": {"dataframe": preprocessed_accident_df, "current_dataset": "test"}}

        # 영문 키로 변환
        accidents = [{
            "weather": valid_eclo_features["기상상태"],
            "road_surface": valid_eclo_features["노면상태"],
            "road_type": valid_eclo_features["도로형태"],
            "accident_type": valid_eclo_features["사고유형"],
            "time_period": valid_eclo_features["시간대"],
            "district": valid_eclo_features["시군구"],
            "day_of_week": valid_eclo_features["요일"],
            "accident_hour": 8,
            "accident_year": 2022,
            "accident_month": 1,
            "accident_day": 15,
        }, {
            "weather": valid_eclo_features["기상상태"],
            "road_surface": valid_eclo_features["노면상태"],
            "road_type": valid_eclo_features["도로형태"],
            "accident_type": valid_eclo_features["사고유형"],
            "time_period": valid_eclo_features["시간대"],
            "district": valid_eclo_features["시군구"],
            "day_of_week": valid_eclo_features["요일"],
            "accident_hour": 18,
            "accident_year": 2022,
            "accident_month": 6,
            "accident_day": 10,
        }]

        # Act
        result = tool_predict_batch.invoke({"accidents": accidents}, config=config)

        # Assert
        assert "배치 예측 결과" in result
        assert "2건" in result


class TestEcloInterpretationLevels:
    """ECLO 해석 수준 통합 테스트"""

    @pytest.mark.integration
    def test_interpretation_consistency(self):
        """
        의도: ECLO 값에 따른 해석이 일관되는지 검증
        """
        test_cases = [
            (0.05, "경미"),
            (0.3, "일반"),
            (0.7, "심각"),
            (1.5, "매우 심각"),
        ]

        for eclo_value, expected_interpretation in test_cases:
            result = interpret_eclo(eclo_value)
            assert result == expected_interpretation, f"ECLO {eclo_value}에 대해 {expected_interpretation}를 기대했지만 {result}를 받음"
