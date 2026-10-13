# 프롬프트 공방

막연하게 쓴 요청을 복사해서 바로 쓸 수 있는 AI 프롬프트로 다듬는 웹 서비스입니다. [기획서](./기획서.md)와 [작업 체크리스트](./작업-체크리스트.md)를 함께 제공합니다.

웹 기술이 처음이라면 [초보자 설명서](./초보자-설명서.md)에서 파일 역할과 버튼을 누른 뒤의 흐름을 볼 수 있습니다.

**GitHub 저장소:** https://github.com/daguri2963/prompt-workshop

**배포 URL:** 배포 완료 후 여기에 기록

## 기능

- 홈 / 프롬프트 다듬기 / 이용 방법, 총 3개 메뉴 섹션
- 초안·활용 목적·결과 형식을 입력하면 개선된 프롬프트와 이유 표시
- 결과 복사 버튼
- 빈 입력, 잘못된 요청, API 오류, 시간 초과 안내
- 휴대폰과 데스크톱에 맞춘 화면

## 기술과 구조

| 역할 | 기술 | 위치 |
| --- | --- | --- |
| 내용 | HTML | `index.html` |
| 모양과 반응형 화면 | CSS | `css/style.css` |
| 버튼·입력·결과 표시 | JavaScript | `js/app.js` |
| 비밀 키를 사용하는 AI 요청 | Python Vercel Function | `api/improve.py` |
| Python 패키지 | pip | `requirements.txt` |

흐름: **사용자 입력 → JavaScript `fetch('/api/improve')` → Python 함수 → 코디세이 OpenAI 호환 API → JSON 응답 → 화면 표시**. 브라우저에는 API 키가 전달되지 않습니다.

## 로컬 실행

Python이 설치되어 있다면 이 폴더에서 다음 명령으로 정적 화면을 볼 수 있습니다.

```powershell
python -m http.server 8000
```

브라우저에서 `http://localhost:8000`을 여세요. 이 방법은 **화면 확인용**입니다. `/api/improve`는 Vercel Python Function이므로 로컬 정적 서버에서는 동작하지 않습니다. 실제 AI 기능은 Vercel 배포 후 시험합니다.

## Vercel 배포

1. 이 프로젝트를 **새 GitHub 저장소**에 올립니다.
2. [Vercel](https://vercel.com/new)에서 GitHub 저장소를 가져옵니다. 프레임워크는 `Other`를 선택하고 루트 디렉터리는 프로젝트 루트로 둡니다.
3. 배포 전에 프로젝트의 **Settings → Environment Variables**에서 `CODYSSEY_API_KEY`를 등록합니다. 코디세이에서 받은 가상 키를 **Vercel 설정 화면에 직접** 붙여 넣으세요. 채팅, 코드, 문서, 스크린샷에는 키를 넣지 않습니다.
4. 필요할 때 `CODYSSEY_MODEL`로 모델을 바꿀 수 있습니다. 코디세이 예시와 같은 기본값은 `gpt-5-mini`입니다.
5. 배포 후 공개 URL에서 초안을 입력해 결과가 나오는지 확인합니다. 환경 변수 변경 후에는 새 배포가 필요합니다.

Vercel은 `.python-version`의 Python 3.12와 `requirements.txt`의 패키지를 사용합니다. 로컬 컴퓨터의 Python 3.15 설치와 별개입니다.

## 비용과 보안

코디세이 키의 사용 가능 모델, 사용 한도, 공개 서비스 허용 범위를 확인하세요. 공개 서비스는 누구나 요청할 수 있습니다. 서버는 입력 길이와 응답 시간을 제한하고, 브라우저에서 버튼 연속 클릭을 막습니다. `CODYSSEY_API_KEY`를 GitHub에 올리지 마세요. `.env` 파일은 Git에서 제외됩니다.

현재 키 하나는 코디세이 API에만 연결됩니다. 같은 서비스의 다른 모델은 코디세이 전체 장애에 대한 백업이 되지 않습니다. 독립적인 백업 제공자를 사용하려면 별도의 API 키와 사용 허가가 필요합니다.

## 제출 자료

- 공개 Vercel URL
- GitHub 저장소
- 이 README
- [서비스 기획서](./기획서.md)
- `evidence/`의 데스크톱·모바일·AI 작동 화면과 AI 코딩 도구 사용 증빙 (`local-` 이미지는 배포 전 미리보기이며, 배포 후 공개 URL에서 다시 촬영)
