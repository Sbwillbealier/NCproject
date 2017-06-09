# -*- coding: utf-8 -*-
"""

"""
import os
import webbrowser
import commands as cmd
#==============================================================================
# functions of Run
#==============================================================================
def RunNc(path):
#    url = r'http://localhost:29512/count'
    command = 'cat %s | nanocube-leaf -q 29512 -f 10000'%(path)
    tmp = os.popen(command).readline()
    if tmp != '':
        com1 = r'ncwebviewer-config -s http://localhost:29512 -o $NANOCUBE_SRC/extra/nc_web_viewer/config_crime.json'
        com2 = r'cd $NANOCUBE_SRC/extra/nc_web_viewer && python -m SimpleHTTPServer 8000'
        os.system(com1)
        os.system(com2)
#    webbrowser.open(url,new = 0)

def DoRunNc(path, q):
#    path = r'/home/gj/nanocube-3.2.1/data/crime50k.dmp'
    command = 'cat %s | nanocube-leaf -q 29512 -f 10000'%(path)
    tmp = os.popen(command)
    if type(tmp) == file:
        com1 = r'ncwebviewer-config -s http://localhost:29512 -o $NANOCUBE_SRC/extra/nc_web_viewer/config_crime.json' 
        com2 = r"cd $NANOCUBE_SRC/extra/nc_web_viewer;python -m SimpleHTTPServer 8000"
        tmp1 = cmd.getstatusoutput(com1)
        tmp2 = os.popen(com2)
        if tmp1[0] == 0 and type(tmp2)==file:
            q.put(0)
        else:
            q.put(-1)

def Showresult():
    url = r'http://localhost:8000/#config_crime'
    webbrowser.open(url,new=1)

#==============================================================================
# 停止进程功能实现
#==============================================================================
def Stop(q):
    tep1 = cmd.getstatusoutput(r'lsof -i:29512')
    tep2 = cmd.getstatusoutput(r'lsof -i:8000')
    if tep1[0]==0 and tep2[0]==0:
        a1 = []
        for i in tep1[1].split(' '):
            if i!='':
                a1.append(i)
        b1 = []
        for i in tep2[1].split(' '):
            if i!='':
                b1.append(i)
            
        comm1 = r"kill -9 %s"%(a1[9])
        comm2 = r'kill -9 %s'%(b1[9])
        tep3 = os.popen(comm1)
        tep4 = os.popen(comm2)
        if type(tep3) ==file and type(tep4) ==file:
            q.put(0)
        else:
            q.put(-1)
#==============================================================================
# functions of convert
#==============================================================================
def CSVtoDMP(fname):
    with open(fname,mode='r') as f:
        fistline = f.readline().strip('\n')
    column = fistline.split(',')
    return column

#==============================================================================
# def Convert(params,fname):
# #    params = {'sep':',','timecol':'time','latcol':'Latitude','loncol':'Longitude','catcol':'crime'}
# #    fname='/home/gj/crime50k.csv'
#     fname_new = fname.replace('csv', 'dmp')
#     command = r"cd $NANOCUBE_SRC/data " + r"nanocube-binning-csv --sep=%s --timecol=%s --latcol=%s --loncol=%s --catcol=%s %s > %s"%(params['sep'],params['timecol'], params['latcol'],params['loncol'], params['catcol'], fname, fname_new)
#     l = cmd.getstatusoutput(command)
#     if l[0] == 0:
#         resultstatus.put(0)
#     else:
#         resultstatus.put(-1)
#==============================================================================
#==============================================================================
# end of convert
#==============================================================================
if __name__ == '__main__':
    pass