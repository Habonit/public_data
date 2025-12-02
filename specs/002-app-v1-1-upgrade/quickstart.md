# Quickstart Guide: 대구 공공데이터 시각화 앱 v1.1

**Feature Branch**: `002-app-v1-1-upgrade`
**Created**: 2025-12-01

## 1. 개발 환경 설정

### 1.1 사전 요구사항

- Python 3.10 이상
- pip 또는 conda

### 1.2 의존성 설치

```bash
# 저장소 클론 (이미 완료된 경우 스킵)
cd /home/paradeigma/workspace/public_data

# 가상환경 활성화 (권장)
source venv/bin/activate  # Linux/macOS
# 또는
.\venv\Scripts\activate  # Windows

# 의존성 설치
pip install -r requirements.txt

# v1.1 추가 의존성 (챗봇용)
pip install anthropic
```

### 1.3 requirements.txt 업데이트

v1.1에서 추가될 내용:
```
# 기존
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.17.0
folium>=0.14.0
streamlit-folium>=0.15.0
matplotlib>=3.8.0
openpyxl>=3.1.5

# 신규 (v1.1)
anthropic>=0.39.0
```

---

## 2. 앱 실행

### 2.1 기본 실행

```bash
streamlit run app.py
```

브라우저에서 `http://localhost:8501` 접속

### 2.2 포트 변경 실행

```bash
streamlit run app.py --server.port 8080
```

---

## 3. v1.1 주요 변경사항 개발 가이드

### 3.1 데이터 업로드 기능

**파일 위치**: `app.py`

```python
# 프로젝트 개요 탭에서 업로드 UI 추가
st.header("📤 데이터 업로드")

# 각 데이터셋별 업로더
for key, info in DATASET_MAPPING.items():
    uploaded_file = st.file_uploader(
        f"{info['display_name']} 데이터",
        type=['csv'],
        key=f"uploader_{key}"
    )

    if uploaded_file is not None:
        # session_state에 저장
        df = read_uploaded_csv(uploaded_file)
        st.session_state.datasets[key] = {
            'df': df,
            'name': uploaded_file.name,
            'size': uploaded_file.size,
            'uploaded_at': datetime.now()
        }
        st.session_state.upload_status[key] = True
        st.success(f"✅ {info['display_name']} 업로드 완료!")
```

### 3.2 챗봇 모듈 추가

**파일 위치**: `utils/chatbot.py` (신규 생성)

```python
"""
AI 챗봇 유틸리티.
"""
from anthropic import Anthropic

SYSTEM_PROMPT = """..."""  # contracts/chatbot-prompts.md 참조

def create_chat_response(
    api_key: str,
    model: str,
    messages: list[dict],
    data_context: str
) -> tuple[str, dict]:
    """
    Anthropic API를 사용하여 응답 생성.

    Parameters:
        api_key (str): Anthropic API Key
        model (str): 모델 ID
        messages (list[dict]): 대화 이력
        data_context (str): 데이터셋 컨텍스트

    Returns:
        tuple: (응답 텍스트, 토큰 사용량)
    """
    client = Anthropic(api_key=api_key)

    response = client.messages.create(
        model=model,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=messages
    )

    tokens = {
        'input': response.usage.input_tokens,
        'output': response.usage.output_tokens,
        'total': response.usage.input_tokens + response.usage.output_tokens
    }

    return response.content[0].text, tokens
```

### 3.3 시각화 다양화

**파일 위치**: `utils/visualizer.py`

```python
def plot_with_options(
    df: pd.DataFrame,
    column: str,
    chart_type: str
) -> go.Figure:
    """
    선택된 차트 유형으로 시각화.

    Parameters:
        df: 데이터셋
        column: 시각화할 컬럼
        chart_type: 'histogram' | 'boxplot' | 'kde' | 'scatter'
    """
    if chart_type == 'histogram':
        return px.histogram(df, x=column, marginal='box')
    elif chart_type == 'boxplot':
        return px.box(df, y=column)
    elif chart_type == 'kde':
        import plotly.figure_factory as ff
        data = df[column].dropna().tolist()
        return ff.create_distplot([data], [column], show_hist=False)
    elif chart_type == 'scatter':
        # 산점도는 x, y 컬럼 필요 - 별도 함수로 분리 권장
        pass
```

### 3.4 버그 수정

**deprecated API 수정**:
```python
# AS-IS
st.dataframe(df, width='stretch')

# TO-BE
st.dataframe(df, use_container_width=True)
```

**mutable default 수정**:
```python
# AS-IS (visualizer.py:96)
def create_folium_map(df, lat_col, lng_col, popup_cols=[]):
    ...

# TO-BE
def create_folium_map(df, lat_col, lng_col, popup_cols=None):
    if popup_cols is None:
        popup_cols = []
    ...
```

**ZeroDivisionError 수정**:
```python
# AS-IS (app.py:54)
missing_pct = sum(info['missing_ratios'].values()) / len(info['missing_ratios']) * 100

# TO-BE
if info['missing_ratios'] and len(info['missing_ratios']) > 0:
    missing_pct = sum(info['missing_ratios'].values()) / len(info['missing_ratios']) * 100
else:
    missing_pct = 0
```

---

## 4. 테스트 가이드

### 4.1 수동 테스트 체크리스트

#### P0: 버그 수정 확인

- [ ] 빈 DataFrame 업로드 시 에러 없이 안내 메시지 표시
- [ ] deprecated warning 없이 앱 실행
- [ ] 숫자형 컬럼 없는 데이터 업로드 시 적절한 안내

#### P1: 업로드 기능

- [ ] CSV 파일 드래그 앤 드롭으로 업로드 가능
- [ ] 업로드 후 파일명, 크기 표시
- [ ] 탭 전환 시 데이터 재로딩 없음
- [ ] 업로드 안 한 탭 접근 시 안내 메시지

#### P2: 시각화

- [ ] 히스토그램, 박스플롯, KDE, 산점도 모두 렌더링
- [ ] 결측치 30% 이상 컬럼에 경고 표시
- [ ] 차트 스타일 개선 확인

#### P3: 챗봇

- [ ] API Key 입력 후 질문 가능
- [ ] 데이터셋 선택 후 관련 질문에 답변
- [ ] 토큰 사용량 실시간 업데이트
- [ ] 잘못된 API Key 입력 시 오류 메시지

### 4.2 테스트 데이터

테스트용 CSV 파일 예시:

```csv
이름,나이,점수,도시
김철수,25,85.5,대구
이영희,30,92.0,서울
박민수,22,,부산
최지연,28,78.5,대구
```

---

## 5. 디버깅 팁

### 5.1 session_state 확인

```python
# 앱 어디서든 현재 상태 확인
st.write(st.session_state)
```

### 5.2 API 응답 확인

```python
# 챗봇 응답 디버깅
try:
    response, tokens = create_chat_response(...)
    st.write(f"Tokens used: {tokens}")
except Exception as e:
    st.error(f"API Error: {e}")
```

### 5.3 데이터 로딩 확인

```python
# 업로드된 데이터 확인
if 'datasets' in st.session_state:
    for key, data in st.session_state.datasets.items():
        st.write(f"{key}: {data['name']} ({data['size']} bytes)")
```

---

## 6. 참고 문서

- [spec.md](./spec.md) - 기능 명세
- [research.md](./research.md) - 기술 리서치
- [data-model.md](./data-model.md) - 데이터 모델
- [contracts/chatbot-prompts.md](./contracts/chatbot-prompts.md) - 챗봇 프롬프트
- [constitution.md](../../.specify/memory/constitution.md) - 프로젝트 원칙
