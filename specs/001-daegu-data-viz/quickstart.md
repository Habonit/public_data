# Quickstart Guide: Daegu Public Data Visualization

**Feature**: 001-daegu-data-viz
**Date**: 2025-11-21
**Audience**: Developers and learners implementing the visualization application

## Purpose

This guide provides step-by-step instructions for setting up, running, and developing
the Daegu public data visualization Streamlit application. Follow this guide to go
from zero to a working application in under 10 minutes.

---

## Prerequisites

Before starting, ensure you have:

- **Python 3.10 or higher** installed
  - Check version: `python --version` or `python3 --version`
  - Download from: https://www.python.org/downloads/

- **pip** package manager (usually comes with Python)
  - Check: `pip --version` or `pip3 --version`

- **Git** (optional, for cloning repository)
  - Check: `git --version`

- **Terminal/Command Prompt** access

- **Text Editor or IDE** (VS Code, PyCharm, or any preferred editor)

---

## Quick Start (5 Minutes)

### 1. Get the Code

**Option A: Clone repository** (if using Git):
```bash
git clone <repository-url>
cd project-directory
```

**Option B: Manual setup**:
1. Create project directory: `mkdir daegu-viz && cd daegu-viz`
2. Download/copy all project files to this directory

### 2. Create Virtual Environment (Recommended)

**On Windows**:
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux**:
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Streamlit (web framework)
- pandas, numpy (data processing)
- plotly (interactive charts)
- folium, streamlit-folium (maps)

**Expected duration**: 1-2 minutes

### 4. Prepare Data Files

Ensure the `/data` directory contains these files:
```
data/
├── 대구 CCTV 정보.csv
├── 대구 보안등 정보.csv
├── 대구 어린이 보호 구역 정보.csv
├── 대구 주차장 정보.csv
├── countrywide_accident.csv
├── train.csv
└── test.csv
```

**Troubleshooting**:
- If any files are missing, you'll see a warning when the app runs
- Ensure file names match exactly (including Korean characters)
- Check that files are CSV format, not Excel or other formats

### 5. Run the Application

```bash
streamlit run app.py
```

The application should automatically open in your default web browser at:
```
http://localhost:8501
```

If it doesn't open automatically, manually navigate to that URL.

**Expected result**: You should see the Daegu Public Data Visualization interface
with nine tabs ready for exploration.

---

## Detailed Setup Guide

### Environment Setup

#### Option 1: Using venv (Recommended for Beginners)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Option 2: Using conda

```bash
# Create environment
conda create -n daegu-viz python=3.10

# Activate
conda activate daegu-viz

# Install dependencies
pip install -r requirements.txt
# OR use conda equivalents:
conda install streamlit pandas numpy plotly
pip install folium streamlit-folium
```

#### Verifying Installation

```bash
# Check Streamlit
streamlit --version

# Check Python packages
python -c "import streamlit, pandas, plotly, folium; print('All packages installed!')"
```

### Project Structure Setup

If starting from scratch, create this directory structure:

```bash
mkdir -p utils data docs specs/001-daegu-data-viz
```

Your final structure should match:
```
project-directory/
├── app.py                   # Main application entry point
├── utils/
│   ├── loader.py           # Data loading utilities
│   ├── geo.py              # Geospatial calculations
│   ├── visualizer.py       # Chart and map generation
│   └── narration.py        # Text insight generation
├── data/
│   └── [CSV files here]
├── requirements.txt
└── specs/
    └── 001-daegu-data-viz/
        ├── spec.md
        ├── plan.md
        ├── research.md
        ├── data-model.md
        ├── quickstart.md         # This file
        └── contracts/
```

---

## Development Workflow

### Starting a Development Session

1. **Activate virtual environment**:
   ```bash
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

2. **Start Streamlit in development mode**:
   ```bash
   streamlit run app.py
   ```

3. **Enable auto-reload**: Streamlit automatically reloads when you save files.
   Just edit code and save - the browser will update!

### Making Changes

#### Editing Utility Functions

Example: Adding a new function to `utils/geo.py`

```python
# utils/geo.py

def calculate_center_point(df: pd.DataFrame, lat_col: str, lng_col: str) -> tuple[float, float]:
    """Calculate geographic center of dataset."""
    lat_mean = df[lat_col].mean()
    lng_mean = df[lng_col].mean()
    return (lat_mean, lng_mean)
```

**Save the file** → Streamlit automatically reloads → Test in browser

#### Adding a New Tab

In `app.py`:

```python
# Inside the main() function
tab9, tab10 = st.tabs(["...", "New Tab"])

