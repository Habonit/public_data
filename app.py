"""
Daegu Public Data Visualization - Streamlit Application

An educational tool for exploring and analyzing public datasets from Daegu.
Provides individual dataset exploration, cross-dataset spatial analysis, and
educational content to help data analysis learners discover insights independently.
"""
import io
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_folium import st_folium
from utils.loader import load_dataset, load_dataset_from_session, get_dataset_info, read_csv_safe, read_uploaded_csv
from utils.geo import detect_lat_lng_columns
from utils.visualizer import (
    plot_numeric_distribution,
    plot_categorical_distribution,
    plot_boxplot,
    plot_kde,
    plot_scatter,
    plot_with_options,
    check_missing_ratio,
    create_folium_map,
    create_overlay_map
)
from utils.chatbot import (
    SYSTEM_PROMPT,
    create_data_context,
    create_chat_response,
    handle_chat_error,
    validate_api_key
)
from anthropic import Anthropic

# 데이터셋 매핑 상수
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

# AI 모델 옵션
AI_MODEL_OPTIONS = [
    {'id': 'claude-sonnet-4-20250514', 'name': 'Claude Sonnet 4', 'description': '빠른 응답, 비용 효율적 (권장)'},
    {'id': 'claude-opus-4-20250514', 'name': 'Claude Opus 4', 'description': '복잡한 분석에 적합'},
    {'id': 'claude-3-5-haiku-20241022', 'name': 'Claude 3.5 Haiku', 'description': '간단한 질문에 최적'}
]


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

    st.session_state.initialized = True

