import os
from pathlib import Path

class Config:
    """애플리케이션 설정"""
    
    # 애플리케이션 정보
    APP_NAME = "메일 모니터링 프로그램"
    APP_VERSION = "v2.0"
    
    # 파일 경로
    BASE_DIR = Path(__file__).parent.parent
    SETTINGS_FILE = BASE_DIR / "email_monitor_settings.json"
    LOG_FILE = BASE_DIR / "email_monitor.log"
    
    # Tesseract 경로
    TESSERACT_PATHS = [
        "./tesseract/tesseract.exe",
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
    ]
    
    # UI 설정
    WINDOW_SIZE = "900x700"
    WINDOW_BG = "#f0f2f5"
    LOG_BG = "#1e1e1e"
    LOG_FG = "#00ff41"
    
    # 모니터링 설정
    DEFAULT_MONITOR_INTERVAL = 5
    DEFAULT_SIMILARITY_THRESHOLD = 0.95
    MAX_LOG_LINES = 100
    
    # OCR 설정
    OCR_LANGUAGES = ['kor+eng', 'kor', 'eng']
    OCR_CONFIGS = {
        'default': '--oem 3 --psm 6',
        'single_word': '--psm 8',
        'korean_optimized': '--oem 3 --psm 6 -l kor'
    }