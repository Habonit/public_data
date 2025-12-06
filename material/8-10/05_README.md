# 예제 5: 확장 가능한 섹션 (Expanders)

## 학습 목표

- `st.expander()`를 사용한 컨텐츠 정리
- 기본 확장 상태 설정
- 중첩 expander 구조
- FAQ 및 상세 정보 표시에 활용

## 핵심 개념

### `st.expander()` 기본 사용법

```python
with st.expander("레이블", expanded=False):
    st.write("접었다 펼칠 수 있는 컨텐츠")
```

**매개변수:**
- `label`: expander의 제목
- `expanded`: 기본 상태 (True=펼침, False=접힘)

## 현재 앱에서의 사용

```python
# app.py:58-59 - 데이터 미리보기
with st.expander("📋 데이터 미리보기", expanded=False):
    st.dataframe(df.head(10), use_container_width=True)

# app.py:62-70 - 컬럼 정보
with st.expander("📊 컬럼 정보", expanded=False):
    st.dataframe(col_info_df, use_container_width=True)

# app.py:331-333 - 상세 통계
with st.expander("📊 상세 통계", expanded=False):
    stats_df = proximity_df.describe()
    st.dataframe(stats_df)
```

## 실행 방법

```bash
streamlit run 05_expanders.py
```

## 사용 사례

1. **긴 데이터 테이블** - 선택적으로 보기
2. **FAQ 섹션** - 질문/답변 정리
3. **상세 설명** - 요약과 상세 정보 분리
4. **디버그 정보** - 개발 중 로그 숨기기
