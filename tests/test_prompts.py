"""
Unit tests for prompts module.

대상: utils/prompts.py
의도: 프롬프트 템플릿과 관련 함수들이 올바르게 동작하는지 검증
"""
import pytest

from utils.prompts import (
    SYSTEM_PROMPT_BASE,
    ECLO_PREDICTION_PROMPT,
    TOOL_DESCRIPTIONS,
    REPORT_GENERATION_PROMPT,
    REPORT_REQUIREMENTS_QUESTIONS,
    SYSTEM_PROMPT,
    detect_report_intent,
    get_tool_list_markdown,
)


# ============================================================================
# 프롬프트 상수 테스트
# ============================================================================

class TestPromptConstants:
    """프롬프트 상수 테스트"""

    def test_system_prompt_base_not_empty(self):
        """의도: SYSTEM_PROMPT_BASE가 비어있지 않은지 검증"""
        assert SYSTEM_PROMPT_BASE is not None
        assert len(SYSTEM_PROMPT_BASE) > 0

    def test_system_prompt_base_contains_key_elements(self):
        """의도: 기본 시스템 프롬프트에 핵심 요소가 포함되어 있는지 검증"""
        assert '데이터 분석' in SYSTEM_PROMPT_BASE
        assert '한국어' in SYSTEM_PROMPT_BASE

    def test_eclo_prediction_prompt_not_empty(self):
        """의도: ECLO_PREDICTION_PROMPT가 비어있지 않은지 검증"""
        assert ECLO_PREDICTION_PROMPT is not None
        assert len(ECLO_PREDICTION_PROMPT) > 0

    def test_eclo_prediction_prompt_contains_features(self):
        """의도: ECLO 프롬프트에 필수 피처 정보가 포함되어 있는지 검증"""
        required_features = [
            'weather', 'road_surface', 'road_type', 'accident_type',
            'time_period', 'district', 'day_of_week'
        ]
        for feature in required_features:
            assert feature in ECLO_PREDICTION_PROMPT, f"{feature} not found in ECLO prompt"

    def test_report_generation_prompt_not_empty(self):
        """의도: REPORT_GENERATION_PROMPT가 비어있지 않은지 검증"""
        assert REPORT_GENERATION_PROMPT is not None
        assert len(REPORT_GENERATION_PROMPT) > 0

    def test_report_generation_prompt_contains_questions(self):
        """의도: 보고서 생성 프롬프트에 필수 질문 요소가 포함되어 있는지 검증"""
        required_elements = ['주제', '스타일', '형태', '분량']
        for element in required_elements:
            assert element in REPORT_GENERATION_PROMPT, f"{element} not found"

    def test_report_requirements_questions_format(self):
        """의도: 보고서 요구사항 질문 템플릿이 올바른 형식인지 검증"""
        assert '주제' in REPORT_REQUIREMENTS_QUESTIONS
        assert '스타일' in REPORT_REQUIREMENTS_QUESTIONS
        assert '형태' in REPORT_REQUIREMENTS_QUESTIONS
        assert '분량' in REPORT_REQUIREMENTS_QUESTIONS

    def test_system_prompt_combined(self):
        """의도: 결합된 SYSTEM_PROMPT가 모든 구성 요소를 포함하는지 검증"""
        assert SYSTEM_PROMPT_BASE in SYSTEM_PROMPT
        assert ECLO_PREDICTION_PROMPT in SYSTEM_PROMPT
        assert REPORT_GENERATION_PROMPT in SYSTEM_PROMPT


# ============================================================================
# TOOL_DESCRIPTIONS 테스트
# ============================================================================

class TestToolDescriptions:
    """TOOL_DESCRIPTIONS 상수 테스트"""

    def test_tool_descriptions_not_empty(self):
        """의도: TOOL_DESCRIPTIONS가 비어있지 않은지 검증"""
        assert TOOL_DESCRIPTIONS is not None
        assert len(TOOL_DESCRIPTIONS) > 0

    def test_required_tools_exist(self):
        """의도: 필수 도구들이 정의되어 있는지 검증"""
        required_tools = [
            'get_dataframe_info',
            'get_column_statistics',
            'get_missing_values',
            'get_value_counts',
            'filter_dataframe',
            'sort_dataframe',
            'get_correlation',
            'predict_eclo',
        ]
        for tool_name in required_tools:
            assert tool_name in TOOL_DESCRIPTIONS, f"{tool_name} not found"

    def test_tool_has_required_fields(self):
        """의도: 각 도구 정의에 필수 필드가 있는지 검증"""
        for tool_name, info in TOOL_DESCRIPTIONS.items():
            assert 'category' in info, f"{tool_name} missing 'category'"
            assert 'description' in info, f"{tool_name} missing 'description'"
            assert 'params' in info, f"{tool_name} missing 'params'"

    def test_tool_categories_valid(self):
        """의도: 도구 카테고리가 유효한 값인지 검증"""
        valid_categories = [
            '데이터 정보', '데이터 조작', '통계 분석',
            '시계열', '지리', '데이터 품질', '예측'
        ]
        for tool_name, info in TOOL_DESCRIPTIONS.items():
            assert info['category'] in valid_categories, \
                f"{tool_name} has invalid category: {info['category']}"

    def test_predict_eclo_has_all_params(self):
        """의도: predict_eclo 도구가 11개 파라미터를 모두 정의하는지 검증"""
        eclo_params = TOOL_DESCRIPTIONS['predict_eclo']['params']
        assert len(eclo_params) == 11
        # 필수 파라미터 이름 확인
        param_str = ' '.join(eclo_params)
        required_params = [
            'weather', 'road_surface', 'road_type', 'accident_type',
            'time_period', 'district', 'day_of_week', 'accident_hour',
            'accident_year', 'accident_month', 'accident_day'
        ]
        for param in required_params:
            assert param in param_str, f"Missing param: {param}"


