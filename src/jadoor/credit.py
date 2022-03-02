import datetime

import src.jadoor.db as db

class Credit:
    def check(self, login):
        #if login == 'arcade-whitelist@epitech.eu':
        #    return True
        print("Current date: " + str(datetime.date.today()))
        print("Last day: " + str(db.get_last_day(login)))
        if db.get_last_day(login) < datetime.date.today():
            return True
        return False

    def consume(self, login):
        #if login == 'arcade-whitelist@epitech.eu':
        #    return
        db.set_last_day(login)
        print("Consumed credit for " + login)