import urllib.request
import urllib.parse
import urllib.error
import twurl
import json
import ssl


def get_account_api():
    TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    print('')
    acct = input('Enter Twitter Account:')
    if (len(acct) < 1):
        print('Wrong')
        return None
    url = twurl.augment(TWITTER_URL, {'screen_name': acct, 'count': '5'})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()

    js = json.loads(data)

    return js


def show_dict_by_key(dictn):
    """
    dict -> None
    Function returns item by the given key.
    """
    print(dictn.keys())
    user_key = input('Please select which key you need and enter it ')
    print('\n')
    return dictn[user_key]


if __name__ == "__main__":
    print(show_dict_by_key(get_account_api()))
