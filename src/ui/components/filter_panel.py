import tkinter as tk
from tkinter import ttk
from ...models.settings import AppSettings

class FilterPanel:
    """필터 패널"""
    
    def __init__(self, parent, settings: AppSettings, app):
        self.parent = parent
        self.settings = settings
        self.app = app
        
        self.setup_ui()
    
    def setup_ui(self):
        """UI 구성"""
        filter_frame = ttk.LabelFrame(self.parent, text="🔍 필터링 설정", padding="10")
        filter_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # 키워드 리스트
        list_frame = ttk.Frame(filter_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.keyword_listbox = tk.Listbox(list_frame, height=6)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.keyword_listbox.yview)
        self.keyword_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.keyword_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 키워드 입력
        self.keyword_entry = ttk.Entry(filter_frame)
        self.keyword_entry.pack(fill=tk.X, pady=2)
        self.keyword_entry.bind('<Return>', lambda e: self.add_keyword())
        
        # 버튼들
        button_frame = ttk.Frame(filter_frame)
        button_frame.pack(fill=tk.X, pady=2)
        
        ttk.Button(button_frame, text="➕ 추가", command=self.add_keyword).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="🗑️ 삭제", command=self.remove_keyword).pack(side=tk.LEFT, padx=2)
        
        # 옵션들
        self.exact_match_var = tk.BooleanVar(value=self.settings.filter_settings.exact_match)
        self.case_sensitive_var = tk.BooleanVar(value=self.settings.filter_settings.case_sensitive)
        
        ttk.Checkbutton(filter_frame, text="완전일치", variable=self.exact_match_var,
                       command=self.update_filter_settings).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(filter_frame, text="대소문자 구분", variable=self.case_sensitive_var,
                       command=self.update_filter_settings).pack(anchor=tk.W, pady=2)
    
    def add_keyword(self):
        """키워드 추가"""
        keyword = self.keyword_entry.get().strip()
        if keyword and keyword not in self.settings.filter_settings.keywords:
            self.settings.filter_settings.keywords.append(keyword)
            self.keyword_listbox.insert(tk.END, keyword)
            self.keyword_entry.delete(0, tk.END)
            self.app.add_log(f"키워드 추가: {keyword}")
    
    def remove_keyword(self):
        """키워드 제거"""
        selected = self.keyword_listbox.curselection()
        if selected:
            index = selected[0]
            keyword = self.settings.filter_settings.keywords.pop(index)
            self.keyword_listbox.delete(index)
            self.app.add_log(f"키워드 삭제: {keyword}")
    
    def update_filter_settings(self):
        """필터 설정 업데이트"""
        self.settings.filter_settings.exact_match = self.exact_match_var.get()
        self.settings.filter_settings.case_sensitive = self.case_sensitive_var.get()
    
    def load_settings(self):
        """설정 로드"""
        self.keyword_listbox.delete(0, tk.END)
        for keyword in self.settings.filter_settings.keywords:
            self.keyword_listbox.insert(tk.END, keyword)
        
        self.exact_match_var.set(self.settings.filter_settings.exact_match)
        self.case_sensitive_var.set(self.settings.filter_settings.case_sensitive)
