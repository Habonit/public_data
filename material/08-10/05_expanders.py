"""
예제 5: 확장 가능한 섹션 (Expanders)

이 예제에서는 st.expander를 사용하여 컨텐츠를 접었다 펼칠 수 있는 방법을 학습합니다.
"""
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="확장 가능한 섹션",
    page_icon="📂",
    layout="wide"
)

st.title("📂 확장 가능한 섹션 (Expanders)")

# ============================================
# 1. 기본 Expander
# ============================================
st.header("1. 기본 Expander")

st.markdown("""
`st.expander()`를 사용하면 많은 정보를 깔끔하게 정리할 수 있습니다.
사용자가 필요할 때만 펼쳐서 볼 수 있습니다.
""")

with st.expander("📖 자세히 보기"):
    st.write("""
    Expander는 다음과 같은 경우에 유용합니다:
    - 상세 정보를 숨기고 싶을 때
    - 페이지가 너무 길어질 때
    - 선택적 정보를 제공할 때
    - FAQ나 도움말 섹션
    """)
    st.info("이 컨텐츠는 expander 안에 있습니다.")

# ============================================
# 2. 기본 확장 상태 설정
# ============================================
st.header("2. 기본 확장 상태 설정")

col1, col2 = st.columns(2)

with col1:
    with st.expander("기본적으로 접힌 상태", expanded=False):
        st.write("이 expander는 기본적으로 접혀있습니다.")
        st.write("사용자가 클릭해야 내용이 보입니다.")

with col2:
    with st.expander("기본적으로 펼쳐진 상태", expanded=True):
        st.write("이 expander는 기본적으로 펼쳐져 있습니다.")
        st.write("중요한 정보는 펼친 상태로 표시할 수 있습니다.")

# ============================================
# 3. 다양한 컨텐츠 담기
# ============================================
st.header("3. Expander에 다양한 컨텐츠 담기")

# 데이터프레임
with st.expander("📊 데이터프레임 보기"):
    df = pd.DataFrame({
        '이름': ['김철수', '이영희', '박민수'],
        '나이': [25, 30, 35],
        '부서': ['개발', '디자인', '마케팅']
    })
    st.dataframe(df, width="stretch")

# 차트
with st.expander("📈 차트 보기"):
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['A', 'B', 'C']
    )
    st.line_chart(chart_data)

# 코드
with st.expander("💻 코드 예시"):
    st.code("""
def hello(name):
    return f"Hello, {name}!"

print(hello("Streamlit"))
    """, language="python")

# 이미지
with st.expander("🖼️ 이미지 보기"):
    st.image("https://via.placeholder.com/600x200/4ECDC4/FFFFFF?text=Sample+Image",
             width="stretch")

# ============================================
# 4. 중첩된 Expander
# ============================================
st.header("4. 중첩된 Expander")

st.markdown("""
Expander 안에 또 다른 Expander를 넣을 수 있습니다.
계층적인 정보 구조에 유용합니다.
""")

with st.expander("1단계: 프로그래밍 언어"):
    st.write("여러 프로그래밍 언어를 선택하세요")

    with st.expander("2단계: Python"):
        st.write("Python은 다양한 분야에서 사용됩니다")

        with st.expander("3단계: 데이터 분석"):
            st.write("- Pandas")
            st.write("- NumPy")
            st.write("- Matplotlib")

        with st.expander("3단계: 웹 개발"):
            st.write("- Django")
            st.write("- Flask")
            st.write("- FastAPI")

    with st.expander("2단계: JavaScript"):
        st.write("JavaScript는 웹 개발의 핵심입니다")

        with st.expander("3단계: 프론트엔드"):
            st.write("- React")
            st.write("- Vue")
            st.write("- Angular")

# ============================================
# 5. 실전 예제: FAQ 섹션
# ============================================
st.header("5. 실전 예제: FAQ 섹션")

st.markdown("---")
st.subheader("자주 묻는 질문 (FAQ)")

faqs = [
    {
        "question": "Streamlit이란 무엇인가요?",
        "answer": """
        Streamlit은 Python으로 데이터 앱을 빠르게 만들 수 있는 오픈소스 프레임워크입니다.
        별도의 프론트엔드 개발 없이 Python 스크립트만으로 웹 앱을 만들 수 있습니다.
        """
    },
    {
        "question": "Streamlit은 무료인가요?",
        "answer": """
        네, Streamlit은 완전 무료 오픈소스입니다.
        Streamlit Community Cloud에 무료로 배포할 수도 있습니다.
        """
    },
    {
        "question": "어떤 데이터 형식을 지원하나요?",
        "answer": """
        Streamlit은 다양한 데이터 형식을 지원합니다:
        - CSV, Excel (pandas를 통해)
        - JSON
        - 이미지 (PNG, JPG, etc.)
        - 비디오
        - 오디오
        - Pandas DataFrame
        - NumPy 배열
        """
    },
    {
        "question": "데이터베이스와 연동할 수 있나요?",
        "answer": """
        네, 가능합니다. Python의 데이터베이스 라이브러리를 사용하면 됩니다:
        - SQLite (sqlite3)
        - PostgreSQL (psycopg2)
        - MySQL (mysql-connector-python)
        - MongoDB (pymongo)
        """
    },
    {
        "question": "배포는 어떻게 하나요?",
        "answer": """
        여러 방법으로 배포할 수 있습니다:
        1. Streamlit Community Cloud (무료)
        2. Heroku
        3. AWS, GCP, Azure
        4. Docker 컨테이너
        """
    }
]

