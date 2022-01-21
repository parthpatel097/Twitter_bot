from mysql.connector.constants import ClientFlag
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    port='3306',
    user='root',
    password='',
    database='twitterbot',
    charset='utf8')

# cursor = conn.cursor()
# sql1 = "INSERT INTO tweet_info(tweet_id,posted) VALUES (%s,%s)"
# val1= (1470263879326441475,1)
# cursor.execute(sql1, val1)

sql_select_Query = "select * from tw"
cursor = conn.cursor()
cursor.execute(sql_select_Query)
# get all records
records = cursor.fetchall()
print("Total number of rows in table: ", cursor.rowcount)

print("\nPrinting each row")
for row in records:
    print("Id = ", row[0], )
    print("Name = ", row[1])
    print("Price  = ", row[2])
    print("Purchase date  = ", row[3], "\n")
conn.commit()
