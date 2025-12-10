"""
예제 10: Folium 지도 통합 (Folium Maps)

이 예제에서는 Folium을 사용한 지도 시각화를 학습합니다.
"""
import streamlit as st
from streamlit_folium import st_folium
import folium
from folium.plugins import MarkerCluster
from folium.features import DivIcon
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Folium 지도",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ Folium 지도 통합")

st.markdown("""
Folium은 Leaflet.js 기반의 인터랙티브 지도를 Python으로 쉽게 만들 수 있는 라이브러리입니다.
streamlit-folium을 사용하여 Streamlit 앱에 통합할 수 있습니다.
""")

# ============================================
# 1. 기본 지도
# ============================================
st.header("1. 기본 지도")

st.markdown("대구 시청을 중심으로 한 기본 지도:")

# 대구 시청 좌표
daegu_center = [35.8714, 128.6014]

# 기본 지도 생성
m = folium.Map(
    location=daegu_center,
    zoom_start=14,
    tiles='OpenStreetMap'
)

# 마커 추가
folium.Marker(
    daegu_center,
    popup='대구 시청',
    tooltip='클릭하세요!',
    icon=folium.Icon(color='red', icon='info-sign')
).add_to(m)

# 지도 표시
st_folium(m, width=700, height=500)

# ============================================
# 2. 다양한 지도 타일
# ============================================
st.header("2. 다양한 지도 스타일")

tile_option = st.selectbox(
    "지도 스타일 선택:",
    ['OpenStreetMap', 'Stamen Terrain', 'Stamen Toner', 'CartoDB positron', 'CartoDB dark_matter']
)

m = folium.Map(
    location=daegu_center,
    zoom_start=12,
    tiles=tile_option
)

st_folium(m, width=700, height=400)

# ============================================
# 3. 여러 마커 추가
# ============================================
st.header("3. 여러 마커 추가")

# 샘플 장소 데이터
places = pd.DataFrame({
    '이름': ['대구 시청', '대구역', '동대구역', '83타워', '앞산공원'],
    '위도': [35.8714, 35.8800, 35.8790, 35.8584, 35.8301],
    '경도': [128.6014, 128.6281, 128.6285, 128.5620, 128.5643],
    '타입': ['관공서', '교통', '교통', '관광', '공원']
})

st.dataframe(places)

# 타입별 색상
color_map = {
    '관공서': 'red',
    '교통': 'blue',
    '관광': 'green',
    '공원': 'orange'
}

# 지도 생성
m = folium.Map(location=daegu_center, zoom_start=12)

# 마커 추가
for idx, row in places.iterrows():
    folium.Marker(
        location=[row['위도'], row['경도']],
        popup=f"<b>{row['이름']}</b><br>타입: {row['타입']}",
        tooltip=row['이름'],
        icon=folium.Icon(color=color_map[row['타입']], icon='info-sign')
    ).add_to(m)

st_folium(m, width=900, height=500)

# 범례 표시
st.markdown("**범례:**")
cols = st.columns(len(color_map))
for i, (type_name, color) in enumerate(color_map.items()):
    with cols[i]:
        st.markdown(f"🔵 {type_name}")

# ============================================
# 4. 마커 클러스터
# ============================================
st.header("4. 마커 클러스터")

st.markdown("""
많은 마커가 있을 때 클러스터링을 사용하면 지도가 깔끔해집니다.
줌 인하면 클러스터가 개별 마커로 분리됩니다.
""")

# 랜덤 포인트 생성
num_points = st.slider("마커 개수", 10, 200, 50, step=10)

np.random.seed(42)
random_points = pd.DataFrame({
    '위도': np.random.uniform(35.7, 36.0, num_points),
    '경도': np.random.uniform(128.4, 128.8, num_points)
})

# 지도 생성
m = folium.Map(location=daegu_center, zoom_start=11)

# 마커 클러스터 생성
marker_cluster = MarkerCluster().add_to(m)