for i, faq in enumerate(faqs):
    with st.expander(f"Q{i+1}. {faq['question']}"):
        st.write(faq['answer'])

# ============================================
# 6. 실전 예제: 데이터 탐색 도구
# ============================================
st.header("6. 실전 예제: 데이터 탐색 도구")

st.markdown("---")

# 샘플 데이터 생성
data = pd.DataFrame({
    '제품': ['노트북', '마우스', '키보드', '모니터', '헤드셋'],
    '카테고리': ['전자제품', '주변기기', '주변기기', '전자제품', '주변기기'],
    '가격': [1500000, 25000, 80000, 350000, 120000],
    '재고': [15, 150, 80, 25, 60],
    '평점': [4.5, 4.2, 4.7, 4.4, 4.3]
})

st.subheader("제품 데이터 탐색")

# 기본 정보는 항상 표시
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("총 제품 수", len(data))
with col2:
    st.metric("카테고리 수", data['카테고리'].nunique())
with col3:
    st.metric("평균 가격", f"₩{data['가격'].mean():,.0f}")
with col4:
    st.metric("평균 평점", f"{data['평점'].mean():.2f}")

# 상세 정보는 expander 안에
with st.expander("📋 전체 데이터 보기", expanded=False):
    st.dataframe(data, width="stretch")

with st.expander("📊 카테고리별 통계", expanded=False):
    category_stats = data.groupby('카테고리').agg({
        '제품': 'count',
        '가격': 'mean',
        '재고': 'sum',
        '평점': 'mean'
    }).round(2)
    category_stats.columns = ['제품 수', '평균 가격', '총 재고', '평균 평점']
    st.dataframe(category_stats, width="stretch")

with st.expander("📈 가격 분포", expanded=False):
    st.bar_chart(data.set_index('제품')['가격'])

with st.expander("⭐ 평점 분포", expanded=False):
    st.bar_chart(data.set_index('제품')['평점'])

# ============================================
# 실습 섹션
# ============================================
st.markdown("---")
st.header("🎯 실습해보세요!")

st.markdown("""
1. FAQ 형식의 정보 페이지를 만들어보세요
2. 3단계 이상의 중첩 expander를 만들어보세요
3. Expander에 차트와 데이터를 함께 넣어보세요
4. 사용자 입력에 따라 동적으로 expander를 생성해보세요
""")

# --------------------------------------------
# 실습 1: 나만의 FAQ 만들기
# --------------------------------------------
st.subheader("실습 1: 나만의 FAQ 만들기")

st.write("**FAQ 항목을 추가해보세요:**")

# FAQ 입력
faq_col1, faq_col2 = st.columns(2)

with faq_col1:
    new_question = st.text_input("질문:", placeholder="예: Streamlit을 어떻게 설치하나요?")
with faq_col2:
    new_answer = st.text_area("답변:", placeholder="예: pip install streamlit 명령어로 설치합니다.", height=100)

# 기본 FAQ 데이터
default_faqs = [
    {"q": "Streamlit 앱을 어떻게 실행하나요?", "a": "`streamlit run app.py` 명령어로 실행합니다."},
    {"q": "앱을 배포하려면 어떻게 해야 하나요?", "a": "Streamlit Community Cloud에 무료로 배포할 수 있습니다."},
    {"q": "데이터를 어떻게 불러오나요?", "a": "`pandas`를 사용하여 CSV, Excel 등 다양한 형식의 데이터를 불러올 수 있습니다."}
]

# FAQ 표시
st.write("**FAQ 목록:**")
for i, faq in enumerate(default_faqs):
    with st.expander(f"Q{i+1}. {faq['q']}"):
        st.write(faq['a'])

# 사용자 입력 FAQ 추가
if new_question and new_answer:
    with st.expander(f"Q{len(default_faqs)+1}. {new_question}"):
        st.write(new_answer)
    st.success("새 FAQ가 추가되었습니다!")

# --------------------------------------------
# 실습 2: 제품 카탈로그 (중첩 Expander)
# --------------------------------------------
st.subheader("실습 2: 제품 카탈로그 (중첩 구조)")

