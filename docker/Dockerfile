FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY . /app

# 安装依赖
RUN pip install --upgrade pip && \
    pip install -r requirements/base.txt && \
    pip install -r requirements/dev.txt

# 安装Playwright浏览器
RUN python -m playwright install

# 安装Allure
RUN apt-get update && apt-get install -y wget unzip && \
    wget -q https://github.com/allure-framework/allure2/releases/download/2.19.0/allure-2.19.0.zip && \
    unzip allure-2.19.0.zip && \
    mv allure-2.19.0 /opt/allure && \
    ln -s /opt/allure/bin/allure /usr/bin/allure && \
    rm allure-2.19.0.zip

# 设置环境变量
ENV ENV=qa

# 运行测试
CMD ["python", "scripts/run_test.py"]