"""
예제 2: 레이아웃과 컬럼 (Columns and Metrics)

이 예제에서는 Streamlit의 레이아웃 시스템과 메트릭 표시를 학습합니다.
"""
import streamlit as st

st.set_page_config(
    page_title="레이아웃과 컬럼",
    page_icon="📐",
    layout="wide"
)

st.title("📐 레이아웃과 컬럼")

# ============================================
# 1. 기본 컬럼 사용법
# ============================================
st.header("1. 기본 컬럼 (Columns)")

st.markdown("""
`st.columns()`를 사용하면 화면을 여러 개의 수직 컬럼으로 나눌 수 있습니다.
각 컬럼에는 독립적으로 컨텐츠를 배치할 수 있습니다.
""")

# 2개의 동일한 너비 컬럼
col1, col2 = st.columns(2)

with col1:
    st.subheader("왼쪽 컬럼")
    st.write("이것은 왼쪽 컬럼입니다.")
    st.image("https://via.placeholder.com/300x200/FF6B6B/FFFFFF?text=Left+Column",
             width='content')

with col2:
    st.subheader("오른쪽 컬럼")
    st.write("이것은 오른쪽 컬럼입니다.")
    st.image("https://via.placeholder.com/300x200/4ECDC4/FFFFFF?text=Right+Column",
             width='content')

# ============================================
# 2. 다양한 컬럼 비율
# ============================================
st.header("2. 컬럼 비율 조정")

st.markdown("""
컬럼의 너비 비율을 리스트로 지정할 수 있습니다.
예: `st.columns([1, 2, 1])`는 1:2:1 비율의 3개 컬럼을 만듭니다.
""")

# 3개의 다른 비율 컬럼 (1:2:1)
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.write("**좁은 컬럼**")
    st.write("1")

with col2:
    st.write("**넓은 컬럼 (2배)**")
    st.write("2")

with col3:
    st.write("**좁은 컬럼**")
    st.write("1")

# ============================================
# 3. 메트릭 (Metric) - 숫자 표시
# ============================================
st.header("3. 메트릭 (Metrics)")

st.markdown("""
`st.metric()`은 중요한 숫자와 변화량을 시각적으로 표시하는데 유용합니다.
대시보드나 데이터 분석 앱에서 자주 사용됩니다.
""")

# 메트릭 3개를 컬럼에 배치
metric_col1, metric_col2, metric_col3 = st.columns(3)

with metric_col1:
    st.metric(
        label="온도",
        value="24°C",
        delta="1.2°C"  # 양수는 초록색 화살표
    )

with metric_col2:
    st.metric(
        label="습도",
        value="65%",
        delta="-5%"  # 음수는 빨간색 화살표
    )

with metric_col3:
    st.metric(
        label="풍속",
        value="12 km/h",
        delta="2 km/h",
        delta_color="off"  # 화살표 색상 비활성화
    )

# ============================================
# 4. 실제 데이터로 메트릭 표시
# ============================================
st.header("4. 실제 데이터로 메트릭 표시")

# 샘플 데이터
current_users = 1250
previous_users = 1100
user_change = current_users - previous_users
user_change_pct = (user_change / previous_users) * 100

current_revenue = 45230
previous_revenue = 42100
revenue_change = current_revenue - previous_revenue
revenue_change_pct = (revenue_change / previous_revenue) * 100

current_sales = 342
previous_sales = 389
sales_change = current_sales - previous_sales
sales_change_pct = (sales_change / previous_sales) * 100

# 컬럼에 메트릭 배치
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="총 사용자 수",
        value=f"{current_users:,}명",
        delta=f"{user_change_pct:.1f}%"
    )

with col2:
    st.metric(
        label="총 매출",
        value=f"₩{current_revenue:,}",
        delta=f"{revenue_change_pct:.1f}%"
    )

with col3:
    st.metric(
        label="판매 건수",
        value=f"{current_sales}건",
        delta=f"{sales_change_pct:.1f}%"
    )

# ============================================
# 5. 중첩된 컬럼
# ============================================
st.header("5. 중첩된 컬럼")

st.markdown("""
컬럼 안에 또 다른 컬럼을 만들 수 있습니다.
복잡한 레이아웃을 구성할 때 유용합니다.
""")

# 외부 컬럼
outer_col1, outer_col2 = st.columns([2, 1])

