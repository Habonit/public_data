# Module Interfaces Contract

**Feature**: 001-daegu-data-viz
**Date**: 2025-11-21
**Purpose**: Define function signatures and interfaces for all utility modules

## Overview

This document serves as the "contract" specification for the Streamlit application's
utility modules. Since there is no REST API or backend service, contracts are defined
as Python function signatures with type hints, docstrings, and expected behaviors.

---

## utils/loader.py

### Purpose
Handle all CSV data loading with encoding fallback and caching.

### Functions

#### `read_csv_safe(file_path: str) -> pd.DataFrame`

**Description**: Read CSV file with automatic encoding detection (UTF-8 → UTF-8-SIG → CP949).

**Parameters**:
- `file_path` (str): Absolute path to CSV file

**Returns**:
- `pd.DataFrame`: Loaded dataset

**Raises**:
- `FileNotFoundError`: If file_path does not exist
- `ValueError`: If file cannot be decoded with any supported encoding

**Example**:
```python
df = read_csv_safe('/data/대구 CCTV 정보.csv')
```

**Contract**:
- MUST attempt UTF-8 first
- MUST fall back to UTF-8-SIG, then CP949
- MUST raise ValueError with clear message if all encodings fail
- MUST preserve all columns and data types from CSV

---

#### `load_dataset(dataset_name: str) -> pd.DataFrame`

**Description**: Load predefined dataset by name with caching.

**Parameters**:
- `dataset_name` (str): One of ['cctv', 'lights', 'zones', 'parking', 'accident', 'train', 'test']

**Returns**:
- `pd.DataFrame`: Cached dataset

**Raises**:
- `ValueError`: If dataset_name not recognized
- `FileNotFoundError`: If corresponding CSV file missing

**Decorator**: `@st.cache_data`

**Example**:
```python
cctv_df = load_dataset('cctv')
train_df = load_dataset('train')
```

**Contract**:
- MUST use @st.cache_data decorator for caching
- MUST map dataset_name to correct file path
- MUST call read_csv_safe internally
- MUST return same DataFrame instance on repeated calls (via cache)

---

#### `get_dataset_info(df: pd.DataFrame) -> dict`

**Description**: Generate comprehensive dataset summary statistics.

**Parameters**:
- `df` (pd.DataFrame): Input dataset

**Returns**:
- `dict`: Summary statistics
  ```python
  {
      'row_count': int,
      'column_count': int,
      'dtypes': dict,           # {col_name: dtype_str}
      'missing_ratios': dict,   # {col_name: float 0-1}
      'numeric_summary': pd.DataFrame,  # describe() for numeric cols
      'categorical_summary': dict       # {col_name: value_counts dict}
  }
  ```

**Example**:
```python
info = get_dataset_info(cctv_df)
print(f"Rows: {info['row_count']}, Cols: {info['column_count']}")
```

**Contract**:
- MUST include all seven summary keys
- MUST handle empty DataFrames gracefully
- MUST separate numeric and categorical column analysis
- MUST calculate missing ratios as proportion (0.0 to 1.0)

---

## utils/geo.py

### Purpose
Geospatial utilities for coordinate detection and distance calculations.

### Functions

#### `detect_lat_lng_columns(df: pd.DataFrame) -> tuple[str | None, str | None]`

**Description**: Auto-detect latitude and longitude column names.

**Parameters**:
- `df` (pd.DataFrame): Dataset with potential coordinate columns

**Returns**:
- `tuple[str | None, str | None]`: (latitude_column_name, longitude_column_name)
  Returns (None, None) if coordinates not found

**Example**:
```python
lat_col, lng_col = detect_lat_lng_columns(cctv_df)
if lat_col and lng_col:
    print(f"Found coordinates: {lat_col}, {lng_col}")
```

**Contract**:
- MUST check these patterns (case-insensitive):
  - Latitude: ['lat', 'latitude', '위도', 'y좌표', 'y', 'Lat']
  - Longitude: ['lng', 'lon', 'longitude', '경도', 'x좌표', 'x', 'Lng', 'Lon']
