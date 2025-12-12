"""
Tests for ECLO prediction module.

대상: utils/predictor.py
의도: LightGBM 기반 ECLO 예측 기능 검증
TDD approach: Tests written before implementation per Constitution XII.
"""
import pytest
from utils.predictor import (
    load_model,
    load_encoders,
    load_feature_config,
    get_valid_values,
    encode_features,
    predict_eclo_value,
    interpret_eclo,
    interpret_eclo_detail,
    predict_eclo_batch,
)


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def valid_features():
    """유효한 전체 피처 세트."""
    # 실제 인코더에 등록된 값을 사용해야 함
    encoders = load_encoders()

    return {
        "기상상태": list(encoders["기상상태"].classes_)[0],
        "노면상태": list(encoders["노면상태"].classes_)[0],
        "도로형태": list(encoders["도로형태"].classes_)[0],
        "사고유형": list(encoders["사고유형"].classes_)[0],
        "시간대": list(encoders["시간대"].classes_)[0],
        "시군구": list(encoders["시군구"].classes_)[0],
        "요일": list(encoders["요일"].classes_)[0],
        "사고시": 8,
        "사고연": 2022,
        "사고월": 1,
        "사고일": 1,
    }


@pytest.fixture
def multiple_valid_features(valid_features):
    """여러 개의 유효한 피처 세트."""
    encoders = load_encoders()

    return [
        valid_features,
        {
            "기상상태": list(encoders["기상상태"].classes_)[0],
            "노면상태": list(encoders["노면상태"].classes_)[0],
            "도로형태": list(encoders["도로형태"].classes_)[0],
            "사고유형": list(encoders["사고유형"].classes_)[0],
            "시간대": list(encoders["시간대"].classes_)[0],
            "시군구": list(encoders["시군구"].classes_)[0],
            "요일": list(encoders["요일"].classes_)[0],
            "사고시": 18,
            "사고연": 2022,
            "사고월": 6,
            "사고일": 15,
        }
    ]


# ============================================================================
# Model Loading Tests
# ============================================================================

class TestLoadModel:
    """
    대상: utils/predictor.py - load_model()
    의도: LightGBM 모델 로드 기능 검증
    """

    def test_load_model_success(self):
        """
        대상: utils/predictor.py:29 - load_model()
        의도: 모델 파일 정상 로드 검증
        """
        model = load_model()
        assert model is not None
        assert hasattr(model, 'predict')

    def test_load_model_cached(self):
        """
        대상: utils/predictor.py:29 - load_model()
        의도: 모델 캐싱 동작 검증 (동일 객체 반환)
        """
        model1 = load_model()
        model2 = load_model()
        assert model1 is model2


class TestLoadEncoders:
    """
    대상: utils/predictor.py - load_encoders()
    의도: 라벨 인코더 로드 기능 검증
    """

    def test_load_encoders_success(self):
        """
        대상: utils/predictor.py:40 - load_encoders()
        의도: 인코더 파일 정상 로드 검증
        """
        encoders = load_encoders()
        assert encoders is not None
        assert isinstance(encoders, dict)

    def test_encoders_have_expected_keys(self):
        """
        대상: utils/predictor.py:40 - load_encoders()
        의도: 필수 범주형 피처 인코더 존재 검증
        """
        encoders = load_encoders()
        expected_keys = ["기상상태", "노면상태", "도로형태", "사고유형", "시간대", "시군구", "요일"]
        for key in expected_keys:
            assert key in encoders, f"'{key}' 인코더가 없습니다"


class TestLoadFeatureConfig:
    """
    대상: utils/predictor.py - load_feature_config()
    의도: 피처 설정 로드 기능 검증
    """

    def test_load_feature_config_success(self):
        """
        대상: utils/predictor.py:51 - load_feature_config()
        의도: 설정 파일 정상 로드 검증
        """
        config = load_feature_config()
        assert config is not None
        assert isinstance(config, dict)

    def test_config_has_required_keys(self):
        """
        대상: utils/predictor.py:51 - load_feature_config()
        의도: 필수 설정 키 존재 검증
        """
        config = load_feature_config()
        assert "feature_cols" in config
        assert "cat_cols" in config
        assert "num_cols" in config


# ============================================================================
# Feature Validation Tests
# ============================================================================

class TestGetValidValues:
    """
    대상: utils/predictor.py - get_valid_values()
    의도: 피처별 유효값 목록 반환 기능 검증
    """

    def test_get_valid_values_weather(self):
        """
        대상: utils/predictor.py:62 - get_valid_values()
        의도: 기상상태 유효값 목록 반환 검증
        """
        values = get_valid_values("기상상태")
        assert isinstance(values, list)
        assert len(values) > 0

    def test_get_valid_values_nonexistent_feature(self):
        """
        대상: utils/predictor.py:62 - get_valid_values()
        의도: 존재하지 않는 피처 빈 리스트 반환 검증
        """
        values = get_valid_values("존재하지않는피처")
        assert values == []


