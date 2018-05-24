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
database = peewee.MySQLDatabase(host = "192.168.110.100" , port = 3306 , user = "mkdc" , password = "MKDC" , database = "mkdc")


class BaseModel(peewee.Model):
    class Meta:
        database = database

class PieceModel(BaseModel):
    name = peewee.CharField(max_length = 10 , unique = True)
    date_added = peewee.DateTimeField(default = datetime.datetime.now)

class Line(BaseModel):
    name = peewee.CharField(max_length = 10 , unique = True)
    alias = peewee.CharField(max_length = 3 , unique = True)
    date_added = peewee.DateTimeField(default = datetime.datetime.now)

class Shift(BaseModel):
    alias = peewee.CharField(max_length = 3 ,)
    date_added = peewee.DateTimeField(default = datetime.datetime.now)



class Piece(BaseModel):
    lot_number = peewee.CharField()
    date_added = peewee.DateTimeField(default = datetime.datetime.now)
    casting_date = peewee.DateTimeField()
    model = peewee.ForeignKeyField(PieceModel , backref = 'pieces')
    line  = peewee.ForeignKeyField(Line , backref = 'pieces')
    shift = peewee.ForeignKeyField(Shift , backref = 'pieces')


class Process(BaseModel):
    name = peewee.CharField()
    piece = peewee.ForeignKeyField(Piece , backref = 'procesess')

class Parameter(BaseModel):
    Process = peewee.ForeignKeyField(Process , backref = 'parameters')
    parameter_1  = peewee.FloatField()
    parameter_2  = peewee.FloatField()
    parameter_3  = peewee.FloatField()
    parameter_4  = peewee.FloatField()
    parameter_5  = peewee.FloatField()
    parameter_6  = peewee.FloatField()
    parameter_7  = peewee.FloatField()
    parameter_8  = peewee.FloatField()
    parameter_9  = peewee.FloatField()
    parameter_10 = peewee.FloatField()







if __name__ == '__main__':

    try:
        PieceModel.create_table()

    except peewee.OperationalError:
        print("PieceModel table already exists!")

    


    try:
        Line.create_table()

    except peewee.OperationalError:
        print("Line table already exists!")

    try:
        Shift.create_table()

    except peewee.OperationalError:
        print("Shift table already exists!")

    try:

        Piece.create_table()

    except peewee.OperationalError:
            print("Piece table already exists!")


    try:
        Process.create_table()

    except peewee.OperationalError:
        print("Process table already exists!")

    try:
        Parameter.create_table()

    except peewee.OperationalError:
        print("Parameter table already exists!")