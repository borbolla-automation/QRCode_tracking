#!/usr/bin/env python

"""
  ____   ____  _____  ____   ____  _      _                                _    _ _______ ____  __  __       _______ _____ ____  _   _ 
 |  _ \ / __ \|  __ \|  _ \ / __ \| |    | |        /\                /\  | |  | |__   __/ __ \|  \/  |   /\|__   __|_   _/ __ \| \ | |
 | |_) | |  | | |__) | |_) | |  | | |    | |       /  \              /  \ | |  | |  | | | |  | | \  / |  /  \  | |    | || |  | |  \| |
 |  _ <| |  | |  _  /|  _ <| |  | | |    | |      / /\ \            / /\ \| |  | |  | | | |  | | |\/| | / /\ \ | |    | || |  | | . ` |
 | |_) | |__| | | \ \| |_) | |__| | |____| |____ / ____ \          / ____ \ |__| |  | | | |__| | |  | |/ ____ \| |   _| || |__| | |\  |
 |____/ \____/|_|  \_\____/ \____/|______|______/_/    \_\        /_/    \_\____/   |_|  \____/|_|  |_/_/    \_\_|  |_____\____/|_| \_|
                                                                                                                                       
 +------------------------------------------------------------------------------------------------------------------------------------+
 |                                                                                                                                    |
 |  Module Name    : String Data Aquisition                                                                                           |
 |  Module Purpose : string aquisition and validation from QR code                                                                    |
 |  Inputs  : Reading from QR code                                                                                                    |
 |  Outputs : model , company , date , shift , piece count , production line id                                                       |
 |  Author : Borbolla Automation Inc                                                                                                  |
 |  Email : ingenieria@borbolla-automation.com                                                                                        |
 |  webpage : www.borbolla-automation.com                                                                                             |
 +------------------------------------------------------------------------------------------------------------------------------------+
"""
from datetime import datetime , timedelta

qr_code = "4G406K170629D0129J0000"

model = qr_code[0:5]
company = qr_code[5]
date = qr_code[6:12]
shift = qr_code[12]
count = qr_code[13:17]
line  = qr_code[17]

date = datetime(year = int(date[:2])+2000 , month = int(date[2:4]) , day = int(date[4:]))
#print("year : %s\tmonth : %s\tday :\t%s"%(int(date[:2]),int(date[2:4]),int(date[4:])))
print("model\t: %s \ncompany\t: %s \ndate\t: %s\nshift\t: %s\ncount\t: %s\nline\t: %s\n"%(model,company,date,shift,count,line))

print(date.year)



