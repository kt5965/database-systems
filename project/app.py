import psycopg2
import traceback

conn = psycopg2.connect("postgres://postgres:1234@host.docker.internal:54321/baedal")

# try:
#     cur = conn.cursor()
#     #sql = 'SELECT * FROM "User"'
#     sql = 'INSERT INTO "User" (name) VALUES (%s)' #구멍 뚫지 않고 그냥 value를 쓰면 실용성이 낮다.
#     #sql = 'INSERT INTO "User" (name, email) VALUES (%(name)s, %(email)s)'
#     result = cur.execute(sql, ["Spiderman"]) #dictinary/tuple/list 를 넣을 수도 있음
#     #cur.execute(sql)
#     cur.execute(sql, ["Spiderman"])
#     #result = cur.execute(sql, {
#     #    "name": "spiderman",
#     #    "email": "Parker@mail.com"
#     #})
#     print(result)
#     #rows = cur.fetchall() #데이터베이스에서 하나씩 뽑아준다.
#     conn.commit() #insert /delete 같은 경우에는 commit을 해줘야 함. 그러지 않으면 갱신이 안됨.
#     #print(rows)
# except Exception:
#     traceback.print_exc()

try:
    cur = conn.cursor()
    sql = 'SELECT * FROM "User"'
    cur.execute(sql)
    result = cur.fetchall()
    print(result)
except Exception:
    traceback.print_exc()