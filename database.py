import mysql.connector

conn = mysql.connector.connect(host='localhost', user='root', password='jesus')
cursor = conn.cursor()
# from androidly import Storage, Notification




cursor.execute("CREATE TABLE IF NOT EXISTS user_info (user_id INTEGER PRIMARY KEY AUTOINCREMENT, username VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL UNIQUE, password VARCHAR(25), )")

cursor.execute("CREATE TABLE IF NOT EXISTS budget (budget_id INTEGER PRIMARY KEY AUTOINCREMENT, budget INT NOT NULL, month VARCHAR(255) NOT NULL, year VARCHAR(255) NOT NULL, day VARCHAR(255) NOT NULL, time VARCHAR(255) NOT NULL)")

cursor.execute("CREATE TABLE IF NOT EXISTS categories (category_id INT PRIMARY KEY AUTO_INCREMENT, category_name VARCHAR(255))")

cursor.execute("CREATE TABLE IF NOT EXISTS expenses(id INTEGER PRIMARY KEY AUTO_INCREMENT, item_bought VARCHAR(255), price VARCHAR(255), category_name VARCHAR(255), date VARCHAR(255), time VARCHAR(255))")

conn.commit()
# DatabaseManager()
