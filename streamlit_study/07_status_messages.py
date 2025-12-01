"""
예제 7: 상태 메시지 (Status Messages)

이 예제에서는 다양한 상태 메시지를 학습합니다.
"""
import streamlit as st
import time

st.set_page_config(
    page_title="상태 메시지",
    page_icon="💬",
    layout="wide"
)

st.title("💬 상태 메시지 (Status Messages)")

st.markdown("""
Streamlit은 사용자에게 정보를 전달하기 위한 다양한 상태 메시지를 제공합니다.
각 메시지는 색상과 아이콘으로 구분되어 의미를 명확히 전달합니다.
""")

# ============================================
# 1. 기본 상태 메시지
# ============================================
st.header("1. 기본 상태 메시지")

# columns는 with 구문으로 마치 세션을 유지하듯듯
col1, col2 = st.columns(2)

with col1:
    st.subheader("왼쪽 컬럼")

    st.success("✅ 성공 메시지 (Success)")
    st.write("작업이 성공적으로 완료되었음을 알립니다.")

    st.info("ℹ️ 정보 메시지 (Info)")
    st.write("일반적인 정보를 제공합니다.")

with col2:
    st.subheader("오른쪽 컬럼")

    st.warning("⚠️ 경고 메시지 (Warning)")
    st.write("주의가 필요한 상황을 알립니다.")

    st.error("❌ 오류 메시지 (Error)")
    st.write("오류가 발생했음을 알립니다.")

# ============================================
# 2. 긴 메시지
# 메시지가 길어질 땐, expander를 사용하거나, 아니면 write 대신 마크다운 
# ============================================
st.header("2. 긴 메시지")

st.info("""
ℹ️ **정보 메시지에 마크다운 사용하기**

상태 메시지에는 마크다운을 포함한 모든 텍스트를 넣을 수 있습니다:

- 리스트 항목 1
- 리스트 항목 2
- 리스트 항목 3

**굵은 글씨**, *기울임*, `코드` 등도 사용 가능합니다.
""")

# ============================================
# 3. 실전 예제: 폼 검증
# ============================================
st.header("3. 실전 예제: 폼 검증")

# st.columns와 더불어 st.form을 사용하여 세션 내에 넣어두면면 폼을 유지 
with st.form("validation_form"):
    st.subheader("사용자 등록")

    username = st.text_input("사용자 이름 (4자 이상)")
    email = st.text_input("이메일")
    password = st.text_input("비밀번호 (8자 이상)", type="password")
    confirm_password = st.text_input("비밀번호 확인", type="password")

    # 모든 버튼은 누르면 True
    submitted = st.form_submit_button("등록")

if submitted:
    # 검증 로직
    # 참고: errors, warnings, success는 모두 전역 변수로 상단에 빼거나 아니면 
    # session_state에 저장해놓는 게 좋다. 
    errors = []
    warnings = []
    success = True

    # 사용자 이름 검증
    if not username:
        errors.append("사용자 이름을 입력해주세요.")
        success = False
    elif len(username) < 4:
        errors.append("사용자 이름은 4자 이상이어야 합니다.")
        success = False

    # 이메일 검증
    if not email:
        errors.append("이메일을 입력해주세요.")
        success = False
    elif "@" not in email:
        errors.append("올바른 이메일 형식이 아닙니다.")
        success = False

    # 비밀번호 검증
    if not password:
        errors.append("비밀번호를 입력해주세요.")
        success = False
    elif len(password) < 8:
        errors.append("비밀번호는 8자 이상이어야 합니다.")
        success = False
    elif password != confirm_password:
        errors.append("비밀번호가 일치하지 않습니다.")
        success = False

    # 결과 표시
    if errors:
        for error in errors:
            st.error(f"❌ {error}")

    if warnings:
        for warning in warnings:
            st.warning(f"⚠️ {warning}")

    if success:
        st.success("✅ 회원가입이 완료되었습니다!")
        st.balloons()
        st.info(f"ℹ️ 환영합니다, {username}님!")

