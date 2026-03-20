import openpyxl
from openpyxl import Workbook
import os

def create_flow_test_data():
    excel_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'excel', 'api_flow_test_data.xlsx')
    excel_path = os.path.abspath(excel_path)
    
    os.makedirs(os.path.dirname(excel_path), exist_ok=True)
    
    wb = Workbook()
    
    ws_register_login = wb.active
    ws_register_login.title = "用户注册登录流程"
    
    ws_register_login.append(["接口地址", "请求参数（JSON）", "预期结果（JSON）", "上下文"])
    
    ws_register_login.append([
        "/api/users/register",
        '{"username":"testuser001","email":"testuser001@example.com","password":"Test@123456"}',
        '{"status":"success"}',
        "userid:data.userid"
    ])
    
    ws_register_login.append([
        "/api/users/login",
        '{"userid":"${userid}","password":"Test@123456"}',
        '{"status":"success"}',
        "token:data.token"
    ])
    
    ws_register_login.append([
        "/api/users/info",
        '{"token":"${token}"}',
        '{"status":"success"}',
        ""
    ])
    
    ws_order = wb.create_sheet("订单创建支付流程")
    
    ws_order.append(["接口地址", "请求参数（JSON）", "预期结果（JSON）", "上下文"])
    
    ws_order.append([
        "/api/products/list",
        '{"category":"electronics"}',
        '{"status":"success"}',
        "product_id:data.products[0].id"
    ])
    
    ws_order.append([
        "/api/cart/add",
        '{"product_id":"${product_id}","quantity":1}',
        '{"status":"success"}',
        "cart_id:data.cart_id"
    ])
    
    ws_order.append([
        "/api/orders/create",
        '{"cart_id":"${cart_id}","address":"测试地址"}',
        '{"status":"success"}',
        "order_id:data.order_id"
    ])
    
    ws_order.append([
        "/api/payment/create",
        '{"order_id":"${order_id}","method":"alipay"}',
        '{"status":"success"}',
        "payment_url:data.payment_url"
    ])
    
    for ws in wb.worksheets:
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 60)
            ws.column_dimensions[column_letter].width = adjusted_width
    
    wb.save(excel_path)
    print(f"流程测试数据Excel文件创建成功: {excel_path}")
    return excel_path

if __name__ == "__main__":
    create_flow_test_data()