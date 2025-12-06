# Streamlit 학습 가이드

현재 대구 공공데이터 시각화 앱을 이해하고 유지보수하기 위한 체계적인 Streamlit 학습 자료입니다.

## 📚 학습 목표

이 예제들을 모두 완료하면 다음을 할 수 있습니다:

- ✅ 현재 앱(`app.py`)의 모든 코드 이해
- ✅ Streamlit 앱 디버깅 및 에러 해결
- ✅ 새로운 기능 추가 및 개선
- ✅ 차트와 지도를 활용한 데이터 시각화
- ✅ 사용자 인터랙션 구현

## 📖 학습 순서

### 🟢 기초 (필수)

| 예제 | 주제 | 현재 앱 연관성 |
|------|------|---------------|------|
| [01](./01_README.md) | 기본 설정 및 텍스트 | `st.set_page_config`, `st.title`, `st.markdown` |
| [02](./02_README.md) | 레이아웃과 컬럼 | `st.columns`, `st.metric` |
| [03](./03_README.md) | 데이터 표시 및 캐싱 | `st.dataframe`, `@st.cache_data` |
| [04](./04_README.md) | 사용자 입력 | `st.selectbox`, `st.multiselect`, `st.button` |
| [05](./05_README.md) | 확장 가능한 섹션 | `st.expander` |

### 🟡 중급 (필수)

| 예제 | 주제 | 현재 앱 연관성 |
|------|------|---------------|------|
| [06](./06_README.md) | 탭 네비게이션 | `st.tabs` (메인 구조) |
| [07](./07_README.md) | 상태 메시지 | `st.success`, `st.warning`, `st.error`, `st.info` |
| [08](./08_README.md) | 로딩 스피너 | `st.spinner` |

### 🔴 고급 (핵심)

| 예제 | 주제 | 현재 앱 연관성 |
|------|------|---------------|
| [09](./09_README.md) | Plotly 차트 | `plot_numeric_distribution`, `plot_categorical_distribution` |
| [10](./10_README.md) | Folium 지도 | `create_folium_map`, `create_overlay_map` |
| [11](./11_README.md) | 고급 통합 | 전체 패턴 통합 |
| [12](./12_README.md) | 완전한 대시보드 | **현재 앱 구조 완전 이해** |

### 🟣 실전 (필수)

| 예제 | 주제 | 현재 앱 연관성 |
|------|------|---------------|
| [13](./13_README.md) | 세션 상태 및 필수 기능 | `st.session_state`, 파일 업로드/다운로드, 사이드바 |
| [14](./14_README.md) | **현재 앱 확장 가이드** | **실제로 app.py에 기능 추가하는 방법** ⭐ |

**총 소요 시간: 약 8-9시간**

## 🚀 빠른 시작

### 1. 첫 번째 예제 실행

```bash
cd streamlit_study
streamlit run 01_basic_setup.py
```

브라우저에서 `http://localhost:8501`이 자동으로 열립니다.

### 2. 순서대로 학습

각 예제는 독립적으로 실행 가능하며, 번호 순서대로 학습하는 것을 권장합니다.

```bash
# 예제 01
streamlit run 01_basic_setup.py

# 예제 02
streamlit run 02_layout_columns.py

# ... 계속
```

### 3. README 참고

각 예제마다 `XX_README.md` 파일이 있습니다:
- 학습 목표
- 핵심 개념
- 현재 앱에서의 사용 예시
- 실습 과제

## 🔧 현재 앱 구조 매핑

| 현재 앱 파일 | 관련 예제 | 핵심 개념 |
|--------------|-----------|----------|
| `app.py` | 12 | 전체 구조 |
| `app.py:15-20` | 01 | 페이지 설정 |
| `app.py:23-136` | 02, 03, 05, 06 | 데이터 탭 렌더링 |
| `app.py:147-157` | 06 | 탭 구조 |
| `app.py:187-349` | 04, 11 | 교차 분석 |
| `utils/loader.py` | 03, 14 | 캐싱, 데이터셋 추가 |
| `utils/visualizer.py` | 09, 10 | 차트/지도 |
| `utils/geo.py` | 10 | 지리 계산 |
| **기능 추가** | **14** | **새 탭/기능 추가 방법** |

## 💡 학습 팁

### 실행하면서 학습

```bash
# 포트 변경 (여러 앱 동시 실행)
streamlit run 01_basic_setup.py --server.port 8502
```

### 코드 수정 실험

각 예제의 코드를 직접 수정하면서 학습하세요:
- 색상 변경
- 텍스트 수정
- 새로운 위젯 추가
- 레이아웃 조정

### README 활용

각 예제의 README에는:
- 💡 핵심 개념
- 📝 코드 예시
- 🎯 실습 과제
- ⚠️ 주의사항

## 🐛 디버깅 가이드

### 일반적인 에러

