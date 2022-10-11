import psycopg2
import traceback  # 더 정확한 에러 뽑는 정석적인 방법

# 이 화면도 docker 내부이다!
conn = psycopg2.connect("postgres://postgres:1234@host.docker.internal:54321/baedal")  # URL 방식을 사용한 것

try:
    cur = conn.cursor()
    #    sql = 'SELECT * FROM "User"'
    sql = 'INSERT INTO "User" (name) VALUES (%s)'

    # sql = 'INSERT INTO "User" (name,email) VALUES (%(name)s, %(email)s)'
    # result = cur.execute(sql, {"name": "spiderman", "email": "Parker@mail.com"})

    result = cur.execute(sql, ["Spiderman"])
    # //여기에 들어간건 딕셔너리, 투플만 가능!!!!!! 'spiderman' 불가능!

    # result = cur.execute(sql, ["Antman"])
    print(result)
    conn.commit()
except Exception:
    traceback.print_exc()

# try:
#     cur = conn.cursor()
#     sql = 'SELECT * FROM "User"'
#     result = cur.execute(sql, ["Spiderman"])
#     result = cur.fetchall()
#     print(result)
# except Exception:
#     traceback.print_exc()