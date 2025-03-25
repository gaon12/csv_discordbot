# 소개
본 저장소는 파이썬으로 작성된 디스코드 봇입니다. 기존에는 각 명령어들을 일일이 입력하고, 답변도 적어 놓아야 하기 때문에 어렵고 복잡했었어요. 물론 자유도는 높지만 말이죠.

이젠 단순히 질문과 답변하는 봇을 만들려면 이 봇을 사용하면 좋지 않을까요? 엄청 간단해요!

# 준비물
다음 준비물이 필요해요.
1. 디스코드 봇을 돌릴 PC가 필요합니다.
2. 디스코드 봇을 돌릴 PC에 파이썬3을 설치해야 합니다.
3. 질문과 답변이 담긴 CSV 파일이 필요해요.
4. 디스코드 봇 토큰값이 필요해요. [디스코드](https://discord.com)에 접속 후 로그인 한 다음, [디스코드 애플리케이션 페이지](https://discord.com/developers/applications)로 들어가 봇 토큰을 생성해 주세요. 생성한 토큰값을 `token.txt`에 저장해 주세요.
5. 디스코드 봇에 권한을 줘야 해요. **PRESENCE INTENT** 권한과 **MESSAGE CONTENT INTENT** 권한 스위치를 켜고, 저장해 주세요.

## CSV 파일 구조
CSV 파일은 다음과 같이 작성해 주세요.

> question, answer<br>
> "안녕?", "안녕하세요!"<br>
> "넌 누구야?", "저는 귀요미 가온이에요!"

헤더는 반드시 <code>question, answer</code> 이렇게 설정해야 합니다.  
또한 질문값과 답변값은 쌍따옴표로 묶어야 합니다. 이렇게 한 이유는 질문값이나 답변값에 콤마가 포함되어 있는 경우, 오작동할 수 있기 때문입니다.

파일 이름은 `qa_data.csv`로 저장해주세요.

## 봇의 작동 방식
본 봇은 질문과 답변을 담고 있는 CSV 파일을 읽어 사용자가 입력한 질문에 맞는 답변을 찾아서 디스코드 채팅창에 출력합니다.

### 봇 사용
1. 디스코드 봇에 질문을 보내면, 봇이 CSV 파일에서 해당 질문을 찾아 답변을 출력합니다.
2. 봇은 `!cmdname <question>` 형식으로 질문을 받습니다.

### 커스터마이징
봇의 기본 명령어와 출력 형식을 커스터마이징할 수 있습니다.

#### 1. **결과값을 인용문으로 출력하기**
그냥 텍스트로 답변을 받으려면 수정하지 않아도 되지만, 인용문으로 출력하기 원한다면 `39~45번째 줄`을 다음과 같이 수정하세요.

수정 전:
```python
@bot.command()
async def cmdname(ctx, *args):
    question = ' '.join(args)
    if question in qa_data:
        await ctx.send(qa_data[question])
    else:
        await ctx.send('Sorry, no answer values were found for the question you entered.')
```

수정 후:
```python
@bot.command()
async def cmdname(ctx, *args):
    question = ' '.join(args)
    if question in qa_data:
        answer = f"> {qa_data[question]}"  # 인용문 형식으로 변경
        await ctx.send(answer)
    else:
        await ctx.send('Sorry, no answer values were found for the question you entered.')
```

#### 2. **명령어 이름 수정**
기본값은 `cmdname`으로 되어있어요. 이 명령어 이름을 수정하려면, `40번째 줄`에 있는 `cmdname`을 원하는 명령어 이름으로 수정하면 돼요.

## 필요한 라이브러리 설치
필요한 라이브러리를 설치해야 해요. 명령 프롬프트나 터미널에 다음과 같이 입력해주세요.

```bash
pip install discord.py csv openpyxl xlrd watchdog
```

### 라이브러리 설명
- `discord.py`: 디스코드 봇을 위한 라이브러리.
- `csv`: CSV 파일을 읽고 쓰는 라이브러리.
- `openpyxl`, `xlrd`: XLSX, XLS 파일을 읽는 라이브러리.
- `watchdog`: 파일 변경 감지를 위한 라이브러리.

## 실행
디스코드 서버에 봇을 초대하고, 명령 프롬프트나 터미널에 다음과 같이 입력하면 봇이 작동해요.

```bash
python bot.py
```

## 명령어 형태
명령어는 다음과 같은 형태로 입력하면 돼요.
> `!cmdname <question>`

## 추가 기능
- **QA 데이터 업데이트**: 봇은 `qa_data.csv` 파일이 변경될 때마다 실시간으로 데이터를 갱신합니다.
- **Custom QA 파일**: 봇에 새로운 질문과 답변을 추가하면, 기존 `qa_data.csv` 파일의 복사본에 `_custom` 접미사를 붙여 저장됩니다. 이를 통해 사용자 정의 데이터 파일을 생성하고 관리할 수 있습니다.

## 라이선스
MIT 라이선스를 사용합니다.