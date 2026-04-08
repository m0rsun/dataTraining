# 计算关键参数
import pymysql

MYSQL_HOST="localhost"
MYSQL_PORT=3306
MYSQL_USER="root"
MYSQL_PASSWORD="123456"
MYSQL_DB_NAME="logistics"

def main():
    conn=pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB_NAME,
        charset="utf8mb4",
    )
    cursor=conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM reviews")
    total=cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM reviews WHERE star <= 2")
    bad_count=cursor.fetchone()[0]

    cursor.execute("SELECT AVG(star) FROM reviews")
    avg_star=cursor.fetchone()[0]
    avg_star=round(avg_star,1)

    bad_rate=bad_count/total*100 if total>0 else 0
    bad_rate=round(bad_rate,2)

    print("评价数据：")
    print(f"总评价数：{total}")
    print(f"差评数：{bad_count}")
    print(f"差评率：{bad_rate}")
    print(f"平均星数：{avg_star}")

    cursor.close
    conn.close

if __name__=="__main__":
    main()