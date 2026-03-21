import os
import sys
import argparse
import subprocess

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from config.settings import config

def run_tests(test_type=None, test_name=None):
    """运行测试"""
    cmd = [
        sys.executable, "-m", "pytest",
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
        if isinstance(test_name, list):
            cmd.extend(test_name)
        else:
            cmd.append(test_name)
    
    # 执行命令（设置环境变量强制使用UTF-8编码）
    print(f"执行命令: {' '.join(cmd)}")
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace', env=env)
    
    # 打印输出
    print(result.stdout)
    if result.stderr:
        print("错误输出:")
        print(result.stderr)
    
    # 生成Allure报告
    # if result.returncode == 0:
    #     generate_report()
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

    result = subprocess.run(cmd, capture_output=True, text=True, shell=True, encoding='utf-8', errors='replace')
    
    if result.returncode == 0:
        print("Allure报告生成成功！")
        print(f"报告路径: {config.ALLURE_REPORT_DIR}")
    else:
        print("Allure报告生成失败:")
        print(result.stderr)

def open_report(port=8080):
    """
    打开Allure报告（使用allure open命令）
    
    Args:
        port: HTTP服务器端口，默认8080
    """
    report_dir = config.ALLURE_REPORT_DIR
    
    if not os.path.exists(report_dir):
        print(f"报告目录不存在: {report_dir}")
        print("请先运行测试生成报告")
        return
    
    cmd = ["allure", "open", "-p", str(port), report_dir]
    print(f"打开Allure报告: {' '.join(cmd)}")
    
    subprocess.run(cmd, shell=True)

def run_specific_test(modules, functions=None, test_type=None):
    """
    直接在代码中指定运行的模块和函数，支持运行多个
    
    Args:
        modules: 支持三种格式
                 - 单个字符串: "test_login"
                 - 列表: ["test_login", "test_user"]
                 - 字典: {"test_login": ["test_login_success", "test_login_fail"]}
        functions: 函数名，当 modules 为字符串或列表时使用
        test_type: 测试类型，可选值 "api", "ui", "e2e"
    
    Example:
        # 运行单个测试
        run_specific_test("test_login", "test_user_login")
        
        # 运行多个模块
        run_specific_test(["test_login", "test_user"], test_type="api")
        
        # 运行多个函数
        run_specific_test("test_login", ["test_login", "test_logout"])
        
        # 字典格式：不同模块运行不同函数
        run_specific_test({
            "test_login": ["test_login_success", "test_login_fail"],
            "test_user_api": ["test_get_user_info"],
        }, test_type="api")
    """
    test_paths = []
    type_dir_map = {
        "api": "tests/api_test",
        "ui": "tests/ui_test",
        "e2e": "tests/e2e_test"
    }
    
    if isinstance(modules, dict):
        for module, funcs in modules.items():
            if not module.endswith('.py'):
                module = f"{module}.py"
            if funcs is None:
                funcs = [None]
            elif isinstance(funcs, str):
                funcs = [funcs]
            
            for func in funcs:
                test_path = module
                if func:
                    test_path = f"{module}::{func}"
                
                if test_type and not module.startswith("tests/"):
                    test_path = f"{type_dir_map.get(test_type, 'tests')}/{module}"
                    if func:
                        test_path = f"{test_path}::{func}"
                
                test_paths.append(test_path)
    else:
        if isinstance(modules, str):
            modules = [modules]
        if functions is None:
            functions = [None] * len(modules)
        elif isinstance(functions, str):
            functions = [functions]
        
        for module, function in zip(modules, functions):
            if not module.endswith('.py'):
                module = f"{module}.py"
            test_path = module
            
            if function:
                test_path = f"{module}::{function}"
            
            if test_type and not module.startswith("tests/"):
                test_path = f"{type_dir_map.get(test_type, 'tests')}/{module}"
                if function:
                    test_path = f"{test_path}::{function}"
            
            test_paths.append(test_path)
    
    return run_tests(test_name=test_paths)

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
    # sys.exit(main())

    import clean_data
    clean_data.main()
    
    run_specific_test({
    # "test_login": ["test_login_success", "test_login_fail"],
    "test_user_api": ["test_user_register"],
    "test_api_flow": ["test_api_flow"],
    
    },
     test_type="api")
    
    open_report()