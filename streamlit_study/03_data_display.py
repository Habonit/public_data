"""
예제 3: 데이터 표시 및 캐싱 (DataFrames and Caching)

이 예제에서는 Pandas 데이터프레임 표시와 st.cache_data를 학습합니다.
"""
import streamlit as st
import pandas as pd
import numpy as np
import time

st.set_page_config(
    page_title="데이터 표시 및 캐싱",
    page_icon="📊",
    layout="wide"
)

st.title("📊 데이터 표시 및 캐싱")

# ============================================
# 1. 데이터프레임 생성
# ============================================
st.header("1. 데이터프레임 생성")

# 샘플 데이터 생성
df = pd.DataFrame({
    '이름': ['김철수', '이영희', '박민수', '정수진', '최지호'],
    '나이': [25, 30, 35, 28, 32],
    '부서': ['개발', '디자인', '개발', '마케팅', '영업'],
    '급여': [5000, 4500, 6000, 4800, 5200],
    '입사일': pd.date_range('2020-01-01', periods=5, freq='6M')
})

st.write("생성된 데이터프레임:")
st.write(df)

# ============================================
# 2. st.dataframe() - 인터랙티브 표
# ============================================
st.header("2. st.dataframe() - 인터랙티브 표")

st.markdown("""
`st.dataframe()`은 인터랙티브한 표를 생성합니다.
- 정렬 가능 (컬럼 헤더 클릭)
- 스크롤 가능
- 검색 가능
""")

st.dataframe(
    df,
    width="stretch",  # 전체 너비 사용
    hide_index=False,           # 인덱스 표시
    height=250                  # 높이 지정 (픽셀)
)

# ============================================
# 3. st.table() - 정적 표
# ============================================
st.header("3. st.table() - 정적 표")

st.markdown("""
`st.table()`은 정적인 표를 생성합니다.
- 정렬 불가
- 모든 데이터를 한 번에 표시
- 작은 데이터셋에 적합
""")

st.table(df.head(3))

# ============================================
# 4. 데이터프레임 스타일링
# ============================================
st.header("4. 데이터프레임 스타일링")

st.markdown("""
Pandas의 스타일 기능을 사용하여 데이터를 강조할 수 있습니다.
""")

# 급여 컬럼에 그라데이션 적용
styled_df = df.style.background_gradient(
    subset=['급여'],
    cmap='YlOrRd'
).format({'급여': '₩{:,.0f}'})

st.dataframe(styled_df, width="stretch")

# ============================================
# 5. 데이터프레임 필터링
# ============================================
st.header("5. 데이터프레임 필터링 및 조작")

# 부서별 필터링
selected_dept = st.selectbox(
    "부서 선택:",
    options=['전체'] + list(df['부서'].unique())
)

if selected_dept == '전체':
    filtered_df = df
else:
    filtered_df = df[df['부서'] == selected_dept]

st.write(f"선택된 부서: **{selected_dept}** ({len(filtered_df)}명)")
st.dataframe(filtered_df, width="stretch")

# 통계 정보 표시
if len(filtered_df) > 0:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("인원 수", f"{len(filtered_df)}명")
    with col2:
        st.metric("평균 나이", f"{filtered_df['나이'].mean():.1f}세")
    with col3:
        st.metric("평균 급여", f"₩{filtered_df['급여'].mean():,.0f}")

# ============================================
# 6. 캐싱 (st.cache_data)
# ============================================
st.header("6. 캐싱 (st.cache_data)")

st.markdown("""
`@st.cache_data`는 데이터 로딩 함수의 결과를 캐싱합니다.
- 같은 입력에 대해 함수를 다시 실행하지 않음
- 앱 성능을 크게 향상
- 데이터 로딩, API 호출 등에 필수적
""")

# 캐싱 없이
st.subheader("6.1 캐싱 없이")

