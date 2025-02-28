import psycopg2


conn = psycopg2.connect(dbname="fastapi", user="fastapi", password="231212", host="127.0.0.1", port="5432")
cursor = conn.cursor()

cursor.execute("INSERT INTO users (id, first_name, phone_number, email, password) VALUES (1, 'Tom', '+79723425688', 'tom@gmail.com', 'abc123')")

conn.commit()
print('Данные добавлены')

cursor.close()
conn.close()
# Fetch