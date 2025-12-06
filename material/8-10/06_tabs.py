"""
예제 6: 탭 네비게이션 (Tabs)

이 예제에서는 st.tabs를 사용하여 컨텐츠를 탭으로 구분하는 방법을 학습합니다.
"""
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="탭 네비게이션",
    page_icon="📑",
    layout="wide"
)

st.title("📑 탭 네비게이션 (Tabs)")

st.markdown("""
탭은 관련된 컨텐츠를 카테고리별로 구분하여 표시할 때 유용합니다.
사용자는 탭을 클릭하여 원하는 컨텐츠로 이동할 수 있습니다.
""")

# ============================================
# 1. 기본 탭 사용법
# ============================================
st.header("1. 기본 탭 사용법")

tab1, tab2, tab3 = st.tabs(["첫 번째 탭", "두 번째 탭", "세 번째 탭"])

with tab1:
    st.subheader("첫 번째 탭의 내용")
    st.write("이것은 첫 번째 탭입니다.")
    st.info("탭을 클릭하여 다른 탭으로 이동할 수 있습니다.")

with tab2:
    st.subheader("두 번째 탭의 내용")
    st.write("이것은 두 번째 탭입니다.")
    st.success("각 탭에는 서로 다른 컨텐츠를 넣을 수 있습니다.")

with tab3:
    st.subheader("세 번째 탭의 내용")
    st.write("이것은 세 번째 탭입니다.")
    st.warning("탭은 최대한 간결하게 유지하는 것이 좋습니다.")

# ============================================
# 2. 이모지를 사용한 탭
# ============================================
st.header("2. 이모지를 사용한 탭")

tabs = st.tabs(["🏠 홈", "📊 데이터", "⚙️ 설정"])

with tabs[0]:
    st.write("### 홈 화면")
    st.write("환영합니다! 이것은 홈 화면입니다.")

with tabs[1]:
    st.write("### 데이터 화면")
    data = pd.DataFrame(np.random.randn(5, 3), columns=['A', 'B', 'C'])
    st.dataframe(data)

with tabs[2]:
    st.write("### 설정 화면")
    theme = st.selectbox("테마 선택", ["밝은 테마", "어두운 테마"])
    st.write(f"선택된 테마: {theme}")

# ============================================
# 3. 데이터 탐색 탭
# ============================================
st.header("3. 실전 예제: 데이터 탐색 탭")

# 샘플 데이터 생성
df = pd.DataFrame({
    '날짜': pd.date_range('2024-01-01', periods=100),
    '매출': np.random.randint(1000, 5000, 100),
    '방문자': np.random.randint(100, 500, 100),
    '전환율': np.random.uniform(1, 5, 100)
})

tab_overview, tab_data, tab_chart, tab_stats = st.tabs([
    "📝 개요",
    "📋 데이터",
    "📈 차트",
    "📊 통계"
])

with tab_overview:
    st.subheader("데이터 개요")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("총 매출", f"₩{df['매출'].sum():,}")
    with col2:
        st.metric("평균 매출", f"₩{df['매출'].mean():,.0f}")
    with col3:
        st.metric("총 방문자", f"{df['방문자'].sum():,}명")
    with col4:
        st.metric("평균 전환율", f"{df['전환율'].mean():.2f}%")

    st.markdown("---")
    st.write("### 최근 트렌드")
    st.line_chart(df.set_index('날짜')['매출'])

with tab_data:
    st.subheader("전체 데이터")

    # 필터링 옵션
    col1, col2 = st.columns(2)

    with col1:
        min_sales = st.number_input("최소 매출", value=0)
    with col2:
        max_sales = st.number_input("최대 매출", value=5000)

    # 필터링된 데이터
    filtered_df = df[(df['매출'] >= min_sales) & (df['매출'] <= max_sales)]

    st.write(f"필터링된 데이터: {len(filtered_df)}개 행")
    st.dataframe(filtered_df, width="stretch", height=400)

with tab_chart:
    st.subheader("시각화")

    chart_type = st.selectbox("차트 유형 선택", ["라인 차트", "영역 차트", "바 차트"])

    if chart_type == "라인 차트":
        st.line_chart(df.set_index('날짜')[['매출', '방문자']])
    elif chart_type == "영역 차트":
        st.area_chart(df.set_index('날짜')[['매출', '방문자']])
    else:
        st.bar_chart(df.set_index('날짜')['매출'])

    st.markdown("---")
    st.write("### 전환율 분포")
    st.bar_chart(df['전환율'].head(20))

