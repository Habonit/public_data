# 예제 11: 고급 통합

## 학습 목표
- 모든 기능을 통합한 완전한 앱 구조
- 사이드바 필터링
- 다중 탭 대시보드
- 데이터 다운로드 기능

## 주요 패턴

### 사이드바 필터
```python
st.sidebar.header("필터")
date_range = st.sidebar.date_input("날짜")
selected = st.sidebar.multiselect("선택", options)
```

### 탭 기반 대시보드
```python
tab1, tab2, tab3 = st.tabs(["개요", "분석", "지도"])

with tab1:
    # 개요 컨텐츠

with tab2:
    # 분석 컨텐츠
```

## 실행 방법

```bash
streamlit run 11_advanced_integration.py
```

## 현재 앱과의 연관성

이 예제는 현재 앱(app.py)의 축소판입니다:
- 필터링 (multiselect)
- 탭 구조
- 데이터-차트-지도 통합
