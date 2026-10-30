# kit

공개 자료를 허용하는 작업 환경에서 사용하는 작은 로컬 도구와 한국어 작업 템플릿입니다. 완성 답안이나 외부 AI 연결 기능은 없습니다. 시험 README와 최신 운영 안내가 항상 우선합니다.

## 시험 환경에서 가져오기

```bash
git clone --depth 1 https://github.com/jui-ced/kit.git
```

제공된 Codex에 다음처럼 요청합니다.

> 시험 README를 먼저 읽고 kit/AGENTS.md도 확인해줘. 시험 규칙과 충돌하지 않는 원칙을 적용하고, kit의 도구 중 필요한 것만 사용해줘. 중요한 기능을 만들거나 실행할 때에는 목적과 선택 이유를 먼저 짧게 설명하고, 이후 실제 결과·검증 상태·남은 문제·다음 단계를 알려줘. 주요 결정은 작업 공간 안의 판단 기록에도 남겨줘. 문제·자료·결과물을 외부로 전송하거나 Push하지 마.

### 처음 사용하는 순서

1. 시험 작업 공간의 터미널에서 위 git clone 명령을 실행합니다. 이미 kit 폴더가 있다면 중복 다운로드 전에 내용을 확인합니다.
2. 시험 작업 공간에서 제공된 Codex를 열고 위 요청을 입력합니다. 이미 Codex를 사용 중이면 같은 대화에서 요청해도 됩니다.
3. Codex가 시험 요구사항과 사용할 도구·선택 이유를 설명하는지 확인합니다. 시험 작업 공간 전체 대신 kit 폴더만 과제로 오인하지 않도록 시험 README 경로를 알려줍니다.
4. CSV는 inspect_csv.py, Excel은 inspect_excel.py, PDF는 extract_pdf.py 중 필요한 것만 실행합니다. 아래 실행 예시의 입력 경로는 실제 제공 파일 경로로 바꿉니다. 필요한 패키지가 이미 있으면 다시 설치하지 않습니다.
5. 중요한 작업 전후의 설명을 확인하고, 이해되지 않는 선택은 구현 단계에서 질문합니다. 판단 기록에는 실제 검증 결과와 한계를 남깁니다.
6. 제출 전에는 입력 → 처리 → 출력 흐름, 선택 이유, 검증 결과, 남은 한계를 본인 말로 설명해봅니다. 후속 서술형에서는 AI나 복사·붙여넣기를 사용하지 않습니다.

진행 설명 예시(실제 수행 결과가 아닌 형식 예시):

> 다음 작업: CSV의 빈칸과 중복을 확인하겠습니다. 집계 결과가 왜곡될 수 있어 원본을 바꾸기 전에 상태를 확인합니다.
>
> 작업 후: 검사 결과를 확인했습니다. 원본은 수정하지 않았으며, 발견한 문제와 처리 방안을 판단 기록에 정리했습니다. 처리 방안을 적용한 뒤 집계 결과를 검증하겠습니다.

하위 폴더의 AGENTS.md가 작업 공간 전체에 자동 적용된다고 가정하지 마세요. 본 저장소는 결과 통지 전까지 공개 상태로 유지해야 합니다. 공개 여부만으로 모든 활용이 허용되는 것은 아니며 외부 결과물로 전체 답안을 대체하면 안 됩니다.

## 실행 (Python 3.10 이상, 저장소 루트 기준)

CSV 도구는 추가 패키지가 필요 없습니다.

```bash
cd kit
python tools/inspect_csv.py examples/sample.csv
python tools/inspect_csv.py /path/to/data.csv --encoding cp949
```

샘플 예상 결과: 데이터 5행, 중복 1행, value 빈칸 1개, 숫자로 읽을 수 있는 value 3개(10,30,30), NULL은 문자열로 보존됩니다. 통계는 숫자로 해석 가능한 값만 대상으로 합니다. 원본은 수정하지 않습니다. 기본 인코딩 탐지는 휴리스틱이므로 이상하면 --encoding을 지정하세요. 대용량 CSV는 전체 메모리 로딩에 주의하세요.

Excel/PDF가 필요할 때만 의존성을 설치합니다. 제공 환경에 이미 있으면 생략합니다.

```bash
python -m pip install -r requirements.txt
python tools/inspect_excel.py /path/to/book.xlsx --sample 5
python tools/extract_pdf.py /path/to/manual.pdf
```

- Excel: 시트·크기·첫 행·샘플을 보여줍니다. 첫 행이 항상 헤더인 것은 아닙니다. 수식 계산과 구형 .xls는 지원하지 않습니다.
- PDF: 페이지 구분을 유지해 텍스트를 출력합니다. OCR은 없으며 표의 읽기 순서가 깨질 수 있으니 원본을 확인하세요. 암호가 필요한 PDF는 지원하지 않습니다.
- 출력에는 원본 샘플이 포함될 수 있습니다. 외부 공유하지 마세요. 모든 처리는 로컬에서 수행됩니다.

## 예제 및 검증

```bash
python examples/make_samples.py
python tools/inspect_excel.py examples/sample.xlsx
python tools/extract_pdf.py examples/sample.pdf
python -m unittest discover -s tests -v
```

make_samples.py는 합성 데이터만 사용하며 기존 샘플 파일을 덮어쓰지 않습니다. Excel 예제는 Data/Notes 2개 시트, PDF 예제는 2페이지(둘째 페이지는 텍스트 없음)입니다.

