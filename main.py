import tkinter as tk
import os
import sys
import logging

# 프로젝트 루트를 Python path에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.app import EmailMonitorApp
from src.config import Config
from src.utils.tesseract_checker import check_tesseract_installation

def setup_logging():
    """로깅 설정"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('email_monitor.log'),
            logging.StreamHandler()
        ]
    )

def main():
    """메인 애플리케이션 실행"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Tesseract 설치 확인
        if not check_tesseract_installation():
            logger.error("Tesseract 또는 한글팩이 설치되지 않았습니다.")
            input("Enter 키를 눌러 종료...")
            return
        
        # 애플리케이션 시작
        root = tk.Tk()
        app = EmailMonitorApp(root)
        
        # 창 닫기 이벤트 처리
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        
        logger.info("애플리케이션 시작")
        root.mainloop()
        
    except Exception as e:
        logger.error(f"애플리케이션 실행 중 오류: {e}")
        input("Enter 키를 눌러 종료...")

if __name__ == "__main__":
    main()