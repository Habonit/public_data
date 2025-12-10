"""
예제 4: 사용자 입력 위젯 (User Input Widgets)

이 예제에서는 다양한 사용자 입력 위젯을 학습합니다.
"""
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="사용자 입력 위젯",
    page_icon="🎛️",
    layout="wide"
)

st.title("🎛️ 사용자 입력 위젯")

# ============================================
# 1. 버튼 (Button)
# ============================================
st.header("1. 버튼 (Button)")

st.markdown("""
버튼은 클릭했을 때만 True를 반환하는 일회성 위젯입니다.
""")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("일반 버튼"):
        st.success("버튼이 클릭되었습니다!")

with col2:
    if st.button("🎨 아이콘 버튼"):
        st.info("아이콘이 있는 버튼도 만들 수 있습니다")

with col3:
    if st.button("비활성화됨", disabled=True):
        st.write("이 코드는 실행되지 않습니다")

# ============================================
# 2. 선택 박스 (Selectbox)
# ============================================
st.header("2. 선택 박스 (Selectbox)")

st.markdown("""
드롭다운 메뉴에서 하나의 옵션을 선택합니다.
""")

city = st.selectbox(
    "도시를 선택하세요:",
    options=["서울", "부산", "대구", "인천", "광주", "대전"],
    index=2,  # 기본 선택 (대구)
    key="city_select"
)

st.write(f"선택된 도시: **{city}**")

# 인덱스 없이 사용
dept = st.selectbox(
    "부서를 선택하세요:",
    ["개발", "디자인", "마케팅", "영업"]
)

# ============================================
# 3. 다중 선택 (Multiselect)
# ============================================
st.header("3. 다중 선택 (Multiselect)")

st.markdown("""
여러 개의 옵션을 동시에 선택할 수 있습니다.
""")

selected_fruits = st.multiselect(
    "좋아하는 과일을 선택하세요:",
    options=["사과", "바나나", "오렌지", "포도", "딸기", "수박"],
    default=["사과", "바나나"]  # 기본 선택
)

st.write(f"선택된 과일 ({len(selected_fruits)}개):", selected_fruits)

if selected_fruits:
    st.success(f"좋은 선택입니다! {', '.join(selected_fruits)}는 건강에 좋습니다.")
else:
    st.warning("최소 하나의 과일을 선택해주세요.")

# ============================================
# 4. 슬라이더 (Slider)
# ============================================
st.header("4. 슬라이더 (Slider)")

st.markdown("""
숫자 범위에서 값을 선택합니다.
""")

col1, col2 = st.columns(2)

with col1:
    age = st.slider(
        "나이를 선택하세요:",
        min_value=0,
        max_value=100,
        value=25,  # 기본값
        step=5     # 증가 단위
    )
    st.write(f"선택된 나이: **{age}세**")

with col2:
    # 범위 선택 (두 개의 값)
    price_range = st.slider(
        "가격 범위를 선택하세요:",
        min_value=0,
        max_value=1000000,
        value=(100000, 500000),  # 기본 범위
        step=10000,
        format="₩%d"
    )
    st.write(f"선택된 범위: **₩{price_range[0]:,} ~ ₩{price_range[1]:,}**")

# ============================================
# 5. 숫자 입력 (Number Input)
# ============================================
st.header("5. 숫자 입력 (Number Input)")

col1, col2 = st.columns(2)

with col1:
    quantity = st.number_input(
        "수량을 입력하세요:",
        min_value=0,
        max_value=100,
        value=1,
        step=1
    )
    st.write(f"입력된 수량: **{quantity}개**")

with col2:
    price = st.number_input(
        "가격을 입력하세요:",
        min_value=0.0,
        max_value=1000000.0,
        value=10000.0,
        step=1000.0,
        format="%.2f"
    )
    st.write(f"입력된 가격: **₩{price:,.2f}**")

