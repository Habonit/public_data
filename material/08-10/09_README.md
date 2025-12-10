# 예제 9: Plotly 차트 통합

## 학습 목표
- Plotly Express를 사용한 빠른 차트 생성
- 다양한 차트 유형 (라인, 막대, 산점도, 파이 등)
- 인터랙티브 기능 활용

## 주요 차트 유형

```python
import plotly.express as px

# 라인 차트
fig = px.line(df, x='x', y='y', title='제목')

# 막대 차트
fig = px.bar(df, x='x', y='y')

# 산점도
fig = px.scatter(df, x='x', y='y', color='category')

# 히스토그램
fig = px.histogram(df, x='value', marginal='box')

# 표시
st.plotly_chart(fig, use_container_width=True)
```

## 현재 앱에서의 사용

```python
# utils/visualizer.py:34-40 - 히스토그램
fig = px.histogram(
    df.dropna(subset=[column]),
    x=column,
    title=title,
    marginal="box"
)

# utils/visualizer.py:76-81 - 막대 차트
fig = px.bar(
    x=value_counts.index,
    y=value_counts.values,
    title=title
)
```

## 실행 방법

```bash
streamlit run 09_plotly_charts.py
```
