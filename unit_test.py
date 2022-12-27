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

savecursor = db.execute("INSERT INTO users(username, password) VALUES(?, ?)", "FO", "RRO")
print(savecursor)
savecursor = db.execute("UPDATE users SET username = ? WHERE id = ?", 'ficu','9')