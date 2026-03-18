import pymysql
from typing import Dict, Optional, Any

class DBClient:
    def __init__(self, host: str, port: int, user: str, password: str, database: str):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
    
    def connect(self) -> None:
        self.connection = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    
    def execute_query(self, query: str, params: Optional[Any] = None) -> list:
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()
        return result
    
    def execute_update(self, query: str, params: Optional[Any] = None) -> int:
        with self.connection.cursor() as cursor:
            affected_rows = cursor.execute(query, params)
            self.connection.commit()
        return affected_rows
    
    def close(self) -> None:
        if self.connection:
            self.connection.close()