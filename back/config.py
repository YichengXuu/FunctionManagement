import os

class Config:
    # 数据库连接字符串
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://shixun:TEzzsLddDRdDwXdE@120:53:31:148/shixun')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 禁用追踪修改，减少开销

class DevelopmentConfig(Config):
    DEBUG = True  # 启用调试模式

class ProductionConfig(Config):
    DEBUG = False  # 生产环境关闭调试

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # 使用内存数据库进行测试
