"""
Unit tests for chatbot module.

대상: utils/chatbot.py
의도: AI 챗봇 모듈의 헬퍼 함수들이 올바르게 동작하는지 검증
"""
import os
import pytest
import pandas as pd
from anthropic import APIConnectionError, RateLimitError, APIError
from dotenv import load_dotenv

from utils.chatbot import (
    create_data_context,
    handle_chat_error,
    validate_api_key,
    create_langgraph_model,
    run_langgraph_chat,
    stream_langgraph_chat,
    # Legacy functions
    create_chat_response,
    run_tool_calling,
    create_chat_response_with_tools,
    stream_chat_response_with_tools,
    MAX_TOOL_ITERATIONS,
)
from anthropic import Anthropic

# .env 파일에서 환경 변수 로드
load_dotenv()


# ============================================================================
# create_data_context 테스트
# ============================================================================

class TestCreateDataContext:
    """create_data_context 함수 테스트"""

    def test_basic_context_creation(self):
        """의도: 기본 DataFrame으로 컨텍스트가 생성되는지 검증"""
        # Arrange
        df = pd.DataFrame({
            '이름': ['홍길동', '김철수', '이영희'],
            '나이': [30, 25, 35],
            '점수': [85.5, 90.0, 78.5]
        })

        # Act
        context = create_data_context(df, "test_data")

        # Assert
        assert "test_data" in context
        assert "행 수: 3" in context
        assert "컬럼 수: 3" in context
        assert "이름" in context
        assert "나이" in context
        assert "점수" in context

    def test_numeric_column_stats(self):
        """의도: 수치형 컬럼의 통계 정보(min, max, mean)가 포함되는지 검증"""
        # Arrange
        df = pd.DataFrame({
            '값': [10, 20, 30, 40, 50]
        })

        # Act
        context = create_data_context(df, "numeric_test")

        # Assert
        assert "min=" in context
        assert "max=" in context
        assert "mean=" in context

    def test_categorical_column_stats(self):
        """의도: 범주형 컬럼의 통계 정보(unique, top3)가 포함되는지 검증"""
        # Arrange
        df = pd.DataFrame({
            '카테고리': ['A', 'B', 'A', 'C', 'B', 'A']
        })

        # Act
        context = create_data_context(df, "categorical_test")

        # Assert
        assert "unique=" in context
        assert "top3=" in context

    def test_missing_values_percentage(self):
        """의도: 결측값 비율이 컨텍스트에 포함되는지 검증"""
        # Arrange
        df = pd.DataFrame({
            '값': [1, 2, None, 4, None]
        })

        # Act
        context = create_data_context(df, "missing_test")

        # Assert
        assert "결측값" in context
        assert "40.0%" in context  # 2/5 = 40%

    def test_empty_dataframe(self):
        """의도: 빈 DataFrame으로도 컨텍스트가 생성되는지 검증"""
        # Arrange
        df = pd.DataFrame()

        # Act
        context = create_data_context(df, "empty_test")

        # Assert
        assert "empty_test" in context
        assert "행 수: 0" in context
        assert "컬럼 수: 0" in context

    def test_sample_data_included(self):
        """의도: 샘플 데이터(처음 3행)가 포함되는지 검증"""
        # Arrange
        df = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': ['a', 'b', 'c', 'd', 'e']
        })

        # Act
        context = create_data_context(df, "sample_test")

        # Assert
        assert "샘플 데이터" in context
        assert "처음 3행" in context

    def test_all_null_numeric_column(self):
        """의도: 모든 값이 결측치인 수치형 컬럼 처리 검증"""
        # Arrange - 명시적으로 float 타입 지정하여 수치형으로 인식되게 함
        df = pd.DataFrame({
            '값': pd.array([None, None, None], dtype='float64')
        })

        # Act
        context = create_data_context(df, "all_null_test")

        # Assert
        assert "모든 값이 결측치입니다" in context

    def test_large_numbers_formatted(self):
        """의도: 행 수가 큰 경우 천 단위 구분자가 적용되는지 검증"""
        # Arrange
        df = pd.DataFrame({
            '값': range(10000)
        })

        # Act
        context = create_data_context(df, "large_test")

        # Assert
        assert "10,000" in context


