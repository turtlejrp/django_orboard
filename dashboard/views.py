from multiprocessing import context
from django.http.response import HttpResponse
from django.db.models import Count
from django.shortcuts import render
from .models import Cycletime, PartNO
from lossreport.models import Loss
from datetime import date,time, datetime, timedelta
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.db.models import Q,Sum

Dayshift = {1: ["07:35", "08:30"], 2: ["08:30", "09:40"], 3: ["09:40", "10:30"], 4: ["10:30", "12:15"], 5: ["12:15", "13:30"], 6: ["13:30", "14:40"],
            7: ["14:40", "15:30"], 8: ["15:30", "16:50"], 9: ["16:50", "17:50"], 10: ["17:50", "18:50"], 11: ["18:50", "19:20"]}
Nightshift = {1: ["19:35", "20:30"], 2: ["20:30", "21:40"], 3: ["21:40", "22:30"], 4: ["22:30", "23:59"], 5: ["00:00", "01:30"], 6: ["01:30", "02:50"],
              7: ["02:50", "03:30"], 8: ["03:30", "04:50"], 9: ["04:50", "05:50"], 10: ["05:50", "06:50"], 11: ["06:50", "07:20"]}
shifttimeday = [3300, 3600, 3000, 2700, 4500, 3600, 3000, 3600, 3600, 3000, 1800]
shifttimenight = [3300, 3600, 3000, 2700, 4500, 3600, 3000, 3600, 3600, 3000, 1800]

# Create your views here.
def orboard(request):
     #set date
    try:
        dateselect = request.POST.get('date')
        CurrentDate = datetime.strptime(dateselect, "%Y-%m-%d").date()
    except:
        CurrentDate = date.today()

    if CurrentDate.month < 10:
        month = '0'+str(CurrentDate.month)
    else:
        month = str(CurrentDate.month)

    if CurrentDate.day < 10:
        day = '0'+str(CurrentDate.day)
    else:
        day = str(CurrentDate.day)

    datedefault= str(CurrentDate.year)+"-"+month+"-"+day
    DateToday = CurrentDate.strftime("%d %B %Y")

    #get currenttime
    CurrentTime = datetime.now().time()
    sec = CurrentTime.hour*3600 + CurrentTime.minute*60 + CurrentTime.second

    #config Shift
    if 'day' in request.POST: 
        #night shift
        toggle = False
        if CurrentDate > date.today() :
            sec = 70501
        elif CurrentDate < date.today():
            CurrentDate = CurrentDate + timedelta(days=1)
            sec = 26400
        elif 27300<sec<70500:
            sec = 70501
    else:
        #day shift
        toggle = True
        if CurrentDate > date.today() :
            sec = 27301
        elif CurrentDate < date.today():
            sec = 69600
    
    if toggle:
        OR_Actual,  OR_Target,  Output_Actual,  Output_Target, OP_DIFF, STD_Target,  CT_Actual, lastpart, Plan, Actual, ORshift, Colorchart,losssum,status = calORday(
            CurrentDate, sec)
    else:
        OR_Actual,  OR_Target,  Output_Actual,  Output_Target, OP_DIFF, STD_Target,  CT_Actual, lastpart, Plan, Actual, ORshift, Colorchart,losssum,status = calORnight(
            CurrentDate, sec)
    

    
    # Demo Data part
    partno = '1234'
    start_time = datetime.strptime('08:15:00', '%H:%M:%S').time()
    current_time = datetime.now().time()
    start_datetime = datetime.combine(datetime.today(), start_time)
    end_datetime = datetime.combine(datetime.today(), current_time)
    cycle_time = []
        
    current_datetime = start_datetime

    while current_datetime <= end_datetime:
        cycle_time.append({
            'partno': partno,
            'create_at_time': current_datetime.time(),
        })
        current_datetime += timedelta(minutes=2)
    
    
    for cycletime_data in cycle_time:
            cycletime = Cycletime.objects.get_or_create(**cycletime_data)
    # Demo Data part

    context = {'OR_Actual': OR_Actual, 'OR_Target': OR_Target, 'Output_Actual': Output_Actual, 'Output_Target': Output_Target,
               'OP_DIFF': OP_DIFF, 'STD_Target': STD_Target, 'CT_Actual': CT_Actual, 'Cur_Part': lastpart, 'Plan': json.dumps(Plan, cls=DjangoJSONEncoder),
               'Actual': json.dumps(Actual, cls=DjangoJSONEncoder), 'ORShift': json.dumps(ORshift, cls=DjangoJSONEncoder),
               'color': json.dumps(Colorchart, cls=DjangoJSONEncoder), 'datedefault':datedefault,
               'DateToday': DateToday, 'shift': toggle,'Loss':losssum,"Status":status}
    request.session['datedefault'] = datedefault
    request.session['shift'] = toggle
    return render(request, 'dashboard/orboard.html', context)


