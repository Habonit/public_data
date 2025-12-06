# 예제 4: 사용자 입력 위젯

## 학습 목표

- 다양한 사용자 입력 위젯 사용법
- selectbox와 multiselect의 차이
- 폼(form)을 사용한 입력 처리
- 위젯의 상태 관리와 key 매개변수

## 핵심 위젯

### 1. `st.selectbox()` - 단일 선택
```python
option = st.selectbox(
    "레이블",
    options=["옵션1", "옵션2", "옵션3"],
    index=0,  # 기본 선택
    key="unique_key"
)
```

### 2. `st.multiselect()` - 다중 선택
```python
options = st.multiselect(
    "레이블",
    options=["A", "B", "C"],
    default=["A", "B"]
)
```

### 3. `st.slider()` - 슬라이더
```python
# 단일 값
value = st.slider("나이", 0, 100, 25)

# 범위 선택
range_val = st.slider("가격", 0, 1000, (100, 500))
```

### 4. `st.button()` - 버튼
```python
if st.button("클릭"):
    st.write("버튼이 클릭됨!")
```

### 5. `st.checkbox()` - 체크박스
```python
checked = st.checkbox("동의합니다", value=False)
```

### 6. `st.radio()` - 라디오 버튼
```python
choice = st.radio("선택", ["옵션1", "옵션2"], horizontal=True)
```

## 폼(Form) 사용

```python
with st.form("my_form"):
    name = st.text_input("이름")
    age = st.slider("나이", 0, 100)

    submitted = st.form_submit_button("제출")
    if submitted:
        st.write(f"{name}, {age}세")
```

## 현재 앱에서의 사용

```python
# app.py:111-115 - selectbox
selected_numeric_col = st.selectbox(
    "시각화할 숫자 컬럼 선택:",
    options=numeric_cols,
    key=f"{dataset_name}_numeric_select"
)

# app.py:208-212 - multiselect
selected_names = st.multiselect(
    "분석할 데이터셋을 선택하세요:",
    options=list(available_datasets.keys()),
    default=['CCTV', '보안등']
)

# app.py:303 - button
if st.button("근접성 분석 실행"):
    # 분석 로직
```

## 실행 방법

```bash
streamlit run 04_user_inputs.py
```
