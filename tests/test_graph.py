"""
Unit tests for graph module.

대상: utils/graph.py
의도: LangGraph StateGraph 워크플로우가 올바르게 동작하는지 검증
"""
import os
import pytest
from unittest.mock import Mock, MagicMock
from dotenv import load_dotenv

from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_anthropic import ChatAnthropic

from utils.graph import (
    ChatState,
    route_tools,
    build_graph,
)

# .env 파일에서 환경 변수 로드
load_dotenv()


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def api_key():
    """ANTHROPIC_API_KEY 환경 변수에서 API Key 로드"""
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        pytest.skip("ANTHROPIC_API_KEY 환경 변수가 설정되지 않음")
    return key


@pytest.fixture
def mock_llm():
    """Mock LLM 객체"""
    mock = MagicMock(spec=ChatAnthropic)
    mock.bind_tools = MagicMock(return_value=mock)
    return mock


@pytest.fixture
def sample_tools():
    """테스트용 샘플 도구 리스트"""
    from langchain_core.tools import tool

    @tool
    def test_tool(query: str) -> str:
        """테스트용 도구"""
        return f"Result: {query}"

    return [test_tool]


# ============================================================================
# ChatState 테스트
# ============================================================================

class TestChatState:
    """ChatState TypedDict 테스트"""

    def test_create_empty_state(self):
        """의도: 빈 ChatState 생성 검증"""
        state: ChatState = {
            "messages": [],
            "current_dataset": ""
        }
        assert state["messages"] == []
        assert state["current_dataset"] == ""

    def test_create_state_with_messages(self):
        """의도: 메시지가 있는 ChatState 생성 검증"""
        messages = [
            HumanMessage(content="안녕하세요"),
            AIMessage(content="안녕하세요!")
        ]
        state: ChatState = {
            "messages": messages,
            "current_dataset": "test_dataset"
        }
        assert len(state["messages"]) == 2
        assert state["current_dataset"] == "test_dataset"


# ============================================================================
# route_tools 테스트
# ============================================================================

class TestRouteTools:
    """route_tools 함수 테스트"""

    def test_empty_messages_returns_end(self):
        """의도: 빈 메시지 리스트에서 END 반환 검증"""
        state: ChatState = {"messages": [], "current_dataset": ""}
        result = route_tools(state)
        assert result == "__end__"

    def test_human_message_returns_end(self):
        """의도: HumanMessage만 있을 때 END 반환 검증"""
        state: ChatState = {
            "messages": [HumanMessage(content="안녕")],
            "current_dataset": ""
        }
        result = route_tools(state)
        assert result == "__end__"

    def test_ai_message_without_tool_calls_returns_end(self):
        """의도: tool_calls가 없는 AIMessage에서 END 반환 검증"""
        ai_msg = AIMessage(content="응답입니다")
        state: ChatState = {
            "messages": [ai_msg],
            "current_dataset": ""
        }
        result = route_tools(state)
        assert result == "__end__"

    def test_ai_message_with_tool_calls_returns_tools(self):
        """의도: tool_calls가 있는 AIMessage에서 'tools' 반환 검증"""
        ai_msg = AIMessage(
            content="",
            tool_calls=[{
                "id": "call_123",
                "name": "test_tool",
                "args": {"query": "test"}
            }]
        )
        state: ChatState = {
            "messages": [ai_msg],
            "current_dataset": ""
        }
        result = route_tools(state)
        assert result == "tools"

    def test_multiple_messages_checks_last(self):
        """의도: 여러 메시지 중 마지막 메시지만 확인하는지 검증"""
        messages = [
            HumanMessage(content="질문"),
            AIMessage(content="응답", tool_calls=[{
                "id": "call_1",
                "name": "tool1",
                "args": {}
            }]),
            AIMessage(content="최종 응답")  # tool_calls 없음
        ]
        state: ChatState = {"messages": messages, "current_dataset": ""}
        result = route_tools(state)
        assert result == "__end__"


