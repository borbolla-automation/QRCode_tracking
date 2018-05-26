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
from tkinter.messagebox import showinfo
from GUI.template import MyGui
#import pyautogui

#from PIL import Image
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


class Interface:
    
    def __init__(self , master):
        self.master = master
        self.master.title = 'Kodaco QRCode tracking'
        self.master.geometry("{0}x{1}+0+0".format(self.master.winfo_screenwidth(), self.master.winfo_screenheight()))
        
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
        
        #borbolla_logo = Image.open('images/borbolla_logo.png')
        #borbolla_logo = borbolla_logo.resize((250, 250), Image.ANTIALIAS)
        
        self.borbolla_logo = PhotoImage(file = 'images/borbolla_logo.png')
        self.logo_b_label = Label(self.master , image = self.borbolla_logo).grid(row = 20 , column = 20 , columnspan = 2 , sticky = NW ,)

        self.scan_label = Label(self.master , text = 'Please scan Converter housing QR Code!')
        self.scan_label.config(font=("Courier", 24))
        self.scan_label.grid(row = 1 , column = 1 ,columnspan = 6)

        self.qr_entry = Entry(self.master , )
        self.qr_entry.grid(row = 1 , column = 7 , columnspan = 8 , rowspan = 1 , sticky = NSEW)
        self.qr_entry.focus_set()

        self.kodaco_logo = PhotoImage(file = 'images/kodaco_logo.png')
        self.logo_k_label = Label(self.master , image = self.kodaco_logo).grid(row = 0 , column =20 , columnspan = 10 , sticky = NW ,)


        #self.last_10_label = Label(self.master , text = "\n")
        #self.last_10_label.grid(row = 2 , column = 1 , columnspan = 4 , rowspan = 4)
        self.last_10()
        self.qr = QRCodeRW('4G101' , 'I')

        self.master.bind('<Return>' , self.get_text)



    def reply(self , message):

        a = showinfo(title = 'MKDC' , message = message)  
        #a.after(3000 , press_enter)
        
        
    def last_10(self):
        pieces = Piece.select().order_by(Piece.date_added.desc()).limit(10)
        header = 'ID\tMODEL\tLINE\tSHIFT\tCASTING DATE\tMANUF_DATE'
        header = header.split('\t')
        print(header)
        info = []
        info.append(header)
        for piece in pieces:
            info.append([piece.id , piece.model.name , piece.line.alias , piece.shift.alias , piece.casting_date , piece.date_added])
        #label_text = header
        print(info)
        print('lenght = %s' % len(pieces))
        height = len(pieces)+1
        if height >10 : height = 10
        width = 6
        for i in range(height): #Rows
            for j in range(width): #Columns
                print('[%s,%s]'%(i,j))
                b = Label(self.master, text=info[i][j])
                b.grid(row=i+4, column=j+1)



        '''for piece in pieces:
            row = (piece.id , piece.model.name , piece.line.alias , piece.shift.alias , piece.casting_date , piece.date_added)
            for data in row :
                labels.append(Label(self.master , text = data))
            
            for label in labels:
                label.grid(row = i , column = j , columnspan = 1 , rowspan = 1)    
                j+=1
                print('i,j = ',i,j)
            i+=1
            print('i = ' , i)'''

        '''for piece in pieces:
                                    label_text = label_text+'\n\t\t%s\t%s\t%s\t%s\t%s\t%s'%(piece.id , piece.model.name , piece.line.alias , piece.shift.alias , piece.casting_date , piece.date_added)'''

        #self.last_10_label.config(text=label_text)



    def hello(self):
        print("Holle!!")

    def press_enter(self):
        pyautogui.press('enter')    

    def get_text(self , event):
        text = self.qr_entry.get()
        print(text)
        qr_code = self.qr.scrap(text)
        validate = self.qr.validation(qr_code)
        if validate:
            self.qr.mysql_insert(qr_code)
        else:
            self.reply('Converter Housing Model different than expected!')
        self.qr_entry.delete(0,'end')
        last_10()
            


if __name__ == '__main__':

    root = Tk()
    gui = Interface(root)
    root.mainloop()
    
"""
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


"""

                

        
    


