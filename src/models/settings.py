from dataclasses import dataclass, field
from typing import List, Optional, Tuple
import json
from pathlib import Path

@dataclass
class AreaSettings:
    """영역 설정"""
    x1: int = 0
    y1: int = 0
    x2: int = 0
    y2: int = 0
    
    def to_tuple(self) -> Tuple[int, int, int, int]:
        return (self.x1, self.y1, self.x2, self.y2)
    
    @classmethod
    def from_tuple(cls, coords: Tuple[int, int, int, int]) -> 'AreaSettings':
        return cls(*coords)

@dataclass
class FilterSettings:
    """필터링 설정"""
    keywords: List[str] = field(default_factory=list)
    exact_match: bool = False
    case_sensitive: bool = False

@dataclass
class SlackSettings:
    """슬랙 설정"""
    webhook_url: str = ""
    channel: str = ""

@dataclass
class MonitorSettings:
    """모니터링 설정"""
    interval: int = 5
    similarity_threshold: float = 0.95
    refresh_enabled: bool = False
    refresh_interval: int = 5

@dataclass
class AppSettings:
    """전체 애플리케이션 설정"""
    title_area: Optional[AreaSettings] = None
    time_area: Optional[AreaSettings] = None
    filter_settings: FilterSettings = field(default_factory=FilterSettings)
    slack_settings: SlackSettings = field(default_factory=SlackSettings)
    monitor_settings: MonitorSettings = field(default_factory=MonitorSettings)
    area_visualization: bool = False
    
    def save(self, file_path: Path):
        """설정 저장"""
        data = {
            'title_area': self.title_area.to_tuple() if self.title_area else None,
            'time_area': self.time_area.to_tuple() if self.time_area else None,
            'keywords': self.filter_settings.keywords,
            'exact_match': self.filter_settings.exact_match,
            'case_sensitive': self.filter_settings.case_sensitive,
            'webhook_url': self.slack_settings.webhook_url,
            'channel': self.slack_settings.channel,
            'monitor_interval': self.monitor_settings.interval,
            'similarity_threshold': self.monitor_settings.similarity_threshold,
            'refresh_enabled': self.monitor_settings.refresh_enabled,
            'refresh_interval': self.monitor_settings.refresh_interval,
            'area_visualization': self.area_visualization
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    @classmethod
    def load(cls, file_path: Path) -> 'AppSettings':
        """설정 로드"""
        if not file_path.exists():
            return cls()
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        settings = cls()
        
        if data.get('title_area'):
            settings.title_area = AreaSettings.from_tuple(data['title_area'])
        if data.get('time_area'):
            settings.time_area = AreaSettings.from_tuple(data['time_area'])
        
        settings.filter_settings = FilterSettings(
            keywords=data.get('keywords', []),
            exact_match=data.get('exact_match', False),
            case_sensitive=data.get('case_sensitive', False)
        )
        
        settings.slack_settings = SlackSettings(
            webhook_url=data.get('webhook_url', ''),
            channel=data.get('channel', '')
        )
        
        settings.monitor_settings = MonitorSettings(
            interval=data.get('monitor_interval', 5),
            similarity_threshold=data.get('similarity_threshold', 0.95),
            refresh_enabled=data.get('refresh_enabled', False),
            refresh_interval=data.get('refresh_interval', 5)
        )
        
        settings.area_visualization = data.get('area_visualization', False)
        
        return settings