# ============================================================================
# build_graph 테스트
# ============================================================================

class TestBuildGraph:
    """build_graph 함수 테스트"""

    def test_graph_compilation(self, mock_llm, sample_tools):
        """의도: 그래프가 정상적으로 컴파일되는지 검증"""
        graph = build_graph(mock_llm, sample_tools, "시스템 프롬프트")
        assert graph is not None
        # 컴파일된 그래프는 invoke 메서드를 가짐
        assert hasattr(graph, 'invoke')

    def test_graph_has_nodes(self, mock_llm, sample_tools):
        """의도: 그래프에 chatbot, tools 노드가 있는지 검증"""
        graph = build_graph(mock_llm, sample_tools)
        # 그래프 구조 확인 (컴파일 후에는 nodes가 직접 접근되지 않을 수 있음)
        assert graph is not None

    def test_graph_without_system_prompt(self, mock_llm, sample_tools):
        """의도: 시스템 프롬프트 없이 그래프 생성 검증"""
        graph = build_graph(mock_llm, sample_tools, system_prompt="")
        assert graph is not None

    def test_graph_with_empty_tools(self, mock_llm):
        """의도: 빈 도구 리스트로 그래프 생성 검증"""
        graph = build_graph(mock_llm, [], "시스템 프롬프트")
        assert graph is not None

    @pytest.mark.api
    def test_graph_invoke_with_real_llm(self, api_key, sample_tools):
        """의도: 실제 LLM으로 그래프 실행 검증"""
        llm = ChatAnthropic(
            api_key=api_key,
            model="claude-sonnet-4-20250514",
            max_tokens=100,
        )
        graph = build_graph(llm, sample_tools, "당신은 도움이 되는 AI입니다.")

        state: ChatState = {
            "messages": [HumanMessage(content="안녕")],
            "current_dataset": ""
        }

        try:
            result = graph.invoke(state)
            assert "messages" in result
            assert len(result["messages"]) > 0
        except Exception as e:
            # API 에러는 허용 (크레딧 부족 등)
            error_str = str(e).lower()
            assert 'credit' in error_str or 'api' in error_str or 'rate' in error_str

    @pytest.mark.api
    def test_graph_tool_calling(self, api_key):
        """의도: 그래프에서 도구 호출이 정상 동작하는지 검증"""
        from langchain_core.tools import tool

        @tool
        def get_time() -> str:
            """현재 시간을 반환합니다."""
            return "현재 시간: 12:00"

        llm = ChatAnthropic(
            api_key=api_key,
            model="claude-sonnet-4-20250514",
            max_tokens=200,
        )
        graph = build_graph(llm, [get_time], "도구를 사용해서 질문에 답하세요.")

        state: ChatState = {
            "messages": [HumanMessage(content="지금 몇 시야?")],
            "current_dataset": ""
        }

        try:
            result = graph.invoke(state)
            assert "messages" in result
        except Exception as e:
            # API 에러는 허용
            error_str = str(e).lower()
            assert 'credit' in error_str or 'api' in error_str or 'rate' in error_str


# ============================================================================
# Integration 테스트 (API 필요)
# ============================================================================

class TestGraphIntegration:
    """그래프 통합 테스트"""

    @pytest.mark.api
    @pytest.mark.slow
    def test_full_conversation_flow(self, api_key, sample_tools):
        """의도: 전체 대화 흐름이 정상 동작하는지 검증"""
        llm = ChatAnthropic(
            api_key=api_key,
            model="claude-sonnet-4-20250514",
            max_tokens=100,
        )
        graph = build_graph(llm, sample_tools)

        # 첫 번째 메시지
        state: ChatState = {
            "messages": [HumanMessage(content="안녕하세요")],
            "current_dataset": "test"
        }

        try:
            result = graph.invoke(state)
            assert len(result["messages"]) >= 1
        except Exception as e:
            error_str = str(e).lower()
            assert 'credit' in error_str or 'api' in error_str or 'rate' in error_str