total = quantity * price
st.info(f"총액: **₩{total:,.2f}**")

# ============================================
# 6. 텍스트 입력 (Text Input)
# ============================================
st.header("6. 텍스트 입력 (Text Input)")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input(
        "이름을 입력하세요:",
        value="",
        placeholder="홍길동"
    )

    if name:
        st.success(f"안녕하세요, {name}님!")

with col2:
    password = st.text_input(
        "비밀번호를 입력하세요:",
        type="password",
        placeholder="비밀번호 입력"
    )

    if password:
        st.info(f"비밀번호 길이: {len(password)}자")

# ============================================
# 7. 텍스트 영역 (Text Area)
# ============================================
st.header("7. 텍스트 영역 (Text Area)")

feedback = st.text_area(
    "의견을 입력하세요:",
    height=150,
    placeholder="여기에 의견을 작성해주세요..."
)

if feedback:
    st.write(f"입력된 글자 수: **{len(feedback)}자**")
    st.write(f"단어 수: **{len(feedback.split())}개**")

# ============================================
# 8. 체크박스 (Checkbox)
# ============================================
st.header("8. 체크박스 (Checkbox)")

agree = st.checkbox("이용약관에 동의합니다")

col1, col2, col3 = st.columns(3)
with col1:
    option1 = st.checkbox("옵션 1", value=True)
with col2:
    option2 = st.checkbox("옵션 2")
with col3:
    option3 = st.checkbox("옵션 3")

if agree:
    st.success("✅ 동의하셨습니다")
    selected_options = []
    if option1:
        selected_options.append("옵션 1")
    if option2:
        selected_options.append("옵션 2")
    if option3:
        selected_options.append("옵션 3")

    if selected_options:
        st.write("선택된 옵션:", ", ".join(selected_options))
else:
    st.warning("⚠️ 계속하려면 이용약관에 동의해주세요")

# ============================================
# 9. 라디오 버튼 (Radio)
# ============================================
st.header("9. 라디오 버튼 (Radio)")

st.markdown("""
여러 옵션 중 하나만 선택할 수 있습니다.
""")

col1, col2 = st.columns(2)

with col1:
    payment_method = st.radio(
        "결제 방법을 선택하세요:",
        options=["신용카드", "계좌이체", "간편결제"],
        index=0,
        horizontal=False
    )

with col2:
    delivery = st.radio(
        "배송 방법:",
        options=["일반 배송", "빠른 배송", "새벽 배송"],
        horizontal=True  # 가로 배치
    )

st.info(f"결제: {payment_method}, 배송: {delivery}")

# ============================================
# 10. 날짜/시간 입력
# ============================================
st.header("10. 날짜/시간 입력")

col1, col2 = st.columns(2)

with col1:
    date = st.date_input(
        "날짜를 선택하세요:",
        value=None
    )
    if date:
        st.write(f"선택된 날짜: {date}")

with col2:
    time = st.time_input(
        "시간을 선택하세요:",
        value=None
    )
    if time:
        st.write(f"선택된 시간: {time}")

# ============================================
# 11. 실전 예제: 사용자 등록 폼
# ============================================
st.header("11. 실전 예제: 사용자 등록 폼")

st.markdown("---")

