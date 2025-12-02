# v1.1.2 개선사항
- 도구를 사용하게 될 때에 아래와 같은 로그가 잘 표시되고 있습니다. 그런데 

✅ 도구 실행 완료 (0.1초)

🔄 1/3 analyze_missing_pattern 실행 중...

✅ 1/3 analyze_missing_pattern 완료 (0.02초)

🔄 2/3 get_missing_values 실행 중...

✅ 2/3 get_missing_values 완료 (0.00초)

🔄 3/3 get_sample_rows 실행 중...

✅ 3/3 get_sample_rows 완료 (0.00초)

✅ 도구 실행 완료 (0.1초)

🔄 1/1 filter_dataframe 실행 중...

✅ 1/1 filter_dataframe 완료 (0.00)  
위와 같은 내용 아래로 언어모델의  답변이 붙는 게 아아니라 도구 상태값 위에 답변이 생성되어서 도구 실행 중간 상태값이 채팅 밑으로 밀림


- 프로젝트 개요에서 주요 기능, 사용방법 삭제 시스템 구조, 데이터분석 기초 개념, 분석 가이드 질문, 교차 데이터 분석의 중요성 삭제 

- 탭 중에서 교차 데이터 분석 탭 삭제 