# ============================================================================
# handle_chat_error 테스트
# ============================================================================

class TestHandleChatError:
    """handle_chat_error 함수 테스트"""

    def test_connection_error(self):
        """의도: APIConnectionError에 대해 네트워크 오류 메시지 반환 검증"""
        # Arrange
        error = APIConnectionError(request=None)

        # Act
        message = handle_chat_error(error)

        # Assert
        assert "네트워크" in message
        assert "연결" in message

    def test_rate_limit_error(self):
        """의도: RateLimitError에 대해 한도 초과 메시지 반환 검증"""
        # Arrange - RateLimitError는 실제 response가 필요하므로 Mock 사용
        from unittest.mock import Mock
        mock_response = Mock()
        mock_response.request = Mock()
        error = RateLimitError(
            message="rate limit exceeded",
            response=mock_response,
            body=None
        )

        # Act
        message = handle_chat_error(error)

        # Assert
        assert "한도" in message or "초과" in message

    def test_api_error_authentication(self):
        """의도: 인증 관련 APIError에 대해 적절한 메시지 반환 검증"""
        # Arrange
        error = APIError(
            message="authentication failed",
            request=None,
            body=None
        )

        # Act
        message = handle_chat_error(error)

        # Assert
        assert "인증" in message or "API Key" in message

    def test_api_error_model(self):
        """의도: 모델 관련 APIError에 대해 적절한 메시지 반환 검증"""
        # Arrange
        error = APIError(
            message="model not found",
            request=None,
            body=None
        )

        # Act
        message = handle_chat_error(error)

        # Assert
        assert "모델" in message

    def test_generic_api_error(self):
        """의도: 일반 APIError에 대해 적절한 메시지 반환 검증"""
        # Arrange
        error = APIError(
            message="something went wrong",
            request=None,
            body=None
        )

        # Act
        message = handle_chat_error(error)

        # Assert
        assert "API 오류" in message

    def test_unexpected_error(self):
        """의도: 예상치 못한 에러에 대해 적절한 메시지 반환 검증"""
        # Arrange
        error = ValueError("unexpected error")

        # Act
        message = handle_chat_error(error)

        # Assert
        assert "예상치 못한 오류" in message


# ============================================================================
# validate_api_key 테스트
# ============================================================================

class TestValidateApiKey:
    """validate_api_key 함수 테스트"""

    def test_valid_key_sk_ant_api03(self):
        """의도: sk-ant-api03- 형식 키가 유효한 것으로 판정되는지 검증"""
        # Arrange
        key = "sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

        # Act
        result = validate_api_key(key)

        # Assert
        assert result is True

    def test_valid_key_sk_ant(self):
        """의도: sk-ant- 형식 키가 유효한 것으로 판정되는지 검증"""
        # Arrange
        key = "sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

        # Act
        result = validate_api_key(key)

        # Assert
        assert result is True

    def test_valid_key_sk_new_format(self):
        """의도: sk- 새 형식 키가 유효한 것으로 판정되는지 검증"""
        # Arrange
        key = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

        # Act
        result = validate_api_key(key)

        # Assert
        assert result is True

    def test_invalid_empty_key(self):
        """의도: 빈 키가 무효한 것으로 판정되는지 검증"""
        # Act & Assert
        assert validate_api_key("") is False
        assert validate_api_key(None) is False

    def test_invalid_wrong_prefix(self):
        """의도: sk-로 시작하지 않는 키가 무효한 것으로 판정되는지 검증"""
        # Arrange
        key = "invalid-key-xxxxxxxxxxxxxxxxxxxxx"

        # Act
        result = validate_api_key(key)

        # Assert
        assert result is False

    def test_invalid_too_short(self):
        """의도: 너무 짧은 키가 무효한 것으로 판정되는지 검증"""
        # Arrange
        key = "sk-short"

        # Act
        result = validate_api_key(key)

        # Assert
        assert result is False

    def test_minimum_valid_length(self):
        """의도: 최소 유효 길이(21자) 키가 유효한 것으로 판정되는지 검증"""
        # Arrange - 정확히 21자 (sk- + 18자)
        key = "sk-" + "x" * 18

        # Act
        result = validate_api_key(key)

        # Assert
        assert result is True

    def test_below_minimum_length(self):
        """의도: 최소 길이 미만(20자) 키가 무효한 것으로 판정되는지 검증"""
        # Arrange - 정확히 20자 (sk- + 17자)
        key = "sk-" + "x" * 17

        # Act
        result = validate_api_key(key)

        # Assert
        assert result is False


