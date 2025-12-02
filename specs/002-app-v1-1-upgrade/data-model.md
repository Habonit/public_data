# Data Model: 대구 공공데이터 시각화 앱 v1.1

**Feature Branch**: `002-app-v1-1-upgrade`
**Created**: 2025-12-01
**Status**: Complete

## 1. 개요

v1.1에서 관리되는 주요 데이터 엔티티와 그 관계를 정의한다. 모든 상태는 `st.session_state`에 저장된다.

---

## 2. 엔티티 정의

### 2.1 UploadedDataset (업로드된 데이터셋)

사용자가 업로드한 CSV 파일을 나타내는 엔티티.

```python
@dataclass
class UploadedDataset:
    """업로드된 데이터셋 정보."""

    df: pd.DataFrame          # 로드된 DataFrame
    name: str                 # 원본 파일명 (예: "대구 CCTV 정보.csv")
    size: int                 # 파일 크기 (bytes)
    uploaded_at: datetime     # 업로드 시간
    row_count: int            # 행 수
    column_count: int         # 컬럼 수
```

**Validation Rules**:
- `df`는 빈 DataFrame이 아니어야 함
- `name`은 `.csv` 확장자를 가져야 함
- `size`는 50MB (52,428,800 bytes) 이하여야 함

**State Transitions**:
```
[없음] ---(업로드)---> [로드됨] ---(삭제)---> [없음]
```

---

### 2.2 ChatSession (챗봇 세션)

AI 챗봇과의 대화 세션을 나타내는 엔티티.

```python
@dataclass
class ChatSession:
    """챗봇 세션 정보."""

    api_key: str              # Anthropic API Key (마스킹됨)
    model: str                # 선택된 모델 (claude-sonnet-4-20250514 등)
    selected_dataset: str     # 질의 대상 데이터셋 키 (예: 'cctv')
    messages: list[dict]      # 대화 이력 [{'role': 'user'|'assistant', 'content': str}]
    tokens: TokenUsage        # 토큰 사용량
```

**TokenUsage 서브 엔티티**:
```python
@dataclass
class TokenUsage:
    """토큰 사용량 추적."""

    total: int = 0            # 전체 토큰
    input: int = 0            # 입력 토큰
    output: int = 0           # 출력 토큰
```

**Validation Rules**:
- `api_key`는 `sk-ant-` 접두사로 시작해야 함 (Anthropic 형식)
- `model`은 허용된 모델 목록에 있어야 함
- `selected_dataset`은 업로드된 데이터셋 중 하나여야 함

**State Transitions**:
```
[초기화] ---(API Key 입력)---> [준비됨] ---(질문)---> [대화중]
    ^                                                    |
    |-----------------(세션 초기화)----------------------|
```

---

### 2.3 VisualizationConfig (시각화 설정)

시각화 관련 설정을 나타내는 엔티티.

```python
@dataclass
class VisualizationConfig:
    """시각화 설정."""

    chart_type: str           # 차트 유형 ('histogram'|'boxplot'|'kde'|'scatter')
    selected_column: str      # 선택된 컬럼
    x_column: str | None      # X축 컬럼 (산점도용)
    y_column: str | None      # Y축 컬럼 (산점도용)
    color_theme: str          # 색상 테마 ('plotly'|'seaborn' 등)
```

**Validation Rules**:
- `chart_type`은 허용된 차트 유형 중 하나여야 함
- `selected_column`은 해당 DataFrame에 존재해야 함
- 산점도의 경우 `x_column`과 `y_column`이 모두 필요

---

### 2.4 SidebarState (사이드바 상태)

사이드바의 전체 상태를 나타내는 엔티티.

```python
@dataclass
class SidebarState:
    """사이드바 상태."""

    api_key: str              # API Key (입력값)
    model: str                # 선택된 모델
    tokens: TokenUsage        # 토큰 사용량
    upload_status: dict[str, bool]  # 데이터셋별 업로드 상태
```

**upload_status 구조**:
```python
{
    'cctv': True,      # 업로드됨
    'lights': False,   # 미업로드
    'zones': False,
    'parking': True,
    'accident': False,
    'train': False,
    'test': False
}
```

---

## 3. Session State 구조

전체 `st.session_state` 구조:

```python
st.session_state = {
    # 업로드된 데이터셋
    'datasets': {
        'cctv': UploadedDataset,
        'lights': UploadedDataset,
        'zones': UploadedDataset,
        'parking': UploadedDataset,
        'accident': UploadedDataset,
        'train': UploadedDataset,
        'test': UploadedDataset
    },

    # 업로드 상태 (빠른 조회용)
    'upload_status': {
        'cctv': bool,
        'lights': bool,
        'zones': bool,
        'parking': bool,
        'accident': bool,
        'train': bool,
        'test': bool
    },

    # 챗봇 세션
    'chatbot': {
        'api_key': str,
        'model': str,
        'selected_dataset': str,
        'messages': list[dict],
        'tokens': {
            'total': int,
            'input': int,
            'output': int
        }
    },

    # 시각화 설정 (탭별)
    'viz_config': {
        'cctv': VisualizationConfig,
        'lights': VisualizationConfig,
        ...
    }
}
```

