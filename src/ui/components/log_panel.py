import tkinter as tk
from tkinter import ttk
from typing import List
from ...config import Config

class LogPanel:
    """로그 패널"""
    
    def __init__(self, parent):
        self.parent = parent
        self.setup_ui()
    
    def setup_ui(self):
        """UI 구성"""
        log_frame = ttk.LabelFrame(self.parent, text="📝 실시간 로그", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 로그 텍스트 영역
        log_text_frame = ttk.Frame(log_frame)
        log_text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(log_text_frame, height=12, bg=Config.LOG_BG, fg=Config.LOG_FG,
                               font=('Courier New', 9), wrap=tk.WORD, state=tk.DISABLED)
        log_scrollbar = ttk.Scrollbar(log_text_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def update_logs(self, log_lines: List[str]):
        """로그 업데이트"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        
        for line in log_lines:
            self.log_text.insert(tk.END, line + "\n")
        
        self.log_text.config(state=tk.DISABLED)
        self.log_text.see(tk.END)