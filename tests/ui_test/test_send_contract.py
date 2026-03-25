import pytest
import allure
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from ui.create_contract_page import CreateContractPage
from ui.send_contract_page import SendContractPage



@allure.feature("发送合同功能")
@allure.story("发送合同")
def test_send_contract_with_seal(authenticated_page, logger):
    contract_page = CreateContractPage(authenticated_page)

    contract_info = {
        "业务类型": "默认配置",
        "合同标题": "测试合同", 
        "文件路径": "C:\\Users\\ww\\Desktop\\测试.pdf",
        "签署方": [
            {
                "类型": "内部员工",
                "姓名": "王耀宇"
            }
        ]
    }
    
    send_contract_page = contract_page.create_contract(contract_info)
    # send_contract_page = SendContractPage(authenticated_page)
    logger.info("开始测试发送合同（拖动印章）")    
    
    send_contract_page.send_contract()    
    # send_contract_page.wait_for_time()
    
    assert_is_send_success(send_contract_page, logger)
    logger.info("合同发送成功")


@allure.feature("发送合同功能")
@allure.story("拖动控件")
def test_drag_seal_to_pdf(authenticated_page, logger):
    send_contract_page = SendContractPage(authenticated_page)
    logger.info("开始测试拖动印章控件到PDF区域")
    
    contract_id = "244815169606123532"
    send_contract_page.navigate(contract_id)
    
    send_contract_page.drag_seal_to_pdf()
    
    logger.info("印章控件拖动成功")


@allure.feature("发送合同功能")
@allure.story("拖动控件")
def test_drag_control_to_pdf(authenticated_page, logger):
    send_contract_page = SendContractPage(authenticated_page)
    logger.info("开始测试拖动不同类型控件到PDF区域")
    
    contract_id = "244815169606123532"
    send_contract_page.navigate(contract_id)
    
    controls = ["印章", "日期", "经办人签名"]
    
    for control in controls:
        send_contract_page.drag_control_to_pdf(control)     
        logger.info(f"{control}控件拖动成功")


@allure.feature("发送合同功能")
@allure.story("发送合同")
def test_send_contract_with_custom_position(authenticated_page, logger):
    send_contract_page = SendContractPage(authenticated_page)
    logger.info("开始测试发送合同（自定义印章位置）")
    
    contract_id = "244815169606123532"
    seal_position = {"x": 400, "y": 300}
    
    send_contract_page.send_contract(contract_id, seal_position)
    
    assert_is_send_success(send_contract_page, logger)
    logger.info("合同发送成功（自定义位置）")


@allure.feature("发送合同功能")
@allure.story("页面导航")
def test_navigate_to_sign_page(authenticated_page, logger):
    send_contract_page = SendContractPage(authenticated_page)
    logger.info("开始测试导航到发送合同页面")
    
    contract_id = "244815169606123532"
    send_contract_page.navigate(contract_id)
    
    page_title = send_contract_page.get_page_title()    
    assert "发送合同" in page_title, f"页面标题应包含'发送合同'，实际标题: {page_title}"
    
    logger.info(f"页面标题: {page_title}")


@allure.feature("发送合同功能")
@allure.story("获取页面信息")
def test_get_files(authenticated_page, logger):
    send_contract_page = SendContractPage(authenticated_page)
    logger.info("开始测试获取文件列表")
    
    contract_id = "244815169606123532"
    send_contract_page.navigate(contract_id)
    
    files = send_contract_page.get_files()
    assert len(files) > 0, "应至少有一个文件"
    
    logger.info(f"文件列表: {files}")


@allure.feature("发送合同功能")
@allure.story("获取页面信息")
def test_get_signers(authenticated_page, logger):
    send_contract_page = SendContractPage(authenticated_page)
    logger.info("开始测试获取签署方列表")
    
    contract_id = "244815169606123532"
    send_contract_page.navigate(contract_id)
    
    signers = send_contract_page.get_signers()
    assert len(signers) > 0, "应至少有一个签署方"
    
    logger.info(f"签署方列表: {signers}")


@allure.feature("发送合同功能")
@allure.story("选择文件和签署方")
def test_select_file_and_signer(authenticated_page, logger):
    send_contract_page = SendContractPage(authenticated_page)
    logger.info("开始测试选择文件和签署方")
    
    contract_id = "244815169606123532"
    send_contract_page.navigate(contract_id)
    
    send_contract_page.select_file(0)
    logger.info("选择第一个文件")
    
    send_contract_page.select_signer(0)
    logger.info("选择第一个签署方")


@allure.feature("发送合同功能")
@allure.story("验证发送按钮状态")
def test_send_button_disabled_without_seal(authenticated_page, logger):
    send_contract_page = SendContractPage(authenticated_page)
    logger.info("开始测试发送按钮状态（未拖动印章）")
    
    contract_id = "244815169606123532"
    send_contract_page.navigate(contract_id)        
    
    send_contract_page.click_send()
    
    message = send_contract_page.get_alert_message()
    assert "需要添加印章控件" in message, f"应提示需要添加印章控件，实际消息: {message}"
    
    logger.info(f"验证消息: {message}")


@allure.feature("发送合同功能")
@allure.story("返回操作")
def test_click_back_button(authenticated_page, logger):
    send_contract_page = SendContractPage(authenticated_page)
    logger.info("开始测试点击返回按钮")
    
    contract_id = "244815169606123532"
    send_contract_page.navigate(contract_id)
    
    send_contract_page.click_back()
    
    logger.info("点击返回按钮成功")


@allure.feature("发送合同功能")
@allure.story("上一步操作")
def test_click_previous_button(authenticated_page, logger):
    send_contract_page = SendContractPage(authenticated_page)
    logger.info("开始测试点击上一步按钮")
    
    contract_id = "244815169606123532"
    send_contract_page.navigate(contract_id)
    
    send_contract_page.click_previous()
    
    logger.info("点击上一步按钮成功")


@allure.feature("发送合同功能")
@allure.story("完整流程")
def test_send_contract_complete_flow(authenticated_page, logger):
    send_contract_page = SendContractPage(authenticated_page)
    logger.info("开始测试发送合同完整流程")
    
    contract_id = "244815169606123532"
    send_contract_page.navigate(contract_id)            
    logger.info(f"导航到发送合同页面，合同ID: {contract_id}")
    
    files = send_contract_page.get_files()
    assert len(files) > 0, "应至少有一个文件"
    logger.info(f"文件列表: {files}")
    
    signers = send_contract_page.get_signers()
    assert len(signers) > 0, "应至少有一个签署方"
    logger.info(f"签署方列表: {signers}")
    
    send_contract_page.select_signer(0)
    logger.info("选择第一个签署方")
    
    send_contract_page.drag_seal_to_pdf()
    logger.info("拖动印章控件到PDF区域")
    
    send_contract_page.click_send()
    logger.info("点击发送按钮")
    
    assert_is_send_success(send_contract_page, logger)  
    
    logger.info("完整流程测试通过")


def assert_is_send_success(page: SendContractPage, logger) -> None:
    message = page.get_alert_message()
    if "保存成功" in message or "发送成功" in message:
        logger.info(f"合同发送成功，实际消息: {message}")
    else:
        raise AssertionError(f"合同发送失败，实际消息: {message}")
