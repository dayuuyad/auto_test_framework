import pytest
import allure
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from ui.login_page import LoginPage

@allure.feature("购买流程")
@allure.story("完整购买流程")
def test_buy_flow(page, logger):
    logger.info("开始测试完整购买流程")
    
    # 1. 登录
    login_page = LoginPage(page)
    login_page.navigate("https://example.com/login")
    login_page.login("user", "password123")
    assert "dashboard" in page.url
    logger.info("登录成功")
    
    # 2. 浏览商品
    page.click("#products-link")
    page.wait_for_selector(".product-list")
    logger.info("进入商品列表页")
    
    # 3. 选择商品
    page.click(".product-item:first-child")
    page.wait_for_selector(".product-detail")
    logger.info("进入商品详情页")
    
    # 4. 添加到购物车
    page.click("#add-to-cart")
    page.wait_for_selector(".cart-notification")
    logger.info("商品添加到购物车")
    
    # 5. 进入购物车
    page.click("#cart-link")
    page.wait_for_selector(".cart-items")
    logger.info("进入购物车页面")
    
    # 6. 结算
    page.click("#checkout")
    page.wait_for_selector(".checkout-form")
    logger.info("进入结算页面")
    
    # 7. 填写订单信息
    page.fill("#address", "测试地址")
    page.fill("#phone", "13800138000")
    page.click("#submit-order")
    logger.info("提交订单")
    
    # 8. 验证订单成功
    page.wait_for_selector(".order-success")
    success_message = page.inner_text(".order-success")
    assert "订单创建成功" in success_message
    logger.info("购买流程测试通过")