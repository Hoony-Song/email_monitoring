import tkinter as tk
from tkinter import messagebox
import logging
from datetime import datetime
from typing import List

from .config import Config
from .models.settings import AppSettings
from .core.ocr_engine import OCREngine
from .core.monitor_service import MonitorService
from .services.notification_service import NotificationService
from .ui.main_window import MainWindow

class EmailMonitorApp:
    """메인 애플리케이션"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.logger = logging.getLogger(__name__)
        
        # 설정 로드
        self.settings = AppSettings.load(Config.SETTINGS_FILE)
        
        # 핵심 서비스 초기화
        self.ocr_engine = OCREngine()
        self.monitor_service = MonitorService(self.settings, self.ocr_engine)
        self.notification_service = NotificationService(self.settings.slack_settings)
        
        # 콜백 설정
        self.monitor_service.set_callbacks(
            on_detection=self.on_detection,
            on_log=self.on_log
        )
        
        # 상태 변수
        self.total_detections = 0
        self.last_detection_time = "없음"
        self.log_lines: List[str] = []
        
        # UI 초기화
        self.ui = MainWindow(root, self.settings, self)
        
        # 초기 로그
        self.add_log("프로그램이 시작되었습니다.")
    
    def on_detection(self, title_text: str, time_text: str):
        """감지 콜백"""
        self.notification_service.send_slack_notification(title_text, time_text)
        self.total_detections += 1
        self.last_detection_time = time_text
        self.ui.update_status_display(
            "모니터링 중",
            self.monitor_service.baseline_time,
            self.last_detection_time,
            self.total_detections
        )
    
    def on_log(self, message: str):
        """로그 콜백"""
        self.add_log(message)
    
    def add_log(self, message: str):
        """로그 추가"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        
        self.log_lines.append(log_message)
        
        if len(self.log_lines) > Config.MAX_LOG_LINES:
            self.log_lines.pop(0)
        
        self.root.after(0, self.ui.update_log_display, self.log_lines)
    
    def start_monitoring(self):
        """모니터링 시작"""
        if not self.settings.title_area or not self.settings.time_area:
            messagebox.showwarning("경고", "제목 영역과 시간 영역을 모두 설정해주세요.")
            return
        
        if not self.settings.filter_settings.keywords:
            messagebox.showwarning("경고", "최소 하나의 키워드를 입력해주세요.")
            return
        
        self.monitor_service.start_monitoring()
        self.ui.set_monitoring_state(True)
        self.ui.update_status_display("모니터링 중", None, None, None)
    
    def stop_monitoring(self):
        """모니터링 중지"""
        self.monitor_service.stop_monitoring()
        self.ui.set_monitoring_state(False)
        self.ui.update_status_display("대기 중", None, None, None)
    
    def save_settings(self):
        """설정 저장"""
        try:
            self.settings.save(Config.SETTINGS_FILE)
            messagebox.showinfo("성공", "설정이 저장되었습니다.")
            self.add_log("설정 저장 완료")
        except Exception as e:
            messagebox.showerror("오류", f"설정 저장 실패: {e}")
            self.add_log(f"설정 저장 오류: {e}")
    
    def test_slack(self):
        """슬랙 테스트"""
        if self.notification_service.test_slack_connection():
            messagebox.showinfo("성공", "슬랙 테스트 메시지가 전송되었습니다.")
            self.add_log("슬랙 테스트 성공")
        else:
            messagebox.showerror("실패", "슬랙 전송에 실패했습니다.")
            self.add_log("슬랙 테스트 실패")
    
    def on_closing(self):
        """애플리케이션 종료"""
        if self.monitor_service.is_monitoring:
            self.stop_monitoring()
        
        self.ui.cleanup()
        self.save_settings()
        self.root.destroy()