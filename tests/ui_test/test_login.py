import pytest
import allure
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from ui.login_page import LoginPage

@allure.feature("登录功能")
@allure.story("成功登录")
def test_successful_login(page, logger):
    login_page = LoginPage(page)
    logger.info("开始测试成功登录")
    login_page.navigate()
    login_page.login("18575695125", "Aa123456")

    # 验证登录成功后的页面跳转
    assert login_page.is_login_success()
    logger.info("登录成功测试通过")

@allure.feature("登录功能")
@allure.story("失败登录")
def test_failed_login(page, logger):
    login_page = LoginPage(page)
    logger.info("开始测试失败登录")
    login_page.navigate()
    login_page.login("admin", "wrongpassword")
    # 验证错误信息
    assert login_page.is_login_failed()
    alert_message = login_page.get_alert_message()
    assert "用户名或密码错误" in alert_message
    logger.info("登录失败测试通过")

