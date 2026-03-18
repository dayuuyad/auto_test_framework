import os
import sys
import subprocess

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

def install_dependencies():
    """安装依赖"""
    print("开始安装依赖...")
    
    # 安装基础依赖
    cmd = ["pip", "install", "-r", "requirements/base.txt"]
    print(f"执行: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("安装基础依赖失败:")
        print(result.stderr)
        return False
    
    # 安装开发依赖
    cmd = ["pip", "install", "-r", "requirements/dev.txt"]
    print(f"执行: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("安装开发依赖失败:")
        print(result.stderr)
        return False
    
    # # 安装Playwright浏览器
    # cmd = ["python", "-m", "playwright", "install"]
    # print(f"执行: {' '.join(cmd)}")
    # result = subprocess.run(cmd, capture_output=True, text=True)
    # if result.returncode != 0:
    #     print("安装Playwright浏览器失败:")
    #     print(result.stderr)
    #     return False
    
    print("依赖安装成功！")
    return True

def create_env_file():
    """创建环境变量文件"""
    env_file = ".env"
    if not os.path.exists(env_file):
        print("创建.env文件...")
        with open(env_file, "w") as f:
            f.write("# 环境变量配置\n")
            f.write("ENV=dev\n")
            f.write("API_BASE_URL=https://api.example.com\n")
            f.write("UI_BASE_URL=https://example.com\n")
            f.write("DB_HOST=localhost\n")
            f.write("DB_PORT=3306\n")
            f.write("DB_USER=root\n")
            f.write("DB_PASSWORD=password\n")
            f.write("DB_NAME=test_db\n")
            f.write("REDIS_HOST=localhost\n")
            f.write("REDIS_PORT=6379\n")
            f.write("TEST_USERNAME=admin\n")
            f.write("TEST_PASSWORD=admin123\n")
        print(".env文件创建成功！")
    else:
        print(".env文件已存在，跳过创建")

def create_directories():
    """创建必要的目录"""
    directories = [
        "reports/allure-results",
        "reports/allure-report",
        "reports/logs",
        "reports/screenshots",
        "data/excel",
        "data/sql"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"创建目录: {directory}")
        else:
            print(f"目录已存在: {directory}")

def main():
    print("开始初始化测试环境...")
    
    # 创建必要的目录
    create_directories()
    
    # 创建环境变量文件
    create_env_file()
    
    # 安装依赖
    if install_dependencies():
        print("\n测试环境初始化成功！")
    else:
        print("\n测试环境初始化失败！")
        sys.exit(1)

if __name__ == "__main__":
    main()