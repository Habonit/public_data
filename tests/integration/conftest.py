"""
Pytest configuration and fixtures for integration tests.
"""
import os
import io
import pytest
import pandas as pd
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()


@pytest.fixture(scope="module")
def sample_accident_csv_content():
    """사고 데이터 CSV 콘텐츠 (UTF-8)."""
    return """사고일시,기상상태,노면상태,도로형태,사고유형,시군구
2022-01-15 08,맑음,건조,교차로 - 교차로안,차대차,대구광역시 수성구 상동
2022-03-20 14,흐림,젖음/습기,단일로 - 기타,차대사람,대구광역시 중구 동성로1가
2022-06-10 23,비,젖음/습기,교차로 - 교차로부근,차대차,대구광역시 달서구 월성동
2022-09-05 03,맑음,건조,단일로 - 기타,차량단독,대구광역시 북구 대현동
2022-12-25 18,눈,적설,교차로 - 교차로안,차대차,대구광역시 동구 신천동"""


@pytest.fixture(scope="module")
def sample_accident_csv_bytes(sample_accident_csv_content):
    """사고 데이터 CSV 바이트 객체."""
    return io.BytesIO(sample_accident_csv_content.encode('utf-8'))


@pytest.fixture(scope="module")
def sample_accident_df():
    """전처리 전 사고 데이터 DataFrame."""
    return pd.DataFrame({
        '사고일시': [
            '2022-01-15 08',
            '2022-03-20 14',
            '2022-06-10 23',
            '2022-09-05 03',
            '2022-12-25 18'
        ],
        '기상상태': ['맑음', '흐림', '비', '맑음', '눈'],
        '노면상태': ['건조', '젖음/습기', '젖음/습기', '건조', '적설'],
        '도로형태': [
            '교차로 - 교차로안',
            '단일로 - 기타',
            '교차로 - 교차로부근',
            '단일로 - 기타',
            '교차로 - 교차로안'
        ],
        '사고유형': ['차대차', '차대사람', '차대차', '차량단독', '차대차'],
        '시군구': [
            '대구광역시 수성구 상동',
            '대구광역시 중구 동성로1가',
            '대구광역시 달서구 월성동',
            '대구광역시 북구 대현동',
            '대구광역시 동구 신천동'
        ]
    })


@pytest.fixture(scope="module")
def preprocessed_accident_df(sample_accident_df):
    """전처리 완료된 사고 데이터 DataFrame."""
    from utils.preprocessing import preprocess_accident_datetime
    return preprocess_accident_datetime(sample_accident_df)


@pytest.fixture(scope="module")
def geo_df():
    """위경도 데이터가 포함된 DataFrame."""
    return pd.DataFrame({
        '위도': [35.8714, 35.8682, 35.8701, 35.8650, 35.8730],
        '경도': [128.6014, 128.5961, 128.5988, 128.6100, 128.5900],
        '시설명': ['CCTV_A', 'CCTV_B', 'CCTV_C', 'CCTV_D', 'CCTV_E'],
        '유형': ['고정', '고정', '회전', '고정', '회전']
    })


@pytest.fixture(scope="session")
def api_key():
    """ANTHROPIC_API_KEY 환경 변수에서 API Key 로드."""
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        pytest.skip("ANTHROPIC_API_KEY 환경 변수가 설정되지 않음")
    return key


@pytest.fixture(scope="module")
def valid_eclo_features():
    """유효한 ECLO 예측 피처."""
    from utils.predictor import load_encoders
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
        "사고일": 15,
    }