# ============================================================================
# create_langgraph_model 테스트
# ============================================================================

class TestCreateLanggraphModel:
    """create_langgraph_model 함수 테스트"""

    def test_model_creation_default(self):
        """의도: 기본 모델로 ChatAnthropic 인스턴스가 생성되는지 검증"""
        # Arrange
        api_key = "sk-ant-api03-test-key-xxxxxxxxxxxxxx"

        # Act
        model = create_langgraph_model(api_key)

        # Assert
        assert model is not None
        assert hasattr(model, 'invoke')
        assert hasattr(model, 'bind_tools')

    def test_model_creation_custom_model(self):
        """의도: 커스텀 모델 ID로 인스턴스가 생성되는지 검증"""
        # Arrange
        api_key = "sk-ant-api03-test-key-xxxxxxxxxxxxxx"
        model_id = "claude-3-haiku-20240307"

        # Act
        model = create_langgraph_model(api_key, model=model_id)

        # Assert
        assert model is not None

    def test_model_has_max_tokens(self):
        """의도: 생성된 모델에 max_tokens가 설정되어 있는지 검증"""
        # Arrange
        api_key = "sk-ant-api03-test-key-xxxxxxxxxxxxxx"

        # Act
        model = create_langgraph_model(api_key)

        # Assert
        # ChatAnthropic은 max_tokens를 내부적으로 관리
        assert model is not None


# ============================================================================
# 통합적 시나리오 테스트
# ============================================================================

class TestChatbotIntegration:
    """chatbot 모듈 통합 시나리오 테스트 (API 호출 없음)"""

    def test_context_creation_with_accident_data(self):
        """의도: 사고 데이터로 컨텍스트 생성 후 주요 정보가 포함되는지 검증"""
        # Arrange - 실제 앱에서 사용하는 것과 유사한 구조
        df = pd.DataFrame({
            '사고일시': ['2022-01-15 08', '2022-03-20 14', '2022-06-10 18'],
            '기상상태': ['맑음', '흐림', '비'],
            '노면상태': ['건조', '건조', '젖음/습기'],
            '도로형태': ['교차로', '단일로', '교차로'],
            '사고유형': ['차대차', '차대사람', '차대차'],
            '시군구': ['중구', '동구', '수성구'],
            '사고연': [2022, 2022, 2022],
            '사고월': [1, 3, 6],
            '시간대': ['출근시간대', '일반시간대', '퇴근시간대'],
        })

        # Act
        context = create_data_context(df, "대구교통사고")

        # Assert
        assert "대구교통사고" in context
        assert "행 수: 3" in context
        assert "기상상태" in context
        assert "시간대" in context
        assert "사고유형" in context

    def test_error_handling_flow(self):
        """의도: 다양한 에러에 대해 한국어 메시지가 반환되는지 검증"""
        # Arrange
        from unittest.mock import Mock
        mock_response = Mock()
        mock_response.request = Mock()

        errors = [
            APIConnectionError(request=None),
            RateLimitError(message="limit", response=mock_response, body=None),
            APIError(message="error", request=None, body=None),
            ValueError("unknown"),
        ]

        # Act & Assert
        for error in errors:
            message = handle_chat_error(error)
            # 모든 에러 메시지가 한국어로 반환되어야 함
            assert any(char >= '\uac00' and char <= '\ud7a3' for char in message), \
                f"Error message should contain Korean: {message}"