class TestEncodeFeatures:
    """
    대상: utils/predictor.py - encode_features()
    의도: 피처 인코딩 기능 검증
    """

    def test_encode_features_success(self, valid_features):
        """
        대상: utils/predictor.py:70 - encode_features()
        의도: 유효한 피처 인코딩 성공 검증
        """
        encoded = encode_features(valid_features)
        assert encoded is not None
        assert len(encoded) == 1  # 단일 행

    def test_encode_features_missing_feature_raises_error(self, valid_features):
        """
        대상: utils/predictor.py:70 - encode_features()
        의도: 필수 피처 누락 시 ValueError 발생 검증
        """
        incomplete_features = valid_features.copy()
        del incomplete_features["기상상태"]

        with pytest.raises(ValueError) as exc_info:
            encode_features(incomplete_features)
        assert "누락" in str(exc_info.value)

    def test_encode_features_invalid_value_raises_error(self, valid_features):
        """
        대상: utils/predictor.py:70 - encode_features()
        의도: 유효하지 않은 피처 값 ValueError 발생 검증
        """
        invalid_features = valid_features.copy()
        invalid_features["기상상태"] = "존재하지않는날씨"

        with pytest.raises(ValueError) as exc_info:
            encode_features(invalid_features)
        assert "유효한 값이 아닙니다" in str(exc_info.value)


# ============================================================================
# Prediction Tests
# ============================================================================

class TestPredictEcloValue:
    """
    대상: utils/predictor.py - predict_eclo_value()
    의도: ECLO 값 예측 기능 검증
    """

    def test_predict_eclo_returns_float(self, valid_features):
        """
        대상: utils/predictor.py:127 - predict_eclo_value()
        의도: ECLO 예측 결과가 float 타입인지 검증
        """
        result = predict_eclo_value(valid_features)
        assert isinstance(result, float)

    def test_predict_eclo_value_range(self, valid_features):
        """
        대상: utils/predictor.py:127 - predict_eclo_value()
        의도: ECLO 예측 값이 합리적 범위 내인지 검증
        """
        result = predict_eclo_value(valid_features)
        # ECLO 값은 일반적으로 0 이상
        assert result >= 0


# ============================================================================
# Interpretation Tests
# ============================================================================

class TestInterpretEclo:
    """
    대상: utils/predictor.py - interpret_eclo()
    의도: ECLO 값 해석 기능 검증
    """

    def test_interpret_eclo_minor(self):
        """
        대상: utils/predictor.py:162 - interpret_eclo()
        의도: 0.1 미만 → 경미 판정 검증
        """
        result = interpret_eclo(0.05)
        assert result == "경미"

    def test_interpret_eclo_normal(self):
        """
        대상: utils/predictor.py:162 - interpret_eclo()
        의도: 0.1~0.5 → 일반 판정 검증
        """
        result = interpret_eclo(0.3)
        assert result == "일반"

    def test_interpret_eclo_severe(self):
        """
        대상: utils/predictor.py:162 - interpret_eclo()
        의도: 0.5~1.0 → 심각 판정 검증
        """
        result = interpret_eclo(0.7)
        assert result == "심각"

    def test_interpret_eclo_very_severe(self):
        """
        대상: utils/predictor.py:162 - interpret_eclo()
        의도: 1.0 이상 → 매우 심각 판정 검증
        """
        result = interpret_eclo(1.5)
        assert result == "매우 심각"


class TestInterpretEcloDetail:
    """
    대상: utils/predictor.py - interpret_eclo_detail()
    의도: ECLO 값 상세 해석 기능 검증
    """

    def test_interpret_detail_minor(self):
        """
        대상: utils/predictor.py:182 - interpret_eclo_detail()
        의도: 경미 수준 상세 해석 검증
        """
        result = interpret_eclo_detail(0.05)
        assert "경미" in result
        assert "부상 가능성이 낮" in result

    def test_interpret_detail_very_severe(self):
        """
        대상: utils/predictor.py:182 - interpret_eclo_detail()
        의도: 매우 심각 수준 상세 해석 검증
        """
        result = interpret_eclo_detail(1.5)
        assert "매우 심각" in result
        assert "치명적" in result


# ============================================================================
# Batch Prediction Tests
# ============================================================================

class TestPredictEcloBatch:
    """
    대상: utils/predictor.py - predict_eclo_batch()
    의도: 배치 ECLO 예측 기능 검증
    """

    def test_batch_predict_success(self, multiple_valid_features):
        """
        대상: utils/predictor.py:214 - predict_eclo_batch()
        의도: 다건 예측 성공 검증
        """
        results = predict_eclo_batch(multiple_valid_features)
        assert len(results) == 2

        for result in results:
            assert "index" in result
            assert "features" in result
            assert "eclo" in result
            assert "interpretation" in result
            assert "error" in result

    def test_batch_predict_with_error(self, valid_features):
        """
        대상: utils/predictor.py:214 - predict_eclo_batch()
        의도: 일부 에러 발생 시 결과에 에러 포함 검증
        """
        invalid_features = valid_features.copy()
        invalid_features["기상상태"] = "존재하지않는날씨"

        results = predict_eclo_batch([valid_features, invalid_features])

        assert len(results) == 2
        # 첫 번째는 성공
        assert results[0]["eclo"] is not None
        assert results[0]["error"] is None
        # 두 번째는 에러
        assert results[1]["eclo"] is None
        assert results[1]["error"] is not None

    def test_batch_predict_empty_list(self):
        """
        대상: utils/predictor.py:214 - predict_eclo_batch()
        의도: 빈 리스트 입력 시 빈 결과 반환 검증
        """
        results = predict_eclo_batch([])
        assert results == []

    def test_batch_predict_result_structure(self, valid_features):
        """
        대상: utils/predictor.py:214 - predict_eclo_batch()
        의도: 결과 구조 검증
        """
        results = predict_eclo_batch([valid_features])

        assert len(results) == 1
        result = results[0]

        assert result["index"] == 1
        assert result["features"] == valid_features
        assert isinstance(result["eclo"], float)
        assert result["interpretation"] in ["경미", "일반", "심각", "매우 심각"]
        assert result["error"] is None