- MUST return None for both if either coordinate not found
- MUST return actual column names (preserving original case)
- MUST handle DataFrames with no matching columns gracefully

---

#### `haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float`

**Description**: Calculate great-circle distance between two points using Haversine formula.

**Parameters**:
- `lat1`, `lon1` (float): First point latitude/longitude in decimal degrees
- `lat2`, `lon2` (float): Second point latitude/longitude in decimal degrees

**Returns**:
- `float`: Distance in kilometers

**Example**:
```python
dist = haversine_distance(35.8714, 128.6014, 35.8800, 128.6100)
print(f"Distance: {dist:.2f} km")
```

**Contract**:
- MUST use Earth radius = 6371 km
- MUST accept decimal degrees (not radians)
- MUST return distance in kilometers
- MUST handle antipodal points correctly
- SHOULD return 0.0 for identical coordinates

---

#### `compute_proximity_stats(df_base: pd.DataFrame, base_lat_col: str, base_lng_col: str, df_target: pd.DataFrame, target_lat_col: str, target_lng_col: str, thresholds: list[float] = [0.5, 1.0, 2.0]) -> pd.DataFrame`

**Description**: Calculate proximity statistics between two datasets.

**Parameters**:
- `df_base` (pd.DataFrame): Base dataset (e.g., train data)
- `base_lat_col`, `base_lng_col` (str): Coordinate column names in df_base
- `df_target` (pd.DataFrame): Target dataset (e.g., CCTV data)
- `target_lat_col`, `target_lng_col` (str): Coordinate column names in df_target
- `thresholds` (list[float]): Distance thresholds in kilometers (default: [0.5, 1.0, 2.0])

**Returns**:
- `pd.DataFrame`: Proximity counts
  - Rows: Each base point (sampled to max 5000 if needed)
  - Columns: One column per threshold with count of target points within that distance

**Example**:
```python
proximity_df = compute_proximity_stats(
    train_df, 'lat', 'lng',
    cctv_df, 'latitude', 'longitude',
    thresholds=[0.5, 1.0, 2.0]
)
print(proximity_df['0.5'].mean())  # Average CCTVs within 500m
```

**Contract**:
- MUST sample df_base to 5000 rows if larger (for performance)
- MUST use haversine_distance for all calculations
- MUST create one column per threshold named as string (e.g., '0.5', '1.0')
- MUST return DataFrame with same row count as (sampled) df_base
- MUST handle edge cases: empty datasets, no coordinates, etc.
- SHOULD complete calculation within 10 seconds for 5000 x 5000 point pairs

---

#### `validate_coordinates(lat: float, lng: float, bounds: dict | None = None) -> bool`

**Description**: Validate if coordinates are within expected bounds (default: Daegu).

**Parameters**:
- `lat` (float): Latitude in decimal degrees
- `lng` (float): Longitude in decimal degrees
- `bounds` (dict | None): Optional bounds dict with keys 'lat_min', 'lat_max', 'lng_min', 'lng_max'
  Default: Daegu bounds (35.7-36.1 N, 128.4-128.8 E)

**Returns**:
- `bool`: True if coordinates valid and within bounds

**Example**:
```python
is_valid = validate_coordinates(35.8714, 128.6014)  # True for Daegu
is_valid = validate_coordinates(0.0, 0.0)  # False (invalid)
```

**Contract**:
- MUST reject (0.0, 0.0) as invalid
- MUST use Daegu default bounds if none provided
- MUST validate latitude in range [-90, 90]
- MUST validate longitude in range [-180, 180]
- MUST check bounds if provided

---

## utils/visualizer.py

### Purpose
Generate Plotly charts and Folium maps for data visualization.

### Functions

#### `plot_numeric_distribution(df: pd.DataFrame, column: str, title: str | None = None) -> go.Figure`

**Description**: Create histogram for numeric column distribution.

**Parameters**:
- `df` (pd.DataFrame): Input dataset
- `column` (str): Numeric column name
- `title` (str | None): Optional chart title (default: auto-generated)

**Returns**:
- `plotly.graph_objects.Figure`: Interactive histogram

