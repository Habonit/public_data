# Research: 대구 공공데이터 시각화 앱 v1.1 업그레이드

**Feature Branch**: `002-app-v1-1-upgrade`
**Created**: 2025-12-01
**Status**: Complete

## 1. Streamlit 파일 업로드 패턴

### Decision: `st.file_uploader` 사용

**Rationale**:
- Streamlit 내장 위젯으로 추가 의존성 불필요
- 드래그 앤 드롭, 파일 선택 UI 자동 제공
- 세션 상태와 자연스럽게 통합

**Alternatives Considered**:
- 직접 구현한 HTML/JS 업로더: 복잡성 증가, Streamlit 철학에 어긋남
- 외부 파일 서버: 로컬 실행 원칙 위반

**Best Practices**:
```python
# 업로드된 파일을 session_state에 저장하여 재로딩 방지
uploaded_file = st.file_uploader("CSV 파일 업로드", type=['csv'])
if uploaded_file is not None:
    if 'datasets' not in st.session_state:
        st.session_state.datasets = {}

    # 파일명 기반 캐싱
    file_key = uploaded_file.name
    if file_key not in st.session_state.datasets:
        df = pd.read_csv(uploaded_file)
        st.session_state.datasets[file_key] = {
            'df': df,
            'name': uploaded_file.name,
            'size': uploaded_file.size
        }
```

---

## 2. Session State 관리 패턴

### Decision: 계층적 session_state 구조 사용

**Rationale**:
- 각 데이터셋, 챗봇 세션, UI 상태를 명확히 분리
- 상호작용 시 불필요한 재계산 방지
- Streamlit의 리렌더링 특성에 대응

**Structure**:
```python
st.session_state = {
    'datasets': {
        'cctv': {'df': DataFrame, 'name': str, 'size': int, 'uploaded_at': datetime},
        'lights': {...},
        ...
    },
    'chatbot': {
        'api_key': str,
        'model': str,
        'messages': list,
        'tokens': {'total': int, 'input': int, 'output': int}
    },
    'ui': {
        'selected_dataset': str,
        'selected_tab': int
    }
}
```

**Alternatives Considered**:
- 전역 변수: Streamlit 리렌더링 시 초기화됨
- 파일 기반 캐싱: 불필요한 I/O 오버헤드

---

## 3. Anthropic API 통합

### Decision: anthropic 공식 Python SDK 사용

**Rationale**:
- 공식 지원 SDK로 안정성 보장
- 스트리밍 응답 지원
- 토큰 사용량 응답에 포함

**Best Practices**:
```python
from anthropic import Anthropic

def create_chat_response(
    api_key: str,
    model: str,
    messages: list[dict],
    system_prompt: str
) -> tuple[str, dict]:
    """
    Anthropic API를 사용하여 챗봇 응답 생성.

    Returns:
        tuple: (응답 텍스트, 토큰 사용량 dict)
    """
    client = Anthropic(api_key=api_key)

    response = client.messages.create(
        model=model,
        max_tokens=1024,
        system=system_prompt,
        messages=messages
    )

    tokens = {
        'input': response.usage.input_tokens,
        'output': response.usage.output_tokens,
        'total': response.usage.input_tokens + response.usage.output_tokens
    }

    return response.content[0].text, tokens
```

**Model Options**:
- `claude-sonnet-4-20250514`: 빠른 응답, 비용 효율적 (기본 권장)
- `claude-opus-4-20250514`: 복잡한 분석에 적합
- `claude-3-5-haiku-20241022`: 간단한 질문에 최적

**Error Handling**:
- API Key 검증 실패 → "API Key를 확인해주세요" 메시지
- Rate limit → 재시도 옵션 제공
- Network timeout → 10초 후 타임아웃, 재시도 버튼

---

## 4. 다양한 시각화 차트

### Decision: Plotly Express 기반 확장

**Rationale**:
- 기존 코드가 Plotly Express 사용
- 일관된 스타일과 인터랙티브 기능
- 추가 의존성 없음

**Chart Types**:

| 차트 유형 | 함수 | 사용 사례 |
|----------|------|----------|
| 히스토그램 | `px.histogram` | 숫자형 분포 (기존) |
| 박스플롯 | `px.box` | 이상치, 사분위수 |
| KDE (커널 밀도) | `ff.create_distplot` | 부드러운 분포 추정 |
| 산점도 | `px.scatter` | 두 변수 관계 |

**Implementation**:
```python
def plot_visualization(
    df: pd.DataFrame,
    column: str,
    chart_type: str,
    x_col: str | None = None,
    y_col: str | None = None
) -> go.Figure:
    """
    선택된 차트 유형에 따른 시각화 생성.
    """
    if chart_type == 'histogram':
        return px.histogram(df, x=column, marginal='box')
    elif chart_type == 'boxplot':
        return px.box(df, y=column)
    elif chart_type == 'kde':
        # plotly figure_factory 사용
        import plotly.figure_factory as ff
        data = df[column].dropna().tolist()
        return ff.create_distplot([data], [column], show_hist=False)
    elif chart_type == 'scatter':
        if x_col and y_col:
            return px.scatter(df, x=x_col, y=y_col)
    return None
```

---

## 5. CSV 인코딩 처리

### Decision: 순차적 인코딩 시도 (UTF-8 → UTF-8-SIG → CP949)

**Rationale**:
- 기존 `read_csv_safe` 함수 재사용
- 한글 CSV 파일의 일반적인 인코딩 커버
- 추가 의존성(chardet 등) 불필요

