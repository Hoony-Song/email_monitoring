import os
import pytesseract
import logging
from ..config import Config

def check_tesseract_installation() -> bool:
    """Tesseract 설치 확인"""
    logger = logging.getLogger(__name__)
    
    # Tesseract 경로 찾기
    tesseract_found = False
    for path in Config.TESSERACT_PATHS:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            tesseract_found = True
            logger.info(f"✅ Tesseract 경로: {path}")
            break
    
    if not tesseract_found:
        logger.error("❌ Tesseract을 찾을 수 없습니다!")
        return False
    
    # 한글 언어팩 확인
    try:
        languages = pytesseract.get_languages()
        logger.info(f"설치된 언어팩: {languages}")
        
        if 'kor' in languages:
            logger.info("✅ 한글 언어팩이 설치되어 있습니다.")
            return True
        else:
            logger.error("❌ 한글 언어팩이 설치되어 있지 않습니다.")
            return False
            
    except Exception as e:
        logger.error(f"Tesseract 확인 중 오류: {e}")
        return False