**Example**:
```python
fig = plot_numeric_distribution(cctv_df, 'installation_year', 'CCTV Installation Timeline')
st.plotly_chart(fig, use_container_width=True)
```

**Contract**:
- MUST use Plotly Express or Graph Objects
- MUST include hover data showing count and bin range
- MUST auto-generate title if not provided
- MUST handle missing values (exclude from bins, show count in title)
- SHOULD use appropriate bin count (Sturges or Freedman-Diaconis rule)

---

#### `plot_categorical_distribution(df: pd.DataFrame, column: str, title: str | None = None, top_n: int = 20) -> go.Figure`

**Description**: Create bar chart for categorical column distribution.

**Parameters**:
- `df` (pd.DataFrame): Input dataset
- `column` (str): Categorical column name
- `title` (str | None): Optional chart title
- `top_n` (int): Show top N categories (default: 20)

**Returns**:
- `plotly.graph_objects.Figure`: Interactive bar chart

**Example**:
```python
fig = plot_categorical_distribution(cctv_df, 'district', top_n=10)
st.plotly_chart(fig, use_container_width=True)
```

**Contract**:
- MUST sort categories by frequency (descending)
- MUST limit to top_n categories (aggregate rest as "Other" if exceeded)
- MUST include value counts in hover data
- MUST handle missing values as separate category or exclude

---

#### `create_folium_map(df: pd.DataFrame, lat_col: str, lng_col: str, popup_cols: list[str] = [], color: str = 'blue', name: str = 'Points', icon: str = 'info-sign') -> folium.Map`

**Description**: Create Folium map with markers for dataset.

**Parameters**:
- `df` (pd.DataFrame): Dataset with coordinates
- `lat_col`, `lng_col` (str): Coordinate column names
- `popup_cols` (list[str]): Columns to include in marker popups (default: empty)
- `color` (str): Marker color (default: 'blue')
- `name` (str): Layer name for legend (default: 'Points')
- `icon` (str): Marker icon (default: 'info-sign')

**Returns**:
- `folium.Map`: Map object ready for rendering

**Example**:
```python
map_obj = create_folium_map(
    cctv_df, 'lat', 'lng',
    popup_cols=['location', 'type'],
    color='red',
    name='CCTV Locations'
)
st_folium(map_obj, width=700, height=500)
```

**Contract**:
- MUST calculate map center as mean of coordinates
- MUST determine appropriate zoom level based on coordinate spread
- MUST sample to 5000 points if dataset larger (for performance)
- MUST create popup HTML from popup_cols if provided
- MUST add MarkerCluster for >100 points
- MUST add LayerControl for layer toggling

---

#### `create_overlay_map(datasets: list[dict]) -> folium.Map`

**Description**: Create map with multiple datasets overlaid as separate layers.

**Parameters**:
- `datasets` (list[dict]): List of dataset specifications
  ```python
  [
      {
          'df': pd.DataFrame,
          'lat_col': str,
          'lng_col': str,
          'popup_cols': list[str],
          'color': str,
          'name': str,
          'icon': str
      },
      ...
  ]
  ```

**Returns**:
- `folium.Map`: Map with multiple togglable layers

**Example**:
```python
map_obj = create_overlay_map([
    {'df': train_df, 'lat_col': 'lat', 'lng_col': 'lng', 'color': 'blue', 'name': 'Train'},
    {'df': cctv_df, 'lat_col': 'latitude', 'lng_col': 'longitude', 'color': 'red', 'name': 'CCTV'}
])
st_folium(map_obj, width=700, height=500)
```

**Contract**:
- MUST create separate FeatureGroup for each dataset
- MUST add LayerControl for toggling visibility
- MUST calculate unified map center from all datasets
- MUST apply sampling to each dataset if needed
- MUST use distinct colors for each layer

---

## utils/narration.py

### Purpose
Generate natural language textual insights from analysis results.

### Functions

#### `summarize_proximity_stats(stats_df: pd.DataFrame, threshold: str, facility_name: str) -> str`

**Description**: Generate natural language summary of proximity analysis results.

