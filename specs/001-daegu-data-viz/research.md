# Research: Daegu Public Data Visualization

**Feature**: 001-daegu-data-viz
**Date**: 2025-11-21
**Phase**: 0 - Technology Research and Decision Making

## Purpose

This document captures research findings and technology decisions for implementing
the Daegu public data visualization Streamlit application. All decisions prioritize
simplicity, educational clarity, and alignment with constitutional principles.

---

## Research Areas

### 1. Streamlit Multi-Tab/Page Architecture

**Question**: Should we use `st.tabs()` in a single `app.py` or Streamlit's multi-page app structure?

**Research**:
- `st.tabs()`: All tab logic in one file, simpler for beginners to understand flow
- Multi-page (`pages/` directory): Each tab is separate file, better code organization for large apps
- Hybrid approach: Start with `st.tabs()`, migrate to multi-page if app.py exceeds ~500 lines

**Decision**: Start with `st.tabs()` in single `app.py`

**Rationale**:
- Aligns with Simplicity & Accessibility principle
- Easier for learners to see entire application flow in one place
- Streamlit automatically handles tab state management
- Can refactor to multi-page later if complexity grows

**Alternatives Considered**:
- Immediate multi-page structure: Rejected due to added mental overhead for beginners
- Dash or Panel frameworks: Rejected as Streamlit is more beginner-friendly per constitution

---

### 2. Map Visualization Library

**Question**: Which library should we use for geospatial visualization?

**Research**:
- **Folium**: Python wrapper for Leaflet.js, simple API, good for educational purposes
- **Pydeck**: Powerful WebGL-based, better performance, steeper learning curve
- **Plotly Maps**: Integrated with Plotly, limited customization for markers
- **streamlit-folium**: Bridge library to integrate Folium maps into Streamlit

**Decision**: Folium with streamlit-folium

**Rationale**:
- Simple, intuitive API perfect for beginners
- Excellent documentation and community support
- Supports layer control for overlay maps (required for cross-analysis)
- MarkerCluster plugin handles large point sets efficiently
- `streamlit-folium` provides seamless Streamlit integration
- Aligns with Educational Purpose principle

**Alternatives Considered**:
- Pydeck: Rejected due to complexity (WebGL, deck.gl concepts too advanced for beginners)
- Plotly Maps: Rejected due to limited interactive marker customization

---

### 3. Distance Calculation Method

**Question**: How should we calculate distances between geographic coordinates?

**Research**:
- **Haversine formula**: Calculates great-circle distance on sphere, accurate for Earth distances
- **Euclidean distance**: Simple but inaccurate for lat/lng (treats Earth as flat)
- **Vincenty formula**: More accurate (ellipsoid model) but computationally expensive
- **geopy library**: Provides distance calculations with multiple algorithms

**Decision**: Haversine formula (manual implementation or geopy)

**Rationale**:
- Haversine provides sufficient accuracy for city-scale analysis (<10km typical distances)
- Simple mathematical formula easy for learners to understand
- Fast computation for thousands of point-to-point calculations
- Euclidean distance would introduce significant errors (up to 30% at high latitudes)
- Vincenty accuracy gain unnecessary for educational exploration

**Implementation Approach**:
```python
from math import radians, cos, sin, asin, sqrt

def haversine(lat1, lon1, lat2, lon2):
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6371 * c  # Earth radius in kilometers
    return km
```

**Alternatives Considered**:
- geopy.distance.geodesic(): Acceptable but adds dependency; manual implementation more educational
- Euclidean distance: Rejected due to accuracy concerns

---

### 4. Data Caching Strategy

**Question**: How should we cache CSV data to improve performance?

**Research**:
- Streamlit caching decorators:
  - `@st.cache_data`: For data transformations (pandas DataFrames, JSON)
  - `@st.cache_resource`: For global resources (database connections, ML models)
- Cache invalidation: Automatically handles based on function inputs and code changes

**Decision**: Use `@st.cache_data` decorator on all data loading functions

**Rationale**:
- Prevents re-reading CSV files on every tab switch or interaction
- Streamlit automatically manages cache lifecycle
- Simple decorator pattern easy for beginners to understand
- Meets performance goal: initial load <3 seconds

**Implementation Example**:
```python
@st.cache_data
def load_dataset(name: str) -> pd.DataFrame:
    # Data loading logic
    return df
```

**Alternatives Considered**:
- Manual caching with session_state: Rejected as overly complex for beginners
- No caching: Rejected due to performance concerns

---

### 5. Encoding Handling for Korean CSV Files

