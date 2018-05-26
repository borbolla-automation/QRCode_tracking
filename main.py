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
 |  Date   : 2018-05-10                                                                                                               |
 |  Email : ingenieria@borbolla-automation.com                                                                                        |
 |  webpage : www.borbolla-automation.com                                                                                             |
 +------------------------------------------------------------------------------------------------------------------------------------+
"""

import datetime

from query.Models.QRCode import *
import peewee
#read = "KD01094G4011707051215888"
#read  = "KD07014G2101804161210021"

class QRCodeRW(object):
    """docstring for QRCodeReader"""
    def __init__(self, model , line):
        
        self.line  = Line.get(Line.alias == line) 
        self.model = PieceModel.get(PieceModel.name == model)

    def scrap(self , reading):
        if len(reading) != 24:
            print('Readed QR code not from casting area , please read again !')

        else:
            company , machine , mold , model , date , time , count = reading[:2],reading[2:4],reading[4:6],reading[6:11],reading[11:17],reading[17:21], reading[21:]                                                                  
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
            
        return qr_code

    def validation(self , qr_code):


        print(self.model.name,qr_code['model'])
        if qr_code['model'] != self.model.name:
            print('False')
            
            return False
        print('True')
        
        return True
            

    def mysql_insert(self , qr_code):
        #model = PieceModel.get(PieceModel.name == qr_code['model'])
        #model.save()

        #line = Line.get(Line.name == 'Line 1' )
        if datetime.datetime.now().hour >= 7 and datetime.datetime.now().hour < 14:
            alias = 'D'
        elif datetime.datetime.now().hour >= 14 and datetime.datetime.now().hour < 22:
            alias = 'N'
        elif datetime.datetime.now().hour >= 22 or datetime.datetime.now().hour < 7:
            alias = 'M'    
        shift = Shift.get(Shift.alias == alias)    
        #shift.save()
        piece , created = Piece.get_or_create(lot_number = qr_code['count'] , casting_date = qr_code['date_time'] , model = self.model , line = self.line , shift = shift)

        print('Piece created = %s'%created )
        if not created:
            print('Piece already scanned , on %s please act accordingly'%piece.date_added)

        print("company\t= %s\nmachine\t= %s\nmold\t= %s\nmodel\t= %s\ndate_time\t= %s\ncount\t= %s\n"%(qr_code['company'],qr_code['machine'],qr_code['mold'],qr_code['model'],qr_code['date_time'],qr_code['count']))


if __name__ == '__main__':

    qr = QRCodeRW('4G101' , 'I')
    
    while True:
        reading = input('please scan qr code with reader : \n>>')
        if not reading: break
        
        qr_code = qr.scrap(reading)

        validate = qr.validation(qr_code)
        print(validate)
        if validate:
            print('Validate = True , proceed to mysql')
            qr.mysql_insert(qr_code)
        else:
            print('Model diferent than expected')
            break




                

        
    


