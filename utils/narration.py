"""
Natural language insight generation from analysis results.
"""
import pandas as pd
import numpy as np


def summarize_proximity_stats(stats_df: pd.DataFrame, threshold: str, facility_name: str) -> str:
    """
    Generate natural language summary of proximity analysis results.

    Parameters:
        stats_df (pd.DataFrame): Proximity statistics (output from compute_proximity_stats)
        threshold (str): Threshold column name (e.g., '0.5', '1.0')
        facility_name (str): Name of target facility type (e.g., 'CCTVs', 'Security Lights')

    Returns:
        str: Natural language summary paragraph
    """
    if stats_df.empty or threshold not in stats_df.columns:
        return f"{facility_name}에 대한 근접 통계를 생성할 수 없습니다."

    values = stats_df[threshold]
    mean_count = values.mean()
    median_count = values.median()
    max_count = values.max()

    # Classify density
    if mean_count > 5:
        density = "높은"
        density_description = "밀집된 분포를 보입니다"
    elif mean_count > 2:
        density = "중간 수준의"
        density_description = "적당한 분포를 보입니다"
    else:
        density = "낮은"
        density_description = "희소한 분포를 보입니다"

    summary = (
        f"평균적으로 각 기준점에서 {threshold}km 반경 내에 "
        f"{mean_count:.1f}개의 {facility_name}이(가) 있습니다. "
        f"이는 {density} 공간적 상관관계를 나타내며, {density_description}. "
        f"중앙값은 {median_count:.1f}개이고, 최대 {max_count:.0f}개까지 관측됩니다."
    )

    return summary


def generate_distribution_insight(df: pd.DataFrame, column: str) -> str:
    """
    Generate insight about column distribution characteristics.

    Parameters:
        df (pd.DataFrame): Input dataset
        column (str): Column name to analyze

    Returns:
        str: Distribution characteristic description
    """
    if column not in df.columns:
        return f"'{column}' 컬럼을 찾을 수 없습니다."

    data = df[column].dropna()

    if len(data) == 0:
        return f"'{column}' 컬럼에 유효한 데이터가 없습니다."

    # Check if numeric
    if not pd.api.types.is_numeric_dtype(data):
        # Categorical analysis
        value_counts = data.value_counts()
        top_category = value_counts.index[0]
        top_ratio = value_counts.iloc[0] / len(data) * 100
        unique_count = data.nunique()

        return (
            f"'{column}'은(는) {unique_count}개의 고유 값을 가진 범주형 데이터입니다. "
            f"가장 빈번한 값은 '{top_category}'로 전체의 {top_ratio:.1f}%를 차지합니다."
        )

    # Numeric analysis
    mean_val = data.mean()
    std_val = data.std()
    median_val = data.median()
    skewness = data.skew()

    # Detect skewness
    if skewness > 1:
        skew_desc = "오른쪽으로 치우친(양의 왜도)"
        skew_explanation = "대부분의 값이 낮은 쪽에 집중되어 있고 높은 값들이 꼬리를 형성합니다"
    elif skewness < -1:
        skew_desc = "왼쪽으로 치우친(음의 왜도)"
        skew_explanation = "대부분의 값이 높은 쪽에 집중되어 있고 낮은 값들이 꼬리를 형성합니다"
    elif abs(skewness) > 0.5:
        skew_desc = "약간 비대칭인"
        skew_explanation = "중심에서 약간 벗어난 분포를 보입니다"
    else:
        skew_desc = "대칭적인"
        skew_explanation = "평균을 중심으로 균형 잡힌 분포를 보입니다"

    # Detect outliers (using IQR method)
    q1, q3 = data.quantile([0.25, 0.75])
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outlier_count = ((data < lower_bound) | (data > upper_bound)).sum()
    outlier_ratio = outlier_count / len(data) * 100

    insight = (
        f"'{column}'은(는) {skew_desc} 분포를 보입니다. "
        f"평균은 {mean_val:.2f}, 중앙값은 {median_val:.2f}이며, "
        f"표준편차는 {std_val:.2f}입니다. "
        f"{skew_explanation}."
    )

    if outlier_ratio > 1:
        insight += f" 데이터의 {outlier_ratio:.1f}%({outlier_count}개)가 이상치로 감지됩니다."

    return insight


def compare_distributions(
    df1: pd.DataFrame,
    col1: str,
    df2: pd.DataFrame,
    col2: str
) -> str:
    """
    Generate comparative insight between two column distributions.

    Parameters:
        df1, df2 (pd.DataFrame): Datasets to compare
        col1, col2 (str): Column names to compare

    Returns:
        str: Comparative analysis text
    """
    if col1 not in df1.columns:
        return f"첫 번째 데이터셋에서 '{col1}' 컬럼을 찾을 수 없습니다."
    if col2 not in df2.columns:
        return f"두 번째 데이터셋에서 '{col2}' 컬럼을 찾을 수 없습니다."

    data1 = df1[col1].dropna()
    data2 = df2[col2].dropna()

    if len(data1) == 0 or len(data2) == 0:
        return "비교할 유효한 데이터가 없습니다."

    # Check if both are numeric
    if not (pd.api.types.is_numeric_dtype(data1) and pd.api.types.is_numeric_dtype(data2)):
        return "두 컬럼 모두 숫자형이어야 분포 비교가 가능합니다."

    # Calculate statistics
    mean1, mean2 = data1.mean(), data2.mean()
    std1, std2 = data1.std(), data2.std()

    # Calculate differences
    mean_diff = abs(mean1 - mean2)
    mean_diff_pct = (mean_diff / max(abs(mean1), abs(mean2), 1e-10)) * 100

    std_diff = abs(std1 - std2)
    std_diff_pct = (std_diff / max(std1, std2, 1e-10)) * 100

    # Determine similarity
    if mean_diff_pct < 5 and std_diff_pct < 10:
        similarity = "매우 유사합니다"
        interpretation = "두 데이터셋은 동일한 모집단에서 추출된 것으로 보입니다"
    elif mean_diff_pct < 10 and std_diff_pct < 20:
        similarity = "유사합니다"
        interpretation = "두 데이터셋은 비슷한 특성을 가지고 있습니다"
    elif mean_diff_pct < 20:
        similarity = "약간 다릅니다"
        interpretation = "두 데이터셋 간에 일부 차이가 관측됩니다"
    else:
        similarity = "상당히 다릅니다"
        interpretation = "두 데이터셋은 다른 특성을 보입니다"

    comparison = (
        f"두 분포는 {similarity}. "
        f"평균 차이는 {mean_diff:.2f} ({mean_diff_pct:.1f}%)이며, "
        f"표준편차 차이는 {std_diff:.2f} ({std_diff_pct:.1f}%)입니다. "
        f"{interpretation}."
    )

    # Add specific statistics
    comparison += (
        f"\n\n**세부 통계:**\n"
        f"- 첫 번째 데이터셋: 평균={mean1:.2f}, 표준편차={std1:.2f}, N={len(data1):,}\n"
        f"- 두 번째 데이터셋: 평균={mean2:.2f}, 표준편차={std2:.2f}, N={len(data2):,}"
    )

    return comparison
