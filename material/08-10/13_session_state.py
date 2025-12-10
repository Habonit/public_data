"""
예제 13: 세션 상태 및 기타 필수 기능

이 예제에서는 st.session_state와 파일 업로드/다운로드, 사이드바 등을 학습합니다.
"""
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import io

st.set_page_config(
    page_title="세션 상태 및 필수 기능",
    page_icon="🔧",
    layout="wide"
)

st.title("🔧 세션 상태 및 기타 필수 기능")

st.markdown("""
Streamlit 앱을 만들 때 꼭 알아야 할 중요한 기능들을 학습합니다.
""")

# 세션 스테이는 상태값 보관용이라고 생각하면 됩니다. 
# ============================================
# 1. Session State - 상태 관리
# ============================================
st.header("1. Session State - 상태 관리")

st.markdown("""
**중요!** Streamlit은 사용자가 위젯과 상호작용할 때마다 스크립트를 처음부터 다시 실행합니다.
`st.session_state`를 사용하면 재실행 사이에 데이터를 유지할 수 있습니다.
""")

# 초기화

test_counter = 0
if 'counter' not in st.session_state:
    st.session_state.counter = 0

if 'name' not in st.session_state:
    st.session_state.name = ''

# 카운터 예제
st.subheader("1.1 간단한 카운터")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("➕ 증가"):
        st.session_state.counter += 1
        test_counter += 1

with col2:
    if st.button("➖ 감소"):
        st.session_state.counter -= 1
        test_counter -= 1
with col3:
    if st.button("🔄 초기화"):
        st.session_state.counter = 0
        test_counter = 0
st.metric("현재 카운터 값", st.session_state.counter)
st.metric("현재 카운터 값", test_counter)
# 입력값 유지
st.subheader("1.2 입력값 유지")

# 일반적인 방법 (재실행 시 초기화됨)
st.write("**Session State 없이:**")
normal_input = st.text_input("이름 입력 (Session State 없음):", key="normal")
st.write(f"입력: {normal_input}")
st.caption("다른 위젯을 클릭하면 초기화될 수 있습니다")

st.markdown("---")

# Session State 사용
st.write("**Session State 사용:**")

def update_name():
    st.session_state.name = st.session_state.name_input

name_input = st.text_input(
    "이름 입력 (Session State):",
    key="name_input",
    on_change=update_name
)

st.write(f"저장된 이름: **{st.session_state.name}**")
st.success("다른 위젯을 클릭해도 유지됩니다!")

# ============================================
# 2. Session State 고급 활용
# ============================================
st.header("2. Session State 고급 활용")

st.subheader("2.1 장바구니 예제")

# 초기화
if 'cart' not in st.session_state:
    st.session_state.cart = []

# 상품 목록
products = {
    "노트북": 1500000,
    "마우스": 25000,
    "키보드": 80000,
    "모니터": 350000,
    "헤드셋": 120000
}

col1, col2 = st.columns([2, 1])

with col1:
    st.write("### 상품 목록")

    for product, price in products.items():
        col_a, col_b = st.columns([3, 1])
        with col_a:
            st.write(f"**{product}** - ₩{price:,}")
        with col_b:
            if st.button(f"추가", key=f"add_{product}"):
                st.session_state.cart.append({
                    'product': product,
                    'price': price
                })
                st.success(f"{product} 추가!")

with col2:
    st.write("### 장바구니")

    if st.session_state.cart:
        total = 0
        for idx, item in enumerate(st.session_state.cart):
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.write(f"{item['product']}")
            with col_b:
                if st.button("❌", key=f"remove_{idx}"):
                    st.session_state.cart.pop(idx)
                    st.rerun()
            total += item['price']

        st.markdown("---")
        st.write(f"**총액: ₩{total:,}**")

        if st.button("🛒 주문하기"):
            st.balloons()
            st.success(f"주문 완료! 총 {len(st.session_state.cart)}개 상품")
            st.session_state.cart = []
    else:
        st.info("장바구니가 비어있습니다")

