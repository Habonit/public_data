"""
예제 8: 로딩 스피너 (Spinner)

이 예제에서는 st.spinner를 사용하여 로딩 중임을 표시하는 방법을 학습합니다.
"""
import streamlit as st
import time
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="로딩 스피너",
    page_icon="⏳",
    layout="wide"
)

# 사용자 경험을 위해서(UX) 중요한 요소 
st.title("⏳ 로딩 스피너 (Spinner)")

st.markdown("""
`st.spinner()`는 시간이 오래 걸리는 작업 중에 로딩 애니메이션을 표시합니다.
사용자에게 앱이 작동 중임을 알려줍니다.
""")

# ============================================
# 1. 기본 스피너
# ============================================
st.header("1. 기본 스피너")

if st.button("기본 스피너 실행"):
    # 스피너도 column, form과 같이 with 구문
    with st.spinner("처리 중..."):
        # 내부에 시간이 오래걸릴법한 작업을 넣으면 됨됨
        time.sleep(0.1)
    st.success("완료!")

# ============================================
# 2. 커스텀 메시지 스피너
# ============================================
st.header("2. 커스텀 메시지")

col1, col2 = st.columns(2)

with col1:
    if st.button("데이터 로딩"):
        with st.spinner("📂 데이터를 불러오는 중..."):
            time.sleep(2)
        st.success("✅ 데이터 로딩 완료!")

with col2:
    if st.button("파일 업로드"):
        with st.spinner("☁️ 파일을 업로드하는 중..."):
            time.sleep(2)
        st.success("✅ 업로드 완료!")

# ============================================
# 3. 실전 예제: 데이터 처리
# ============================================
st.header("3. 실전 예제: 대용량 데이터 처리")

num_rows = st.slider("생성할 데이터 행 수", 1000, 100000, 10000, step=1000)

if st.button("데이터 생성 및 처리"):
    # 1단계: 데이터 생성
    with st.spinner(f"1/3 단계: {num_rows:,}개 행 생성 중..."):
        start = time.time()
        df = pd.DataFrame({
            'A': np.random.randn(num_rows),
            'B': np.random.randn(num_rows),
            'C': np.random.randint(0, 100, num_rows),
            'D': np.random.choice(['X', 'Y', 'Z'], num_rows)
        })
        time.sleep(1)
        end = time.time()
        st.write(f"데이터 생성 시간: {end - start:.2f}초")

    st.success(f"✅ {len(df):,}개 행 생성 완료")

    # 2단계: 데이터 분석
    with st.spinner("2/3 단계: 데이터 분석 중..."):
        start = time.time()
        stats = df.describe()
        time.sleep(1)
        end = time.time()
        st.write(f"데이터 분석 시간: {end - start:.2f}초")
    st.success("✅ 분석 완료")

    # 3단계: 시각화
    with st.spinner("3/3 단계: 시각화 생성 중..."):
        start = time.time()
        time.sleep(1)
        end = time.time()
        st.write(f"시각화 생성 시간: {end - start:.2f}초")

    st.success("✅ 모든 작업 완료!")

    # 결과 표시
    col1, col2 = st.columns(2)

    with col1:
        st.write("### 데이터 미리보기")
        st.dataframe(df.head(10))

    with col2:
        st.write("### 통계")
        st.dataframe(stats)

# ============================================
# 4. 중첩 스피너
# ============================================
st.header("4. 중첩 스피너")

if st.button("다단계 프로세스 실행"):
    with st.spinner("전체 프로세스 시작..."):
        st.write("🚀 전체 프로세스 시작")
        time.sleep(1)

        with st.spinner("→ 1단계: 초기화 중..."):
            time.sleep(1)
            st.write("✅ 1단계 완료")

        with st.spinner("→ 2단계: 데이터 처리 중..."):
            time.sleep(1)
            st.write("✅ 2단계 완료")

        with st.spinner("→ 3단계: 마무리 중..."):
            time.sleep(1)
            st.write("✅ 3단계 완료")

    st.success("🎉 전체 프로세스 완료!")
    st.balloons()

