import datetime
import time

import ndef

'''
reader.beep(self.clf, nb)
--
Makes the NFC reader blink its led and beep a given number of times
--
self.clf : NFC backend device
nb : Number of times to blink/beep
'''


def beep(clf, nb):
    i = 0
    while i < nb:
        clf.device.turn_on_led_and_buzzer()
        time.sleep(0.05)
        clf.device.turn_off_led_and_buzzer()
        time.sleep(0.1)
        i += 1


'''
reader.get_id(tag)
--
Retrieves the tag ID string from the tag object
--
tag : Tag object
'''


def get_id(tag):
    return tag.identifier.hex().upper()


'''
write_time_record(tag)
--
Writes current time info on the tag
--
tag : Tag object
'''


def write_time_record(tag):
    if tag.ndef is None:
        return
    timerecord = ndef.TextRecord(
        datetime.datetime.now().strftime("EpiArcade last scanned on %d/%m/%Y - %H:%M:%S"))
    second_record = ndef.TextRecord('Don\'t forget to unit test your projects -- <3 Ender')
    print('Writing time record')
    tag.ndef.records = [timerecord, second_record]