# ============================================
# 3. 파일 업로드
# ============================================
st.header("3. 파일 업로드")

st.markdown("""
사용자가 파일을 업로드하여 분석할 수 있습니다.
""")

uploaded_file = st.file_uploader(
    "CSV 파일을 업로드하세요",
    type=['csv'],
    help="CSV 형식의 파일만 업로드 가능합니다"
)

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        st.success(f"✅ 파일 업로드 성공: {uploaded_file.name}")

        # 파일 정보
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("행 수", len(df))
        with col2:
            st.metric("열 수", len(df.columns))
        with col3:
            st.metric("파일 크기", f"{uploaded_file.size / 1024:.1f} KB")

        # 데이터 미리보기
        st.write("### 데이터 미리보기")
        st.dataframe(df.head(10), width="stretch")

        # 기본 통계
        with st.expander("📊 기본 통계"):
            st.dataframe(df.describe(), width="stretch")

    except Exception as e:
        st.error(f"❌ 파일 읽기 오류: {str(e)}")
else:
    st.info("⬆️ CSV 파일을 업로드하면 자동으로 분석됩니다")

# ============================================
# 4. 파일 다운로드
# ============================================
st.header("4. 파일 다운로드")

st.markdown("""
생성한 데이터를 다운로드할 수 있습니다.
""")

# 샘플 데이터 생성
if st.button("샘플 데이터 생성"):
    sample_df = pd.DataFrame({
        '날짜': pd.date_range('2024-01-01', periods=10),
        '판매량': np.random.randint(10, 100, 10),
        '매출': np.random.randint(100000, 1000000, 10)
    })

    st.session_state.sample_data = sample_df
    st.success("✅ 샘플 데이터 생성 완료!")