def calORday(CurrentDate, sec):
    Target_Time = 0
    Plan = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    Actual = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    Colorchart = list()
    ORshift = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if 27300 <= sec <= 30600:  # 7.35-8.30
        shift = 1
        startshift = 27300
    elif 30600 < sec <= 34800:  # 8.30-9.30
        shift = 2
        startshift = 27300
    elif 34800 < sec <= 37800:  # 9.40-10.30
        shift = 3
        startshift = 27900
    elif 37800 < sec <= 44100:  # 10.30-11.15
        shift = 4
        startshift = 27900
    elif 44100 < sec <= 48600:  # 12.15-13.30
        shift = 5
        startshift = 31500
    elif 48600 < sec <= 52800:  # 13.30-14.30
        shift = 6
        startshift = 31500
    elif 52800 < sec <= 55800:  # 14.40-15.30
        shift = 7
        startshift = 32100
    elif 55800 < sec <= 60600:  # 15.30-16.30
        shift = 8
        startshift = 32100
    elif 60600 < sec <= 64200:  # 16.50-17.50
        shift = 9
        startshift = 33300
    elif 64200 < sec <= 67200:  # 17.50-18.40
        shift = 10
        startshift = 33300
    else:  # 18.50-19.20
        shift = 11
        startshift = 33900
    ACC_Worktime = sec - startshift
    allproblem = Loss.objects.filter(create_at_date=CurrentDate,create_at_time__range=["07:35", "19:20"]).aggregate((Sum('duration')))
    if allproblem['duration__sum'] is None:
        losssum = 0
    else:
        losssum = round((allproblem['duration__sum']*6000)/sec,2)
    partgroup = Cycletime.objects.values('partno').annotate(
        dcount=Count('partno')).filter(create_at_date=CurrentDate, create_at_time__gte="07:30", create_at_time__lte="19:20")
    Output_Actual = Cycletime.objects.filter(
        create_at_date=CurrentDate, create_at_time__gte="07:30", create_at_time__lte="19:20").count()
    lastpart = Cycletime.objects.last().partno
    for part in partgroup:
        try:
            ct = PartNO.objects.get(partnumber=part['partno'])
            Target_Time += ct.cycletime*part['dcount']
        except:
            Target_Time += 55*a['dcount']
    if Output_Actual == 0:
        STD_Target = 60
        CT_Actual = 0
    else:
        STD_Target = round(Target_Time/Output_Actual, 2)
        CT_Actual = round(ACC_Worktime/Output_Actual, 2)
    Output_Target = int(ACC_Worktime/STD_Target)
    OP_DIFF = int(Output_Actual-Output_Target)
    if OP_DIFF >= 0 :
        status = "ON TIME"
    else:
        status = "DELAY"
    for a in range(shift):
        part_per_shift = Cycletime.objects.filter(
            create_at_date=CurrentDate, create_at_time__range=[Dayshift[a+1][0], Dayshift[a+1][1]])
        Actual[a] += part_per_shift.count()
        if part_per_shift.count()==0:
            ACC_Worktime -= shifttimeday[a]
        cycletime_per_shift = Cycletime.objects.values('partno').annotate(dcount=Count('partno')).filter(
            create_at_date=CurrentDate, create_at_time__range=[Dayshift[a+1][0], Dayshift[a+1][1]])
        for b in cycletime_per_shift:
            try:
                ctshift = PartNO.objects.get(partnumber=b['partno'])
                ORshift[a] += round((ctshift.cycletime *
                                    b['dcount']*100/shifttimeday[a]), 2)
            except:
                ORshift[a] += round((55 *
                                    b['dcount']*100/shifttimeday[a]), 2)
        Plan[a] += int(shifttimeday[a]*0.92/STD_Target)
        if Actual[a] >= Plan[a]:
            Colorchart.append("aquamarine")
        else:
            Colorchart.append("#FF6384")
    if ACC_Worktime == 0:
        OR_Actual = 0
    else:
        OR_Actual = round((Target_Time/abs(ACC_Worktime))*100, 2)
    OR_Target = 92
    return OR_Actual,  OR_Target,  Output_Actual,  Output_Target, OP_DIFF, STD_Target,  CT_Actual, lastpart, Plan, Actual, ORshift, Colorchart,losssum,status


