# 대구 공공데이터 시각화 앱 개선 제안서 (v1.0 → v1.1)

**문서 버전**: v1.1
**작성일**: 2025-12-01
**참고 문서**: `docs/v1.1/notes.md`

---

## 1. 개요

본 문서는 대구 공공데이터 시각화 앱 v1.0의 현재 상태(AS-IS)와 v1.1에서 목표하는 개선 상태(TO-BE)를 비교 분석한다.

---

## 2. 기능별 AS-IS / TO-BE 비교

### 2.1 데이터 로딩 방식

| 구분 | AS-IS (v1.0) | TO-BE (v1.1) |
|:-----|:-------------|:-------------|
| 로딩 방식 | `data/*.csv` 파일을 직접 읽어서 앱 구동 | CSV 파일 업로드 방식으로 전환 |
| 데이터 소스 | 서버 내 고정된 파일 경로 | 사용자가 직접 업로드 |
| 유연성 | 사전 정의된 7개 데이터셋만 사용 가능 | 사용자가 원하는 데이터셋 업로드 가능 |

---

### 2.2 성능 최적화

| 구분 | AS-IS (v1.0) | TO-BE (v1.1) |
|:-----|:-------------|:-------------|
| 데이터 읽기 | 상호작용마다 데이터를 다시 읽음 | `session_state`와 `cache`로 한 번만 읽기 |
| 로딩 속도 | 상호작용 시 로딩 지연 발생 | 업로드 후 상호작용해도 재로딩 없음 |
| 사용자 경험 | 느린 반응 속도 | 빠른 반응 속도 |

---

### 2.3 시각화 기능

| 구분 | AS-IS (v1.0) | TO-BE (v1.1) |
|:-----|:-------------|:-------------|
| 디자인 | 투박한 기본 스타일 | Plotly로 예쁜 색깔과 스타일 적용 |
| 차트 종류 | 히스토그램, bar chart만 제공 | 히스토그램, 박스플롯, KDE, 산점도 등 다양화 |
| 시각적 품질 | 단조로운 시각화 | 풍부하고 다채로운 시각화 |

---

### 2.4 지도 시각화

| 구분 | AS-IS (v1.0) | TO-BE (v1.1) |
|:-----|:-------------|:-------------|
| 포인트 제한 | 5,000개 샘플링 (암묵적) | 명시적 limit 설정으로 병목 방지 |
| 성능 | 대용량 데이터 시 지연 가능 | limit으로 안정적 렌더링 보장 |

---

### 2.5 탭 구조 및 명칭

| 구분 | AS-IS (v1.0) | TO-BE (v1.1) |
|:-----|:-------------|:-------------|
| 탭 개수 | 9개 탭 | 10개 탭 (데이터 질의응답 추가) |
| Train 탭 명칭 | "🚂 기차" (오역) | "📊 훈련 데이터" |
| Test 탭 명칭 | "📝 테스트" (모호) | "📋 테스트 데이터" |
| 신규 탭 | 없음 | "💬 데이터 질의응답" (챗봇) |

---

### 2.6 결측치 처리

| 구분 | AS-IS (v1.0) | TO-BE (v1.1) |
|:-----|:-------------|:-------------|
| 결측치 표시 | 컬럼별 결측률 테이블로만 표시 | 결측률 테이블 + 30% 이상 시 warning 알림 |
| 사용자 안내 | 수동으로 확인 필요 | 자동으로 주의가 필요한 컬럼 강조 |

---

### 2.7 교차 데이터 분석

| 구분 | AS-IS (v1.0) | TO-BE (v1.1) |
|:-----|:-------------|:-------------|
| 통합 지도 시각화 | 제공 | 유지 |
| 근접성 분석 | 거리 임계값별 분석 제공 | 제거 |
| 분포 히스토그램 | 근접성 결과 히스토그램 | 제거 |

---

### 2.8 프로젝트 개요 페이지

| 구분 | AS-IS (v1.0) | TO-BE (v1.1) |
|:-----|:-------------|:-------------|
| 역할 | 프로젝트 소개 및 사용법 안내 | 데이터셋 업로드 허브 + 소개 |
| 데이터 업로드 | 없음 | 각 탭별 데이터셋 업로드 UI 제공 |
| 업로드 현황 | 없음 | 파일명, 파일 크기 표시 |
| 탭 활성화 | 모든 탭 항상 활성화 | 해당 데이터 업로드 시에만 탭 활성화 |
| 미업로드 안내 | 없음 | 시각화 탭 접근 시 "업로드 먼저" 안내 |

---

### 2.9 챗봇 기능 (신규)