## 템플릿

- templates/plan.md: 필수 조건, 자료 확인, 우선순위
- templates/decisions.md: 선택 이유, 근거, 실제 검증, 외부 코드 출처
- templates/submission.md: 실행법, 충족 조건, 한계, 제출 점검
- templates/test_report.md: 정상·예외·경계 입력의 기대/실제 결과와 미실행 기록

필요한 템플릿만 작업 공간에 복사하고 실제 시험의 파일명·양식을 따르세요. 빈 표나 예시를 완료 기록으로 제출하지 마세요.

## 180분 추천 흐름 (공식 시간 배분 아님)

0~15분 요구사항 → 15~30분 질문·계획 → 30~110분 구현 → 110~145분 검증 → 145~170분 설명·한계 정리 → 마지막 10분 제출.

후속 서술형은 AI·복사 붙여넣기 없이 직접 답변합니다. 구현 중부터 선택 이유, 바꾼 부분, 검증 결과, 한계를 이해하세요. 최신 공지의 종료 시각과 화면 타이머가 우선합니다.

## 웹 IDE 요령

- codex 실행 후 /status, /model로 제공 환경의 모델·권한을 확인합니다.
- 승인 대기와 실행 중을 구분하고 같은 요청을 반복하지 않습니다.
- 서버는 0.0.0.0 바인딩, 실제 포트·경로로 내부 Browser에서 확인합니다. 서버 터미널은 유지합니다.
- 같은 파일을 에디터와 AI가 동시에 수정하면 충돌 내용을 비교합니다.
- 사용법·제출 절차는 Cofa Helper, 업무 맥락은 실무자 에이전트, 장애는 문제 신고를 이용합니다.
- 외부 AI·개인 API 키·Computer Use·Git Push·제한 우회는 사용하지 않습니다. 외부 MCP로 시험 자료를 보내지 않습니다.

## 추가된 빠른 도구

기존 `tools/`, `templates/` 경로를 유지합니다. 제안된 `python/`, `documents/`와 역할이 같으며 중복 폴더를 만들지 않았습니다. 전체 준비 범위와 15분 점검은 [PREPARATION.md](PREPARATION.md)를 참고하세요.

### 최소 점검 명령

저장소 루트에서 실행합니다. 아래 도구는 표준 라이브러리만 사용합니다.

```bash
python tools/inspect_csv.py examples/sample.csv
python tools/analyze_data.py examples/sample.csv --value value --group status
python tools/analyze_data.py examples/sample.csv --value value --where status=ok
python tools/validate_json.py examples/sample.json --each --required id status
python -m unittest discover -s tests -v
```

- CSV 집계: JSON 배열 출력. `ok` 그룹은 3행, 평균 약 23.3333, 최솟값 10, 최댓값 30입니다. 빈칸은 `missing`, NULL·NaN·무한대 등 숫자가 아닌 값은 `invalid`로 셉니다. 원본과 중복은 보존합니다. `--where COLUMN=VALUE`는 문자열 정확 일치이며 `--encoding cp949`를 지정할 수 있습니다. 빈 파일·중복 헤더·열 개수 불일치는 오류입니다. 헤더만 있거나 필터 결과가 없으면 빈 배열입니다. 통계는 유효한 숫자만 대상으로 하며 해당 값들을 메모리에 저장합니다.
- JSON 검증: 문법, 중복 키, 비표준 NaN/Infinity, 필수 필드 누락/null을 확인합니다. `--each`는 배열의 모든 객체를 검사합니다. 샘플의 id/status 검사는 3개 통과하며 value를 필수로 지정하면 null 때문에 실패합니다. 빈 배열은 0개 검사로 통과합니다. 빈 문자열·자료형·중첩 필드·JSON Schema 검증은 포함하지 않습니다.
- API 점검: `python tools/smoke_test.py URL --status 200 --required ok`. HTTP 상태와 최상위 JSON 필드 존재/non-null을 확인합니다. 값의 의미까지 검증하지 않으며 시간 제한 기본값은 5초입니다. 명시한 URL에 GET 요청하므로 허용된 내부 API에만 사용하세요.
- 위 세 도구는 성공 시 종료 코드 0, 검증 실패·읽기 오류 시 1, 잘못된 명령 인자 시 2입니다.
- Excel/PDF 패키지가 없으면 해당 테스트 2개는 **skipped**로 표시됩니다. 통과로 간주하지 마세요. 선택 의존성을 설치한 뒤 전체 테스트를 실행하면 함께 검증합니다.

### 프롬프트와 웹 예제

`prompts/01_analyze_requirements.md` → `02_implementation.md` → 필요시 `03_debugging.md` → `04_verification.md` → `05_final_review.md` 순서로 필요한 내용을 복사합니다. 대괄호 자리에는 실제 단계·명령·오류를 적습니다.

웹이 필요한 경우 [web/README.md](web/README.md)의 명령으로 API와 대시보드를 함께 실행합니다. 외부 패키지·CDN 없이 폼·버튼·표·막대 그래프를 제공합니다.

## 출처 고지

코드와 템플릿은 이 저장소를 위해 작성되었습니다. 실제 시험 문제·제공 파일·답안은 포함하지 않습니다. 의존 패키지는 각각의 라이선스를 따릅니다. AGENTS.md는 일반 작업 지침이며 설치형 Skill이나 에이전트 하네스는 포함하지 않습니다.
