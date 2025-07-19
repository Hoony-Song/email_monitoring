import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageGrab
import pytesseract
import re
import logging
from typing import List, Tuple, Optional
from datetime import datetime

class OCREngine:
    """OCR 처리 엔진"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def capture_area(self, area: Tuple[int, int, int, int]) -> Optional[np.ndarray]:
        """화면 영역 캡처"""
        try:
            x1, y1, x2, y2 = area
            screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            return np.array(screenshot)
        except Exception as e:
            self.logger.error(f"영역 캡처 오류: {e}")
            return None
    
    def preprocess_image(self, pil_image: Image.Image) -> Image.Image:
        """이미지 전처리"""
        try:
            # 크기 확대
            width, height = pil_image.size
            scale_factor = max(4, 300 / width)
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            pil_image = pil_image.resize((new_width, new_height), Image.LANCZOS)
            
            # 그레이스케일 변환
            gray_image = pil_image.convert('L')
            
            # 가우시안 블러
            img_array = np.array(gray_image)
            blurred = cv2.GaussianBlur(img_array, (1, 1), 0)
            
            # 적응형 임계값
            adaptive_thresh = cv2.adaptiveThreshold(
                blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY, 11, 2
            )
            
            # 모폴로지 연산
            kernel = np.ones((1, 1), np.uint8)
            morphed = cv2.morphologyEx(adaptive_thresh, cv2.MORPH_CLOSE, kernel)
            
            return Image.fromarray(morphed)
            
        except Exception as e:
            self.logger.error(f"이미지 전처리 오류: {e}")
            return pil_image
    
    def extract_text(self, image: np.ndarray) -> str:
        """이미지에서 텍스트 추출"""
        try:
            if isinstance(image, np.ndarray):
                pil_image = Image.fromarray(image)
            else:
                pil_image = image
            
            text_results = []
            
            # 다양한 OCR 방식 시도
            ocr_methods = [
                ('원본', lambda img: pytesseract.image_to_string(img, lang='kor+eng')),
                ('전처리', lambda img: pytesseract.image_to_string(self.preprocess_image(img), lang='kor+eng')),
                ('한글전용', lambda img: pytesseract.image_to_string(img, lang='kor')),
                ('영어전용', lambda img: pytesseract.image_to_string(img, lang='eng')),
                ('PSM8', lambda img: pytesseract.image_to_string(img, lang='kor+eng', config='--psm 8')),
                ('확대', lambda img: pytesseract.image_to_string(
                    img.resize((img.width * 3, img.height * 3), Image.LANCZOS), lang='kor+eng'
                ))
            ]
            
            for method_name, method_func in ocr_methods:
                try:
                    result = method_func(pil_image)
                    cleaned = self._clean_text(result)
                    text_results.append((method_name, cleaned))
                    self.logger.debug(f"OCR [{method_name}]: '{cleaned}'")
                except Exception as e:
                    self.logger.debug(f"OCR [{method_name}] 실패: {e}")
            
            # 한글 포함 결과 우선 선택
            return self._select_best_result(text_results)
            
        except Exception as e:
            self.logger.error(f"OCR 처리 오류: {e}")
            return ""
    
    def _clean_text(self, text: str) -> str:
        """텍스트 정리"""
        if not text:
            return ""
        
        # 개행 문자 제거 및 공백 정리
        cleaned = re.sub(r'\s+', ' ', text.strip())
        
        # 불필요한 특수문자 제거
        cleaned = re.sub(r'[|]', '', cleaned)
        
        # 연속된 공백 제거
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        return cleaned.strip()
    
    def _select_best_result(self, results: List[Tuple[str, str]]) -> str:
        """최적 결과 선택"""
        if not results:
            return ""
        
        # 한글 포함 결과 찾기
        korean_results = []
        for method, result in results:
            if re.search(r'[가-힣]', result):
                korean_results.append((method, result, len(result)))
        
        if korean_results:
            best_korean = max(korean_results, key=lambda x: x[2])
            self.logger.info(f"최종 선택 [한글우선-{best_korean[0]}]: '{best_korean[1]}'")
            return best_korean[1]
        else:
            best_result = max(results, key=lambda x: len(x[1]))
            self.logger.info(f"최종 선택 [길이우선-{best_result[0]}]: '{best_result[1]}'")
            return best_result[1]
    
    def calculate_similarity(self, img1: np.ndarray, img2: np.ndarray) -> float:
        """이미지 유사도 계산"""
        try:
            gray1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
            gray2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
            
            if gray1.shape != gray2.shape:
                gray2 = cv2.resize(gray2, (gray1.shape[1], gray1.shape[0]))
            
            result = cv2.matchTemplate(gray1, gray2, cv2.TM_CCOEFF_NORMED)
            return max(0, result[0][0])
            
        except Exception as e:
            self.logger.error(f"유사도 계산 오류: {e}")
            return 0