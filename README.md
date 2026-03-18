# 自动化测试框架

基于 Pytest + Requests + Playwright + Allure 的自动化测试框架，支持API测试、UI测试和端到端测试。

## 项目结构

```
auto_test_framework/
├── .github/                          # GitHub Actions CI配置
│   └── workflows/
│       ├── daily-test.yml            # 每日定时测试
│       └── pr-test.yml               # PR触发测试
│
├── src/                               # 被测系统客户端封装
│   ├── api/                           # API接口封装
│   │   ├── __init__.py
│   │   ├── base_api.py                # API基础类
│   │   └── user_api.py                # 用户模块接口
│   │
│   ├── ui/                             # UI页面对象
│   │   ├── __init__.py
│   │   ├── base_page.py                # 页面基类
│   │   └── login_page.py               # 登录页面
│   │
│   └── utils/                          # 工具类
│       ├── __init__.py
│       ├── logger.py                    # 日志封装
│       ├── db_client.py                  # 数据库客户端
│       ├── redis_client.py                # Redis客户端
│       └── encrypt_util.py               # 加密解密工具
│
├── tests/                              # 测试用例
│   ├── __init__.py
│   ├── conftest.py                      # pytest fixtures配置
│   │
│   ├── api_test/                        # 接口测试
│   │   ├── __init__.py
│   │   └── test_user_api.py
│   │
│   ├── ui_test/                         # UI测试
│   │   ├── __init__.py
│   │   └── test_login.py
│   │
│   └── e2e_test/                         # 端到端测试
│       ├── __init__.py
│       └── test_buy_flow.py
│
├── data/                                # 测试数据
│   ├── test_data.json                    # JSON测试数据
│   ├── test_data.yaml                    # YAML测试数据
│   ├── excel/                            # Excel数据文件
│   └── sql/                              # SQL脚本
│       └── init_data.sql
│
├── config/                              # 配置文件
│   ├── __init__.py
│   ├── settings.py                        # 全局配置
│   ├── dev_config.py                      # 开发环境配置
│   ├── qa_config.py                       # 测试环境配置
│   ├── staging_config.py                  # 预发布配置
│   └── prod_config.py                     # 生产环境配置
│
├── reports/                             # 测试报告
│   ├── allure-results/                   # Allure原始数据
│   ├── allure-report/                    # Allure HTML报告
│   ├── logs/                              # 运行日志
│   └── screenshots/                       # 失败截图
│
├── scripts/                             # 辅助脚本
│   ├── run_test.py                        # 自定义运行脚本
│   ├── init_env.py                        # 环境初始化
│   └── clean_data.py                      # 数据清理
│
├── requirements/                        # 依赖管理
│   ├── base.txt                          # 基础依赖
│   ├── dev.txt                            # 开发依赖
│   └── prod.txt                           # 生产依赖
│
├── docker/                              # Docker配置
│   └── Dockerfile                        # 测试环境容器化
│
├── .env                                  # 环境变量
├── .gitignore                            # Git忽略文件
├── pytest.ini                            # Pytest配置
├── setup.cfg                             # 项目配置
├── pyproject.toml                        # 项目元数据
└── README.md                             # 项目文档
```

## 环境要求

- Python 3.7+
- pip
- Allure Report (可选，用于生成测试报告)

## 安装步骤

1. 克隆项目

2. 进入项目目录
   ```bash
   cd auto_test_framework
   ```

3. 初始化环境
   ```bash
   python scripts/init_env.py
   ```

## 运行测试

### 运行所有测试
```bash
python scripts/run_test.py
```

### 运行API测试
```bash
python scripts/run_test.py --type api
```

### 运行UI测试
```bash
python scripts/run_test.py --type ui
```

### 运行端到端测试
```bash
python scripts/run_test.py --type e2e
```

### 运行指定测试用例
```bash
python scripts/run_test.py --name tests/api_test/test_user_api.py::test_user_register
```

## 生成报告

测试运行完成后，会自动生成Allure报告。也可以手动生成报告：

```bash
python scripts/run_test.py --report
```

## 清理数据

清理测试报告和临时文件：

```bash
python scripts/clean_data.py
```

## Docker运行

1. 构建Docker镜像
   ```bash
   docker build -t auto-test-framework -f docker/Dockerfile .
   ```

2. 运行Docker容器
   ```bash
   docker run --rm auto-test-framework
   ```

## CI/CD

项目配置了GitHub Actions CI，包括：
- 每日定时测试 (`daily-test.yml`)
- PR触发测试 (`pr-test.yml`)

## 配置说明

- 环境变量配置：`.env` 文件
- 不同环境配置：`config/` 目录下的配置文件
- 测试数据：`data/` 目录下的测试数据文件

## 扩展指南

1. **添加API接口**：在 `src/api/` 目录下创建新的接口文件
2. **添加UI页面**：在 `src/ui/` 目录下创建新的页面文件
3. **添加测试用例**：在 `tests/` 目录下创建新的测试文件
4. **添加工具类**：在 `src/utils/` 目录下创建新的工具类

## 注意事项

- 运行UI测试和端到端测试需要安装Playwright浏览器
- 生成Allure报告需要安装Allure Report工具
- 数据库和Redis连接需要根据实际环境配置

## 联系方式

- 测试团队：test@example.com