# ============================================
# 4. 조건부 메시지
# ============================================
st.header("4. 조건부 메시지")

st.write("슬라이더로 값을 조정하면 메시지가 변경됩니다:")

value = st.slider("값을 선택하세요", 0, 100, 50, step=10)

if value < 30:
    st.error(f"❌ 너무 낮습니다! (현재: {value})")
elif value < 70:
    st.warning(f"⚠️ 적정 범위입니다. (현재: {value})")
else:
    st.success(f"✅ 좋습니다! (현재: {value})")

# ============================================
# 5. 동적 메시지
# ============================================
st.header("5. 동적 메시지")

if st.button("파일 처리 시뮬레이션"):
    st.info("ℹ️ 파일 처리를 시작합니다...")
    time.sleep(1)

    st.warning("⚠️ 대용량 파일이 감지되었습니다. 처리 시간이 길어질 수 있습니다.")
    time.sleep(1)

    st.success("✅ 파일 처리가 완료되었습니다!")

# ============================================
# 6. 예외 처리
# ============================================
st.header("6. 예외 처리")

st.write("의도적으로 오류를 발생시켜 보겠습니다:")

if st.button("오류 발생시키기"):
    try:
        # 의도적인 오류
        result = 1 / 0
    except ZeroDivisionError as e:
        st.error(f"❌ 오류 발생: {str(e)}")
        st.info("ℹ️ 0으로 나눌 수 없습니다.")

# ============================================
# 7. 실전 예제: 로그인 시스템
# ============================================
st.header("7. 실전 예제: 로그인 시스템")

st.markdown("---")

# 간단한 로그인 (실제로는 보안이 필요!)
VALID_USERS = {
    "admin": "password123",
    "user": "user123"
}

with st.form("login_form"):
    st.subheader("로그인")

    login_id = st.text_input("아이디")
    login_pwd = st.text_input("비밀번호", type="password")

    login_submitted = st.form_submit_button("로그인")

if login_submitted:
    if not login_id or not login_pwd:
        st.warning("⚠️ 아이디와 비밀번호를 모두 입력해주세요.")
    elif login_id not in VALID_USERS:
        st.error("❌ 존재하지 않는 사용자입니다.")
    elif VALID_USERS[login_id] != login_pwd:
        st.error("❌ 비밀번호가 올바르지 않습니다.")
    else:
        st.success(f"✅ 로그인 성공! 환영합니다, {login_id}님!")
        st.balloons()

        # 사용자 정보 표시
        if login_id == "admin":
            st.info("ℹ️ 관리자 권한으로 로그인하셨습니다.")
        else:
            st.info("ℹ️ 일반 사용자로 로그인하셨습니다.")

# ============================================
# 실습 섹션
# ============================================
st.markdown("---")
st.header("🎯 실습해보세요!")

st.markdown("""
1. 복잡한 폼 검증 로직을 만들어보세요
2. 단계별 프로세스에 각 단계마다 다른 메시지 표시
3. 에러 핸들링을 추가하여 사용자 친화적인 메시지 표시
4. 조건부 메시지를 사용한 대화형 앱 만들기
""")

with st.expander("💡 상태 메시지 사용 가이드"):
    st.markdown("""
    **언제 어떤 메시지를 사용할까?**

    - **st.success()**: 작업 완료, 성공, 올바른 입력
    - **st.info()**: 일반 정보, 도움말, 안내
    - **st.warning()**: 주의 사항, 권장 사항, 선택적 문제
    - **st.error()**: 오류, 실패, 필수 문제

    **베스트 프랙티스:**
    - 명확하고 구체적인 메시지 작성
    - 사용자가 취할 수 있는 행동 제시
    - 긍정적이고 도움이 되는 톤 유지
    - 기술적 용어보다는 일반 사용자가 이해할 수 있는 언어 사용

    **피해야 할 것:**
    - 너무 많은 메시지 (중요한 것만)
    - 모호한 메시지 ("오류 발생" 대신 "파일을 찾을 수 없습니다" 등)
    - 부정적인 톤
    """)