**Enhancement**:
```python
def read_uploaded_csv(uploaded_file) -> pd.DataFrame:
    """
    업로드된 CSV 파일을 인코딩 자동 감지하여 읽기.
    """
    encodings = ['utf-8', 'utf-8-sig', 'cp949', 'euc-kr']
    content = uploaded_file.getvalue()

    for enc in encodings:
        try:
            return pd.read_csv(io.BytesIO(content), encoding=enc)
        except UnicodeDecodeError:
            continue

    raise ValueError(
        f"지원되지 않는 인코딩입니다. "
        f"UTF-8, UTF-8-SIG, CP949, EUC-KR 중 하나로 저장해주세요."
    )
```

---

## 6. 탭 활성화/비활성화 패턴

### Decision: 조건부 탭 콘텐츠 렌더링

**Rationale**:
- Streamlit은 탭 자체의 비활성화를 지원하지 않음
- 탭 콘텐츠 내에서 조건부 메시지 표시로 대체
- 사용자에게 명확한 피드백 제공

**Implementation**:
```python
# 프로젝트 개요 탭에서 업로드 상태 추적
if 'upload_status' not in st.session_state:
    st.session_state.upload_status = {
        'cctv': False,
        'lights': False,
        'zones': False,
        'parking': False,
        'accident': False,
        'train': False,
        'test': False
    }

# 각 데이터셋 탭에서
def render_dataset_tab(dataset_key: str, display_name: str):
    if not st.session_state.upload_status.get(dataset_key, False):
        st.warning(f"⚠️ {display_name} 데이터를 먼저 업로드해주세요.")
        st.info("📤 '프로젝트 개요' 탭에서 데이터를 업로드할 수 있습니다.")
        return

    # 데이터 시각화 로직
    df = st.session_state.datasets[dataset_key]['df']
    ...
```

---

## 7. 결측치 경고 알림

### Decision: 30% 기준 st.warning 표시

**Rationale**:
- spec에서 정의된 30% 기준 준수
- 시각화 컬럼 선택 시점에 경고 표시
- 사용자의 데이터 품질 인식 향상

**Implementation**:
```python
def check_missing_ratio(df: pd.DataFrame, column: str, threshold: float = 0.3) -> bool:
    """
    결측치 비율이 임계값을 초과하는지 확인.
    """
    missing_ratio = df[column].isnull().sum() / len(df)
    return missing_ratio >= threshold

# 시각화 선택 시
if check_missing_ratio(df, selected_column):
    st.warning(
        f"⚠️ **{selected_column}** 컬럼의 결측치가 30% 이상입니다. "
        f"시각화 결과가 왜곡될 수 있습니다."
    )
```

---

## 8. Deprecated API 대체

### Decision: use_container_width=True로 통일

**Rationale**:
- Streamlit 공식 권장 API
- 반응형 레이아웃에 적합
- 향후 호환성 보장

**Changes**:
```python
# AS-IS
st.dataframe(df, width='stretch')
st.plotly_chart(fig, width='stretch')

# TO-BE
st.dataframe(df, use_container_width=True)
st.plotly_chart(fig, use_container_width=True)
```

---

## 9. Mutable Default Argument 수정

### Decision: None 기본값 + 함수 내 초기화

**Rationale**:
- Python 모범 사례 준수
- 예상치 못한 상태 공유 방지
- pylint/flake8 경고 제거

**Pattern**:
```python
# AS-IS
def func(items: list = []):
    items.append(1)
    return items

# TO-BE
def func(items: list | None = None):
    if items is None:
        items = []
    items.append(1)
    return items
```

---

## 10. 사이드바 구성

### Decision: 계층적 사이드바 레이아웃

**Structure**:
```
사이드바
├── 🔑 API 설정
│   ├── API Key 입력 (password)
│   └── 모델 선택 (selectbox)
├── 📊 토큰 사용량
│   ├── 전체 토큰
│   ├── 입력 토큰
│   └── 출력 토큰
└── 📤 데이터 업로드 현황
    ├── CCTV: ✅/❌
    ├── 보안등: ✅/❌
    └── ...
```

**Implementation**:
```python
with st.sidebar:
    st.header("🔑 API 설정")
    api_key = st.text_input(
        "Anthropic API Key",
        type="password",
        key="api_key"
    )
    model = st.selectbox(
        "AI 모델",
        options=['claude-sonnet-4-20250514', 'claude-opus-4-20250514', 'claude-3-5-haiku-20241022'],
        index=0
    )

    st.divider()

    st.header("📊 토큰 사용량")
    tokens = st.session_state.get('chatbot', {}).get('tokens', {})
    col1, col2, col3 = st.columns(3)
    col1.metric("전체", tokens.get('total', 0))
    col2.metric("입력", tokens.get('input', 0))
    col3.metric("출력", tokens.get('output', 0))

    st.divider()

    st.header("📤 업로드 현황")
    for key, name in DATASET_NAMES.items():
        status = "✅" if st.session_state.upload_status.get(key) else "❌"
        st.write(f"{status} {name}")
```

---

## Summary

| 영역 | 결정 | 근거 |
|------|------|------|
| 파일 업로드 | st.file_uploader + session_state | Streamlit 네이티브, 재로딩 방지 |
| 상태 관리 | 계층적 session_state | 명확한 구조, 확장성 |
| AI 챗봇 | anthropic SDK | 공식 지원, 토큰 추적 |
| 시각화 | Plotly Express 확장 | 일관성, 무추가 의존성 |
| 인코딩 | 순차 시도 (UTF-8→CP949) | 기존 로직 재사용 |
| 탭 제어 | 조건부 콘텐츠 렌더링 | Streamlit 제약 대응 |
| 결측치 | 30% 기준 경고 | spec 정의 준수 |
| API 마이그레이션 | use_container_width | 공식 권장 |
| Mutable default | None + 내부 초기화 | Python 모범 사례 |
| 사이드바 | 계층적 레이아웃 | 정보 구조화 |
