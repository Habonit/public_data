# 예제 13: 세션 상태 및 기타 필수 기능

## 학습 목표

- **st.session_state**를 사용한 상태 관리 (매우 중요!)
- 파일 업로드 및 다운로드
- 사이드바 활용
- 기타 유용한 위젯들

## 핵심 개념

### 1. Session State - 상태 관리

**가장 중요한 개념입니다!**

Streamlit은 사용자가 위젯과 상호작용할 때마다 스크립트를 처음부터 재실행합니다.
Session State를 사용하면 재실행 사이에 데이터를 유지할 수 있습니다.

```python
# 초기화
if 'counter' not in st.session_state:
    st.session_state.counter = 0

# 사용
if st.button("증가"):
    st.session_state.counter += 1

st.write(f"카운터: {st.session_state.counter}")
```

**주요 사용 사례:**
- 로그인 상태 유지
- 폼 데이터 임시 저장
- 장바구니/선택 항목
- 카운터/점수
- 다단계 프로세스

### 2. 파일 업로드

```python
uploaded_file = st.file_uploader(
    "파일 선택",
    type=['csv', 'xlsx', 'json']
)

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)
```

### 3. 파일 다운로드

```python
# CSV
csv = df.to_csv(index=False).encode('utf-8-sig')
st.download_button(
    "CSV 다운로드",
    data=csv,
    file_name='data.csv',
    mime='text/csv'
)

# Excel (openpyxl 필요)
output = io.BytesIO()
with pd.ExcelWriter(output, engine='openpyxl') as writer:
    df.to_excel(writer, index=False)
excel_data = output.getvalue()

st.download_button(
    "Excel 다운로드",
    data=excel_data,
    file_name='data.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)
```

### 4. 사이드바

```python
# 사이드바에 위젯 배치
st.sidebar.header("필터")
option = st.sidebar.selectbox("선택", ["A", "B", "C"])
value = st.sidebar.slider("값", 0, 100)
```

### 5. 기타 유용한 위젯

```python
# 색상 선택
color = st.color_picker("색상", "#FF6B6B")

# 카메라
photo = st.camera_input("사진 찍기")

# 이미지 표시
st.image("path/to/image.png", use_container_width=True)
```

## 현재 앱에서의 활용 가능성

현재 앱(`app.py`)에서는 Session State를 **직접 사용하지 않습니다**.
하지만 다음과 같은 기능 추가 시 필요합니다:

1. **즐겨찾기 기능**
   ```python
   if 'favorites' not in st.session_state:
       st.session_state.favorites = []

   # 지점을 즐겨찾기에 추가
   if st.button("⭐ 즐겨찾기"):
       st.session_state.favorites.append(location_data)
   ```

2. **필터 설정 저장**
   ```python
   if 'last_filters' not in st.session_state:
       st.session_state.last_filters = {}

   # 사용자가 마지막으로 선택한 필터 복원
   ```

3. **비교 기능**
   ```python
   if 'comparison_list' not in st.session_state:
       st.session_state.comparison_list = []

   # 여러 지점을 선택하여 비교
   ```

4. **데이터 내보내기**
   ```python
   # 필터링된 데이터 CSV 다운로드
   csv = filtered_df.to_csv(index=False).encode('utf-8-sig')
   st.download_button("데이터 다운로드", csv, "filtered_data.csv")
   ```

## 실행 방법

```bash
streamlit run 13_session_state.py
```

## 실습 과제

1. **로그인 시스템 구현**
   - Session State로 로그인 상태 관리
   - 로그인 시에만 특정 탭 표시

2. **북마크 기능**
   - 관심 있는 데이터 포인트 저장
   - 나중에 다시 확인

3. **데이터 필터 히스토리**
   - 이전에 사용한 필터 조합 저장
   - 빠른 재적용

4. **비교 모드**
   - 여러 지점/데이터 선택
   - 한 화면에서 비교

## Session State vs 캐싱

| 구분 | Session State | @st.cache_data |
|------|---------------|----------------|
| 용도 | 사용자 상태 | 데이터 로딩 |
| 범위 | 사용자별 세션 | 전체 사용자 공유 |
| 수명 | 세션 종료 시 | 캐시 만료 시 |
| 예시 | 장바구니, 로그인 | CSV 파일 로드 |

## 주의사항

1. **메모리 관리**
   - 너무 큰 데이터는 Session State에 저장하지 않기
   - 필요없는 상태는 삭제

2. **초기화 패턴**
   - 항상 존재 여부 확인 후 사용
   - `if 'key' not in st.session_state:`

3. **재실행**
   - `st.rerun()`으로 강제 재실행 가능
   - 상태 변경 후 즉시 반영 필요 시 사용

## 다음 단계

다음 예제(14)에서는 **이러한 기능들을 현재 앱에 실제로 추가하는 방법**을 배웁니다!