with outer_col1:
    st.subheader("메인 컨텐츠 영역")

    # 내부 컬럼
    inner_col1, inner_col2 = st.columns(2)

    with inner_col1:
        st.write("**내부 왼쪽**")
        st.info("중첩 컬럼 1")

    with inner_col2:
        st.write("**내부 오른쪽**")
        st.info("중첩 컬럼 2")

with outer_col2:
    st.subheader("사이드바 영역")
    st.success("외부 오른쪽 컬럼")
    st.write("추가 정보를 여기에 표시")

# ============================================
# 6. 컨테이너 (Container)
# ============================================
st.header("6. 컨테이너 (Container)")

st.markdown("""
`st.container()`를 사용하면 요소들을 그룹화하고 나중에 컨텐츠를 추가할 수 있습니다.
""")

# 컨테이너 생성
container = st.container()

st.write("이 텍스트는 컨테이너 밖에 있습니다.")

# 컨테이너에 컨텐츠 추가
with container:
    st.info("이 텍스트는 컨테이너 안에 있습니다.")
    st.write("컨테이너를 사용하면 레이아웃을 더 유연하게 구성할 수 있습니다.")

# ============================================
# 7. 실전 예제: 대시보드 레이아웃
# ============================================
st.header("7. 실전 예제: 대시보드 레이아웃")

st.markdown("---")

# 헤더 영역
st.subheader("📊 일일 리포트 대시보드")

# 메트릭 행
metric_cols = st.columns(4)
metrics_data = [
    {"label": "방문자", "value": "12,345", "delta": "+5.2%"},
    {"label": "페이지뷰", "value": "45,678", "delta": "+3.1%"},
    {"label": "이탈률", "value": "32.5%", "delta": "-1.2%"},
    {"label": "평균 체류시간", "value": "3m 24s", "delta": "+12s"}
]

for col, metric in zip(metric_cols, metrics_data):
    with col:
        st.metric(
            label=metric["label"],
            value=metric["value"],
            delta=metric["delta"]
        )

st.markdown("---")

# 컨텐츠 영역
content_col1, content_col2 = st.columns([2, 1])

with content_col1:
    st.write("**주요 차트 영역**")
    st.info("여기에 차트가 표시됩니다 (예제 9에서 학습)")

with content_col2:
    st.write("**최근 활동**")
    st.success("✅ 새 사용자 가입: 42명")
    st.warning("⚠️ 서버 응답 시간 증가")
    st.info("ℹ️ 시스템 업데이트 예정")

# ============================================
# 실습 섹션
# ============================================
st.markdown("---")
st.header("🎯 실습해보세요!")

st.markdown("""
1. 4개의 동일한 너비 컬럼을 만들어보세요
2. 메트릭에 다양한 `delta_color` 옵션을 시도해보세요
3. 3단계 중첩 컬럼을 만들어보세요
4. 자신만의 대시보드 레이아웃을 설계해보세요
""")

# --------------------------------------------
# 실습 1: 4개의 동일한 너비 컬럼
# --------------------------------------------
st.subheader("실습 1: 4개의 동일한 너비 컬럼")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.info("컬럼 1")
    st.write("25% 너비")

with c2:
    st.success("컬럼 2")
    st.write("25% 너비")

with c3:
    st.warning("컬럼 3")
    st.write("25% 너비")

with c4:
    st.error("컬럼 4")
    st.write("25% 너비")

# --------------------------------------------
# 실습 2: delta_color 옵션 비교
# --------------------------------------------
st.subheader("실습 2: delta_color 옵션 비교")

st.write("""
`delta_color` 옵션:
- `"normal"` (기본값): 양수=초록, 음수=빨강
- `"inverse"`: 양수=빨강, 음수=초록 (비용 등에 유용)
- `"off"`: 색상 없음 (중립적인 정보)
""")

delta_cols = st.columns(3)

with delta_cols[0]:
    st.metric(
        label="매출 (normal)",
        value="₩1,000,000",
        delta="+15%",
        delta_color="normal"
    )
    st.caption("증가=좋음 (초록)")

with delta_cols[1]:
    st.metric(
        label="비용 (inverse)",
        value="₩500,000",
        delta="+15%",
        delta_color="inverse"
    )
    st.caption("증가=나쁨 (빨강)")