with st.expander("🛍️ 전자제품 카탈로그", expanded=True):
    st.write("카테고리를 선택하세요")

    with st.expander("📱 스마트폰"):
        st.write("다양한 스마트폰 제품")

        with st.expander("삼성 갤럭시"):
            st.write("- Galaxy S24 Ultra: ₩1,650,000")
            st.write("- Galaxy S24+: ₩1,350,000")
            st.write("- Galaxy S24: ₩1,150,000")

        with st.expander("애플 아이폰"):
            st.write("- iPhone 15 Pro Max: ₩1,890,000")
            st.write("- iPhone 15 Pro: ₩1,550,000")
            st.write("- iPhone 15: ₩1,250,000")

    with st.expander("💻 노트북"):
        st.write("다양한 노트북 제품")

        with st.expander("맥북"):
            st.write("- MacBook Pro 16: ₩3,490,000")
            st.write("- MacBook Air M3: ₩1,690,000")

        with st.expander("삼성 갤럭시북"):
            st.write("- Galaxy Book4 Ultra: ₩3,290,000")
            st.write("- Galaxy Book4 Pro: ₩2,190,000")

# --------------------------------------------
# 실습 3: 데이터 분석 리포트
# --------------------------------------------
st.subheader("실습 3: 데이터 분석 리포트")

# 샘플 데이터
analysis_data = pd.DataFrame({
    '월': ['1월', '2월', '3월', '4월', '5월', '6월'],
    '매출': [1200, 1350, 1100, 1500, 1800, 2100],
    '비용': [800, 850, 750, 900, 1000, 1100],
    '이익': [400, 500, 350, 600, 800, 1000]
})

with st.expander("📊 월별 매출 현황", expanded=False):
    st.dataframe(analysis_data, width="stretch")
    st.bar_chart(analysis_data.set_index('월')['매출'])

with st.expander("📈 이익 추이", expanded=False):
    st.line_chart(analysis_data.set_index('월')['이익'])
    total_profit = analysis_data['이익'].sum()
    avg_profit = analysis_data['이익'].mean()
    st.metric("총 이익", f"₩{total_profit:,}만", f"월평균 ₩{avg_profit:,.0f}만")

with st.expander("📋 상세 분석", expanded=False):
    st.write("**기술 통계:**")
    st.dataframe(analysis_data.describe(), width="stretch")

    st.write("**인사이트:**")
    max_month = analysis_data.loc[analysis_data['매출'].idxmax(), '월']
    min_month = analysis_data.loc[analysis_data['매출'].idxmin(), '월']
    st.info(f"- 최고 매출월: {max_month}")
    st.warning(f"- 최저 매출월: {min_month}")

# --------------------------------------------
# 실습 4: 동적 Expander 생성
# --------------------------------------------
st.subheader("실습 4: 동적 Expander 생성")

num_expanders = st.slider("생성할 Expander 개수:", 1, 10, 3, key="dynamic_exp_slider")

expander_type = st.radio(
    "Expander 타입:",
    ["숫자 카드", "색상 카드", "진행률 카드"],
    horizontal=True
)

for i in range(num_expanders):
    if expander_type == "숫자 카드":
        with st.expander(f"📌 항목 {i+1}"):
            st.metric(f"값 {i+1}", f"{(i+1) * 100:,}", f"+{(i+1) * 10}%")

    elif expander_type == "색상 카드":
        colors = ["🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "⚫", "⚪", "🟤", "🩷"]
        with st.expander(f"{colors[i % len(colors)]} 색상 {i+1}"):
            st.write(f"이것은 {i+1}번째 색상 카드입니다.")
            progress = (i + 1) / num_expanders
            st.progress(progress)

    elif expander_type == "진행률 카드":
        with st.expander(f"📊 프로젝트 {i+1}"):
            progress_val = np.random.randint(10, 100)
            st.progress(progress_val / 100)
            st.write(f"진행률: {progress_val}%")
            if progress_val >= 80:
                st.success("거의 완료!")
            elif progress_val >= 50:
                st.info("진행 중...")
            else:
                st.warning("시작 단계")

with st.expander("💡 Expander 사용 팁"):
    st.markdown("""
    **언제 사용하면 좋을까?**
    - 페이지가 너무 길어질 때
    - 선택적 정보 (모든 사용자가 볼 필요 없는 정보)
    - 상세 설명이나 도움말
    - 디버그 정보나 로그

    **주의사항:**
    - 너무 많은 expander는 피하기 (사용자 혼란)
    - 중요한 정보는 항상 보이게 하기
    - 일관된 레이블 사용

    **성능:**
    - Expander 안의 코드는 접혀있어도 실행됨
    - 무거운 연산은 버튼과 함께 사용하는 것이 좋음
    """)
