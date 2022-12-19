import mariadb
import sys

# Resource: https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/

class idmSQLmanager:
    config = {}
    def __init__(self, user='', password='', host='127.0.0.1', port='3306', database=''):
        """ Creates an idmSQLmanager object. 
        Autocommit and Cursor Dictionary are Enabled by default.
        """
        try:
            self.connection = mariadb.connect(
                                            user=user,
                                            password=password,
                                            host=host,
                                            port=port,
                                            database=database
                                            )
            self.config = {
                'user' : user,
                'password' : password,
                'host' : host,
                'port' : port,
                'database' : database
            }
            self.connection.autocommit = True
        except Exception as e:
            print(f"Failed to Connect into MariaDB. \nERROR: {e}")
            sys.exit(1)
        
        self.cursor = self.connection.cursor(dictionary=True)
        
        return None


    def disableCursorDictionary(self):
        """
            Disables dictionary into cursor result for cases where it'd be desidered to handle tuples.
        """
        self.cursor = self.connection.cursor(dictionary=False)
        return True

    def enableCursorDictionary(self):
        """
            Enables dictionary into cursor result so it's easier to deal with resulting data from queries.
        """
        self.cursor = self.connection.cursor(dictionary=True)
        return True


    def enableAutoCommit(self):
        """
            Enables autocommit to use idmSQLmanager.execute() method.
        """
        self.connection.autocommit = True
        return True
    

    def disabelAutoCommit(self):
        """
            Enables autocommit to use idmSQLmanager.Transactions methods.
        """
        self.connection.autocommit = False
        return True


    def checkQuery(self, query):
        """
            Check on query for multiple statements, validity of operaton and existence of statement.
        """
        # https://sqlparse.readthedocs.io/en/latest/api/
        import sqlparse

        # parse into a list of statements and each statement into a list of tokens
        statList = sqlparse.parse(sqlparse.format(query, strip_comments=True).strip())

        # Not sure about MariaDB dealing multiple statements.
        if len(statList) > 1:
            raise RuntimeError('Can\t handle more than one statement')
        elif len(statList) == 0:
            raise RuntimeError('Missing Statement')
        elif not(statList[0][0].value in ["UPDATE", "INSERT", "SELECT", "DELETE"]):
            raise RuntimeError('Not a valid operation')

        return None


    # Based on https://github.com/cs50/python-cs50/blob/main/src/cs50/sql.py
    def execute(self, query, *args):
        """
            Executes a query if 
        """
        if self.connection.autocommit == False:
            raise RuntimeError('Can\'t use execute while transactions are enabled.')
        
        self.checkQuery(query)

        qmarkCount = query.count('?')
        if qmarkCount > len(args):
            raise RuntimeError('More placeholders than arguments')
        elif qmarkCount < len(args):
            raise RuntimeError('More arguments than placeholders')
        
        currReadyArgs = tuple(args)

        self.cursor.execute(query, currReadyArgs)

        curList = list(self.cursor)
        print(curList)
    
    class Transaction:
        def __init__():
            if self.connection.autocommit == True:
                raise RuntimeError('Can\'t use transactions while autocommit is active')
                
        def addStatement(query, *args):
            if self.connection.autocommit == True:
                raise RuntimeError('Can\'t use transactions while autocommit is active')

            self.checkQuery(query)

            qmarkCount = query.count('?')
            if qmarkCount > len(args):
                raise RuntimeError('More placeholders than arguments')
            elif qmarkCount < len(args):
                raise RuntimeError('More arguments than placeholders')
            


config = {
    'user':'root',
    'password':'root',
    'host':'127.0.0.1',
    'port':3306,
    'database':'familymanager'
}

d = idmSQLmanager(**config)
d.enableAutoCommit()
d.disableCursorDicitonary()
print(d.execute("SELECT * FROM test"))
print(d.execute("SELECT * FROM test WHERE val1=?", 1))