# ============================================
# 실습 과제 구현
# ============================================
st.markdown("---")
st.header("📝 실습 과제 구현 예시")

# --------------------------------------------
# 실습 1: 복잡한 폼 검증 로직
# --------------------------------------------
st.subheader("실습 1: 복잡한 폼 검증 - 주문서 작성")

with st.form("order_form"):
    st.write("**상품 주문서**")

    col_order1, col_order2 = st.columns(2)

    with col_order1:
        product_name = st.selectbox(
            "상품 선택",
            ["선택하세요", "노트북", "태블릿", "스마트폰", "이어폰"]
        )
        quantity = st.number_input("수량", min_value=0, max_value=100, value=0)

    with col_order2:
        delivery_date = st.date_input("배송 희망일")
        delivery_address = st.text_area("배송 주소", height=100)

    coupon_code = st.text_input("쿠폰 코드 (선택사항)")
    agree_terms = st.checkbox("이용약관에 동의합니다")

    order_submitted = st.form_submit_button("주문하기", type="primary")

if order_submitted:
    order_errors = []
    order_warnings = []
    order_success = True

    # 상품 검증
    if product_name == "선택하세요":
        order_errors.append("상품을 선택해주세요.")
        order_success = False

    # 수량 검증
    if quantity <= 0:
        order_errors.append("수량은 1개 이상이어야 합니다.")
        order_success = False
    elif quantity > 10:
        order_warnings.append(f"대량 주문({quantity}개)은 배송이 지연될 수 있습니다.")

    # 배송 주소 검증
    if not delivery_address.strip():
        order_errors.append("배송 주소를 입력해주세요.")
        order_success = False
    elif len(delivery_address) < 10:
        order_errors.append("배송 주소를 더 상세히 입력해주세요.")
        order_success = False

    # 쿠폰 코드 검증 (선택사항이지만 입력했다면 검증)
    valid_coupons = ["SAVE10", "WELCOME", "VIP2024"]
    if coupon_code and coupon_code.upper() not in valid_coupons:
        order_warnings.append(f"'{coupon_code}'는 유효하지 않은 쿠폰입니다. 쿠폰 없이 진행됩니다.")
    elif coupon_code:
        st.info(f"ℹ️ 쿠폰 '{coupon_code.upper()}'가 적용되었습니다!")

    # 약관 동의 검증
    if not agree_terms:
        order_errors.append("이용약관에 동의해주세요.")
        order_success = False

    # 결과 표시
    for err in order_errors:
        st.error(f"❌ {err}")
    for warn in order_warnings:
        st.warning(f"⚠️ {warn}")

    if order_success:
        st.success(f"✅ 주문이 완료되었습니다! {product_name} {quantity}개가 {delivery_date}에 배송됩니다.")
        st.balloons()

# --------------------------------------------
# 실습 2: 단계별 프로세스
# --------------------------------------------
st.subheader("실습 2: 단계별 프로세스 - 데이터 처리 파이프라인")

if st.button("데이터 처리 시작", key="process_btn"):
    # 진행 상태를 표시할 컨테이너
    status_container = st.empty()
    progress_bar = st.progress(0)

    steps = [
        ("데이터 로드 중...", "info", 20),
        ("데이터 유효성 검사 중...", "info", 40),
        ("중복 데이터 발견! 자동으로 제거합니다.", "warning", 50),
        ("데이터 변환 중...", "info", 70),
        ("결과 저장 중...", "info", 90),
        ("모든 처리가 완료되었습니다!", "success", 100),
    ]

    for message, msg_type, progress in steps:
        progress_bar.progress(progress)

        with status_container.container():
            if msg_type == "info":
                st.info(f"ℹ️ {message}")
            elif msg_type == "warning":
                st.warning(f"⚠️ {message}")
            elif msg_type == "success":
                st.success(f"✅ {message}")

        time.sleep(0.8)

    st.write("**처리 결과:**")
    col_result1, col_result2, col_result3 = st.columns(3)
    with col_result1:
        st.metric("처리된 행", "1,234")
    with col_result2:
        st.metric("제거된 중복", "56")
    with col_result3:
        st.metric("처리 시간", "4.2초")

