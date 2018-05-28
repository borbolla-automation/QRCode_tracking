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
import peewee , threading
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
from GUI.template import MyGui
#import pyautogui

#from PIL import Image
#read = "KD01094G4011707051215888"
#read  = "KD07014G2101804161210021"

color = '#7da6cf'

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

    def validation(self , qr_code , model):


        print(model,qr_code['model'])
        if qr_code['model'] != model:
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

        #print('Piece created = %s'%created )
        if not created:
            print('Piece already scanned , on %s please act accordingly'%piece.date_added)

        #print("company\t= %s\nmachine\t= %s\nmold\t= %s\nmodel\t= %s\ndate_time\t= %s\ncount\t= %s\n"%(qr_code['company'],qr_code['machine'],qr_code['mold'],qr_code['model'],qr_code['date_time'],qr_code['count']))


class Interface:
    
    def __init__(self , master):
        self.master = master
        self.master.geometry("{0}x{1}+0+0".format(self.master.winfo_screenwidth(), self.master.winfo_screenheight()))
        self.menubar()
        self.widgets()
        self.last_10()
        self.qr = QRCodeRW('4G101' , 'I')

        self.master.bind('<Return>' , self.get_text)
        self.model_combo_box()

    def menubar(self):
        self.menubar = Menu(self.master)
        # create a pulldown menu, and add it to the menu bar
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.hello)
        filemenu.add_command(label="Save", command=self.hello)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.master.quit)
        self.menubar.add_cascade(label="File", menu=filemenu)

        # create more pulldown menus
        editmenu = Menu(self.menubar, tearoff=0)
        editmenu.add_command(label="Cut", command=self.hello)
        editmenu.add_command(label="Copy", command=self.hello)
        editmenu.add_command(label="Paste", command=self.hello)
        self.menubar.add_cascade(label="Edit", menu=editmenu)

        helpmenu = Menu(self.menubar, tearoff=0)
        helpmenu.add_command(label="About", command=self.hello)
        self.menubar.add_cascade(label="Help", menu=helpmenu)

        # display the menu
        self.master.config(menu=self.menubar)

    def widgets(self):
        self.borbolla_logo = PhotoImage(file = 'images/borbolla_logo.png')
        self.logo_b_label = Label(self.master , image = self.borbolla_logo , background=color).grid(row = 0 , column = 1 , columnspan = 4 , sticky = NW ,)

        self.scan_label = Label(self.master , text = 'Please scan Converter housing QR Code!' , font = "Courier 24 bold" , background=color)
        #self.scan_label.config(font=("Courier", 24))
        self.scan_label.grid(row = 1 , column = 1 ,columnspan = 6)

        self.test_last = Label(self.master , text = 'helo' , background=color)
        self.test_last.config(font=("Courier", 24))
        self.test_last.grid(row = 20 , column = 1 ,columnspan = 6)

        self.manufacturing_info = Label(self.master , text = 'Manufacturing info' , font = "Courier 24 bold" , background=color)
        #self.manufacturing_info.config(font=("Courier", 24))
        self.manufacturing_info.grid(row = 5 , column = 1 ,columnspan = 6)

        self.qr_entry = Entry(self.master , state = DISABLED , font = "Courier 24")
        self.qr_entry.grid(row = 2 , column = 1 , columnspan = 20 , rowspan = 2 ,sticky = NSEW)
        self.qr_entry.focus_set()

        #self.kodaco_logo = PhotoImage(file = 'images/kodaco_logo.png')
        #self.logo_k_label = Label(self.master , image = self.kodaco_logo).grid(row = 0 , column =20 , columnspan = 10 , sticky = NW ,)

        self.combo_label = Label(self.master , text = 'Please select production Model' , font = "Courier 24 bold" , background=color)
        #self.combo_label.config(font=("Courier", 20))
        self.combo_label.grid(row = 1 ,column = 23 , sticky =  NSEW , )

        self.combo_label = Label(self.master , text = '   ' , background=color)
        self.combo_label.config(font=("Courier", 20))
        self.combo_label.grid(row = 1 ,column = 24 , sticky =  NSEW , )

        self.combo_label = Label(self.master , text = '     ' , background=color)
        self.combo_label.config(font=("Courier", 24))
        self.combo_label.grid(row = 2 ,column = 22 , sticky =  NSEW , )

        self.combo_label = Label(self.master , text = '     ' , background=color)
        self.combo_label.config(font=("Courier", 24))
        self.combo_label.grid(row = 0 ,column = 0 , sticky =  NSEW , )

        self.combo = self.model_combo_box()
        self.combo.grid(row = 2 , column = 23 , sticky = NSEW)
        self.combo.bind("<<ComboboxSelected>>", self.combo_selected)

        #self.master.grid_columnconfigure(0, weight=0.5)
        self.master.grid_rowconfigure(24, weight=1)
        self.master.grid_rowconfigure(20, weight=1)
        self.master.grid_rowconfigure(5, weight=1)
        self.master.grid_rowconfigure(0, weight=1)

    def model_combo_box(self):
        model_list = []
        model_list.append('Select Model')
        models = PieceModel.select()
        for model in models:
            model_list.append(model.name)

        model_tuple = tuple(model_list)
        combo = ttk.Combobox(self.master ,  state = 'readonly' , font = "Courier 24" , background = color)
        combo['values'] = model_tuple
        combo.current(0)

        return combo

    def combo_selected(self , event):
        combo_text = self.combo.get()

        if combo_text != 'Select Model':
            print(combo_text)
            self.qr_entry.config(state = NORMAL)
            self.qr_entry.focus_set()
        else:
            self.qr_entry.config(state = DISABLED)

        


    def reply(self , message):

        a = showinfo(title = 'MKDC' , message = message)  
        #a.after(3000 , press_enter)
        
        
    def last_10(self):
        pieces = Piece.select().order_by(Piece.date_added.desc()).limit(10)
        header = 'ID\tMODEL\tLINE\tSHIFT\tCASTING DATE\tMANUF_DATE'
        header = header.split('\t')
        #print(header)
        info = []
        info.append(header)
        for piece in pieces:
            info.append([piece.id , piece.model.name , piece.line.alias , piece.shift.alias , piece.casting_date , piece.date_added])
        #label_text = header
        #print(info)
        #print('lenght = %s' % len(pieces))
        height = len(pieces)+1
        if height >10 : height = 10
        width = 6
        for i in range(height): #Rows
            for j in range(width): #Columns
                #print('[%s,%s]'%(i,j))
                b = Label(self.master, text=str(info[i][j])+'  ' ,  font =  "Courier 16", background=color)
                b.grid(row=i+6, column=j+1)


    def hello(self):
        print("Holle!!")


    def get_text(self , event):
        text = self.qr_entry.get()
        print(text)
        qr_code = self.qr.scrap(text)
        model = self.combo.get()
        validate = self.qr.validation(qr_code , model)
        if validate:
            self.qr.mysql_insert(qr_code)
        else:
            self.reply('Converter Housing Model different than expected!')
        self.qr_entry.delete(0,'end')
        self.last_10()
            


if __name__ == '__main__':
    
    root = Tk()
    root.title('Kodaco QRCode tracking')
    root.configure(background=color)
    gui = Interface(root)

    root.mainloop()
    

    


