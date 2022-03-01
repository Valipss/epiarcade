import sqlite3

db = sqlite3.connect('lists.db')
cursor = db.cursor()

check = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='whitelist'")
if check.fetchone() is None:
    print('Creating empty database...')
    cursor.execute("CREATE TABLE IF NOT EXISTS whitelist (id text)")
    cursor.execute("CREATE TABLE IF NOT EXISTS blacklist (id text)")
    cursor.execute("INSERT INTO whitelist VALUES ('04376922A96A80')")
    db.commit()
    print('Database created.')

'''
db.check_whitelist(id_str)
--
Returns (boolean) whether the given tag ID is in the whitelist table
--
id_str : Tag unique ID, in a string
'''


def check_whitelist(id_str):
    result = cursor.execute("SELECT * FROM whitelist WHERE id = ?", (id_str,))
    if result.fetchone() is None:
        return False
    return True


'''
db.check_blacklist(id_str)
--
Returns (boolean) whether the given tag ID is in the blacklist table
--
id_str : Tag unique ID, in a string
'''


def check_blacklist(id_str):
    result = cursor.execute("SELECT * FROM blacklist WHERE id = ?", (id_str,))
    if result.fetchone() is None:
        return False
    return True


'''
db.check_exit_tags(id_str)
--
Returns (boolean) whether the given tag ID is in the exit_list table
--
id_str : Tag unique ID, in a string
'''


def check_exit_tags(id_str):
    result = cursor.execute("SELECT * FROM exit_list WHERE id = ?", (id_str,))
    if result.fetchone() is None:
        return False
    return True