# Page configuration
st.set_page_config(
    page_title="대구 공공데이터 시각화",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


def render_dataset_tab(dataset_name: str, dataset_display_name: str):
    """
    Render a complete tab for exploring an individual dataset.

    Parameters:
        dataset_name (str): Internal dataset name for load_dataset()
        dataset_display_name (str): Display name for UI
    """
    st.header(f"{dataset_display_name} 데이터셋")

    # Check if dataset is uploaded (T020, T021)
    if not st.session_state.upload_status.get(dataset_name, False):
        st.info(f"📤 **{dataset_display_name}** 데이터를 먼저 업로드해주세요.")
        st.markdown("**프로젝트 개요** 탭에서 CSV 파일을 업로드할 수 있습니다.")
        return

    # Load dataset from session_state (T022)
    df = load_dataset_from_session(dataset_name)
    if df is None:
        st.warning(f"⚠️ {dataset_display_name} 데이터를 불러올 수 없습니다. 다시 업로드해주세요.")
        return

    # Get dataset info
    info = get_dataset_info(df)

    # Display basic statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("전체 행 수", f"{info['row_count']:,}")
    with col2:
        st.metric("전체 컬럼 수", info['column_count'])
    with col3:
        missing_pct = sum(info['missing_ratios'].values()) / len(info['missing_ratios']) * 100 if info['missing_ratios'] else 0
        st.metric("평균 결측값 %", f"{missing_pct:.1f}%")

    # Data Preview
    with st.expander("📋 데이터 미리보기 (처음 10개 행)", expanded=False):
        st.dataframe(df.head(10), use_container_width=True)

    # Column Information
    with st.expander("📊 컬럼 정보", expanded=False):
        col_info_df = []
        for col in df.columns:
            col_info_df.append({
                '컬럼': col,
                '타입': info['dtypes'][col],
                '결측값 %': f"{info['missing_ratios'][col] * 100:.1f}%"
            })
        st.dataframe(col_info_df, use_container_width=True)

    # Descriptive Statistics for Numeric Columns
    if not info['numeric_summary'].empty:
        with st.expander("📈 숫자 컬럼 통계", expanded=False):
            st.dataframe(info['numeric_summary'], use_container_width=True)

    # Visualizations
    st.subheader("시각화")

    # Detect coordinates
    lat_col, lng_col = detect_lat_lng_columns(df)

    # Map Visualization
    if lat_col and lng_col:
        st.markdown("### 🗺️ 지리적 분포")
        st.info(f"감지된 좌표: **{lat_col}** (위도), **{lng_col}** (경도)")

        # Get columns for popup (exclude coordinate columns, limit to first 3 non-numeric)
        popup_candidates = [col for col in df.columns if col not in [lat_col, lng_col]]
        popup_cols = popup_candidates[:3]  # Show first 3 columns in popup

        # Create map
        map_obj = create_folium_map(
            df, lat_col, lng_col,
            popup_cols=popup_cols,
            color='blue',
            name=dataset_display_name
        )

        # Display map
        st_folium(map_obj, width=700, height=500)
    else:
        st.info("ℹ️ 지리 좌표가 감지되지 않았습니다. 이 데이터셋에는 지도 시각화를 사용할 수 없습니다.")

    # Numeric Distributions (T029-T033: 차트 유형 선택, 결측치 경고)
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    if numeric_cols:
        st.markdown("### 📊 숫자 컬럼 분포")

        # T029: Chart type selection
        chart_type = st.selectbox(
            "차트 유형 선택:",
            options=['히스토그램', '박스플롯', 'KDE', '산점도'],
            key=f"{dataset_name}_chart_type"
        )

        chart_type_map = {
            '히스토그램': 'histogram',
            '박스플롯': 'boxplot',
            'KDE': 'kde',
            '산점도': 'scatter'
        }

        # T030: For scatter plot, show X/Y column selection
        if chart_type == '산점도':
            col1, col2 = st.columns(2)
            with col1:
                x_col = st.selectbox(
                    "X축 컬럼:",
                    options=numeric_cols,
                    key=f"{dataset_name}_scatter_x"
                )
            with col2:
                y_col = st.selectbox(
                    "Y축 컬럼:",
                    options=[c for c in numeric_cols if c != x_col] if len(numeric_cols) > 1 else numeric_cols,
                    key=f"{dataset_name}_scatter_y"
                )

            # T033: Missing value warning for scatter
            x_warning, x_ratio = check_missing_ratio(df, x_col)
            y_warning, y_ratio = check_missing_ratio(df, y_col)
            if x_warning:
                st.warning(f"⚠️ {x_col} 컬럼의 결측값이 {x_ratio*100:.1f}%입니다. 결과가 왜곡될 수 있습니다.")
            if y_warning:
                st.warning(f"⚠️ {y_col} 컬럼의 결측값이 {y_ratio*100:.1f}%입니다. 결과가 왜곡될 수 있습니다.")

            # T031: Render scatter plot
            fig = plot_scatter(df, x_col, y_col)
            st.plotly_chart(fig, use_container_width=True)
        else:
            # Single column selection for other chart types
            selected_numeric_col = st.selectbox(
                "시각화할 숫자 컬럼 선택:",
                options=numeric_cols,
                key=f"{dataset_name}_numeric_select"
            )

            if selected_numeric_col:
                # T033: Missing value warning
                is_high_missing, missing_ratio = check_missing_ratio(df, selected_numeric_col)
                if is_high_missing:
                    st.warning(f"⚠️ {selected_numeric_col} 컬럼의 결측값이 {missing_ratio*100:.1f}%입니다. 결과가 왜곡될 수 있습니다.")

                # T031: Render selected chart type
                fig = plot_with_options(df, selected_numeric_col, chart_type_map[chart_type])
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("ℹ️ 이 데이터셋에는 숫자형 컬럼이 없습니다.")

    # Categorical Distributions
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    if categorical_cols:
        st.markdown("### 📊 범주형 컬럼 분포")

        # Let user select which categorical column to visualize
        selected_cat_col = st.selectbox(
            "시각화할 범주형 컬럼 선택:",
            options=categorical_cols,
            key=f"{dataset_name}_cat_select"
        )

        if selected_cat_col:
            fig = plot_categorical_distribution(df, selected_cat_col)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("ℹ️ 이 데이터셋에는 범주형 컬럼이 없습니다.")


def render_overview_tab():
    """
    Render the project overview tab with upload functionality. (T016-T019)
    """
    st.header("📖 프로젝트 개요")

    # Project Introduction
    st.markdown("""
    ## 대구 공공데이터 시각화 프로젝트

    이 프로젝트는 대구시의 다양한 공공 데이터를 탐색하고 분석할 수 있는 대화형 웹 애플리케이션입니다.
    데이터 분석을 학습하는 사용자들이 실제 공공 데이터를 통해 인사이트를 발견하고
    데이터 시각화 기술을 익힐 수 있도록 설계되었습니다.
    """)

    # Data Upload Section (T017-T019)
    st.subheader("📤 데이터 업로드")
    st.markdown("각 데이터셋에 해당하는 CSV 파일을 업로드하세요.")

    # Display upload status
    uploaded_count = sum(st.session_state.upload_status.values())
    st.info(f"업로드 현황: {uploaded_count} / {len(DATASET_MAPPING)} 데이터셋")

    # Create upload widgets for each dataset
    for dataset_key, dataset_info in DATASET_MAPPING.items():
        with st.expander(
            f"{dataset_info['tab_icon']} {dataset_info['display_name']} "
            f"({'✅ 업로드됨' if st.session_state.upload_status.get(dataset_key) else '⏳ 대기중'})"
        ):
            st.markdown(f"**예상 파일명**: `{dataset_info['expected_file']}`")

            uploaded_file = st.file_uploader(
                f"{dataset_info['display_name']} CSV 파일 선택",
                type=['csv'],
                key=f"upload_{dataset_key}"
            )

            if uploaded_file is not None:
                try:
                    df = read_uploaded_csv(uploaded_file)
                    # Store in session_state (T018)
                    st.session_state.datasets[dataset_key] = df
                    st.session_state.upload_status[dataset_key] = True

                    # Display upload info (T019)
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("파일명", uploaded_file.name)
                    with col2:
                        file_size_kb = uploaded_file.size / 1024
                        if file_size_kb > 1024:
                            st.metric("파일 크기", f"{file_size_kb/1024:.2f} MB")
                        else:
                            st.metric("파일 크기", f"{file_size_kb:.2f} KB")
                    with col3:
                        st.metric("행 x 컬럼", f"{len(df):,} x {len(df.columns)}")

                    st.success(f"✅ {dataset_info['display_name']} 데이터 업로드 완료!")

                    # Show preview
                    with st.expander("📋 데이터 미리보기", expanded=False):
                        st.dataframe(df.head(5), use_container_width=True)

                except Exception as e:
                    st.error(f"❌ 파일 읽기 오류: {str(e)}")

    st.markdown("---")

    # Key Features
    st.subheader("🎯 주요 기능")
    feature_col1, feature_col2 = st.columns(2)

    with feature_col1:
        st.markdown("""
        **개별 데이터셋 탐색**
        - 7개의 공공 데이터셋 지원
        - 기본 통계 및 데이터 미리보기
        - 대화형 차트 및 그래프
        - 지리적 분포 지도 시각화
        """)

        st.markdown("""
        **교차 데이터 분석**
        - 여러 데이터셋 동시 시각화
        - 공간적 관계 분석
        """)

    with feature_col2:
        st.markdown("""
        **사용자 친화적 인터페이스**
        - 직관적인 탭 기반 네비게이션
        - 반응형 레이아웃
        - 실시간 데이터 필터링
        - 다양한 시각화 옵션
        """)

        st.markdown("""
        **AI 데이터 분석**
        - 자연어 질의응답
        - 데이터 인사이트 제안
        """)

    # How to Use
    st.subheader("📚 사용 방법")

    st.markdown("""
    ### 1️⃣ 데이터 업로드
    1. 위의 각 데이터셋 섹션을 열어 CSV 파일을 업로드합니다
    2. 업로드된 파일 정보와 미리보기를 확인합니다

    ### 2️⃣ 개별 데이터셋 탐색
    1. 해당 데이터셋 탭을 선택합니다
    2. 기본 통계와 데이터 미리보기를 확인합니다
    3. 숫자형/범주형 컬럼을 선택하여 분포를 시각화합니다

    ### 3️⃣ AI 데이터 분석
    1. 사이드바에서 API Key를 입력합니다
    2. "데이터 질의응답" 탭에서 질문을 입력합니다
    """)

    # Technical Information
    st.subheader("🔧 기술 스택")

    tech_col1, tech_col2, tech_col3 = st.columns(3)

    with tech_col1:
        st.markdown("""
        **프론트엔드**
        - Streamlit
        - Plotly
        - Folium
        """)

    with tech_col2:
        st.markdown("""
        **데이터 처리**
        - Pandas
        - NumPy
        """)

    with tech_col3:
        st.markdown("""
        **AI**
        - Anthropic Claude
        - Python 3.10+
        """)


def render_cross_analysis_tab():
    """
    Render the cross-data analysis tab. (T023, T024 - simplified, no proximity analysis)
    """
    st.header("🔄 교차 데이터 분석")
    st.markdown("""
    여러 데이터셋을 동시에 지도 위에 표시하여 공간적 관계를 분석합니다.
    """)

    # Check if any datasets are uploaded
    uploaded_datasets = [
        key for key, uploaded in st.session_state.upload_status.items()
        if uploaded
    ]

    if not uploaded_datasets:
        st.info("📤 먼저 **프로젝트 개요** 탭에서 데이터셋을 업로드해주세요.")
        return

    # Dataset selection
    st.subheader("데이터셋 선택")

    available_options = {
        DATASET_MAPPING[key]['display_name']: key
        for key in uploaded_datasets
    }

    # Multi-select for datasets
    selected_names = st.multiselect(
        "분석할 데이터셋을 선택하세요 (2개 이상 권장):",
        options=list(available_options.keys()),
        default=list(available_options.keys())[:2] if len(available_options) >= 2 else list(available_options.keys())
    )

    if len(selected_names) == 0:
        st.warning("⚠️ 최소 1개 이상의 데이터셋을 선택해주세요.")
        return

    # Load selected datasets
    datasets_to_overlay = []
    dataset_colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'darkblue']

    for idx, name in enumerate(selected_names):
        dataset_key = available_options[name]
        df = load_dataset_from_session(dataset_key)

        if df is not None:
            lat_col, lng_col = detect_lat_lng_columns(df)

            if lat_col and lng_col:
                popup_candidates = [col for col in df.columns if col not in [lat_col, lng_col]]
                popup_cols = popup_candidates[:3]

                datasets_to_overlay.append({
                    'df': df,
                    'lat_col': lat_col,
                    'lng_col': lng_col,
                    'popup_cols': popup_cols,
                    'color': dataset_colors[idx % len(dataset_colors)],
                    'name': name,
                    'icon': 'info-sign'
                })
            else:
                st.warning(f"⚠️ {name} 데이터셋에서 좌표 정보를 찾을 수 없습니다.")

    # Display overlay map (T024)
    if datasets_to_overlay:
        st.subheader("🗺️ 통합 지도 시각화")

        # Show legend
        st.markdown("**범례:**")
        legend_cols = st.columns(min(len(datasets_to_overlay), 4))
        for idx, ds in enumerate(datasets_to_overlay):
            with legend_cols[idx % 4]:
                st.markdown(f"🔵 **{ds['name']}** ({len(ds['df']):,}개)")

        # Create and display map
        overlay_map = create_overlay_map(datasets_to_overlay)
        st_folium(overlay_map, width=900, height=600)

        st.info("💡 지도 우측 상단의 레이어 컨트롤을 사용하여 각 데이터셋을 개별적으로 켜고 끌 수 있습니다.")
    else:
        st.warning("⚠️ 좌표 정보가 있는 데이터셋이 없습니다.")


