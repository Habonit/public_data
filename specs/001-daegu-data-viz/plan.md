# Implementation Plan: Daegu Public Data Visualization

**Branch**: `001-daegu-data-viz` | **Date**: 2025-11-21 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-daegu-data-viz/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a Streamlit-based web application for visualizing seven public datasets from Daegu
(CCTV, Security Lights, Child Protection Zones, Parking Lots) plus nationwide accident
data and train/test datasets. The application provides tab-based navigation for
individual dataset exploration with statistics and maps, cross-dataset spatial analysis
using Haversine distance calculations, and integrated educational content explaining
data analysis concepts. The primary goal is enabling data analysis learners to
independently discover insights and formulate project ideas through interactive visualization.

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: Streamlit, pandas, numpy, plotly, folium, streamlit-folium
**Storage**: CSV files in `/data` directory (no database)
**Testing**: Manual exploratory testing (automated tests optional, must not add complexity per constitution)
**Target Platform**: Local execution on Windows, macOS, Linux
**Project Type**: Single Streamlit application
**Performance Goals**: Initial load <3 seconds, map rendering smooth up to 5,000 points, tab switching <1 second
**Constraints**: Python beginners must understand code (no complex patterns), local-only execution (no deployment), educational clarity prioritized over optimization
**Scale/Scope**: 7 datasets, 9 tabs, single app.py or modular pages/ structure, <1GB total data

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Data-First Exploration ✅

**Requirement**: Feature must prioritize data structure, relationships, and distribution understanding.

**Compliance**: PASS - The entire application is designed around exploring seven datasets
with statistics, visualizations, and cross-dataset spatial analysis. Every tab focuses
on data comprehension rather than complex modeling.

### Principle II: Simplicity & Accessibility ✅

**Requirement**: Code must be simple enough for Python beginners to understand.

**Compliance**: PASS - Architecture uses simple module structure (utils/loader.py, utils/geo.py,
utils/visualizer.py) with no complex patterns (no repositories, factories, dependency injection).
All logic is straightforward data loading, calculation, and visualization.

### Principle III: Educational Purpose (NON-NEGOTIABLE) ✅

**Requirement**: Feature must support learners in defining problems and planning projects independently.

**Compliance**: PASS - Application provides:
- Statistical summaries and visualizations triggering analytical thinking
- Cross-dataset correlation discovery capabilities
- Project Overview tab with educational concepts
- Natural language insights to guide interpretation
- Multiple examples of spatial pattern analysis

### Principle IV: Streamlit-Based Visualization ✅

**Requirement**: Must be Streamlit-based responsive web visualization tool.

**Compliance**: PASS - Entire application built on Streamlit with:
- Tab-based navigation for each dataset
- Interactive graphs using Plotly
- Map-based visualizations using Folium
- Responsive UI design
- Local execution only

### Principle V: Scope Discipline ✅

**Requirement**: Features must stay within defined scope boundaries.

**Compliance**: PASS - Included scope items all present (Streamlit UI, CSV loading, graph/map
visualizations, cross-dataset exploration). Excluded scope items properly avoided
(no backend API, no database, no ML model training, no deployment infrastructure,
no advanced GIS operations).

### Summary

**Status**: ✅ ALL CHECKS PASSED

No constitution violations detected. All five core principles are satisfied by the
planned architecture and feature set.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
project-directory/
├── app.py                      # Main Streamlit entry point, tab configuration
├── pages/                      # Optional: multi-page structure for each tab
│   ├── 01_CCTV.py
│   ├── 02_Security_Lights.py
│   ├── 03_Child_Protection_Zones.py
│   ├── 04_Parking_Lots.py
│   ├── 05_Accident.py
│   ├── 06_Train.py
│   ├── 07_Test.py
│   ├── 08_Cross_Analysis.py
│   └── 09_Project_Overview.py
├── utils/
│   ├── loader.py              # Data loading with caching (@st.cache_data)
│   ├── geo.py                 # Haversine distance calculation, coordinate detection
│   ├── visualizer.py          # Common graph/map generation functions
│   └── narration.py           # Text-based insight generation
├── data/
│   ├── 대구 CCTV 정보.csv
│   ├── 대구 보안등 정보.csv
│   ├── 대구 어린이 보호 구역 정보.csv
│   ├── 대구 주차장 정보.csv
│   ├── countrywide_accident.csv
│   ├── train.csv
│   └── test.csv
├── requirements.txt
├── docs/
│   ├── daegu_constitution.md
│   ├── daegu_spec.md
│   └── dagu_plan.md
└── specs/
    └── 001-daegu-data-viz/
        ├── spec.md
        ├── plan.md              # This file
        ├── research.md          # Phase 0 output
        ├── data-model.md        # Phase 1 output
        ├── quickstart.md        # Phase 1 output
        └── contracts/           # Phase 1 output (if applicable)
```

**Structure Decision**: Single Streamlit application with modular utility functions.
Initially implement all tabs within `app.py` using `st.tabs()` for simplicity.
If code becomes unwieldy (>500 lines), migrate to `pages/` multi-page structure
with numbered files for tab ordering. The `utils/` directory provides clean
separation of concerns (data loading, geospatial calculations, visualization,
narrative generation) while maintaining beginner-friendly code readability.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No complexity violations detected. All architectural decisions align with constitution principles.
