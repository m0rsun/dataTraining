# 将data.csv的数据全部插入sql库中

import pandas as pd
import pymysql

MYSQL_HOST="localhost"
MYSQL_PORT=3306
MYSQL_USER="root"
MYSQL_PASSWORD="123456"
MYSQL_DB_NAME="logistics"

def main():
    df=pd.read_csv("data.csv",encoding="utf-8")

    conn=pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB_NAME,
        charset="utf8mb4",
    )
    cursor=conn.cursor()
    for idx,row in df.iterrows():
        review_id=row["评价ID"]
        user_id=row["评价者账号"]
        sku=row["商品编号"]
        send_time=row["发货时间"]
        arrive_time=row["送达时间"]
        area=row["区域"]
        star=row["星数"]
        content=str(row["评价内容"]).strip()

        sql="""
        INSERT INTO reviews (
            `review_id`,`user_id`,`sku`,`send_time`,`arrive_time`,`area`,`star`,`content`
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sql,(review_id,user_id,sku,send_time,arrive_time,area,star,content))

    conn.commit()
    cursor.close()
    conn.close()
    print("update finished")


if __name__=="__main__":
    main()
