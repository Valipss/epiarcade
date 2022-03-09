import time

import nfc

from src.jadoor import login, reader, db


class JaDoor:

    def __init__(self):
        self.student_login = None
        self.clf = nfc.ContactlessFrontend('usb')
        print(self.clf)

    '''
    on_tag_connect(tag)
    --
    Checks sequentially for the tag :
    - Tag type : Deny access if not NTAG203/213
    - Whitelist : Allow access if tag ID in whitelist
    - Blacklist : Deny access if tag ID is blacklist
    - Login : Sends tag ID to cards API, allow access if tag is linked to a login

    If tag is a valid student tag, a time record is written on the tag
    --
    tag : NFC tag object, given by the NFC backend
    '''

    def on_tag_connect(self, tag):
        id_str = reader.get_id(tag)
        print('ID: ' + id_str)
        print('Product: ' + tag.product)

        if tag.product not in {'NXP NTAG203', 'NXP NTAG213', 'Type4Tag'}:
            print('Invalid tag type')
            reader.beep(self.clf, 3)
            time.sleep(5)
            return False

        if db.check_whitelist(id_str) is True:
            print('Tag in whitelist authenticated')
            reader.beep(self.clf, 2)
            self.student_login = "arcade-whitelist@epitech.eu"
            return False

        if db.check_blacklist(id_str) is True:
            print('Blacklisted card tried to open')
            reader.beep(self.clf, 5)
            return False

        login_str = login.retrieve(id_str)
        if type(login_str) != str or '@epitech.eu' not in login_str:
            print('Unknown card scanned')
            reader.beep(self.clf, 3)
            return False
        print('Authenticated ' + login_str)
        self.student_login = login_str

        try:
            reader.write_time_record(tag)
        except nfc.tag.tt2.Type2TagCommandError:
            print('Error when writing tag')
            reader.beep(self.clf, 1)
            time.sleep(1)
        reader.beep(self.clf, 1)
        print('Tag written')
        return False

    '''
    read_tag_loop(self.clf)
    --
    Scans for a tag, until the nfc device backend is closed
    --
    self.clf : NFC backend device
    '''

    def read_tag(self):
        started = time.time()
        self.clf.connect(terminate=lambda: time.time() - started > 2, rdwr={
            'on-connect': self.on_tag_connect,
            'beep-on-connect': False, 'targets': ['106A'],
        })

    '''
    main()
    --
    Launches the nfc device backend, then launching the read tag loop
    '''

    def read(self):
        if not self.clf:
            self.clf = nfc.ContactlessFrontend('usb')
        self.read_tag()
        self.clf.close()
        self.clf = None
        student_login = self.student_login
        self.student_login = None
        return student_login