**1. ModuleNotFoundError**
```bash
pip install streamlit pandas plotly folium streamlit-folium
```

**2. 포트 이미 사용 중**
```bash
streamlit run app.py --server.port 8502
```

**3. 캐시 문제**
- 앱 실행 중 `C` 키 누르기
- "Clear cache" 선택

**4. 파일 경로 에러**
- 절대 경로 사용
- `os.path.join()` 활용

### 도움말

```bash
streamlit --help
streamlit run --help
```

## 📅 일차별 정리

### 8일차: Streamlit 기초 (01-05)

| 파일 | 주제 | 핵심 학습 내용 |
|------|------|---------------|
| `01_basic_setup.py`, `01_README.md` | 기본 설정 및 텍스트 | `st.set_page_config()` 페이지 설정, `st.title/header/subheader` 텍스트 표시, 마크다운 문법 |
| `02_layout_columns.py`, `02_README.md` | 레이아웃과 컬럼 | `st.columns()` 화면 분할, `st.metric()` 핵심 지표 표시, 컬럼 비율 조정 |
| `03_data_display.py`, `03_README.md` | 데이터 표시 및 캐싱 | `st.dataframe()` vs `st.table()`, `@st.cache_data` 성능 최적화, 데이터프레임 스타일링 |
| `04_user_inputs.py`, `04_README.md` | 사용자 입력 위젯 | `st.selectbox()` 단일 선택, `st.multiselect()` 다중 선택, 폼(form) 입력 처리 |
| `05_expanders.py`, `05_README.md` | 확장 가능한 섹션 | `st.expander()` 컨텐츠 정리, 기본 확장 상태 설정, FAQ/상세 정보 표시 활용 |

### 9일차: Streamlit 중급 (06)

| 파일 | 주제 | 핵심 학습 내용 |
|------|------|---------------|
| `06_tabs.py`, `06_README.md` | 탭 네비게이션 | `st.tabs()` 탭 기반 네비게이션, 각 탭에 서로 다른 컨텐츠 표시, 동적 탭 생성 |

### 10일차: Streamlit 중급~고급 (예정)

| 파일 | 주제 | 핵심 학습 내용 |
|------|------|---------------|
| `07_status_messages.py`, `07_README.md` | 상태 메시지 | `st.success/warning/error/info` 4가지 상태 메시지 구분 |
| `08_spinner.py`, `08_README.md` | 로딩 스피너 | `st.spinner()` 로딩 중 UX 개선 |
| `09_plotly_charts.py`, `09_README.md` | Plotly 차트 | 다양한 차트 유형 (bar, line, scatter, pie, histogram) |
| `10_folium_maps.py`, `10_README.md` | Folium 지도 | `folium.Map`, `MarkerCluster`, 지도 시각화 |

---

## 📊 학습 체크리스트

기초 과정 (01-05):
- [x] 01: st.set_page_config 이해
- [x] 02: st.columns와 st.metric 사용
- [x] 03: @st.cache_data 이해
- [x] 04: st.selectbox, st.multiselect 사용
- [x] 05: st.expander로 UI 정리

중급 과정 (06-08):
- [x] 06: st.tabs로 페이지 구조화
- [x] 07: 4가지 상태 메시지 구분
- [x] 08: st.spinner로 UX 개선

고급 과정 (09-12):
- [x] 09: Plotly 차트 5가지 이상
- [x] 10: Folium 지도에 마커 추가
- [x] 11: 필터링 + 탭 + 차트 + 지도 통합
- [x] 12: 현재 앱 구조 완전 이해

실전 과정 (13-14):
- [x] 13: Session State로 상태 관리
- [x] 13: 파일 업로드/다운로드 구현
- [x] 14: 새 탭 추가 시나리오 따라하기
- [x] 14: 기존 기능 확장 시나리오 따라하기
- [x] 14: 새 데이터셋 추가 시나리오 따라하기

## 🎓 다음 단계

모든 예제를 완료했다면:

1. **현재 앱 분석**
   ```bash
   cd ..
   streamlit run app.py
   ```

2. **코드 읽기**
   - `app.py` 전체
   - `utils/` 디렉토리 각 파일

3. **기능 추가**
   - 새로운 메트릭
   - 다른 차트 유형
   - 필터 옵션

4. **최적화**
   - 성능 개선
   - UI/UX 개선
   - 에러 처리 강화

## 📚 추가 자료

- [Streamlit 공식 문서](https://docs.streamlit.io)
- [Streamlit API Reference](https://docs.streamlit.io/library/api-reference)
- [Plotly Python](https://plotly.com/python/)
- [Folium 문서](https://python-visualization.github.io/folium/)
---

**즐거운 학습 되세요! 🚀**

궁금한 점이 있으면 각 예제의 README를 참고하거나,
Streamlit 공식 문서를 확인하세요.
