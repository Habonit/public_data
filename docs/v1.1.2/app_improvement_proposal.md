# 대구 공공데이터 시각화 앱 개선 제안서 (v1.1.1 → v1.1.2)

**문서 버전**: v1.1.2
**작성일**: 2025-12-02
**참고 문서**: `docs/v1.1.2/notes.md`

---

## 1. 개요

본 문서는 대구 공공데이터 시각화 앱 v1.1.1의 현재 상태(AS-IS)와 v1.1.2에서 목표하는 개선 상태(TO-BE)를 비교 분석한다.

v1.1.2는 Tool Calling 기반 챗봇의 **사용자 경험(UX) 개선**에 초점을 맞춘다.

---

## 2. 기능별 AS-IS / TO-BE 비교

### 2.1 Tool Calling 실행 피드백

| 구분 | AS-IS (v1.1.1) | TO-BE (v1.1.2) |
|:-----|:---------------|:---------------|
| 실행 상태 표시 | "도구를 실행 중입니다..." 단순 텍스트 | 단계별 시각적 피드백 (색상, 아이콘) |
| 도구 정보 | 실행 중인 도구 정보 없음 | 도구명, 순번(1/3, 2/3) 표시 |
| 소요 시간 | 표시 없음 | 실시간 경과 시간 표시 |
| 진행 상황 | 불명확 | 단계별 진행 표시 (탐색 → 실행 → 완료) |

#### 2.1.1 Tool Calling 피드백 UI 예시

```
┌─────────────────────────────────────────────────────┐
│  🔍 도구 탐색 중... (2.3초)                          │
│  ├─ 1/2 get_column_statistics ✅ 완료               │
│  └─ 2/2 get_missing_values 🔄 실행 중...            │
└─────────────────────────────────────────────────────┘
```

#### 2.1.2 구현 방안

```python
# AS-IS
st.info("도구를 실행 중입니다...")

# TO-BE
with st.status("🔍 도구 탐색 중...", expanded=True) as status:
    st.write(f"1/{total_tools} `{tool_name}` 실행 중...")
    # 도구 실행
    status.update(label=f"✅ {tool_name} 완료", state="complete")
```

---

### 2.2 챗봇 응답 대기 UX

| 구분 | AS-IS (v1.1.1) | TO-BE (v1.1.2) |
|:-----|:---------------|:---------------|
| 로딩 표시 위치 | 전체 페이지 로딩 느낌 | 입력창 하단에 스피너 |
| 입력창 상태 | 응답 완료까지 비활성화 | 스피너와 함께 대기 상태 표시 |
| 사용자 경험 | 전체 화면 멈춤 느낌 | 부분적 로딩으로 자연스러운 대기 |

#### 2.2.1 구현 방안

```python
# AS-IS
response = create_chat_response(...)
st.write(response)

# TO-BE
with st.chat_message("assistant"):
    with st.spinner("답변 생성 중..."):
        response = create_chat_response(...)
    st.write(response)
```

---

### 2.3 데이터셋 전환 시 응답 시간

| 구분 | AS-IS (v1.1.1) | TO-BE (v1.1.2) |
|:-----|:---------------|:---------------|
| 데이터셋 전환 | 매번 전체 컨텍스트 재생성 | 데이터셋 정보 캐싱 활용 |
| 응답 속도 | 느림 (전체 재계산) | 빠름 (캐싱된 정보 재사용) |
| 메모리 사용 | 매번 새로 계산 | 캐싱으로 효율적 사용 |

#### 2.3.1 캐싱 전략

```python
# AS-IS
data_context = create_data_context(df, dataset_name)  # 매번 호출

# TO-BE
cache_key = f"context_{dataset_name}_{len(df)}"
if cache_key not in st.session_state:
    st.session_state[cache_key] = create_data_context(df, dataset_name)
data_context = st.session_state[cache_key]
```

---

### 2.4 토큰 사용량 표시

| 구분 | AS-IS (v1.1.1) | TO-BE (v1.1.2) |
|:-----|:---------------|:---------------|
| 토큰 표시 | 사이드바에 표시되나 업데이트 안됨 | 실시간 토큰 사용량 업데이트 |
| 입력/출력 구분 | 표시만 됨 | 실제 API 응답에서 추출하여 반영 |
| 누적 계산 | 미작동 | 세션 내 누적 토큰 정확히 계산 |

#### 2.4.1 토큰 추적 구현

```python
# AS-IS
# 토큰 정보 업데이트 없음

# TO-BE
response = client.messages.create(...)
st.session_state.chatbot['tokens']['input'] += response.usage.input_tokens
st.session_state.chatbot['tokens']['output'] += response.usage.output_tokens
st.session_state.chatbot['tokens']['total'] += (
    response.usage.input_tokens + response.usage.output_tokens
)
```

---

### 2.5 도구 미발견 시 폴백 처리

| 구분 | AS-IS (v1.1.1) | TO-BE (v1.1.2) |
|:-----|:---------------|:---------------|
| 도구 미발견 시 | "현재 앱이 답변할 수 없는 질문입니다." 고정 메시지 | LLM 폴백으로 관련 응답 생성 |
| 사용자 경험 | 단절감, 재질문 필요 | 불완전하더라도 관련 정보 제공 |
| 처리 방식 | 정적 에러 메시지 | 동적 LLM 응답 |

#### 2.5.1 폴백 로직 구현

```python
# AS-IS
if not tool_results:
    return "현재 앱이 답변할 수 없는 질문입니다."

# TO-BE
if not tool_results:
    # 도구 없이 LLM에게 직접 질문
    fallback_response = client.messages.create(
        model=model,
        system=f"데이터셋 정보: {data_context}\n질문에 가능한 범위 내에서 답변해주세요.",
        messages=[{"role": "user", "content": query}]
    )
    return fallback_response.content[0].text
```

