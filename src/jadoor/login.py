import requests

'''
login.retrieve(id_str)
--
Returns a string containing either the login of the scanned tag, or 'UNKNOWN' if
the tag has not been linked to a login (or a network error)
--
id_str : Tag unique ID, in a string
'''


def retrieve(id_str):
    req = requests.get('https://whatsupdoc.epitech.eu/card/' + id_str)
    if req.status_code == 200 and 'login' in req.json():
        print('Identified student card')
        login = req.json()['login']
        return login
    else:
        print('Invalid response from cards API.')
        return None