def load_data_no_cache():
    """캐싱 없이 데이터 로드 (느림)"""
    time.sleep(2)  # 느린 작업 시뮬레이션
    return pd.DataFrame({
        'x': np.random.randn(1000),
        'y': np.random.randn(1000)
    })

if st.button("캐싱 없이 데이터 로드 (2초 대기)"):
    start_time = time.time()
    data = load_data_no_cache()
    elapsed_time = time.time() - start_time
    st.success(f"로딩 완료! 소요 시간: {elapsed_time:.2f}초")
    st.write(f"데이터 크기: {len(data)} 행")

# 캐싱 사용
st.subheader("6.2 캐싱 사용")

@st.cache_data
def load_data_with_cache():
    """캐싱을 사용하여 데이터 로드 (첫 번째만 느림)"""
    time.sleep(2)  # 느린 작업 시뮬레이션
    return pd.DataFrame({
        'x': np.random.randn(1000),
        'y': np.random.randn(1000)
    })

if st.button("캐싱으로 데이터 로드 (첫 번째만 2초)"):
    start_time = time.time()
    data = load_data_with_cache()
    elapsed_time = time.time() - start_time
    st.success(f"로딩 완료! 소요 시간: {elapsed_time:.2f}초")
    st.info("다시 버튼을 눌러보세요. 즉시 로딩됩니다!")
    st.write(f"데이터 크기: {len(data)} 행")

# ============================================
# 7. 캐싱 매개변수
# ============================================
st.header("7. 캐싱 고급 기능")

st.markdown("""
캐싱 함수에 매개변수를 전달하면, 매개변수가 다를 때마다 별도로 캐싱됩니다.
""")

@st.cache_data
def generate_data(num_rows, seed):
    """매개변수에 따라 다른 데이터 생성"""
    time.sleep(1)  # 로딩 시뮬레이션
    np.random.seed(seed)
    return pd.DataFrame({
        'A': np.random.randn(num_rows),
        'B': np.random.randn(num_rows),
        'C': np.random.choice(['X', 'Y', 'Z'], num_rows)
    })

col1, col2 = st.columns(2)
with col1:
    num_rows = st.slider("행 개수", 10, 1000, 100)
with col2:
    seed = st.number_input("시드 값", 0, 100, 42)

if st.button("데이터 생성"):
    with st.spinner("데이터 생성 중..."):
        data = generate_data(num_rows, seed)
    st.success(f"{len(data)}개 행 생성 완료!")
    st.dataframe(data.head(10), width="stretch")
    st.info("동일한 매개변수로 다시 실행하면 캐시된 결과를 즉시 반환합니다.")

# ============================================
# 8. 실전 예제: CSV 파일 로더
# ============================================
st.header("8. 실전 예제: CSV 파일 로더")

@st.cache_data
def load_csv_cached(file_path):
    """CSV 파일을 캐싱하여 로드"""
    return pd.read_csv(file_path)

st.markdown("""
실제 앱에서는 이렇게 CSV 파일을 캐싱하여 로드합니다:

```python
@st.cache_data
def load_dataset(dataset_name: str) -> pd.DataFrame:
    dataset_map = {
        'cctv': 'data/대구 CCTV 정보.csv',
        'lights': 'data/대구 보안등 정보.csv',
        ...
    }
    file_path = dataset_map[dataset_name]
    return pd.read_csv(file_path)
```

이렇게 하면 파일을 한 번만 읽고, 이후에는 캐시된 데이터를 사용합니다.
""")

# ============================================
# 실습 섹션
# ============================================
st.markdown("---")
st.header("🎯 실습해보세요!")

st.markdown("""
1. 자신만의 데이터프레임을 만들어보세요
2. `st.dataframe()`의 다양한 옵션을 시도해보세요
3. Pandas 스타일 함수를 더 탐색해보세요 (highlight_max, bar 등)
4. 캐싱을 사용하는 함수를 작성하고 성능 차이를 확인해보세요
5. 캐시 매개변수를 변경하며 캐싱 동작을 관찰해보세요
""")