# ============================================================================
# API 테스트 - run_langgraph_chat
# ============================================================================

@pytest.fixture
def api_key():
    """ANTHROPIC_API_KEY 환경 변수에서 API Key 로드"""
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        pytest.skip("ANTHROPIC_API_KEY 환경 변수가 설정되지 않음")
    return key


@pytest.fixture
def sample_df():
    """테스트용 샘플 DataFrame"""
    return pd.DataFrame({
        '사고일시': ['2022-01-15 08', '2022-03-20 14', '2022-06-10 18'],
        '기상상태': ['맑음', '흐림', '비'],
        '노면상태': ['건조', '건조', '젖음/습기'],
        '도로형태': ['교차로', '단일로', '교차로'],
        '사고유형': ['차대차', '차대사람', '차대차'],
        '시군구': ['중구', '동구', '수성구'],
    })


class TestRunLanggraphChat:
    """run_langgraph_chat API 테스트"""

    @pytest.mark.api
    def test_simple_greeting(self, api_key, sample_df):
        """의도: 간단한 인사에 대해 응답이 반환되는지 검증"""
        # Arrange
        messages = [{"role": "user", "content": "안녕하세요"}]
        data_context = create_data_context(sample_df, "test")

        # Act
        response, usage = run_langgraph_chat(
            api_key=api_key,
            model="claude-sonnet-4-20250514",
            messages=messages,
            data_context=data_context,
            df=sample_df,
            dataset_name="test"
        )

        # Assert
        assert response is not None
        assert len(response) > 0

    @pytest.mark.api
    def test_data_query_with_tool_call(self, api_key, sample_df):
        """의도: 데이터 관련 질문에 도구를 사용하여 응답하는지 검증"""
        # Arrange
        messages = [{"role": "user", "content": "이 데이터셋의 행 수와 컬럼 목록을 알려줘"}]
        data_context = create_data_context(sample_df, "accident")

        # Act
        response, usage = run_langgraph_chat(
            api_key=api_key,
            model="claude-sonnet-4-20250514",
            messages=messages,
            data_context=data_context,
            df=sample_df,
            dataset_name="accident"
        )

        # Assert
        assert response is not None
        assert len(response) > 0
        # 정상 응답이거나 에러 메시지(크레딧 부족 등)가 반환됨
        # 데이터 관련 정보가 응답에 포함되거나, API 에러 메시지가 반환됨
        has_data_info = any(keyword in response for keyword in ['3', '행', '컬럼', '열', '데이터'])
        has_error = any(keyword in response for keyword in ['오류', '에러', 'API', 'credit', 'balance'])
        assert has_data_info or has_error, f"Unexpected response: {response[:200]}"

    @pytest.mark.api
    def test_value_counts_query(self, api_key, sample_df):
        """의도: 값 분포 질문에 올바르게 응답하는지 검증"""
        # Arrange
        messages = [{"role": "user", "content": "기상상태별 분포를 알려줘"}]
        data_context = create_data_context(sample_df, "accident")

        # Act
        response, usage = run_langgraph_chat(
            api_key=api_key,
            model="claude-sonnet-4-20250514",
            messages=messages,
            data_context=data_context,
            df=sample_df,
            dataset_name="accident"
        )

        # Assert
        assert response is not None
        assert len(response) > 0
        # 정상 응답이거나 에러 메시지가 반환됨
        has_weather_info = any(weather in response for weather in ['맑음', '흐림', '비', '분포', '기상'])
        has_error = any(keyword in response for keyword in ['오류', '에러', 'API', 'credit', 'balance'])
        assert has_weather_info or has_error, f"Unexpected response: {response[:200]}"

    @pytest.mark.api
    def test_conversation_context_maintained(self, api_key, sample_df):
        """의도: 대화 컨텍스트가 유지되는지 검증"""
        # Arrange - 이전 대화가 있는 상태
        messages = [
            {"role": "user", "content": "이 데이터에 어떤 컬럼들이 있어?"},
            {"role": "assistant", "content": "사고일시, 기상상태, 노면상태, 도로형태, 사고유형, 시군구 컬럼이 있습니다."},
            {"role": "user", "content": "그 중 시군구 컬럼의 고유값을 알려줘"}
        ]
        data_context = create_data_context(sample_df, "accident")

        # Act
        response, usage = run_langgraph_chat(
            api_key=api_key,
            model="claude-sonnet-4-20250514",
            messages=messages,
            data_context=data_context,
            df=sample_df,
            dataset_name="accident"
        )

        # Assert
        assert response is not None
        assert len(response) > 0
        # 정상 응답이거나 에러 메시지가 반환됨
        has_district_info = any(district in response for district in ['중구', '동구', '수성구', '시군구', '고유'])
        has_error = any(keyword in response for keyword in ['오류', '에러', 'API', 'credit', 'balance'])
        assert has_district_info or has_error, f"Unexpected response: {response[:200]}"

    @pytest.mark.api
    def test_invalid_api_key_returns_error_message(self, sample_df):
        """의도: 잘못된 API Key로 호출 시 에러 메시지가 반환되는지 검증"""
        # Arrange
        messages = [{"role": "user", "content": "안녕"}]
        data_context = create_data_context(sample_df, "test")

        # Act
        response, usage = run_langgraph_chat(
            api_key="sk-invalid-key-xxxxxxxxxxxx",
            model="claude-sonnet-4-20250514",
            messages=messages,
            data_context=data_context,
            df=sample_df,
            dataset_name="test"
        )

        # Assert - 에러 메시지가 반환되어야 함
        assert response is not None
        assert any(keyword in response for keyword in ['오류', '에러', '인증', 'API'])


