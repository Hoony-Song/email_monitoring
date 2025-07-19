import tkinter as tk
from tkinter import ttk
from ...models.settings import AppSettings

class MonitorPanel:
    """모니터링 패널"""
    
    def __init__(self, parent, settings: AppSettings, app):
        self.parent = parent
        self.settings = settings
        self.app = app
        
        self.setup_ui()
    
    def setup_ui(self):
        """UI 구성"""
        monitor_frame = ttk.LabelFrame(self.parent, text="⚙️ 모니터링 설정", padding="10")
        monitor_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # 모니터링 주기
        ttk.Label(monitor_frame, text="모니터링 주기(초):").pack(anchor=tk.W)
        self.interval_var = tk.IntVar(value=self.settings.monitor_settings.interval)
        interval_combo = ttk.Combobox(monitor_frame, textvariable=self.interval_var, 
                                     values=[3, 5, 10, 30], state="readonly")
        interval_combo.pack(fill=tk.X, pady=2)
        interval_combo.bind('<<ComboboxSelected>>', self.update_interval)
        
        # 유사도 임계값
        ttk.Label(monitor_frame, text="유사도 임계값:").pack(anchor=tk.W, pady=(10,0))
        self.similarity_var = tk.DoubleVar(value=self.settings.monitor_settings.similarity_threshold)
        self.similarity_scale = ttk.Scale(monitor_frame, from_=0.8, to=1.0, 
                                         variable=self.similarity_var, orient=tk.HORIZONTAL)
        self.similarity_scale.pack(fill=tk.X, pady=2)
        self.similarity_scale.configure(command=self.update_similarity)
        
        self.similarity_label = ttk.Label(monitor_frame, text=f"{self.similarity_var.get():.2f}")
        self.similarity_label.pack(anchor=tk.W)
        
        # 새로고침 설정
        self.refresh_var = tk.BooleanVar(value=self.settings.monitor_settings.refresh_enabled)
        ttk.Checkbutton(monitor_frame, text="새로고침 활성화(분)", 
                       variable=self.refresh_var,
                       command=self.update_refresh_enabled).pack(anchor=tk.W, pady=2)
        
        self.refresh_interval_var = tk.IntVar(value=self.settings.monitor_settings.refresh_interval)
        refresh_combo = ttk.Combobox(monitor_frame, textvariable=self.refresh_interval_var,
                                    values=[1, 5, 10, 30, 60], state="readonly")
        refresh_combo.pack(fill=tk.X, pady=2)
        refresh_combo.bind('<<ComboboxSelected>>', self.update_refresh_interval)
    
    def update_interval(self, event=None):
        """모니터링 주기 업데이트"""
        self.settings.monitor_settings.interval = self.interval_var.get()
    
    def update_similarity(self, value):
        """유사도 임계값 업데이트"""
        self.settings.monitor_settings.similarity_threshold = float(value)
        self.similarity_label.config(text=f"{float(value):.2f}")
    
    def update_refresh_enabled(self):
        """새로고침 활성화 업데이트"""
        self.settings.monitor_settings.refresh_enabled = self.refresh_var.get()
    
    def update_refresh_interval(self, event=None):
        """새로고침 주기 업데이트"""
        self.settings.monitor_settings.refresh_interval = self.refresh_interval_var.get()
    
    def load_settings(self):
        """설정 로드"""
        self.interval_var.set(self.settings.monitor_settings.interval)
        self.similarity_var.set(self.settings.monitor_settings.similarity_threshold)
        self.similarity_label.config(text=f"{self.settings.monitor_settings.similarity_threshold:.2f}")
        self.refresh_var.set(self.settings.monitor_settings.refresh_enabled)
        self.refresh_interval_var.set(self.settings.monitor_settings.refresh_interval)
