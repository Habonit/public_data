# Data Model: Daegu Public Data Visualization

**Feature**: 001-daegu-data-viz
**Date**: 2025-11-21
**Phase**: 1 - Data Model Design

## Purpose

This document defines the data structures, relationships, and processing rules for
the seven CSV datasets used in the Daegu public data visualization application.
Note: This is a read-only visualization application with no database or persistence
layer beyond CSV files.

---

## Dataset Entities

### 1. CCTV Data

**Source File**: `data/대구 CCTV 정보.csv`

**Purpose**: Represents closed-circuit television installations across Daegu for
security and traffic monitoring.

**Expected Columns** (auto-detected, actual columns may vary):
- Location identifiers (address, district, neighborhood)
- Geographic coordinates (latitude, longitude or 위도, 경도)
- Installation details (type, purpose, installation date)
- Administrative metadata (managing organization)

**Key Attributes**:
- `lat/latitude/위도`: Decimal degrees latitude
- `lng/longitude/경도`: Decimal degrees longitude
- Location text fields for popup displays
- Categorical fields for distribution analysis

**Validation Rules**:
- Coordinates must be within Daegu bounds (~35.8°N - 36.0°N, ~128.5°E - 128.7°E)
- Missing coordinates: exclude from map visualizations, include in statistics

**Relationships**:
- Spatial proximity to Security Lights, Child Protection Zones, Parking Lots
- Cross-analysis with Train data points

---

### 2. Security Lights Data

**Source File**: `data/대구 보안등 정보.csv`

**Purpose**: Represents street lighting infrastructure for nighttime safety.

**Expected Columns**:
- Location identifiers
- Geographic coordinates
- Light specifications (type, wattage, installation date)
- Road/district classifications

**Key Attributes**:
- `lat/latitude/위도`: Decimal degrees latitude
- `lng/longitude/경도`: Decimal degrees longitude
- Light type/classification for categorical analysis
- Installation dates for temporal analysis

**Validation Rules**:
- Coordinates within Daegu municipal boundaries
- Handle missing installation dates gracefully

**Relationships**:
- Spatial correlation with accident locations (safety hypothesis)
- Proximity analysis with Train data points

---

### 3. Child Protection Zone Data

**Source File**: `data/대구 어린이 보호 구역 정보.csv`

**Purpose**: Represents designated child safety areas around schools and facilities.

**Expected Columns**:
- Zone identifiers (name, school name)
- Geographic coordinates (zone center or boundary points)
- Zone specifications (area, length, speed limit)
- Associated school/facility information

**Key Attributes**:
- `lat/latitude/위도`: Zone center latitude
- `lng/longitude/경도`: Zone center longitude
- Zone name/school for popup labels
- Area/length measurements for distribution analysis

**Validation Rules**:
- Coordinates within Daegu boundaries
- Area/length values should be positive if present

**Relationships**:
- Spatial overlap analysis with accident data
- Proximity to Train data points

---

### 4. Parking Lot Data

**Source File**: `data/대구 주차장 정보.csv`

**Purpose**: Represents parking facilities (public, private, surface, underground).

**Expected Columns**:
- Facility identifiers (name, address)
- Geographic coordinates
- Capacity information (total spaces, disabled spaces)
- Operational details (type, hours, fees)

**Key Attributes**:
- `lat/latitude/위도`: Facility latitude
- `lng/longitude/경도`: Facility longitude
- Parking type (public/private, surface/underground)
- Capacity (numeric) for distribution analysis

**Validation Rules**:
- Coordinates within Daegu boundaries
- Capacity should be positive integer if present

**Relationships**:
- Infrastructure density analysis with other facilities
- Proximity to Train data points

---

### 5. Accident Data

**Source File**: `data/countrywide_accident.csv`

**Purpose**: Represents traffic/safety incidents nationwide (focus on Daegu subset).

**Expected Columns**:
- Incident identifiers
- Geographic coordinates
- Temporal information (date, time, day of week)
- Accident characteristics (type, severity, cause, weather)
- Location details (road type, district)