# --------------------------------------------
# 실습 1: 나만의 데이터프레임 만들기
# --------------------------------------------
st.subheader("실습 1: 나만의 데이터프레임 만들기")

# 사용자가 데이터를 입력할 수 있는 UI
st.write("**직접 데이터를 입력해보세요:**")

col1, col2 = st.columns(2)
with col1:
    num_rows = st.slider("행 개수:", 3, 10, 5, key="practice_rows")
with col2:
    include_random = st.checkbox("랜덤 데이터 포함", value=True)

# 동적 데이터프레임 생성
practice_df = pd.DataFrame({
    '제품명': [f'제품 {chr(65+i)}' for i in range(num_rows)],
    '가격': np.random.randint(10000, 100000, num_rows) if include_random else [10000 * (i+1) for i in range(num_rows)],
    '재고': np.random.randint(10, 200, num_rows) if include_random else [50 * (i+1) for i in range(num_rows)],
    '평점': np.round(np.random.uniform(3.0, 5.0, num_rows), 1) if include_random else [4.0] * num_rows
})

st.dataframe(practice_df, width="stretch")

st.code("""
# 데이터프레임 생성 코드
import pandas as pd
import numpy as np

df = pd.DataFrame({
    '제품명': ['제품 A', '제품 B', '제품 C'],
    '가격': [10000, 20000, 30000],
    '재고': [100, 50, 30],
    '평점': [4.5, 4.0, 4.8]
})
""", language="python")

# --------------------------------------------
# 실습 2: 다양한 스타일 함수 적용
# --------------------------------------------
st.subheader("실습 2: Pandas 스타일 함수 활용")

st.write("**다양한 스타일 함수 비교:**")

style_option = st.selectbox(
    "스타일 선택:",
    ["기본", "최대값 강조", "최소값 강조", "그라데이션", "바 차트", "전체 스타일"]
)

sample_df = pd.DataFrame({
    '이름': ['김철수', '이영희', '박민수', '정수진'],
    '국어': [85, 92, 78, 88],
    '영어': [90, 85, 95, 82],
    '수학': [88, 78, 92, 95]
})

numeric_cols = ['국어', '영어', '수학']

if style_option == "기본":
    st.dataframe(sample_df, width="stretch")

elif style_option == "최대값 강조":
    styled = sample_df.style.highlight_max(subset=numeric_cols, color='lightgreen')
    st.dataframe(styled, width="stretch")
    st.code("df.style.highlight_max(subset=['국어', '영어', '수학'], color='lightgreen')")

elif style_option == "최소값 강조":
    styled = sample_df.style.highlight_min(subset=numeric_cols, color='lightcoral')
    st.dataframe(styled, width="stretch")
    st.code("df.style.highlight_min(subset=['국어', '영어', '수학'], color='lightcoral')")

elif style_option == "그라데이션":
    styled = sample_df.style.background_gradient(subset=numeric_cols, cmap='Blues')
    st.dataframe(styled, width="stretch")
    st.code("df.style.background_gradient(subset=['국어', '영어', '수학'], cmap='Blues')")

elif style_option == "바 차트":
    styled = sample_df.style.bar(subset=numeric_cols, color='steelblue')
    st.dataframe(styled, width="stretch")
    st.code("df.style.bar(subset=['국어', '영어', '수학'], color='steelblue')")

elif style_option == "전체 스타일":
    styled = (sample_df.style
              .highlight_max(subset=numeric_cols, color='lightgreen')
              .highlight_min(subset=numeric_cols, color='lightcoral')
              .format(subset=numeric_cols, formatter='{:.0f}점'))
    st.dataframe(styled, width="stretch")
    st.code("""
df.style
  .highlight_max(subset=numeric_cols, color='lightgreen')
  .highlight_min(subset=numeric_cols, color='lightcoral')
  .format(subset=numeric_cols, formatter='{:.0f}점')
""")

