import threading
import time
import pyautogui
import logging
import re
from typing import Optional, Callable
from .ocr_engine import OCREngine
from ..models.settings import AppSettings

class MonitorService:
    """모니터링 서비스"""
    
    def __init__(self, settings: AppSettings, ocr_engine: OCREngine):
        self.settings = settings
        self.ocr_engine = ocr_engine
        self.logger = logging.getLogger(__name__)
        
        self.is_monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.refresh_thread: Optional[threading.Thread] = None
        
        self.previous_title_image = None
        self.previous_time_image = None
        self.baseline_time = None
        
        # 콜백 함수들
        self.on_detection_callback: Optional[Callable] = None
        self.on_log_callback: Optional[Callable] = None
    
    def set_callbacks(self, on_detection: Callable, on_log: Callable):
        """콜백 함수 설정"""
        self.on_detection_callback = on_detection
        self.on_log_callback = on_log
    
    def start_monitoring(self):
        """모니터링 시작"""
        if self.is_monitoring:
            return
        
        self.is_monitoring = True
        self._set_baseline()
        
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        if self.settings.monitor_settings.refresh_enabled:
            self.refresh_thread = threading.Thread(target=self._refresh_loop, daemon=True)
            self.refresh_thread.start()
        
        self._log("모니터링 시작")
    
    def stop_monitoring(self):
        """모니터링 중지"""
        self.is_monitoring = False
        self._log("모니터링 중지")
    
    def _set_baseline(self):
        """기준점 설정"""
        try:
            if not self.settings.time_area:
                return
            
            time_image = self.ocr_engine.capture_area(self.settings.time_area.to_tuple())
            if time_image is not None:
                time_text = self.ocr_engine.extract_text(time_image)
                if time_text:
                    self.baseline_time = time_text
                    self._log(f"기준점 설정: {self.baseline_time}")
        except Exception as e:
            self._log(f"기준점 설정 오류: {e}")
    
    def _monitor_loop(self):
        """모니터링 메인 루프"""
        while self.is_monitoring:
            try:
                self._log("유사도 감지 중...")
                
                # 현재 이미지 캡처
                title_image = self.ocr_engine.capture_area(self.settings.title_area.to_tuple())
                time_image = self.ocr_engine.capture_area(self.settings.time_area.to_tuple())
                
                if title_image is None or time_image is None:
                    continue
                
                # 변화 감지
                if self._detect_changes(title_image, time_image):
                    self._log("변화 감지 -> 검증 시작")
                    self._process_detection(title_image, time_image)
                
                # 이전 이미지 저장
                self.previous_title_image = title_image
                self.previous_time_image = time_image
                
                time.sleep(self.settings.monitor_settings.interval)
                
            except Exception as e:
                self._log(f"모니터링 오류: {e}")
                time.sleep(self.settings.monitor_settings.interval)
    
    def _detect_changes(self, title_image, time_image) -> bool:
        """변화 감지"""
        if self.previous_title_image is None or self.previous_time_image is None:
            return True
        
        title_similarity = self.ocr_engine.calculate_similarity(title_image, self.previous_title_image)
        time_similarity = self.ocr_engine.calculate_similarity(time_image, self.previous_time_image)
        
        threshold = self.settings.monitor_settings.similarity_threshold
        return title_similarity < threshold or time_similarity < threshold
    
    def _process_detection(self, title_image, time_image):
        """감지 처리"""
        title_text = self.ocr_engine.extract_text(title_image)
        time_text = self.ocr_engine.extract_text(time_image)
        
        self._log(f'제목: "{title_text}" | 시간: "{time_text}"')
        
        # 시간 중복 확인
        if time_text != self.baseline_time:
            # 필터링 확인
            if self._check_keyword_match(title_text):
                self._log("필터링 일치 -> 알림 발송")
                
                if self.on_detection_callback:
                    self.on_detection_callback(title_text, time_text)
                
                # 기준점 갱신
                self.baseline_time = time_text
            else:
                self._log("필터링 불일치 -> 패스")
        else:
            self._log("시간 중복 -> 패스")
    
    def _check_keyword_match(self, text: str) -> bool:
        """키워드 매칭 확인"""
        if not text or not self.settings.filter_settings.keywords:
            return False
        
        normalized_text = self._normalize_text(text)
        
        for keyword in self.settings.filter_settings.keywords:
            normalized_keyword = self._normalize_text(keyword)
            
            if self.settings.filter_settings.exact_match:
                if self.settings.filter_settings.case_sensitive:
                    if keyword == text:
                        return True
                else:
                    if normalized_keyword == normalized_text:
                        return True
            else:
                if self.settings.filter_settings.case_sensitive:
                    if keyword in text:
                        return True
                else:
                    if normalized_keyword in normalized_text:
                        return True
        
        return False
    
    def _normalize_text(self, text: str) -> str:
        """텍스트 정규화"""
        if not text:
            return ""
        
        normalized = text.lower()
        normalized = re.sub(r'\s+', ' ', normalized)
        return normalized.strip()
    
    def _refresh_loop(self):
        """새로고침 루프"""
        while self.is_monitoring and self.settings.monitor_settings.refresh_enabled:
            try:
                time.sleep(self.settings.monitor_settings.refresh_interval * 60)
                if self.is_monitoring:
                    pyautogui.press('f5')
                    self._log("새로고침 실행")
            except Exception as e:
                self._log(f"새로고침 오류: {e}")
    
    def _log(self, message: str):
        """로그 출력"""
        self.logger.info(message)
        if self.on_log_callback:
            self.on_log_callback(message)
