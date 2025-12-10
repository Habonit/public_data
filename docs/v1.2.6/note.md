- v1.2.4에서 고치려는 문제 수정 x / 문제 지적을 잘못한 게 아닌가,  / 이 부분은 개발자가 직접 해결해야 할 거 같은데
소스의 어느 부분을 확인하면 될지 AI 에게 문서화 요청. => 해결 완료했으며 데이터 자체의 문제를 방어코딩을 통해 해결 -=> 해결 되었는지 확인해달라고 요청청

- 
문제 원인: execute_tool 함수(1178줄)에서 도구를 호출할 때 config를 tool_input에 병합하여 전달합니다:

  return tool_func.invoke({**tool_input, "config": config})

  하지만 @tool 데코레이터로 정의된 LangChain 도구는 config 파라미터를 tool_input dict에서 추출하지 않습니다.
  LangChain의 @tool 데코레이터는 RunnableConfig를 별도의 키워드 인자로 받거나 invoke(input, config=config) 형태로
  받아야 합니다.

  흐름 분석:

  1. app.py: stream_chat_response_with_tools(df=df) 호출
  2. chatbot.py: execute_tool(tool_name, tool_input, df) 호출
  3. tools.py: tool_func.invoke({**tool_input, "config": config})
     └─ 문제: config가 input dict에 들어가지만,
        @tool 데코레이터가 이를 RunnableConfig로 인식 못함
  4. get_sample_rows: config=None (기본값 사용됨)
  5. get_dataframe_from_config(None) → KeyError 발생

  결론: Legacy execute_tool 함수에서 LangChain @tool로 정의된 도구에 config를 전달하는 방식이 호환되지 않습니다.
  config가 None으로 전달되어 "현재 활성화된 데이터셋이 없습니다" 오류가 발생합니다.

● 전체 분석 결과

  문제 요약

  근본 원인: execute_tool 함수(1178줄)에서 LangChain @tool 데코레이터 도구 호출 시 config를 input dict에 병합하여
  전달:

  return tool_func.invoke({**tool_input, "config": config})

  LangChain의 @tool 데코레이터는 config를 input dict의 키가 아닌 별도 인자로 받아야 합니다:

  # 올바른 방식
  return tool_func.invoke(tool_input, config=config)

  ---
  영향받는 도구 목록 (22개 전체)

  | 줄    | 도구명                                | config 파라미터                   | 영향     |
  |------|------------------------------------|-------------------------------|--------|
  | 46   | get_dataframe_info                 | config: RunnableConfig (필수)   | ❌ 영향받음 |
  | 73   | get_column_statistics              | config: RunnableConfig (필수)   | ❌ 영향받음 |
  | 113  | get_missing_values                 | config: RunnableConfig (필수)   | ❌ 영향받음 |
  | 140  | get_value_counts                   | config: RunnableConfig = None | ❌ 영향받음 |
  | 166  | filter_dataframe                   | config: RunnableConfig (필수)   | ❌ 영향받음 |
  | 215  | sort_dataframe                     | config: RunnableConfig = None | ❌ 영향받음 |
  | 248  | get_correlation                    | config: RunnableConfig = None | ❌ 영향받음 |
  | 281  | group_by_aggregate                 | config: RunnableConfig (필수)   | ❌ 영향받음 |
  | 327  | get_unique_values                  | config: RunnableConfig (필수)   | ❌ 영향받음 |
  | 355  | get_date_range                     | config: RunnableConfig (필수)   | ❌ 영향받음 |
  | 392  | get_outliers                       | config: RunnableConfig = None | ❌ 영향받음 |
  | 441  | get_sample_rows                    | config: RunnableConfig = None | ❌ 영향받음 |
  | 481  | calculate_percentile               | config: RunnableConfig (필수)   | ❌ 영향받음 |
  | 514  | get_geo_bounds                     | config: RunnableConfig (필수)   | ❌ 영향받음 |
  | 554  | cross_tabulation                   | config: RunnableConfig = None | ❌ 영향받음 |
  | 594  | analyze_missing_pattern            | config: RunnableConfig (필수)   | ❌ 영향받음 |
  | 664  | get_column_correlation_with_target | config: RunnableConfig (필수)   | ❌ 영향받음 |
  | 717  | detect_data_types                  | config: RunnableConfig (필수)   | ❌ 영향받음 |
  | 794  | get_temporal_pattern               | config: RunnableConfig (필수)   | ❌ 영향받음 |
  | 854  | summarize_categorical_distribution | config: RunnableConfig (필수)   | ❌ 영향받음 |
  | 912  | predict_eclo                       | config: RunnableConfig (필수)   | ❌ 영향받음 |
  | 1004 | predict_eclo_batch                 | config: RunnableConfig (필수)   | ❌ 영향받음 |

  ---
  결론

  모든 22개 도구가 동일한 문제의 영향을 받습니다. Legacy execute_tool 함수를 통해 호출되면 config가 제대로
  전달되지 않아 "현재 활성화된 데이터셋이 없습니다" 오류가 발생합니다.

  해결 방법: execute_tool 함수의 1178줄을 수정해야 합니다:

   # AS-IS (문제)
  return tool_func.invoke({**tool_input, "config": config})

  # TO-BE (해결)
  return tool_func.invoke(tool_input, config=config)

  위의 해결 책이 맞는지 점검하고 맞다면 이를 통해 해결하고 툴콜링이 모두 다 되는지 테스트까지 진행하기.

- 보고서 작성 시 마크다운으로 다운로드하는 기능을 삭제하고 AI의 모든 대답에 각각 복사 버튼이 있어서 그걸 누르면 마크다운 형태로 대답이 복사되는 형태

