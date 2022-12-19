import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

# Resource: https://mariadb.com/resources/blog/using-sqlalchemy-with-mariadb-connector-python-part-1/

class idmSQLmanager:
    config = {}
    def __init__(self, databaseName='', connectorName='', user='', password='', host='', port='', defaultDatabase=''):
        self.config['databaseName'] = databaseName
        self.config['connectorName'] = connectorName;
        self.config['user'] = user;
        self.config['password'] = password;
        self.config['host'] = host;
        self.config['port'] = port;
        self.config['defaultDatabase'] = defaultDatabase;
        
        self.configString = f"""{self.config['databaseName']}+{self.config['connectorName']}://{self.config['user']}:{self.config['password']}@{self.config['host']}:{self.config['port']}/{self.config['defaultDatabase']}"""
        self.engine = sqlalchemy.create_engine(self.configString)

        self.Base = declarative_base()
        self.Base.metadata.create_all(self.engine)

        self.Session = sqlalchemy.orm.sessionmaker()
        self.Session.configure(bind=self.engine)
        self.Session = self.Session()

        return None



config = {
    'databaseName':'mariadb',
    'connectorName':'mariadbconnector',
    'user':'root',
    'password':'root',
    'host':'127.0.0.1',
    'port':'3306',
    'defaultDatabase':'familymanager'
}

d = idmSQLmanager(**config)