with tab_stats:
    st.subheader("통계 분석")

    st.write("### 기술 통계")
    st.dataframe(df.describe(), width="stretch")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### 매출 통계")
        st.write(f"- 최소값: ₩{df['매출'].min():,}")
        st.write(f"- 최대값: ₩{df['매출'].max():,}")
        st.write(f"- 중앙값: ₩{df['매출'].median():,}")
        st.write(f"- 표준편차: ₩{df['매출'].std():,.2f}")

    with col2:
        st.write("### 방문자 통계")
        st.write(f"- 최소값: {df['방문자'].min():,}명")
        st.write(f"- 최대값: {df['방문자'].max():,}명")
        st.write(f"- 중앙값: {df['방문자'].median():,}명")
        st.write(f"- 표준편차: {df['방문자'].std():,.2f}명")

# ============================================
# 4. 다양한 컨텐츠 유형
# ============================================
st.header("4. 탭에 다양한 컨텐츠 담기")

content_tabs = st.tabs(["📄 텍스트", "🖼️ 이미지", "💻 코드", "🎨 스타일"])

with content_tabs[0]:
    st.markdown("""
    ### 마크다운 텍스트

    탭 안에는 **마크다운**을 포함한 *모든 Streamlit 요소*를 넣을 수 있습니다.

    - 리스트
    - 표
    - 링크
    - 등등...
    """)

with content_tabs[1]:
    st.write("### 이미지 갤러리")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.image("https://via.placeholder.com/200/FF6B6B/FFFFFF?text=Image+1")
    with col2:
        st.image("https://via.placeholder.com/200/4ECDC4/FFFFFF?text=Image+2")
    with col3:
        st.image("https://via.placeholder.com/200/45B7D1/FFFFFF?text=Image+3")

with content_tabs[2]:
    st.write("### 코드 예시")
    st.code("""
# Python 코드 예시
def calculate_total(items):
    total = sum(item['price'] for item in items)
    return total

items = [
    {'name': 'Apple', 'price': 1000},
    {'name': 'Banana', 'price': 500}
]

print(f"Total: {calculate_total(items)}")
    """, language="python")

with content_tabs[3]:
    st.write("### 스타일 요소")

    st.success("✅ 성공 메시지")
    st.info("ℹ️ 정보 메시지")
    st.warning("⚠️ 경고 메시지")
    st.error("❌ 오류 메시지")

    st.progress(0.75)
    st.write("진행률: 75%")

# ============================================
# 5. 동적 탭 생성
# ============================================
st.header("5. 동적 탭 생성")

num_tabs = st.slider("탭 개수 선택", 2, 10, 4)

# 동적으로 탭 이름 생성
tab_names = [f"탭 {i+1}" for i in range(num_tabs)]
dynamic_tabs = st.tabs(tab_names)

for i, tab in enumerate(dynamic_tabs):
    with tab:
        st.write(f"### {tab_names[i]}의 컨텐츠")
        st.write(f"이것은 동적으로 생성된 {i+1}번째 탭입니다.")

        # 각 탭에 다른 컨텐츠
        if i % 2 == 0:
            st.info(f"탭 {i+1}은 짝수 탭입니다.")
        else:
            st.success(f"탭 {i+1}은 홀수 탭입니다.")

# ============================================
# 실습 섹션
# ============================================
st.markdown("---")
st.header("🎯 실습해보세요!")

st.markdown("""
1. 5개 이상의 탭을 만들어보세요
2. 각 탭에 다른 종류의 컨텐츠를 넣어보세요
3. 탭 안에 Expander를 넣어보세요
4. 사용자 입력에 따라 동적으로 탭을 생성해보세요
5. 현재 앱(app.py)의 탭 구조를 분석해보세요
""")

# --------------------------------------------
# 실습 1: 프로필 카드 탭 (5개 탭)
# --------------------------------------------
st.subheader("실습 1: 프로필 카드 (5개 탭)")

profile_tabs = st.tabs(["👤 기본정보", "📚 학력", "💼 경력", "🛠️ 기술", "📞 연락처"])

