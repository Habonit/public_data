"""
예제 11: 고급 통합 (Advanced Integration)

이 예제에서는 Pandas, Plotly, Folium을 통합하여 복잡한 데이터 분석 앱을 만듭니다.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

st.set_page_config(
    page_title="고급 통합",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 고급 통합: 완전한 데이터 분석 앱")

st.markdown("""
이 예제에서는 지금까지 배운 모든 것을 통합하여
실제 사용 가능한 데이터 분석 앱을 만듭니다.
""")

# ============================================
# 데이터 생성
# ============================================
@st.cache_data
def load_sample_data():
    np.random.seed(42)
    dates = pd.date_range('2024-01-01', periods=100)

    df = pd.DataFrame({
        '날짜': dates,
        '지점명': np.random.choice(['강남점', '서초점', '역삼점'], 100),
        '위도': np.random.uniform(35.8, 35.9, 100),
        '경도': np.random.uniform(128.5, 128.7, 100),
        '매출': np.random.randint(500000, 2000000, 100),
        '방문자': np.random.randint(50, 200, 100),
        '제품군': np.random.choice(['전자제품', '의류', '식품'], 100)
    })

    # 전환율 계산
    df['전환율'] = (df['매출'] / df['방문자'] / 10000 * 100).round(2)

    # 날짜 컬럼 명시적 datetime 변환 (Arrow 호환성)
    df['날짜'] = pd.to_datetime(df['날짜'])

    return df

df = load_sample_data()
st.dataframe(df)

# ============================================
# 사이드바: 필터
# ============================================
st.sidebar.header("🎛️ 필터")

# 날짜 범위
date_range = st.sidebar.date_input(
    "날짜 범위:",
    value=(df['날짜'].min(), df['날짜'].max())
)

# 지점 선택
selected_branches = st.sidebar.multiselect(
    "지점:",
    options=df['지점명'].unique(),
    default=df['지점명'].unique()
)

# 제품군 선택
selected_products = st.sidebar.multiselect(
    "제품군:",
    options=df['제품군'].unique(),
    default=df['제품군'].unique()
)

# 매출 범위
sales_range = st.sidebar.slider(
    "매출 범위 (만원):",
    min_value=int(df['매출'].min() / 10000),
    max_value=int(df['매출'].max() / 10000),
    value=(int(df['매출'].min() / 10000), int(df['매출'].max() / 10000))
)

# 필터 적용
if len(date_range) == 2:
    filtered_df = df[
        (df['날짜'] >= pd.to_datetime(date_range[0])) &
        (df['날짜'] <= pd.to_datetime(date_range[1])) &
        (df['지점명'].isin(selected_branches)) &
        (df['제품군'].isin(selected_products)) &
        (df['매출'] >= sales_range[0] * 10000) &
        (df['매출'] <= sales_range[1] * 10000)
    ]
else:
    filtered_df = df[
        (df['지점명'].isin(selected_branches)) &
        (df['제품군'].isin(selected_products))
    ]

st.sidebar.markdown("---")
st.sidebar.info(f"📊 필터링된 데이터: {len(filtered_df)}개 행")

# ============================================
# 메인: 탭 구성
# ============================================
tab_overview, tab_analysis, tab_map, tab_data = st.tabs([
    "📊 개요",
    "📈 분석",
    "🗺️ 지도",
    "📋 데이터"
])

# ============================================
# 탭 1: 개요
# ============================================
with tab_overview:
    st.header("📊 주요 지표")

    # 메트릭
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_sales = filtered_df['매출'].sum()
        avg_sales_change = ((filtered_df['매출'].tail(10).mean() /
                           filtered_df['매출'].head(10).mean() - 1) * 100)
        st.metric(
            "총 매출",
            f"₩{total_sales:,.0f}",
            f"{avg_sales_change:+.1f}%"
        )

    with col2:
        total_visitors = filtered_df['방문자'].sum()
        st.metric(
            "총 방문자",
            f"{total_visitors:,}명"
        )

    with col3:
        avg_conversion = filtered_df['전환율'].mean()
        st.metric(
            "평균 전환율",
            f"{avg_conversion:.2f}%"
        )

    with col4:
        num_records = len(filtered_df)
        st.metric(
            "데이터 건수",
            f"{num_records:,}건"
        )

    st.markdown("---")

    # 시계열 차트
    st.subheader("📈 일별 매출 추이")

    # 이거랑 똑같이 할 거라면
    daily_sales = filtered_df.groupby('날짜').agg({'매출': 'sum'}).reset_index()
    # daily_sales = filtered_df.groupby('날짜')['매출'].sum().reset_index()

    fig = px.line(
        daily_sales,
        x='날짜',
        y='매출',
        title='일별 총 매출',
        labels={'매출': '매출 (원)'}
    )
    fig.update_traces(line_color='#FF6B6B', line_width=3)
    st.plotly_chart(fig, width="stretch")

    # 2컬럼 차트
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("지점별 매출")
        branch_sales = filtered_df.groupby('지점명')['매출'].sum().reset_index()
        fig = px.bar(
            branch_sales,
            x='지점명',
            y='매출',
            color='매출',
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig, width="stretch")

    with col2:
        st.subheader("제품군별 매출")
        product_sales = filtered_df.groupby('제품군')['매출'].sum().reset_index()
        fig = px.pie(
            product_sales,
            values='매출',
            names='제품군',
            hole=0.4
        )
        st.plotly_chart(fig, width="stretch")

# ============================================
# 탭 2: 분석
# ============================================
with tab_analysis:
    st.header("📈 상세 분석")

    # 분석 유형 선택
    analysis_type = st.selectbox(
        "분석 유형 선택:",
        ["상관 관계", "시계열 분해", "지점 비교"]
    )

    if analysis_type == "상관 관계":
        st.subheader("변수 간 상관관계")

        fig = px.scatter(
            filtered_df,
            x='방문자',
            y='매출',
            color='지점명',
            size='전환율',
            hover_data=['날짜', '제품군'],
            title='방문자 vs 매출 (지점별)'
        )
        st.plotly_chart(fig, width="stretch")

        # 상관계수
        corr = filtered_df[['매출', '방문자', '전환율']].corr()
        st.write("### 상관계수 행렬")
        st.dataframe(corr.style.background_gradient(cmap='coolwarm'),
                    width="stretch")

    elif analysis_type == "시계열 분해":
        st.subheader("시계열 트렌드 분석")

        # 일별 집계
        daily = filtered_df.groupby('날짜')['매출'].sum().reset_index()

        # 이동 평균
        daily['MA7'] = daily['매출'].rolling(window=7).mean()
        daily['MA14'] = daily['매출'].rolling(window=14).mean()

        fig = px.line(
            daily,
            x='날짜',
            y=['매출', 'MA7', 'MA14'],
            title='매출 및 이동평균 (7일, 14일)',
            labels={'value': '매출 (원)', 'variable': '지표'}
        )
        st.plotly_chart(fig, width="stretch")

    else:  # 지점 비교
        st.subheader("지점별 비교 분석")

        # 지점별 일별 매출
        branch_daily = filtered_df.groupby(['날짜', '지점명'])['매출'].sum().reset_index()

        fig = px.line(
            branch_daily,
            x='날짜',
            y='매출',
            color='지점명',
            title='지점별 일별 매출'
        )
        st.plotly_chart(fig, width="stretch")

        # 박스 플롯
        fig = px.box(
            filtered_df,
            x='지점명',
            y='매출',
            color='지점명',
            title='지점별 매출 분포'
        )
        st.plotly_chart(fig, width="stretch")

# ============================================
# 탭 3: 지도
# ============================================
with tab_map:
    st.header("🗺️ 지리적 분포")

    # 지점별 집계
    branch_agg = filtered_df.groupby('지점명').agg({
        '위도': 'mean',
        '경도': 'mean',
        '매출': 'sum',
        '방문자': 'sum'
    }).reset_index()

    # 지도 중심
    center_lat = branch_agg['위도'].mean()
    center_lng = branch_agg['경도'].mean()

    # 지도 생성
    m = folium.Map(location=[center_lat, center_lng], zoom_start=12)

    # 마커 추가
    for idx, row in branch_agg.iterrows():
        # 크기를 매출에 비례
        radius = (row['매출'] / branch_agg['매출'].max()) * 30 + 10

        popup_html = f"""
        <div style='width: 250px'>
            <h4>{row['지점명']}</h4>
            <b>총 매출:</b> ₩{row['매출']:,.0f}<br>
            <b>총 방문자:</b> {row['방문자']:,}명<br>
            <b>평균 객단가:</b> ₩{row['매출']/row['방문자']:,.0f}
        </div>
        """

        folium.CircleMarker(
            location=[row['위도'], row['경도']],
            radius=radius,
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=row['지점명'],
            color='red',
            fill=True,
            fillColor='red',
            fillOpacity=0.6
        ).add_to(m)

    st_folium(m, width=900, height=600)

    # 지점 통계
    st.subheader("지점별 통계")
    st.dataframe(branch_agg.style.format({
        '매출': '₩{:,.0f}',
        '방문자': '{:,.0f}명',
        '위도': '{:.4f}',
        '경도': '{:.4f}'
    }), width="stretch")

# ============================================
# 탭 4: 데이터
# ============================================
with tab_data:
    st.header("📋 원본 데이터")

    # 데이터 표시 옵션
    col1, col2 = st.columns(2)

    with col1:
        show_all = st.checkbox("전체 데이터 표시", value=False)

    with col2:
        if st.button("CSV 다운로드"):
            csv = filtered_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="다운로드",
                data=csv,
                file_name='filtered_data.csv',
                mime='text/csv'
            )

    # 데이터 표시
    if show_all:
        st.dataframe(filtered_df, width="stretch")
    else:
        st.dataframe(filtered_df.head(50), width="stretch")
        st.info(f"처음 50개 행만 표시 중 (전체: {len(filtered_df)}개)")

    # 기술 통계
    with st.expander("📊 기술 통계"):
        st.dataframe(filtered_df.describe(), width="stretch")

# ============================================
# 실습 섹션
# ============================================
st.markdown("---")
st.header("🎯 실습해보세요!")

st.markdown("""
1. 사이드바 필터를 조작하여 데이터 변화 관찰
2. 각 탭의 기능을 탐색하고 인사이트 찾기
3. 이 구조를 기반으로 자신만의 분석 앱 만들기
4. 실제 CSV 데이터를 로드하여 적용해보기
""")

# ============================================
# 추가 지식: st.query_params (URL 파라미터)
# ============================================
st.markdown("---")
st.header("📚 알아두면 좋은 기능: URL 파라미터")

st.markdown("""
### 🔗 st.query_params란?

