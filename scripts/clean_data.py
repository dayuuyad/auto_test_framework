import os
import sys
import shutil

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from config.settings import config

def clean_reports():
    """清理测试报告"""
    print("开始清理测试报告...")
    
    # 清理Allure结果和报告
    if os.path.exists(config.ALLURE_RESULTS_DIR):
        shutil.rmtree(config.ALLURE_RESULTS_DIR)
        os.makedirs(config.ALLURE_RESULTS_DIR, exist_ok=True)
        print(f"清理Allure结果目录: {config.ALLURE_RESULTS_DIR}")
    
    if os.path.exists(config.ALLURE_REPORT_DIR):
        shutil.rmtree(config.ALLURE_REPORT_DIR)
        os.makedirs(config.ALLURE_REPORT_DIR, exist_ok=True)
        print(f"清理Allure报告目录: {config.ALLURE_REPORT_DIR}")
    
    # 清理日志文件
    if os.path.exists(config.LOG_DIR):
        for file in os.listdir(config.LOG_DIR):
            file_path = os.path.join(config.LOG_DIR, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"删除日志文件: {file}")
    
    # 清理截图
    if os.path.exists(config.SCREENSHOTS_DIR):
        for file in os.listdir(config.SCREENSHOTS_DIR):
            file_path = os.path.join(config.SCREENSHOTS_DIR, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"删除截图文件: {file}")
    
    print("测试报告清理完成！")

def clean_temp_files():
    """清理临时文件"""
    print("开始清理临时文件...")
    
    # 清理__pycache__目录
    for root, dirs, files in os.walk("."):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                dir_path = os.path.join(root, dir_name)
                shutil.rmtree(dir_path)
                print(f"清理__pycache__目录: {dir_path}")
    
    # 清理.pytest_cache目录
    if os.path.exists(".pytest_cache"):
        shutil.rmtree(".pytest_cache")
        print("清理.pytest_cache目录")
    
    print("临时文件清理完成！")

def main():
    print("开始清理数据...")
    
    # 清理测试报告
    clean_reports()
    
    # 清理临时文件
    # clean_temp_files()
    
    print("\n数据清理完成！")

if __name__ == "__main__":
    main()