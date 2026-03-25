import pytest
import allure
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from ui.create_contract_page import CreateContractPage
from ui.contract_list_page import ContractListPage
from ui.sign_contract_page import SignContractPage


@allure.feature("签署合同功能")
@allure.story("签署合同")
def test_sign_contract_with_password(authenticated_page, logger):
    contract_page = CreateContractPage(authenticated_page)

    contract_info = {
        "业务类型": "默认配置",
        "合同标题": "测试合同全流程", 
        "文件路径": "C:\\Users\\ww\\Desktop\\测试.pdf",
        "签署方": [
            {
                "类型": "内部员工",
                "姓名": "王耀宇"
            }
        ]
    }
    
    send_contract_page = contract_page.create_contract(contract_info)
    logger.info("开始测试发送合同（拖动印章）")    
    
    contract_list_page = send_contract_page.send_contract()
    logger.info("开始测试签署合同（带密码）")
    
    sign_page = contract_list_page.go_to_sign({"合同状态": "需要我签署"})
    
    # sign_page = SignContractPage(authenticated_page)
    # sign_page.navigate_to_sign("244998183531315328")
    
    sign_page.sign_contract(password="1q")
    # 签署成功
    assert sign_page.get_alert_message() == "签署成功", f"合同签署失败：{sign_page.get_alert_message()}"
    logger.info("合同签署成功")


@allure.feature("签署合同功能")
@allure.story("签署合同")
def test_sign_contract_default_password(authenticated_page, logger):
    sign_page = SignContractPage(authenticated_page)
    logger.info("开始测试签署合同（默认密码）")
    
    contract_id = "244998512096313491"
    sign_page.navigate_to_sign(contract_id)
    
    sign_page.sign_contract()
    
    assert sign_page.is_sign_success(), "合同签署应成功"
    logger.info("合同签署成功")


@allure.feature("签署合同功能")
@allure.story("签署流程")
def test_click_seal_position(authenticated_page, logger):
    sign_page = SignContractPage(authenticated_page)
    logger.info("开始测试点击印章位置")
    
    contract_id = "244998512096313491"
    sign_page.navigate_to_sign(contract_id)
    
    sign_page.click_seal_position()
    
    dialog_visible = sign_page.page.locator(sign_page.seal_dialog).is_visible()
    assert dialog_visible, "印章选择对话框应显示"
    logger.info("印章选择对话框显示成功")


@allure.feature("签署合同功能")
@allure.story("签署流程")
def test_select_seal(authenticated_page, logger):
    sign_page = SignContractPage(authenticated_page)
    logger.info("开始测试选择印章")
    
    contract_id = "244998512096313491"
    sign_page.navigate_to_sign(contract_id)
    
    sign_page.click_seal_position()
    sign_page.select_first_seal()
    sign_page.click_confirm()
    
    logger.info("印章选择成功")


@allure.feature("签署合同功能")
@allure.story("签署流程")
def test_check_agreements(authenticated_page, logger):
    sign_page = SignContractPage(authenticated_page)
    logger.info("开始测试勾选协议")
    
    contract_id = "244998512096313491"
    sign_page.navigate_to_sign(contract_id)
    
    sign_page.click_seal_position()
    sign_page.select_first_seal()
    sign_page.click_confirm()
    sign_page.click_sign_now()
    
    sign_page.check_agreements()
    
    checkbox1 = sign_page.page.locator(sign_page.agreement_checkbox_1).first
    checkbox2 = sign_page.page.locator(sign_page.agreement_checkbox_2)
    
    assert checkbox1.is_checked(), "第一个协议复选框应被勾选"
    assert checkbox2.is_checked(), "第二个协议复选框应被勾选"
    logger.info("协议勾选成功")


@allure.feature("签署合同功能")
@allure.story("签署流程")
def test_enter_password(authenticated_page, logger):
    sign_page = SignContractPage(authenticated_page)
    logger.info("开始测试输入签署密码")
    
    contract_id = "244998512096313491"
    sign_page.navigate_to_sign(contract_id)
    
    sign_page.click_seal_position()
    sign_page.select_first_seal()
    sign_page.click_confirm()
    sign_page.click_sign_now()
    sign_page.check_agreements()
    
    test_password = "1q"
    sign_page.enter_password(test_password)
    
    password_value = sign_page.page.locator(sign_page.password_input).input_value()
    assert password_value == test_password, f"密码输入应为 '{test_password}'"
    logger.info("密码输入成功")