---

### 2.6 추가 분석 도구 (신규)

| 구분 | AS-IS (v1.1.1) | TO-BE (v1.1.2) |
|:-----|:---------------|:---------------|
| 결측값 분석 | 결측값 개수만 제공 | 결측값 원인/패턴 분석 도구 추가 |
| 도구 개수 | 15개 | 20개 (+5개 추가) |

#### 2.6.1 추가 도구 목록

| 번호 | 도구명 | 설명 |
|:-----|:-------|:-----|
| 16 | `analyze_missing_pattern` | 결측값 패턴 분석 (MCAR, MAR, MNAR 추정) |
| 17 | `get_column_correlation_with_target` | 특정 타겟 컬럼과의 상관관계 분석 |
| 18 | `detect_data_types` | 컬럼별 실제 데이터 타입 추론 |
| 19 | `get_temporal_pattern` | 시간 관련 컬럼의 패턴 분석 |
| 20 | `summarize_categorical_distribution` | 범주형 컬럼 분포 요약 |

---

## 3. 코드 품질 개선

### 3.1 토큰 추적 미작동

| 위치 | 문제 | AS-IS (v1.1.1) | TO-BE (v1.1.2) | 심각도 |
|:-----|:-----|:---------------|:---------------|:-------|
| `app.py` | 토큰 미업데이트 | 토큰 변수 초기화만 됨 | API 응답에서 토큰 추출하여 업데이트 | 🔴 Error |

---

### 3.2 스트리밍 응답 시 토큰 추적

| 위치 | 문제 | AS-IS (v1.1.1) | TO-BE (v1.1.2) | 심각도 |
|:-----|:-----|:---------------|:---------------|:-------|
| `chatbot.py` | 스트리밍 시 usage 정보 없음 | `stream.text_stream` 사용 | `stream.get_final_message()` 로 usage 추출 | ⚠️ Warning |

#### 3.2.1 수정 코드

```python
# AS-IS
with client.messages.stream(...) as stream:
    for text in stream.text_stream:
        yield text

# TO-BE
with client.messages.stream(...) as stream:
    for text in stream.text_stream:
        yield text
    final_message = stream.get_final_message()
    # usage 정보 반환 또는 저장
    return final_message.usage
```

---

## 4. 변경 요약표

| 영역 | 변경 유형 | 내용 |
|:-----|:---------|:-----|
| Tool Calling UX | 🔧 개선 | 단계별 시각적 피드백, 도구명/순번/시간 표시 |
| 응답 대기 UX | 🔧 개선 | 입력창 하단 스피너로 부분 로딩 표시 |
| 데이터셋 전환 | 🔧 개선 | 컨텍스트 캐싱으로 응답 속도 향상 |
| 토큰 사용량 | 🐛 수정 | 실제 API 응답에서 토큰 추출하여 표시 |
| 도구 미발견 처리 | 🔧 개선 | LLM 폴백으로 동적 응답 생성 |
| 분석 도구 | ➕ 추가 | 5개 도구 추가 (결측값 패턴, 상관관계 등) |

---

## 5. 구현 우선순위

### 🔴 P0 - 버그 수정 (필수)

| 순위 | 항목 | 설명 |
|:-----|:-----|:-----|
| 1 | 토큰 사용량 표시 | API 응답에서 토큰 추출하여 사이드바 업데이트 |
| 2 | Claude 4.5 모델 확인 | 실제 사용 모델 검증 및 설정 확인 |

### 🟡 P1 - UX 개선 (중요)

| 순위 | 항목 | 설명 |
|:-----|:-----|:-----|
| 3 | Tool Calling 피드백 | st.status 활용 단계별 진행 표시 |
| 4 | 응답 대기 스피너 | 입력창 하단 부분 로딩 표시 |
| 5 | 도구 미발견 폴백 | LLM 폴백으로 동적 응답 생성 |

### 🟢 P2 - 기능 추가

| 순위 | 항목 | 설명 |
|:-----|:-----|:-----|
| 6 | 데이터셋 컨텍스트 캐싱 | 데이터셋 전환 시 응답 속도 향상 |
| 7 | 추가 분석 도구 (5개) | 결측값 패턴, 상관관계 분석 등 |

---

## 6. 예상 Tool Calling 피드백 UI

```
┌─────────────────────────────────────────────────────────────────┐
│  💬 데이터 질의응답                                              │
├─────────────────────────────────────────────────────────────────┤
│  [User] 도로노선번호가 결측값인 데이터의 특성을 분석해줘          │
├─────────────────────────────────────────────────────────────────┤
│  [Assistant]                                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 🔍 도구 탐색 중... (3.2초)                               │   │
│  │ ┌─ 1/3 get_missing_values ✅ 완료 (1.1초)               │   │
│  │ ├─ 2/3 filter_dataframe ✅ 완료 (0.8초)                 │   │
│  │ └─ 3/3 get_column_statistics 🔄 실행 중... (1.3초)      │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  분석 결과:                                                     │
│  도로노선번호가 결측값인 데이터는 총 1,234건으로...              │
└─────────────────────────────────────────────────────────────────┘
```

---

## 7. 다음 단계

1. **P0 구현**: 토큰 사용량 표시 수정, Claude 4.5 모델 검증
2. **P1 구현**: Tool Calling 피드백 UI, 응답 대기 스피너, 폴백 로직
3. **P2 구현**: 컨텍스트 캐싱, 추가 분석 도구 5개
4. **테스트**: 전체 기능 통합 테스트
5. **문서화**: 사용자 가이드 업데이트