| 구분 | AS-IS (v1.0) | TO-BE (v1.1) |
|:-----|:-------------|:-------------|
| 챗봇 | 없음 | Anthropic 언어모델 기반 챗봇 추가 |
| 탭 위치 | - | "데이터 질의응답" 신규 탭 |
| 데이터 연동 | - | 업로드된 데이터셋만 질의 가능 |
| 데이터 선택 | - | select box로 질의할 데이터셋 선택 |

---

### 2.10 사이드바 기능 (신규)

| 구분 | AS-IS (v1.0) | TO-BE (v1.1) |
|:-----|:-------------|:-------------|
| API Key 입력 | 없음 | Anthropic API Key 입력 필드 |
| 모델 선택 | 없음 | select box로 모델 선택 |
| 토큰 사용량 | 없음 | 전체/입력/출력 토큰 표시 |
| 업로드 현황 | 없음 | 데이터셋별 업로드 상태 표시 |

---

## 3. 코드 품질 개선 (버그/Warning 수정)

### 3.1 Deprecated API 수정

| 위치 | AS-IS (v1.0) | TO-BE (v1.1) | 심각도 |
|:-----|:-------------|:-------------|:-------|
| `app.py:59,70,75` | `st.dataframe(..., width='stretch')` | `st.dataframe(..., use_container_width=True)` | ⚠️ Warning |
| `app.py:119,135` | `st.plotly_chart(fig, width='stretch')` | `st.plotly_chart(fig, use_container_width=True)` | ⚠️ Warning |

---

### 3.2 잠재적 에러 수정

| 위치 | 문제 | AS-IS (v1.0) | TO-BE (v1.1) | 심각도 |
|:-----|:-----|:-------------|:-------------|:-------|
| `app.py:54` | ZeroDivisionError 가능 | `sum(...) / len(info['missing_ratios'])` | 빈 dict 체크 추가 | 🔴 Error |
| `app.py:336` | 함수 내부 import | `import plotly.express as px` (함수 내) | 파일 상단으로 이동 | ⚠️ Warning |
| `visualizer.py:96` | Mutable default argument | `popup_cols: list[str] = []` | `popup_cols: list[str] | None = None` | ⚠️ Warning |
| `geo.py:126` | Mutable default argument | `thresholds: list[float] = [0.5, 1.0, 2.0]` | `thresholds: list[float] | None = None` | ⚠️ Warning |

---

### 3.3 성능 병목 개선

| 위치 | 문제 | AS-IS (v1.0) | TO-BE (v1.1) | 심각도 |
|:-----|:-----|:-------------|:-------------|:-------|
| `geo.py:155-176` | O(n*m) 이중 루프 | `iterrows()` 이중 순회 | numpy/scipy vectorized 연산 | 🟡 Performance |
| `visualizer.py:159,277` | DataFrame 순회 | `iterrows()` 사용 | vectorized 연산 또는 `itertuples()` | 🟡 Performance |
| `app.py` 전체 | session_state 미활용 | 매 상호작용마다 재계산 | `st.session_state`로 상태 유지 | 🟡 Performance |

---

### 3.4 에러 핸들링 강화

| 상황 | AS-IS (v1.0) | TO-BE (v1.1) |
|:-----|:-------------|:-------------|
| 숫자형 컬럼 없음 | 빈 selectbox 표시 | 안내 메시지 표시 |
| 범주형 컬럼 없음 | 빈 selectbox 표시 | 안내 메시지 표시 |
| 빈 DataFrame | 에러 발생 가능 | early return + 안내 메시지 |
| 좌표 컬럼 타입 오류 | 암묵적 실패 | 타입 검증 + 변환 시도 |
| 대용량 파일 업로드 | 메모리 부족 가능 | 파일 크기 제한 + 경고 |

---

### 3.5 코드 수정 상세

#### 3.5.1 `app.py:54` - ZeroDivisionError 방지

```python
# AS-IS
missing_pct = sum(info['missing_ratios'].values()) / len(info['missing_ratios']) * 100 if info['missing_ratios'] else 0

# TO-BE
if info['missing_ratios'] and len(info['missing_ratios']) > 0:
    missing_pct = sum(info['missing_ratios'].values()) / len(info['missing_ratios']) * 100
else:
    missing_pct = 0
```

#### 3.5.2 `visualizer.py:96` - Mutable Default Argument

```python
# AS-IS
def create_folium_map(
    df: pd.DataFrame,
    lat_col: str,
    lng_col: str,
    popup_cols: list[str] = [],  # 위험!
    ...
)

# TO-BE
def create_folium_map(
    df: pd.DataFrame,
    lat_col: str,
    lng_col: str,
    popup_cols: list[str] | None = None,
    ...
):
    if popup_cols is None:
        popup_cols = []
```

#### 3.5.3 Deprecated `width='stretch'`