Streamlit 앱의 URL에 파라미터를 추가하여 **앱의 상태를 공유**할 수 있습니다.
예를 들어, 특정 필터가 적용된 상태를 동료에게 링크로 공유할 수 있습니다.

**사용 예시:**
```
http://localhost:8501/?branch=강남점&product=전자제품
```

### 왜 중요한가요?
- 📤 **공유 용이**: 필터가 적용된 상태를 URL로 공유
- 🔖 **북마크 가능**: 자주 보는 뷰를 저장
- 🔄 **새로고침 유지**: 페이지 새로고침해도 상태 유지
""")

# 실제 구현 예시
st.subheader("💻 구현 예시")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**현재 URL 파라미터 읽기:**")
    st.code("""
# URL에서 파라미터 읽기
params = st.query_params

# 특정 파라미터 가져오기 (기본값 설정)
branch = params.get("branch", "전체")
product = params.get("product", "전체")

st.write(f"지점: {branch}, 제품군: {product}")
""", language="python")

with col2:
    st.markdown("**URL 파라미터 설정하기:**")
    st.code("""
# URL 파라미터 설정
st.query_params["branch"] = "강남점"
st.query_params["product"] = "전자제품"

# 여러 파라미터 한번에 설정
st.query_params.from_dict({
    "branch": "강남점",
    "product": "전자제품",
    "date": "2024-01-01"
})

