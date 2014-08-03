#!/usr/bin/python3

class Accounts:
    the_url = 'https://smsapi.free-mobile.fr/sendmsg'

    accounts = { 'cf' : {'user' : 'loginNumber',
                        'pass' : 'PaSsWoRdStRiNg' }
              }

if __name__ == '__main__':
    print( 'URL : ' + Accounts.the_url)
    for a in Accounts.accounts:
        print(repr(a) + ' : ' + repr(Accounts.accounts[a]))
