"""
Data preprocessing utilities for accident datetime processing.

v1.3: 사고일시 전처리 모듈 - ML 모델 입력 피처 자동 생성
"""
import pandas as pd
import streamlit as st


def hour_to_period(hour: int) -> str:
    """
    시간 값을 시간대 범주로 분류합니다.

    분류 기준 (data-model.md 참조):
    - 출근시간대: 7 ≤ hour ≤ 9
    - 퇴근시간대: 17 ≤ hour ≤ 19
    - 심야: hour ≥ 22 또는 hour ≤ 5
    - 일반시간대: 그 외

    Parameters:
        hour (int): 시간 값 (0-23)

    Returns:
        str: 시간대 분류 ("출근시간대", "퇴근시간대", "심야", "일반시간대")
    """
    if 7 <= hour <= 9:
        return "출근시간대"
    elif 17 <= hour <= 19:
        return "퇴근시간대"
    elif hour >= 22 or hour <= 5:
        return "심야"
    else:
        return "일반시간대"


def preprocess_accident_datetime(df: pd.DataFrame) -> pd.DataFrame:
    """
    사고일시 컬럼을 파싱하여 ML 모델 입력 피처를 생성합니다.

    FR-001: 사고연, 사고월, 사고일, 사고시 4개 정수 컬럼 생성
    FR-002: 시간대 범주형 컬럼 생성
    FR-003: 사고일시 컬럼 없으면 원본 그대로 반환
    FR-009: 원본 데이터 변경 금지 - DataFrame.copy() 사용
    FR-010: 파싱 실패 행 제외 및 경고 메시지

    Parameters:
        df (pd.DataFrame): 입력 DataFrame (사고일시 컬럼 포함 가능)

    Returns:
        pd.DataFrame: 파생 피처가 추가된 DataFrame (또는 원본)
    """
    # FR-003: 사고일시 컬럼 존재 확인
    if '사고일시' not in df.columns:
        return df

    # FR-009: 원본 데이터 변경 금지 - 복사본 생성
    result = df.copy()

    # pd.to_datetime() 파싱 (errors='coerce'로 실패 시 NaT 반환)
    result['사고일시_parsed'] = pd.to_datetime(
        result['사고일시'],
        format='%Y-%m-%d %H',
        errors='coerce'
    )

    # FR-010: 파싱 실패 행 확인 및 경고
    invalid_count = result['사고일시_parsed'].isna().sum()
    original_count = len(result)

    if invalid_count > 0:
        # Streamlit 환경에서만 경고 표시
        try:
            st.warning(
                f"⚠️ 사고일시 파싱 실패: {invalid_count}건 제외됨 "
                f"(전체 {original_count}건 중 {invalid_count}건)"
            )
        except Exception:
            # Streamlit 환경이 아닌 경우 (테스트 등) 무시
            pass

        # 파싱 실패 행 제외
        result = result.dropna(subset=['사고일시_parsed']).reset_index(drop=True)

    # FR-001: 사고연, 사고월, 사고일, 사고시 컬럼 추출
    result['사고연'] = result['사고일시_parsed'].dt.year.astype(int)
    result['사고월'] = result['사고일시_parsed'].dt.month.astype(int)
    result['사고일'] = result['사고일시_parsed'].dt.day.astype(int)
    result['사고시'] = result['사고일시_parsed'].dt.hour.astype(int)

    # FR-002: 시간대 컬럼 생성
    result['시간대'] = result['사고시'].apply(hour_to_period)

    # 임시 파싱 컬럼 제거
    result = result.drop(columns=['사고일시_parsed'])

    return result
