from time import sleep
import pytest
import allure
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from ui.contract_list_page import ContractListPage


@allure.feature("合同列表功能")
@allure.story("搜索合同")
def test_search_by_contract_name(authenticated_page, logger):
    contract_page = ContractListPage(authenticated_page)
    logger.info("开始测试按合同名称搜索")
    contract_page.navigate()
    dict =  {
        "合同名称": "测试2",
        "合同编号": "2020260321000623654",
    }
    contract_page.search_by_dict(dict)
    
    contract_page.assert_search_results(dict)    
    contract_page.go_to_sign(dict)
    
    # logger.info(f"搜索到 {len(results)} 条记录")


@allure.feature("合同列表功能")
@allure.story("搜索合同")
def test_search_by_enterprise(authenticated_page, logger):
    contract_page = ContractListPage(authenticated_page)
    logger.info("开始测试按企业名称搜索")
    contract_page.navigate()
    
    contract_page.search_by_dict({"企业名称": "回归"})
    
    results = contract_page.get_search_results()
    assert len(results) > 0, "搜索结果不应为空"
    
    logger.info(f"搜索到 {len(results)} 条记录")


@allure.feature("合同列表功能")
@allure.story("搜索合同")
def test_search_by_status(authenticated_page, logger):
    contract_page = ContractListPage(authenticated_page)
    logger.info("开始测试按状态搜索")
    contract_page.navigate()
    
    contract_page.search_by_dict({"合同状态": "未签署"})
    
    results = contract_page.get_search_results()
    assert len(results) > 0, "搜索结果不应为空"
    
    for result in results:
        assert "未签署" in result["状态"], f"状态应为'未签署'，实际为: {result['状态']}"
    
    logger.info(f"搜索到 {len(results)} 条未签署合同")


@allure.feature("合同列表功能")
@allure.story("搜索合同")
def test_search_no_result(authenticated_page, logger):
    contract_page = ContractListPage(authenticated_page)
    logger.info("开始测试无结果搜索")
    contract_page.navigate()
    
    contract_page.search_by_dict({"合同名称": "不存在的合同名称xyz123"})
    
    count = contract_page.get_search_result_count()
    assert count == 0, "搜索结果应为空"
    
    logger.info("无结果搜索测试通过")


@allure.feature("合同列表功能")
@allure.story("重置搜索")
def test_reset_search(authenticated_page, logger):
    contract_page = ContractListPage(authenticated_page)
    logger.info("开始测试重置搜索")
    contract_page.navigate()
    
    contract_page.search_by_dict({"合同名称": "测试"})
    before_count = contract_page.get_search_result_count()
    
    contract_page.reset_search()
    after_count = contract_page.get_search_result_count()
    
    assert after_count >= before_count, "重置后结果数量应大于等于搜索结果"
    logger.info(f"重置前: {before_count} 条, 重置后: {after_count} 条")


@allure.feature("合同列表功能")
@allure.story("获取列表数据")
def test_get_all_contract_names(authenticated_page, logger):
    contract_page = ContractListPage(authenticated_page)
    logger.info("开始测试获取所有合同名称")
    contract_page.navigate()
    
    names = contract_page.get_all_contract_names()
    
    assert len(names) > 0, "合同名称列表不应为空"
    logger.info(f"获取到 {len(names)} 个合同名称")


@allure.feature("合同列表功能")
@allure.story("获取列表数据")
def test_get_all_statuses(authenticated_page, logger):
    contract_page = ContractListPage(authenticated_page)
    logger.info("开始测试获取所有状态")
    contract_page.navigate()
    
    statuses = contract_page.get_all_statuses()
    
    assert len(statuses) > 0, "状态列表不应为空"
    logger.info(f"获取到 {len(statuses)} 个状态: {set(statuses)}")


@allure.feature("合同列表功能")
@allure.story("断言搜索结果")
def test_assert_search_results(authenticated_page, logger):
    contract_page = ContractListPage(authenticated_page)
    logger.info("开始测试断言搜索结果")
    contract_page.navigate()
    
    contract_page.search_by_dict({"合同名称": "测试"})
    
    contract_page.assert_search_results({"合同名称": "测试"})
    
    logger.info("断言搜索结果测试通过")


@allure.feature("合同列表功能")
@allure.story("跳转签署")
def test_go_to_sign(authenticated_page, logger):
    contract_page = ContractListPage(authenticated_page)
    logger.info("开始测试跳转签署页面")
    contract_page.navigate()
    try:
        sign_page = contract_page.go_to_sign({"合同名称": "测试"})

        logger.info("成功跳转到签署页面")
    except RuntimeError as e:
        logger.warning(f"没有可签署的合同: {e}")
        pytest.skip("没有可签署的合同")


@allure.feature("合同列表功能")
@allure.story("跳转签署")
def test_go_to_sign2(authenticated_page, logger):
    contract_page = ContractListPage(authenticated_page)
    logger.info("开始测试跳转签署页面")
    contract_page.navigate()
    dict =  {
        "合同状态": "需要我签署",
    }
    try:
        sign_page = contract_page.go_to_sign(dict)
        sleep(5)

        logger.info("成功跳转到签署页面")
    except RuntimeError as e:
        logger.warning(f"没有可签署的合同: {e}")
        pytest.skip("没有可签署的合同")


