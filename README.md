# kit

공개 자료를 허용하는 작업 환경에서 사용하는 작은 로컬 도구와 한국어 작업 템플릿입니다. 완성 답안이나 외부 AI 연결 기능은 없습니다. 시험 README와 최신 운영 안내가 항상 우선합니다.

## 시험 환경에서 가져오기

```bash
git clone https://github.com/jui-ced/kit.git
```

제공된 Codex에 다음처럼 요청합니다.

> 시험 README와 필수 제출 조건을 먼저 읽어줘. kit/AGENTS.md도 읽고 시험 규칙과 충돌하지 않는 원칙을 적용해줘. kit/README.md에서 필요한 도구만 골라 사용하고, 결과를 직접 검증해줘. 문제·자료·결과물을 외부로 전송하거나 Push하지 마.

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

## 출처와 범위

코드와 템플릿은 이 저장소를 위해 작성되었습니다. 실제 시험 문제·제공 파일·답안은 포함하지 않습니다. 의존 패키지는 각각의 라이선스를 따릅니다. AGENTS.md는 일반 작업 지침이며 설치형 Skill이나 에이전트 하네스는 포함하지 않습니다.
