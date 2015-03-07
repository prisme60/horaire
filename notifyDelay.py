#!/usr/bin/python3

import sys
import datetime
import checkHoraire
import sendSMS


def notify_horaire_problem(pathinfo: str, destination: str, expected_time: datetime.time, allowed_delay: int):
    delay, data = checkHoraire.testHoraire(pathinfo, destination, expected_time)
    msg = None
    if delay > allowed_delay:
        msg = 'Retard : {0} minutes\rGare : {1}\rDestination : {2}\rHeure théorique : {3}\rHeure affichée : {4}'.format(
              delay, pathinfo, destination, expected_time, data.get('heure'))
    return msg

def notify_horaire_problem_sms(user: str, pathinfo: str, destination: str, expected_time: datetime.time, allowed_delay: int):
    msg = notify_horaire_problem(pathinfo, destination, expected_time, allowed_delay)
    if msg is not None:
        sendSMS.writeMsgUser(msg, user)

""" notifyDelay.py cf chars 'PARIS SAINT-LAZARE' 7:44 5 """
if __name__ == '__main__':
    if len(sys.argv) == 6:
        expected_time_of_train = datetime.time(*[int(number) for number in sys.argv[4].split(":")])
        delay = int(sys.argv[5])
        print(notify_horaire_problem_sms(sys.argv[1], sys.argv[2], sys.argv[3], expected_time_of_train, delay))
    else:
        print('Expected format is :\n user origin destination time_of_train allowed_delay')
