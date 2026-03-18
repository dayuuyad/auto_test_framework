import os
from dotenv import load_dotenv

# 加载环境变量，指定UTF-8编码
load_dotenv(encoding='utf-8')

# 基础配置
class BaseConfig:
    # API配置
    API_BASE_URL = os.getenv('API_BASE_URL', 'https://api.example.com')
    API_TIMEOUT = 30
    
    # UI配置
    UI_BASE_URL = os.getenv('UI_BASE_URL', 'https://example.com')
    UI_TIMEOUT = 30
    
    # 数据库配置
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
    DB_NAME = os.getenv('DB_NAME', 'test_db')
    
    # Redis配置
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')
    REDIS_DB = int(os.getenv('REDIS_DB', 0))
    
    # 测试配置
    TEST_USERNAME = os.getenv('TEST_USERNAME', 'admin')
    TEST_PASSWORD = os.getenv('TEST_PASSWORD', 'admin123')
    
    # 报告配置
    ALLURE_RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports', 'allure-results')
    ALLURE_REPORT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports', 'allure-report')
    LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports', 'logs')
    SCREENSHOTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports', 'screenshots')

# 开发环境配置
class DevConfig(BaseConfig):
    API_BASE_URL = os.getenv('DEV_API_BASE_URL', 'https://dev-api.example.com')
    UI_BASE_URL = os.getenv('DEV_UI_BASE_URL', 'https://dev.example.com')

# 测试环境配置
class QaConfig(BaseConfig):
    API_BASE_URL = os.getenv('QA_API_BASE_URL', 'http://localhost:3000/api')
    UI_BASE_URL = os.getenv('QA_UI_BASE_URL', 'http://localhost:3000')

# 预发布环境配置
class StagingConfig(BaseConfig):
    API_BASE_URL = os.getenv('STAGING_API_BASE_URL', 'https://staging-api.example.com')
    UI_BASE_URL = os.getenv('STAGING_UI_BASE_URL', 'https://staging.example.com')

# 生产环境配置
class ProdConfig(BaseConfig):
    API_BASE_URL = os.getenv('PROD_API_BASE_URL', 'https://api.example.com')
    UI_BASE_URL = os.getenv('PROD_UI_BASE_URL', 'https://example.com')

# 根据环境变量选择配置
ENV = os.getenv('ENV', 'qa')

if ENV == 'dev':
    config = DevConfig()
elif ENV == 'qa':
    config = QaConfig()
elif ENV == 'staging':
    config = StagingConfig()
elif ENV == 'prod':
    config = ProdConfig()
else:
    config = QaConfig()