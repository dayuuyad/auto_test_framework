"""API端点路径配置"""

# 用户管理API端点
USER_API_ENDPOINTS = {
    "REGISTER": "/users/register",
    "LOGIN": "/users/login", 
    "GET_USER_INFO": "/users/{user_id}",
    "UPDATE_USER": "/users/{user_id}",
    "DELETE_USER": "/users/{user_id}"
}

# 其他模块的API端点可以在这里添加
# PRODUCT_API_ENDPOINTS = {
#     "LIST_PRODUCTS": "/api/products",
#     "GET_PRODUCT": "/api/products/{product_id}"
# }