**Question**: How should we handle potential encoding issues with Korean filenames/content?

**Research**:
- Common encodings for Korean text:
  - UTF-8: Universal standard, most modern
  - UTF-8-SIG: UTF-8 with BOM (Byte Order Mark), used by Excel
  - CP949 (EUC-KR): Legacy Korean encoding, still common in government data
- pandas `read_csv()` supports `encoding` parameter

**Decision**: Try multiple encodings in sequence (UTF-8 → UTF-8-SIG → CP949)

**Rationale**:
- Government data often uses mixed encodings
- Graceful fallback ensures data loads without manual intervention
- Aligns with user-friendly error handling requirements

**Implementation Approach**:
```python
def read_csv_safe(path: str) -> pd.DataFrame:
    encodings = ['utf-8', 'utf-8-sig', 'cp949']
    for enc in encodings:
        try:
            return pd.read_csv(path, encoding=enc)
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Could not decode {path} with any encoding")
```

**Alternatives Considered**:
- Single encoding assumption: Rejected due to real-world variability
- chardet library for auto-detection: Rejected as overkill for known encoding set

---

### 6. Cross-Dataset Proximity Analysis Algorithm

**Question**: What's the optimal approach for calculating proximity statistics between datasets?

**Research**:
- **Nested loop**: For each train point, check all facility points
  - Complexity: O(n*m) where n=train rows, m=facility rows
  - Acceptable for <10k points per dataset
- **Spatial indexing (R-tree)**: Pre-index points for fast proximity queries
  - Libraries: scipy.spatial, rtree, shapely
  - Complexity: O(n log m) but added complexity
- **Sampling**: Limit analysis to representative sample of points
  - Reduces computation but maintains statistical validity

**Decision**: Nested loop with optional sampling for large datasets

**Rationale**:
- Simple algorithm easy for learners to understand
- Performance acceptable for expected data sizes (<5,000 points)
- If dataset exceeds 5,000 rows, randomly sample to maintain <3 second calculation time
- Avoids spatial indexing library complexity (violates Simplicity principle)

**Implementation Approach**:
```python
def compute_proximity_stats(df_base, df_target, thresholds=[0.5, 1.0, 2.0]):
    # Sample if needed
    if len(df_base) > 5000:
        df_base = df_base.sample(5000)

    results = []
    for _, base_row in df_base.iterrows():
        counts = {t: 0 for t in thresholds}
        for _, target_row in df_target.iterrows():
            dist = haversine(base_row['lat'], base_row['lng'],
                           target_row['lat'], target_row['lng'])
            for t in thresholds:
                if dist <= t:
                    counts[t] += 1
        results.append(counts)
    return pd.DataFrame(results)
```

**Alternatives Considered**:
- scipy.spatial.cKDTree: Rejected due to complexity and coordinate conversion requirements
- GPU acceleration: Rejected as overkill for educational project

---

### 7. Natural Language Insight Generation

**Question**: How should we generate textual insights from proximity analysis results?

**Research**:
- **Rule-based templates**: if-else logic with threshold-based messages
- **LLM API calls**: GPT/Claude to generate narrative (requires API keys, internet)
- **Statistical summarization**: Automated text from mean/median/max values

**Decision**: Rule-based template system with statistical summarization

**Rationale**:
- No external dependencies or API keys required
- Deterministic, predictable output
- Educational transparency (learners can see how insights are generated)
- Aligns with Simplicity principle

**Implementation Example**:
```python
def summarize_proximity_stats(stats_df, threshold, facility_name):
    mean_count = stats_df[threshold].mean()
    if mean_count > 5:
        density = "high"
    elif mean_count > 2:
        density = "moderate"
    else:
        density = "low"

    return f"On average, there are {mean_count:.1f} {facility_name} within {threshold}km " \
           f"of train data points, indicating {density} spatial correlation."
```

**Alternatives Considered**:
- LLM API integration: Rejected due to external dependency and cost concerns
- No narrative generation: Rejected as reduces educational value

---

### 8. Coordinate Column Auto-Detection

**Question**: How should we automatically detect latitude/longitude columns in datasets?

**Research**:
- Common Korean column names: 위도 (latitude), 경도 (longitude), Y좌표, X좌표
- Common English names: lat, latitude, Lat, lng, lon, longitude, Lng
- Case sensitivity: Korean doesn't apply, English varies

**Decision**: Multi-language pattern matching with case-insensitive search

