import idmSQLmanager

config = {
    'user':'root',
    'password':'root',
    'host':'127.0.0.1',
    'port':3306,
    'database':'familymanager'
}

db = idmSQLmanager.idmSQLmanager(**config)

db.disabelAutoCommit()
transact = db.Transaction()
transact.addStatement("INSERT INTO test(val1, val2) VALUES(?,?)", 1, "fu")
transact.addStatement("INSERT INTO test(val1, val2) VALUES(?,?)", 5, "fud")
transact.commitStatementList()

db.enableAutoCommit()
print(db.execute("SELECT * FROM test"))
db.refreshConnection()