# ============================================
# 5. 프로그레스 바와 함께 사용
# ============================================
st.header("5. 프로그레스 바와 함께 사용")

if st.button("프로그레스 바로 진행 상황 표시"):
    progress_text = st.empty()
    progress_bar = st.progress(0)

    for i in range(100):
        # 진행률 업데이트
        progress = i + 1
        progress_bar.progress(progress)
        progress_text.text(f"진행 중... {progress}%")

        # 실제 작업 시뮬레이션
        time.sleep(0.02)

    progress_text.text("완료!")
    st.success("✅ 모든 작업이 완료되었습니다!")

# ============================================
# 6. 실전 예제: 데이터 다운로드 시뮬레이션
# ============================================
st.header("6. 실전 예제: API 호출 시뮬레이션")

api_endpoint = st.selectbox(
    "API 엔드포인트 선택:",
    ["/api/users", "/api/products", "/api/orders"]
)

if st.button("API 호출"):
    with st.spinner(f"⏳ {api_endpoint}에서 데이터를 가져오는 중..."):
        # API 호출 시뮬레이션
        time.sleep(2)

        # 가짜 데이터 생성
        if "users" in api_endpoint:
            data = pd.DataFrame({
                '사용자ID': range(1, 11),
                '이름': [f"User{i}" for i in range(1, 11)],
                '이메일': [f"user{i}@example.com" for i in range(1, 11)]
            })
        elif "products" in api_endpoint:
            data = pd.DataFrame({
                '제품ID': range(1, 11),
                '제품명': [f"Product {i}" for i in range(1, 11)],
                '가격': np.random.randint(10000, 100000, 10)
            })
        else:
            data = pd.DataFrame({
                '주문ID': range(1, 11),
                '주문일': pd.date_range('2024-01-01', periods=10),
                '금액': np.random.randint(50000, 500000, 10)
            })

    st.success(f"✅ {api_endpoint}에서 {len(data)}개 레코드를 가져왔습니다!")
    st.dataframe(data, width="stretch")

# ============================================
# 7. 에러 처리와 함께
# ============================================
st.header("7. 에러 처리와 함께 사용")

if st.button("랜덤 성공/실패"):
    try:
        with st.spinner("작업 처리 중..."):
            time.sleep(2)

            # 랜덤하게 성공 또는 실패
            if np.random.random() > 0.5:
                result = "성공!"
            else:
                raise Exception("랜덤 에러 발생")

        st.success(f"✅ {result}")

    except Exception as e:
        st.error(f"❌ 작업 실패: {str(e)}")
        st.info("ℹ️ 다시 시도해주세요.")

# ============================================
# 실습 섹션
# ============================================
st.markdown("---")
st.header("🎯 실습해보세요!")

st.markdown("""
1. 다단계 작업에 각 단계마다 스피너 추가
2. 프로그레스 바와 스피너를 함께 사용
3. 에러가 발생할 수 있는 작업에 스피너와 try-except 적용
4. 실제 파일 로딩 또는 API 호출에 스피너 적용
""")

with st.expander("💡 스피너 사용 가이드"):
    st.markdown("""
    **언제 사용해야 할까?**
    - 2초 이상 걸리는 작업
    - 파일 로딩, API 호출
    - 복잡한 계산
    - 데이터베이스 쿼리

    **베스트 프랙티스:**
    - 명확한 메시지 ("처리 중..." 보다 "데이터를 불러오는 중...")
    - 작업이 얼마나 걸릴지 예상 가능하면 알려주기
    - 매우 긴 작업은 프로그레스 바와 함께 사용
    - 에러 처리와 함께 사용

    **주의사항:**
    - 너무 짧은 작업에는 사용하지 않기 (깜빡임)
    - 스피너 안에서 st.write() 등은 스피너가 끝날 때까지 보이지 않음
    - 매우 긴 작업(1분 이상)은 백그라운드 작업 고려
    """)

# ============================================
# 실습 과제 구현
# ============================================
st.markdown("---")
st.header("📝 실습 과제 구현")