# 마커 추가
for idx, row in random_points.iterrows():
    folium.Marker(
        location=[row['위도'], row['경도']],
        popup=f"Point {idx+1}",
    ).add_to(marker_cluster)

st_folium(m, width=900, height=500)

# ============================================
# 5. 다양한 마커 스타일
# ============================================
st.header("5. 다양한 마커 스타일")

m = folium.Map(location=daegu_center, zoom_start=13)

# 기본 마커
folium.Marker(
    [35.87, 128.60],
    popup='기본 마커',
    icon=folium.Icon(color='blue', icon='info-sign')
).add_to(m)

# 원형 마커
folium.CircleMarker(
    [35.87, 128.61],
    radius=10,
    popup='원형 마커',
    color='red',
    fill=True,
    fillColor='red'
).add_to(m)

# 큰 원
folium.Circle(
    [35.87, 128.62],
    radius=500,  # 미터
    popup='500m 반경',
    color='green',
    fill=True,
    fillOpacity=0.2
).add_to(m)

st_folium(m, width=900, height=500)

# ============================================
# 6. 레이어 컨트롤
# ============================================
st.header("6. 레이어 컨트롤")

st.markdown("""
여러 데이터셋을 레이어로 구분하여 선택적으로 표시할 수 있습니다.
지도 우측 상단의 컨트롤로 레이어를 켜고 끌 수 있습니다.
""")

# 지도 생성
m = folium.Map(location=daegu_center, zoom_start=12)

# 레이어 1: 관광지
tourist_layer = folium.FeatureGroup(name='관광지', show=True)
tourist_places = [
    [35.8584, 128.5620, '83타워'],
    [35.8301, 128.5643, '앞산공원']
]

for place in tourist_places:
    folium.Marker(
        [place[0], place[1]],
        popup=place[2],
        icon=folium.Icon(color='green', icon='camera')
    ).add_to(tourist_layer)

tourist_layer.add_to(m)

# 레이어 2: 교통
transport_layer = folium.FeatureGroup(name='교통', show=True)
transport_places = [
    [35.8800, 128.6281, '대구역'],
    [35.8790, 128.6285, '동대구역']
]

for place in transport_places:
    folium.Marker(
        [place[0], place[1]],
        popup=place[2],
        icon=folium.Icon(color='blue', icon='train')
    ).add_to(transport_layer)

transport_layer.add_to(m)

# 레이어 컨트롤 추가
folium.LayerControl(collapsed=False).add_to(m)

st_folium(m, width=900, height=500, key="layer_map")

st.info("💡 지도 우측 상단의 레이어 버튼을 클릭하여 레이어를 켜고 끌 수 있습니다.")

# ============================================
# 7. 실전 예제: 데이터 기반 지도
# ============================================
st.header("7. 실전 예제: 데이터 기반 지도")

# 샘플 데이터 생성
@st.cache_data
def create_location_data():
    np.random.seed(42)
    return pd.DataFrame({
        '이름': [f'지점 {i+1}' for i in range(30)],
        '위도': np.random.uniform(35.7, 36.0, 30),
        '경도': np.random.uniform(128.4, 128.8, 30),
        '매출': np.random.randint(1000, 10000, 30),
        '카테고리': np.random.choice(['A', 'B', 'C'], 30)
    })

location_data = create_location_data()

# 필터
selected_categories = st.multiselect(
    "카테고리 선택:",
    options=location_data['카테고리'].unique(),
    default=location_data['카테고리'].unique()
)

filtered_data = location_data[location_data['카테고리'].isin(selected_categories)]

# 지도 생성
m = folium.Map(location=daegu_center, zoom_start=11)

# 마커 클러스터
marker_cluster = MarkerCluster().add_to(m)

# 카테고리별 색상
category_colors = {'A': 'red', 'B': 'blue', 'C': 'green'}

