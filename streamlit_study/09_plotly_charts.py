"""
예제 9: Plotly 차트 통합 (Plotly Charts)

이 예제에서는 Plotly를 사용한 인터랙티브 차트를 학습합니다.
"""
from tkinter import HORIZONTAL
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
# streamlit이 plotly라는 시각화 툴과 호환이 되는 상황

st.set_page_config(
    page_title="Plotly 차트",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Plotly 차트 통합")

st.markdown("""
Plotly는 인터랙티브한 차트를 만들 수 있는 강력한 라이브러리입니다.
줌, 팬, 호버 등 다양한 상호작용이 가능합니다.
""")

# 샘플 데이터 생성
# 데이터를 다루는 함수에서는 cache_data를 써주시면 좋아요 
# return하는 데이터가 변경되는가 변경되지 않는가. 
@st.cache_data
def create_sample_data():
    dates = pd.date_range('2024-01-01', periods=100)
    df = pd.DataFrame({
        '날짜': dates,
        '매출': np.random.randint(1000, 5000, 100) + np.arange(100) * 20,
        '방문자': np.random.randint(100, 500, 100) + np.arange(100) * 3,
        '전환율': np.random.uniform(2, 5, 100),
        '카테고리': np.random.choice(['A', 'B', 'C'], 100)
    })
    return df

df = create_sample_data()
st.dataframe(df)
# ============================================
# 1. 라인 차트 (Line Chart)
# ============================================
st.header("1. 라인 차트")

col1, col2 = st.columns(2)

with col1:
    st.subheader("기본 라인 차트")
    fig = px.line(df, x='날짜', y='매출', title='일별 매출 추이')
    st.plotly_chart(fig, width="stretch")

# hue가 2개 있다고 하는데요
with col2:
    st.subheader("여러 라인")
    fig = px.line(df, x='날짜', y=['매출', '방문자'], title='매출 vs 방문자')
    st.plotly_chart(fig, width="stretch")

# ============================================
# 2. 막대 차트 (Bar Chart)
# ============================================
st.header("2. 막대 차트")

# 카테고리별 평균
category_data = df.groupby('카테고리').agg({
    '매출': 'mean',
    '방문자': 'sum'
}).reset_index()

st.dataframe(category_data)

col1, col2 = st.columns(2)

with col1:
    st.subheader("기본 막대 차트")
    fig = px.bar(category_data, x='카테고리', y='매출', title='카테고리별 평균 매출')
    st.plotly_chart(fig, width="stretch")

with col2:
    st.subheader("그룹화된 막대 차트")
    fig = px.bar(category_data, x='카테고리', y=['매출', '방문자'],
                 title='카테고리별 매출 및 방문자', barmode='group')
    st.plotly_chart(fig, width="stretch")

# ============================================
# 3. 히스토그램 (Histogram)
# ============================================
st.header("3. 히스토그램")

selected_column = st.selectbox("분포를 볼 컬럼 선택:", ['매출', '방문자', '전환율'])

fig = px.histogram(df, x=selected_column, title=f'{selected_column} 분포',
                   marginal='box')  # 상단에 박스 플롯 추가
st.plotly_chart(fig, width="stretch")

# ============================================
# 4. 산점도 (Scatter Plot)
# ============================================
st.header("4. 산점도")

fig = px.scatter(df, x='방문자', y='매출', color='카테고리',
                size='전환율', hover_data=['날짜'],
                title='방문자 vs 매출 (카테고리별)')
st.plotly_chart(fig, width="stretch")

# ============================================
# 5. 파이 차트 (Pie Chart)
# ============================================
st.header("5. 파이 차트")

col1, col2 = st.columns(2)

with col1:
    st.subheader("카테고리별 매출 비중")
    pie_data = df.groupby('카테고리')['매출'].sum().reset_index()
    fig = px.pie(pie_data, values='매출', names='카테고리',
                title='카테고리별 매출 비중')
    st.plotly_chart(fig, width="stretch")

# seaborn 이걸 explode
# plotly에서는 이걸 hole 
with col2:
    st.subheader("도넛 차트")
    fig = px.pie(pie_data, values='매출', names='카테고리',
                title='카테고리별 매출 비중', hole=0.4)  # hole로 도넛 모양
    st.plotly_chart(fig, width="stretch")

# ============================================
# 6. 박스 플롯 (Box Plot)
# ============================================
st.header("6. 박스 플롯")

fig = px.box(df, x='카테고리', y='매출', title='카테고리별 매출 분포')
st.plotly_chart(fig, width="stretch")

# ============================================
# 7. 시계열 차트 (Time Series)
# ============================================
st.header("7. 고급 시계열 차트")

# Plotly Graph Objects 사용
fig = go.Figure()

fig.add_trace(go.Scatter(x=df['날짜'], y=df['매출'],
                        mode='lines+markers', name='매출',
                        line=dict(color='#FF6B6B', width=2)))

fig.add_trace(go.Scatter(x=df['날짜'], y=df['방문자'],
                        mode='lines+markers', name='방문자',
                        line=dict(color='#4ECDC4', width=2),
                        yaxis='y2'))  # 두 번째 y축 사용

# 레이아웃 설정
fig.update_layout(
    title='매출 및 방문자 추이 (이중 축)',
    xaxis=dict(title='날짜'),
    yaxis=dict(title='매출', side='left'),
    yaxis2=dict(title='방문자', side='right', overlaying='y'),
    hovermode='x unified'
)

st.plotly_chart(fig, width="stretch")

# ============================================
# 8. 인터랙티브 대시보드
# ============================================
st.header("8. 실전 예제: 인터랙티브 대시보드")

st.markdown("---")

# 필터
col1, col2 = st.columns(2)

with col1:
    selected_category = st.multiselect(
        "카테고리 선택:",
        options=df['카테고리'].unique(),
        default=df['카테고리'].unique()
    )

with col2:
    date_range = st.date_input(
        "기간 선택:",
        value=(df['날짜'].min(), df['날짜'].max())
    )

# 필터 적용
if len(date_range) == 2:
    filtered_df = df[
        (df['카테고리'].isin(selected_category)) &
        (df['날짜'] >= pd.to_datetime(date_range[0])) &
        (df['날짜'] <= pd.to_datetime(date_range[1]))
    ]
else:
    filtered_df = df[df['카테고리'].isin(selected_category)]

st.dataframe(filtered_df)
# 메트릭
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("총 매출", f"₩{filtered_df['매출'].sum():,.0f}")
with col2:
    st.metric("평균 매출", f"₩{filtered_df['매출'].mean():,.0f}")
with col3:
    st.metric("총 방문자", f"{filtered_df['방문자'].sum():,}명")
with col4:
    st.metric("평균 전환율", f"{filtered_df['전환율'].mean():.2f}%")

# 차트
col1, col2 = st.columns(2)

with col1:
    fig = px.line(filtered_df, x='날짜', y='매출', color='카테고리',
                 title='카테고리별 매출 추이')
    st.plotly_chart(fig, width="stretch")

with col2:
    fig = px.bar(filtered_df.groupby('카테고리')['매출'].sum().reset_index(),
                x='카테고리', y='매출', title='카테고리별 총 매출')
    st.plotly_chart(fig, width="stretch")

st.dataframe(filtered_df.groupby('카테고리').agg({"매출":"mean"}))

# ============================================
# 실습 섹션
# ============================================
st.markdown("---")
st.header("🎯 실습해보세요!")

st.markdown("""
1. 다양한 차트 유형을 조합하여 대시보드 만들기
2. Plotly의 인터랙티브 기능 (줌, 팬, 호버) 탐색
3. 사용자 입력에 따라 동적으로 차트 업데이트
4. 현재 앱(app.py)의 차트 코드 분석 및 개선
""")

with st.expander("💡 Plotly 사용 팁"):
    st.markdown("""
    **Express vs Graph Objects:**
    - `plotly.express`: 간단하고 빠르게, 대부분의 경우 사용
    - `plotly.graph_objects`: 세밀한 제어가 필요할 때

    **유용한 매개변수:**
    - `width="stretch"`: 전체 너비 사용
    - `title`: 차트 제목
    - `color`: 색상으로 구분
    - `size`: 크기로 구분
    - `hover_data`: 호버 시 추가 정보

    **스타일링:**
    - `fig.update_layout()`: 전체 레이아웃 수정
    - `fig.update_traces()`: 특정 트레이스 수정
    - `fig.update_xaxes()`, `fig.update_yaxes()`: 축 수정
    """)

# ============================================
# 실습과제 구현
# ============================================
st.markdown("---")
st.header("📝 실습과제 구현")

# 1. 다양한 차트 유형 조합 대시보드
st.subheader("1. 다양한 차트 조합 대시보드")

col1, col2 = st.columns(2)

with col1:
    # 라인 차트
    fig_line = px.line(df, x='날짜', y='매출', title='매출 추이')
    st.plotly_chart(fig_line, width="stretch")

with col2:
    # 파이 차트
    pie_df = df.groupby('카테고리')['매출'].sum().reset_index()
    fig_pie = px.pie(pie_df, values='매출', names='카테고리', title='카테고리별 매출')
    st.plotly_chart(fig_pie, width="stretch")

# 2. 사용자 입력에 따른 동적 차트
st.subheader("2. 사용자 입력 기반 동적 차트")

chart_type = st.radio("차트 유형 선택:", ['라인', '막대', '산점도'], horizontal=True)

if chart_type == '라인':
    fig = px.line(df, x='날짜', y='매출')
elif chart_type == '막대':
    fig = px.bar(df.groupby('카테고리')['매출'].mean().reset_index(), x='카테고리', y='매출')
else:
    fig = px.scatter(df, x='방문자', y='매출', color='카테고리')

st.plotly_chart(fig, width="stretch")
