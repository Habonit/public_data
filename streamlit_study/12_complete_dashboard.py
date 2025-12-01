"""
예제 12: 완전한 대시보드 (Complete Dashboard)

현재 앱(app.py)의 핵심 패턴을 모두 적용한 실전 대시보드입니다.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

st.set_page_config(
    page_title="완전한 대시보드",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# 데이터 로딩 (캐싱 적용)
# ============================================
@st.cache_data
def load_dataset(dataset_name):
    """데이터셋 로딩 (캐싱)"""
    np.random.seed(42)

    if dataset_name == 'sales':
        return pd.DataFrame({
            '날짜': pd.date_range('2024-01-01', periods=200),
            '지점': np.random.choice(['강남', '서초', '역삼', '논현'], 200),
            '카테고리': np.random.choice(['전자', '의류', '식품'], 200),
            '매출': np.random.randint(500000, 3000000, 200),
            '수량': np.random.randint(10, 100, 200),
            '위도': np.random.uniform(35.85, 35.90, 200),
            '경도': np.random.uniform(128.55, 128.65, 200)
        })
    else:  # 'traffic'
        return pd.DataFrame({
            '날짜': pd.date_range('2024-01-01', periods=200),
            '지점': np.random.choice(['강남', '서초', '역삼', '논현'], 200),
            '방문자': np.random.randint(100, 500, 200),
            '체류시간': np.random.randint(10, 60, 200),
            '위도': np.random.uniform(35.85, 35.90, 200),
            '경도': np.random.uniform(128.55, 128.65, 200)
        })

def get_dataset_info(df):
    """데이터셋 정보 생성"""
    return {
        'row_count': len(df),
        'column_count': len(df.columns),
        'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
        'missing_ratios': {col: df[col].isnull().sum() / len(df) for col in df.columns},
        'numeric_summary': df.select_dtypes(include=['number']).describe()
    }

# ============================================
# 메인 앱
# ============================================
def main():
    st.title("🎯 완전한 데이터 대시보드")

    st.markdown("""
    이 대시보드는 현재 앱(app.py)의 모든 핵심 패턴을 포함합니다:
    - 페이지 설정 및 레이아웃
    - 탭 기반 네비게이션
    - 데이터 캐싱
    - 인터랙티브 차트 (Plotly)
    - 지도 시각화 (Folium)
    - 상태 메시지 및 스피너
    """)

    # ============================================
    # 탭 구성 (현재 앱과 동일한 패턴)
    # ============================================
    tabs = st.tabs([
        "📊 매출 데이터",
        "👥 방문 데이터",
        "🔄 교차 분석",
        "📖 가이드"
    ])

    # ==================== 탭 1: 매출 데이터 ====================
    with tabs[0]:
        render_dataset_tab('sales', '매출')

    # ==================== 탭 2: 방문 데이터 ====================
    with tabs[1]:
        render_dataset_tab('traffic', '방문')

    # ==================== 탭 3: 교차 분석 ====================
    with tabs[2]:
        st.header("🔄 교차 데이터 분석")

        st.markdown("""
        여러 데이터셋을 동시에 분석하여 인사이트를 발견합니다.
        """)

        # 데이터셋 선택
        selected_datasets = st.multiselect(
            "분석할 데이터셋 선택:",
            options=['매출', '방문'],
            default=['매출', '방문']
        )

        if len(selected_datasets) == 0:
            st.warning("⚠️ 최소 1개 이상의 데이터셋을 선택해주세요.")
        else:
            # 데이터 로딩
            datasets = []

            with st.spinner("데이터셋 로딩 중..."):
                if '매출' in selected_datasets:
                    datasets.append({
                        'name': '매출',
                        'df': load_dataset('sales'),
                        'color': 'red'
                    })
                if '방문' in selected_datasets:
                    datasets.append({
                        'name': '방문',
                        'df': load_dataset('traffic'),
                        'color': 'blue'
                    })

            # 통합 지도
            st.subheader("🗺️ 통합 지도")

            # 범례
            legend_cols = st.columns(len(datasets))
            for idx, ds in enumerate(datasets):
                with legend_cols[idx]:
                    st.markdown(f"🔵 **{ds['name']}** ({len(ds['df']):,}개)")

            # 지도 생성
            all_lats = []
            all_lngs = []

            for ds in datasets:
                all_lats.extend(ds['df']['위도'].tolist())
                all_lngs.extend(ds['df']['경도'].tolist())

            center_lat = sum(all_lats) / len(all_lats)
            center_lng = sum(all_lngs) / len(all_lngs)

            m = folium.Map(location=[center_lat, center_lng], zoom_start=12)

            # 각 데이터셋을 레이어로 추가
            for ds in datasets:
                feature_group = folium.FeatureGroup(name=ds['name'])

                for idx, row in ds['df'].head(100).iterrows():
                    folium.CircleMarker(
                        location=[row['위도'], row['경도']],
                        radius=5,
                        popup=f"{ds['name']}: {row['지점']}",
                        color=ds['color'],
                        fill=True,
                        fillColor=ds['color']
                    ).add_to(feature_group)

                feature_group.add_to(m)

            folium.LayerControl().add_to(m)

            st_folium(m, width=900, height=600)

            st.info("💡 지도 우측 상단의 레이어 컨트롤로 각 데이터셋을 개별적으로 확인할 수 있습니다.")

    # ==================== 탭 4: 가이드 ====================
    with tabs[3]:
        st.header("📖 사용 가이드")

        st.markdown("""
        ## 🎯 이 대시보드의 구조

        이 예제는 **현재 앱(app.py)의 핵심 패턴**을 모두 포함합니다:

        ### 1. 페이지 설정
        ```python
        st.set_page_config(
            page_title="...",
            page_icon="...",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        ```

        ### 2. 데이터 캐싱
        ```python
        @st.cache_data
        def load_dataset(dataset_name):
            # 데이터 로딩 로직
            return df
        ```

        ### 3. 탭 기반 구조
        ```python
        tabs = st.tabs(["탭1", "탭2", "탭3"])

        with tabs[0]:
            # 탭1 컨텐츠

        with tabs[1]:
            # 탭2 컨텐츠
        ```

        ### 4. 재사용 가능한 컴포넌트
        ```python
        def render_dataset_tab(dataset_name, display_name):
            # 공통 탭 렌더링 로직
        ```

        ### 5. Plotly 차트
        - 히스토그램 (분포 시각화)
        - 막대 차트 (카테고리 비교)

        ### 6. Folium 지도
        - 마커 클러스터
        - 다중 레이어
        - 인터랙티브 컨트롤

        ### 7. 상태 관리
        - st.spinner (로딩)
        - st.success/warning/error/info (상태 메시지)
        - st.expander (상세 정보)

        ## 📚 학습 경로

        1. 예제 01-08: 기본 기능 학습
        2. 예제 09-10: 차트 및 지도
        3. 예제 11: 통합 패턴
        4. **예제 12 (현재)**: 현재 앱 구조 이해
        5. 실제 앱(app.py) 디버깅 및 개선

        ## 🔧 현재 앱(app.py)과의 비교

        | 기능 | 현재 앱 | 이 예제 |
        |------|---------|---------|
        | 데이터셋 수 | 7개 | 2개 |
        | 탭 수 | 9개 | 4개 |
        | 지도 기능 | ✅ | ✅ |
        | 차트 기능 | ✅ | ✅ |
        | 필터링 | ✅ | ✅ |
        | 근접성 분석 | ✅ | ❌ |

        ## 🚀 다음 단계

        1. 현재 앱(app.py) 코드 읽기
        2. 각 함수의 역할 이해
        3. utils/ 디렉토리의 모듈 분석
        4. 자신만의 기능 추가
        """)

        with st.expander("💡 디버깅 팁"):
            st.markdown("""
            **자주 발생하는 문제:**

            1. **FileNotFoundError**
               - 데이터 파일 경로 확인
               - 상대 경로 vs 절대 경로

            2. **KeyError (컬럼 없음)**
               - 데이터프레임 컬럼 이름 확인
               - `df.columns` 출력해보기

            3. **지도가 안 보임**
               - 위도/경도 컬럼 확인
               - 좌표 값이 올바른지 확인

            4. **차트가 깨짐**
               - 데이터 타입 확인
               - NaN 값 처리

            5. **캐시 문제**
               - `C` → "Clear cache"
               - 또는 코드에서 `st.cache_data.clear()`
            """)


def render_dataset_tab(dataset_name, dataset_display_name):
    """
    개별 데이터셋 탭 렌더링 (현재 앱의 render_dataset_tab 패턴)
    """
    st.header(f"{dataset_display_name} 데이터셋")

    # 데이터 로딩
    try:
        df = load_dataset(dataset_name)
    except Exception as e:
        st.error(f"❌ 데이터 로딩 오류: {str(e)}")
        return

    # 데이터 정보
    info = get_dataset_info(df)

    # 메트릭 (현재 앱과 동일한 패턴)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("전체 행 수", f"{info['row_count']:,}")
    with col2:
        st.metric("전체 컬럼 수", info['column_count'])
    with col3:
        missing_pct = sum(info['missing_ratios'].values()) / len(info['missing_ratios']) * 100
        st.metric("평균 결측값 %", f"{missing_pct:.1f}%")

    # 데이터 미리보기 (Expander 사용)
    with st.expander("📋 데이터 미리보기", expanded=False):
        st.dataframe(df.head(10), width="stretch")

    # 컬럼 정보
    with st.expander("📊 컬럼 정보", expanded=False):
        col_info = pd.DataFrame({
            '컬럼': df.columns,
            '타입': [info['dtypes'][col] for col in df.columns],
            '결측값 %': [f"{info['missing_ratios'][col] * 100:.1f}%" for col in df.columns]
        })
        st.dataframe(col_info, width="stretch")

    # 통계
    if not info['numeric_summary'].empty:
        with st.expander("📈 숫자 컬럼 통계", expanded=False):
            st.dataframe(info['numeric_summary'], width="stretch")

    # 시각화
    st.subheader("시각화")

    # 숫자 컬럼 분포
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    if numeric_cols:
        st.markdown("### 📊 숫자 컬럼 분포")

        selected_col = st.selectbox(
            "시각화할 컬럼:",
            options=numeric_cols,
            key=f"{dataset_name}_numeric"
        )

        if selected_col:
            fig = px.histogram(
                df,
                x=selected_col,
                title=f"{selected_col} 분포",
                marginal="box"
            )
            st.plotly_chart(fig, width="stretch", key=f"{dataset_name}_hist")

    # 범주형 컬럼 분포
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    if cat_cols:
        st.markdown("### 📊 범주형 컬럼 분포")

        selected_cat = st.selectbox(
            "시각화할 컬럼:",
            options=cat_cols,
            key=f"{dataset_name}_cat"
        )

        if selected_cat:
            value_counts = df[selected_cat].value_counts().head(10)
            fig = px.bar(
                x=value_counts.index,
                y=value_counts.values,
                labels={'x': selected_cat, 'y': '개수'},
                title=f"{selected_cat} 분포 (상위 10개)"
            )
            st.plotly_chart(fig, width="stretch", key=f"{dataset_name}_bar")

    # 지도 (위도/경도가 있는 경우)
    if '위도' in df.columns and '경도' in df.columns:
        st.markdown("### 🗺️ 지리적 분포")

        m = folium.Map(
            location=[df['위도'].mean(), df['경도'].mean()],
            zoom_start=12
        )

        # 샘플링 (성능을 위해, random_state 고정으로 깜빡임 방지)
        sample_df = df.sample(min(100, len(df)), random_state=42)

        marker_cluster = MarkerCluster().add_to(m)

        for idx, row in sample_df.iterrows():
            folium.Marker(
                location=[row['위도'], row['경도']],
                popup=f"{row['지점'] if '지점' in row else 'Point'}"
            ).add_to(marker_cluster)

        st_folium(m, width=700, height=500)

# ============================================
# 추가 지식: st.fragment (부분 재실행)
# ============================================
def knowledge_section():
    st.markdown("---")
    st.header("📚 알아두면 좋은 기능: @st.fragment")

    st.markdown("""
    ### ⚡ @st.fragment란?

    Streamlit은 기본적으로 **위젯 상호작용 시 전체 스크립트를 재실행**합니다.
    하지만 `@st.fragment`를 사용하면 **특정 부분만 재실행**할 수 있어 성능이 크게 향상됩니다.

    ### 왜 중요한가요?
    - 🚀 **성능 향상**: 전체 페이지 대신 일부만 업데이트
    - ⏱️ **빠른 반응**: 무거운 연산을 건너뜀
    - 🗺️ **지도 깜빡임 방지**: 지도가 매번 새로 그려지는 문제 해결
    """)

    st.subheader("💻 구현 예시")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**❌ 기존 방식 (전체 재실행):**")
        st.code("""
