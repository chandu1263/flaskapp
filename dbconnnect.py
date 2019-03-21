import  MySQLdb

def connection():
    conn=MySQLdb.connect(host="localhost",
                        user="root",
                        passwd = "iiit123",
                        db="APP")
    c=conn.cursor()
    return c,conn
    
