#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 12 11:37:39 2017

@author: GJ
"""

import Tkinter as tk
import tkMessageBox
import tkFileDialog
import RunNc
import threading
import Queue
import commands as cmd
import time
import os

class CreateWinNc(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        self.createMenu()
        window["menu"]=self.menubar   
        self.fname = ''
         
#==============================================================================
# 创建窗体       
#==============================================================================
    def createWidgets(self):
        #label1
        tk.Label(self, text='', font=('Consolas', 16), width= 10, height=6).grid(row=0,column=0)

        tk.Label(self, text='', font=('Consolas', 16), width= 10, height=6).grid(row=2,column=0)
        tk.Label(self, text='File: ', font=('Consolas', 16), width= 10).grid(row=1,column=0)
        tk.Label(self, text='Status: ', font=('Consolas', 16), width= 10).grid(row=3,column=0)
        #file path entry
        self.entryfile = tk.Entry(self, text = 'please choose .dmp files',font=('Consolas', 16), state = 'normal', width=50)
        self.entryfile.grid(row=1,column=1)
        #state label
        self.stateLab =tk.Label(self, text = 'Nanocubes', font=('Consolas', 16), bg='springgreen',wraplength=500, anchor='w', width=50,height=2)   
        self.stateLab.grid(row=3,column=1)  

    def createMenu(self):
        self.menubar = tk.Menu(window,font=('Consolas', 18))
        #filemenu
        self.filemenu = tk.Menu(self.menubar, font=('Consolas', 18), tearoff=0)
        self.menubar.add_cascade(label='File', menu=self.filemenu)
        self.filemenu.add_command(label='OpenDMP', command=self.OpenDMP)
        self.filemenu.add_command(label='OpenCSV', command=self.OpenCSV)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Exit', command=window.destroy)
        
        #editmenu
        self.editmenu = tk.Menu(self.menubar,font=('Consolas', 18), tearoff=0)
        self.menubar.add_cascade(label='Edit', menu=self.editmenu)
        self.editmenu.add_command(label='CSVtoDMp', command=self.CSVtoDMp)
        
        #runmenu
        self.runmenu = tk.Menu(self.menubar, font=('Consolas', 18), tearoff=0)
        self.menubar.add_cascade(label='Run', menu=self.runmenu)
        self.runmenu.add_command(label='RunNC', command=self.RunNC)
        self.runmenu.add_command(label='Show', command=self.ShowResult)
        self.runmenu.add_separator()
        self.runmenu.add_command(label='Stop', command=self.StopRun)
 
#==============================================================================
# 打开文件
#==============================================================================
    #open DMP file
    def OpenDMP(self):
        self.fname = tkFileDialog.askopenfilename(initialdir = '/home/gj/nanocube-3.2.1/data')
        print self.fname
        self.entryfile.delete(0,tk.END)
        if self.fname.endswith('.dmp'):
            self.entryfile.delete(0,tk.END)
            self.entryfile.insert(0,self.fname)
            self.stateLab['text']='open success'
        else:
            self.stateLab["text"] = 'please choose dmp file'
            
    #open csv file
    def OpenCSV(self):
        self.fname = tkFileDialog.askopenfilename(initialdir = '/home/gj/nanocube-3.2.1/data')
        print self.fname
        self.entryfile.delete(0,tk.END)
        self.var_stat_info = 'open success'
        if self.fname.endswith('.csv'):
            self.entryfile.delete(0,tk.END)
            self.entryfile.insert(0,self.fname)
            self.stateLab['text'] = 'open success, converting CSV files into nanocube-ready DMP files'    #插入内容到text文本框中 
        else:
            self.stateLab['text'] = 'please choose csv file for conversion'  #插入内容到text文本框中

#==============================================================================
# CSV文件转DMP文件
#==============================================================================
    #convert csv file to dmp
    def CSVtoDMp(self):
        if self.fname =='':
            return
        column = RunNc.CSVtoDMP(self.fname)
        column.insert(0,'default')
        CSVwind = tk.Tk()
        CSVwind.title('CSV to DMP')
        CSVwind.geometry('450x700')
        
        #sep timecol latcol loncol catcol
        l1 = tk.Label(CSVwind, text='sep    ',font=('Consolas', 16), width=10,height=2).grid(row=0,column=0)
        l2 = tk.Label(CSVwind, text='timecol',font=('Consolas', 16), width=10,height=2).grid(row=1,column=0)
        l3 = tk.Label(CSVwind, text='latcol ',font=('Consolas', 16), width=10,height=2).grid(row=2,column=0)
        l4 = tk.Label(CSVwind, text='loncol ',font=('Consolas', 16), width=10,height=2).grid(row=3,column=0)
        l5 = tk.Label(CSVwind, text='catcol ',font=('Consolas', 16), width=10,height=2).grid(row=4,column=0)
        
        #listbox
        lb1 = tk.Listbox(CSVwind, font=('Consolas', 16), width=15, height=3)
        for iterm in ['default',',','|']:
            lb1.insert('end',iterm)
        lb1.grid(row=0,column=1)
        
        lb2 = tk.Listbox(CSVwind, font=('Consolas', 16), width=15,height=5)
        for iterm in column:
            lb2.insert('end',iterm)
        lb2.grid(row=1,column=1)
        
        lb3 = tk.Listbox(CSVwind, font=('Consolas', 16), width=15,height=5)
        for iterm in column:
            lb3.insert('end',iterm)
        lb3.grid(row=2,column=1)
        
        lb4 = tk.Listbox(CSVwind, font=('Consolas', 16), width=15,height=5)
        for iterm in column:
            lb4.insert('end',iterm)
        lb4.grid(row=3,column=1)
        
        lb5 = tk.Listbox(CSVwind, font=('Consolas', 16), width=15,height=5)
        for iterm in column:
            lb5.insert('end',iterm)
        lb5.grid(row=4,column=1)
        
        params = {'sep':'', 'timecol':''}

        def Confirm1():
            ch = lb1.get(lb1.curselection()).strip('\r')  
            if ch == 'default':
                params['sep'] = ' '
            else:
                params['sep'] = ch 
        def Confirm2():
            params['timecol'] = lb2.get(lb2.curselection()).strip('\r') 
        def Confirm3():
            params['latcol'] = lb3.get(lb3.curselection()).strip('\r')  
        def Confirm4():
            params['loncol'] = lb4.get(lb4.curselection()).strip('\r')  
        def Confirm5():
            params['catcol'] = lb5.get(lb5.curselection()).strip('\r')

        def Convert():
            resultstatus = Queue.Queue()
            if self.fname.endswith('.csv'):
                self.thread_Convert = threading.Thread(target=self.DoConvert,args=(params, self.fname, resultstatus))
                self.thread_Convert.start()
                if resultstatus.get() == 0:
                    self.stateLab['text']='Conversion Sucess!'
                    CSVwind.destroy()
                else:
                    self.stateLab['text']='Conversion Error'
                    CSVwind.destroy()

        bt1 = tk.Button(CSVwind,text='Confirm', font=('Consolas', 16), width=5, command=Confirm1).grid(row=0,column=2)
        bt2 = tk.Button(CSVwind,text='Confirm', font=('Consolas', 16), width=5, command=Confirm2).grid(row=1,column=2)
        bt3 = tk.Button(CSVwind,text='Confirm', font=('Consolas', 16), width=5, command=Confirm3).grid(row=2,column=2)
        bt4 = tk.Button(CSVwind,text='Confirm', font=('Consolas', 16), width=5, command=Confirm4).grid(row=3,column=2)
        bt5 = tk.Button(CSVwind,text='Confirm', font=('Consolas', 16), width=5, command=Confirm5).grid(row=4,column=2)
        bt5 = tk.Button(CSVwind,text='Convert', font=('Consolas', 16), width=5, command=Convert).grid(row=5,column=1)

        CSVwind.mainloop()
        
    def DoConvert(self, params, fname, resultstatus):
        fname_new = fname.replace('csv', 'dmp')
        #command = r"cd $NANOCUBE_SRC/data " + r"nanocube-binning-csv --sep=%s --timecol=%s --latcol=%s --loncol=%s --catcol=%s %s > %s"%(params['sep'],params['timecol'], params['latcol'],params['loncol'], params['catcol'], fname, fname_new)
        #command =r"cd $NANOCUBE_SRC/data && nanocube-binning-csv   --sep=%s  --timecol=%s  --latcol=%s  --loncol=%s --catcol=%s %s > %s"%(params['sep'],params['timecol'], params['latcol'],params['loncol'], params['catcol'], fname, fname_new)
        command =r"cd $NANOCUBE_SRC/data && nanocube-binning-csv --sep=',' --latcol=latitude --loncol=longitude --timecol=time --catcol=device socialwebsite.csv > socialwebsite.dmp"
        l = os.popen(command)
        time.sleep(10)
        if type(l) == file:
            resultstatus.put(0)
        else:
            resultstatus.put(-1)

#==============================================================================
# 运行Nanocube      
#==============================================================================
    def RunNC(self):
        q = Queue.Queue()
        self.thread_RunNc = threading.Thread(target=RunNc.DoRunNc, args=(self.fname, q))
        if self.entryfile.get().endswith('.dmp'):
            self.stateLab['text'] = 'please waitting!'
            self.thread_RunNc.start()
            time.sleep(3)
            if q.get() == 0:  
                self.stateLab['text'] = 'Nanocubes sever is runnning!'
            else:
                self.stateLab['text'] = 'Error!'
        else:
            tkMessageBox.showerror(title='error!', message='No dmp file')
    
#==============================================================================
# 打开web浏览结果
#==============================================================================
    def ShowResult(self):
        threa_show = threading.Thread(target=RunNc.Showresult)
        threa_show.start()
        print(threading.active_count())

#==============================================================================
# 停止Nanocube服务
#==============================================================================
    def StopRun(self):
        q = Queue.Queue()
        threa_stop = threading.Thread(target=RunNc.Stop, args=(q,))
        threa_stop.start()
        if q.get() == 0:
            time.sleep(2)
            self.stateLab['text'] = 'Nanocubes sever is stopped'
        else:
            self.stateLab['text'] = 'Nanocubes sever is not runnning'

if __name__ == "__main__":
    window = tk.Tk()
    window.title('Nanocubes')
    window.geometry('690x400')
    app = CreateWinNc(master=window)
    app.mainloop()

    
