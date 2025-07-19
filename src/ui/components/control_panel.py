import tkinter as tk
from tkinter import ttk
from ...models.settings import AppSettings

class ControlPanel:
    """제어 패널"""
    
    def __init__(self, parent, settings: AppSettings, app):
        self.parent = parent
        self.settings = settings
        self.app = app
        
        self.setup_ui()
    
    def setup_ui(self):
        """UI 구성"""
        control_frame = ttk.LabelFrame(self.parent, text="🎮 제어", padding="10")
        control_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        # 시작/중지 버튼
        self.start_button = ttk.Button(control_frame, text="▶️ 시작", command=self.app.start_monitoring)
        self.start_button.pack(fill=tk.X, pady=2)
        
        self.stop_button = ttk.Button(control_frame, text="⏹️ 중지", command=self.app.stop_monitoring, state=tk.DISABLED)
        self.stop_button.pack(fill=tk.X, pady=2)
        
        # 설정 버튼
        ttk.Button(control_frame, text="💾 설정 저장", command=self.app.save_settings).pack(fill=tk.X, pady=2)
    
    def set_monitoring_state(self, is_monitoring: bool):
        """모니터링 상태 설정"""
        if is_monitoring:
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
        else:
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