# --------------------------------------------
# 실습 3: 에러 핸들링
# --------------------------------------------
st.subheader("실습 3: 에러 핸들링 - 파일 처리 시뮬레이션")

uploaded_filename = st.text_input(
    "처리할 파일명을 입력하세요",
    placeholder="예: data.csv, report.xlsx",
    key="file_input"
)

if st.button("파일 처리", key="file_process_btn"):
    if not uploaded_filename:
        st.error("❌ 파일명을 입력해주세요.")
    else:
        try:
            # 파일 확장자 검증
            valid_extensions = ['.csv', '.xlsx', '.json', '.txt']
            file_ext = '.' + uploaded_filename.split('.')[-1].lower() if '.' in uploaded_filename else ''

            if not file_ext:
                raise ValueError("파일 확장자가 없습니다. (예: .csv, .xlsx)")

            if file_ext not in valid_extensions:
                raise TypeError(f"지원하지 않는 파일 형식입니다. 지원 형식: {', '.join(valid_extensions)}")

            # 특정 파일명으로 에러 시뮬레이션
            if "error" in uploaded_filename.lower():
                raise IOError("파일을 읽는 중 오류가 발생했습니다.")

            if "empty" in uploaded_filename.lower():
                raise ValueError("파일이 비어있습니다.")

            # 성공
            st.success(f"✅ '{uploaded_filename}' 파일이 성공적으로 처리되었습니다!")
            st.info(f"ℹ️ 파일 형식: {file_ext.upper()[1:]} | 처리 완료")

        except ValueError as ve:
            st.error(f"❌ 입력 오류: {str(ve)}")
            st.info("ℹ️ 파일명을 확인하고 다시 시도해주세요.")
        except TypeError as te:
            st.error(f"❌ 형식 오류: {str(te)}")
            st.warning("⚠️ CSV, XLSX, JSON, TXT 파일만 처리할 수 있습니다.")
        except IOError as ie:
            st.error(f"❌ 파일 오류: {str(ie)}")
            st.warning("⚠️ 파일이 손상되었거나 접근 권한이 없을 수 있습니다.")
        except Exception as e:
            st.error(f"❌ 예상치 못한 오류: {str(e)}")
            st.info("ℹ️ 관리자에게 문의해주세요.")

# --------------------------------------------
# 실습 4: 조건부 메시지를 사용한 대화형 앱
# --------------------------------------------
st.subheader("실습 4: 대화형 앱 - BMI 계산기")

col_bmi1, col_bmi2 = st.columns(2)

with col_bmi1:
    height = st.number_input("키 (cm)", min_value=100.0, max_value=250.0, value=170.0, step=0.1)
with col_bmi2:
    weight = st.number_input("체중 (kg)", min_value=20.0, max_value=300.0, value=65.0, step=0.1)

if st.button("BMI 계산", key="bmi_btn"):
    # BMI 계산
    height_m = height / 100
    bmi = weight / (height_m ** 2)

    st.write(f"**당신의 BMI: {bmi:.1f}**")

    # BMI에 따른 조건부 메시지
    if bmi < 18.5:
        st.warning(f"⚠️ 저체중입니다 (BMI: {bmi:.1f})")
        st.info("ℹ️ 균형 잡힌 식단과 적절한 영양 섭취를 권장합니다.")
    elif bmi < 23:
        st.success(f"✅ 정상 체중입니다 (BMI: {bmi:.1f})")
        st.info("ℹ️ 현재 건강 상태를 유지하세요!")
    elif bmi < 25:
        st.warning(f"⚠️ 과체중입니다 (BMI: {bmi:.1f})")
        st.info("ℹ️ 규칙적인 운동과 식단 조절을 권장합니다.")
    else:
        st.error(f"❌ 비만입니다 (BMI: {bmi:.1f})")
        st.warning("⚠️ 건강을 위해 전문가 상담을 권장합니다.")

    # 추가 정보
    with st.expander("BMI 기준표"):
        st.markdown("""
        | 분류 | BMI 범위 |
        |------|----------|
        | 저체중 | 18.5 미만 |
        | 정상 | 18.5 ~ 22.9 |
        | 과체중 | 23 ~ 24.9 |
        | 비만 | 25 이상 |

        *대한비만학회 기준 (아시아-태평양 기준)*
        """)

