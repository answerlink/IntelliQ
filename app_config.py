import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """应用配置类"""
    
    # 后端配置
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    BACKEND_HOST = os.getenv('BACKEND_HOST', 'localhost')
    BACKEND_PORT = int(os.getenv('BACKEND_PORT', 5050))
    
    # 前端配置
    FRONTEND_HOST = os.getenv('FRONTEND_HOST', 'localhost')
    FRONTEND_PORT = int(os.getenv('FRONTEND_PORT', 3000))
    
    # API配置
    API_PREFIX = os.getenv('API_PREFIX', '/api')
    
    # CORS配置
    CORS_ORIGINS = "*"
    
    # 其他配置
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
    
    @property
    def backend_url(self):
        """获取后端完整URL"""
        return f"http://{self.BACKEND_HOST}:{self.BACKEND_PORT}"
    
    @property
    def frontend_url(self):
        """获取前端完整URL"""
        return f"http://{self.FRONTEND_HOST}:{self.FRONTEND_PORT}"

# 全局配置实例
config = Config() 