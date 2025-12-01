<!--
Sync Impact Report:
===================
Version: 1.0.0 (initial ratification)
Ratification Date: 2025-11-21
Last Amended: 2025-11-21

Modified Principles:
- NEW: I. Data-First Exploration
- NEW: II. Simplicity & Accessibility
- NEW: III. Educational Purpose (NON-NEGOTIABLE)
- NEW: IV. Streamlit-Based Visualization
- NEW: V. Scope Discipline

Added Sections:
- Core Principles (5 principles defined)
- Data Governance
- Development Workflow
- Governance

Templates Requiring Updates:
✅ spec-template.md - aligned (focus on user scenarios and requirements)
✅ plan-template.md - aligned (constitution check section present)
✅ tasks-template.md - aligned (supports phased implementation)

Follow-up TODOs:
- None (all placeholders filled)
-->

# Daegu Public Data Visualization Project Constitution

## Core Principles

### I. Data-First Exploration

**The data is not just provided — it is a tool to provoke thought.**

Every feature MUST prioritize understanding data structure, relationships, and distribution over
complex feature engineering or modeling. Users MUST be able to explore multiple public datasets
(CCTV, security lights, child protection zones, parking lots, accident data, train/test datasets)
in an integrated environment that facilitates rapid comprehension.

**Rationale**: This project exists to help learners discover insights and formulate project ideas
independently. Data visualization and exploration are the primary mechanisms for achieving this goal.

### II. Simplicity & Accessibility

**All code MUST be simple enough for Python beginners to understand.**

- No complex architectural patterns (repositories, factories, dependency injection)
- No advanced GIS processing (coordinate transformation, spatial joins)
- No separate backend servers or database construction
- Code structure MUST be clear, consistent, and self-explanatory
- Avoid over-optimization; educational clarity takes precedence over performance

**Rationale**: Target users are data analysis beginners and Python/Streamlit learners. If the code
is too complex, it defeats the educational purpose and creates barriers to learning.

### III. Educational Purpose (NON-NEGOTIABLE)

**Every feature MUST support learners in defining problems and planning projects independently.**

- Provide statistical summaries and visualizations that trigger analytical thinking
- Enable correlation discovery between datasets (e.g., train/test data, accident data,
  Daegu public facilities)
- Facilitate project idea generation through visual information
- Support hands-on learning of Streamlit, data analysis, and visualization basics

**Rationale**: The highest-level objective is empowering learners to independently conceive and
plan their next project. Features that do not contribute to this goal MUST be rejected.

### IV. Streamlit-Based Visualization

**The application MUST be a Streamlit-based responsive web visualization tool.**

- Tab-based navigation for each dataset
- Interactive graphs using Plotly or similar libraries
- Map-based visualizations using Folium, Pydeck, or equivalent
- Responsive UI that adapts to different screen sizes (mobile, tablet, desktop)
- Local execution only (no deployment required)

**Rationale**: Streamlit enables rapid prototyping and provides a low-barrier entry point for
learners to build interactive data applications. The focus on local execution reduces complexity.

### V. Scope Discipline

**Features outside the defined scope MUST be explicitly excluded.**

**Included Scope**:
- Streamlit-based responsive web UI
- CSV data loading and basic statistics
- Graph visualizations (Plotly, etc.)
- Map-based visualizations (Folium, Pydeck, etc.)
- Cross-dataset relationship exploration
- Lightweight exploratory analysis features

**Excluded Scope**:
- Separate backend API development
- Database construction
- Machine learning / deep learning model training
- Dashboard deployment (production hosting)
- Advanced GIS operations (complex spatial processing)

**Rationale**: Clear boundaries prevent scope creep and maintain focus on the educational mission.
Adding excluded features increases complexity and maintenance burden without commensurate
educational value.

## Data Governance

**Dataset Specifications**: All data files MUST reside in the `/data` directory:

- `대구 CCTV 정보.csv`
- `대구 보안등 정보.csv`
- `대구 어린이 보호 구역 정보.csv`
- `대구 주차장 정보.csv`
- `countrywide_accident.csv`
- `train.csv`
- `test.csv`

**Data Integrity**: File names and extensions MUST NOT be changed. Each dataset serves one or more
of the following purposes:

- Location-based map visualization
- Basic descriptive statistics
- Data distribution / pattern estimation
- Cross-dataset relationship analysis
- Project planning insights

**Data Access**: All datasets MUST be loaded via pandas or equivalent standard libraries. No
external databases or data processing pipelines are permitted.

## Development Workflow

**Environment Requirements**:
- Python 3.10 or higher
- pip or conda package management
- Cross-platform support (Windows, macOS, Linux)

**Installation Process**:
1. Clone repository
2. Install dependencies from `requirements.txt`:
   - streamlit
   - pandas
   - numpy
   - plotly
   - folium
   - geopandas (optional for map rendering)
   - pydeck or leafmap (optional)

**Execution**:
```bash
streamlit run app.py
```
Application runs at `http://localhost:8501` by default.

**Quality Standards**:
- Code simplicity MUST be prioritized over cleverness
- All functionality MUST be executable by anyone without complex setup
- Data exploration and visualization MUST be the central focus
- Code structure MUST be clear and consistent
- Excessive optimization MUST be avoided; maintain educational focus

**Testing Strategy**:
- Manual exploratory testing is sufficient for educational projects
- Automated tests are optional and MUST NOT add complexity
- Verification MUST focus on: data loading, visualization rendering, UI responsiveness

## Governance

**Constitution Authority**: This constitution supersedes all other development practices and
decisions. All specifications (spec.md), plans (plan.md), and tasks (tasks.md) MUST comply with
the principles defined herein.

**Amendment Process**:
1. Proposed amendments MUST be documented with clear rationale
2. Impact on existing features MUST be assessed
3. Template updates (spec-template.md, plan-template.md, tasks-template.md) MUST be synchronized
4. Version number MUST be incremented according to semantic versioning:
   - MAJOR: Backward-incompatible principle removals or redefinitions
   - MINOR: New principles added or material expansions
   - PATCH: Clarifications, wording fixes, non-semantic refinements

**Compliance Verification**:
- All feature specifications MUST include a "Constitution Check" section verifying alignment
- Code reviews MUST verify adherence to simplicity and accessibility principles
- Any complexity additions MUST be justified in the plan.md "Complexity Tracking" section
- Educational value MUST be the primary decision criterion for all features

**Versioning Policy**: Use semantic versioning (MAJOR.MINOR.PATCH) to track constitution changes.
Document all changes in the Sync Impact Report at the top of this file.

**Version**: 1.0.0 | **Ratified**: 2025-11-21 | **Last Amended**: 2025-11-21
