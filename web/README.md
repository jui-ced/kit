# 작은 API + 대시보드

추가 패키지·빌드·외부 CDN 없이 Python 표준 라이브러리로 실행합니다. 저장소 루트에서:

```bash
python web/simple-api-example/server.py --port 8000
```

내부 Browser 미리보기에서 해당 포트의 `/`를 엽니다. 로컬 PC에서는 `http://127.0.0.1:8000/`입니다. 서버 터미널을 유지하고 종료는 Ctrl+C입니다.

- `GET /health` → `{"ok": true}`
- `GET /api/summary?values=10,20,30` → 개수 3, 평균 20, 최소 10, 최대 30
- 빈 입력·문자·NaN·무한대 → HTTP 400 JSON 오류
- 없는 경로 → HTTP 404
- API 점검 도구는 HTTP(S)의 localhost·127.0.0.1·[::1]만 허용하며 프록시와 리다이렉트를 차단합니다. 서버 바인딩 주소 0.0.0.0 대신 아래처럼 127.0.0.1로 요청하세요. 다른 내부 호스트·외부 주소는 지원하지 않습니다.
- 화면: 입력 폼, 버튼, 결과 표, 절댓값 막대 그래프. 오류 시 이전 결과를 비웁니다.

```bash
python tools/smoke_test.py http://127.0.0.1:8000/health --required ok
python tools/smoke_test.py "http://127.0.0.1:8000/api/summary?values=10,20,30" --required count mean min max
python tools/smoke_test.py "http://127.0.0.1:8000/api/summary?values=bad" --status 400 --required error
```

인증·DB·파일 업로드·운영 배포 기능은 없는 내부 미리보기 예제입니다. 숫자는 부동소수점 근삿값이며 정밀한 금액 계산에는 Decimal 등을 적용하세요. 핵심 입력 검증과 API 처리 부분만 현재 과제에 맞게 재사용하세요.
