# 예제 14: 현재 앱에 기능 추가하기

## 학습 목표

**가장 실전적인 예제입니다!**

- 현재 앱(`app.py`) 구조 완전 이해
- 새 탭 추가 방법
- 기존 기능 확장 방법
- 새 데이터셋 통합 방법
- 실전 개발 워크플로우

## 핵심 패턴

### 1. 새 탭 추가 (가장 자주 사용)

```python
# Step 1: 탭 목록에 추가 (app.py:147-157)
tabs = st.tabs([
    # ... 기존 탭들 ...
    "📖 프로젝트 개요",
    "⭐ 내 새 탭"  # ← 추가!
])

# Step 2: 탭 컨텐츠 작성
with tabs[9]:  # 인덱스 조정
    st.header("⭐ 내 새 탭")
    # 컨텐츠 작성
```

### 2. render_dataset_tab() 확장

```python
# 위치: app.py:23-136
def render_dataset_tab(dataset_name, dataset_display_name):
    # ... 기존 코드 ...

    # 새 기능 추가 위치:
    # 1) 데이터 로딩 직후 (35줄)
    # 2) 메트릭 다음 (55줄)
    # 3) 시각화 섹션 (78줄)
    # 4) 지도 표시 다음 (101줄)
```

### 3. 새 데이터셋 추가

```python
# utils/loader.py의 dataset_map 수정
dataset_map = {
    # ... 기존 ...
    'mynew': 'data/my_new_data.csv'  # ← 추가!
}

# app.py에서 사용
with tabs[X]:
    render_dataset_tab('mynew', '내 데이터')
```

## 실전 시나리오

### 시나리오 1: 데이터 다운로드 기능 추가

**목표:** 각 데이터셋을 CSV로 다운로드

**수정 위치:** `app.py:58` (데이터 미리보기 다음)

```python
# 기존 코드
with st.expander("📋 데이터 미리보기", expanded=False):
    st.dataframe(df.head(10), use_container_width=True)

# 추가 코드
st.markdown("---")
csv = df.to_csv(index=False).encode('utf-8-sig')
st.download_button(
    label=f"📥 {dataset_display_name} 전체 데이터 다운로드",
    data=csv,
    file_name=f'{dataset_name}_complete.csv',
    mime='text/csv',
    help=f"{len(df):,}개 행의 데이터를 CSV로 다운로드합니다"
)
```

**테스트:**
```bash
streamlit run app.py
# CCTV 탭 → 다운로드 버튼 확인
```

### 시나리오 2: 즐겨찾기 탭 추가

**목표:** 관심 데이터셋을 즐겨찾기

**Step 1:** 탭 추가 (`app.py:147-157`)

```python
tabs = st.tabs([
    # ... 기존 탭들 ...
    "📖 프로젝트 개요",
    "⭐ 즐겨찾기"  # 추가!
])
```

**Step 2:** 즐겨찾기 버튼 (`app.py:55` 메트릭 다음)

```python
# 메트릭 표시 후
col1, col2, col3 = st.columns(3)
# ...

# 즐겨찾기 버튼 추가
if st.button(f"⭐ {dataset_display_name} 즐겨찾기"):
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []

    if dataset_name not in st.session_state.favorites:
        st.session_state.favorites.append(dataset_name)
        st.success(f"✅ {dataset_display_name}을(를) 즐겨찾기에 추가했습니다!")
    else:
        st.info("이미 즐겨찾기에 추가되어 있습니다.")
```

**Step 3:** 즐겨찾기 탭 컨텐츠 (`app.py:534` 마지막)

```python
# Tab 9: 즐겨찾기
with tabs[9]:
    st.header("⭐ 즐겨찾기")

    if 'favorites' not in st.session_state:
        st.session_state.favorites = []

    if st.session_state.favorites:
        st.write(f"총 {len(st.session_state.favorites)}개의 데이터셋이 즐겨찾기되어 있습니다.")

        for fav_name in st.session_state.favorites:
            with st.expander(f"📊 {fav_name.upper()}"):
                # 즐겨찾기된 데이터셋 미리보기
                try:
                    fav_df = load_dataset(fav_name)
                    st.dataframe(fav_df.head(5))

                    if st.button(f"❌ 제거", key=f"remove_{fav_name}"):
                        st.session_state.favorites.remove(fav_name)
                        st.rerun()
                except Exception as e:
                    st.error(f"로딩 오류: {e}")
    else:
        st.info("즐겨찾기가 비어있습니다. 데이터셋 탭에서 ⭐ 버튼을 클릭하세요!")
```

