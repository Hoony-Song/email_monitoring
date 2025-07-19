import tkinter as tk
from tkinter import ttk
from typing import List, Optional
from ..config import Config
from ..models.settings import AppSettings
from .components.area_selector import AreaSelector
from .components.filter_panel import FilterPanel
from .components.slack_panel import SlackPanel
from .components.monitor_panel import MonitorPanel
from .components.control_panel import ControlPanel
from .components.log_panel import LogPanel
from .components.status_panel import StatusPanel

class MainWindow:
    """메인 윈도우"""
    
    def __init__(self, root: tk.Tk, settings: AppSettings, app):
        self.root = root
        self.settings = settings
        self.app = app
        
        self.setup_window()
        self.setup_ui()
        self.load_settings_to_ui()
    
    def setup_window(self):
        """윈도우 설정"""
        self.root.title(f"{Config.APP_NAME} {Config.APP_VERSION}")
        self.root.geometry(Config.WINDOW_SIZE)
        self.root.configure(bg=Config.WINDOW_BG)
    
    def setup_ui(self):
        """UI 구성"""
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 스크롤 가능한 캔버스
        canvas = tk.Canvas(main_frame, bg=Config.WINDOW_BG)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # UI 컴포넌트들
        self.area_selector = AreaSelector(scrollable_frame, self.settings, self.app)
        self.status_panel = StatusPanel(scrollable_frame)
        
        # 설정 패널들 (좌우 배치)
        settings_frame = ttk.Frame(scrollable_frame)
        settings_frame.pack(fill=tk.X, pady=5)
        
        self.filter_panel = FilterPanel(settings_frame, self.settings, self.app)
        self.slack_panel = SlackPanel(settings_frame, self.settings, self.app)
        
        # 제어 패널들 (좌우 배치)
        control_frame = ttk.Frame(scrollable_frame)
        control_frame.pack(fill=tk.X, pady=5)
        
        self.monitor_panel = MonitorPanel(control_frame, self.settings, self.app)
        self.control_panel = ControlPanel(control_frame, self.settings, self.app)
        
        # 로그 패널
        self.log_panel = LogPanel(scrollable_frame)
        
        # 스크롤바 패킹
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def load_settings_to_ui(self):
        """설정을 UI에 로드"""
        self.area_selector.load_settings()
        self.filter_panel.load_settings()
        self.slack_panel.load_settings()
        self.monitor_panel.load_settings()
    
    def set_monitoring_state(self, is_monitoring: bool):
        """모니터링 상태 설정"""
        self.control_panel.set_monitoring_state(is_monitoring)
    
    def update_status_display(self, status: str, baseline_time: Optional[str] = None, 
                             last_detection: Optional[str] = None, total_detections: Optional[int] = None):
        """상태 디스플레이 업데이트"""
        self.status_panel.update_status(status, baseline_time, last_detection, total_detections)
    
    def update_log_display(self, log_lines: List[str]):
        """로그 디스플레이 업데이트"""
        self.log_panel.update_logs(log_lines)
    
    def cleanup(self):
        """정리"""
        self.area_selector.cleanup()