# --------------------------------------------
# 실습 3: 데이터프레임 편집 기능
# --------------------------------------------
st.subheader("실습 3: 데이터프레임 편집 (st.data_editor)")

st.write("**st.data_editor()로 직접 데이터를 편집해보세요:**")

editable_df = pd.DataFrame({
    '할일': ['Streamlit 학습', '데이터 분석', '보고서 작성'],
    '완료': [True, False, False],
    '우선순위': [1, 2, 3],
    '마감일': pd.to_datetime(['2024-03-01', '2024-03-05', '2024-03-10'])
})

edited_df = st.data_editor(
    editable_df,
    width="stretch",
    num_rows="dynamic",  # 행 추가/삭제 가능
    column_config={
        "완료": st.column_config.CheckboxColumn("완료?", default=False),
        "우선순위": st.column_config.NumberColumn("우선순위", min_value=1, max_value=5),
        "마감일": st.column_config.DateColumn("마감일", format="YYYY-MM-DD")
    }
)

st.write("**편집된 결과:**")
st.write(f"- 완료된 항목: {edited_df['완료'].sum()}개")
st.write(f"- 미완료 항목: {(~edited_df['완료']).sum()}개")

st.code("""
# st.data_editor 사용법
edited_df = st.data_editor(
    df,
    width="stretch",
    num_rows="dynamic",  # 행 추가/삭제 허용
    column_config={
        "완료": st.column_config.CheckboxColumn("완료?"),
        "우선순위": st.column_config.NumberColumn("우선순위", min_value=1, max_value=5),
        "마감일": st.column_config.DateColumn("마감일", format="YYYY-MM-DD")
    }
)
""", language="python")

# --------------------------------------------
# 실습 4: 캐싱 성능 비교
# --------------------------------------------
st.subheader("실습 4: 캐싱 성능 직접 비교")

st.write("**버튼을 번갈아 눌러서 캐싱의 효과를 확인해보세요:**")

@st.cache_data
def heavy_computation_cached(n):
    """캐싱된 무거운 연산"""
    time.sleep(2)
    return pd.DataFrame({
        'x': range(n),
        'y': [i**2 for i in range(n)]
    })

def heavy_computation_no_cache(n):
    """캐싱 없는 무거운 연산"""
    time.sleep(2)
    return pd.DataFrame({
        'x': range(n),
        'y': [i**2 for i in range(n)]
    })

comp_col1, comp_col2 = st.columns(2)

with comp_col1:
    if st.button("캐싱 없이 실행", key="no_cache_btn"):
        start = time.time()
        result = heavy_computation_no_cache(100)
        elapsed = time.time() - start
        st.error(f"소요 시간: {elapsed:.2f}초")
        st.write(f"결과: {len(result)}행")

with comp_col2:
    if st.button("캐싱으로 실행", key="cache_btn"):
        start = time.time()
        result = heavy_computation_cached(100)
        elapsed = time.time() - start
        st.success(f"소요 시간: {elapsed:.2f}초")
        st.write(f"결과: {len(result)}행")
        if elapsed < 0.1:
            st.info("캐시에서 즉시 로드됨!")

# 추가 정보
with st.expander("💡 캐싱 관련 팁"):
    st.markdown("""
    **언제 캐싱을 사용해야 할까?**
    - CSV, Excel 파일 로딩
    - API 호출
    - 복잡한 계산
    - 데이터 전처리

    **캐싱하면 안 되는 경우:**
    - 매번 다른 결과가 필요한 경우 (난수 생성 등)
    - 실시간 데이터
    - 매우 큰 데이터 (메모리 문제)

    **캐시 초기화:**
    - 앱 실행 중 `C` 키 → "Clear cache"
    - 코드에서: `st.cache_data.clear()`
    """)