# 파라미터 삭제
del st.query_params["branch"]

# 모든 파라미터 삭제
st.query_params.clear()
""", language="python")

# 실제 동작 데모
st.subheader("🎮 직접 체험해보기")

# 현재 URL 파라미터 표시
current_params = dict(st.query_params)
if current_params:
    st.info(f"📍 현재 URL 파라미터: {current_params}")
else:
    st.info("📍 현재 URL 파라미터가 없습니다.")

# 파라미터 설정 UI
demo_col1, demo_col2, demo_col3 = st.columns(3)

with demo_col1:
    demo_branch = st.selectbox(
        "지점 선택 (URL에 저장):",
        options=["선택안함", "강남점", "서초점", "역삼점"],
        key="demo_branch"
    )

with demo_col2:
    demo_product = st.selectbox(
        "제품군 선택 (URL에 저장):",
        options=["선택안함", "전자제품", "의류", "식품"],
        key="demo_product"
    )

with demo_col3:
    st.write("")  # 공백
    st.write("")  # 정렬용
    if st.button("🔗 URL에 저장"):
        if demo_branch != "선택안함":
            st.query_params["branch"] = demo_branch
        if demo_product != "선택안함":
            st.query_params["product"] = demo_product
        st.success("URL이 업데이트되었습니다! 브라우저 주소창을 확인하세요.")

    if st.button("🗑️ URL 파라미터 초기화"):
        st.query_params.clear()
        st.success("URL 파라미터가 초기화되었습니다!")

# URL 파라미터로 필터 적용 예시
st.subheader("📊 URL 파라미터로 필터 적용 예시")

st.markdown("""
아래 코드를 사이드바 필터에 적용하면, URL 파라미터로 필터 상태를 공유할 수 있습니다:
""")

st.code("""
# 사이드바 필터 with URL 파라미터
# URL에서 기본값 읽기
default_branch = st.query_params.get("branch", None)
default_product = st.query_params.get("product", None)