with profile_tabs[0]:
    st.write("### 기본 정보")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://via.placeholder.com/150/4ECDC4/FFFFFF?text=Profile", width=150)
    with col2:
        st.write("**이름:** 홍길동")
        st.write("**생년월일:** 1995년 3월 15일")
        st.write("**주소:** 대구광역시 중구")

with profile_tabs[1]:
    st.write("### 학력 사항")
    education_df = pd.DataFrame({
        '기간': ['2014-2018', '2011-2014'],
        '학교': ['서울대학교', '대구고등학교'],
        '전공/계열': ['컴퓨터공학', '이과'],
        '학위': ['학사', '졸업']
    })
    st.dataframe(education_df, width="stretch", hide_index=True)

with profile_tabs[2]:
    st.write("### 경력 사항")
    st.write("**현재: 삼성전자 소프트웨어 엔지니어 (2020 ~ 현재)**")
    st.write("- AI 모델 개발 및 최적화")
    st.write("- 팀 리드 역할 수행")
    st.markdown("---")
    st.write("**이전: 네이버 인턴 (2019)**")
    st.write("- 검색 엔진 개선 프로젝트 참여")

with profile_tabs[3]:
    st.write("### 기술 스택")
    skills = {
        'Python': 95,
        'JavaScript': 80,
        'SQL': 85,
        'Machine Learning': 90,
        'Streamlit': 100
    }
    for skill, level in skills.items():
        st.write(f"**{skill}**")
        st.progress(level / 100)

with profile_tabs[4]:
    st.write("### 연락처")
    st.write("📧 이메일: hong@example.com")
    st.write("📱 전화: 010-1234-5678")
    st.write("🔗 GitHub: github.com/honggildong")
    st.write("💼 LinkedIn: linkedin.com/in/honggildong")

# --------------------------------------------
# 실습 2: 탭 + Expander 조합
# --------------------------------------------
st.subheader("실습 2: 탭 안에 Expander 넣기")

combo_tabs = st.tabs(["📖 Python 기초", "🔧 고급 기능", "🚀 실전 프로젝트"])

with combo_tabs[0]:
    st.write("### Python 기초 문법")

    with st.expander("변수와 자료형"):
        st.code("""
# 변수 선언
name = "홍길동"      # 문자열
age = 25             # 정수
height = 175.5       # 실수
is_student = True    # 불리언
        """, language="python")

    with st.expander("조건문"):
        st.code("""
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "C"
        """, language="python")

    with st.expander("반복문"):
        st.code("""
# for 문
for i in range(5):
    print(i)

# while 문
count = 0
while count < 5:
    print(count)
    count += 1
        """, language="python")

with combo_tabs[1]:
    st.write("### Python 고급 기능")

    with st.expander("리스트 컴프리헨션"):
        st.code("""
# 기본
squares = [x**2 for x in range(10)]

# 조건 포함
even_squares = [x**2 for x in range(10) if x % 2 == 0]
        """, language="python")

    with st.expander("데코레이터"):
        st.code("""
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"실행 시간: {time.time() - start:.2f}초")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)
        """, language="python")

with combo_tabs[2]:
    st.write("### 실전 프로젝트 예제")

    with st.expander("Streamlit 대시보드 만들기"):
        st.write("1. 데이터 로드 (`@st.cache_data`)")
        st.write("2. 필터링 UI 구성")
        st.write("3. 시각화 (Plotly/Folium)")
        st.write("4. 배포 (Streamlit Cloud)")

    with st.expander("프로젝트 구조"):
        st.code("""
my_project/
├── app.py           # 메인 앱
├── utils/
│   ├── data.py      # 데이터 처리
│   └── charts.py    # 차트 함수
├── data/
│   └── sample.csv   # 데이터 파일
└── requirements.txt # 의존성
        """)

# --------------------------------------------
# 실습 3: 실시간 데이터 대시보드
# --------------------------------------------
st.subheader("실습 3: 실시간 스타일 대시보드")

dashboard_tabs = st.tabs(["📊 실시간", "📈 트렌드", "⚙️ 설정"])