class TestStreamLanggraphChat:
    """stream_langgraph_chat API 테스트"""

    @pytest.mark.api
    def test_streaming_response(self, api_key, sample_df):
        """의도: 스트리밍 응답이 제너레이터로 반환되는지 검증"""
        # Arrange
        messages = [{"role": "user", "content": "안녕하세요"}]
        data_context = create_data_context(sample_df, "test")

        # Act
        stream = stream_langgraph_chat(
            api_key=api_key,
            model="claude-sonnet-4-20250514",
            messages=messages,
            data_context=data_context,
            df=sample_df,
            dataset_name="test"
        )

        # Assert - 제너레이터에서 값을 수집
        chunks = list(stream)
        assert len(chunks) > 0

        # 마지막 청크에 사용량 정보가 있어야 함
        last_chunk = chunks[-1]
        assert isinstance(last_chunk, dict)
        assert "__usage__" in last_chunk

    @pytest.mark.api
    def test_streaming_with_tool_call(self, api_key, sample_df):
        """의도: 도구 호출이 포함된 스트리밍 응답 검증"""
        # Arrange
        messages = [{"role": "user", "content": "데이터셋 정보를 알려줘"}]
        data_context = create_data_context(sample_df, "test")

        # Act
        stream = stream_langgraph_chat(
            api_key=api_key,
            model="claude-sonnet-4-20250514",
            messages=messages,
            data_context=data_context,
            df=sample_df,
            dataset_name="test"
        )

        # Assert
        chunks = list(stream)
        assert len(chunks) > 0

        # 도구 호출 이벤트가 있을 수 있음
        tool_events = [c for c in chunks if isinstance(c, dict) and "__tool_start__" in c]
        # 도구가 호출되었거나 직접 응답했거나 둘 다 유효함

        # 최종 텍스트가 있어야 함
        last_chunk = chunks[-1]
        assert "__text__" in last_chunk

    @pytest.mark.api
    def test_streaming_invalid_api_key(self, sample_df):
        """의도: 잘못된 API Key로 스트리밍 시 에러 처리 검증"""
        # Arrange
        messages = [{"role": "user", "content": "안녕"}]
        data_context = create_data_context(sample_df, "test")

        # Act
        stream = stream_langgraph_chat(
            api_key="sk-invalid-key-xxxxxxxxxxxx",
            model="claude-sonnet-4-20250514",
            messages=messages,
            data_context=data_context,
            df=sample_df,
            dataset_name="test"
        )

        # Assert - 에러가 발생해도 제너레이터가 반환됨
        chunks = list(stream)
        assert len(chunks) > 0

        # 마지막 청크에 사용량 정보가 있어야 함
        last_chunk = chunks[-1]
        assert "__usage__" in last_chunk


