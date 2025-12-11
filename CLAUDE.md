# public_data Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-11-21

## Active Technologies
- Python 3.12 (현재 환경), Python 3.10+ 호환 + Streamlit 1.28.0+, pandas 2.0.0+, numpy 1.24.0+, plotly 5.17.0+, folium 0.14.0+, streamlit-folium 0.15.0+, anthropic (신규) (002-app-v1-1-upgrade)
- N/A (파일 기반, 사용자 업로드 CSV) (002-app-v1-1-upgrade)
- Python 3.10+ (현재 환경 Python 3.12 호환) (004-app-v12-upgrade)
- 파일 기반 (CSV 업로드, session_state 캐싱), model/ 디렉토리 (pkl 파일) (004-app-v12-upgrade)
- Python 3.10+ (현재 환경 Python 3.12 호환) + Streamlit 1.28.0+, pandas 2.0.0+, scikit-learn 1.7.2+, lightgbm 4.6.0+ (005-v1-3-deploy-prep)
- 파일 기반 (CSV 업로드, st.session_state 캐싱), model/ 디렉토리 (pkl 파일) (005-v1-3-deploy-prep)

- Python 3.10+ + Streamlit, pandas, numpy, plotly, folium, streamlit-folium (001-daegu-data-viz)

## Project Structure

```text
src/
tests/
```

## Commands

cd src [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] pytest [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] ruff check .

## Code Style

Python 3.10+: Follow standard conventions

## Recent Changes
- 005-v1-3-deploy-prep: Added Python 3.10+ (현재 환경 Python 3.12 호환) + Streamlit 1.28.0+, pandas 2.0.0+, scikit-learn 1.7.2+, lightgbm 4.6.0+
- 004-app-v12-upgrade: Added Python 3.10+ (현재 환경 Python 3.12 호환)
- 004-app-v12-upgrade: Added Python 3.10+ (현재 환경 Python 3.12 호환)


<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