def render_sidebar():
    """
    Render the sidebar with API key input and status. (T041-T044)
    """
    with st.sidebar:
        st.header("🤖 AI 설정")

        # T041: API Key input
        api_key = st.text_input(
            "Anthropic API Key",
            type="password",
            placeholder="sk-ant-...",
            help="Anthropic API Key를 입력하세요. https://console.anthropic.com 에서 발급받을 수 있습니다.",
            key="sidebar_api_key"
        )

        if api_key:
            if validate_api_key(api_key):
                st.session_state.chatbot['api_key'] = api_key
                st.success("✅ API Key 설정됨")
            else:
                st.error("❌ API Key 형식이 올바르지 않습니다")
        else:
            st.info("API Key를 입력하면 AI 챗봇을 사용할 수 있습니다")

        # T042: Model selection
        st.subheader("모델 선택")
        model_options = {opt['name']: opt['id'] for opt in AI_MODEL_OPTIONS}
        model_descriptions = {opt['name']: opt['description'] for opt in AI_MODEL_OPTIONS}

        selected_model_name = st.selectbox(
            "AI 모델",
            options=list(model_options.keys()),
            help=model_descriptions.get(list(model_options.keys())[0], ""),
            key="sidebar_model"
        )
        st.session_state.chatbot['model'] = model_options[selected_model_name]
        st.caption(model_descriptions[selected_model_name])

        # T043: Token usage display
        st.subheader("📊 토큰 사용량")
        tokens = st.session_state.chatbot['tokens']
        col1, col2 = st.columns(2)
        with col1:
            st.metric("입력", f"{tokens['input']:,}")
        with col2:
            st.metric("출력", f"{tokens['output']:,}")
        st.metric("총계", f"{tokens['total']:,}")

        st.markdown("---")

        # T044: Upload status display
        st.subheader("📁 데이터 업로드 현황")
        uploaded_count = sum(st.session_state.upload_status.values())
        st.progress(uploaded_count / len(DATASET_MAPPING))
        st.caption(f"{uploaded_count} / {len(DATASET_MAPPING)} 데이터셋 업로드됨")

        for key, status in st.session_state.upload_status.items():
            icon = "✅" if status else "⏳"
            st.text(f"{icon} {DATASET_MAPPING[key]['display_name']}")