# 실습 1: 다단계 작업에 각 단계마다 스피너 추가
st.subheader("실습 1: 다단계 이미지 처리 시뮬레이션")

image_processing_steps = st.multiselect(
    "처리할 단계 선택:",
    ["이미지 로딩", "노이즈 제거", "색상 보정", "크기 조정", "압축"],
    default=["이미지 로딩", "색상 보정", "압축"]
)

if st.button("이미지 처리 시작", key="practice1"):
    if not image_processing_steps:
        st.warning("최소 1개 이상의 단계를 선택하세요!")
    else:
        total_steps = len(image_processing_steps)

        for idx, step in enumerate(image_processing_steps, 1):
            with st.spinner(f"🖼️ [{idx}/{total_steps}] {step} 진행 중..."):
                time.sleep(1.5)
            st.success(f"✅ {step} 완료!")

        st.balloons()
        st.success(f"🎉 모든 이미지 처리 완료! (총 {total_steps}단계)")

st.markdown("---")

# 실습 2: 프로그레스 바와 스피너를 함께 사용
st.subheader("실습 2: 파일 다운로드 시뮬레이션")

file_size = st.number_input("파일 크기 (MB)", min_value=10, max_value=500, value=100, step=10)

if st.button("파일 다운로드 시작", key="practice2"):
    with st.spinner("🔗 서버 연결 중..."):
        time.sleep(1)
    st.info("서버 연결 성공!")

    progress_bar = st.progress(0)
    status_text = st.empty()
    speed_text = st.empty()

    downloaded = 0
    chunk_size = file_size // 20  # 20번에 나눠서 다운로드

    for i in range(20):
        downloaded += chunk_size
        progress = min(100, int((downloaded / file_size) * 100))
        progress_bar.progress(progress)

        # 다운로드 속도 시뮬레이션 (랜덤하게)
        speed = np.random.uniform(5, 15)
        status_text.text(f"📥 다운로드 중... {downloaded}MB / {file_size}MB")
        speed_text.text(f"⚡ 속도: {speed:.1f} MB/s")

        time.sleep(0.15)

    status_text.text(f"📥 다운로드 완료: {file_size}MB")
    speed_text.empty()
    st.success("✅ 파일 다운로드가 완료되었습니다!")

st.markdown("---")

# 실습 3: 에러 처리와 스피너, try-except 적용
st.subheader("실습 3: 데이터베이스 연결 시뮬레이션")

col_db1, col_db2 = st.columns(2)

with col_db1:
    db_type = st.selectbox("데이터베이스 선택:", ["MySQL", "PostgreSQL", "MongoDB", "SQLite"])

with col_db2:
    connection_timeout = st.slider("연결 타임아웃 (초)", 1, 10, 3)

error_rate = st.slider("에러 발생 확률 (%)", 0, 100, 30)

if st.button("데이터베이스 연결 테스트", key="practice3"):
    max_retries = 3

    for attempt in range(1, max_retries + 1):
        try:
            with st.spinner(f"🔌 {db_type}에 연결 시도 중... (시도 {attempt}/{max_retries})"):
                time.sleep(connection_timeout)

                # 에러 발생 시뮬레이션
                if np.random.randint(0, 100) < error_rate:
                    raise ConnectionError(f"{db_type} 연결 타임아웃")

                # 연결 성공
                st.success(f"✅ {db_type} 연결 성공! (시도 {attempt}회)")

                # 연결 정보 표시
                st.json({
                    "database": db_type,
                    "status": "connected",
                    "latency": f"{np.random.uniform(10, 50):.2f}ms",
                    "connection_id": f"conn_{np.random.randint(1000, 9999)}"
                })
                break

        except ConnectionError as e:
            st.warning(f"⚠️ 연결 실패 (시도 {attempt}): {str(e)}")

            if attempt == max_retries:
                st.error(f"❌ {max_retries}회 시도 후 연결 실패. 나중에 다시 시도해주세요.")
                st.info("💡 팁: 네트워크 상태를 확인하거나 에러 발생 확률을 낮춰보세요.")
            else:
                st.info(f"🔄 {2}초 후 재시도합니다...")
                time.sleep(2)

