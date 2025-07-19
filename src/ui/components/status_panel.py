import tkinter as tk
from tkinter import ttk
from typing import Optional

class StatusPanel:
    """상태 패널"""
    
    def __init__(self, parent):
        self.parent = parent
        self.setup_ui()
    
    def setup_ui(self):
        """UI 구성"""
        status_frame = ttk.LabelFrame(self.parent, text="📊 상태 정보", padding="10")
        status_frame.pack(fill=tk.X, pady=5)
        
        # 상태 정보 그리드
        info_frame = ttk.Frame(status_frame)
        info_frame.pack(fill=tk.X)
        
        # 현재 상태
        self.status_label = ttk.Label(info_frame, text="현재 상태: 대기 중")
        self.status_label.grid(row=0, column=0, sticky=tk.W, padx=5)
        
        # 기준점 시간
        self.baseline_label = ttk.Label(info_frame, text="기준점 시간: 없음")
        self.baseline_label.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # 마지막 감지
        self.last_detection_label = ttk.Label(info_frame, text="마지막 감지: 없음")
        self.last_detection_label.grid(row=1, column=0, sticky=tk.W, padx=5)
        
        # 총 감지 수
        self.total_detections_label = ttk.Label(info_frame, text="총 감지 수: 0")
        self.total_detections_label.grid(row=1, column=1, sticky=tk.W, padx=5)
    
    def update_status(self, status: str, baseline_time: Optional[str] = None, 
                     last_detection: Optional[str] = None, total_detections: Optional[int] = None):
        """상태 업데이트"""
        self.status_label.config(text=f"현재 상태: {status}")
        
        if baseline_time is not None:
            self.baseline_label.config(text=f"기준점 시간: {baseline_time or '없음'}")
        
        if last_detection is not None:
            self.last_detection_label.config(text=f"마지막 감지: {last_detection}")
        
        if total_detections is not None:
            self.total_detections_label.config(text=f"총 감지 수: {total_detections}")