**Implementation Approach**:
```python
def detect_lat_lng_columns(df):
    lat_candidates = ['lat', 'latitude', '위도', 'y좌표', 'y', 'Lat', 'Latitude']
    lng_candidates = ['lng', 'lon', 'longitude', '경도', 'x좌표', 'x', 'Lng', 'Lon', 'Longitude']

    lat_col = None
    lng_col = None

    for col in df.columns:
        if col.lower() in [c.lower() for c in lat_candidates]:
            lat_col = col
        if col.lower() in [c.lower() for c in lng_candidates]:
            lng_col = col

    return lat_col, lng_col
```

**Rationale**:
- Handles both Korean and English column names
- Case-insensitive to handle data entry variations
- Simple list-based matching easy to understand and extend

**Alternatives Considered**:
- Regex patterns: Rejected as harder for beginners to understand
- Manual column specification: Rejected as reduces usability

---

### 9. Visualization Library for Statistical Charts

**Question**: Which library should we use for histograms, bar charts, and distribution plots?

**Research**:
- **Matplotlib**: Python standard, static plots, familiar to beginners
- **Seaborn**: Statistical visualization, beautiful defaults, built on matplotlib
- **Plotly**: Interactive, modern, web-based, integrates well with Streamlit
- **Altair**: Declarative, Vega-Lite based, good for exploratory analysis

**Decision**: Plotly Express

**Rationale**:
- Native Streamlit support via `st.plotly_chart()`
- Interactive features (zoom, pan, hover) enhance exploration
- Simple one-line API for common charts
- Consistent visual style with modern web aesthetics
- Better user experience than static matplotlib plots

**Implementation Example**:
```python
import plotly.express as px

fig = px.histogram(df, x='column_name', title='Distribution')
st.plotly_chart(fig, use_container_width=True)
```

**Alternatives Considered**:
- Matplotlib: Rejected due to lack of interactivity
- Seaborn: Rejected as redundant with Plotly Express's simple API
- Altair: Rejected due to less familiar syntax for beginners

---

### 10. Testing Strategy

**Question**: What testing approach should we take given constitutional constraints?

**Research**:
- Constitution explicitly states: "Manual exploratory testing sufficient" and "Automated tests optional, must not add complexity"
- Educational project focuses on learning, not production deployment
- pytest framework would require test structure setup

**Decision**: Manual exploratory testing with documented test scenarios

**Rationale**:
- Aligns perfectly with constitution's testing guidance
- Reduces cognitive load for learners
- Focuses on functional verification rather than test infrastructure
- Test scenarios documented in spec.md acceptance criteria

**Test Documentation Approach**:
- Create simple checklist in plan.md or tasks.md
- Each user story maps to manual test scenario
- No pytest, no test files, no test infrastructure

**Alternatives Considered**:
- pytest suite: Rejected per constitutional guidance
- No testing: Rejected as verification still necessary

---

## Technology Stack Summary

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| **Language** | Python 3.10+ | Constitution requirement, broad compatibility |
| **Web Framework** | Streamlit | Constitution requirement, beginner-friendly |
| **Data Processing** | pandas, numpy | Industry standard, familiar to learners |
| **Charts** | Plotly Express | Interactive, simple API, Streamlit-native |
| **Maps** | Folium + streamlit-folium | Simple, educational, supports layers |
| **Distance Calc** | Haversine (manual) | Simple math, transparent algorithm |
| **Caching** | @st.cache_data | Built-in Streamlit feature |
| **Encoding** | UTF-8/UTF-8-SIG/CP949 fallback | Handles Korean data variability |
| **Testing** | Manual exploratory | Constitution-compliant simplicity |

---

## Dependencies (requirements.txt)

```text
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.17.0
folium>=0.14.0
streamlit-folium>=0.15.0
```

**Notes**:
- Version minimums ensure compatibility with Python 3.10+
- No testing frameworks included per constitution
- No ML libraries (stays within scope)
- No database drivers (CSV-only storage)

---

## Open Questions Resolved

All technical context items marked "NEEDS CLARIFICATION" have been resolved:
- ✅ Multi-tab architecture approach defined
- ✅ Map library selected (Folium)
- ✅ Distance calculation method chosen (Haversine)
- ✅ Caching strategy determined (@st.cache_data)
- ✅ Encoding handling approach established
- ✅ Proximity analysis algorithm designed
- ✅ Insight generation method decided
- ✅ Coordinate detection approach specified
- ✅ Chart library selected (Plotly)
- ✅ Testing strategy clarified

No unresolved clarifications remain. Ready to proceed to Phase 1: Design & Contracts.
