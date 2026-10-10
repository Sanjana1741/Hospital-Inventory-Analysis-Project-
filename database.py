import mysql.connector
  #this part is where we connect our python to our database
def get_connection():
    db=mysql.connector.connect( 
        host="localhost",
        user="root",
        password="root",
        database="hospital_inventory"
    )
    return db

db=get_connection()

print("Database connected sucessfully!")



#to check whether python can actuall retrieve data from the database
cursor=db.cursor()

cursor.execute("SELECT * FROM drugs LIMIT 5")

drugs=cursor.fetchall()

print("Drug records:")
print(drugs)

cursor.close()
db.close()
