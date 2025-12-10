# 예제 1: Streamlit 기본 설정 및 텍스트 표시

## 학습 목표

이 예제를 통해 다음을 학습합니다:
- Streamlit 앱의 페이지 설정 방법
- 다양한 텍스트 표시 방법 (title, header, subheader, markdown 등)
- st.write()의 활용법
- 마크다운 문법 사용법

## 핵심 개념

### 1. `st.set_page_config()`

모든 Streamlit 앱은 페이지 설정으로 시작합니다. **이 함수는 반드시 스크립트의 가장 첫 번째 Streamlit 명령어여야 합니다!**

```python
st.set_page_config(
    page_title="제목",        # 브라우저 탭 제목
    page_icon="🎯",           # 브라우저 탭 아이콘
    layout="wide",            # "wide" 또는 "centered"
    initial_sidebar_state="expanded"  # 사이드바 초기 상태
)
```

**주요 매개변수:**
- `page_title`: 브라우저 탭에 표시될 제목
- `page_icon`: 브라우저 탭의 favicon (이모지 또는 이미지 URL)
- `layout`: 페이지 레이아웃 방식
  - `"wide"`: 전체 화면 너비 사용
  - `"centered"`: 중앙 정렬된 좁은 레이아웃
- `initial_sidebar_state`: 사이드바 초기 상태
  - `"expanded"`: 펼쳐진 상태
  - `"collapsed"`: 접힌 상태

### 2. 텍스트 표시 계층 구조

Streamlit은 다양한 크기의 텍스트 표시를 지원합니다:

```python
st.title("가장 큰 제목")          # H1
st.header("헤더")                 # H2
st.subheader("서브헤더")          # H3
st.markdown("### 마크다운 헤더")  # H3
```

**사용 가이드:**
- `st.title()`: 페이지의 메인 제목 (한 페이지에 하나)
- `st.header()`: 주요 섹션 제목
- `st.subheader()`: 하위 섹션 제목
- `st.markdown()`: 커스텀 포맷팅이 필요할 때

### 3. `st.markdown()` - 풍부한 텍스트 표현

마크다운을 사용하면 다양한 형식의 텍스트를 작성할 수 있습니다:

```python
st.markdown("""
# 제목
## 부제목

**굵은 글씨**, *기울임*, ~~취소선~~

- 리스트 항목 1
- 리스트 항목 2

1. 번호 리스트
2. 두 번째

[링크](https://streamlit.io)

\`\`\`python
# 코드 블록
print("Hello")
\`\`\`
""")
```

**고급 사용:**
```python
# HTML 허용 (주의해서 사용!)
st.markdown("<span style='color:red'>빨간 텍스트</span>", unsafe_allow_html=True)
```

### 4. `st.write()` - 만능 표시 함수

`st.write()`는 인자의 타입에 따라 자동으로 적절한 방식으로 표시합니다:

```python
st.write("텍스트")                    # 텍스트로 표시
st.write(123)                        # 숫자로 표시
st.write({"key": "value"})           # JSON으로 표시
st.write(dataframe)                  # 표로 표시
st.write(matplotlib_figure)          # 차트로 표시
```

**장점:**
- 간단하고 직관적
- 다양한 데이터 타입 자동 처리
- 여러 인자를 동시에 받을 수 있음

**단점:**
- 세밀한 제어가 어려움
- 특수한 경우 전용 함수가 더 나을 수 있음

### 5. 기타 텍스트 함수들

```python
st.text("고정폭 폰트 텍스트")          # 코드나 로그에 적합
st.caption("작은 회색 텍스트")        # 설명이나 주석
st.code("code", language="python")  # 코드 블록 (문법 강조)
st.latex(r"수식")                    # 수학 수식 (LaTeX)
```

## 실행 방법

```bash
cd streamlit_study
streamlit run 01_basic_setup.py
```

브라우저에서 자동으로 `http://localhost:8501` 열립니다.

## 실습 과제

1. **페이지 설정 변경하기**
   - `page_icon`을 다른 이모지로 변경
   - `layout`을 "centered"로 변경하고 차이 확인

2. **마크다운 연습하기**
   - 표(table) 문법 추가해보기
   - 중첩 리스트 만들어보기

3. **st.write() 실험하기**
   - 딕셔너리의 딕셔너리 출력해보기
   - 여러 인자를 한 번에 전달해보기

## 현재 앱(`app.py`)에서의 사용 예시

메인 앱에서는 다음과 같이 사용됩니다:

```python
# app.py:15-20
st.set_page_config(
    page_title="대구 공공데이터 시각화",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# app.py:140
st.title("📊 대구 공공데이터 시각화")

# app.py:141-144
st.markdown("""
대구 공공데이터 시각화 도구에 오신 것을 환영합니다! ...
""")
```

## 주요 포인트

1. ✅ `st.set_page_config()`는 반드시 가장 먼저 호출
2. ✅ 텍스트 계층 구조를 명확히 (title > header > subheader)
3. ✅ 긴 텍스트는 마크다운 사용
4. ✅ 간단한 출력은 st.write() 활용
5. ⚠️ HTML 사용 시 `unsafe_allow_html=True` 필요 (보안 주의)

## 다음 단계

다음 예제에서는 **레이아웃과 컬럼**을 사용하여 페이지를 구조화하는 방법을 배웁니다.

## 참고 자료

- [Streamlit API Reference - Text elements](https://docs.streamlit.io/library/api-reference/text)
- [Markdown Cheat Sheet](https://www.markdownguide.org/cheat-sheet/)
