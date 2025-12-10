# 예제 10: Folium 지도 통합

## 학습 목표
- Folium과 streamlit-folium 사용법
- 마커, 팝업, 툴팁 추가
- 마커 클러스터링
- 다중 레이어 관리

## 기본 사용법

```python
import folium
from streamlit_folium import st_folium

# 지도 생성
m = folium.Map(location=[lat, lng], zoom_start=12)

# 마커 추가
folium.Marker(
    [lat, lng],
    popup='팝업 내용',
    tooltip='툴팁',
    icon=folium.Icon(color='red')
).add_to(m)

# 표시
st_folium(m, width=700, height=500)
```

## 현재 앱에서의 사용

```python
# utils/visualizer.py:142-146 - 기본 지도
m = folium.Map(
    location=[center_lat, center_lng],
    zoom_start=zoom_start,
    tiles='OpenStreetMap'
)

# utils/visualizer.py:152-156 - 마커 클러스터
if len(df_clean) > 100:
    marker_cluster = MarkerCluster().add_to(feature_group)
    marker_container = marker_cluster
```

## 실행 방법

```bash
streamlit run 10_folium_maps.py
```