**Key Attributes**:
- `lat/latitude/위도`: Incident latitude
- `lng/longitude/경도`: Incident longitude
- Date/time for temporal distribution analysis
- Accident type/severity for categorical analysis
- Daegu-specific incidents (filter by coordinate bounds or city field)

**Validation Rules**:
- Valid date/time formats
- Coordinates should be valid decimal degrees
- Filter to Daegu region for focused analysis

**Relationships**:
- Spatial correlation with security infrastructure (CCTV, lights)
- Temporal pattern analysis
- Cross-analysis with Train data points

---

### 6. Train Data

**Source File**: `data/train.csv`

**Purpose**: Training dataset for analysis, potentially containing features related to
incidents or locations requiring various public facilities.

**Expected Columns**: Unknown - will be auto-detected on load

**Key Attributes**:
- Geographic coordinates (if present)
- Numeric features for distribution analysis
- Categorical features for grouping
- Target variable (if supervised learning context)

**Validation Rules**:
- Flexible schema - adapt visualization based on detected columns
- Coordinates optional but enable spatial analysis if present
- Handle missing values according to column type

**Relationships**:
- PRIMARY dataset for cross-analysis
- Spatial proximity analysis with all public facility datasets
- Distribution comparison with Test data

**Notes**:
- Central to Cross-Data Analysis feature
- May represent incident locations, facility requests, or other spatially-distributed phenomena

---

### 7. Test Data

**Source File**: `data/test.csv`

**Purpose**: Test dataset with structure similar to Train data for comparison.

**Expected Columns**: Should mirror Train data structure

**Key Attributes**:
- Same schema as Train data
- Used for distribution comparison
- Validates train data representativeness

**Validation Rules**:
- Schema should match Train data (warn if significant differences)
- Same validation rules as Train data

**Relationships**:
- Direct comparison with Train data distributions
- Optional spatial analysis if coordinates present

---

## Derived Data Structures

### Proximity Analysis Result

**Generated from**: Cross-dataset spatial analysis

**Structure**:
```python
{
    'base_dataset': str,           # e.g., 'train'
    'target_dataset': str,         # e.g., 'cctv'
    'thresholds': [0.5, 1.0, 2.0], # km
    'stats': pd.DataFrame,         # Rows: base points, Cols: threshold counts
    'summary': {
        '0.5km_mean': float,
        '1.0km_mean': float,
        '2.0km_mean': float,
        '0.5km_median': float,
        # ... etc
    }
}
```

**Purpose**: Quantify spatial relationships between datasets

**Validation**:
- Both datasets must have valid coordinates
- At least one point in each dataset
- Thresholds must be positive

---

### Statistical Summary

**Generated from**: Individual dataset analysis

**Structure**:
```python
{
    'dataset_name': str,
    'row_count': int,
    'column_count': int,
    'dtypes': dict,              # {col_name: dtype}
    'missing_ratios': dict,      # {col_name: missing_pct}
    'numeric_summary': pd.DataFrame,  # describe() output
    'categorical_summary': dict  # {col_name: value_counts}
}
```

**Purpose**: Provide comprehensive dataset overview

---

### Map Visualization Data

**Generated from**: Datasets with coordinates

**Structure**:
```python
{
    'points': pd.DataFrame,      # [lat, lng, popup_text, color, icon]
    'center': [lat, lng],        # Map center
    'zoom': int,                 # Initial zoom level
    'bounds': [[sw_lat, sw_lng], [ne_lat, ne_lng]]
}
```

**Purpose**: Prepare data for Folium map rendering

**Notes**:
- Automatically calculate center as mean of coordinates
- Determine zoom based on coordinate spread
- Limit to 5,000 points for performance (sample if needed)

---

## Data Processing Pipeline

### 1. Load Phase

```
CSV File → Encoding Detection (UTF-8/UTF-8-SIG/CP949)
         → pandas DataFrame
         → @st.cache_data (cache in session)
```

### 2. Coordinate Detection Phase

```
DataFrame → Column Name Pattern Matching
          → (lat_col, lng_col) or (None, None)
          → Flag: has_coordinates
```

### 3. Statistical Analysis Phase

```
DataFrame → Numeric Columns → describe()
          → Categorical Columns → value_counts()
          → Missing Values → isnull().sum()
          → Results cached per dataset
```

