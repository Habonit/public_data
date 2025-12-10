# 예제 6: 탭 네비게이션 (Tabs)

## 학습 목표

- `st.tabs()`를 사용한 탭 기반 네비게이션
- 각 탭에 서로 다른 컨텐츠 표시
- 동적 탭 생성

## 핵심 개념

### 기본 사용법

```python
tab1, tab2, tab3 = st.tabs(["첫 번째", "두 번째", "세 번째"])

with tab1:
    st.write("탭 1의 내용")

with tab2:
    st.write("탭 2의 내용")

with tab3:
    st.write("탭 3의 내용")
```

## 현재 앱에서의 사용

```python
# app.py:147-157
tabs = st.tabs([
    "🎥 CCTV",
    "💡 보안등",
    "🏫 어린이 보호구역",
    "🅿️ 주차장",
    "🚗 사고",
    "🚂 기차",
    "📝 테스트",
    "🔄 교차 데이터 분석",
    "📖 프로젝트 개요"
])

with tabs[0]:
    render_dataset_tab('cctv', 'CCTV')
# ... 각 탭마다 다른 컨텐츠
```

## 실행 방법

```bash
streamlit run 06_tabs.py
```