# 버튼 클릭 시 전체 스크립트 재실행
# → 지도, 차트 모두 다시 그려짐 (느림)

st.title("대시보드")

# 무거운 데이터 로딩
df = load_large_data()  # 매번 실행

# 지도 (매번 다시 그려짐)
m = create_map(df)
st_folium(m)

# 버튼 클릭 시 위 모든 코드 재실행!
if st.button("업데이트"):
    st.write("클릭됨")
""", language="python")

    with col2:
        st.markdown("**✅ @st.fragment 사용:**")
        st.code("""
# fragment 안의 버튼은 해당 부분만 재실행
# → 지도, 차트는 그대로 유지 (빠름)

st.title("대시보드")

# 무거운 데이터 로딩 (재실행 안됨)
df = load_large_data()

# 지도 (재실행 안됨)
m = create_map(df)
st_folium(m)

# 이 부분만 재실행!
@st.fragment
def quick_update():
    if st.button("업데이트"):
        st.write("클릭됨")
        # 가벼운 작업만 수행

quick_update()
""", language="python")

    # 실제 동작 데모
    st.subheader("🎮 직접 체험해보기")

    st.markdown("""
    아래 두 버튼의 동작 차이를 비교해보세요:
    - **일반 버튼**: 클릭 시 카운터가 초기화됨 (전체 재실행)
    - **Fragment 버튼**: 클릭 시 카운터 유지 (부분 재실행)
    """)

    # 세션 상태로 카운터 관리
    if 'normal_count' not in st.session_state:
        st.session_state.normal_count = 0
    if 'fragment_count' not in st.session_state:
        st.session_state.fragment_count = 0

    demo_col1, demo_col2 = st.columns(2)

    with demo_col1:
        st.markdown("**일반 버튼:**")
        if st.button("일반 클릭", key="normal_btn"):
            st.session_state.normal_count += 1
        st.metric("일반 카운터", st.session_state.normal_count)
        st.caption("다른 위젯 상호작용 시 이 카운터도 영향받음")

    with demo_col2:
        st.markdown("**Fragment 버튼:**")

        @st.fragment
        def fragment_counter():
            if st.button("Fragment 클릭", key="fragment_btn"):
                st.session_state.fragment_count += 1
            st.metric("Fragment 카운터", st.session_state.fragment_count)
            st.caption("이 부분만 독립적으로 업데이트됨")

        fragment_counter()

    # 실전 활용 예시
    st.subheader("📊 실전 활용: 자동 새로고침")

    st.markdown("""
    `@st.fragment`의 `run_every` 파라미터로 **주기적 자동 업데이트**를 구현할 수 있습니다:
    """)

    st.code("""