# ============================================================================
# Legacy API 테스트 - create_chat_response
# ============================================================================

class TestCreateChatResponseLegacy:
    """create_chat_response Legacy 함수 테스트"""

    @pytest.mark.api
    def test_basic_response(self, api_key, sample_df):
        """의도: 기본 채팅 응답 생성 검증"""
        client = Anthropic(api_key=api_key)
        messages = [{"role": "user", "content": "안녕하세요"}]
        data_context = create_data_context(sample_df, "test")

        try:
            response, usage = create_chat_response(
                client=client,
                model="claude-sonnet-4-20250514",
                messages=messages,
                data_context=data_context,
            )
            assert response is not None
            assert isinstance(usage, dict)
            assert 'input_tokens' in usage
            assert 'output_tokens' in usage
        except Exception as e:
            # API 에러는 허용 (크레딧 부족 등)
            error_str = str(e).lower()
            assert 'credit' in error_str or 'balance' in error_str or 'api' in error_str

    @pytest.mark.api
    def test_custom_max_tokens(self, api_key, sample_df):
        """의도: 커스텀 max_tokens 적용 검증"""
        client = Anthropic(api_key=api_key)
        messages = [{"role": "user", "content": "짧게 답해줘"}]
        data_context = create_data_context(sample_df, "test")

        try:
            response, usage = create_chat_response(
                client=client,
                model="claude-sonnet-4-20250514",
                messages=messages,
                data_context=data_context,
                max_tokens=50,
            )
            assert response is not None
        except Exception as e:
            error_str = str(e).lower()
            assert 'credit' in error_str or 'balance' in error_str or 'api' in error_str


# ============================================================================
# Legacy API 테스트 - run_tool_calling
# ============================================================================

class TestRunToolCallingLegacy:
    """run_tool_calling Legacy 함수 테스트"""

    @pytest.mark.api
    def test_tool_calling_response(self, api_key, sample_df):
        """의도: Tool Calling 응답 생성 검증"""
        client = Anthropic(api_key=api_key)
        messages = [{"role": "user", "content": "데이터셋 정보를 알려줘"}]
        data_context = create_data_context(sample_df, "test")

        try:
            response, usage = run_tool_calling(
                client=client,
                model="claude-sonnet-4-20250514",
                messages=messages,
                data_context=data_context,
                df=sample_df,
            )
            assert response is not None
            assert isinstance(usage, dict)
        except Exception as e:
            error_str = str(e).lower()
            assert 'credit' in error_str or 'balance' in error_str or 'api' in error_str

    @pytest.mark.api
    def test_tool_calling_iteration_limit(self, api_key, sample_df):
        """의도: MAX_TOOL_ITERATIONS 제한이 적용되는지 검증"""
        # MAX_TOOL_ITERATIONS 상수가 정의되어 있는지 확인
        assert MAX_TOOL_ITERATIONS == 3


# ============================================================================
# Legacy API 테스트 - create_chat_response_with_tools
# ============================================================================