### 시나리오 3: 새 데이터셋 추가

**목표:** "대구 공원 정보" 데이터셋 추가

**Step 1:** CSV 파일 준비

```bash
# 파일을 data/ 디렉토리에 복사
cp 대구_공원_정보.csv public_data/data/
```

**Step 2:** `utils/loader.py` 수정 (59-67줄)

```python
dataset_map = {
    'cctv': 'data/대구 CCTV 정보.csv',
    'lights': 'data/대구 보안등 정보.csv',
    'zones': 'data/대구 어린이 보호 구역 정보.csv',
    'parking': 'data/대구 주차장 정보.csv',
    'accident': 'data/countrywide_accident.csv',
    'train': 'data/train.csv',
    'test': 'data/test.csv',
    'parks': 'data/대구_공원_정보.csv'  # ← 추가!
}
```

**Step 3:** `app.py` 탭 추가 (147-157줄)

```python
tabs = st.tabs([
    "🎥 CCTV",
    "💡 보안등",
    "🏫 어린이 보호구역",
    "🅿️ 주차장",
    "🚗 사고",
    "🚂 기차",
    "📝 테스트",
    "🌳 공원",  # ← 추가!
    "🔄 교차 데이터 분석",
    "📖 프로젝트 개요"
])
```

**Step 4:** 탭 렌더링 추가 (186줄 다음)

```python
# Tab 6: Test
with tabs[6]:
    render_dataset_tab('test', '테스트')

# Tab 7: Parks (새로 추가!)
with tabs[7]:
    render_dataset_tab('parks', '공원')

# Tab 8: Cross-Data Analysis (인덱스 조정!)
with tabs[8]:
    st.header("🔄 교차 데이터 분석")
    # ...
```

**Step 5:** 교차 분석에도 추가 (198-206줄)

```python
available_datasets = {
    'CCTV': 'cctv',
    '보안등': 'lights',
    '어린이 보호구역': 'zones',
    '주차장': 'parking',
    '사고': 'accident',
    '기차': 'train',
    '공원': 'parks'  # ← 추가!
}
```

## 개발 워크플로우

### 1. 계획
- 무엇을 추가할지 명확히
- 어디에 추가할지 결정
- 필요한 리소스 확인

### 2. 개발
```bash
# 브랜치 생성
git checkout -b feature/my-feature

# 코드 수정
# ...

# 테스트
streamlit run app.py
```

### 3. 테스트 체크리스트
- [ ] 새 기능 정상 작동
- [ ] 기존 기능 영향 없음
- [ ] 모든 탭 확인
- [ ] 에러 처리 확인
- [ ] 다양한 데이터로 테스트

### 4. 커밋
```bash
git add .
git commit -m "feat: 즐겨찾기 기능 추가"
git push origin feature/my-feature
```

## 자주 하는 실수

### 1. 탭 인덱스 오류
```python
# ❌ 잘못됨 - 인덱스를 업데이트 안 함
tabs = st.tabs([..., "새 탭", "교차 분석", "개요"])

with tabs[7]:  # 여전히 7로 하드코딩
    st.header("교차 분석")  # 오류!

# ✅ 올바름 - 인덱스 조정
with tabs[8]:  # 8로 변경
    st.header("교차 분석")
```

### 2. Session State 초기화 누락
```python
# ❌ 잘못됨
st.session_state.favorites.append(item)  # KeyError!

# ✅ 올바름
if 'favorites' not in st.session_state:
    st.session_state.favorites = []
st.session_state.favorites.append(item)
```

### 3. 파일 경로 오류
```python
# ❌ 잘못됨
'mydata': 'my_new_data.csv'  # data/ 빠짐!

# ✅ 올바름
'mydata': 'data/my_new_data.csv'
```

## 실행 방법

```bash
streamlit run 14_extending_app.py
```

이 예제 자체가 가이드이므로, 탭별로 단계를 따라하세요!

## 다음 단계

1. ✅ 이 예제의 모든 탭 읽기
2. ✅ 각 시나리오 이해
3. ✅ `app.py` 실제 수정 시도
4. ✅ 간단한 기능부터 추가
5. ✅ 점진적으로 복잡한 기능 구현

## 마무리

축하합니다! 🎉

이제 현재 앱을 완전히 이해하고 수정할 수 있습니다.
- 예제 01-13: Streamlit 기초부터 고급까지
- 예제 14: 현재 앱에 적용하는 방법

**이제 실전입니다. `app.py`를 열고 시작하세요!**