### 4. Spatial Analysis Phase (if coordinates present)

```
DataFrame A + DataFrame B → Coordinate Extraction
                          → Haversine Distance Matrix
                          → Proximity Counts per Threshold
                          → Statistical Summary
                          → Cached by (dataset_a, dataset_b, thresholds)
```

### 5. Visualization Phase

```
Statistical Summary → Plotly Charts (histogram, bar)
Coordinate Data → Folium Map + Markers
Proximity Results → Overlay Map + Statistics Table + Narrative Text
```

---

## Data Quality Considerations

### Missing Data Handling

- **Coordinates**: Exclude from maps, include in statistics, warn user
- **Numeric features**: Show missing ratios, skip in calculations, visualize missingness
- **Categorical features**: Treat as separate category or exclude based on context
- **Dates**: Parse flexibly, handle invalid formats gracefully

### Coordinate Validation

- **Daegu bounds**: Approximately 35.7°N - 36.1°N, 128.4°E - 128.8°E
- **Invalid coordinates**: 0, 0 or out-of-bound values flagged and excluded
- **Coordinate precision**: Accept 4-6 decimal places typical for geographic data

### Encoding Issues

- **Fallback sequence**: UTF-8 → UTF-8-SIG → CP949
- **Failure handling**: Display user-friendly error with troubleshooting steps
- **Column name detection**: Case-insensitive, multi-language (Korean/English)

### Performance Thresholds

- **Map rendering**: Sample to 5,000 points if dataset larger
- **Proximity analysis**: Sample base dataset to 5,000 if needed
- **Cache size**: Limit cached datasets to 7 (one per file)

---

## Data Relationships Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     CSV Data Files                          │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐          │
│  │  CCTV   │ │ Lights  │ │  Zones  │ │ Parking │          │
│  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘          │
│       │           │           │           │                 │
│  ┌────┴────┐ ┌────┴────┐ ┌────┴────┐ ┌────┴────┐          │
│  │Accident │ │  Train  │ │  Test   │ │         │          │
│  └────┬────┘ └────┬────┘ └────┬────┘ └─────────┘          │
└───────┼───────────┼───────────┼──────────────────────────┘
        │           │           │
        ▼           ▼           ▼
  ┌─────────────────────────────────┐
  │   Coordinate Detection          │
  │   (lat_col, lng_col finder)     │
  └──────────┬──────────────────────┘
             │
             ▼
  ┌─────────────────────────────────┐
  │   Statistical Analysis          │
  │   (describe, value_counts)      │
  └──────────┬──────────────────────┘
             │
        ┌────┴────┐
        │         │
        ▼         ▼
  ┌──────────┐ ┌──────────────────┐
  │  Charts  │ │   Map Rendering  │
  │ (Plotly) │ │    (Folium)      │
  └──────────┘ └──────────────────┘
        │                │
        │                │
        ▼                ▼
  ┌─────────────────────────────────┐
  │       Cross-Dataset Analysis    │
  │  (Haversine + Proximity Stats)  │
  └──────────┬──────────────────────┘
             │
             ▼
  ┌─────────────────────────────────┐
  │  Overlay Maps + Insights        │
  │  (Layer control + narratives)   │
  └─────────────────────────────────┘
```

---

## State Management

Since this is a Streamlit application with no backend persistence:

**Session State Usage**:
- **Cached DataFrames**: Managed by `@st.cache_data` decorator
- **UI State**: Streamlit automatically manages tab selection, widget states
- **No manual state management**: Streamlit's reactivity handles all state transitions

**No Database**:
- All data read-only from CSV files
- No writes, no updates, no deletes
- No user-generated data persistence

---

## Summary

This data model defines seven independent CSV datasets with optional spatial
coordinates, flexible schema detection, and derived structures for proximity
analysis and visualization. The design prioritizes simplicity (no ORM, no
complex relationships) while enabling rich exploratory analysis through
spatial correlation and statistical summarization.

All data transformations are pure functions (input CSV → output visualization)
with Streamlit caching for performance. This aligns with the constitutional
principles of simplicity, accessibility, and educational transparency.