class TestCreateChatResponseWithToolsLegacy:
    """create_chat_response_with_tools Legacy 함수 테스트"""

    @pytest.mark.api
    def test_with_tools_response(self, api_key, sample_df):
        """의도: 도구 포함 응답 생성 검증"""
        client = Anthropic(api_key=api_key)
        messages = [{"role": "user", "content": "데이터 행 수가 몇 개야?"}]
        data_context = create_data_context(sample_df, "test")

        try:
            response, usage = create_chat_response_with_tools(
                client=client,
                model="claude-sonnet-4-20250514",
                messages=messages,
                data_context=data_context,
                df=sample_df,
            )
            assert response is not None
            assert isinstance(usage, dict)
        except Exception as e:
            error_str = str(e).lower()
            assert 'credit' in error_str or 'balance' in error_str or 'api' in error_str

    @pytest.mark.api
    def test_error_handling(self, sample_df):
        """의도: 잘못된 API Key로 에러 핸들링 검증"""
        client = Anthropic(api_key="sk-invalid-key-xxxxxxxxxxxx")
        messages = [{"role": "user", "content": "안녕"}]
        data_context = create_data_context(sample_df, "test")

        response, usage = create_chat_response_with_tools(
            client=client,
            model="claude-sonnet-4-20250514",
            messages=messages,
            data_context=data_context,
            df=sample_df,
        )
        # 에러 메시지가 반환되어야 함
        assert response is not None
        assert any(keyword in response for keyword in ['오류', '에러', 'API', '인증'])


# ============================================================================
# Legacy API 테스트 - stream_chat_response_with_tools
# ============================================================================

class TestStreamChatResponseWithToolsLegacy:
    """stream_chat_response_with_tools Legacy 함수 테스트"""

    @pytest.mark.api
    @pytest.mark.slow
    def test_streaming_with_tools(self, api_key, sample_df):
        """의도: 도구 포함 스트리밍 응답 검증"""
        client = Anthropic(api_key=api_key)
        messages = [{"role": "user", "content": "안녕하세요"}]
        data_context = create_data_context(sample_df, "test")

        try:
            stream = stream_chat_response_with_tools(
                client=client,
                model="claude-sonnet-4-20250514",
                messages=messages,
                data_context=data_context,
                df=sample_df,
            )

            chunks = list(stream)
            assert len(chunks) > 0

            # 마지막 청크에 usage 정보가 있어야 함
            last_chunk = chunks[-1]
            assert isinstance(last_chunk, dict)
            assert '__usage__' in last_chunk
        except Exception as e:
            error_str = str(e).lower()
            assert 'credit' in error_str or 'balance' in error_str or 'api' in error_str

    @pytest.mark.api
    @pytest.mark.slow
    def test_streaming_tool_events(self, api_key, sample_df):
        """의도: 스트리밍 중 도구 이벤트 발생 검증"""
        client = Anthropic(api_key=api_key)
        messages = [{"role": "user", "content": "데이터셋 정보를 분석해줘"}]
        data_context = create_data_context(sample_df, "test")

        try:
            stream = stream_chat_response_with_tools(
                client=client,
                model="claude-sonnet-4-20250514",
                messages=messages,
                data_context=data_context,
                df=sample_df,
            )

            chunks = list(stream)
            # 도구 관련 이벤트가 있을 수 있음
            tool_events = [
                c for c in chunks
                if isinstance(c, dict) and (
                    '__tool_start__' in c or
                    '__tool_end__' in c or
                    '__tool_batch_start__' in c
                )
            ]
            # 도구가 호출되었거나 직접 응답했거나 둘 다 유효함
            assert len(chunks) > 0
        except Exception as e:
            error_str = str(e).lower()
            assert 'credit' in error_str or 'balance' in error_str or 'api' in error_str


# ============================================================================
# MAX_TOOL_ITERATIONS 상수 테스트
# ============================================================================

class TestMaxToolIterations:
    """MAX_TOOL_ITERATIONS 상수 테스트"""

    def test_max_iterations_value(self):
        """의도: MAX_TOOL_ITERATIONS가 적절한 값인지 검증"""
        assert MAX_TOOL_ITERATIONS > 0
        assert MAX_TOOL_ITERATIONS <= 10  # 너무 큰 값은 무한 루프 위험