# ============================================
# 수강생을 위한 추가 학습 내용
# ============================================
st.markdown("---")
st.header("📚 수강생을 위한 추가 학습 내용")

st.write("""
아래는 상태 메시지를 더 효과적으로 활용하기 위한 **심화 내용**입니다.
실무에서 자주 사용되는 패턴과 주의사항을 정리했습니다.
""")

# 탭으로 구분하여 정보 제공
tab1, tab2, tab3, tab4 = st.tabs(["🔄 동적 업데이트", "🎨 커스텀 스타일링", "⚡ 성능 팁", "🛡️ 보안 고려사항"])

with tab1:
    st.markdown("""
    ### 동적으로 메시지 업데이트하기

    `st.empty()`를 사용하면 같은 위치에서 메시지를 업데이트할 수 있습니다.

    ```python
    # placeholder 생성
    status = st.empty()

    # 메시지 업데이트
    status.info("처리 중...")
    time.sleep(1)
    status.warning("거의 완료...")
    time.sleep(1)
    status.success("완료!")
    ```

    **장점:**
    - 화면이 지저분해지지 않음
    - 진행 상황을 같은 위치에서 표시
    - 사용자 경험(UX) 향상

    **실제 사용 예시:**
    - 파일 업로드 진행률
    - API 호출 상태
    - 데이터 처리 단계 표시
    """)

with tab2:
    st.markdown("""
    ### 커스텀 스타일링 방법

    기본 상태 메시지 외에 더 다양한 스타일을 원한다면:

    **1. 마크다운 + HTML 활용**
    ```python
    st.markdown('''
    <div style="padding: 1rem; background-color: #d4edda;
                border-radius: 0.5rem; border-left: 5px solid #28a745;">
        <strong>✅ 커스텀 성공 메시지</strong><br>
        원하는 스타일로 꾸밀 수 있습니다.
    </div>
    ''', unsafe_allow_html=True)
    ```

    **2. st.toast() 활용 (Streamlit 1.23+)**
    ```python
    st.toast("저장되었습니다!", icon="✅")
    ```
    - 화면 우측 하단에 일시적으로 표시
    - 자동으로 사라짐
    - 사용자 작업 흐름을 방해하지 않음

    **3. st.status() 활용 (Streamlit 1.29+)**
    ```python
    with st.status("처리 중...", expanded=True) as status:
        st.write("데이터 로드 중...")
        time.sleep(1)
        st.write("분석 중...")
        time.sleep(1)
        status.update(label="완료!", state="complete")
    ```
    """)

with tab3:
    st.markdown("""
    ### 성능 최적화 팁

    **1. 불필요한 메시지 최소화**
    - 모든 단계마다 메시지를 표시하지 않기
    - 중요한 상태 변화만 알림

    **2. session_state 활용**
    ```python
    # 메시지 상태 저장
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # 조건부 렌더링
    if st.session_state.show_success:
        st.success("완료!")
    ```

    **3. 조건부 렌더링으로 리렌더링 최소화**
    ```python
    # 나쁜 예 - 항상 모든 메시지 렌더링
    st.success("성공") if success else st.error("실패")

    # 좋은 예 - 필요할 때만 렌더링
    if success:
        st.success("성공")
    elif has_error:
        st.error("실패")
    ```

    **4. @st.cache_data와 함께 사용**
    - 데이터 처리 결과를 캐시하고
    - 캐시 히트/미스에 따라 다른 메시지 표시
    """)