st.markdown("---")

# 실습 4: 실제 파일 로딩 또는 API 호출에 스피너 적용
st.subheader("실습 4: 외부 API 데이터 분석 시뮬레이션")

api_options = {
    "날씨 API": {"icon": "🌤️", "fields": ["도시", "온도", "습도", "날씨상태"]},
    "주식 API": {"icon": "📈", "fields": ["종목", "현재가", "변동률", "거래량"]},
    "뉴스 API": {"icon": "📰", "fields": ["제목", "출처", "발행일", "카테고리"]}
}

selected_api = st.selectbox("API 선택:", list(api_options.keys()))
record_count = st.slider("가져올 레코드 수:", 5, 50, 20)

if st.button("API 데이터 가져오기 및 분석", key="practice4"):
    api_info = api_options[selected_api]

    # 1단계: API 인증
    with st.spinner(f"{api_info['icon']} API 인증 중..."):
        time.sleep(1)
    st.success("🔑 API 인증 완료")

    # 2단계: 데이터 요청
    with st.spinner(f"📡 {selected_api}에서 데이터 요청 중..."):
        time.sleep(1.5)

        # 가짜 데이터 생성
        if selected_api == "날씨 API":
            data = pd.DataFrame({
                "도시": [f"City_{i}" for i in range(1, record_count + 1)],
                "온도": np.random.uniform(-10, 35, record_count).round(1),
                "습도": np.random.randint(20, 100, record_count),
                "날씨상태": np.random.choice(["맑음", "흐림", "비", "눈"], record_count)
            })
        elif selected_api == "주식 API":
            data = pd.DataFrame({
                "종목": [f"STOCK_{i:03d}" for i in range(1, record_count + 1)],
                "현재가": np.random.randint(10000, 500000, record_count),
                "변동률": np.random.uniform(-5, 5, record_count).round(2),
                "거래량": np.random.randint(1000, 1000000, record_count)
            })
        else:
            data = pd.DataFrame({
                "제목": [f"뉴스 기사 {i}" for i in range(1, record_count + 1)],
                "출처": np.random.choice(["조선일보", "중앙일보", "한겨레", "경향신문"], record_count),
                "발행일": pd.date_range(end="2024-12-01", periods=record_count).strftime("%Y-%m-%d"),
                "카테고리": np.random.choice(["정치", "경제", "사회", "문화"], record_count)
            })

    st.success(f"📥 {len(data)}개 레코드 수신 완료")

    # 3단계: 데이터 분석
    with st.spinner("🔍 데이터 분석 중..."):
        time.sleep(1)

    # 결과 표시
    tab1, tab2 = st.tabs(["📋 데이터", "📊 분석 결과"])

    with tab1:
        st.dataframe(data, width="stretch")

    with tab2:
        if selected_api == "날씨 API":
            col1, col2, col3 = st.columns(3)
            col1.metric("평균 온도", f"{data['온도'].mean():.1f}°C")
            col2.metric("평균 습도", f"{data['습도'].mean():.0f}%")
            col3.metric("맑은 날", f"{(data['날씨상태'] == '맑음').sum()}개")
        elif selected_api == "주식 API":
            col1, col2, col3 = st.columns(3)
            col1.metric("평균 주가", f"{data['현재가'].mean():,.0f}원")
            col2.metric("상승 종목", f"{(data['변동률'] > 0).sum()}개")
            col3.metric("총 거래량", f"{data['거래량'].sum():,}")
        else:
            col1, col2 = st.columns(2)
            col1.metric("총 기사 수", f"{len(data)}개")
            with col2:
                st.write("카테고리별 기사 수:")
                st.dataframe(data['카테고리'].value_counts())

    st.success("✅ 분석 완료!")

# ============================================
# 수강생을 위한 추가 학습 자료
# ============================================
st.markdown("---")
st.header("📚 수강생을 위한 심화 학습")

