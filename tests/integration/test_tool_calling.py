"""
Integration tests for Tool Calling workflow.

대상: INT-003 (Tool Calling 워크플로우)
의도: chatbot → graph → tools 연결 검증 (LangGraph 전체 흐름)
"""
import pytest
import pandas as pd
from langchain_core.messages import HumanMessage, AIMessage
from utils.chatbot import (
    create_langgraph_model,
    run_langgraph_chat,
    create_data_context,
    validate_api_key,
)
from utils.graph import ChatState, build_graph, route_tools
from utils.tools import get_all_tools


# ============================================================================
# INT-003: Tool Calling 워크플로우
# ============================================================================

class TestToolCallingWorkflow:
    """
    INT-003: Tool Calling 워크플로우 통합 테스트
    흐름: 사용자 질문 → chatbot → graph.build_graph() → tools 실행 → 응답
    """

    @pytest.mark.integration
    def test_route_tools_with_tool_calls(self):
        """
        의도: tool_calls가 있는 AIMessage에서 "tools"로 라우팅되는지 검증
        """
        # Arrange - tool_calls가 있는 AIMessage 생성
        ai_message = AIMessage(
            content="",
            tool_calls=[{
                "id": "test_id",
                "name": "get_dataframe_info",
                "args": {}
            }]
        )
        state = ChatState(messages=[ai_message], current_dataset="test")

        # Act
        result = route_tools(state)

        # Assert
        assert result == "tools"

    @pytest.mark.integration
    def test_route_tools_without_tool_calls(self):
        """
        의도: tool_calls가 없는 AIMessage에서 END로 라우팅되는지 검증
        """
        # Arrange - tool_calls가 없는 AIMessage
        ai_message = AIMessage(content="일반 응답입니다.")
        state = ChatState(messages=[ai_message], current_dataset="test")

        # Act
        result = route_tools(state)

        # Assert
        assert result == "__end__"

    @pytest.mark.integration
    def test_route_tools_empty_messages(self):
        """
        의도: 빈 메시지 리스트에서 END로 라우팅되는지 검증
        """
        # Arrange
        state = ChatState(messages=[], current_dataset="test")

        # Act
        result = route_tools(state)

        # Assert
        assert result == "__end__"

    @pytest.mark.integration
    def test_build_graph_returns_compiled_graph(self, api_key):
        """
        의도: build_graph가 컴파일된 StateGraph를 반환하는지 검증
        """
        # Arrange
        llm = create_langgraph_model(api_key)
        tools = get_all_tools()

        # Act
        graph = build_graph(llm, tools, "테스트 시스템 프롬프트")

        # Assert
        assert graph is not None
        assert hasattr(graph, 'invoke')
        assert hasattr(graph, 'astream_events')

    @pytest.mark.integration
    @pytest.mark.api
    def test_langgraph_chat_dataframe_info_query(self, api_key, preprocessed_accident_df):
        """
        의도: "데이터 정보 알려줘" 질문에 get_dataframe_info 도구가 호출되어
              DataFrame 정보가 포함된 응답이 반환되는지 검증
        """
        # Arrange
        messages = [{"role": "user", "content": "이 데이터셋의 기본 정보를 알려줘. 행 수와 컬럼 목록을 포함해서."}]
        data_context = create_data_context(preprocessed_accident_df, "accident")

        # Act
        response, usage = run_langgraph_chat(
            api_key=api_key,
            model="claude-sonnet-4-20250514",
            messages=messages,
            data_context=data_context,
            df=preprocessed_accident_df,
            dataset_name="accident"
        )

        # Assert
        assert response is not None
        assert len(response) > 0
        # 응답에 데이터 관련 정보가 포함되어야 함
        assert any(keyword in response for keyword in ['행', '컬럼', '열', '데이터', '5'])

    @pytest.mark.integration
    @pytest.mark.api
    def test_langgraph_chat_statistics_query(self, api_key, preprocessed_accident_df):
        """
        의도: "통계 보여줘" 질문에 get_column_statistics 도구가 호출되어
              통계 정보가 포함된 응답이 반환되는지 검증
        """
        # Arrange
        messages = [{"role": "user", "content": "사고월 컬럼의 통계를 보여줘."}]
        data_context = create_data_context(preprocessed_accident_df, "accident")

        # Act
        response, usage = run_langgraph_chat(
            api_key=api_key,
            model="claude-sonnet-4-20250514",
            messages=messages,
            data_context=data_context,
            df=preprocessed_accident_df,
            dataset_name="accident"
        )

        # Assert
        assert response is not None
        # 통계 관련 용어가 포함되어야 함
        assert any(keyword in response for keyword in ['평균', '최소', '최대', '통계', 'mean', 'min', 'max'])

    @pytest.mark.integration
    @pytest.mark.api
    def test_langgraph_chat_no_tool_needed(self, api_key, preprocessed_accident_df):
        """
        의도: 도구 필요 없는 일반 질문에 도구 호출 없이 직접 응답하는지 검증
        """
        # Arrange - 데이터와 무관한 일반 질문
        messages = [{"role": "user", "content": "안녕하세요. 반갑습니다."}]
        data_context = create_data_context(preprocessed_accident_df, "accident")

        # Act
        response, usage = run_langgraph_chat(
            api_key=api_key,
            model="claude-sonnet-4-20250514",
            messages=messages,
            data_context=data_context,
            df=preprocessed_accident_df,
            dataset_name="accident"
        )

        # Assert
        assert response is not None
        assert len(response) > 0
        # 인사에 대한 응답

    @pytest.mark.integration
    @pytest.mark.api
    def test_langgraph_chat_value_counts_query(self, api_key, preprocessed_accident_df):
        """
        의도: "분포 보여줘" 질문에 get_value_counts 도구가 호출되어
              값 분포가 포함된 응답이 반환되는지 검증
        """
        # Arrange
        messages = [{"role": "user", "content": "기상상태별 분포를 알려줘."}]
        data_context = create_data_context(preprocessed_accident_df, "accident")

        # Act
        response, usage = run_langgraph_chat(
            api_key=api_key,
            model="claude-sonnet-4-20250514",
            messages=messages,
            data_context=data_context,
            df=preprocessed_accident_df,
            dataset_name="accident"
        )

        # Assert
        assert response is not None
        # 기상상태 값들이 응답에 포함되어야 함
        assert any(weather in response for weather in ['맑음', '흐림', '비', '눈', '분포', '개'])

    @pytest.mark.integration
    @pytest.mark.api
    def test_langgraph_chat_conversation_context(self, api_key, preprocessed_accident_df):
        """
        의도: 대화 컨텍스트가 유지되어 후속 질문에 적절히 응답하는지 검증
        """
        # Arrange - 이전 대화가 있는 상태
        messages = [
            {"role": "user", "content": "이 데이터셋에 어떤 컬럼들이 있어?"},
            {"role": "assistant", "content": "이 데이터셋에는 사고일시, 기상상태, 노면상태, 도로형태, 사고유형, 시군구, 그리고 전처리로 생성된 사고연, 사고월, 사고일, 사고시, 시간대 컬럼이 있습니다."},
            {"role": "user", "content": "그 중 시간대 컬럼의 값 분포를 알려줘."}
        ]
        data_context = create_data_context(preprocessed_accident_df, "accident")

        # Act
        response, usage = run_langgraph_chat(
            api_key=api_key,
            model="claude-sonnet-4-20250514",
            messages=messages,
            data_context=data_context,
            df=preprocessed_accident_df,
            dataset_name="accident"
        )

        # Assert
        assert response is not None
        # 시간대 관련 응답


