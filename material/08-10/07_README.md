# 예제 7: 상태 메시지

## 학습 목표
- 4가지 상태 메시지 사용법
- 폼 검증에 메시지 활용
- 에러 처리와 사용자 피드백

## 핵심 메시지

```python
st.success("작업 완료!")    # 초록색
st.info("정보입니다")        # 파란색
st.warning("주의하세요")     # 노란색
st.error("오류 발생!")       # 빨간색
```

## 현재 앱에서의 사용

```python
# app.py:37-38 - warning
st.warning(f"⚠️ {dataset_display_name} 데이터 파일을 찾을 수 없습니다.")

# app.py:41-42 - error
st.error(f"❌ {dataset_display_name} 로딩 오류: {str(e)}")

# app.py:315 - success
st.success("✅ 근접성 분석 완료!")

# app.py:264 - info
st.info("💡 지도 우측 상단의 레이어 컨트롤을 사용하여...")
```
