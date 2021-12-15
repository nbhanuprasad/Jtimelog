from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from .forms import formupload
import sys
from datetime import datetime, timedelta
from django.core.files import File
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from django.conf import settings
import numpy as np
import pandas as pd
from datetime import *
# Create your views here.
def Converting_to_secconds_to_hours(seconds):
    a = str(seconds // 3600)
    b = str((seconds % 3600) // 60)
    c = str((seconds % 3600) % 60)
    d = "{} hours {} mins {} seconds".format(a, b, c)
    return d


def function(line1,s):
    f = open(s,"r")
    lines = []
    dates = []
    data_line =[]
    while line1:
        line1 = f.readline()
        lines.append(line1)
    #splitting the lines to seperate the date
    for i in range(len(lines)):
        a = lines[i].split(': ')
        if len(a) == 2:
            dates.append(a[0])
            data_line.append(a[1])
        else:
            dates.append(np.NaN)
            data_line.append(a[0])
    return (dates,data_line)

def function1(filename):
    f = open(filename,"r")
    line = f.readline()
    #function to count the time used
    df = pd.DataFrame([])

    #Checking the condition for "TIME LOG:"
    while line:
        if line == 'Time Log:\n' :
            (dates,data_line) = function(line,filename)
            df['Date'] = dates
            df['Workdone'] = data_line
            break
        else:
            line = f.readline()
            print('Not Found')

    #############################
    #Changing the date in dataframe
    df['Date'].fillna( method ='ffill', inplace = True)

    start_time = []
    end_time = []
    mainpulation = []
    for i in df['Workdone'].values:
        a = i.split(' - ')
        if len(a) >= 2:
            mainpulation.append(a[1])
            start_time.append(a[0].strip())
        else:
            mainpulation.append(a[0])
            start_time.append('Notime')

    for i in mainpulation:
        a = i.split(' ',1)
        end_time.append(a[0])


    df['Start Time'] = start_time
    df['End Time'] = end_time

    #STEP 1 - removing the values which are not time

    # 0 - found
    # -1 any number - not found
    up = []

    for i in df['End Time']:
        a = i.find('am')
        b = i.find('pm')
        if a == -1 and b == -1 :
            up.append('Notime')
        else:
            up.append(i)

    # Cleaning end time
    up1 = []
    for i in up:
        if i == 'Notime':
            up1.append('Notime')
        else:
            a = str(i).split('\n')
            up1.append(a[0])
    df['End Time'] = up1
    ###################################
    df= df[df['End Time'] != 'Notime']

    #Creating the time format
    cn_st = []
    cn_et = []

    for i,j in zip(df['Start Time'],df['End Time']):
        cn_st.append(datetime.strptime(i,'%I:%M%p').time())
        cn_et.append(datetime.strptime(j,'%I:%M%p').time())


    #Calculating the time difference
    seconds = []
    for i,j in zip(cn_st,cn_et):
        time_1 = datetime.strptime(str(i),"%H:%M:%S")
        time_2 = datetime.strptime(str(j),"%H:%M:%S")
        seconds.append((time_2 - time_1).total_seconds())

    #Remonving the difference
    seconds_values = []
    for i in seconds:
        if i < 0:
            a = 86400 + i
            seconds_values.append(a)
        else:
            seconds_values.append(i)
    abcd=sum(seconds_values)
    return Converting_to_secconds_to_hours(abcd)
def parser(request):
    if request.method=='POST':
        form = formupload(request.POST, request.FILES)
        timefile=request.FILES['uploadedfile']
        path=default_storage.save('temp/temp.txt',ContentFile(timefile.read()))
        file_loc = os.path.join(settings.MEDIA_ROOT, path)
        timelogtime=function1(file_loc)
        msg = f'Total time from the uploaded <strong>{timefile}</strong> is {timelogtime}'
        os.remove(file_loc)
        return HttpResponse(msg)
        #
        #    return HttpResponse('Submitted')
    else:
        timefile= formupload()
        return render(request,"upload.html",{'formupload':timefile})