def render_chatbot_tab():
    """
    Render the chatbot tab for data Q&A. (T045-T050)
    """
    st.header("💬 데이터 질의응답")
    st.markdown("업로드한 데이터셋에 대해 AI에게 질문하세요.")

    # T050: Check API Key
    api_key = st.session_state.chatbot.get('api_key', '')
    if not api_key or not validate_api_key(api_key):
        st.warning("⚠️ 사이드바에서 Anthropic API Key를 먼저 입력해주세요.")
        st.info("""
        **API Key 발급 방법:**
        1. [Anthropic Console](https://console.anthropic.com) 방문
        2. 계정 생성 또는 로그인
        3. API Keys 메뉴에서 새 키 생성
        4. 생성된 키를 사이드바에 입력
        """)
        return

    # Check uploaded datasets
    uploaded_datasets = {
        DATASET_MAPPING[key]['display_name']: key
        for key, uploaded in st.session_state.upload_status.items()
        if uploaded
    }

    if not uploaded_datasets:
        st.info("📤 먼저 **프로젝트 개요** 탭에서 데이터셋을 업로드해주세요.")
        return

    # T046: Dataset selection
    selected_display_name = st.selectbox(
        "분석할 데이터셋 선택:",
        options=list(uploaded_datasets.keys()),
        key="chatbot_dataset"
    )
    selected_dataset_key = uploaded_datasets[selected_display_name]
    st.session_state.chatbot['selected_dataset'] = selected_dataset_key

    # Load selected dataset
    df = load_dataset_from_session(selected_dataset_key)
    if df is None:
        st.error("데이터를 불러올 수 없습니다.")
        return

    # Show dataset summary
    with st.expander("📊 데이터셋 요약", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("행 수", f"{len(df):,}")
        with col2:
            st.metric("컬럼 수", len(df.columns))
        with col3:
            missing_pct = df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100
            st.metric("전체 결측률", f"{missing_pct:.1f}%")
        st.dataframe(df.head(3), use_container_width=True)

    st.markdown("---")

    # T049: Display conversation history
    st.subheader("대화 내역")

    for msg in st.session_state.chatbot['messages']:
        with st.chat_message(msg['role']):
            st.markdown(msg['content'])

    # T047, T048: Question input and send
    user_question = st.chat_input("데이터에 대해 질문하세요...")

    if user_question:
        # Add user message to history
        st.session_state.chatbot['messages'].append({
            'role': 'user',
            'content': user_question
        })

        # Display user message
        with st.chat_message('user'):
            st.markdown(user_question)

        # Generate response
        with st.chat_message('assistant'):
            with st.spinner("AI가 답변을 생성하고 있습니다..."):
                try:
                    # Create Anthropic client
                    client = Anthropic(api_key=api_key)

                    # Create data context
                    data_context = create_data_context(df, selected_display_name)

                    # Prepare messages for API
                    api_messages = [
                        {'role': m['role'], 'content': m['content']}
                        for m in st.session_state.chatbot['messages']
                    ]

                    # Get response
                    response_text, usage = create_chat_response(
                        client=client,
                        model=st.session_state.chatbot['model'],
                        messages=api_messages,
                        data_context=data_context
                    )

                    # Update token usage
                    st.session_state.chatbot['tokens']['input'] += usage['input_tokens']
                    st.session_state.chatbot['tokens']['output'] += usage['output_tokens']
                    st.session_state.chatbot['tokens']['total'] += (
                        usage['input_tokens'] + usage['output_tokens']
                    )

                    # Display response
                    st.markdown(response_text)

                    # Add assistant message to history
                    st.session_state.chatbot['messages'].append({
                        'role': 'assistant',
                        'content': response_text
                    })

                except Exception as e:
                    error_msg = handle_chat_error(e)
                    st.error(error_msg)

    # Clear conversation button
    if st.session_state.chatbot['messages']:
        if st.button("🗑️ 대화 내역 삭제", key="clear_chat"):
            st.session_state.chatbot['messages'] = []
            st.rerun()


def main():
    """Main application entry point."""
    # Initialize session state
    init_session_state()

    # Render sidebar (T041-T044)
    render_sidebar()

    st.title("📊 대구 공공데이터 시각화")
    st.markdown("""
    대구 공공데이터 시각화 도구에 오신 것을 환영합니다! 이 애플리케이션은
    7개의 공공 데이터셋을 탐색하고 대화형 시각화를 통해 공간 패턴을 발견할 수 있도록 도와줍니다.
    """)

    # Create tabs - T013: 프로젝트 개요 first, T014: tab names, T015: 데이터 질의응답 추가
    tabs = st.tabs([
        "📖 프로젝트 개요",
        "🎥 CCTV",
        "💡 보안등",
        "🏫 어린이 보호구역",
        "🅿️ 주차장",
        "🚗 사고",
        "📊 훈련 데이터",
        "📋 테스트 데이터",
        "🔄 교차 데이터 분석",
        "💬 데이터 질의응답"
    ])

    # Tab 0: Project Overview (with upload)
    with tabs[0]:
        render_overview_tab()

    # Tab 1: CCTV
    with tabs[1]:
        render_dataset_tab('cctv', 'CCTV')

    # Tab 2: Security Lights
    with tabs[2]:
        render_dataset_tab('lights', '보안등')

    # Tab 3: Child Protection Zones
    with tabs[3]:
        render_dataset_tab('zones', '어린이 보호구역')

    # Tab 4: Parking Lots
    with tabs[4]:
        render_dataset_tab('parking', '주차장')

    # Tab 5: Accident
    with tabs[5]:
        render_dataset_tab('accident', '사고')

    # Tab 6: Train Data (T014: renamed)
    with tabs[6]:
        render_dataset_tab('train', '훈련 데이터')

    # Tab 7: Test Data (T014: renamed)
    with tabs[7]:
        render_dataset_tab('test', '테스트 데이터')

    # Tab 8: Cross-Data Analysis (T023, T024: simplified)
    with tabs[8]:
        render_cross_analysis_tab()

    # Tab 9: Chatbot (T045-T050)
    with tabs[9]:
        render_chatbot_tab()


if __name__ == "__main__":
    main()
