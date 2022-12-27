import mariadb
import sys
import traceback

# Resource: https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/
# Resource: https://mariadb-corporation.github.io/mariadb-connector-python/index.html
# Resource: https://mariadb.com/docs/skysql/connect/programming-languages/python/transactions/

class idmSQLmanager(object):
    """
        Class that serves the purpose of providing easy and fast SQL Access to the IDM application.
    """
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
            print(f"Failed to Connect into MariaDB.\nERROR: {e}")
            sys.exit(1)
        
        self.cursor = self.connection.cursor(dictionary=True)
        
        return None
    

    def __del__(self):
        """
            idmSQLmanager class finalizer
        """
        self.connection.close()

        return None


    def refreshConnection(self):
        try:
            self.connection.close()
            self.connection = mariadb.connect(**self.config)
            self.cursor = self.connection.cursor(dictionary=True)
        except:
            raise RuntimeError(f"Couldn't refresh connection to MariaDB.\nERROR: {e}")


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

        if statList[0][0].value == "SELECT":
            return True
        else:
            return None


    # Based on https://github.com/cs50/python-cs50/blob/main/src/cs50/sql.py
    def execute(self, query, *args):
        """
            Executes a query if autocommit is enabled and the user has given the same amount of placeholders and values.
        """
        if self.connection.autocommit == False:
            raise RuntimeError('Can\'t use execute while transactions are enabled.')
        
        resultQuery = self.checkQuery(query)

        qmarkCount = query.count('?')
        if qmarkCount > len(args):
            raise RuntimeError('More placeholders than arguments')
        elif qmarkCount < len(args):
            raise RuntimeError('More arguments than placeholders')
        
        currReadyArgs = tuple(args)
        try:
            self.cursor.execute(query, currReadyArgs) # Returns NoneType
            if resultQuery is None:
                return self.cursor.lastrowid
            else:  
                return list(self.cursor)
        except Exception as e:
            print(traceback.format_exc())
            return False
        
        
        
        

    def Transaction(self):
        """
            Factory method for transactions class.
        """
        return Transactions(self)

    

class Transactions(object):
    """
       Class that hold methods to deal with transactions wrapping MariaDB Connector methods.
    """
    def __init__(self, idmSQL):
        if idmSQL.connection.autocommit == True:
            raise RuntimeError('Can\'t use transactions while autocommit is enabled.')
        self.idmSQL = idmSQL
        self.statementList = []


    def addStatement(self, query, *args):
        """
            Method to add a statement to a statementList to be executed at once in a query, allowing minimal time of
            open transactions.
            TO-DO:
                - Test efficiecy.
        """
        if self.idmSQL.connection.autocommit == True:
            raise RuntimeError('Can\'t use transactions while autocommit is active')

        self.idmSQL.checkQuery(query)

        qmarkCount = query.count('?')
        if qmarkCount > len(args):
            raise RuntimeError('More placeholders than arguments')
        elif qmarkCount < len(args):
            raise RuntimeError('More arguments than placeholders')
            
        currReadyArgs = tuple(args)
        self.statementList.append((query, currReadyArgs))

    def getStatementList(self):
        """
            Retrieve items from statementList.
        """
        return self.statementList
    
    def removeFromStatementList(self, pair):
        """
            Remove items from the statementList
        """
        try:
            self.statementList.remove(pair)
            return True
        except:
            return False

    def commitStatementList(self):
        """
            Execute and commit all items from the statementList
        """
        if len(self.statementList) == 0:
            raise RuntimeError("Missing statements in statementList")
        for commitable in self.statementList:
            self.idmSQL.cursor.execute(commitable[0], commitable[1])
        
        self.idmSQL.connection.commit()
        self.idmSQL.refreshConnection()

