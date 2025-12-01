"""
예제 14: 현재 앱에 기능 추가하기

이 예제에서는 현재 앱(app.py)에 새로운 기능을 추가하는 방법을 단계별로 학습합니다.
실제로 사용할 수 있는 코드와 가이드를 제공합니다.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

st.set_page_config(
    page_title="앱 확장 가이드",
    page_icon="🔌",
    layout="wide"
)

st.title("🔌 현재 앱에 기능 추가하기")

st.markdown("""
이 예제는 **실전 가이드**입니다.
여기서 배운 패턴을 그대로 `app.py`에 적용할 수 있습니다.
""")

# ============================================
# 가이드 탭 구성
# ============================================
tabs = st.tabs([
    "📚 1. 구조 이해",
    "➕ 2. 새 탭 추가",
    "🔧 3. 기능 확장",
    "💾 4. 데이터 추가",
    "🎨 5. UI 개선",
    "✅ 6. 체크리스트"
])

# ============================================
# 탭 1: 구조 이해
# ============================================
with tabs[0]:
    st.header("1. 현재 앱 구조 이해")

    st.markdown("""
    ## 📁 파일 구조

    ```
    public_data/
    ├── app.py                 # 메인 앱
    ├── utils/
    │   ├── loader.py         # 데이터 로딩
    │   ├── visualizer.py     # 차트/지도
    │   └── geo.py            # 지리 계산
    ├── data/                  # CSV 파일들
    └── streamlit_study/       # 이 학습 자료
    ```

    ## 🔍 app.py 주요 부분

    ### 1) 페이지 설정 (15-20줄)
    ```python
    st.set_page_config(
        page_title="대구 공공데이터 시각화",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    ```

    ### 2) 재사용 함수 (23-136줄)
    ```python
    def render_dataset_tab(dataset_name: str, dataset_display_name: str):
        # 각 데이터셋 탭을 렌더링하는 공통 함수
        # 이 패턴을 이해하면 쉽게 확장 가능!
    ```

    ### 3) 메인 함수 (138-537줄)
    ```python
    def main():
        st.title("...")

        # 탭 생성 (147-157줄)
        tabs = st.tabs([
            "🎥 CCTV",
            "💡 보안등",
            # ...
        ])

        # 각 탭 렌더링 (160-186줄)
        with tabs[0]:
            render_dataset_tab('cctv', 'CCTV')

        # 교차 분석 (187-349줄)
        with tabs[7]:
            # 복잡한 로직
    ```

    ## 🎯 확장 포인트

    새 기능을 추가할 수 있는 주요 지점:

    1. **새 탭 추가** → `tabs = st.tabs([...])` 부분
    2. **새 데이터셋** → `utils/loader.py`의 `dataset_map`
    3. **새 시각화** → `utils/visualizer.py`에 함수 추가
    4. **새 분석** → 교차 분석 탭 패턴 참고
    """)

    st.info("""
    💡 **핵심:** 현재 앱은 모듈화가 잘 되어 있습니다.
    - `utils/` 모듈의 함수들을 재사용
    - `render_dataset_tab()` 패턴을 따름
    - 새 기능은 기존 구조에 맞춰 추가
    """)

# ============================================
# 탭 2: 새 탭 추가
# ============================================
with tabs[1]:
    st.header("2. 새 탭 추가하기")

    st.markdown("""
    ## 📋 단계별 가이드

    ### Step 1: app.py의 탭 목록 수정

    **위치:** `app.py` 147-157줄

    ```python
    # 기존 코드
    tabs = st.tabs([
        "🎥 CCTV",
        "💡 보안등",
        # ...
        "📖 프로젝트 개요"
    ])

    # 새 탭 추가 (맨 뒤에 추가)
    tabs = st.tabs([
        "🎥 CCTV",
        "💡 보안등",
        # ... 기존 탭들 ...
        "📖 프로젝트 개요",
        "⭐ 즐겨찾기"  # ← 새 탭!
    ])
    ```

    ### Step 2: 탭 컨텐츠 추가

    **위치:** `app.py` 351줄 (프로젝트 개요 탭 다음)

    ```python
    # Tab 8: 프로젝트 개요
    with tabs[8]:
        st.header("📖 프로젝트 개요")
        # ... 기존 코드 ...

    # Tab 9: 즐겨찾기 (새로 추가!)
    with tabs[9]:
        st.header("⭐ 즐겨찾기")
        st.markdown(\"\"\"
        즐겨찾기한 지점들을 관리합니다.
        \"\"\")

        # Session State 초기화
        if 'favorites' not in st.session_state:
            st.session_state.favorites = []

        # 즐겨찾기 목록 표시
        if st.session_state.favorites:
            for fav in st.session_state.favorites:
                st.write(f"- {fav}")
        else:
            st.info("즐겨찾기가 비어있습니다.")
    ```

    ### Step 3: 테스트

    ```bash
    streamlit run app.py
    ```

    새 탭이 표시되는지 확인!
    """)

    st.success("""
    ✅ **성공 기준:**
    - 새 탭이 탭 목록에 표시됨
    - 탭 클릭 시 컨텐츠가 보임
    - 에러 없이 실행됨
    """)

    # 실제 동작 예시
    st.markdown("---")
    st.subheader("💻 실제 동작 예시")

    demo_tabs = st.tabs(["기존 탭", "새 탭 (즐겨찾기)"])

    with demo_tabs[0]:
        st.write("기존 탭의 내용")

    with demo_tabs[1]:
        st.write("### ⭐ 즐겨찾기")

        if 'demo_favorites' not in st.session_state:
            st.session_state.demo_favorites = []

        new_fav = st.text_input("즐겨찾기 추가", key="demo_fav")
        if st.button("추가") and new_fav:
            st.session_state.demo_favorites.append(new_fav)

        if st.session_state.demo_favorites:
            for idx, fav in enumerate(st.session_state.demo_favorites):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"{idx+1}. {fav}")
                with col2:
                    if st.button("삭제", key=f"del_{idx}"):
                        st.session_state.demo_favorites.pop(idx)
                        st.rerun()

# ============================================
# 탭 3: 기능 확장
# ============================================
with tabs[2]:
    st.header("3. 기존 기능 확장하기")

    st.markdown("""
    ## 🔧 render_dataset_tab() 확장

    현재 앱의 핵심 함수인 `render_dataset_tab()`에 기능을 추가하는 방법입니다.

    ### 예시 1: 데이터 다운로드 버튼 추가

    **위치:** `app.py` 58줄 (데이터 미리보기 expander 다음)

    ```python
    # 기존 코드
    with st.expander("📋 데이터 미리보기", expanded=False):
        st.dataframe(df.head(10), width="stretch")

    # 추가: 다운로드 버튼
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 전체 데이터 다운로드",
        data=csv,
        file_name=f'{dataset_name}_data.csv',
        mime='text/csv'
    )
    ```

    ### 예시 2: 즐겨찾기 기능 추가

    **위치:** `app.py` 100줄 (지도 표시 부분)

    ```python
    # 기존 지도 표시 코드
    st_folium(map_obj, width=700, height=500)

    # 추가: 즐겨찾기 버튼
    if st.button(f"⭐ {dataset_display_name} 즐겨찾기에 추가"):
        if 'favorites' not in st.session_state:
            st.session_state.favorites = []

        st.session_state.favorites.append({
            'name': dataset_display_name,
            'dataset': dataset_name,
            'timestamp': datetime.now()
        })
        st.success(f"{dataset_display_name}을(를) 즐겨찾기에 추가했습니다!")
    ```

    ### 예시 3: 추가 통계 표시

    **위치:** `app.py` 55줄 (메트릭 다음)

    ```python
    # 기존 메트릭
    col1, col2, col3 = st.columns(3)
    # ...

    # 추가: 더 많은 통계
    st.subheader("📊 추가 통계")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if '날짜' in df.columns:
            st.metric("최신 데이터", df['날짜'].max())

    with col2:
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            st.metric("숫자 컬럼 수", len(numeric_cols))

    # ... 더 추가
    ```
    """)

    st.info("""
    💡 **수정 팁:**
    1. 작은 변경부터 시작
    2. 한 번에 하나씩 추가
    3. 각 추가마다 테스트
    4. Git으로 버전 관리
    """)

# ============================================
# 탭 4: 새 데이터셋 추가
# ============================================
with tabs[3]:
    st.header("4. 새 데이터셋 추가하기")

    st.markdown("""
    ## 📊 데이터셋 추가 3단계

    ### Step 1: CSV 파일 준비

    ```bash
    # 파일을 data/ 디렉토리에 복사
    cp my_new_data.csv public_data/data/
    ```

    **필수 요구사항:**
    - CSV 형식
    - 인코딩: UTF-8 또는 CP949
    - (선택) 위도/경도 컬럼 (지도 표시용)

    ### Step 2: loader.py 수정

    **파일:** `utils/loader.py`
    **위치:** 59-67줄

    ```python
    # 기존 dataset_map
    dataset_map = {
        'cctv': 'data/대구 CCTV 정보.csv',
        'lights': 'data/대구 보안등 정보.csv',
        'zones': 'data/대구 어린이 보호 구역 정보.csv',
        'parking': 'data/대구 주차장 정보.csv',
        'accident': 'data/countrywide_accident.csv',
        'train': 'data/train.csv',
        'test': 'data/test.csv'
    }

    # 새 데이터셋 추가
    dataset_map = {
        # ... 기존 항목들 ...
        'test': 'data/test.csv',
        'mydata': 'data/my_new_data.csv'  # ← 추가!
    }
    ```

    ### Step 3: app.py에 탭 추가

    ```python
    # 탭 목록에 추가
    tabs = st.tabs([
        "🎥 CCTV",
        # ... 기존 탭들 ...
        "📝 테스트",
        "🆕 내 데이터",  # ← 추가!
        "🔄 교차 데이터 분석",
        "📖 프로젝트 개요"
    ])

    # 탭 렌더링 추가
    with tabs[7]:  # 인덱스 조정 필요
        render_dataset_tab('mydata', '내 데이터')
    ```

    ### Step 4: 테스트

    ```bash
    streamlit run app.py
    ```

    1. 새 탭이 보이는지 확인
    2. 데이터가 로드되는지 확인
    3. 차트와 지도가 정상 작동하는지 확인
    """)

    st.warning("""
    ⚠️ **주의사항:**
    - 탭 인덱스 번호 조정 필요 (새 탭 추가 시)
    - 위도/경도 컬럼 이름 확인 (자동 감지)
    - 한글 파일명은 UTF-8 인코딩 필요
    """)

    # 실제 예시
    st.markdown("---")
    st.subheader("💻 데이터 로딩 시뮬레이션")

    if st.button("새 데이터셋 로드 시뮬레이션"):
        with st.spinner("데이터 로딩 중..."):
            # 가상 데이터 생성
            new_df = pd.DataFrame({
                '이름': [f'지점{i}' for i in range(10)],
                '위도': np.random.uniform(35.8, 35.9, 10),
                '경도': np.random.uniform(128.5, 128.6, 10),
                '값': np.random.randint(10, 100, 10)
            })

        st.success("✅ 로딩 완료!")
        st.dataframe(new_df)

        # 지도 표시
        m = folium.Map(
            location=[new_df['위도'].mean(), new_df['경도'].mean()],
            zoom_start=12
        )

        for _, row in new_df.iterrows():
            folium.Marker(
                [row['위도'], row['경도']],
                popup=row['이름']
            ).add_to(m)

        st_folium(m, height=400)

# ============================================
# 탭 5: UI 개선
# ============================================
with tabs[4]:
    st.header("5. UI/UX 개선하기")

    st.markdown("""
    ## 🎨 UI 개선 아이디어

    ### 1. 로딩 상태 개선

    **현재:** 즉시 로딩, 피드백 부족

    **개선:**
    ```python
    # app.py의 데이터 로딩 부분
    with st.spinner(f"{dataset_display_name} 데이터를 불러오는 중..."):
        df = load_dataset(dataset_name)
    st.success(f"✅ {len(df):,}개 행 로드 완료!")
    ```

    ### 2. 에러 메시지 개선

    **현재:**
    ```python
    except Exception as e:
        st.error(f"❌ {dataset_display_name} 로딩 오류: {str(e)}")
    ```

    **개선:**
    ```python
    except FileNotFoundError:
        st.error(f"❌ 파일을 찾을 수 없습니다: {dataset_display_name}")
        st.info("📁 data/ 디렉토리를 확인해주세요.")
    except pd.errors.EmptyDataError:
        st.error("❌ 파일이 비어있습니다.")
    except Exception as e:
        st.error(f"❌ 예상치 못한 오류: {str(e)}")
        with st.expander("상세 오류 정보"):
            st.code(str(e))
    ```

    ### 3. 도움말 추가

    ```python
    st.help(st.selectbox)  # 위젯 도움말

    # 커스텀 도움말
    with st.expander("❓ 이 기능은 무엇인가요?"):
        st.markdown(\"\"\"
        이 기능은 ...
        사용 방법:
        1. ...
        2. ...
        \"\"\")
    ```

    ### 4. 프로그레스 바 추가

    ```python
    progress_bar = st.progress(0)
    for i in range(100):
        # 작업 수행
        progress_bar.progress(i + 1)
    progress_bar.empty()  # 완료 후 제거
    ```

    ### 5. 빈 상태 처리

    ```python
    if filtered_df.empty:
        st.warning("⚠️ 필터 조건에 맞는 데이터가 없습니다.")
        st.info("💡 필터를 조정해보세요.")
    else:
        # 데이터 표시
    ```
    """)

    # UI 개선 예시
    st.markdown("---")
    st.subheader("💻 개선 전/후 비교")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**개선 전**")
        st.code("데이터 로딩 중...")
        st.code("오류: File not found")

    with col2:
        st.write("**개선 후**")
        with st.spinner("데이터를 불러오는 중..."):
            pass
        st.error("❌ 파일을 찾을 수 없습니다")
        st.info("📁 data/ 디렉토리를 확인해주세요")

# ============================================
# 탭 6: 체크리스트
# ============================================
with tabs[5]:
    st.header("6. 개발 체크리스트")

    st.markdown("""
    ## ✅ 새 기능 추가 체크리스트

    ### 계획 단계
    - [ ] 추가할 기능 명확히 정의
    - [ ] 어느 탭/위치에 추가할지 결정
    - [ ] 필요한 데이터/라이브러리 확인
    - [ ] 기존 코드에 미치는 영향 파악

    ### 개발 단계
    - [ ] Git 브랜치 생성 (`git checkout -b feature/my-feature`)
    - [ ] 코드 수정
    - [ ] 로컬에서 테스트 (`streamlit run app.py`)
    - [ ] 에러 처리 추가
    - [ ] 사용자 피드백 추가 (spinner, success 등)

    ### 테스트 단계
    - [ ] 모든 탭이 정상 작동하는지 확인
    - [ ] 기존 기능이 깨지지 않았는지 확인
    - [ ] 다양한 데이터로 테스트
    - [ ] 에러 상황 테스트 (빈 데이터, 잘못된 입력 등)
    - [ ] 여러 브라우저에서 확인

    ### 배포 단계
    - [ ] 코드 정리 및 주석 추가
    - [ ] README.md 업데이트 (필요 시)
    - [ ] Git 커밋 및 푸시
    - [ ] Pull Request 생성 (팀 작업 시)

    ## 🐛 디버깅 가이드

    ### 1. 에러 발생 시

    ```python
    # 디버그 정보 출력
    st.write("DEBUG:", st.session_state)
    st.write("데이터 타입:", df.dtypes)
    st.write("컬럼:", df.columns.tolist())
    ```

    ### 2. 캐시 문제

    ```bash
    # 앱 실행 중 C 키 → Clear cache
    # 또는 코드에서:
    st.cache_data.clear()
    ```

    ### 3. 레이아웃 깨짐

    - `width="stretch"` 사용
    - `st.columns()` 비율 조정
    - 모바일 뷰 확인

    ### 4. 성능 문제

    - 데이터 샘플링 (대용량 시)
    - 불필요한 재계산 제거
    - `@st.cache_data` 활용

    ## 📝 코드 스타일 가이드

    현재 앱의 스타일을 따르세요:

    ```python
    # 1. 함수 독스트링
    def my_function(param: str) -> pd.DataFrame:
        \"\"\"
        함수 설명

        Parameters:
            param (str): 파라미터 설명

        Returns:
            pd.DataFrame: 반환값 설명
        \"\"\"
        pass

    # 2. 임포트 순서
    # 표준 라이브러리
    import os

    # 서드파티
    import streamlit as st
    import pandas as pd

    # 로컬 모듈
    from utils.loader import load_dataset

    # 3. 주석
    # 섹션 구분
    # ============================================
    # 데이터 로딩
    # ============================================
    ```
    """)

    st.success("""
    ✅ **개발 완료 기준:**
    - 모든 체크리스트 항목 완료
    - 에러 없이 실행
    - 기존 기능 정상 작동
    - 코드 리뷰 통과 (팀 작업 시)
    """)

# ============================================
# 마무리
# ============================================
st.markdown("---")
st.header("🎓 다음 단계")

st.markdown("""
## 실전 연습

1. **간단한 기능부터 시작**
   - 데이터 다운로드 버튼 추가
   - 추가 메트릭 표시
   - 도움말 텍스트 추가

2. **중급 기능**
   - 새 탭 추가
   - Session State로 즐겨찾기
   - 필터 기능 개선

3. **고급 기능**
   - 새 데이터셋 통합
   - 커스텀 분석 추가
   - 대시보드 레이아웃 재설계

## 추천 학습 순서

1. ✅ 이 예제 완전히 이해
2. ✅ `app.py` 전체 코드 읽기
3. ✅ 간단한 수정 시도 (버튼, 텍스트 등)
4. ✅ 새 탭 추가
5. ✅ 새 기능 구현

## 도움이 필요할 때

- 이 예제의 패턴 참고
- 예제 01-13 복습
- Streamlit 공식 문서
- app.py의 기존 코드 패턴 따라하기
""")

st.balloons()
