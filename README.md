# 해당 코드는 Claude AI 를 통해 바이브 코딩으로 작성한 프로그램 입니다 

## 🚀 실행 방법

### 개발 환경
```bash
# 의존성 설치
pip install -r requirements.txt

# 아래 링크에서 Tesseract-OCR 설치 
https://github.com/tesseract-ocr/tesseract

#  아래 링크에서 한글 언어팩 다운로드후 C:\Program Files\Tesseract-OCR\tessdata\kor.traineddata 경로에 배치 
https://github.com/tesseract-ocr/tessdata/raw/main/kor.traineddata

# 프로그램 실행
python main.py
```

### 패키지 설치
```bash
# 개발 모드 패키지 설치
pip install -e .

# 명령어로 실행
email-monitor
```

### EXE 빌드
```bash
# PyInstaller로 빌드
pyinstaller --onefile --noconsole --name="메일모니터링" main.py
```


