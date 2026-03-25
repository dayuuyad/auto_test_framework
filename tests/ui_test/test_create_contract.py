import pytest
import allure
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from ui.create_contract_page import CreateContractPage


@allure.feature("创建合同功能")
@allure.story("创建合同")
def test_aaa(authenticated_page, logger):
    contract_page = CreateContractPage(authenticated_page)
    logger.info("开始测试创建合同（最小信息）")
    contract_page.navigate()
    contract_page.fill_contract_title("测试合同123456")
    contract_page.wait_for_time()



@allure.feature("创建合同功能")
@allure.story("创建合同")
def test_create_contract_with_minimal_info(authenticated_page, logger):
    contract_page = CreateContractPage(authenticated_page)
    logger.info("开始测试创建合同（最小信息）")
    
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
    
    contract_page.create_contract(contract_info)
    
    contract_page.wait_for_time()
    
    assert_is_created_success(contract_page, logger)
    logger.info("最小信息合同创建成功")
    return
    
@allure.feature("创建合同功能")
@allure.story("创建合同")
def test_create_contract_with_all_info(authenticated_page, logger):
    contract_page = CreateContractPage(authenticated_page)
    logger.info("开始测试创建合同（完整信息）")
    
    contract_page.navigate()
    
    contract_page.select_business_type("默认配置")
    contract_page.fill_contract_title("完整测试合同")
    
    contract_page.upload_file("C:\\Users\\ww\\Desktop\\测试.pdf")
    
    assert contract_page.is_file_uploaded("测试.pdf"), "文件应上传成功"
    logger.info("文件上传成功")
    
    contract_page.add_internal_employee("王耀宇")
    
    signers = contract_page.get_signers()
    assert len(signers) > 0, "应至少有一个签署方"
    logger.info(f"添加了 {len(signers)} 个签署方")
    
    contract_page.click_next()
    
    assert contract_page.is_success_message_displayed(), "应显示成功消息"
    message = contract_page.get_success_message()
    logger.info(f"创建结果: {message}")


@allure.feature("创建合同功能")
@allure.story("上传文件")
def test_upload_contract_file(authenticated_page, logger):
    contract_page = CreateContractPage(authenticated_page)
    logger.info("开始测试上传合同文件")
    
    contract_page.navigate()
    
    contract_page.upload_file("C:\\Users\\ww\\Desktop\\测试.pdf")
    
    uploaded_files = contract_page.get_uploaded_files()
    assert len(uploaded_files) > 0, "应至少上传一个文件"
    assert "测试.pdf" in uploaded_files[0], "文件名应包含'测试.pdf'"
    
    logger.info(f"上传文件: {uploaded_files}")


@allure.feature("创建合同功能")
@allure.story("选择业务类型")
def test_select_business_type(authenticated_page, logger):
    contract_page = CreateContractPage(authenticated_page)
    logger.info("开始测试选择业务类型")
    
    contract_page.navigate()
    
    business_types = ["默认配置", "入职"]
    
    for business_type in business_types:
        contract_page.select_business_type(business_type)
        logger.info(f"选择业务类型: {business_type}")


@allure.feature("创建合同功能")
@allure.story("添加签署方")
def test_add_internal_employee_signer(authenticated_page, logger):
    contract_page = CreateContractPage(authenticated_page)
    logger.info("开始测试添加内部员工签署方")
    
    contract_page.navigate()
    
    contract_page.add_internal_employee("王耀宇")
    
    signers = contract_page.get_signers()
    assert len(signers) > 0, "应至少有一个签署方"
    assert "王耀宇" in signers[0]["姓名"], "签署人姓名应为'王耀宇'"
    
@allure.feature("创建合同功能")
@allure.story("添加签署方")
def test_add_enterprise_signer(authenticated_page, logger):
    contract_page = CreateContractPage(authenticated_page)
    logger.info("开始测试添加企业签署方")
    
    contract_page.navigate()
    
    contract_page.add_enterprise_signer("测试企业")
    
    signers = contract_page.get_signers()
    assert len(signers) > 0, "应至少有一个签署方"
    assert "测试企业" in signers[0]["姓名"], "签署人姓名应为'测试企业'"
    
    logger.info(f"添加签署方成功: {signers}")


