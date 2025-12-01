# 예제 12: 완전한 대시보드

## 학습 목표

이 예제는 **현재 앱(app.py)의 모든 핵심 패턴을 통합**한 완전한 대시보드입니다.

- 현재 앱의 구조 이해
- 재사용 가능한 컴포넌트 패턴
- 전체 워크플로우 파악

## 핵심 패턴

### 1. 재사용 가능한 렌더링 함수

```python
def render_dataset_tab(dataset_name, display_name):
    """각 데이터셋 탭을 렌더링하는 재사용 함수"""
    df = load_dataset(dataset_name)
    # 메트릭, 차트, 지도 표시
```

이 패턴은 현재 앱에서 7개 데이터셋에 동일하게 적용됩니다.

### 2. 정보 추출 함수

```python
def get_dataset_info(df):
    """데이터셋의 메타 정보 추출"""
    return {
        'row_count': len(df),
        'column_count': len(df.columns),
        'dtypes': {...},
        'missing_ratios': {...}
    }
```

### 3. 탭 기반 구조

```python
tabs = st.tabs(["탭1", "탭2", "탭3"])

with tabs[0]:
    render_dataset_tab('dataset1', '데이터셋 1')

with tabs[1]:
    render_dataset_tab('dataset2', '데이터셋 2')
```

## 현재 앱(app.py)과의 대응

| 현재 앱 | 이 예제 | 설명 |
|---------|---------|------|
| `app.py:23-42` | `render_dataset_tab()` | 개별 데이터셋 렌더링 |
| `app.py:44-77` | 메트릭 + expander | 데이터 정보 표시 |
| `app.py:147-157` | `st.tabs()` | 탭 네비게이션 |
| `app.py:187-349` | 교차 분석 탭 | 다중 데이터셋 분석 |
| `utils/loader.py:43` | `@st.cache_data` | 데이터 캐싱 |
| `utils/visualizer.py` | Plotly/Folium | 시각화 |

## 실행 방법

```bash
streamlit run 12_complete_dashboard.py
```

## 학습 순서

1. **이 예제 실행** → 전체 구조 파악
2. **현재 앱 실행** → 실제 동작 확인
3. **코드 비교** → 패턴 이해
4. **수정 및 실험** → 직접 개선

## 다음 단계

이제 현재 앱(app.py)의 코드를 읽고 수정할 준비가 되었습니다!

1. `app.py` 전체 구조 파악
2. `utils/` 디렉토리 모듈 분석
3. 기능 추가 또는 개선
4. 디버깅 및 최적화
