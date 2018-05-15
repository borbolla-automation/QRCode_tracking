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
 |  Module Name    : Models                                                                                                           |
 |  Module Purpose : Mysql Database Design , and model relationship , for database functioning                                        |
 |  Inputs  : ORM class                                                                                                               |
 |  Outputs : Create code , database Object                                                                                           |
 |  Author : Borbolla Automation Inc                                                                                                  |
 |  Email : ingenieria@borbolla-automation.com                                                                                        |
 |  webpage : www.borbolla-automation.com                                                                                             |
 +------------------------------------------------------------------------------------------------------------------------------------+
"""

import peewee
import datetime
#database =  peewee.SqliteDatabase("QR_code.db")
database = peewee.MySQLDatabase(host = "192.168.110.100" , port = 3306 , user = "mkdc" , password = "MKDC" , database = "QRCode")

class PieceModel(peewee.Model):
    date_added = peewee.DateTimeField(default = datetime.datetime.now)
    name = peewee.CharField(max_length = 10 , unique = True)

    class Meta:
        database = database

class Location(peewee.Model):
    location_name = peewee.CharField(max_length = 10 , unique = True)
    alias = peewee.CharField(max_length = 3 , unique = True)

    class Meta:
        database = database

class Shift(peewee.Model):
    date_added = peewee.DateTimeField(default = datetime.datetime.now)
    alias = peewee.CharField(max_length = 2)

    class Meta:
        database = database


class Piece(peewee.Model):
    #_id = peewee.PrimaryKeyField(null = False)
    lot_number = peewee.IntegerField(primary_key = True)
    model = peewee.ForeignKeyField(PieceModel , related_name = 'piece_model')
    date = peewee.DateTimeField(default=datetime.datetime.now)
    manufacturing_date = peewee.DateTimeField(default=datetime.datetime.now)
    #casting_date_time = peewe.DateTimeFIeld()
    shift = peewee.ForeignKeyField(Shift)
    line = peewee.ForeignKeyField(Location , related_name = 'created_line')
    

    class Meta:
        database = database


        
        
"""
class Receipt(peewee.Model):
    
    manufacturing_date = peewee.DateField(default=datetime.datetime.now)
    #casting_date = peewe.DateFIeld()
    shift = peewee.CharField()
    date = peewee.DateField(default=datetime.datetime.now)
    piece = peewee.ForeignKeyField(Piece)
    class Meta:
        database = database

class Line(peewee.Model):
    name = peewee.CharField()
    date = peewee.DateField(default=datetime.datetime.now)
    piece = peewee.ForeignKeyField(Piece , backref = 'lines')
    class Meta:
        database = database
"""
"""
if __name__ == '__main__':
    try:
        Piece.create_table()

    except peewee.OperationalError:
            print("Piece table already exists!")

    try:
        Receipt.create_table()

    except peewee.OperationalError:
        print("Receipt table already exists!")

    try:
        Line.create_table()

    except peewee.OperationalError:
        print("Line table already exists!")

"""