# 5초마다 이 부분만 자동 업데이트
@st.fragment(run_every="5s")
def live_metrics():
    # 실시간 데이터 가져오기
    current_time = datetime.now().strftime("%H:%M:%S")
    live_value = get_live_data()  # API 호출 등

    col1, col2 = st.columns(2)
    col1.metric("현재 시간", current_time)
    col2.metric("실시간 값", live_value)

live_metrics()

# 나머지 무거운 컴포넌트는 재실행 안됨
heavy_chart()  # 그대로 유지
heavy_map()    # 그대로 유지
""", language="python")

    # 실시간 데모
    st.markdown("**실시간 업데이트 데모:**")

    @st.fragment(run_every="2s")
    def live_demo():
        import time
        current = time.strftime("%H:%M:%S")
        random_val = np.random.randint(100, 999)

        col1, col2, col3 = st.columns(3)
        col1.metric("⏰ 현재 시간", current)
        col2.metric("📊 랜덤 값", random_val)
        col3.metric("🔄 상태", "업데이트 중...")
        st.caption("2초마다 이 부분만 자동 업데이트됩니다 (페이지 전체는 재실행 안됨)")

    live_demo()

    # 실습 과제
    st.subheader("✏️ 실습 과제")

    st.markdown("""
    1. **기본 실습**: 위의 "일반 버튼"과 "Fragment 버튼"을 번갈아 클릭해보세요.
       일반 버튼 클릭 시 Fragment 카운터가 어떻게 되는지 관찰하세요.

    2. **응용 실습**: 지도가 있는 탭에서 `@st.fragment`를 적용해보세요.
       - 필터 변경 시에도 지도가 깜빡이지 않도록 개선
       - 힌트: 필터 UI를 fragment로 분리

    3. **심화 실습**: 실시간 대시보드를 만들어보세요.
       - `@st.fragment(run_every="10s")`로 10초마다 데이터 갱신
       - 메트릭만 업데이트, 차트는 유지
    """)

    with st.expander("💡 정답 예시 보기"):
        st.code("""