with tab10:
    st.title("New Analysis Tab")
    # Your new content here
```

### Debugging Tips

#### Check Logs

Streamlit shows errors in two places:
1. **Browser**: Red error boxes with stack traces
2. **Terminal**: Full error messages and print statements

#### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'streamlit'`
- **Solution**: Activate virtual environment first

**Issue**: `FileNotFoundError: [Errno 2] No such file or directory: 'data/...'`
- **Solution**: Check data files are in correct location with correct names

**Issue**: `UnicodeDecodeError`
- **Solution**: The `read_csv_safe()` function should handle this. If not, check file encoding manually.

**Issue**: Map not rendering
- **Solution**: Check that streamlit-folium is installed: `pip show streamlit-folium`

#### Using Streamlit's Built-in Debugger

Add this to any function:
```python
import streamlit as st

st.write("Debug info:", variable_name)
```

Or use Python's debugger:
```python
import pdb; pdb.set_trace()
```

---

## Testing Your Changes

### Manual Testing Checklist

After making changes, verify:

**Basic Functionality**:
- [ ] Application starts without errors
- [ ] All nine tabs are visible
- [ ] Data loads in each tab

**Individual Dataset Tabs**:
- [ ] Data preview shows (head of DataFrame)
- [ ] Statistics calculate correctly (rows, columns, missing values)
- [ ] Histograms render for numeric columns
- [ ] Bar charts render for categorical columns
- [ ] Maps appear if coordinates detected
- [ ] Map markers are clickable (show popups)

**Cross-Data Analysis Tab**:
- [ ] Dataset selection dropdowns work
- [ ] Proximity analysis calculates (within 10 seconds)
- [ ] Statistics table displays threshold counts
- [ ] Overlay map shows both datasets with different colors
- [ ] Layer toggle controls work
- [ ] Narrative text generates meaningful insights

**Project Overview Tab**:
- [ ] Project description displays
- [ ] System diagram renders (if using Mermaid)
- [ ] Educational concepts section is readable
- [ ] All markdown formatting correct

### Performance Testing

Check these performance criteria:

```bash
# Time the initial load
time streamlit run app.py
# Should be <3 seconds to start
```

In browser DevTools (F12):
- Initial page load: <3 seconds
- Tab switching: <1 second
- Map rendering (5000 points): <5 seconds

### Data Validation Testing

Test with edge cases:

1. **Missing CSV file**: Remove one file temporarily, check warning appears
2. **Empty dataset**: Create empty CSV, verify graceful handling
3. **Missing coordinates**: Test dataset without lat/lng columns
4. **Large dataset**: Test with >10,000 rows, verify sampling occurs
5. **Special characters**: Ensure Korean characters in data display correctly

---

## Deployment (Local Only)

Per constitutional requirement, this application runs locally only. No cloud deployment.

### Sharing with Others

To share the application with teammates:

1. **Package the code**:
   ```bash
   # Zip the project directory
   zip -r daegu-viz.zip . -x "venv/*" -x "*.pyc" -x "__pycache__/*"
   ```

2. **Share zip + instructions**:
   - Send the zip file
   - Include this quickstart.md
   - Ensure they have Python 3.10+

3. **Recipient setup**:
   ```bash
   unzip daegu-viz.zip
   cd daegu-viz
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   streamlit run app.py
   ```

### Running on Different Port

If port 8501 is in use:
```bash
streamlit run app.py --server.port 8502
```

### Running on Network (Local Network Access)

To access from other devices on same WiFi:
```bash
streamlit run app.py --server.address 0.0.0.0
```

Then access via: `http://<your-ip>:8501`
- Find your IP: `ipconfig` (Windows) or `ifconfig` (macOS/Linux)

---

## Updating Dependencies

If new packages are added:

1. **Add to requirements.txt**:
   ```text
   new-package>=1.0.0
   ```

2. **Install**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Freeze current versions** (optional):
   ```bash
   pip freeze > requirements-frozen.txt
   ```

---

## Troubleshooting Guide

### Streamlit Won't Start

**Symptom**: `streamlit: command not found`

**Solutions**:
1. Check virtual environment is activated (should see `(venv)` in prompt)
2. Reinstall Streamlit: `pip install streamlit`
3. Try `python -m streamlit run app.py` instead

### Data Files Not Loading

**Symptom**: "File not found" warnings in app

