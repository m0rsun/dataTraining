# 可视化差评数据

import pandas as pd
import pymysql
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

plt.rcParams["font.sans-serif"]="SimHei"
plt.rcParams["axes.unicode_minus"]=False

MYSQL_HOST="localhost"
MYSQL_PORT=3306
MYSQL_USER="root"
MYSQL_PASSWORD="123456"
MYSQL_DB_NAME="logistics"

# 按区域差评数据
def get_area_bad_stats():
    conn=pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB_NAME,
        charset="utf8mb4",
    )
    sql="""
        SELECT area,count(*) AS bad_count
        FROM reviews
        WHERE star<=2
        GROUP BY area
    """
    df=pd.read_sql(sql,conn)
    conn.close()
    return df

# 按发出日差评数据
def get_day_bad_stats():
    conn=pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB_NAME,
        charset="utf8mb4",
    )
    sql="""
        SELECT DATE(send_time) AS d,count(*) AS bad_count
        FROM reviews
        WHERE star<=2
        GROUP BY d
        ORDER BY d
    """
    df=pd.read_sql(sql,conn)
    conn.close()
    return df

# 按日平均星数
def get_day_average():
    conn=pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB_NAME,
        charset="utf8mb4",
    )
    sql="""
        SELECT DATE(send_time) AS d, AVG(star) AS average
        FROM reviews
        GROUP BY d
        ORDER BY d
    """
    df=pd.read_sql(sql,conn)
    conn.close()
    return df

# 各类问题数量
def get_problem_stats():
    conn=pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB_NAME,
        charset="utf8mb4",
    )
    # 位运算统计每类问题的数量
    sql = """
        SELECT
            SUM(CASE WHEN (problem_types & 1) > 0 THEN 1 ELSE 0 END) AS delay,
            SUM(CASE WHEN (problem_types & 2) > 0 THEN 1 ELSE 0 END) AS package,
            SUM(CASE WHEN (problem_types & 4) > 0 THEN 1 ELSE 0 END) AS service,
            SUM(CASE WHEN (problem_types & 8) > 0 THEN 1 ELSE 0 END) AS wrong,
            SUM(CASE WHEN (problem_types & 16) > 0 THEN 1 ELSE 0 END) AS other
        FROM reviews
        WHERE problem_types > 0;
    """
    df = pd.read_sql(sql, conn)
    conn.close()
    return df

def main():
    fig=plt.figure(figsize=(16,10))

    ax1=fig.add_subplot(2,2,1)
    df1=get_area_bad_stats()
    ax1.pie(df1["bad_count"],labels=df1["area"],autopct="%1.1f%%",colors=plt.cm.Set3.colors)
    ax1.set_title("各地区差评占比图")

    ax2=fig.add_subplot(2,2,2)
    df2=get_day_bad_stats()
    ax2.plot(df2["d"],df2["bad_count"],marker="o",color="#ff6b6b")
    ax2.set_title("每日差评走势图")
    ax2.grid(alpha=0.3)

    ax3=fig.add_subplot(2,2,3)
    df3=get_day_average()
    ax3.plot(df3["d"],df3["average"],marker="o",color="#4ecdc4")
    ax3.set_title("每日平均星数走势图")
    ax3.grid(alpha=0.3)

    ax4=fig.add_subplot(2,2,4)
    df4=get_problem_stats()
    labels = ['时效延误', '包装破损', '服务态度', '发货错误', '其他问题']
    values = [
        df4['delay'].iloc[0],
        df4['package'].iloc[0],
        df4['service'].iloc[0],
        df4['wrong'].iloc[0],
        df4['other'].iloc[0]
    ]
    
    bars = ax4.bar(labels, values, color=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0'])
    ax4.set_title('差评原因分布统计', fontsize=14)
    ax4.set_ylabel('出现次数')
    ax4.tick_params(axis='x', rotation=15)
    # 在柱子上显示数字
    for bar in bars:
        height = bar.get_height()
        ax4.annotate(f'{int(height)}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom')
    ax4.grid(axis='y', alpha=0.3)

    fig.suptitle("评价数据看板",fontsize=20)
    plt.tight_layout()
    plt.show()


if __name__=="__main__":
    main()