with st.form("registration_form"):
    st.subheader("회원 가입")

    # 이름
    user_name = st.text_input("이름*", placeholder="홍길동")

    # 이메일
    email = st.text_input("이메일*", placeholder="example@email.com")

    # 비밀번호
    pwd = st.text_input("비밀번호*", type="password")

    # 성별
    gender = st.radio("성별", ["남성", "여성", "선택 안 함"], horizontal=True)

    # 나이
    user_age = st.slider("나이", 14, 100, 25)

    # 관심사
    interests = st.multiselect(
        "관심사",
        ["스포츠", "음악", "영화", "독서", "여행", "요리", "게임"]
    )

    # 뉴스레터 구독
    newsletter = st.checkbox("뉴스레터 구독")

    # 제출 버튼
    submitted = st.form_submit_button("가입하기")

    if submitted:
        # 입력 검증
        if not user_name or not email or not pwd:
            st.error("❌ 필수 항목을 모두 입력해주세요!")
        elif len(pwd) < 8:
            st.error("❌ 비밀번호는 8자 이상이어야 합니다!")
        else:
            st.success("✅ 회원가입이 완료되었습니다!")
            st.balloons()

            # 입력된 정보 표시
            st.write("### 등록 정보")
            info_df = pd.DataFrame({
                "항목": ["이름", "이메일", "성별", "나이", "관심사", "뉴스레터"],
                "내용": [
                    user_name,
                    email,
                    gender,
                    f"{user_age}세",
                    ", ".join(interests) if interests else "없음",
                    "구독" if newsletter else "미구독"
                ]
            })
            st.table(info_df)

# ============================================
# 실습 섹션
# ============================================
st.markdown("---")
st.header("🎯 실습해보세요!")

st.markdown("""
1. 각 위젯의 다양한 옵션을 시도해보세요
2. `key` 매개변수를 사용하여 위젯을 구분해보세요
3. 폼(form) 안팎의 위젯 동작 차이를 확인해보세요
4. 자신만의 입력 폼을 만들어보세요
5. 위젯 값에 따라 조건부로 다른 위젯을 표시해보세요
""")

# --------------------------------------------
# 실습 1: 조건부 위젯 표시
# --------------------------------------------
st.subheader("실습 1: 조건부 위젯 표시")

st.write("**선택에 따라 다른 위젯이 나타납니다:**")

category = st.selectbox(
    "카테고리 선택:",
    ["음식 주문", "영화 예매", "호텔 예약"],
    key="practice_category"
)

if category == "음식 주문":
    st.write("**음식 주문 옵션:**")
    food_type = st.radio("음식 종류:", ["한식", "중식", "양식", "일식"], horizontal=True)
    quantity = st.number_input("수량:", min_value=1, max_value=10, value=1)
    delivery = st.checkbox("배달 요청")
    if delivery:
        address = st.text_input("배달 주소:")
        st.write(f"📍 배달지: {address if address else '주소를 입력해주세요'}")

elif category == "영화 예매":
    st.write("**영화 예매 옵션:**")
    movie_date = st.date_input("날짜 선택:")
    movie_time = st.selectbox("시간 선택:", ["10:00", "13:00", "16:00", "19:00", "22:00"])
    seats = st.slider("좌석 수:", 1, 8, 2)
    st.info(f"🎬 {movie_date} {movie_time} / {seats}석")

elif category == "호텔 예약":
    st.write("**호텔 예약 옵션:**")
    check_in = st.date_input("체크인:")
    check_out = st.date_input("체크아웃:")
    room_type = st.selectbox("객실 유형:", ["스탠다드", "디럭스", "스위트"])
    guests = st.number_input("인원:", min_value=1, max_value=4, value=2)

    if check_in and check_out:
        nights = (check_out - check_in).days
        if nights > 0:
            st.success(f"🏨 {nights}박 / {room_type} / {guests}명")
        else:
            st.error("체크아웃 날짜는 체크인 이후여야 합니다.")

# --------------------------------------------
# 실습 2: key 매개변수 이해하기
# --------------------------------------------
st.subheader("실습 2: key 매개변수 이해하기")

st.write("""
**왜 key가 필요한가요?**
- 같은 타입의 위젯을 여러 개 사용할 때 구분하기 위함
- `st.session_state`에서 위젯 값에 접근할 때 사용
""")

col1, col2 = st.columns(2)

with col1:
    st.write("**위젯 A:**")
    value_a = st.slider("값 선택:", 0, 100, 50, key="slider_a")
    st.write(f"값: {value_a}")