with tab4:
    st.markdown("""
    ### 보안 관련 주의사항

    **1. 민감 정보 노출 금지**
    ```python
    # ❌ 나쁜 예
    st.error(f"DB 연결 실패: {connection_string}")

    # ✅ 좋은 예
    st.error("데이터베이스 연결에 실패했습니다. 관리자에게 문의하세요.")
    ```

    **2. 상세한 에러 메시지는 로그로**
    ```python
    import logging

    try:
        # 작업 수행
        pass
    except Exception as e:
        logging.error(f"상세 에러: {e}")  # 서버 로그에만 기록
        st.error("처리 중 오류가 발생했습니다.")  # 사용자에게는 간단히
    ```

    **3. 사용자 입력 검증**
    - 상태 메시지에 사용자 입력을 표시할 때 XSS 주의
    - `st.write()`는 기본적으로 안전하지만, `unsafe_allow_html=True` 사용 시 주의

    **4. 인증 상태 메시지**
    ```python
    # ❌ 나쁜 예 - 정보 노출
    st.error("비밀번호가 틀렸습니다.")

    # ✅ 좋은 예 - 모호하게
    st.error("아이디 또는 비밀번호가 올바르지 않습니다.")
    ```
    """)

# ============================================
# 심화 학습 내용 실제 구현
# ============================================
st.markdown("---")
st.header("🔬 심화 학습 내용 실제 구현")

# 1. st.empty() - 동적 메시지 업데이트
st.subheader("1. st.empty() - 동적 메시지 업데이트")

if st.button("동적 업데이트 시작", key="dynamic_update_btn"):
    status = st.empty()
    status.info("ℹ️ 처리 중...")
    time.sleep(1)
    status.warning("⚠️ 거의 완료...")
    time.sleep(1)
    status.success("✅ 완료!")

# 2. st.toast() - 토스트 메시지
st.subheader("2. st.toast() - 토스트 메시지")

col1, col2 = st.columns(2)
with col1:
    if st.button("토스트 표시", key="toast_btn"):
        st.toast("저장되었습니다!", icon="✅")
with col2:
    if st.button("다중 토스트", key="toast_multi"):
        for i in range(1, 4):
            st.toast(f"{i}단계 완료", icon=f"{i}️⃣")
            time.sleep(0.5)

# 3. st.status() - 상태 컨테이너
st.subheader("3. st.status() - 상태 컨테이너")

if st.button("st.status() 실행", key="status_demo_btn"):
    with st.status("처리 중...", expanded=True) as status:
        st.write("📂 데이터 로드...")
        time.sleep(1)
        st.write("🔍 분석 중...")
        time.sleep(1)
        status.update(label="✅ 완료!", state="complete", expanded=False)

# 4. 커스텀 스타일 메시지
st.subheader("4. 커스텀 스타일 메시지 (HTML)")

st.markdown('''
<div style="padding: 1rem; background-color: #d4edda; border-radius: 0.5rem; border-left: 5px solid #28a745;">
    <strong>✅ 커스텀 성공 메시지</strong> - HTML/CSS로 스타일링
</div>
''', unsafe_allow_html=True)

# 마무리 요약
st.markdown("---")
st.info("""
**📌 핵심 요약**

1. **적절한 메시지 선택**: 상황에 맞는 메시지 타입(success/info/warning/error)을 사용하세요.
2. **사용자 친화적**: 기술 용어보다는 일반 사용자가 이해할 수 있는 언어를 사용하세요.
3. **행동 지향적**: 문제 발생 시 사용자가 취할 수 있는 행동을 안내하세요.
4. **적절한 양**: 너무 많은 메시지는 오히려 혼란을 줍니다.
5. **동적 업데이트**: `st.empty()`나 `st.status()`를 활용해 깔끔한 UX를 제공하세요.
""")

st.success("🎉 실습 과제를 모두 완료했습니다! 다음 예제로 넘어가세요.")
