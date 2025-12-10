# 예제 3: 데이터 표시 및 캐싱

## 학습 목표

이 예제를 통해 다음을 학습합니다:
- Pandas 데이터프레임을 Streamlit에 표시하는 방법
- `st.dataframe()` vs `st.table()` 차이점
- 데이터프레임 스타일링
- `@st.cache_data`를 사용한 성능 최적화
- 캐싱의 작동 원리와 활용법

## 핵심 개념

### 1. `st.dataframe()` - 인터랙티브 표

사용자가 상호작용할 수 있는 동적 표를 생성합니다.

```python
st.dataframe(
    df,
    use_container_width=True,  # 컨테이너 전체 너비 사용
    hide_index=False,           # 인덱스 표시 여부
    height=300                  # 높이 (픽셀)
)
```

**특징:**
- ✅ 컬럼 헤더 클릭으로 정렬 가능
- ✅ 스크롤 지원 (큰 데이터셋)
- ✅ 검색 기능
- ✅ 복사/붙여넣기 지원

**언제 사용?**
- 큰 데이터셋 (100+ 행)
- 사용자가 데이터를 탐색해야 할 때
- 정렬/필터링이 필요할 때

### 2. `st.table()` - 정적 표

모든 데이터를 한 번에 표시하는 정적 표입니다.

```python
st.table(df)
```

**특징:**
- 정렬 불가
- 모든 행을 한 번에 렌더링
- 스크롤 없음

**언제 사용?**
- 작은 데이터셋 (< 20행)
- 요약 통계 표시
- 고정된 형식이 필요할 때

### 3. 데이터프레임 스타일링

Pandas의 `style` API를 사용하여 데이터를 시각적으로 강조합니다.

```python
# 배경 그라데이션
styled = df.style.background_gradient(
    subset=['급여'],  # 적용할 컬럼
    cmap='YlOrRd'     # 색상 맵
)

# 최대값 강조
styled = df.style.highlight_max(subset=['점수'])

# 최소값 강조
styled = df.style.highlight_min(subset=['비용'])

# 숫자 포맷팅
styled = df.style.format({
    '급여': '₩{:,.0f}',
    '비율': '{:.2%}'
})

# 여러 스타일 체이닝
styled = df.style\
    .background_gradient(subset=['급여'], cmap='YlGn')\
    .highlight_max(subset=['점수'])\
    .format({'급여': '₩{:,.0f}'})

st.dataframe(styled)
```

**주요 메서드:**
- `background_gradient()`: 배경색 그라데이션
- `highlight_max()`: 최대값 강조
- `highlight_min()`: 최소값 강조
- `format()`: 숫자/날짜 포맷팅
- `bar()`: 막대 차트 표시

### 4. `@st.cache_data` - 데이터 캐싱

함수의 결과를 캐싱하여 반복 실행을 방지합니다.

```python
@st.cache_data
def load_data():
    # 시간이 오래 걸리는 작업
    df = pd.read_csv('large_file.csv')
    return df

# 첫 번째 호출: 느림 (파일 읽기)
data = load_data()

# 두 번째 호출: 빠름 (캐시에서 가져옴)
data = load_data()
```

**작동 원리:**
1. 함수가 호출되면 입력 매개변수를 확인
2. 같은 매개변수로 이전에 실행된 적이 있으면 캐시된 결과 반환
3. 없으면 함수 실행 후 결과를 캐시에 저장

**매개변수가 있는 경우:**
```python
@st.cache_data
def load_data(file_name, encoding='utf-8'):
    return pd.read_csv(file_name, encoding=encoding)

# 각각 별도로 캐싱됨
data1 = load_data('file1.csv')
data2 = load_data('file2.csv')
data3 = load_data('file1.csv', encoding='cp949')
```

### 5. 캐싱 베스트 프랙티스

