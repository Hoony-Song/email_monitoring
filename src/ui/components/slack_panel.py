import tkinter as tk
from tkinter import ttk
from ...models.settings import AppSettings

class SlackPanel:
    """슬랙 패널"""
    
    def __init__(self, parent, settings: AppSettings, app):
        self.parent = parent
        self.settings = settings
        self.app = app
        
        self.setup_ui()
    
    def setup_ui(self):
        """UI 구성"""
        slack_frame = ttk.LabelFrame(self.parent, text="📢 슬랙 설정", padding="10")
        slack_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        # 웹훅 URL
        ttk.Label(slack_frame, text="웹훅 URL:").pack(anchor=tk.W)
        self.webhook_var = tk.StringVar(value=self.settings.slack_settings.webhook_url)
        self.webhook_entry = ttk.Entry(slack_frame, textvariable=self.webhook_var, width=40)
        self.webhook_entry.pack(fill=tk.X, pady=2)
        self.webhook_entry.bind('<KeyRelease>', self.update_webhook_url)
        
        # 채널
        ttk.Label(slack_frame, text="채널:").pack(anchor=tk.W)
        self.channel_var = tk.StringVar(value=self.settings.slack_settings.channel)
        self.channel_entry = ttk.Entry(slack_frame, textvariable=self.channel_var, width=40)
        self.channel_entry.pack(fill=tk.X, pady=2)
        self.channel_entry.bind('<KeyRelease>', self.update_channel)
        
        # 버튼들
        button_frame = ttk.Frame(slack_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="🧪 테스트", command=self.app.test_slack).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="🔄 초기화", command=self.reset_slack).pack(side=tk.LEFT, padx=2)
    
    def update_webhook_url(self, event=None):
        """웹훅 URL 업데이트"""
        self.settings.slack_settings.webhook_url = self.webhook_var.get()
        self.app.notification_service.slack_settings = self.settings.slack_settings
    
    def update_channel(self, event=None):
        """채널 업데이트"""
        self.settings.slack_settings.channel = self.channel_var.get()
        self.app.notification_service.slack_settings = self.settings.slack_settings
    
    def reset_slack(self):
        """슬랙 설정 초기화"""
        self.webhook_var.set("")
        self.channel_var.set("")
        self.settings.slack_settings.webhook_url = ""
        self.settings.slack_settings.channel = ""
        self.app.notification_service.slack_settings = self.settings.slack_settings
        self.app.add_log("슬랙 설정이 초기화되었습니다.")
    
    def load_settings(self):
        """설정 로드"""
        self.webhook_var.set(self.settings.slack_settings.webhook_url)
        self.channel_var.set(self.settings.slack_settings.channel)