# 지도 깜빡임 방지 예시

# 지도는 fragment 밖에 (재실행 안됨)
df = load_data()
m = create_map(df)
st_folium(m, width=700, height=500)

# 필터만 fragment로 분리 (이 부분만 재실행)
@st.fragment
def filter_section():
    selected = st.multiselect("지점 선택:", options=["A", "B", "C"])

    if st.button("필터 적용"):
        # 필터링된 결과만 표시
        filtered = df[df['지점'].isin(selected)]
        st.dataframe(filtered)
        st.success(f"{len(filtered)}개 행 필터링됨")

filter_section()

# 실시간 메트릭 예시
@st.fragment(run_every="30s")
def realtime_metrics():
    # 30초마다 최신 데이터 fetch
    latest = fetch_latest_metrics()

    col1, col2, col3 = st.columns(3)
    col1.metric("매출", f"₩{latest['sales']:,}")
    col2.metric("방문자", f"{latest['visitors']:,}")
    col3.metric("전환율", f"{latest['conversion']:.1f}%")

realtime_metrics()
""", language="python")

    st.markdown("""
    ---
    ### 📝 핵심 정리

    | 기능 | 설명 | 사용 시점 |
    |------|------|----------|
    | `@st.fragment` | 해당 함수만 재실행 | 무거운 컴포넌트와 가벼운 UI 분리 |
    | `run_every` | 주기적 자동 실행 | 실시간 데이터 모니터링 |
    | Session State | 상태 유지 | Fragment 간 데이터 공유 |

    **주의사항:**
    - Fragment 안에서 변경된 값은 Fragment 밖에 영향 없음
    - 전역 상태 변경이 필요하면 `st.session_state` 사용
    - 너무 많은 Fragment는 오히려 복잡해질 수 있음
    """)

# 메인 앱 실행 후 지식 섹션 추가
if __name__ == "__main__":
    main()
    knowledge_section()