#### ✅ 캐싱을 사용해야 하는 경우
```python
@st.cache_data
def load_csv(file_path):
    """파일 I/O는 느리므로 캐싱 필수"""
    return pd.read_csv(file_path)

@st.cache_data
def expensive_computation(data):
    """복잡한 계산은 캐싱"""
    return data.groupby('category').agg({'value': 'mean'})

@st.cache_data
def fetch_api_data(url):
    """API 호출은 캐싱하여 재사용"""
    return requests.get(url).json()
```

#### ❌ 캐싱하면 안 되는 경우
```python
# 매번 다른 결과가 필요한 경우
def generate_random_data():
    return np.random.randn(100)  # 캐싱 X

# 실시간 데이터
def get_current_time():
    return datetime.now()  # 캐싱 X

# 사용자 입력에 직접 의존
def process_user_input(user_text):
    # 입력이 매번 다르므로 캐싱 효과 적음
    return user_text.upper()
```

### 6. 캐시 관리

```python
# 캐시 초기화
st.cache_data.clear()

# TTL (Time To Live) 설정
@st.cache_data(ttl=3600)  # 1시간 후 캐시 만료
def load_data():
    return pd.read_csv('data.csv')

# 캐시 크기 제한
@st.cache_data(max_entries=10)  # 최대 10개 항목만 캐싱
def load_data(file_name):
    return pd.read_csv(file_name)
```

## 실행 방법

```bash
cd streamlit_study
streamlit run 03_data_display.py
```

## 실습 과제

1. **데이터프레임 스타일링**
   - `highlight_max()`와 `highlight_min()` 동시 사용
   - `bar()` 메서드로 인라인 차트 만들기
   - 조건부 포맷팅 적용

2. **캐싱 실험**
   - 캐싱 없이 함수 실행 → 시간 측정
   - 캐싱 추가 → 시간 차이 확인
   - 다른 매개변수로 호출하며 캐싱 동작 관찰

3. **데이터 필터링**
   - 여러 조건 필터링 (부서 + 나이)
   - 필터링된 데이터의 통계 표시
   - 동적 컬럼 선택 기능 추가

4. **실제 데이터 로딩**
   - CSV 파일 로더 함수 작성
   - 캐싱 적용
   - 에러 처리 추가

## 현재 앱(`app.py`)에서의 사용 예시

### 데이터 캐싱
```python
# utils/loader.py:43-77
@st.cache_data
def load_dataset(dataset_name: str) -> pd.DataFrame:
    dataset_map = {
        'cctv': 'data/대구 CCTV 정보.csv',
        'lights': 'data/대구 보안등 정보.csv',
        ...
    }
    file_path = dataset_map[dataset_name]
    return read_csv_safe(file_path)
```

### 데이터프레임 표시
```python
# app.py:58-59
with st.expander("📋 데이터 미리보기", expanded=False):
    st.dataframe(df.head(10), use_container_width=True)

# app.py:62-70
with st.expander("📊 컬럼 정보", expanded=False):
    col_info_df = [...]
    st.dataframe(col_info_df, use_container_width=True)
```

### 통계 표시
```python
# app.py:73-75
with st.expander("📈 숫자 컬럼 통계", expanded=False):
    st.dataframe(info['numeric_summary'], use_container_width=True)
```

## 주요 포인트

1. ✅ 큰 데이터는 `st.dataframe()`, 작은 요약은 `st.table()`
2. ✅ 스타일링으로 데이터 가독성 향상
3. ✅ 파일 로딩, API 호출, 복잡한 계산은 반드시 캐싱
4. ✅ 캐시는 매개변수별로 별도 저장
5. ⚠️ 너무 큰 데이터는 메모리 문제 발생 가능
6. 💡 `use_container_width=True`로 반응형 표 구현

## 다음 단계

다음 예제에서는 **사용자 입력 위젯**을 학습하여 인터랙티브한 앱을 만드는 방법을 배웁니다.

## 참고 자료

- [Streamlit API Reference - Data elements](https://docs.streamlit.io/library/api-reference/data)
- [Streamlit Caching](https://docs.streamlit.io/library/advanced-features/caching)
- [Pandas Styling](https://pandas.pydata.org/docs/user_guide/style.html)