st.write("""
### 🎓 st.spinner()에 대해 더 알아두면 좋은 내용

---

#### 1. st.spinner() vs st.progress() - 언제 무엇을 사용할까?

| 상황 | 추천 컴포넌트 | 이유 |
|------|---------------|------|
| 작업 시간을 예측할 수 없을 때 | `st.spinner()` | 진행률을 알 수 없으므로 |
| 작업 진행률을 알 수 있을 때 | `st.progress()` | 사용자에게 더 정확한 정보 제공 |
| 여러 단계 작업 | 둘 다 함께 | 현재 단계 + 전체 진행률 |
| 1초 미만 작업 | 사용 안 함 | UI 깜빡임만 발생 |

---

#### 2. st.status() - Streamlit 1.25+ 신기능

`st.spinner()`의 업그레이드 버전인 `st.status()`를 사용하면 더 풍부한 로딩 UI를 만들 수 있습니다:

```python
with st.status("작업 처리 중...", expanded=True) as status:
    st.write("1단계: 데이터 로딩")
    time.sleep(1)
    st.write("2단계: 처리 중")
    time.sleep(1)
    status.update(label="완료!", state="complete", expanded=False)
```

**st.status()의 장점:**
- 진행 상황을 실시간으로 내부에 표시 가능
- `expanded` 파라미터로 접기/펼치기 가능
- `state` 파라미터로 상태 표시 (`running`, `complete`, `error`)

---

#### 3. @st.cache_data와 함께 사용하기

데이터 로딩 시 캐싱을 활용하면 두 번째 실행부터는 스피너가 거의 보이지 않습니다:

```python
@st.cache_data
def load_large_data():
    # 첫 실행: 느림, 두 번째부터: 캐시에서 즉시 로드
    return pd.read_csv("large_file.csv")

with st.spinner("데이터 로딩 중..."):
    df = load_large_data()  # 캐시되면 스피너가 거의 안 보임
```

**팁:** 캐시된 함수는 스피너 안에서 호출해도 됩니다. 캐시 히트 시 즉시 반환됩니다.

---

#### 4. 비동기 작업과 st.spinner()

실제 프로덕션에서는 비동기 처리가 필요할 수 있습니다:

```python
import asyncio

async def fetch_data_async():
    await asyncio.sleep(2)  # 비동기 API 호출
    return {"data": "result"}

# Streamlit에서 비동기 함수 실행
with st.spinner("비동기 작업 처리 중..."):
    result = asyncio.run(fetch_data_async())
```

---

#### 5. 사용자 경험(UX) 팁

| 팁 | 설명 |
|-----|------|
| **구체적인 메시지** | "처리 중..." → "1,000개 레코드 분석 중..." |
| **예상 시간 안내** | "대용량 파일 처리 중 (약 30초 소요)..." |
| **취소 버튼 제공** | 긴 작업에는 취소 옵션 고려 |
| **에러 복구 안내** | 실패 시 구체적인 해결 방법 제시 |

---

#### 6. 성능 모니터링 패턴

작업 시간을 측정하고 표시하는 패턴:

```python
import time

start_time = time.time()

with st.spinner("작업 처리 중..."):
    # 실제 작업
    heavy_computation()

elapsed = time.time() - start_time
st.success(f"완료! (소요 시간: {elapsed:.2f}초)")
```

---

#### 7. 자주 하는 실수들

| 실수 | 문제점 | 해결책 |
|------|--------|--------|
| 스피너 안에서 `st.write()` | 스피너 종료 전까지 안 보임 | 스피너 밖에서 출력 |
| 0.5초 미만 작업에 스피너 | 깜빡임만 발생 | 스피너 제거 |
| 에러 처리 누락 | 무한 로딩처럼 보임 | try-except 필수 |
| 중첩 스피너 과다 사용 | UI 복잡해짐 | st.status() 권장 |

---

#### 8. 실무에서 자주 쓰는 패턴 모음

```python
# 패턴 1: 재시도 로직
for attempt in range(3):
    try:
        with st.spinner(f"시도 {attempt + 1}/3..."):
            result = risky_operation()
        break
    except Exception:
        if attempt == 2:
            st.error("모든 시도 실패")

# 패턴 2: 조건부 스피너
if data_size > 10000:
    with st.spinner("대용량 처리 중..."):
        process(data)
else:
    process(data)  # 작은 데이터는 스피너 없이

# 패턴 3: 스피너 + 프로그레스 콤보
with st.spinner("전체 작업 진행 중..."):
    progress = st.progress(0)
    for i, item in enumerate(items):
        process(item)
        progress.progress((i + 1) / len(items))
```

---

### 💡 핵심 요약

1. **st.spinner()는 UX의 핵심** - 사용자가 앱이 멈춘 게 아님을 알 수 있음
2. **적절한 사용 시점** - 1~30초 작업에 적합, 더 긴 작업은 프로그레스 바 권장
3. **에러 처리 필수** - try-except와 함께 사용하여 실패 시 피드백 제공
4. **캐싱과 병행** - @st.cache_data로 반복 로딩 최소화
5. **Streamlit 1.25+** - st.status()로 더 풍부한 로딩 UI 구현 가능
""")