with col2:
    st.write("**위젯 B:**")
    value_b = st.slider("값 선택:", 0, 100, 50, key="slider_b")
    st.write(f"값: {value_b}")

st.write("**session_state에서 값 확인:**")
st.code(f"""
st.session_state['slider_a'] = {st.session_state.get('slider_a', 'Not set')}
st.session_state['slider_b'] = {st.session_state.get('slider_b', 'Not set')}
""")

# --------------------------------------------
# 실습 3: 폼 vs 폼 외부 위젯 비교
# --------------------------------------------
st.subheader("실습 3: 폼 vs 일반 위젯 비교")

compare_col1, compare_col2 = st.columns(2)

with compare_col1:
    st.write("**일반 위젯 (즉시 반응):**")
    normal_text = st.text_input("이름:", key="normal_text")
    normal_age = st.slider("나이:", 0, 100, 25, key="normal_age")
    st.write(f"입력값: {normal_text}, {normal_age}세")
    st.caption("⚡ 값을 변경할 때마다 앱이 새로고침됩니다")

with compare_col2:
    st.write("**폼 안의 위젯 (제출 시 반응):**")
    with st.form("comparison_form"):
        form_text = st.text_input("이름:", key="form_text")
        form_age = st.slider("나이:", 0, 100, 25, key="form_age")
        submitted = st.form_submit_button("제출")
        if submitted:
            st.write(f"입력값: {form_text}, {form_age}세")
    st.caption("📝 '제출' 버튼을 눌러야 값이 처리됩니다")

# --------------------------------------------
# 실습 4: 실전 주문 폼 만들기
# --------------------------------------------
st.subheader("실습 4: 커피 주문 폼")

with st.form("coffee_order_form"):
    st.write("**☕ 커피 주문서**")

    order_col1, order_col2 = st.columns(2)

    with order_col1:
        coffee_type = st.selectbox(
            "음료 선택:",
            ["아메리카노", "카페라떼", "카푸치노", "바닐라라떼", "카라멜마끼아또"]
        )
        size = st.radio("사이즈:", ["Tall", "Grande", "Venti"], horizontal=True)

    with order_col2:
        temperature = st.radio("온도:", ["HOT", "ICE"], horizontal=True)
        shots = st.number_input("샷 추가:", 0, 3, 0)

    sweetness = st.slider("당도:", 0, 100, 50, format="%d%%")

    options = st.multiselect(
        "추가 옵션:",
        ["휘핑크림", "시럽 추가", "우유 변경(두유)", "디카페인"]
    )

    memo = st.text_area("요청사항:", placeholder="예: 얼음 적게 해주세요")

    order_submitted = st.form_submit_button("주문하기")

    if order_submitted:
        st.success("✅ 주문이 완료되었습니다!")
        st.markdown(f"""
        **주문 내역:**
        - 음료: {coffee_type} ({size}, {temperature})
        - 샷 추가: {shots}샷
        - 당도: {sweetness}%
        - 옵션: {', '.join(options) if options else '없음'}
        - 요청사항: {memo if memo else '없음'}
        """)

        # 가격 계산 (예시)
        base_price = {"Tall": 4500, "Grande": 5000, "Venti": 5500}
        total = base_price[size] + (shots * 500) + (len(options) * 500)
        st.info(f"💰 결제 금액: ₩{total:,}")

with st.expander("💡 위젯 사용 팁"):
    st.markdown("""
    **key 매개변수:**
    - 각 위젯은 고유한 `key`를 가져야 합니다
    - 같은 페이지에 동일한 위젯이 여러 개 있을 때 필수
    - `st.session_state`로 값에 접근 가능

    **form 사용:**
    - 여러 입력을 한 번에 처리할 때 유용
    - form 안의 위젯은 제출 버튼을 누를 때까지 앱을 재실행하지 않음
    - 성능 최적화에 도움

    **기본값 설정:**
    - 사용자 경험 향상
    - 예시를 보여주는 효과
    """)
