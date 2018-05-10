#!/usr/bin/env python

import datetime

#read = "KD01094G0011707051215888"
#read  = "KD07014G2101804161210021"
read  = input('Please scan code on die casting piece :\n>>')
print(len(read))

if len(read) != 24:
    print('Readed QR code not from casting area , please read again !')

else:
    company = read[:2]

    machine = read[2:4]

    mold    = read[4:6]

    model   = read[6:11]

    date    = read[11:17]

    time    = read[17:21]

    count   = read[21:]

    print("company\t= %s\nmachine\t= %s\nmold\t= %s\nmodel\t= %s\ndate\t= %s\ntime\t= %s\ncount\t= %s\n"%(company,machine,mold,model,date,time,count))
    s_year = date[:2]
    ts_year = int(s_year)+2000
    s_month = int(date[2:4])
    s_day   = int(date[4:])

    s_hour  = int(time[:2])
    s_minute = int(time[2:])

    date_time = datetime.datetime(year = ts_year , month = s_month , day = s_day , hour = s_hour , minute = s_minute)

    qr_code={'company':company,
            'machine':machine,
            'mold':mold,
            'model':model,
            'date_time':date_time,
            'count':count}

    print(qr_code)
    
    print('\n')

    print(qr_code['date_time'])

    