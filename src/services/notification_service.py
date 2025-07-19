import requests
import logging
from typing import Optional
from ..models.settings import SlackSettings

class NotificationService:
    """알림 서비스"""
    
    def __init__(self, slack_settings: SlackSettings):
        self.slack_settings = slack_settings
        self.logger = logging.getLogger(__name__)
    
    def send_slack_notification(self, title_text: str, time_text: str) -> bool:
        """슬랙 알림 전송"""
        if not self.slack_settings.webhook_url:
            self.logger.warning("슬랙 URL이 설정되지 않음")
            return False
        
        try:
            message_text = f"[{title_text}]메일이 왔습니다 확인하세요 [{time_text}]"
            
            message = {"text": message_text}
            
            if self.slack_settings.channel:
                message["channel"] = self.slack_settings.channel
            
            response = requests.post(
                self.slack_settings.webhook_url, 
                json=message, 
                timeout=10
            )
            
            if response.status_code == 200:
                self.logger.info("슬랙 전송 성공")
                return True
            else:
                self.logger.error(f"슬랙 전송 실패: {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.error(f"슬랙 전송 오류: {e}")
            return False
    
    def test_slack_connection(self) -> bool:
        """슬랙 연결 테스트"""
        if not self.slack_settings.webhook_url:
            return False
        
        try:
            message = {
                "text": f"테스트 메시지입니다. 채널: {self.slack_settings.channel or 'default'}"
            }
            
            if self.slack_settings.channel:
                message["channel"] = self.slack_settings.channel
            
            response = requests.post(
                self.slack_settings.webhook_url, 
                json=message, 
                timeout=10
            )
            
            return response.status_code == 200
            
        except Exception as e:
            self.logger.error(f"슬랙 테스트 오류: {e}")
            return False