```python
# AS-IS
st.dataframe(df.head(10), width='stretch')
st.plotly_chart(fig, width='stretch')

# TO-BE
st.dataframe(df.head(10), use_container_width=True)
st.plotly_chart(fig, use_container_width=True)
```

---

## 4. 변경 요약표

| 영역 | 변경 유형 | 내용 |
|:-----|:---------|:-----|
| 데이터 로딩 | 🔄 변경 | 파일 직접 읽기 → 업로드 방식 |
| 성능 | 🔧 개선 | session_state + cache 적용 |
| 시각화 | 🔧 개선 | Plotly 스타일 + 다양한 차트 추가 |
| 지도 | 🔧 개선 | 명시적 limit 설정 |
| 탭 명칭 | 🔄 변경 | 기차→훈련 데이터, 테스트→테스트 데이터 |
| 결측치 | ➕ 추가 | 30% 이상 warning 알림 |
| 교차 분석 | ➖ 제거 | 근접성 분석 제거, 통합 지도만 유지 |
| 프로젝트 개요 | 🔄 변경 | 데이터 업로드 허브로 전환 |
| 챗봇 | ➕ 추가 | Anthropic 기반 데이터 질의응답 |
| 사이드바 | ➕ 추가 | API 설정, 토큰 현황, 업로드 현황 |
| 코드 품질 | 🐛 수정 | Deprecated API, 잠재적 에러 수정 |

---

## 5. 구현 우선순위

### 🔴 P0 - 버그/Warning 수정 (즉시)

| 순위 | 항목 | 파일 | 설명 |
|:-----|:-----|:-----|:-----|
| 0-1 | ZeroDivisionError 수정 | `app.py:54` | 빈 dict 체크 |
| 0-2 | Deprecated API 수정 | `app.py` | `width='stretch'` → `use_container_width=True` |
| 0-3 | Mutable default 수정 | `visualizer.py`, `geo.py` | `[]` → `None` |
| 0-4 | Import 위치 수정 | `app.py:336` | 상단으로 이동 |

### 🔴 P1 - 핵심 변경 (필수)

| 순위 | 항목 | 설명 |
|:-----|:-----|:-----|
| 1 | 업로드 방식 전환 | 전체 앱 구조 변경의 기반 |
| 2 | session_state/cache 적용 | 성능 문제 해결 |
| 3 | 프로젝트 개요 → 업로드 허브 | 업로드 방식의 진입점 |

### 🟡 P2 - 기능 개선

| 순위 | 항목 | 설명 |
|:-----|:-----|:-----|
| 4 | 시각화 다양화 | 박스플롯, KDE, 산점도 추가 |
| 5 | 시각화 스타일 개선 | Plotly 색상/스타일 적용 |
| 6 | 결측치 warning | 30% 이상 컬럼 경고 |
| 7 | 탭 명칭 수정 | 기차→훈련, 테스트→테스트 데이터 |
| 8 | 근접성 분석 제거 | 교차 분석 단순화 |
| 9 | 성능 최적화 | iterrows → vectorized 연산 |

### 🟢 P3 - 신규 기능

| 순위 | 항목 | 설명 |
|:-----|:-----|:-----|
| 10 | 챗봇 탭 추가 | 데이터 질의응답 기능 |
| 11 | 사이드바 기능 | API 설정, 토큰/업로드 현황 |

---

## 6. 예상 탭 구조 (v1.1)

```
┌─────────────────────────────────────────────────────────────┐
│  사이드바                                                    │
│  ├─ API Key 입력                                            │
│  ├─ 모델 선택 (select box)                                  │
│  ├─ 토큰 사용량 (전체/입력/출력)                            │
│  └─ 데이터 업로드 현황                                      │
├─────────────────────────────────────────────────────────────┤
│  탭 구조                                                     │
│  1. 📊 프로젝트 개요 (업로드 허브)                          │
│  2. 🎥 CCTV                                                 │
│  3. 💡 보안등                                               │
│  4. 🏫 어린이 보호구역                                      │
│  5. 🅿️ 주차장                                               │
│  6. 🚗 사고                                                 │
│  7. 📊 훈련 데이터                                          │
│  8. 📋 테스트 데이터                                        │
│  9. 🔄 교차 데이터 분석 (통합 지도만)                       │
│ 10. 💬 데이터 질의응답 (챗봇)                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 7. 다음 단계

1. **P0 구현**: 버그/Warning 즉시 수정
2. **P1 구현**: 업로드 방식 전환 및 캐싱 구조 설계
3. **P2 구현**: 시각화 개선 및 UI 수정
4. **P3 구현**: 챗봇 및 사이드바 기능 추가
5. **테스트**: 전체 기능 통합 테스트
6. **문서화**: 사용자 가이드 업데이트
