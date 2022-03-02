import sqlite3
import datetime

db = sqlite3.connect('lists.db')
cursor = db.cursor()

check = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='whitelist'")
if check.fetchone() is None:
    print('Creating empty database...')
    cursor.execute("CREATE TABLE IF NOT EXISTS whitelist (id text)")
    cursor.execute("CREATE TABLE IF NOT EXISTS blacklist (id text)")
    cursor.execute("INSERT INTO whitelist VALUES ('04376922A96A80')")  # Sébastien
    cursor.execute("INSERT INTO whitelist VALUES ('0410632AA96A80')")  # Valentin
    cursor.execute("CREATE TABLE IF NOT EXISTS credits (id text, last_day integer)")
    db.commit()
    print('Database created.')


def get_last_day(id_str):
    """
    db.get_last_day(id_str)
    --
    Returns (integer) the last day of the given tag ID
    --
    id_str : Tag unique ID, in a string
    """
    result = cursor.execute("SELECT last_day FROM credits WHERE id = ?", (id_str,))
    fetched = result.fetchone()
    if fetched is None:
        print("Creating initial credit for {}".format(id_str))
        day = 1
        date = datetime.date.fromordinal(day)
        cursor.execute("INSERT INTO credits VALUES (?, ?)", (id_str, day))
        db.commit()
    else:
        date = datetime.date.fromordinal(fetched[0])
    return date


def set_last_day(id_str):
    """
    db.set_last_day(id_str, day)
    --
    Sets the last day of the given tag ID
    --
    id_str : Tag unique ID, in a string
    """
    date = datetime.date.today()
    day = date.toordinal()
    cursor.execute("UPDATE credits SET last_day = ? WHERE id = ?", (day, id_str))
    db.commit()


def check_whitelist(id_str):
    """
    db.check_whitelist(id_str)
    --
    Returns (boolean) whether the given tag ID is in the whitelist table
    --
    id_str : Tag unique ID, in a string
    """
    result = cursor.execute("SELECT * FROM whitelist WHERE id = ?", (id_str,))
    if result.fetchone() is None:
        return False
    return True


def check_blacklist(id_str):
    """
    db.check_blacklist(id_str)
    --
    Returns (boolean) whether the given tag ID is in the blacklist table
    --
    id_str : Tag unique ID, in a string
    """
    result = cursor.execute("SELECT * FROM blacklist WHERE id = ?", (id_str,))
    if result.fetchone() is None:
        return False
    return True
