import mariadb
import sys

# Resource: https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/

class idmSQLmanager:
    config = {}
    def __init__(self, user='', password='', host='127.0.0.1', port='3306', database=''):
        try:
            self.connection = mariadb.connect(
                                            user=user,
                                            password=password,
                                            host=host,
                                            port=port,
                                            database=database
                                            )
        except Exception as e:
            print(f"Failed to Connect into MariaDB. \nERROR: {e}")
            sys.exit(1)
        
        self.cursor = self.connection.cursor()

        return None
    
def execute(query, *args):
    import sqlparse
    print(sqlparse.parse(sqlparse.format(query, strip_comments=True).strip()))

execute("SELECT * FROM FOO")
    




config = {
    'user':'root',
    'password':'root',
    'host':'127.0.0.1',
    'port':'3306',
    'database':'familymanager'
}

d = idmSQLmanager(**config)