**Parameters**:
- `stats_df` (pd.DataFrame): Proximity statistics (output from compute_proximity_stats)
- `threshold` (str): Threshold column name (e.g., '0.5', '1.0')
- `facility_name` (str): Name of target facility type (e.g., 'CCTVs', 'Security Lights')

**Returns**:
- `str`: Natural language summary paragraph

**Example**:
```python
text = summarize_proximity_stats(proximity_df, '0.5', 'CCTVs')
# Output: "On average, there are 3.2 CCTVs within 0.5km of train data points, indicating moderate spatial correlation."
```

**Contract**:
- MUST calculate mean, median, max from stats_df[threshold]
- MUST classify density as "high" (mean > 5), "moderate" (2-5), or "low" (<2)
- MUST return complete grammatical sentence
- MUST include specific numeric values
- SHOULD be understandable to data analysis beginners

---

#### `generate_distribution_insight(df: pd.DataFrame, column: str) -> str`

**Description**: Generate insight about column distribution characteristics.

**Parameters**:
- `df` (pd.DataFrame): Input dataset
- `column` (str): Column name to analyze

**Returns**:
- `str`: Distribution characteristic description

**Example**:
```python
text = generate_distribution_insight(cctv_df, 'installation_year')
# Output: "The data is right-skewed with most installations occurring after 2015."
```

**Contract**:
- MUST detect skewness (left/right/symmetric)
- MUST identify concentration patterns
- MUST mention outliers if significant (>3 std dev)
- MUST return educational, beginner-friendly language

---

#### `compare_distributions(df1: pd.DataFrame, col1: str, df2: pd.DataFrame, col2: str) -> str`

**Description**: Generate comparative insight between two column distributions.

**Parameters**:
- `df1`, `df2` (pd.DataFrame): Datasets to compare
- `col1`, `col2` (str): Column names to compare

**Returns**:
- `str`: Comparative analysis text

**Example**:
```python
text = compare_distributions(train_df, 'feature_x', test_df, 'feature_x')
# Output: "Train and test distributions are similar with mean difference of 0.3 (5%)."
```

**Contract**:
- MUST calculate mean/std difference
- MUST comment on distributional similarity (KS test or simple heuristics)
- MUST express difference in absolute and percentage terms
- MUST provide interpretation (similar/different/partially overlapping)

---

## Integration Contracts

### Streamlit Page Functions

Each tab/page should implement this standard interface:

#### `render_<dataset>_tab(df: pd.DataFrame) -> None`

**Description**: Render complete tab content for a specific dataset.

**Parameters**:
- `df` (pd.DataFrame): Dataset to visualize

**Returns**:
- `None`: Side effects only (Streamlit rendering)

**Behavior**:
- MUST display dataset info (rows, columns, missing values)
- MUST show descriptive statistics in expander
- MUST generate distribution plots for numeric/categorical columns
- MUST render map if coordinates detected
- MUST handle errors gracefully with st.error() or st.warning()

**Example**:
```python
def render_cctv_tab(df: pd.DataFrame) -> None:
    st.title("CCTV Data")
    st.write(f"Total CCTVs: {len(df)}")
    # ... visualization logic
```

---

## Error Handling Contract

All functions MUST adhere to this error handling pattern:

1. **Validation**: Check preconditions (non-empty DataFrames, valid column names)
2. **Graceful degradation**: Return empty/default values rather than crashing when possible
3. **Clear error messages**: Raise exceptions with actionable messages for developers
4. **User-friendly fallbacks**: In Streamlit context, use st.error()/st.warning() for end-user messages

---

## Testing Contract

While automated tests are optional per constitution, all functions MUST be manually
testable with these criteria:

- **Unit testability**: Functions should work with simple test DataFrames
- **Observable outputs**: Clear return values or Streamlit outputs
- **Reproducibility**: Same inputs always produce same outputs (caching aside)
- **Edge case handling**: Empty DataFrames, missing columns, invalid coordinates all handled

---

## Summary

This contract specification defines 15 core functions across 4 utility modules,
establishing clear interfaces for data loading, geospatial processing, visualization,
and narrative generation. All contracts prioritize simplicity, educational clarity,
and beginner-friendly implementation per constitutional principles.