class TestValidateApiKey:
    """API Key 유효성 검사 테스트"""

    @pytest.mark.integration
    def test_valid_api_key_format(self):
        """의도: 유효한 API Key 형식 검증"""
        assert validate_api_key("sk-ant-api03-xxxxxxxxxxxxxxxxxxxx") is True
        assert validate_api_key("sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx") is True

    @pytest.mark.integration
    def test_invalid_api_key_format(self):
        """의도: 잘못된 API Key 형식 검증"""
        assert validate_api_key("") is False
        assert validate_api_key("invalid-key") is False
        assert validate_api_key("sk-short") is False


class TestCreateDataContext:
    """데이터 컨텍스트 생성 테스트"""

    @pytest.mark.integration
    def test_create_context_with_preprocessed_data(self, preprocessed_accident_df):
        """의도: 전처리된 데이터로 컨텍스트가 올바르게 생성되는지 검증"""
        # Act
        context = create_data_context(preprocessed_accident_df, "accident")

        # Assert
        assert "accident" in context
        assert "행 수: 5" in context
        assert "시간대" in context

    @pytest.mark.integration
    def test_create_context_with_empty_dataframe(self):
        """의도: 빈 DataFrame으로 컨텍스트 생성 시 처리"""
        # Arrange
        empty_df = pd.DataFrame()

        # Act
        context = create_data_context(empty_df, "empty")

        # Assert
        assert "행 수: 0" in context
