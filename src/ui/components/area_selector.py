import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageGrab
import re
from typing import Optional, Tuple
from ...models.settings import AppSettings, AreaSettings

class AreaSelector:
    """영역 선택 컴포넌트"""
    
    def __init__(self, parent, settings: AppSettings, app):
        self.parent = parent
        self.settings = settings
        self.app = app
        
        self.is_selecting = False
        self.overlay_window = None
        self.selection_overlay = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """UI 구성"""
        area_frame = ttk.LabelFrame(self.parent, text="🎯 영역 설정", padding="10")
        area_frame.pack(fill=tk.X, pady=5)
        
        # 제목 영역
        title_frame = ttk.Frame(area_frame)
        title_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(title_frame, text="제목 영역:").pack(side=tk.LEFT)
        ttk.Button(title_frame, text="영역 선택", 
                  command=lambda: self.select_area("title")).pack(side=tk.LEFT, padx=5)
        self.title_coord_label = ttk.Label(title_frame, text="(x1: 0, y1: 0, x2: 0, y2: 0)")
        self.title_coord_label.pack(side=tk.LEFT, padx=5)
        
        # 시간 영역
        time_frame = ttk.Frame(area_frame)
        time_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(time_frame, text="시간 영역:").pack(side=tk.LEFT)
        ttk.Button(time_frame, text="영역 선택", 
                  command=lambda: self.select_area("time")).pack(side=tk.LEFT, padx=5)
        self.time_coord_label = ttk.Label(time_frame, text="(x1: 0, y1: 0, x2: 0, y2: 0)")
        self.time_coord_label.pack(side=tk.LEFT, padx=5)
        
        # 시각화 토글
        viz_frame = ttk.Frame(area_frame)
        viz_frame.pack(fill=tk.X, pady=5)
        
        self.visualization_var = tk.BooleanVar(value=self.settings.area_visualization)
        ttk.Checkbutton(viz_frame, text="감지 영역 표시", 
                       variable=self.visualization_var,
                       command=self.toggle_visualization).pack(side=tk.LEFT)
        
        ttk.Label(viz_frame, text="🟥 제목 영역", foreground="red").pack(side=tk.LEFT, padx=10)
        ttk.Label(viz_frame, text="🟦 시간 영역", foreground="blue").pack(side=tk.LEFT, padx=5)
    
    def select_area(self, area_type: str):
        """영역 선택"""
        self.is_selecting = True
        self.area_type = area_type
        self.app.add_log(f"{area_type} 영역 선택을 시작합니다.")
        
        # 메인 윈도우 숨기기
        self.app.root.withdraw()
        
        # 전체 화면 캡처
        screenshot = ImageGrab.grab()
        
        # 선택 오버레이 생성
        self.selection_overlay = tk.Toplevel()
        self.selection_overlay.attributes('-fullscreen', True)
        self.selection_overlay.attributes('-alpha', 0.3)
        self.selection_overlay.configure(bg='black')
        
        # 캔버스 생성
        canvas = tk.Canvas(self.selection_overlay, highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        # 스크린샷 표시
        self.canvas_image = ImageTk.PhotoImage(screenshot)
        canvas.create_image(0, 0, anchor=tk.NW, image=self.canvas_image)
        
        # 선택 변수
        self.start_x = self.start_y = 0
        self.rect_id = None
        self.canvas = canvas
        
        # 이벤트 바인딩
        canvas.bind("<Button-1>", self.on_mouse_down)
        canvas.bind("<B1-Motion>", self.on_mouse_drag)
        canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        canvas.bind("<Escape>", self.cancel_selection)
        canvas.focus_set()
    
    def on_mouse_down(self, event):
        """마우스 다운"""
        self.start_x = event.x
        self.start_y = event.y
    
    def on_mouse_drag(self, event):
        """마우스 드래그"""
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        
        color = 'red' if self.area_type == 'title' else 'blue'
        self.rect_id = self.canvas.create_rectangle(
            self.start_x, self.start_y, event.x, event.y,
            outline=color, width=3
        )
    
    def on_mouse_up(self, event):
        """마우스 업"""
        end_x = event.x
        end_y = event.y
        
        # 좌표 정규화
        x1 = min(self.start_x, end_x)
        y1 = min(self.start_y, end_y)
        x2 = max(self.start_x, end_x)
        y2 = max(self.start_y, end_y)
        
        # 설정 저장
        area_settings = AreaSettings(x1, y1, x2, y2)
        if self.area_type == 'title':
            self.settings.title_area = area_settings
        else:
            self.settings.time_area = area_settings
        
        self.app.add_log(f"{self.area_type} 영역 설정: ({x1}, {y1}, {x2}, {y2})")
        self.finish_selection()
    
    def cancel_selection(self, event=None):
        """선택 취소"""
        self.app.add_log("영역 선택이 취소되었습니다.")
        self.finish_selection()
    
    def finish_selection(self):
        """선택 완료"""
        if self.selection_overlay:
            self.selection_overlay.destroy()
        self.app.root.deiconify()
        self.is_selecting = False
        self.load_settings()
    
    def toggle_visualization(self):
        """시각화 토글"""
        self.settings.area_visualization = self.visualization_var.get()
        if self.settings.area_visualization:
            self.show_overlay()
        else:
            self.hide_overlay()
    
    def show_overlay(self):
        """오버레이 표시"""
        if not self.settings.title_area and not self.settings.time_area:
            self.visualization_var.set(False)
            messagebox.showwarning("경고", "먼저 영역을 설정해주세요.")
            return
        
        self.overlay_window = tk.Toplevel(self.app.root)
        self.overlay_window.attributes('-fullscreen', True)
        self.overlay_window.attributes('-alpha', 0.3)
        self.overlay_window.attributes('-topmost', True)
        self.overlay_window.configure(bg='black')
        self.overlay_window.wm_attributes('-transparentcolor', 'black')
        
        canvas = tk.Canvas(self.overlay_window, highlightthickness=0, bg='black')
        canvas.pack(fill=tk.BOTH, expand=True)
        
        if self.settings.title_area:
            coords = self.settings.title_area.to_tuple()
            canvas.create_rectangle(*coords, outline='red', width=3, fill='')
        
        if self.settings.time_area:
            coords = self.settings.time_area.to_tuple()
            canvas.create_rectangle(*coords, outline='blue', width=3, fill='')
    
    def hide_overlay(self):
        """오버레이 숨기기"""
        if self.overlay_window:
            self.overlay_window.destroy()
            self.overlay_window = None
    
    def load_settings(self):
        """설정 로드"""
        if self.settings.title_area:
            coords = self.settings.title_area.to_tuple()
            self.title_coord_label.config(text=f"(x1: {coords[0]}, y1: {coords[1]}, x2: {coords[2]}, y2: {coords[3]})")
        
        if self.settings.time_area:
            coords = self.settings.time_area.to_tuple()
            self.time_coord_label.config(text=f"(x1: {coords[0]}, y1: {coords[1]}, x2: {coords[2]}, y2: {coords[3]})")
        
        self.visualization_var.set(self.settings.area_visualization)
        if self.settings.area_visualization:
            self.show_overlay()
    
    def cleanup(self):
        """정리"""
        self.hide_overlay()