with delta_cols[2]:
    st.metric(
        label="온도 (off)",
        value="25°C",
        delta="+3°C",
        delta_color="off"
    )
    st.caption("중립적 정보")

# --------------------------------------------
# 실습 3: 3단계 중첩 컬럼
# --------------------------------------------
st.subheader("실습 3: 3단계 중첩 컬럼 구조")

# 1단계
level1_col1, level1_col2 = st.columns(2)

with level1_col1:
    st.write("**1단계 - 왼쪽 (50%)**")

    # 2단계
    level2_col1, level2_col2 = st.columns(2)

    with level2_col1:
        st.write("2단계 - 왼쪽")

        # 3단계
        level3_col1, level3_col2 = st.columns(2)
        with level3_col1:
            st.success("3단계-1")
        with level3_col2:
            st.info("3단계-2")

    with level2_col2:
        st.write("2단계 - 오른쪽")
        st.warning("깊은 중첩!")

with level1_col2:
    st.write("**1단계 - 오른쪽 (50%)**")
    st.info("중첩 컬럼은 복잡한 레이아웃에 유용하지만, 너무 깊은 중첩은 가독성을 해칠 수 있습니다.")

# --------------------------------------------
# 실습 4: 간단한 대시보드 만들기
# --------------------------------------------
st.subheader("실습 4: 나만의 미니 대시보드")

# 사용자 입력으로 대시보드 커스터마이징
dashboard_title = st.text_input("대시보드 제목:", value="내 대시보드")

# 메트릭 데이터 입력
input_col1, input_col2, input_col3 = st.columns(3)

with input_col1:
    metric1_value = st.number_input("매출 (만원)", value=1000, step=100)
    metric1_delta = st.number_input("매출 변화 (%)", value=10.0, step=0.5)

with input_col2:
    metric2_value = st.number_input("고객 수", value=500, step=10)
    metric2_delta = st.number_input("고객 변화 (%)", value=-5.0, step=0.5)

with input_col3:
    metric3_value = st.number_input("전환율 (%)", value=3.5, step=0.1)
    metric3_delta = st.number_input("전환율 변화", value=0.5, step=0.1)

# 대시보드 출력
st.markdown(f"### {dashboard_title}")
st.markdown("---")

dash_col1, dash_col2, dash_col3 = st.columns(3)

with dash_col1:
    st.metric("매출", f"₩{metric1_value:,}만", f"{metric1_delta:+.1f}%")

with dash_col2:
    st.metric("고객 수", f"{metric2_value:,}명", f"{metric2_delta:+.1f}%")

with dash_col3:
    st.metric("전환율", f"{metric3_value:.1f}%", f"{metric3_delta:+.1f}%p")

# --------------------------------------------
# 교육용 정보
# --------------------------------------------
with st.expander("📚 알아두면 좋은 정보"):
    st.markdown("""
### 컬럼 비율 지정 방법

```python
# 방법 1: 숫자로 동일 너비
col1, col2, col3 = st.columns(3)  # 1:1:1 비율

# 방법 2: 리스트로 비율 지정
col1, col2 = st.columns([3, 1])   # 3:1 비율

# 방법 3: 소수점 비율도 가능
col1, col2, col3 = st.columns([0.2, 0.5, 0.3])
```

### 컬럼 gap 설정 (버전 1.28+)

```python
# 컬럼 간 간격 조절
st.columns(3, gap="small")   # 기본값
st.columns(3, gap="medium")  # 중간 간격
st.columns(3, gap="large")   # 넓은 간격
```

### st.metric() 숫자 포맷팅 팁

```python
# 천 단위 콤마
f"{value:,}"           # 1234567 → "1,234,567"

# 소수점 자릿수
f"{value:.2f}"         # 3.14159 → "3.14"

# 부호 항상 표시
f"{delta:+.1f}%"       # 10 → "+10.0%", -5 → "-5.0%"

# 통화 형식
f"₩{value:,.0f}"       # 10000 → "₩10,000"
```

### 레이아웃 설계 팁

1. **모바일 대응**: `layout="wide"` 사용 시 모바일에서 컬럼이 세로로 쌓임
2. **가독성**: 컬럼은 최대 4개까지 권장
3. **중첩**: 2단계 이상의 중첩은 피하는 것이 좋음
4. **메트릭 배치**: 중요 지표는 항상 상단에 배치
    """)
