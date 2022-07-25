import mysql


def data_base():
    try:
        conn = mysql.connector.connect(
                        host = '127.0.0.1',
                        user = 'root',
                        passwd = '1234',
                        database="sql_project"
                        )
    
    except (mysql.connector.errors.ProgrammingError):
        conn = mysql.connector.connect(
                    host = '127.0.0.1',
                    user = 'root',
                    passwd = '1234'
                    )
        cur = conn.cursor()
        cur.execute("CREATE DATABASE sql_project")
        
    cur = conn.cursor()  
    cur.execute("""CREATE TABLE IF NOT EXISTS customers (
                        id MEDIUMINT NOT NULL AUTO_INCREMENT,
                        PRIMARY KEY (id),
                        name varchar(255),
                        age int,
                        address varchar (255),
                        number text,
                        time_in datetime,
                        time_out datetime,
                        status text)
                        """)
    return conn   