---

## 4. 데이터셋 매핑

### 4.1 데이터셋 키와 표시명

```python
DATASET_MAPPING = {
    'cctv': {
        'display_name': 'CCTV',
        'tab_icon': '🎥',
        'expected_file': '대구 CCTV 정보.csv',
        'color': 'red'
    },
    'lights': {
        'display_name': '보안등',
        'tab_icon': '💡',
        'expected_file': '대구 보안등 정보.csv',
        'color': 'blue'
    },
    'zones': {
        'display_name': '어린이 보호구역',
        'tab_icon': '🏫',
        'expected_file': '대구 어린이 보호 구역 정보.csv',
        'color': 'green'
    },
    'parking': {
        'display_name': '주차장',
        'tab_icon': '🅿️',
        'expected_file': '대구 주차장 정보.csv',
        'color': 'purple'
    },
    'accident': {
        'display_name': '사고',
        'tab_icon': '🚗',
        'expected_file': 'countrywide_accident.csv',
        'color': 'orange'
    },
    'train': {
        'display_name': '훈련 데이터',
        'tab_icon': '📊',
        'expected_file': 'train.csv',
        'color': 'darkred'
    },
    'test': {
        'display_name': '테스트 데이터',
        'tab_icon': '📋',
        'expected_file': 'test.csv',
        'color': 'darkblue'
    }
}
```

### 4.2 AI 모델 옵션

```python
AI_MODEL_OPTIONS = [
    {
        'id': 'claude-sonnet-4-20250514',
        'name': 'Claude Sonnet 4',
        'description': '빠른 응답, 비용 효율적 (권장)'
    },
    {
        'id': 'claude-opus-4-20250514',
        'name': 'Claude Opus 4',
        'description': '복잡한 분석에 적합'
    },
    {
        'id': 'claude-3-5-haiku-20241022',
        'name': 'Claude 3.5 Haiku',
        'description': '간단한 질문에 최적'
    }
]
```

---

## 5. 엔티티 관계도

```
┌─────────────────────────────────────────────────────────────┐
│                     st.session_state                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────┐       ┌─────────────────┐              │
│  │   SidebarState  │       │   ChatSession   │              │
│  ├─────────────────┤       ├─────────────────┤              │
│  │ api_key         │──────▶│ api_key         │              │
│  │ model           │──────▶│ model           │              │
│  │ tokens ─────────│──────▶│ tokens          │              │
│  │ upload_status   │       │ selected_dataset│───┐          │
│  └─────────────────┘       │ messages        │   │          │
│         │                  └─────────────────┘   │          │
│         │                                        │          │
│         ▼                                        ▼          │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                    datasets                          │    │
│  ├─────────────────────────────────────────────────────┤    │
│  │  'cctv'    │  'lights'  │  'zones'  │  ...          │    │
│  │     │           │            │                       │    │
│  │     ▼           ▼            ▼                       │    │
│  │ ┌──────────┐ ┌──────────┐ ┌──────────┐              │    │
│  │ │Uploaded  │ │Uploaded  │ │Uploaded  │              │    │
│  │ │Dataset   │ │Dataset   │ │Dataset   │              │    │
│  │ └──────────┘ └──────────┘ └──────────┘              │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                   viz_config (탭별)                   │    │
│  ├─────────────────────────────────────────────────────┤    │
│  │  'cctv' → VisualizationConfig                       │    │
│  │  'lights' → VisualizationConfig                     │    │
│  │  ...                                                 │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. 초기화 함수

```python
def init_session_state():
    """
    session_state 초기화.
    앱 시작 시 한 번 호출.
    """
    if 'initialized' in st.session_state:
        return

    # 데이터셋 저장소
    if 'datasets' not in st.session_state:
        st.session_state.datasets = {}

    # 업로드 상태
    if 'upload_status' not in st.session_state:
        st.session_state.upload_status = {
            key: False for key in DATASET_MAPPING.keys()
        }

    # 챗봇 세션
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = {
            'api_key': '',
            'model': 'claude-sonnet-4-20250514',
            'selected_dataset': None,
            'messages': [],
            'tokens': {'total': 0, 'input': 0, 'output': 0}
        }

    # 시각화 설정
    if 'viz_config' not in st.session_state:
        st.session_state.viz_config = {}

    st.session_state.initialized = True
```

---

## 7. 요약

| 엔티티 | 용도 | 저장 위치 |
|--------|------|----------|
| UploadedDataset | 업로드된 CSV 데이터 | `st.session_state.datasets[key]` |
| ChatSession | AI 챗봇 대화 | `st.session_state.chatbot` |
| VisualizationConfig | 시각화 설정 | `st.session_state.viz_config[key]` |
| SidebarState | 사이드바 전체 상태 | 분산 저장 (api_key, model, tokens, upload_status) |
