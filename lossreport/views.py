from django.shortcuts import render
from multiprocessing import context
from .models import Loss
from django.db.models import Count
from datetime import datetime,date, timedelta
from dashboard.views import calORday,calORnight
from django.db.models import Sum,Q
from .forms import LossForm
from django.http import HttpResponseRedirect
# Create your views here.

def lossreport(request):
    form = LossForm()
    shiftTime = dict()
    shift = True
    #set date
    try:
        dateselect = request.POST.get('date')
        CurrentDate = datetime.strptime(dateselect, "%Y-%m-%d").date()
    except:
        dateselect = request.session['datedefault']
        CurrentDate = datetime.strptime(dateselect, "%Y-%m-%d").date()
        shift = request.session['shift']

    if 'problem' in request.POST:
        form = LossForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_loss = Loss()
            new_loss.problem = data['problem']
            new_loss.lossType = data['lossType']
            if data['lossType'] == 'changing':
                new_loss.ABCType = 'B'
            else:
                new_loss.ABCType = 'C'
            new_loss.duration = data['duration']
            new_loss.create_at_time = data['create_at_time']
            new_loss.create_at_date = data['create_at_date']
            new_loss.save()
            return HttpResponseRedirect('/report')

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
    if 'day' in request.POST or not shift: 
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
        shift = {1: ["07:35", "08:30"], 2: ["08:30", "09:30"], 3: ["09:40", "10:30"], 4: ["10:30", "11:15"], 5: ["12:15", "13:30"], 6: ["13:30", "14:30"],
            7: ["14:40", "15:30"], 8: ["15:30", "16:30"], 9: ["16:50", "17:50"], 10: ["17:50", "18:40"], 11: ["18:50", "19:20"]}
        allproblem = Loss.objects.filter(create_at_date=CurrentDate,create_at_time__range=["07:35", "19:20"]).aggregate((Sum('duration')))
        for a in shift:
            problems = Loss.objects.filter(create_at_date=CurrentDate, create_at_time__range=[shift[a][0], shift[a][1]])
            problemchart = Loss.objects.values('problem').annotate(sum=Sum(('duration'))).order_by('-sum').filter(create_at_date=CurrentDate,create_at_time__range=["07:35", "19:20"])
            shiftTime[a]={"time":shift[a][0]+"-"+shift[a][1]}
            prob = ""
            duration = 0
            shiftTime[a]["duration"] = duration
            shiftTime[a]["loss_percent"] = duration
            for p in problems:
                prob += p.problem+","
                duration += p.duration
                shiftTime[a]["problem"] = prob
                shiftTime[a]["duration"] = duration
                shiftTime[a]["loss_percent"] = round((duration*6000/sec),2)
    else:
        OR_Actual,  OR_Target,  Output_Actual,  Output_Target, OP_DIFF, STD_Target,  CT_Actual, lastpart, Plan, Actual, ORshift, Colorchart,losssum = calORnight(
            CurrentDate, sec)
        shift = {1: ["19:35", "20:30"], 2: ["20:30", "21:30"], 3: ["21:40", "22:30"], 4: ["22:30", "23:30"], 5: ["00:20", "01:30"], 6: ["01:30", "02:30"],
              7: ["02:50", "03:30"], 8: ["03:30", "04:30"], 9: ["04:50", "05:50"], 10: ["05:50", "06:40"], 11: ["06:50", "07:20"]}
        if sec >70000:
            allproblem = Loss.objects.filter(create_at_date=CurrentDate,create_at_time__range=["19:30", "23:59"]).aggregate((Sum('duration')))
            problemchart = Loss.objects.values('problem').annotate(sum=Sum(('duration'))).order_by('-sum').filter(create_at_date=CurrentDate,create_at_time__range=["19:35", "23:59"])
            for a in shift:
                if a <5:
                    problems = Loss.objects.filter(create_at_date=CurrentDate, create_at_time__range=[shift[a][0], shift[a][1]])
                shiftTime[a]={"time":shift[a][0]+"-"+shift[a][1]}
                prob = ""
                duration = 0
                shiftTime[a]["duration"] = duration
                shiftTime[a]["loss_percent"] = duration
                for p in problems:
                    prob += p.problem+","
                    duration += p.duration
                    shiftTime[a]["problem"] = prob
                    shiftTime[a]["duration"] = duration
                    shiftTime[a]["loss_percent"] = round((duration*6000/sec),2)
        else:
            query = Q(create_at_date=CurrentDate-timedelta(days=1))
            query.add(Q(create_at_time__gte='19:20'), Q.AND)
            query2 = Q(create_at_date=CurrentDate)
            query2.add(Q(create_at_time__lte='07:20'), Q.AND)
            query.add(query2, Q.OR)
            allproblem = Loss.objects.filter(query).aggregate((Sum('duration')))
            problemchart = Loss.objects.values('problem').annotate(sum=Sum(('duration'))).order_by('-sum').filter(query)
            for a in shift:
                if a <5:
                    problems = Loss.objects.filter(create_at_date=CurrentDate-timedelta(days=1), create_at_time__range=[shift[a][0], shift[a][1]])
                else:
                    problems = Loss.objects.filter(create_at_date=CurrentDate, create_at_time__range=[shift[a][0], shift[a][1]])
                shiftTime[a]={"time":shift[a][0]+"-"+shift[a][1]}
                prob = ""
                duration = 0
                shiftTime[a]["duration"] = duration
                shiftTime[a]["loss_percent"] = duration
                for p in problems:
                    prob += p.problem+","
                    duration += p.duration
                    shiftTime[a]["problem"] = prob
                    shiftTime[a]["duration"] = duration
                    shiftTime[a]["loss_percent"] = round((duration*6000/sec),2)

    for a in shift:
        shiftTime[a]["target"] = Plan[a-1]
        shiftTime[a]["actual"] = Actual[a-1]
    if allproblem['duration__sum'] is None:
        losssum = 0
        durationsum = 0
    else:
        durationsum = allproblem['duration__sum']
        losssum = round((allproblem['duration__sum']*6000)/sec,2)
    undefined = round(100-OR_Actual-losssum,2)
    context = {"or":OR_Actual,"loss":losssum,"undefined":undefined,'opactual':Output_Actual,'optarget':Output_Target,'durationsum':durationsum,
             'shifttime':shiftTime,'problemchart':problemchart,'datedefault':datedefault,'shift': toggle,'form':form}
    request.session['datedefault'] = datedefault
    request.session['shift'] = toggle
    return render(request, 'lossreport/lossreport.html',context)

def analyze(request):
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
    if request.POST:
        loss = Loss.objects.filter(create_at_date__gte=request.POST['start_date'], create_at_date__lte=request.POST['end_date']).order_by('-create_at_date')
        if request.POST['shift'] == 'day':
            loss = loss.filter(create_at_time__range=["07:35", "19:20"])
        elif request.POST['shift'] == 'night':
            loss = loss.filter(create_at_time__range=["00:00", "07:34"])|loss.filter(create_at_time__range=["19:21", "23:59"])

        if 'losstype' in request.POST:
            losstype = request.POST['losstype']
            loss = loss.filter(lossType__iexact=losstype)

        problemchart = loss.values('problem').annotate(sum=Sum(('duration'))).order_by('-sum')
        
        return render(request, 'lossreport/analyze.html',{'datedefault':datedefault,'loss':loss,'problemchart':problemchart})
        
    return render(request, 'lossreport/analyze.html',{'datedefault':datedefault})