# ============================================================================
# detect_report_intent 테스트
# ============================================================================

class TestDetectReportIntent:
    """detect_report_intent 함수 테스트"""

    def test_detect_report_keyword(self):
        """의도: '보고서' 키워드 감지 검증"""
        assert detect_report_intent("보고서 만들어줘") is True
        assert detect_report_intent("보고서 작성해줘") is True

    def test_detect_report_english(self):
        """의도: 'report' 영어 키워드 감지 검증"""
        assert detect_report_intent("Generate a report") is True
        assert detect_report_intent("Create report please") is True

    def test_detect_markdown_keyword(self):
        """의도: '마크다운' 키워드 감지 검증"""
        assert detect_report_intent("마크다운으로 정리해줘") is True
        assert detect_report_intent("markdown 형식으로") is True

    def test_detect_document_keyword(self):
        """의도: '문서' 관련 키워드 감지 검증"""
        assert detect_report_intent("문서로 만들어줘") is True
        assert detect_report_intent("문서화해줘") is True

    def test_detect_summary_document(self):
        """의도: '요약 문서' 키워드 감지 검증"""
        assert detect_report_intent("분석 결과 요약 문서 작성") is True

    def test_no_report_intent(self):
        """의도: 보고서 의도가 없는 경우 False 반환 검증"""
        assert detect_report_intent("데이터 분석해줘") is False
        assert detect_report_intent("이 컬럼 통계 보여줘") is False
        assert detect_report_intent("안녕하세요") is False

    def test_case_insensitive(self):
        """의도: 대소문자 구분 없이 감지되는지 검증"""
        assert detect_report_intent("REPORT 만들어줘") is True
        assert detect_report_intent("Report please") is True
        assert detect_report_intent("MARKDOWN으로") is True

    def test_partial_match(self):
        """의도: 부분 일치로 감지되는지 검증"""
        assert detect_report_intent("리포트 생성 요청합니다") is True


# ============================================================================
# get_tool_list_markdown 테스트
# ============================================================================

class TestGetToolListMarkdown:
    """get_tool_list_markdown 함수 테스트"""

    def test_returns_string(self):
        """의도: 문자열 반환 검증"""
        result = get_tool_list_markdown()
        assert isinstance(result, str)

    def test_contains_markdown_table(self):
        """의도: 마크다운 테이블 형식이 포함되어 있는지 검증"""
        result = get_tool_list_markdown()
        assert '|' in result
        assert '도구명' in result
        assert '설명' in result
        assert '파라미터' in result

    def test_contains_all_categories(self):
        """의도: 모든 카테고리가 포함되어 있는지 검증"""
        result = get_tool_list_markdown()
        categories = set(info['category'] for info in TOOL_DESCRIPTIONS.values())
        for category in categories:
            assert category in result, f"Category '{category}' not in output"

    def test_contains_tool_names(self):
        """의도: 도구 이름이 백틱으로 감싸져 있는지 검증"""
        result = get_tool_list_markdown()
        for tool_name in TOOL_DESCRIPTIONS.keys():
            assert f"`{tool_name}`" in result, f"Tool '{tool_name}' not formatted correctly"

    def test_markdown_table_format(self):
        """의도: 올바른 마크다운 테이블 형식인지 검증"""
        result = get_tool_list_markdown()
        lines = result.strip().split('\n')
        # 테이블 헤더와 구분선이 있어야 함
        has_header = any('도구명' in line and '설명' in line for line in lines)
        has_separator = any(line.startswith('|') and '---' in line for line in lines)
        assert has_header
        assert has_separator


# ============================================================================
# 프롬프트 품질 테스트
# ============================================================================

class TestPromptQuality:
    """프롬프트 품질 테스트"""

    def test_no_placeholder_in_prompts(self):
        """의도: 프롬프트에 미완성 플레이스홀더가 없는지 검증"""
        prompts = [SYSTEM_PROMPT_BASE, ECLO_PREDICTION_PROMPT, REPORT_GENERATION_PROMPT]
        placeholders = ['TODO', 'FIXME', '{{', '}}', '[INSERT]', '<INSERT>']
        for prompt in prompts:
            for placeholder in placeholders:
                assert placeholder not in prompt, f"Found placeholder '{placeholder}' in prompt"

    def test_prompt_encoding(self):
        """의도: 프롬프트가 올바른 한글 인코딩인지 검증"""
        # 한글이 포함된 프롬프트들
        prompts = [SYSTEM_PROMPT_BASE, ECLO_PREDICTION_PROMPT, REPORT_GENERATION_PROMPT]
        for prompt in prompts:
            # 인코딩 테스트
            encoded = prompt.encode('utf-8')
            decoded = encoded.decode('utf-8')
            assert decoded == prompt

    def test_prompt_length_reasonable(self):
        """의도: 프롬프트 길이가 합리적인 범위인지 검증"""
        # 너무 짧거나 너무 길지 않아야 함
        assert len(SYSTEM_PROMPT_BASE) > 100
        assert len(SYSTEM_PROMPT_BASE) < 10000
        assert len(ECLO_PREDICTION_PROMPT) > 100
        assert len(ECLO_PREDICTION_PROMPT) < 10000