# ============================================
# 심화 학습 내용 실제 구현
# ============================================
st.markdown("---")
st.header("🔬 심화 학습 내용 실제 구현")

# 1. st.status() - 풍부한 로딩 UI
st.subheader("1. st.status() - 스피너의 업그레이드 버전")

if st.button("st.status() 실행", key="status_demo"):
    with st.status("작업 처리 중...", expanded=True) as status:
        st.write("📂 데이터 로딩...")
        time.sleep(1)
        st.write("🔍 분석 중...")
        time.sleep(1)
        status.update(label="✅ 완료!", state="complete", expanded=False)

# 2. @st.cache_data와 스피너 조합
st.subheader("2. @st.cache_data와 스피너")

@st.cache_data
def load_cached_data(size):
    time.sleep(2)
    return pd.DataFrame({'A': np.random.randn(size)})

if st.button("캐시 데이터 로드", key="cache_load_btn"):
    start_time = time.time()
    with st.spinner("📂 로딩 중..."):
        df = load_cached_data(1000)
    elapsed = time.time() - start_time

    if elapsed < 0.5:
        st.success(f"⚡ 캐시 히트! ({elapsed:.3f}초)")
    else:
        st.info(f"📥 첫 로드 ({elapsed:.2f}초) - 다음부터는 즉시 로드")

# 3. 재시도 로직 패턴
st.subheader("3. 재시도 로직 패턴")

if st.button("재시도 패턴 실행", key="retry_btn"):
    for attempt in range(1, 4):
        try:
            with st.spinner(f"🔄 시도 {attempt}/3..."):
                time.sleep(0.5)
                if np.random.random() < 0.5:
                    raise ConnectionError("연결 실패")
            st.success(f"✅ {attempt}번째 시도에 성공!")
            break
        except ConnectionError:
            if attempt < 3:
                st.warning(f"⚠️ 시도 {attempt} 실패, 재시도...")
            else:
                st.error("❌ 모든 시도 실패")

# 4. 스피너 + 프로그레스 콤보
st.subheader("4. 스피너 + 프로그레스 콤보")

if st.button("콤보 패턴 실행", key="combo_btn"):
    with st.spinner("🔄 전체 작업 진행 중..."):
        progress = st.progress(0)
        for i in range(10):
            time.sleep(0.2)
            progress.progress((i + 1) / 10, text=f"처리 중... {i + 1}/10")
    st.success("✅ 완료!")

# 5. 성능 모니터링 패턴
st.subheader("5. 성능 모니터링 패턴")

if st.button("성능 측정", key="perf_btn"):
    start = time.time()
    with st.spinner("작업 처리 중..."):
        time.sleep(np.random.uniform(1, 2))
    elapsed = time.time() - start
    st.success(f"✅ 완료! (소요 시간: {elapsed:.2f}초)")
