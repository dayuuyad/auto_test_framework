import os
import sys
import argparse
import subprocess

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from config.settings import config

def run_tests(test_type=None, test_name=None):
    """运行测试"""
    # 构建pytest命令
    cmd = [
        "python", "-m", "pytest",
        "--alluredir", config.ALLURE_RESULTS_DIR,
        "--tb=short"
    ]
    
    # 根据测试类型选择测试目录
    if test_type == "api":
        cmd.append("tests/api_test")
    elif test_type == "ui":
        cmd.append("tests/ui_test")
    elif test_type == "e2e":
        cmd.append("tests/e2e_test")
    
    # 运行指定的测试用例
    if test_name:
        cmd.append(test_name)
    
    # 执行命令
    print(f"执行命令: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # 打印输出
    print(result.stdout)
    if result.stderr:
        print("错误输出:")
        print(result.stderr)
    
    # 生成Allure报告
    if result.returncode == 0:
        generate_report()
    
    return result.returncode

def generate_report():
    """生成Allure报告"""
    cmd = [
        "allure", "generate",
        config.ALLURE_RESULTS_DIR,
        "-o", config.ALLURE_REPORT_DIR,
        "--clean"
    ]
    
    print(f"生成Allure报告: {' '.join(cmd)}")

    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    
    if result.returncode == 0:
        print("Allure报告生成成功！")
        print(f"报告路径: {config.ALLURE_REPORT_DIR}")
    else:
        print("Allure报告生成失败:")
        print(result.stderr)

def main():
    parser = argparse.ArgumentParser(description="运行自动化测试")
    parser.add_argument("--type", choices=["api", "ui", "e2e"], help="测试类型")
    parser.add_argument("--name", help="测试用例名称")
    parser.add_argument("--report", action="store_true", help="仅生成报告")
    
    args = parser.parse_args()
    
    if args.report:
        generate_report()
    else:
        run_tests(args.type, args.name)

if __name__ == "__main__":
    generate_report()
    # sys.exit(main())