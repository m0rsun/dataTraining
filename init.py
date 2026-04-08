# 建库

import pymysql
from pymysql.err import OperationalError

#建立连接
MYSQL_HOST="localhost"
MYSQL_PORT=3306
MYSQL_USER="root"
MYSQL_PASSWORD="123456"
MYSQL_DB_NAME="logistics"

def main():
    try:
        conn=pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            charset="utf8mb4"
        )
        cursor=conn.cursor()

        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        print(f"{MYSQL_DB_NAME} successfully generated")

        cursor.execute(f"USE {MYSQL_DB_NAME};")
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS reviews (
                review_id INT PRIMARY KEY,
                user_id VARCHAR(50),
                sku VARCHAR(50),
                send_time DATETIME,
                arrive_time DATETIME,
                area VARCHAR(20),
                star INT,
                content VARCHAR(100)
                );
            """
        )

        conn.commit()
        print("table generated")
    except OperationalError as e:
        print("error in connection")
    finally:
        if 'conn' in locals() and conn.open:
            cursor.close()
            conn.close()

if __name__ == '__main__':
    main()