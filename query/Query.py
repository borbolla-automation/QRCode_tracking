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
 |  Module Name    : Query class                                                                                                           |
 |  Module Purpose : Class containing progmatic SQL queries                                        |
 |  Inputs  : ORM class (peewee)                                                                                                               |
 |  Outputs : String converted query outpit object                                                                                           |
 |  Author : Borbolla Automation Inc                                                                                                  |
 |  Email : ingenieria@borbolla-automation.com                                                                                        |
 |  webpage : www.borbolla-automation.com                                                                                             |
 +------------------------------------------------------------------------------------------------------------------------------------+
"""

import peewee
import datetime
from query.Models.QRCode import *

class Query(object):
    """docstring for Query"""
    def __init__(self, model):
        self.model = model

    def get_by_model(self , name):
        self.model_query = self.model.get(self.model.model == str(name))

        return self.model_query
        