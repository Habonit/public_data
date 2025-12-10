# 예제 8: 로딩 스피너

## 학습 목표
- `st.spinner()` 사용법
- 다단계 작업에 스피너 적용
- 프로그레스 바와 함께 사용

## 기본 사용법

```python
with st.spinner("처리 중..."):
    # 시간이 오래 걸리는 작업
    time.sleep(2)
    df = load_data()

st.success("완료!")
```

## 현재 앱에서의 사용

```python
# app.py:222-248
with st.spinner("데이터셋 로딩 중..."):
    for idx, name in enumerate(selected_names):
        df = load_dataset(available_datasets[name])
        # ...

# app.py:304-313
with st.spinner("근접성 계산 중..."):
    proximity_df = compute_proximity_stats(...)
```

## 실행 방법

```bash
streamlit run 08_spinner.py
```
