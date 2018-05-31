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

database =  peewee.SqliteDatabase("QR_code.db")
#database = peewee.MySQLDatabase(host = "192.168.110.100" , port = 3306 , user = "mkdc" , password = "MKDC" , database = "mkdc")


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
    casting_date = peewee.DateTimeField(unique = True)
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

    database.create_tables([PieceModel , Line , Shift , Piece , Process , Parameter])
    
    models = ['4G401' , '4G101' , '4G110' , '4G210' , '4G450' , '4G150' , '4G160' , '4G260']


    for model in models:
        PieceModel.create(name = model)

        
    Line.create(name = 'Line 1' , alias = 'I')
    Line.create(name = 'Line 2' , alias = 'J')
    Line.create(name = 'Line 3' , alias = 'K')

    Shift.create(alias = 'D')
    Shift.create(alias = 'N')
    Shift.create(alias = 'M')