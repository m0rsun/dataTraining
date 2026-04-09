import os
from volcenginesdkarkruntime import Ark
import pymysql

MYSQL_HOST="localhost"
MYSQL_PORT=3306
MYSQL_USER="root"
MYSQL_PASSWORD="123456"
MYSQL_DB_NAME="logistics"

client = Ark(
    base_url='https://ark.cn-beijing.volces.com/api/v3',
    api_key=os.getenv('ARK_API_KEY'),
)

PROMPT = """
你是物流评价分析助手。
根据评价内容，判断属于哪些问题，满足就加对应数字，只返回最终结果：
时效延误=1，包装破损=2，服务态度=4，发货错误=8，其他问题=16
无任何问题返回0。不要解释，不要输出任何文字，只输出一个数字。
评价内容：
"""

def get_label(text):
    try:
        response = client.responses.create(
        model="doubao-seed-1-8-251228",
        input=PROMPT + text.strip(), # Replace with your prompt
        
        thinking={"type": "disabled"}, #  Manually disable deep thinking
        )

        result = response.output[0].content[0].text.strip()
        #print(f"大模型返回：{result}")
        return int(result)
        #return int(response["choices"][0]["message"]["content"].strip())
    except Exception as e:
        print(f"LLM调用失败: {e}")
        return 0

def main():
    conn=pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB_NAME,
        charset="utf8mb4",
    )
    cursor = conn.cursor()

    # 低星评价
    cursor.execute("SELECT review_id, content FROM reviews WHERE star <= 3")
    rows = cursor.fetchall()

    for review_id, content in rows:
        pt = get_label(content)
        print(f"review_id={review_id}, problem_types={pt}")
        cursor.execute(
            "UPDATE reviews SET problem_types = %s WHERE review_id = %s",
            (pt, review_id)
        )

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()