# 마커 추가
for idx, row in filtered_data.iterrows():
    label = row['카테고리']
    color = category_colors[label]
    popup_html = f"""
    <div style='width: 200px'>
        <b>{row['이름']}</b><br>
        카테고리: {label}<br>
        매출: ₩{row['매출']:,}
    </div>
    """
    icon_html = f"""
    <div style="
        background:{color};
        color:#fff;
        font-weight:700;
        border-radius:50%;
        width:28px;
        height:28px;
        line-height:28px;
        text-align:center;
        border:2px solid #ffffff;
        box-shadow:0 0 6px rgba(0,0,0,0.35);
    ">
        {label}
    </div>
    """

    folium.Marker(
        location=[row['위도'], row['경도']],
        popup=folium.Popup(popup_html, max_width=300),
        tooltip=f"[{label}] {row['이름']}",
        icon=DivIcon(html=icon_html, icon_size=(28, 28), icon_anchor=(14, 14))
    ).add_to(marker_cluster)

st_folium(m, width=900, height=600)

# 통계
st.subheader("선택된 데이터 통계")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("지점 수", len(filtered_data))
with col2:
    st.metric("총 매출", f"₩{filtered_data['매출'].sum():,}")
with col3:
    st.metric("평균 매출", f"₩{filtered_data['매출'].mean():,.0f}")

# ============================================
# 실습 섹션
# ============================================
st.markdown("---")
st.header("🎯 실습해보세요!")

st.markdown("""
1. 현재 위치 또는 원하는 위치의 지도 만들기
2. 실제 데이터(CSV 파일)를 지도에 표시
3. 팝업에 이미지나 차트 추가
4. 여러 레이어를 사용한 복잡한 지도 구성
5. 현재 앱(app.py)의 지도 기능 분석 및 개선
""")

with st.expander("💡 Folium 사용 팁"):
    st.markdown("""
    **마커 최적화:**
    - 100개 이상의 마커는 MarkerCluster 사용
    - 너무 많은 마커는 성능 저하 (샘플링 고려)

    **팝업 커스터마이징:**
    - HTML을 사용하여 풍부한 팝업 생성
    - 이미지, 링크, 차트도 가능

    **레이어 활용:**
    - 서로 다른 데이터셋은 별도 레이어로
    - LayerControl로 사용자가 선택하도록

    **지도 중심 계산:**
    ```python
    center_lat = df['위도'].mean()
    center_lng = df['경도'].mean()
    ```

    **줌 레벨:**
    - 1-5: 대륙/국가
    - 6-9: 지역
    - 10-12: 도시
    - 13-15: 동네
    - 16-18: 건물
    """)

# ============================================
# 실습과제 구현
# ============================================
st.markdown("---")
st.header("📝 실습과제 구현")

# 1. 원하는 위치의 지도 만들기
st.subheader("1. 원하는 위치 지도")

col1, col2 = st.columns(2)
with col1:
    user_lat = st.number_input("위도", value=35.8714, format="%.4f")
with col2:
    user_lng = st.number_input("경도", value=128.6014, format="%.4f")

user_map = folium.Map(location=[user_lat, user_lng], zoom_start=14)
folium.Marker([user_lat, user_lng], popup="선택한 위치").add_to(user_map)
st_folium(user_map, width=700, height=400, key="user_map")

# 2. CSV 데이터를 지도에 표시
st.subheader("2. CSV 데이터 지도 표시")

uploaded_file = st.file_uploader("CSV 파일 업로드 (위도, 경도 컬럼 필요)", type=['csv'])

if uploaded_file:
    csv_data = pd.read_csv(uploaded_file)
    st.dataframe(csv_data.head())

    lat_col = st.selectbox("위도 컬럼", csv_data.columns)
    lng_col = st.selectbox("경도 컬럼", csv_data.columns)

    csv_map = folium.Map(location=[csv_data[lat_col].mean(), csv_data[lng_col].mean()], zoom_start=12)
    cluster = MarkerCluster().add_to(csv_map)

    for _, row in csv_data.iterrows():
        folium.Marker([row[lat_col], row[lng_col]]).add_to(cluster)

    st_folium(csv_map, width=700, height=400, key="csv_map")
else:
    st.info("CSV 파일을 업로드하세요.")
