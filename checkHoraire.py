#!/usr/bin/python3

import re
import datetime
import scrappingHoraire



def testHoraire(pathinfo:str, destination:str, expected_time:datetime.time):
    train_info = scrappingHoraire.horaires_dict(pathinfo)
    #remove info on not wanted destination
    print(train_info)
    print('expectetime=' + str(expected_time))
    p = re.compile('(\d\d):(\d\d)')
    not_found_element = {'destination': destination, 'heure': 'not found'}
    dict_of_delays = {24*60 : not_found_element}
    for info in train_info:
        if info.get('destination') == destination:
            # hour, minute = info.get('heure').split(':') # only works with correctly formated strings!
            m = p.match(info.get('heure'))
            if m is not None:
                train_time = datetime.time(int(m.group(1)), int(m.group(2)))
                print("train_time =" + str(train_time))
                fake_date = datetime.date(1,1,1)
                delta_time = datetime.datetime.combine(fake_date, train_time) - datetime.datetime.combine(fake_date, expected_time)
                print(str(delta_time))
                # postive difference means the train is late
                minutes_of_delay = delta_time.total_seconds() / 60
                print('minutes_of_delay = ', minutes_of_delay)
                dict_of_delays[int(minutes_of_delay)] = info
    min_delay = min(dict_of_delays)
    return min_delay, dict_of_delays[min_delay]

def check_PSL_from_Chars_7h44():
    return testHoraire('chars', 'PARIS SAINT-LAZARE', datetime.time(7, 44))
    

if __name__ == '__main__':
    print(check_PSL_from_Chars_7h44())
