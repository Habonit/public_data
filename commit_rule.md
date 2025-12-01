# Commit Message Convention

## 구조
```
[tag] title

description
```

---

## Tag 종류

| Tag | 사용 시점 |
|-----|----------|
| `feat` | 새로운 기능 추가 |
| `fix` | 버그 수정 |
| `refactor` | 코드 구조 개선 (기능 변경 없음) |
| `docs` | 문서 추가/수정 |
| `test` | 테스트 코드 추가/수정 |
| `chore` | 빌드, CI/CD, 패키지 설정 등 |
| `style` | 코드 포맷팅 (로직 변경 없음) |
| `hotfix` | 프로덕션 긴급 수정 |

---

## Title 작성 규칙

- 50자 이내
- 동사로 마침침 (추가, 수정, 제거, 개선 등)
- 마침표 없이 종료

---

## Description 작성 규칙

- 왜 변경했는지 (Why)
- 어떻게 해결했는지 (How)

---

## 예시
```
[feat] 사용자 인증 API 추가

JWT 기반 로그인 구현. access/refresh token 발급 방식 적용.

```