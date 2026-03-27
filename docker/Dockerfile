# FROM python:3.13-slim
# FROM python-allure-base:3.13
FROM auto_test_framework:latest
# 设置工作目录
WORKDIR /appnew

# # 安装Allure（需要Java环境）
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     wget \
#     unzip \
#     openjdk-11-jre-headless \
#     && wget -q https://github.com/allure-framework/allure2/releases/download/2.19.0/allure-2.19.0.zip \
#     && unzip allure-2.19.0.zip \
#     && mv allure-2.19.0 /opt/allure \
#     && chmod +x /opt/allure/bin/allure \
#     && ln -s /opt/allure/bin/allure /usr/bin/allure \
#     && rm allure-2.19.0.zip \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

# # 设置 JAVA_HOME 环境变量
# ENV JAVA_HOME=/opt/java
# ENV PATH="${JAVA_HOME}/bin:${PATH}"

# 复制项目文件
COPY . /appnew

# 安装依赖
RUN pip install --upgrade pip && \
    pip install -r requirements/docker.txt

# 安装Playwright浏览器
# RUN python -m playwright install

# 设置环境变量
ENV ENV=qa

# 运行测试
CMD ["python", "scripts/run_test.py"]