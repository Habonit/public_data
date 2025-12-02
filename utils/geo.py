"""
Geospatial utilities for coordinate detection and distance calculations.
"""
from math import radians, cos, sin, asin, sqrt
import pandas as pd


def detect_lat_lng_columns(df: pd.DataFrame) -> tuple[str | None, str | None]:
    """
    Auto-detect latitude and longitude column names.

    Parameters:
        df (pd.DataFrame): Dataset with potential coordinate columns

    Returns:
        tuple[str | None, str | None]: (latitude_column_name, longitude_column_name)
        Returns (None, None) if coordinates not found
    """
    # Common patterns for latitude and longitude column names
    lat_candidates = ['lat', 'latitude', '위도', 'y좌표', 'y', 'Lat', 'Latitude']
    lng_candidates = ['lng', 'lon', 'longitude', '경도', 'x좌표', 'x', 'Lng', 'Lon', 'Longitude']

    lat_col = None
    lng_col = None

    # Check each column name against candidates (case-insensitive for English)
    for col in df.columns:
        # Check latitude
        if not lat_col:
            for candidate in lat_candidates:
                if col == candidate or col.lower() == candidate.lower():
                    lat_col = col
                    break

        # Check longitude
        if not lng_col:
            for candidate in lng_candidates:
                if col == candidate or col.lower() == candidate.lower():
                    lng_col = col
                    break

        # Stop if both found
        if lat_col and lng_col:
            break

    # Only return if both coordinates found
    if lat_col and lng_col:
        return (lat_col, lng_col)
    else:
        return (None, None)


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate great-circle distance between two points using Haversine formula.

    The Haversine formula calculates the shortest distance over the earth's surface,
    giving an "as-the-crow-flies" distance between two points (ignoring terrain).

    Mathematical basis:
    - The formula uses spherical trigonometry
    - a = sin²(Δlat/2) + cos(lat1) × cos(lat2) × sin²(Δlon/2)
    - c = 2 × arcsin(√a)
    - distance = R × c, where R is Earth's radius (6371 km)

    Parameters:
        lat1, lon1 (float): First point latitude/longitude in decimal degrees
        lat2, lon2 (float): Second point latitude/longitude in decimal degrees

    Returns:
        float: Distance in kilometers

    Example:
        >>> haversine_distance(35.8714, 128.6014, 35.8800, 128.6100)
        1.23  # approximately 1.23 km
    """
    # Step 1: Convert decimal degrees to radians (required for trigonometric functions)
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Step 2: Calculate differences in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Step 3: Apply Haversine formula
    # 'a' represents the square of half the chord length between the points
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

    # Step 4: Calculate central angle 'c' using inverse haversine
    c = 2 * asin(sqrt(a))

    # Step 5: Calculate distance using Earth's mean radius (6371 km)
    # Note: This assumes Earth is a perfect sphere (good approximation for most purposes)
    km = 6371 * c
    return km


def validate_coordinates(lat: float, lng: float, bounds: dict | None = None) -> bool:
    """
    Validate if coordinates are within expected bounds (default: Daegu).

    Parameters:
        lat (float): Latitude in decimal degrees
        lng (float): Longitude in decimal degrees
        bounds (dict | None): Optional bounds dict with keys 'lat_min', 'lat_max', 'lng_min', 'lng_max'
            Default: Daegu bounds (35.7-36.1 N, 128.4-128.8 E)

    Returns:
        bool: True if coordinates valid and within bounds
    """
    # Reject invalid coordinates (0, 0)
    if lat == 0.0 and lng == 0.0:
        return False

    # Check basic latitude/longitude validity
    if not (-90 <= lat <= 90):
        return False
    if not (-180 <= lng <= 180):
        return False

    # Default Daegu bounds
    if bounds is None:
        bounds = {
            'lat_min': 35.7,
            'lat_max': 36.1,
            'lng_min': 128.4,
            'lng_max': 128.8
        }

    # Check bounds
    if not (bounds['lat_min'] <= lat <= bounds['lat_max']):
        return False
    if not (bounds['lng_min'] <= lng <= bounds['lng_max']):
        return False

    return True


def compute_proximity_stats(
    df_base: pd.DataFrame,
    base_lat_col: str,
    base_lng_col: str,
    df_target: pd.DataFrame,
    target_lat_col: str,
    target_lng_col: str,
    thresholds: list[float] | None = None
) -> pd.DataFrame:
    """
    Calculate proximity statistics between two datasets.

    This function implements a spatial proximity analysis that counts how many
    target points are within specified distance thresholds of each base point.

    Algorithm Overview:
    1. For each point in the base dataset
    2. Calculate distance to every point in the target dataset (using Haversine)
    3. Count how many target points fall within each threshold distance
    4. Return summary statistics

    Complexity: O(n × m) where n = base points, m = target points
    Performance optimization: Samples to 5000 points if dataset is larger

    Use Cases:
    - How many CCTVs are within 500m of each accident location?
    - What is the average number of security lights near parking lots?
    - Identify areas with high/low facility density

    Parameters:
        df_base (pd.DataFrame): Base dataset (e.g., train data)
        base_lat_col, base_lng_col (str): Coordinate column names in df_base
        df_target (pd.DataFrame): Target dataset (e.g., CCTV data)
        target_lat_col, target_lng_col (str): Coordinate column names in df_target
        thresholds (list[float] | None): Distance thresholds in kilometers (default: [0.5, 1.0, 2.0])

    Returns:
        pd.DataFrame: Proximity counts
            - Rows: Each base point (sampled to max 5000 if needed)
            - Columns: One column per threshold with count of target points within that distance

    Example:
        >>> proximity_df = compute_proximity_stats(
        ...     train_df, 'lat', 'lng',
        ...     cctv_df, 'latitude', 'longitude',
        ...     thresholds=[0.5, 1.0, 2.0]
        ... )
        >>> proximity_df['0.5'].mean()  # Average CCTVs within 500m
        3.2
    """
    # Default thresholds: 500m, 1km, 2km - common distances for urban analysis
    if thresholds is None:
        thresholds = [0.5, 1.0, 2.0]

    # Performance optimization: sample to 5000 rows if larger
    # This keeps computation time reasonable (< 10 seconds typically)
    if len(df_base) > 5000:
        df_base = df_base.sample(5000, random_state=42)

    # Initialize results dictionary with string keys for DataFrame columns
    results = {str(t): [] for t in thresholds}

    # Data cleaning: remove rows with missing coordinates
    # (cannot calculate distance without valid coordinates)
    df_base_clean = df_base.dropna(subset=[base_lat_col, base_lng_col])
    df_target_clean = df_target.dropna(subset=[target_lat_col, target_lng_col])

    # Main computation loop: for each base point, count nearby target points
    for _, base_row in df_base_clean.iterrows():
        base_lat = base_row[base_lat_col]
        base_lng = base_row[base_lng_col]

        # Initialize counts for each threshold
        counts = {t: 0 for t in thresholds}

        # Calculate distance to each target point
        for _, target_row in df_target_clean.iterrows():
            target_lat = target_row[target_lat_col]
            target_lng = target_row[target_lng_col]

            # Calculate Haversine distance (great-circle distance)
            dist = haversine_distance(base_lat, base_lng, target_lat, target_lng)

            # Increment counts for all thresholds that include this distance
            # (if within 0.5km, it's also within 1km and 2km)
            for t in thresholds:
                if dist <= t:
                    counts[t] += 1

        # Add counts to results
        for t in thresholds:
            results[str(t)].append(counts[t])

    # Convert to DataFrame for easy analysis
    return pd.DataFrame(results)