def calORnight(CurrentDate, sec):
    Target_Time = 0
    Plan = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    Actual = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    Colorchart = list()
    ORshift = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if 27300 <= sec <= 73800:  # 19.35-20.30
        shift = 1
        startshift = 70500
    elif 73800 <= sec <= 77400:  # 20.30-21.30
        shift = 2
        startshift = 70500
    elif 77400 <= sec <= 81000:  # 21.40-22.30
        shift = 3
        startshift = 71100
    elif 81000 <= sec <= 84600:  # 22.30-23.30
        shift = 4
        startshift = 71100
    elif 84600 <= sec <= 86400 or 0 <= sec <= 5400:  # 00.20-01.30
        shift = 5
        startshift = 1200
    elif 5400 <= sec <= 9000:  # 01.30-02.30
        shift = 6
        startshift = 1200
    elif 9000 <= sec <= 12600:  # 02.50-03.30
        shift = 7
        startshift = 2400
    elif 12600 <= sec <= 16200:  # 03.30-04.30
        shift = 8
        startshift = 2400
    elif 17400 <= sec <= 21000:  # 04.50-05.50
        shift = 9
        startshift = 3600
    elif 21000 <= sec <= 24000:  # 05.50-06.40
        shift = 10
        startshift = 3600
    else:  # 06.50-07.20
        shift = 11
        startshift = 4200
    if sec > 70000:
        ACC_Worktime = abs(sec - startshift)
        partgroup = Cycletime.objects.values('partno').annotate(
            dcount=Count('partno')).filter(create_at_date=CurrentDate, create_at_time__gte="19:30", create_at_time__lte="23:59")
        Output_Actual = Cycletime.objects.filter(
            create_at_date=CurrentDate, create_at_time__gte="19:30", create_at_time__lte="23:59").count()
        allproblem = Loss.objects.filter(create_at_date=CurrentDate,create_at_time__range=["19:30", "23:59"]).aggregate((Sum('duration')))

    else:
        query = Q(create_at_date=CurrentDate-timedelta(days=1))
        query.add(Q(create_at_time__gte='19:20'), Q.AND)
        query2 = Q(create_at_date=CurrentDate)
        query2.add(Q(create_at_time__lte='07:20'), Q.AND)
        query.add(query2, Q.OR)
        ACC_Worktime = abs(sec - startshift + 12600)
        partgroup = Cycletime.objects.values('partno').annotate(
            dcount=Count('partno')).filter(query)
        Output_Actual = Cycletime.objects.filter(query).count()
        allproblem = Loss.objects.filter(query).aggregate((Sum('duration')))
    if allproblem['duration__sum'] is None:
        losssum = 0
    else:
        losssum = round((allproblem['duration__sum']*6000)/sec,2)
    lastpart = Cycletime.objects.last().partno
    for a in partgroup:
        try:
            ct = PartNO.objects.get(partnumber=a['partno'])
            Target_Time += ct.cycletime*a['dcount']
        except:
            Target_Time += 55*a['dcount']
    if Output_Actual == 0:
        STD_Target = 60
        CT_Actual = 0
    else:
        STD_Target = round(Target_Time/Output_Actual, 2)
        CT_Actual = round(ACC_Worktime/Output_Actual, 2)
    Output_Target = int(ACC_Worktime/STD_Target)
    OP_DIFF = int(Output_Actual-Output_Target)
    if OP_DIFF >= 0 :
        status = "ON TIME"
    else:
        status = "DELAY"
    if shift < 5:
        for a in range(shift):
            Day = CurrentDate
            part_per_shift = Cycletime.objects.filter(
                create_at_date=Day, create_at_time__range=[Nightshift[a+1][0], Nightshift[a+1][1]])
            if part_per_shift.count()==0:
                ACC_Worktime -= shifttimenight[a]
            Actual[a] += part_per_shift.count()
            cycletime_per_shift = Cycletime.objects.values('partno').annotate(dcount=Count('partno')).filter(
                create_at_date=Day, create_at_time__range=[Nightshift[a+1][0], Nightshift[a+1][1]])
            for b in cycletime_per_shift:
                try:
                    ctshift = PartNO.objects.get(partnumber=b['partno'])
                    ORshift[a] += round((ctshift.cycletime *
                                        b['dcount']*100/shifttimenight[a]), 2)
                except:
                    ORshift[a] += round((55*b['dcount']*100/shifttimenight[a]),2)
            Plan[a] += int(shifttimenight[a]/STD_Target)
            if Actual[a] >= Plan[a]:
                Colorchart.append("aquamarine")
            else:
                Colorchart.append("#FF6384")
    else:
        for a in range(shift):
            if a < 4:
                Day = CurrentDate-timedelta(days=1)
            else:
                Day = CurrentDate
            part_per_shift = Cycletime.objects.filter(
                create_at_date=Day, create_at_time__range=[Nightshift[a+1][0], Nightshift[a+1][1]])
            Actual[a] += part_per_shift.count()
            if part_per_shift.count()==0:
                ACC_Worktime -= shifttimenight[a]
            cycletime_per_shift = Cycletime.objects.values('partno').annotate(dcount=Count('partno')).filter(
                create_at_date=Day, create_at_time__range=[Nightshift[a+1][0], Nightshift[a+1][1]])
            for b in cycletime_per_shift:
                try:
                    ctshift = PartNO.objects.get(partnumber=b['partno'])
                    ORshift[a] += round((ctshift.cycletime *
                                        b['dcount']*100/shifttimenight[a]), 2)
                except:
                    ORshift[a] += round((55*b['dcount']*100/shifttimenight[a]),2)
            Plan[a] += int(shifttimenight[a]*0.92/STD_Target)
            if Actual[a] >= Plan[a]:
                Colorchart.append("aquamarine")
            else:
                Colorchart.append("#FF6384")
    if ACC_Worktime == 0:
        OR_Actual = 0
    else:
        OR_Actual = round((Target_Time/abs(ACC_Worktime))*100, 2)
    OR_Target = 92
    return OR_Actual,  OR_Target,  Output_Actual,  Output_Target, OP_DIFF, STD_Target,  CT_Actual, lastpart, Plan, Actual, ORshift, Colorchart,losssum,status