if 'sample_data' in st.session_state:
    df_download = st.session_state.sample_data

    st.dataframe(df_download, width="stretch")

    col1, col2 = st.columns(2)

    with col1:
        # CSV 다운로드
        csv = df_download.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 CSV 다운로드",
            data=csv,
            file_name=f'data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
            mime='text/csv'
        )

    with col2:
        # Excel 다운로드
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_download.to_excel(writer, index=False, sheet_name='Data')
        excel_data = output.getvalue()

        st.download_button(
            label="📥 Excel 다운로드",
            data=excel_data,
            file_name=f'data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

# ============================================
# 5. 사이드바 활용
# ============================================
st.header("5. 사이드바 활용")

st.markdown("""
사이드바는 필터나 설정을 배치하기 좋은 공간입니다.
현재 앱에서는 사용하지 않지만, 유용한 패턴입니다.
""")

# 사이드바에 위젯 추가
st.sidebar.header("⚙️ 설정")

theme = st.sidebar.selectbox(
    "테마 선택",
    ["밝은 테마", "어두운 테마", "자동"]
)

show_advanced = st.sidebar.checkbox("고급 옵션 표시", value=False)

if show_advanced:
    st.sidebar.slider("투명도", 0, 100, 50)
    st.sidebar.multiselect(
        "관심 카테고리",
        ["기술", "비즈니스", "과학", "예술"]
    )

st.sidebar.markdown("---")
st.sidebar.info("💡 사이드바는 필터와 설정에 적합합니다")

# 메인 영역에 표시
st.write(f"선택된 테마: **{theme}**")
if show_advanced:
    st.success("고급 옵션이 활성화되었습니다")

# ============================================
# 6. 이미지 표시
# ============================================
st.header("6. 이미지 표시")

col1, col2 = st.columns(2)

with col1:
    st.subheader("URL 이미지")
    st.image(
        "https://via.placeholder.com/400x300/FF6B6B/FFFFFF?text=Streamlit",
        caption="플레이스홀더 이미지",
        width="stretch"
    )

with col2:
    st.subheader("업로드 이미지")
    image_file = st.file_uploader(
        "이미지 업로드",
        type=['png', 'jpg', 'jpeg'],
        key="image_upload"
    )

    if image_file:
        st.image(
            image_file,
            caption=f"업로드: {image_file.name}",
            width="stretch"
        )

# ============================================
# 7. 기타 유용한 위젯
# ============================================
st.header("7. 기타 유용한 위젯")

col1, col2 = st.columns(2)

with col1:
    st.subheader("색상 선택")
    color = st.color_picker("색상 선택", "#FF6B6B")
    st.write(f"선택된 색상: {color}")
    st.markdown(f"<div style='background-color: {color}; padding: 20px; border-radius: 5px;'>샘플 박스</div>",
                unsafe_allow_html=True)

with col2:
    st.subheader("카메라 입력")
    camera_photo = st.camera_input("사진 찍기")
    if camera_photo:
        st.success("사진이 촬영되었습니다!")

# ============================================
# 8. 실전 예제: 간단한 Todo 앱
# ============================================
st.header("8. 실전 예제: Todo 앱")

st.markdown("---")

# 초기화
if 'todos' not in st.session_state:
    st.session_state.todos = []

# Todo 추가
with st.form("add_todo"):
    new_todo = st.text_input("새로운 할 일")
    submitted = st.form_submit_button("➕ 추가")

    if submitted and new_todo:
        st.session_state.todos.append({
            'task': new_todo,
            'done': False,
            'created_at': datetime.now()
        })
        st.success(f"'{new_todo}' 추가됨!")

# Todo 목록
st.subheader(f"할 일 목록 ({len(st.session_state.todos)}개)")

if st.session_state.todos:
    for idx, todo in enumerate(st.session_state.todos):
        col1, col2, col3 = st.columns([1, 6, 1])

        with col1:
            done = st.checkbox(
                "완료",
                value=todo['done'],
                key=f"todo_{idx}",
                label_visibility="collapsed"
            )
            if done != todo['done']:
                st.session_state.todos[idx]['done'] = done
                st.rerun()

        with col2:
            if todo['done']:
                st.markdown(f"~~{todo['task']}~~")
            else:
                st.write(todo['task'])
            st.caption(f"추가: {todo['created_at'].strftime('%Y-%m-%d %H:%M')}")

        with col3:
            if st.button("🗑️", key=f"delete_{idx}"):
                st.session_state.todos.pop(idx)
                st.rerun()

    # 통계
    completed = sum(1 for todo in st.session_state.todos if todo['done'])
    st.progress(completed / len(st.session_state.todos))
    st.write(f"완료: {completed} / {len(st.session_state.todos)}")

else:
    st.info("할 일이 없습니다. 위에서 추가해보세요!")

# ============================================
# 실습 섹션
# ============================================
st.markdown("---")
st.header("🎯 실습해보세요!")

st.markdown("""
1. Session State로 로그인 상태 관리 구현
2. 업로드한 CSV 파일을 가공하여 다운로드
3. 사이드바로 복잡한 필터 시스템 구현
4. Todo 앱에 수정 기능 추가
5. 이미지 업로드 후 Pillow로 필터 적용
""")

with st.expander("💡 Session State 핵심 개념"):
    st.markdown("""
    **Session State란?**
    - 앱 재실행 사이에 데이터를 유지하는 방법
    - 딕셔너리처럼 사용: `st.session_state.key = value`
    - 위젯의 상태도 저장 가능

    **주요 사용 사례:**
    1. **카운터/점수** - 클릭 횟수, 게임 점수 등
    2. **사용자 입력 유지** - 폼 데이터, 검색어 등
    3. **로그인 상태** - 인증 정보 유지
    4. **장바구니/즐겨찾기** - 선택 항목 목록
    5. **다단계 폼** - 단계별 데이터 저장

    **초기화 패턴:**
    ```python
    if 'my_var' not in st.session_state:
        st.session_state.my_var = initial_value
    ```

    **콜백 함수:**
    ```python
    def update_value():
        st.session_state.result = st.session_state.input * 2

    st.text_input("입력", key="input", on_change=update_value)
    ```

    **주의사항:**
    - 너무 큰 데이터는 저장하지 않기 (메모리 문제)
    - 필요없는 상태는 삭제: `del st.session_state.key`
    - `st.rerun()`으로 강제 재실행 가능
    """)

with st.expander("💡 파일 업로드/다운로드 팁"):
    st.markdown("""
    **업로드:**
    - `st.file_uploader(type=['csv', 'xlsx', 'json'])`
    - 여러 파일: `accept_multiple_files=True`
    - 업로드된 파일은 BytesIO 객체

    **다운로드:**
    - CSV: `df.to_csv().encode('utf-8-sig')`
    - Excel: `pd.ExcelWriter` 사용
    - JSON: `json.dumps().encode()`
    - 파일명에 타임스탬프 추가 권장

    **현재 앱에서:**
    - 현재는 미사용
    - 추가 가능: 데이터 내보내기 기능
    - 추가 가능: 사용자 데이터 업로드
    """)

# ============================================
# 추가 지식: @st.cache_data vs session_state
# ============================================
st.markdown("---")
st.header("📚 알아두면 좋은 기능: @st.cache_data vs session_state")

st.markdown("""
### 🤔 둘 다 데이터를 저장하는데, 뭐가 다를까?

| 구분 | `@st.cache_data` | `st.session_state` |
|------|------------------|-------------------|
| **비유** | 🏢 공용 냉장고 | 🔐 개인 사물함 |
| **범위** | 모든 사용자 공유 | 해당 사용자만 |
| **목적** | 계산 결과 재사용 (성능) | 사용자별 상태 저장 |
| **수명** | 앱 실행 중 유지 | 브라우저 탭 열려있는 동안 |
""")

st.subheader("💻 코드로 이해하기")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**@st.cache_data (공용 냉장고)**")
    st.code("""
# 한 번 요리해두면 모든 손님이 먹음
@st.cache_data
def load_product_list():
    # 무거운 작업 (DB 조회, 파일 읽기)
    return pd.read_csv("products.csv")

# 사용자 A가 호출 → 파일 읽음, 캐시 저장
# 사용자 B가 호출 → 캐시에서 바로 반환!
df = load_product_list()
""", language="python")

with col2:
    st.markdown("**session_state (개인 사물함)**")
    st.code("""
# 각 손님이 자기 물건만 보관
if 'my_cart' not in st.session_state:
    st.session_state.my_cart = []

# 사용자 A의 장바구니: ["노트북"]
# 사용자 B의 장바구니: ["마우스", "키보드"]
# → 서로 다른 공간!

st.session_state.my_cart.append("새 상품")
""", language="python")

st.markdown("---")
st.subheader("🎮 직접 체험해보기: 파일 업로드 캐싱 비교")

st.markdown("""
**상황**: CSV 파일을 업로드하면 DataFrame으로 변환해야 합니다.
두 가지 방법으로 구현할 수 있습니다.
""")

# 탭으로 두 방식 비교
cache_tab, session_tab = st.tabs(["방법 1: @st.cache_data", "방법 2: session_state"])

with cache_tab:
    st.markdown("""
    ### @st.cache_data 방식

    ```python
    @st.cache_data
    def load_csv(uploaded_file):
        return pd.read_csv(uploaded_file)
    ```

    **특징:**
    - ✅ 같은 파일 재업로드 시 캐시에서 즉시 반환
    - ⚠️ 다른 사용자가 같은 파일 올리면 결과 공유됨
    - 📁 적합: 공통 데이터 파일, 변하지 않는 파일
    """)

    @st.cache_data
    def load_csv_cached(uploaded_file):
        return pd.read_csv(uploaded_file)

    cache_file = st.file_uploader("CSV 업로드 (cache_data 방식)", type="csv", key="cache_upload")

    if cache_file:
        df_cached = load_csv_cached(cache_file)
        st.success(f"✅ 로드 완료: {len(df_cached)}행 (캐시 사용)")
        st.dataframe(df_cached.head(5), width="stretch")

with session_tab:
    st.markdown("""
    ### session_state 방식

    ```python
    if uploaded_file:
        if 'df' not in st.session_state or st.session_state.file_name != uploaded_file.name:
            st.session_state.df = pd.read_csv(uploaded_file)
            st.session_state.file_name = uploaded_file.name
    ```

    **특징:**
    - ✅ 사용자별로 독립적인 데이터 저장
    - ✅ 다른 사용자와 절대 공유 안됨
    - 📁 적합: 사용자가 각자 업로드하는 파일
    """)

    session_file = st.file_uploader("CSV 업로드 (session_state 방식)", type="csv", key="session_upload")

    if session_file:
        # 파일이 바뀌었을 때만 새로 로드
        if 'user_df' not in st.session_state or st.session_state.get('user_file_name') != session_file.name:
            st.session_state.user_df = pd.read_csv(session_file)
            st.session_state.user_file_name = session_file.name
            st.info("📂 새 파일 로드됨")
        else:
            st.info("💾 session_state에서 불러옴 (재로드 안함)")

        st.success(f"✅ 로드 완료: {len(st.session_state.user_df)}행")
        st.dataframe(st.session_state.user_df.head(5), width="stretch")

st.markdown("---")
st.subheader("📊 실제 시나리오별 선택 가이드")

st.markdown("""
| 시나리오 | 추천 방식 | 이유 |
|----------|-----------|------|
| 앱에서 제공하는 고정 CSV 로드 | `@st.cache_data` | 모든 사용자가 같은 데이터, 한 번만 로드 |
| 사용자가 각자 파일 업로드 | `session_state` | 사용자별 독립 데이터 필요 |
| API에서 공통 데이터 fetch | `@st.cache_data` | 같은 요청 반복 방지 |
| 사용자 장바구니, 설정 | `session_state` | 개인화 데이터 |
| 무거운 ML 모델 로딩 | `@st.cache_resource` | 모델은 공유해도 OK |
""")

st.subheader("✏️ 실습 과제")

st.markdown("""
1. **기본 실습**: 위의 두 탭에서 같은 CSV 파일을 각각 업로드해보세요.
   - 힌트: `data/` 폴더의 CSV 파일 사용

2. **비교 실습**: 브라우저 새 탭을 열어서 같은 앱에 접속해보세요.
   - `session_state` 방식의 데이터가 공유되는지 확인
   - (실제로는 각 탭이 별도 세션이라 공유 안됨)

3. **응용 실습**: 아래 코드를 완성하세요.
""")

with st.expander("💡 실습 3: 코드 완성하기"):
    st.code("""
# 문제: 사용자가 업로드한 파일을 session_state에 저장하고,
# 파일명이 같으면 재로드하지 않도록 구현하세요.

uploaded = st.file_uploader("CSV 업로드", type="csv")

if uploaded:
    # TODO: 여기를 완성하세요
    # 1. session_state에 'uploaded_df'가 없거나
    # 2. 저장된 파일명이 현재 파일명과 다르면
    # → 새로 로드

    pass  # 이 부분을 구현
""", language="python")

    st.markdown("**정답:**")
    st.code("""
uploaded = st.file_uploader("CSV 업로드", type="csv")

if uploaded:
    # 파일이 없거나 파일명이 바뀌었으면 새로 로드
    if 'uploaded_df' not in st.session_state or \\
       st.session_state.get('uploaded_name') != uploaded.name:

        st.session_state.uploaded_df = pd.read_csv(uploaded)
        st.session_state.uploaded_name = uploaded.name
        st.success("새 파일 로드!")

    # session_state에서 데이터 사용
    df = st.session_state.uploaded_df
    st.dataframe(df)
""", language="python")

st.markdown("""
---
### 📝 핵심 정리

```
@st.cache_data = "이 계산 비싸니까 결과 저장해두자" (성능 최적화)
session_state  = "이 사용자 데이터 기억해두자" (상태 관리)
```

**선택 기준:**
- 🤝 **공유해도 되는 데이터** → `@st.cache_data`
- 🔒 **사용자별 개인 데이터** → `session_state`
""")