# 지점 선택 (URL 파라미터가 있으면 해당 값을 기본값으로)
all_branches = df['지점명'].unique().tolist()
if default_branch and default_branch in all_branches:
    default_idx = all_branches.index(default_branch)
else:
    default_idx = 0

selected_branch = st.sidebar.selectbox(
    "지점:",
    options=all_branches,
    index=default_idx
)

# 선택이 바뀌면 URL 업데이트
if selected_branch:
    st.query_params["branch"] = selected_branch
""", language="python")

# 실습 과제
st.subheader("✏️ 실습 과제")

st.markdown("""
1. **기본 실습**: 위의 "직접 체험해보기"에서 지점과 제품군을 선택하고 URL에 저장해보세요.
   브라우저 주소창에서 파라미터가 추가되는 것을 확인하세요.

2. **응용 실습**: 이 앱의 사이드바 필터에 URL 파라미터 기능을 추가해보세요.
   - 힌트: `st.query_params.get()`으로 기본값 설정
   - 힌트: 필터 변경 시 `st.query_params["key"] = value`로 URL 업데이트

3. **심화 실습**: 날짜 범위도 URL 파라미터로 저장/복원해보세요.
   - 힌트: 날짜는 문자열로 변환 필요 (`str(date)`)
""")

with st.expander("💡 정답 예시 보기"):
    st.code("""
# 사이드바에 URL 파라미터 통합 예시

# URL에서 파라미터 읽기
params = st.query_params
url_branch = params.get("branch", None)
url_product = params.get("product", None)

# 지점 필터 (URL 파라미터 반영)
all_branches = df['지점명'].unique().tolist()
default_branches = [url_branch] if url_branch in all_branches else all_branches

selected_branches = st.sidebar.multiselect(
    "지점:",
    options=all_branches,
    default=default_branches
)

# URL 업데이트 (첫 번째 선택된 지점만 저장)
if selected_branches:
    st.query_params["branch"] = selected_branches[0]
elif "branch" in st.query_params:
    del st.query_params["branch"]
""", language="python")
