# 준비 범위와 15분 점검
이 문서는 사전 준비용이며 공식 시험 규칙을 대신하지 않습니다.

| 우선순위 | 준비 항목 | 위치 |
|---|---|---|
| 1 | 분석·구현·수정·검증·최종 검토 프롬프트 | prompts/ |
| 1 | CSV 품질 검사, 조건 필터·그룹 집계 | tools/inspect_csv.py, tools/analyze_data.py |
| 1 | JSON 문법·필수 필드, API 점검 | tools/validate_json.py, tools/smoke_test.py |
| 2 | Excel 검사·PDF 텍스트 추출 | 기존 tools/inspect_excel.py, tools/extract_pdf.py |
| 2 | API·표·폼·그래프 웹 예제 | web/ |
| 2 | 계획·판단·검증·제출 기록 | templates/ |
| 3 | 시각화 | web의 기본 막대 그래프 |
| 3 | RAG, Embedding, MCP/설치형 Skill | 기본 구성 제외 |

RAG와 외부 MCP 연결은 기존 저장소의 외부 AI·개인 API 키·시험 자료 외부 전송 제한에 맞춰 포함하지 않았습니다. 실제 허용 범위와 필요성이 확인될 때만 별도로 준비합니다. TXT는 기본 편집기나 Python의 pathlib.Path.read_text로 읽을 수 있습니다. 문서 검색·OCR·임베딩 검색은 구현되어 있지 않습니다.

## 15분 사전 체험
1. 0~3분: 운영 안내에서 공개 저장소와 직접 만든 도구의 허용 여부를 확인합니다.
2. 3~6분: git clone --depth 1 https://github.com/jui-ced/kit.git 실행을 확인합니다.
3. 6~9분: README의 최소 점검 명령을 샘플 데이터로 실행합니다.
4. 9~12분: Codex가 실제 과제 README와 kit/AGENTS.md를 구분해 읽는지 확인합니다.
5. 12~15분: 웹이 필요한 경우 서버 포트 미리보기와 종료를 확인합니다.

다운로드나 설치가 안 되면 실제 오류를 기록하고 허용된 도구만으로 과제 환경에서 새로 구현합니다. 문제·결과물·시험 파일을 공개 저장소로 보내지 않습니다.