@allure.feature("创建合同功能")
@allure.story("配置签署设置")
def test_configure_sign_settings(authenticated_page, logger):
    contract_page = CreateContractPage(authenticated_page)
    logger.info("开始测试配置签署设置")
    
    contract_page.navigate()
    
    contract_page.add_internal_employee("王耀宇")
    
    contract_page.configure_sign_settings(
        receive_notification=True,
        specify_position=True
    )
    
    logger.info("签署设置配置成功")


@allure.feature("创建合同功能")
@allure.story("删除签署方")
def test_delete_signer(authenticated_page, logger):
    contract_page = CreateContractPage(authenticated_page)
    logger.info("开始测试删除签署方")
    
    contract_page.navigate()
    
    contract_page.add_internal_employee("王耀宇")
    
    signers_before = contract_page.get_signers()
    assert len(signers_before) > 0, "应至少有一个签署方"
    
    contract_page.delete_signer()
    
    signers_after = contract_page.get_signers()
    assert len(signers_after) == 0, "签署方应被删除"
    
    logger.info("签署方删除成功")


@allure.feature("创建合同功能")
@allure.story("验证表单")
def test_validate_required_fields(authenticated_page, logger):
    contract_page = CreateContractPage(authenticated_page)
    logger.info("开始测试必填项验证")
    
    contract_page.navigate()
    
    contract_page.fill_contract_title("测试合同")
    contract_page.upload_file("C:\\Users\\ww\\Desktop\\测试.pdf")
    
    contract_page.click_next()
    
    alert_message = contract_page.get_alert_message()
    logger.info(f"验证消息: {alert_message}")


@allure.feature("创建合同功能")
@allure.story("取消创建")
def test_cancel_contract_creation(authenticated_page, logger):
    contract_page = CreateContractPage(authenticated_page)
    logger.info("开始测试取消创建合同")
    
    contract_page.navigate()
    
    contract_page.fill_contract_title("测试合同")
    
    contract_page.click_cancel()
    
    logger.info("合同创建已取消")


@allure.feature("创建合同功能")
@allure.story("获取页面信息")
def test_get_uploaded_files(authenticated_page, logger):
    contract_page = CreateContractPage(authenticated_page)
    logger.info("开始测试获取上传文件列表")
    
    contract_page.navigate()
    
    contract_page.upload_file("C:\\Users\\ww\\Desktop\\测试.pdf")
    
    files = contract_page.get_uploaded_files()
    assert len(files) > 0, "应至少有一个文件"
    
    logger.info(f"上传的文件: {files}")


@allure.feature("创建合同功能")
@allure.story("获取页面信息")
def test_get_signers(authenticated_page, logger):
    contract_page = CreateContractPage(authenticated_page)
    logger.info("开始测试获取签署方列表")
    
    contract_page.navigate()
    
    contract_page.add_internal_employee("王耀宇")
    
    signers = contract_page.get_signers()
    assert len(signers) > 0, "应至少有一个签署方"
    
    for signer in signers:
        logger.info(f"签署方: {signer}")


@allure.feature("创建合同功能")
@allure.story("完整流程")
def test_create_contract_complete_flow(authenticated_page, logger):
    contract_page = CreateContractPage(authenticated_page)
    logger.info("开始测试创建合同完整流程")
    
    contract_page.navigate()
    # contract_page.wait_for_page_load()
    
    contract_page.select_business_type("默认配置")
    logger.info("选择业务类型: 默认配置")
    
    contract_page.fill_contract_title("完整流程测试合同")
    logger.info("填写合同标题: 完整流程测试合同")
    
    contract_page.upload_file("C:\\Users\\ww\\Desktop\\测试.pdf")
    logger.info("上传文件: 测试.pdf")
    
    assert contract_page.is_file_uploaded("测试.pdf"), "文件应上传成功"
    
    contract_page.add_internal_employee("王耀宇")
    logger.info("添加签署方: 王耀宇")
    
    signers = contract_page.get_signers()
    assert len(signers) > 0, "应至少有一个签署方"
    
    contract_page.configure_sign_settings(
        receive_notification=True,
        specify_position=True
    )
    logger.info("配置签署设置")
    
    contract_page.click_next()
    logger.info("点击下一步")
    
    assert_is_created_success(contract_page, logger)    
   
    logger.info("完整流程测试通过")



def assert_is_created_success(page: CreateContractPage, logger) -> None:
    message = page.get_alert_message()
    if "提交数据成功" in message:
        logger.info(f"合同创建成功，实际消息: {message}")
    else:
        raise AssertionError(f"合同创建失败，实际消息: {message}")