**Solutions**:
1. Verify file paths: `ls data/` (macOS/Linux) or `dir data\` (Windows)
2. Check file name spelling (case-sensitive on Linux/macOS)
3. Verify CSV format (not Excel .xlsx)
4. Check encoding (should auto-detect UTF-8/CP949)

### Maps Not Displaying

**Symptom**: Blank space where map should be

**Solutions**:
1. Check streamlit-folium installed: `pip show streamlit-folium`
2. Look for JavaScript errors in browser console (F12)
3. Verify coordinates in dataset (use st.write(df.head()) to check)
4. Try clearing Streamlit cache: Add `?clear_cache=true` to URL

### Performance Issues

**Symptom**: App is slow or unresponsive

**Solutions**:
1. Check dataset sizes: `df.shape` for each dataset
2. Verify caching is working (should see "Using cached value" in logs)
3. Reduce map points (sampling should auto-trigger at 5000+)
4. Close other tabs to free memory
5. Restart Streamlit: Ctrl+C in terminal, then `streamlit run app.py` again

### Korean Characters Display Issues

**Symptom**: Boxes or garbled text instead of Korean characters

**Solutions**:
1. Ensure file saved with UTF-8 encoding
2. Check terminal supports UTF-8
3. On Windows, try: `chcp 65001` before running
4. Verify font supports Korean characters

---

## Next Steps

After getting the application running:

1. **Explore the Code**:
   - Read `utils/loader.py` to understand data loading
   - Review `utils/geo.py` for geospatial calculations
   - Study `utils/visualizer.py` for chart generation patterns

2. **Customize Visualizations**:
   - Change color schemes in Plotly charts
   - Add new chart types (scatter plots, box plots)
   - Customize map markers and popups

3. **Add New Features**:
   - Implement additional cross-dataset analyses
   - Add temporal visualizations (time series)
   - Create export functionality (download results as CSV)

4. **Read the Specs**:
   - Review `specs/001-daegu-data-viz/spec.md` for full requirements
   - Check `data-model.md` for data structure details
   - Consult `contracts/module-interfaces.md` for function specifications

5. **Generate Tasks**:
   - Run `/speckit.tasks` to generate implementation task list
   - Follow task-by-task development workflow

---

## Getting Help

### Documentation References

- **Streamlit Docs**: https://docs.streamlit.io/
- **Pandas Docs**: https://pandas.pydata.org/docs/
- **Plotly Docs**: https://plotly.com/python/
- **Folium Docs**: https://python-visualization.github.io/folium/

### Common Commands Reference

```bash
# Start app
streamlit run app.py

# Start with custom port
streamlit run app.py --server.port 8502

# Clear cache
streamlit cache clear

# Check Streamlit version
streamlit --version

# Update Streamlit
pip install --upgrade streamlit

# List installed packages
pip list

# Check where Python is running from
which python  # macOS/Linux
where python  # Windows
```

### Streamlit Shortcuts (in browser)

- **R**: Rerun app
- **C**: Clear cache
- **Ctrl+Alt+R**: Record screen (for sharing bugs)

---

## Success Checklist

You're ready to develop when:

- [x] Python 3.10+ installed and verified
- [x] Virtual environment created and activated
- [x] All dependencies installed successfully
- [x] Data files present in `/data` directory
- [x] Application starts with `streamlit run app.py`
- [x] Browser opens to localhost:8501
- [x] All tabs visible and clickable
- [x] At least one dataset loads and displays
- [x] You can make a code change and see it reload

**Estimated setup time**: 5-10 minutes

**Estimated time to first customization**: 15-20 minutes

---

## Additional Resources

### Example Workflows

**Workflow 1: Adding a New Visualization**

1. Identify the dataset and tab to modify
2. Open corresponding function in `app.py` or create new function
3. Use existing visualizer functions from `utils/visualizer.py`
4. Test with sample data first
5. Add to main tab rendering logic
6. Verify with full dataset

**Workflow 2: Improving Proximity Analysis**

1. Review current algorithm in `utils/geo.py`
2. Make changes to `compute_proximity_stats()`
3. Test with small datasets (100 rows each)
4. Verify performance with larger datasets
5. Update narrative generation in `utils/narration.py` if needed
6. Test full cross-analysis tab workflow

**Workflow 3: Adding Educational Content**

1. Draft content in markdown format
2. Add to Project Overview tab in `app.py`
3. Use `st.markdown()` or `st.expander()` for organization
4. Include code examples if helpful
5. Test readability with target audience (beginners)

---

## Conclusion

You now have everything needed to run, develop, and customize the Daegu Public Data
Visualization application. The application is designed to be beginner-friendly, so
don't hesitate to experiment with the code. Streamlit's auto-reload makes iteration
fast and fun.

Happy coding! 🚀