with dashboard_tabs[0]:
    st.write("### 실시간 데이터")

    # 시뮬레이션 데이터
    realtime_col1, realtime_col2, realtime_col3 = st.columns(3)

    with realtime_col1:
        cpu_usage = np.random.randint(20, 80)
        st.metric("CPU 사용률", f"{cpu_usage}%",
                  f"{np.random.randint(-5, 10)}%")

    with realtime_col2:
        memory_usage = np.random.randint(40, 70)
        st.metric("메모리 사용률", f"{memory_usage}%",
                  f"{np.random.randint(-3, 5)}%")

    with realtime_col3:
        network_speed = np.random.randint(100, 500)
        st.metric("네트워크 속도", f"{network_speed} Mbps",
                  f"{np.random.randint(-50, 100)} Mbps")

    # 실시간 차트 시뮬레이션
    chart_data = pd.DataFrame({
        '시간': pd.date_range(start='09:00', periods=20, freq='5min'),
        'CPU': np.random.randint(20, 80, 20),
        '메모리': np.random.randint(40, 70, 20)
    })
    st.line_chart(chart_data.set_index('시간'))

with dashboard_tabs[1]:
    st.write("### 주간 트렌드")

    trend_data = pd.DataFrame({
        '요일': ['월', '화', '수', '목', '금', '토', '일'],
        '방문자': [1200, 1400, 1100, 1600, 1800, 2200, 1900],
        '전환': [120, 140, 88, 192, 216, 286, 209]
    })

    st.bar_chart(trend_data.set_index('요일'))

    st.write("**주간 요약:**")
    st.write(f"- 총 방문자: {trend_data['방문자'].sum():,}명")
    st.write(f"- 총 전환: {trend_data['전환'].sum():,}건")
    st.write(f"- 평균 전환율: {(trend_data['전환'].sum() / trend_data['방문자'].sum() * 100):.1f}%")

with dashboard_tabs[2]:
    st.write("### 대시보드 설정")

    st.write("**알림 설정:**")
    cpu_alert = st.slider("CPU 알림 임계값:", 50, 100, 80, key="cpu_threshold")
    memory_alert = st.slider("메모리 알림 임계값:", 50, 100, 70, key="memory_threshold")

    st.write("**새로고침 설정:**")
    refresh_rate = st.selectbox("새로고침 주기:", ["5초", "10초", "30초", "1분"])

    st.write("**알림 수단:**")
    email_notify = st.checkbox("이메일 알림", value=True)
    slack_notify = st.checkbox("Slack 알림")

    if st.button("설정 저장"):
        st.success("설정이 저장되었습니다!")
        st.json({
            "cpu_threshold": cpu_alert,
            "memory_threshold": memory_alert,
            "refresh_rate": refresh_rate,
            "notifications": {
                "email": email_notify,
                "slack": slack_notify
            }
        })

# --------------------------------------------
# 실습 4: 동적 탭 생성
# --------------------------------------------
st.subheader("실습 4: 동적 탭 생성기")

st.write("**탭 이름을 입력하세요 (쉼표로 구분):**")
tab_names_input = st.text_input(
    "탭 이름들:",
    value="홈, 소개, 서비스, 연락처",
    key="dynamic_tabs_input"
)

if tab_names_input:
    custom_tab_names = [name.strip() for name in tab_names_input.split(",") if name.strip()]

    if len(custom_tab_names) >= 2:
        custom_tabs = st.tabs(custom_tab_names)

        for i, tab in enumerate(custom_tabs):
            with tab:
                st.write(f"### {custom_tab_names[i]} 탭")
                st.info(f"이것은 '{custom_tab_names[i]}' 탭의 내용입니다.")
                st.write(f"탭 인덱스: {i}")

                # 각 탭에 다른 위젯 추가
                st.text_area(f"{custom_tab_names[i]} 메모:", key=f"memo_{i}")
    else:
        st.warning("최소 2개 이상의 탭 이름을 입력해주세요.")

with st.expander("💡 탭 사용 팁"):
    st.markdown("""
    **언제 사용하면 좋을까?**
    - 관련된 여러 카테고리의 정보
    - 데이터의 다른 뷰(데이터, 차트, 통계 등)
    - 워크플로우의 단계별 구분
    - 설정 화면의 섹션 구분

    **주의사항:**
    - 탭이 너무 많으면 혼란스러움 (최대 5-7개 권장)
    - 중요한 정보는 첫 번째 탭에
    - 탭 이름은 명확하고 간결하게
    - 모바일에서도 잘 보이도록 고려

    **Expander vs Tabs:**
    - Expander: 같은 페이지에서 정보 숨기기/보이기
    - Tabs: 서로 다른 뷰나 카테고리 전환
    - 함께 사용 가능 (탭 안에 expander)
    """)
