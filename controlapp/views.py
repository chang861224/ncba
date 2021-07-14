from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import auth
from django.http import HttpResponse
from django.contrib.auth.models import User, Permission, Group
from django.db.models import Q
from controlapp import models, sendmail
import random, string
import math
import datetime
import csv

page = 1

def register(request):
    message = ''
    
    if request.method == 'POST':
        username = request.POST['username']
        try:
            user = User.objects.get(username=username)
        except:
            user = None

        if user != None:
            message = '帳號已建立！請使用其他帳號註冊！'
            return render(request, 'register.html', locals())
        else:
            if request.POST['password'] != request.POST['password_confirm']:
                message = '密碼不相符！請再試一次！'
                return render(request, 'register.html', locals())
            else:
                user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                user.is_staff = False
                user.save()

                if request.POST['username'].split('_')[0] == 'team':
                    group = Group.objects.get(name='team')
                else:
                    group = Group.objects.get(name='guest')
                
                user.groups.add(group)
        return redirect('/index/')
    return render(request, 'register.html', locals())

def homepage(request):
    return redirect('/index/')

def index(request):
    try:
        game = models.GameUnit.objects.get(date=datetime.date.today(), postpone=False)
        try:
            order = models.OrderGuestUnit.objects.get(game__id=game.id)
            guest = []
            guest.append({'order': 1, 'number': order.first.split('_')[1], 'name': order.first.split('_')[2], 'pos': order.first.split('_')[3]})
            guest.append({'order': 2, 'number': order.second.split('_')[1], 'name': order.second.split('_')[2], 'pos': order.second.split('_')[3]})
            guest.append({'order': 3, 'number': order.third.split('_')[1], 'name': order.third.split('_')[2], 'pos': order.third.split('_')[3]})
            guest.append({'order': 4, 'number': order.fourth.split('_')[1], 'name': order.fourth.split('_')[2], 'pos': order.fourth.split('_')[3]})
            guest.append({'order': 5, 'number': order.fifth.split('_')[1], 'name': order.fifth.split('_')[2], 'pos': order.fifth.split('_')[3]})
            guest.append({'order': 6, 'number': order.sixth.split('_')[1], 'name': order.sixth.split('_')[2], 'pos': order.sixth.split('_')[3]})
            guest.append({'order': 7, 'number': order.seventh.split('_')[1], 'name': order.seventh.split('_')[2], 'pos': order.seventh.split('_')[3]})
            guest.append({'order': 8, 'number': order.eighth.split('_')[1], 'name': order.eighth.split('_')[2], 'pos': order.eighth.split('_')[3]})
            guest.append({'order': 9, 'number': order.nineth.split('_')[1], 'name': order.nineth.split('_')[2], 'pos': order.nineth.split('_')[3]})
            guestSP = {'number': order.SP.split('_')[1], 'name': order.SP.split('_')[2]}
            guestSubmit = order.submitTime
        except:
            guest = None
        try:
            order = models.OrderHomeUnit.objects.get(game__id=game.id)
            home = []
            home.append({'order': 1, 'number': order.first.split('_')[1], 'name': order.first.split('_')[2], 'pos': order.first.split('_')[3]})
            home.append({'order': 2, 'number': order.second.split('_')[1], 'name': order.second.split('_')[2], 'pos': order.second.split('_')[3]})
            home.append({'order': 3, 'number': order.third.split('_')[1], 'name': order.third.split('_')[2], 'pos': order.third.split('_')[3]})
            home.append({'order': 4, 'number': order.fourth.split('_')[1], 'name': order.fourth.split('_')[2], 'pos': order.fourth.split('_')[3]})
            home.append({'order': 5, 'number': order.fifth.split('_')[1], 'name': order.fifth.split('_')[2], 'pos': order.fifth.split('_')[3]})
            home.append({'order': 6, 'number': order.sixth.split('_')[1], 'name': order.sixth.split('_')[2], 'pos': order.sixth.split('_')[3]})
            home.append({'order': 7, 'number': order.seventh.split('_')[1], 'name': order.seventh.split('_')[2], 'pos': order.seventh.split('_')[3]})
            home.append({'order': 8, 'number': order.eighth.split('_')[1], 'name': order.eighth.split('_')[2], 'pos': order.eighth.split('_')[3]})
            home.append({'order': 9, 'number': order.nineth.split('_')[1], 'name': order.nineth.split('_')[2], 'pos': order.nineth.split('_')[3]})
            homeSP = {'number': order.SP.split('_')[1], 'name': order.SP.split('_')[2]}
            homeSubmit = order.submitTime
        except:
            home = None
    except:
        game = None

    newsall = models.NewsUnit.objects.filter(publish=True).order_by('-date')
    if len(newsall) > 5:
        newslist = newsall[:5]
    else:
        newslist = newsall
    datasize = len(newsall)
    return render(request, 'index.html', locals())

def newslist(request, pageindex=None):
    global page
    pagesize = 10
    newsall = models.NewsUnit.objects.filter(publish=True).order_by('-date')
    datasize = len(newsall)
    totalpage = math.ceil(datasize / pagesize)

    if pageindex == None:
        page = 1
        newslist = models.NewsUnit.objects.filter(publish=True).order_by('-date')[:pagesize]
    elif pageindex == '1':
        start = (page - 2) * pagesize

        if start >= 0:
            newslist = models.NewsUnit.objects.filter(publish=True).order_by('-date')[start:(start+pagesize)]
            page -= 1
    elif pageindex == '2':
        start = page * pageindex

        if start < datasize:
            newslist = models.NewsUnit.objects.filter(publish=True).order_by('date')[start:(start+pagesize)]
            page += 1
    elif pageindex == '3':
        start = (page - 1) * pagesize
        newslist = models.NewsUnit.objects.filter(publish=True).order_by('-date')[start:(start+pagesize)]

    currentpage = page
    return render(request, 'newslist.html', locals())

def news(request, newsid=None):
    news = models.NewsUnit.objects.get(id=newsid)
    news.press += 1
    news.save()
    return render(request, 'news.html', locals())

def schedule(request, year=None):
    if request.method == 'POST':
        return redirect('/schedule/' + request.POST['year'] + '/')

    teams = models.TeamUnit.objects.all().order_by('id')
    years = []
    for team in teams:
        if team.year not in years:
            years.append(team.year)

    if year == None:
        return redirect('/schedule/' + str(max(years)) + '/')

    years.sort(reverse=True)
    games = models.GameUnit.objects.filter(year=year).order_by('date')
    return render(request, 'schedule.html', locals())

def box(request, year=None, datestr=None, number=None):
    game = models.GameUnit.objects.get(year=year, number=number, date=datetime.datetime.strptime(datestr, '%Y-%m-%d'))
    score = models.ScoreUnit.objects.get(game__id=game.id)
    hitters = models.HitterUnit.objects.filter(number__id=game.id).order_by('id')
    pitchers = models.PitcherUnit.objects.filter(number__id=game.id).order_by('id')
    fielders = models.FielderUnit.objects.filter(number__id=game.id).order_by('id')

    GHit = 0
    GErr = 0
    HHit = 0
    HErr = 0

    for hitter in hitters:
        if hitter.player.team.id == game.guest.id:
            GHit += hitter.H
        elif hitter.player.team.id == game.home.id:
            HHit += hitter.H
    for fielder in fielders:
        if fielder.player.team.id == game.guest.id:
            GErr += fielder.E
        elif fielder.player.team.id == game.home.id:
            HErr += fielder.E

    WP = models.PitcherUnit.objects.filter(number__id=game.id, conseq='W')
    LP = models.PitcherUnit.objects.filter(number__id=game.id, conseq='L')
    SV = models.PitcherUnit.objects.filter(number__id=game.id, conseq='S')
    HO = models.PitcherUnit.objects.filter(number__id=game.id, conseq='H')
    BS = models.PitcherUnit.objects.filter(number__id=game.id, conseq='BS')
    return render(request, 'box.html', locals())

def standing(request, year=None):
    if request.method == 'POST':
        return redirect('/standing/' + request.POST['year'] + '/')

    teams = models.TeamUnit.objects.all().order_by('id')
    years = []
    for team in teams:
        if team.year not in years:
            years.append(team.year)

    if year == None:
        return redirect('/standing/' + str(max(years)) + '/')

    years.sort(reverse=True)
    groupA = models.TeamUnit.objects.filter(year=year, group='A').order_by('-PCT')
    groupB = models.TeamUnit.objects.filter(year=year, group='B').order_by('-PCT')
    return render(request, 'standing.html', locals())

def teams(request, year=None, teamid=None, itemtype=None):
    if request.method == 'POST':
        return redirect('/teams/' + str(year) + '/' + request.POST['team'] + '/' + itemtype + '/')

    teams = models.TeamUnit.objects.all().order_by('id')
    years = []
    for team in teams:
        if team.year not in years:
            years.append(team.year)

    if year == None:
        teams = models.TeamUnit.objects.filter(year=max(years)).order_by('id')
        return redirect('/teams/' + str(max(years)) + '/' + str(teams[0].id) + '/players/')

    years.sort(reverse=True)
    teams = models.TeamUnit.objects.filter(year=year).order_by('id')
    
    # DEBUG
    hitter_score_update(year=year)

    if teamid == None:
        return redirect('/teams/' + str(year) + '/' + str(teams[0].id) + '/players/')

    if itemtype == 'players':
        players = models.PlayerUnit.objects.filter(team__year=year, team__id=teamid).order_by('player__studentID')
    elif itemtype == 'hitters':
        hitters = models.PlayerHitterUnit.objects.filter(player__team__id=teamid).order_by('player__player__studentID')
    elif itemtype == 'fielders':
        fielders = models.PlayerFielderUnit.objects.filter(player__team__id=teamid).order_by('player__player__studentID')
    elif itemtype == 'picatchers':
        catchers = models.PlayerCatcherUnit.objects.filter(player__team__id=teamid).order_by('player__player__studentID')
        units = models.PlayerPitcherUnit.objects.filter(player__team__id=teamid).order_by('player__player__studentID')
        pitchers = []
        for player in units:
            pitchers.append({'model': player, 'innt': player.inn3 // 3, 'innf': player.inn3 % 3})
    return render(request, 'teams.html', locals())

def player(request, personid=None):
    player = models.PersonUnit.objects.get(id=personid)
    IDs = [player.studentID]
    for ID in IDs:
        for p in models.TransferUnit.objects.filter(Q(originalID=ID) | Q(newID=ID)):
            if p.originalID not in IDs:
                IDs.append(p.originalID)
            if p.newID not in IDs:
                IDs.append(p.newID)
    IDs.sort()

    person = models.PersonUnit.objects.filter(studentID__in=IDs).order_by('studentID')
    seasons = models.PlayerUnit.objects.filter(player__in=person).order_by('team__year')
    hitters = models.PlayerHitterUnit.objects.filter(player__player__in=person).order_by('player__team__year')
    fielders = models.PlayerFielderUnit.objects.filter(player__player__in=person).order_by('player__team__year')
    catchers = models.PlayerCatcherUnit.objects.filter(player__player__in=person).order_by('player__team__year')
    pitcherlist = models.PlayerPitcherUnit.objects.filter(player__player__in=person).order_by('player__team__year')
    pitchers = []
    for p in pitcherlist:
        pitchers.append({
            'year': p.player.team.year,
            'W': p.W,
            'L': p.L,
            'HO': p.HO,
            'S': p.S,
            'BS': p.BS,
            'inn3': p.inn3,
            'inn1': p.inn3 + 1,
            'inn2': p.inn3 + 2,
            'TPAF': p.TPAF,
            'TBF': p.TBF,
            'P': p.P,
            'CG': p.CG,
            'SHO': p.SHO,
            'no_walks': p.no_walks,
            'H': p.H,
            'HR': p.HR,
            'SH': p.SH,
            'SF': p.SF,
            'BB': p.BB,
            'IBB': p.IBB,
            'DB': p.DB,
            'K': p.K,
            'WP': p.WP,
            'BK': p.BK,
            'R': p.R,
            'ER': p.ER,
            'ERA': p.ERA,
            'WHIP': p.WHIP,
            'AVG': p.AVG,
            'OBA': p.OBA
        })
    return render(request, 'player.html', locals())

def rank(request, year=None):
    if request.method == 'POST':
        return redirect('/rank/' + request.POST['year'] + '/')

    teams = models.TeamUnit.objects.all().order_by('id')
    years = []
    for team in teams:
        if team.year not in years:
            years.append(team.year)

    if year == None:
        return redirect('/rank/' + str(max(years)) + '/')

    years.sort(reverse=True)

    AVG3 = models.PlayerHitterUnit.objects.filter(player__team__year=year, AB__gte=7).order_by('-AVG')
    if len(AVG3) > 3:
        AVG3 = AVG3[:3]
    
    SLG3 = models.PlayerHitterUnit.objects.filter(player__team__year=year, AB__gte=7).order_by('-SLG')
    if len(SLG3) > 3:
        SLG3 = SLG3[:3]

    RBI3 = models.PlayerHitterUnit.objects.filter(player__team__year=year).exclude(RBI=0).order_by('-RBI', 'PA')
    if len(RBI3) > 3:
        RBI3 = RBI3[:3]

    SB3 = models.PlayerHitterUnit.objects.filter(player__team__year=year).exclude(SB=0).order_by('-SB')
    if len(SB3) > 3:
        SB3 = SB3[:3]

    W3 = models.PlayerPitcherUnit.objects.filter(player__team__year=year).exclude(W=0).order_by('-W', 'ERA')
    if len(W3) > 3:
        W3 = W3[:3]

    K3 = models.PlayerPitcherUnit.objects.filter(player__team__year=year).exclude(K=0).order_by('-K', 'inn3')
    if len(K3) > 3:
        K3 = K3[:3]

    ERA3 = models.PlayerPitcherUnit.objects.filter(player__team__year=year, inn3__gte=23).order_by('ERA')
    if len(ERA3) > 3:
        ERA3 = ERA3[:3]
    return render(request, 'rank.html', locals())

def activity(request, eventid=None):
    if eventid == None:
        events = models.EventUnit.objects.all().order_by('-id')
        count = len(events)
    else:
        event = models.EventUnit.objects.get(id=eventid)

        if datetime.datetime.now() - datetime.datetime(event.startDate.year, event.startDate.month, event.startDate.day, 0, 0, 0, 0) < datetime.timedelta(microseconds=0):
            status = 'notyet'
        elif datetime.datetime.now() - datetime.datetime(event.endDate.year, event.endDate.month, event.endDate.day, 23, 59, 59, 999999) > datetime.timedelta(microseconds=0):
            status = 'expired'
        else:
            status = 'processing'

        if event.public == True:
            permit = True
        else:
            if request.user.is_authenticated and request.user.has_perm('auth.team') == False:
                permit = True
            else:
                permit = False

        if event.eventSelection:
            items = models.OptionUnit.objects.filter(event__id=eventid)

            if request.method == 'POST':
                email = request.POST['email']

                try:
                    repeat = models.VoterUnit.objects.get(option__event__id=eventid, email=email, confirm=True)
                except:
                    repeat = None

                if repeat == None:
                    unconfirm = models.VoterUnit.objects.filter(option__event__id=eventid, email=email, confirm=False)
                    for unit in unconfirm:
                        unit.delete()

                    randomkey = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(10))
                    checklist = request.POST.getlist('option')
                    
                    for item in checklist:
                        option = models.OptionUnit.objects.get(id=int(item))
                        vote = models.VoterUnit.objects.create(option=option, email=email, randomkey=randomkey)
                        vote.save()
                        sendmail.sendmail(email, str(eventid), randomkey)
                    return render(request, 'unconfirm.html', locals())
                else:
                    return redirect('/repeatvote/')
        elif event.eventChoice:
            items = models.OptionUnit.objects.filter(event__id=eventid)

            if request.method == 'POST':
                email = request.POST['email']

                try:
                    repeat = models.VoterUnit.objects.get(option__event__id=eventid, email=email, confirm=True)
                except:
                    repeat = None

                if repeat == None:
                    unconfirm = models.VoterUnit.objects.filter(option__event__id=eventid, email=email, confirm=False)
                    for unit in unconfirm:
                        unit.delete()

                    randomkey = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(10))

                    res = request.POST['option']
                    option = models.OptionUnit.objects.get(id=int(res))
                    vote = models.VoterUnit.objects.create(option=option, email=email, randomkey=randomkey)
                    vote.save()
                    sendmail.sendmail(email, str(eventid), randomkey)

                    return render(request, 'unconfirm.html', locals())
                else:
                    return redirect('/repeatvote/')
    return render(request, 'activity.html', locals())

def repeatvote(request):
    return render(request, 'repeatvote.html', locals())

def mailvote(request, eventid=None, randomkey=None):
    items = models.VoterUnit.objects.filter(option__event__id=eventid, randomkey=randomkey)

    if len(items) != 0:
        for item in items:
            if item.confirm == False:
                option = models.OptionUnit.objects.get(id=item.option.id)
                option.votes += 1
                option.save()
                item.confirm = True
                item.save()

        options = models.OptionUnit.objects.filter(event__id=eventid).order_by('id')
        total = sum(option.votes for option in options)
        if total != 0:
            for option in options:
                option.percent = option.votes / total * 100
                option.save()
    else:
        return render(request, 'urlnotexist.html', locals())
    return render(request, 'mailconfirm.html', locals())

def umpire(request, year=None):
    if request.method == 'POST':
        return redirect('/umpire/' + request.POST['year'] + '/')

    teams = models.TeamUnit.objects.all().order_by('id')
    years = []
    for team in teams:
        if team.year not in years:
            years.append(team.year)

    if year == None:
        return redirect('/umpire/' + str(max(years)) + '/')

    years.sort(reverse=True)
    umpires = models.PlayerUnit.objects.filter(team__year=year, umpire=True).order_by('team__id', 'player__studentID')
    return render(request, 'umpire.html', locals())

def login(request):
    message = ''

    if request.method == 'POST':
        username = request.POST['username'].strip()
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth.login(request, user)
                request.session['username'] = username
                request.session.set_expiry(18000)
                #if username.split('_')[0] == 'team':
                if request.user.has_perm('auth.team') and request.user.is_superuser == False:
                    # ORDER LIST
                    return redirect('/orderlist/' + username.split('_')[1] + '/')

                    # PLAYER ADD
                    #team = models.TeamUnit.objects.get(id=int(username.split('_')[1]))
                    return redirect('/playeradd/' + str(team.year) + '/' + str(team.id) + '/')
                elif request.user.has_perm('auth.member'):
                    return redirect('/option/')
                else:
                    return redirect('/index/')
            else:
                message = '帳號不存在！'
        else:
            message = '登入失敗！'
    return render(request, 'login.html', locals())

def logout(request):
    auth.logout(request)
    if 'username' in request.session:
        del request.session['username']
    return redirect('/login/')

def option(request):
    return render(request, 'option.html', locals())

def teamadd(request, year=None):
    message = ''
    teams = models.TeamUnit.objects.filter(year=year).order_by('id')

    if request.user.has_perm('auth.member'):
        if request.method == 'POST':
            team = request.POST['team']
            group = request.POST['group']
            captain1 = request.POST['captain1']
            captain2 = request.POST['captain2']

            unit = models.TeamUnit.objects.create(year=year, team=team, group=group, captain1=captain1, captain2=captain2)
            unit.save()
            message = '球隊 ' + team + ' 登錄成功'
            return redirect('/teamadd/' + str(year) + '/')
    else:
        return redirect('/option/')
    return render(request, 'teamadd.html', locals())

def teamedit(request, teamid=None):
    if request.user.has_perm('auth.member'):
        team = models.TeamUnit.objects.get(id=teamid)

        if request.method == 'POST':
            team.team = request.POST['team']
            team.group = request.POST['group']
            team.captain1 = request.POST['captain1']
            team.captain2 = request.POST['captain2']
            team.save()
            return redirect('/teamadd/' + str(team.year) + '/')
    else:
        return redirect('/option/')
    return render(request, 'teamedit.html', locals())

def teamdelete(request, teamid=None):
    if request.user.has_perm('auth.member'):
        team = models.TeamUnit.objects.get(id=teamid)
        year = team.year
        team.delete()
        return redirect('/teamadd/' + str(year) + '/')
    return redirect('/option/')

def playeradd(request, year=None, teamid=None):
    teams = models.TeamUnit.objects.filter(year=year).order_by('id')

    if request.user.has_perm('auth.member') or request.user.has_perm('auth.team'):
        if teamid == None:
            if request.method == 'POST':
                team = models.TeamUnit.objects.get(id=int(request.POST['team']))
                return redirect('/playeradd/' + str(year) + '/' + str(team.id) + '/')
        else:
            team = models.TeamUnit.objects.get(id=teamid)
            players = models.PlayerUnit.objects.filter(team__id=teamid).order_by('id')

            if request.method == 'POST':
                if request.POST['student_id_old'] != '':
                    try:
                        unit = models.TransferUnit.objects.get(originalID=request.POST['student_id_old'])
                        unit.newID = request.POST['student_id']
                        unit.save()
                    except:
                        unit = models.TransferUnit.objects.create(originalID=request.POST['student_id_old'], newID=request.POST['student_id'])
                        unit.save()
                else:
                    try:
                        unit = models.TransferUnit.objects.get(originalID=request.POST['student_id'])
                        unit.newID = request.POST['student_id']
                        unit.save()
                    except:
                        unit = models.TransferUnit.objects.create(originalID=request.POST['student_id'], newID=request.POST['student_id'])
                        unit.save()

                try:
                    player = models.PersonUnit.objects.get(studentID=request.POST['student_id'])
                    player.name = request.POST['name']
                    player.save()
                except:
                    player = models.PersonUnit.objects.create(name=request.POST['name'], studentID=request.POST['student_id'])
                    player.save()

                dept = request.POST['dept']
                number = request.POST['number']
                bt = request.POST['bt']

                unit = models.PlayerUnit.objects.create(team=team, player=player, dept=dept, number=number, bt=bt, umpire=False)
                unit.save()
                return redirect('/playeradd/' + str(year) + '/' + str(teamid) + '/')
    else:
        return redirect('/option/')
    return render(request, 'playeradd.html', locals())

def playeredit(request, edittype=None, playerid=None):
    if request.user.has_perm('auth.member') or request.user.has_perm('auth.team'):
        player = models.PlayerUnit.objects.get(id=playerid)
        team = player.team

        if edittype == 'delete':
            player.delete()
            return redirect('/playeradd/' + str(team.year) + '/' + str(team.id) + '/')
        elif edittype == 'edit':
            if request.method == 'POST':
                player.player.name = request.POST['name']
                player.dept = request.POST['dept']
                player.number = request.POST['number']
                player.bt = request.POST['bt']
                player.save()
                return redirect('/playeradd/' + str(team.year) + '/' + str(team.id) + '/')
    else:
        return redirect('/option/')
    return render(request, 'playeredit.html', locals())

def gameadd(request, year=None):
    teams = models.TeamUnit.objects.filter(year=year).order_by('id')
    games = models.GameUnit.objects.filter(year=year).order_by('date')

    if request.user.has_perm('auth.member'):
        if request.method == 'POST':
            number = request.POST['number']
            date = datetime.datetime.strptime(request.POST['game_date'], '%Y-%m-%d')
            guest = models.TeamUnit.objects.get(id=int(request.POST['guest']))
            home = models.TeamUnit.objects.get(id=int(request.POST['home']))
            umpire1 = request.POST['umpire1']
            umpire2 = request.POST['umpire2']
            umpire3 = request.POST['umpire3']
            if request.POST['type'] == 'playoff':
                playoff = True
                allstar = False
            elif request.POST['type'] == 'allstar':
                playoff = False
                allstar = True
            else:
                playoff = False
                allstar = False
            ps = request.POST.get('PS', '')

            unit = models.GameUnit.objects.create(year=year, number=number, date=date, guest=guest, home=home, umpire1=umpire1, umpire2=umpire2, umpire3=umpire3, playoff=playoff, allstar=allstar, ps=ps)
            unit.save()
            return redirect('/gameadd/' + str(year) + '/')
    else:
        return redirect('/option/')
    return render(request, 'gameadd.html', locals())

def gameedit(request, gameid=None, edittype=None):
    if request.user.has_perm('auth.member'):
        game = models.GameUnit.objects.get(id=gameid)
        year = game.year
        datestr = str(game.date)

        if edittype == 'postpone':
            game.umpire1 = ''
            game.umpire2 = ''
            game.umpire3 = ''
            game.regular = False
            game.postpone = True
            game.ps = request.POST.get('PS', '')
            game.save()
            return redirect('/gameadd/' + str(year) + '/')
        elif edittype == 'delete':
            try:
                score = models.ScoreUnit.objects.get(game__id=gameid)
            except:
                score = models.ScoreUnit.objects.create(game=game)
            score.delete()
            game.delete()
            return redirect('/gameadd/' + str(year) + '/')
        elif edittype == 'edit':
            teams = models.TeamUnit.objects.filter(year=year).order_by('id')
            
            if request.method == 'POST':
                game.number = request.POST['number']
                game.date = datetime.datetime.strptime(request.POST['game_date'], '%Y-%m-%d')
                game.guest = models.TeamUnit.objects.get(id=int(request.POST['guest']))
                game.home = models.TeamUnit.objects.get(id=int(request.POST['home']))
                game.umpire1 = request.POST['umpire1']
                game.umpire2 = request.POST['umpire2']
                game.umpire3 = request.POST['umpire3']
                if request.POST['type'] == 'playoff':
                    game.playoff = True
                    game.allstar = False
                elif request.POST['type'] == 'allstar':
                    game.playoff = False
                    game.allstar = True
                else:
                    game.playoff = False
                    game.allstar = False
                if request.POST['status'] == 'regular':
                    game.regular = True
                    game.postpone = False
                    game.finish = False
                elif request.POST['status'] == 'postpone':
                    game.regular = False
                    game.postpone = True
                    game.finish = False
                game.album = request.POST['album']
                game.ps = request.POST['PS']
                game.save()
                return redirect('/gameadd/' + str(year) + '/')
    else:
        return redirect('/option/')
    return render(request, 'gameedit.html', locals())

def addup(teamid=None):
    team = models.TeamUnit.objects.get(id=teamid)
    G = 0
    W = 0
    L = 0

    games = models.GameUnit.objects.filter(guest__id=teamid, playoff=False, finish=True)
    G += len(games)
    for game in games:
        if game.guestScore != None and game.homeScore != None:
            if game.guestScore > game.homeScore:
                W += 1
            else:
                L += 1

    games = models.GameUnit.objects.filter(home__id=teamid, playoff=False, finish=True)
    G += len(games)
    for game in games:
        if game.guestScore != None and game.homeScore != None:
            if game.homeScore > game.guestScore:
                W += 1
            else:
                L += 1

    team.G = G
    team.W = W
    team.L = L
    if team.G != 0:
        team.PCT = team.W / team.G
    else:
        team.PCT = None
    team.save()

def gamenotplay(request, year=None, gameid=None):
    if request.user.has_perm('auth.member'):
        game = models.GameUnit.objects.get(id=gameid)

        game.regular = True
        game.postpone = False
        game.finish = False
        game.guestScore = None
        game.homeScore = None
        game.save()

        try:
            score = models.ScoreUnit.objects.get(game__id=gameid)
        except:
            score = models.ScoreUnit.objects.create(game=game)

        score.delete()

        addup(game.guest.id)
        addup(game.home.id)
        return redirect('/boxadd/' + str(year) + '/')
    return redirect('/option/')

def lineuplist(request, year=None):
    if request.user.has_perm('auth.member'):
        games = models.GameUnit.objects.filter(year=year, postpone=False).order_by('date')
        return render(request, 'lineuplist.html', locals())
    return redirect('/option/')

def lineup(request, gameid=None):
    if request.user.has_perm('auth.member'):
        game = models.GameUnit.objects.get(id=gameid)
        try:
            guest = models.OrderGuestUnit.objects.get(game__id=gameid)

            guestLineup = []
            guestLineup.append({'order': 1, 'number': guest.first.split('_')[1], 'name': guest.first.split('_')[2], 'pos': guest.first.split('_')[3]})
            guestLineup.append({'order': 2, 'number': guest.second.split('_')[1], 'name': guest.second.split('_')[2], 'pos': guest.second.split('_')[3]})
            guestLineup.append({'order': 3, 'number': guest.third.split('_')[1], 'name': guest.third.split('_')[2], 'pos': guest.third.split('_')[3]})
            guestLineup.append({'order': 4, 'number': guest.fourth.split('_')[1], 'name': guest.fourth.split('_')[2], 'pos': guest.fourth.split('_')[3]})
            guestLineup.append({'order': 5, 'number': guest.fifth.split('_')[1], 'name': guest.fifth.split('_')[2], 'pos': guest.fifth.split('_')[3]})
            guestLineup.append({'order': 6, 'number': guest.sixth.split('_')[1], 'name': guest.sixth.split('_')[2], 'pos': guest.sixth.split('_')[3]})
            guestLineup.append({'order': 7, 'number': guest.seventh.split('_')[1], 'name': guest.seventh.split('_')[2], 'pos': guest.seventh.split('_')[3]})
            guestLineup.append({'order': 8, 'number': guest.eighth.split('_')[1], 'name': guest.eighth.split('_')[2], 'pos': guest.eighth.split('_')[3]})
            guestLineup.append({'order': 9, 'number': guest.nineth.split('_')[1], 'name': guest.nineth.split('_')[2], 'pos': guest.nineth.split('_')[3]})
            guestSP = {'number': guest.SP.split('_')[1], 'name': guest.SP.split('_')[2]}
            
            guestSubstitution = []
            
            if guest.substitute1 != None:
                guestSubstitution.append({'number': guest.substitute1.split('_')[1], 'name': guest.substitute1.split('_')[2]})
            else:
                guestSubstitution.append(None)
            
            if guest.substitute2 != None:
                guestSubstitution.append({'number': guest.substitute2.split('_')[1], 'name': guest.substitute2.split('_')[2]})
            else:
                guestSubstitution.append(None)
            
            if guest.substitute3 != None:
                guestSubstitution.append({'number': guest.substitute3.split('_')[1], 'name': guest.substitute3.split('_')[2]})
            else:
                guestSubstitution.append(None)
            
            if guest.substitute4 != None:
                guestSubstitution.append({'number': guest.substitute4.split('_')[1], 'name': guest.substitute4.split('_')[2]})
            else:
                guestSubstitution.append(None)
            
            if guest.substitute5 != None:
                guestSubstitution.append({'number': guest.substitute5.split('_')[1], 'name': guest.substitute5.split('_')[2]})
            else:
                guestSubstitution.append(None)
            
            if guest.substitute6 != None:
                guestSubstitution.append({'number': guest.substitute6.split('_')[1], 'name': guest.substitute6.split('_')[2]})
            else:
                guestSubstitution.append(None)
            
            if guest.substitute7 != None:
                guestSubstitution.append({'number': guest.substitute7.split('_')[1], 'name': guest.substitute7.split('_')[2]})
            else:
                guestSubstitution.append(None)
            
            if guest.substitute8 != None:
                guestSubstitution.append({'number': guest.substitute8.split('_')[1], 'name': guest.substitute8.split('_')[2]})
            else:
                guestSubstitution.append(None)
            
            if guest.substitute9 != None:
                guestSubstitution.append({'number': guest.substitute9.split('_')[1], 'name': guest.substitute9.split('_')[2]})
            else:
                guestSubstitution.append(None)
        except:
            guest = None
        try:
            home = models.OrderHomeUnit.objects.get(game__id=gameid)

            homeLineup = []
            homeLineup.append({'order': 1, 'number': home.first.split('_')[1], 'name': home.first.split('_')[2], 'pos': home.first.split('_')[3]})
            homeLineup.append({'order': 2, 'number': home.second.split('_')[1], 'name': home.second.split('_')[2], 'pos': home.second.split('_')[3]})
            homeLineup.append({'order': 3, 'number': home.third.split('_')[1], 'name': home.third.split('_')[2], 'pos': home.third.split('_')[3]})
            homeLineup.append({'order': 4, 'number': home.fourth.split('_')[1], 'name': home.fourth.split('_')[2], 'pos': home.fourth.split('_')[3]})
            homeLineup.append({'order': 5, 'number': home.fifth.split('_')[1], 'name': home.fifth.split('_')[2], 'pos': home.fifth.split('_')[3]})
            homeLineup.append({'order': 6, 'number': home.sixth.split('_')[1], 'name': home.sixth.split('_')[2], 'pos': home.sixth.split('_')[3]})
            homeLineup.append({'order': 7, 'number': home.seventh.split('_')[1], 'name': home.seventh.split('_')[2], 'pos': home.seventh.split('_')[3]})
            homeLineup.append({'order': 8, 'number': home.eighth.split('_')[1], 'name': home.eighth.split('_')[2], 'pos': home.eighth.split('_')[3]})
            homeLineup.append({'order': 9, 'number': home.nineth.split('_')[1], 'name': home.nineth.split('_')[2], 'pos': home.nineth.split('_')[3]})
            homeSP = {'number': home.SP.split('_')[1], 'name': home.SP.split('_')[2]}

            homeSubstitution = []

            if home.substitute1 != None:
                homeSubstitution.append({'number': home.substitute1.split('_')[1], 'name': home.substitute1.split('_')[2]})
            else:
                homeSubstitution.append(None)

            if home.substitute2 != None:
                homeSubstitution.append({'number': home.substitute2.split('_')[1], 'name': home.substitute2.split('_')[2]})
            else:
                homeSubstitution.append(None)

            if home.substitute3 != None:
                homeSubstitution.append({'number': home.substitute3.split('_')[1], 'name': home.substitute3.split('_')[2]})
            else:
                homeSubstitution.append(None)

            if home.substitute4 != None:
                homeSubstitution.append({'number': home.substitute4.split('_')[1], 'name': home.substitute4.split('_')[2]})
            else:
                homeSubstitution.append(None)

            if home.substitute5 != None:
                homeSubstitution.append({'number': home.substitute5.split('_')[1], 'name': home.substitute5.split('_')[2]})
            else:
                homeSubstitution.append(None)

            if home.substitute6 != None:
                homeSubstitution.append({'number': home.substitute6.split('_')[1], 'name': home.substitute6.split('_')[2]})
            else:
                homeSubstitution.append(None)

            if home.substitute7 != None:
                homeSubstitution.append({'number': home.substitute7.split('_')[1], 'name': home.substitute7.split('_')[2]})
            else:
                homeSubstitution.append(None)

            if home.substitute8 != None:
                homeSubstitution.append({'number': home.substitute8.split('_')[1], 'name': home.substitute8.split('_')[2]})
            else:
                homeSubstitution.append(None)

            if home.substitute9 != None:
                homeSubstitution.append({'number': home.substitute9.split('_')[1], 'name': home.substitute9.split('_')[2]})
            else:
                homeSubstitution.append(None)
        except:
            home = None
        
        return render(request, 'lineup.html', locals())
    return redirect('/option/')

def album(request, year=None, gameid=None):
    if request.user.has_perm('auth.member'):
        if gameid == None:
            games = models.GameUnit.objects.filter(year=year, postpone=False).order_by('date')
        else:
            if request.method == 'POST':
                game = models.GameUnit.objects.get(id=gameid)
                game.album = request.POST['album']
                game.save()
                return redirect('/album/109/')
    else:
        return redirect('/option/')
    return render(request, 'albumlist.html', locals())

def boxadd(request, year=None, gameid=None, itemtype=None):
    if request.user.has_perm('auth.member'):
        if gameid == None:
            games = models.GameUnit.objects.filter(year=year, postpone=False).order_by('date')

            if request.method == 'POST':
                game = request.POST['gameid']
                edittype = request.POST['item']
                return redirect('/boxadd/' + str(year) + '/' + game + '/' + edittype + '/')
        else:
            game = models.GameUnit.objects.get(id=gameid)
            players1 = models.PlayerUnit.objects.filter(team__id=game.guest.id).order_by('id')
            players2 = models.PlayerUnit.objects.filter(team__id=game.home.id).order_by('id')
            count = range(1, 21)

            if itemtype == 'score':
                try:
                    score = models.ScoreUnit.objects.get(game__id=gameid)
                except:
                    score = models.ScoreUnit.objects.create(game=game)

                match = ['guest', 'home']
                inning = [1, 2, 3, 4, 5, 6, 7]
                guest = []
                guestscore = 0
                home = []
                homescore = 0

                if request.method == 'POST':
                    for m in match:
                        for i in inning:
                            if m == 'guest':
                                if request.POST[m + str(i)] == '':
                                    guest.append(None)
                                else:
                                    guest.append(int(request.POST[m + str(i)]))
                                    guestscore += int(request.POST[m + str(i)])
                            else:
                                if request.POST[m + str(i)] == '':
                                    home.append(None)
                                else:
                                    home.append(int(request.POST[m + str(i)]))
                                    homescore += int(request.POST[m + str(i)])

                    score.guest1 = guest[0]
                    score.guest2 = guest[1]
                    score.guest3 = guest[2]
                    score.guest4 = guest[3]
                    score.guest5 = guest[4]
                    score.guest6 = guest[5]
                    score.guest7 = guest[6]
                    score.home1 = home[0]
                    score.home2 = home[1]
                    score.home3 = home[2]
                    score.home4 = home[3]
                    score.home5 = home[4]
                    score.home6 = home[5]
                    score.home7 = home[6]
                    score.save()
                    
                    game.guestScore = guestscore
                    game.homeScore = homescore
                    game.regular = False
                    game.finish = True
                    game.save()

                    addup(game.guest.id)
                    addup(game.home.id)
                    return redirect('/boxadd/' + str(year) + '/')
            elif itemtype == 'hitter':
                titles = ['姓名', '打席', '打數', '打點', '得分', '安打', '二安', '三安', '全壘打', '壘打數',
                        '雙殺打', '犧短', '犧飛', '四死球', '三振', '盜壘', '盜壘刺', '殘壘']
                items = ['player', 'PA', 'AB', 'RBI', 'R', 'H', '2BH', '3BH', 'HR', 'TB',
                        'DP', 'SH', 'SF', 'Walks', 'SO', 'SB', 'CS', 'LOB']
                players = models.HitterUnit.objects.filter(number__id=gameid).order_by('id')

                if request.method == 'POST':
                    for i in count:
                        if request.POST['player' + str(i)] == '':
                            break
                        else:
                            player = models.PlayerUnit.objects.get(id=request.POST['player' + str(i)])
                            data = []

                            for item in items:
                                data.append(request.POST[item + str(i)])

                            unit = models.HitterUnit.objects.create(
                                    player=player, number=game, PA=data[1], AB=data[2], RBI=data[3],
                                    R=data[4], H=data[5], TwoBH=data[6], ThreeBH=data[7], HR=data[8],
                                    TB=data[9], DP=data[10], SH=data[11], SF=data[12], Walks=data[13],
                                    SO=data[14], SB=data[15], CS=data[16], LOB=data[17])
                            unit.save()

                            if game.playoff == False or (game.playoff == True and game.number <= 4):
                                try:
                                    playerscore = models.PlayerHitterUnit.objects.get(player__id=player.id)
                                except:
                                    playerscore = models.PlayerHitterUnit.objects.create(player=player)

                                playerscore.PA += int(data[1])
                                playerscore.AB += int(data[2])
                                playerscore.RBI += int(data[3])
                                playerscore.R += int(data[4])
                                playerscore.H += int(data[5])
                                playerscore.TwoBH += int(data[6])
                                playerscore.ThreeBH += int(data[7])
                                playerscore.HR += int(data[8])
                                playerscore.TB += int(data[9])
                                playerscore.DP += int(data[10])
                                playerscore.SH += int(data[11])
                                playerscore.SF += int(data[12])
                                playerscore.Walks += int(data[13])
                                playerscore.SO += int(data[14])
                                playerscore.SB += int(data[15])
                                playerscore.CS += int(data[16])
                                playerscore.LOB += int(data[17])

                                if playerscore.AB != 0:
                                    playerscore.AVG = playerscore.H / playerscore.AB
                                    playerscore.SLG = playerscore.TB / playerscore.AB

                                if playerscore.AB + playerscore.Walks + playerscore.SF != 0:
                                    playerscore.OBP = (playerscore.H + playerscore.Walks) / (playerscore.AB + playerscore.Walks + playerscore.SF)

                                playerscore.save()
                    return redirect('/boxadd/' + str(year) + '/' + str(gameid) + '/' + itemtype + '/')
            elif itemtype == 'pitcher':
                titles = ['姓名', '勝負', '局數(整)', '局數(分)', '面對打席', '面對打數', '投球數', '完投', '完封', '無四死',
                        '被安打', '被全壘打', '犧牲短打', '犧牲飛球', '四壞球', '敬遠', '觸身球', '奪三振', '暴投', '犯規',
                        '失分', '責失分']
                items = ['player', 'conseq', 'inn_int', 'inn_float', 'TPAF', 'TBF', 'P', 'CG', 'SHO', 'no_walks',
                        'H', 'HR', 'SH', 'SF', 'BB', 'IBB', 'DB', 'K', 'WP', 'BK',
                        'R','ER']
                players = models.PitcherUnit.objects.filter(number__id=gameid).order_by('id')
                
                if request.method == 'POST':
                    for i in count:
                        if request.POST['player' + str(i)] == '':
                            break
                        else:
                            player = models.PlayerUnit.objects.get(id=request.POST['player' + str(i)])
                            data = []

                            for item in items:
                                if item == 'CG' or item == 'SHO' or item == 'no_walks':
                                    if request.POST[item + str(i)] == 'no':
                                        data.append(False)
                                    else:
                                        data.append(True)
                                else:
                                    data.append(request.POST[item + str(i)])

                            unit = models.PitcherUnit.objects.create(
                                    player=player, number=game, conseq=data[1], inn_int=data[2], inn_float=data[3],
                                    TPAF=data[4], TBF=data[5], P=data[6], CG=data[7], SHO=data[8],
                                    no_walks=data[9], H=data[10], HR=data[11], SH=data[12], SF=data[13],
                                    BB=data[14], IBB=data[15], DB=data[16], K=data[17], WP=data[18],
                                    BK=data[19], R=data[20], ER=data[21])
                            unit.save()

                            if game.playoff == False or (game.playoff == True and game.number <= 4):
                                try:
                                    playerscore = models.PlayerPitcherUnit.objects.get(player__id=player.id)
                                except:
                                    playerscore = models.PlayerPitcherUnit.objects.create(player=player)

                                if unit.conseq == 'W':
                                    playerscore.W += 1
                                if unit.conseq == 'L':
                                    playerscore.L += 1
                                if unit.conseq == 'H':
                                    playerscore.HO += 1
                                if unit.conseq == 'S':
                                    playerscore.S += 1
                                if unit.conseq == 'BS':
                                    playerscore.BS += 1
                                playerscore.inn3 += (int(data[2]) * 3 + int(data[3]))
                                playerscore.TPAF += int(data[4])
                                playerscore.TBF += int(data[5])
                                playerscore.P += int(data[6])
                                if unit.CG == True:
                                    playerscore.CG += 1
                                if unit.SHO == True:
                                    playerscore.SHO += 1
                                if unit.no_walks == True:
                                    playerscore.no_walks += 1
                                playerscore.H += int(data[10])
                                playerscore.HR += int(data[11])
                                playerscore.SH += int(data[12])
                                playerscore.SF += int(data[13])
                                playerscore.BB += int(data[14])
                                playerscore.IBB += int(data[15])
                                playerscore.DB += int(data[16])
                                playerscore.K += int(data[17])
                                playerscore.WP += int(data[18])
                                playerscore.BK += int(data[19])
                                playerscore.R += int(data[20])
                                playerscore.ER += int(data[21])

                                if playerscore.inn3 != 0:
                                    playerscore.ERA = playerscore.ER * 5 / (playerscore.inn3 / 3)
                                    playerscore.WHIP = (playerscore.H + playerscore.BB) / (playerscore.inn3 / 3)

                                if playerscore.TBF != 0:
                                    playerscore.AVG = playerscore.H / playerscore.TBF 

                                if playerscore.TPAF != 0:
                                    playerscore.OBA = (playerscore.H + playerscore.BB + playerscore.IBB + playerscore.DB) / playerscore.TPAF

                                playerscore.save()
                    return redirect('/boxadd/' + str(year) + '/' + str(gameid) + '/' + itemtype + '/')
            elif itemtype == 'fielder':
                titles = ['姓名', '守備位置', '刺殺', '助殺', '失誤', '雙殺參與']
                items = ['player', 'pos', 'PO', 'A', 'E', 'DP']
                players = models.FielderUnit.objects.filter(number__id=gameid).order_by('id')

                if request.method == 'POST':
                    for i in count:
                        if request.POST['player' + str(i)] == '':
                            break
                        else:
                            player = models.PlayerUnit.objects.get(id=request.POST['player' + str(i)])
                            data = []

                            for item in items:
                                data.append(request.POST[item + str(i)])

                            unit = models.FielderUnit.objects.create(
                                    player=player, number=game, pos=data[1], PO=data[2], A=data[3],
                                    E=data[4], DP=data[5])
                            unit.save()
                            
                            if game.playoff == False or (game.playoff == True and game.number <= 4):
                                try:
                                    playerscore = models.PlayerFielderUnit.objects.get(player__id=player.id, pos=data[1])
                                except:
                                    playerscore = models.PlayerFielderUnit.objects.create(player=player, pos=data[1])

                                playerscore.PO += int(data[2])
                                playerscore.A += int(data[3])
                                playerscore.E += int(data[4])
                                playerscore.DP += int(data[5])
                                
                                if playerscore.PO + playerscore.A + playerscore.E != 0:
                                    playerscore.FLD = (playerscore.PO + playerscore.A) / (playerscore.PO + playerscore.A + playerscore.E)

                                playerscore.save()
                    return redirect('/boxadd/' + str(year) + '/' + str(gameid) + '/' + itemtype + '/')
            elif itemtype == 'catcher':
                titles = ['姓名', '捕逸', '妨礙打擊', '被盜壘', '盜壘阻殺']
                items = ['player', 'PB', 'interference', 'stolen', 'CS']
                players = models.CatcherUnit.objects.filter(number__id=gameid).order_by('id')

                if request.method == 'POST':
                    for i in count:
                        if request.POST['player' + str(i)] == '':
                            break
                        else:
                            player = models.PlayerUnit.objects.get(id=request.POST['player' + str(i)])
                            data = []

                            for item in items:
                                data.append(request.POST[item + str(i)])

                            unit = models.CatcherUnit.objects.create(
                                    player=player, number=game, PB=data[1], interference=data[2], stolen=data[3],
                                    CS=data[4])
                            unit.save()
                            
                            if game.playoff == False or (game.playoff == True and game.number <= 4):
                                try:
                                    playerscore = models.PlayerCatcherUnit.objects.get(player__id=player.id)
                                except:
                                    playerscore = models.PlayerCatcherUnit.objects.create(player=player)

                                playerscore.PB += int(data[1])
                                playerscore.interference += int(data[2])
                                playerscore.stolen += int(data[3])
                                playerscore.CS += int(data[4])
                                
                                if playerscore.stolen != 0:
                                    playerscore.CSP = playerscore.CS / playerscore.stolen

                                playerscore.save()
                    return redirect('/boxadd/' + str(year) + '/' + str(gameid) + '/' + itemtype + '/')
    else:
        return redirect('/option/')
    return render(request, 'boxadd.html', locals())
    
def hitter_score_update(year=None):
    if year != None:
        players = models.PlayerHitterUnit.objects.filter(player__team__year=year)

        for player in players:
            units = models.HitterUnit.objects.filter(player__id=player.player.id)
            
            print("Player:", player.player.team.team, player.player.player.name)
            for idx, unit in enumerate(units):
                print(idx, unit.player.player.name)
            return

def delhitterscore(playerscore, box):
    playerscore.PA -= box.PA
    playerscore.AB -= box.AB
    playerscore.RBI -= box.RBI
    playerscore.R -= box.R
    playerscore.H -= box.H
    playerscore.TwoBH -= box.TwoBH
    playerscore.ThreeBH -= box.ThreeBH
    playerscore.HR -= box.HR
    playerscore.TB -= box.TB
    playerscore.DP -= box.DP
    playerscore.SH -= box.SH
    playerscore.SF -= box.SF
    playerscore.Walks -= box.Walks
    playerscore.SO -= box.SO
    playerscore.SB -= box.SB
    playerscore.CS -= box.CS
    playerscore.LOB -= box.LOB

def delfielderscore(playerscore, box):
    playerscore.PO -= box.PO
    playerscore.A -= box.A
    playerscore.E -= box.E
    playerscore.DP -= box.DP

def delcatcherscore(playerscore, box):
    playerscore.PB -= box.PB
    playerscore.interference -= box.interference
    playerscore.stolen -= box.stolen
    playerscore.CS -= box.CS

def boxedit(request, gameid=None, itemtype=None, boxid=None, edittype=None):
    if request.user.has_perm('auth.member'):
        game = models.GameUnit.objects.get(id=gameid)
        players1 = models.PlayerUnit.objects.filter(team__id=game.guest.id).order_by('id')
        players2 = models.PlayerUnit.objects.filter(team__id=game.home.id).order_by('id')

        if itemtype == 'hitter':
            box = models.HitterUnit.objects.get(id=boxid)
            playerscore = models.PlayerHitterUnit.objects.get(player__id=box.player.id)

            if edittype == 'delete':
                delhitterscore(playerscore, box)

                if playerscore.AB != 0:
                    playerscore.AVG = playerscore.H / playerscore.AB
                    playerscore.SLG = playerscore.TB / playerscore.AB
                else:
                    playerscore.AVG = None
                    playerscore.SLG = None

                if playerscore.AB + playerscore.Walks + playerscore.SF != 0:
                    playerscore.OBP = (playerscore.H + playerscore.Walks) / (playerscore.AB + playerscore.Walks + playerscore.SF)
                else:
                    playerscore.OBP = None

                playerscore.save()
                box.delete()
                return redirect('/boxadd/' + str(game.year) + '/' + str(gameid) + '/' + itemtype + '/')
            elif edittype == 'edit':
                if request.method == 'POST':
                    playerscore.PA = playerscore.PA - box.PA + int(request.POST['PA'])
                    playerscore.AB = playerscore.AB - box.AB + int(request.POST['AB'])
                    playerscore.RBI = playerscore.RBI - box.RBI + int(request.POST['RBI'])
                    playerscore.R = playerscore.R - box.R + int(request.POST['R'])
                    playerscore.H = playerscore.H - box.H + int(request.POST['H'])
                    playerscore.TwoBH = playerscore.TwoBH - box.TwoBH + int(request.POST['2BH'])
                    playerscore.ThreeBH = playerscore.ThreeBH - box.ThreeBH + int(request.POST['3BH'])
                    playerscore.HR = playerscore.HR - box.HR + int(request.POST['HR'])
                    playerscore.TB = playerscore.TB - box.TB + int(request.POST['TB'])
                    playerscore.DP = playerscore.DP - box.DP + int(request.POST['DP'])
                    playerscore.SH = playerscore.SH - box.SH + int(request.POST['SH'])
                    playerscore.SF = playerscore.SF - box.SF + int(request.POST['SF'])
                    playerscore.Walks = playerscore.Walks - box.Walks + int(request.POST['Walks'])
                    playerscore.SO = playerscore.SO - box.SO + int(request.POST['SO'])
                    playerscore.SB = playerscore.SB - box.SB + int(request.POST['SB'])
                    playerscore.CS = playerscore.CS - box.CS + int(request.POST['CS'])
                    playerscore.LOB = playerscore.LOB - box.LOB + int(request.POST['LOB'])

                    if playerscore.AB != 0:
                        playerscore.AVG = playerscore.H / playerscore.AB
                        playerscore.SLG = playerscore.TB / playerscore.AB
                    else:
                        playerscore.AVG = None
                        playerscore.SLG = None

                    if playerscore.AB + playerscore.Walks + playerscore.SF != 0:
                        playerscore.OBP = (playerscore.H + playerscore.Walks) / (playerscore.AB + playerscore.Walks + playerscore.SF)
                    else:
                        playerscore.OBP = None

                    playerscore.save()

                    box.PA = request.POST['PA']
                    box.AB = request.POST['AB']
                    box.RBI = request.POST['RBI']
                    box.R = request.POST['R']
                    box.H = request.POST['H']
                    box.TwoBH = request.POST['2BH']
                    box.ThreeBH = request.POST['3BH']
                    box.HR = request.POST['HR']
                    box.TB = request.POST['TB']
                    box.DP = request.POST['DP']
                    box.SH = request.POST['SH']
                    box.SF = request.POST['SF']
                    box.Walks = request.POST['Walks']
                    box.SO = request.POST['SO']
                    box.SB = request.POST['SB']
                    box.CS = request.POST['CS']
                    box.LOB = request.POST['LOB']
                    box.save()
                    return redirect('/boxadd/' + str(game.year) + '/' + str(gameid) + '/' + itemtype + '/')
        elif itemtype == 'pitcher':
            box = models.PitcherUnit.objects.get(id=boxid)
            playerscore = models.PlayerPitcherUnit.objects.get(player__id=box.player.id)

            if edittype == 'delete':
                if box.conseq == 'W':
                    playerscore.W -= 1
                if box.conseq == 'L':
                    playerscore.L -= 1
                if box.conseq == 'H':
                    playerscore.HO -= 1
                if box.conseq == 'S':
                    playerscore.S -= 1
                if box.conseq == 'BS':
                    playerscore.BS -= 1
                playerscore.inn3 -= (box.inn_int * 3 + box.inn_float)
                playerscore.TPAF -= box.TPAF
                playerscore.TBF -= box.TBF
                playerscore.P -= box.P
                if box.CG == True:
                    playerscore.CG -= 1
                if box.SHO == True:
                    playerscore.SHO -= 1
                if box.no_walks == True:
                    playerscore.no_walks -= 1
                playerscore.H -= box.H
                playerscore.HR -= box.HR
                playerscore.SH -= box.SH
                playerscore.SF -= box.SF
                playerscore.BB -= box.BB
                playerscore.IBB -= box.IBB
                playerscore.DB -= box.DB
                playerscore.K -= box.K
                playerscore.WP -= box.WP
                playerscore.BK -= box.BK
                playerscore.R -= box.R
                playerscore.ER -= box.ER

                if playerscore.inn3 != 0:
                    playerscore.ERA = playerscore.ER * 5 / (playerscore.inn3 / 3)
                    playerscore.WHIP = (playerscore.H + playerscore.BB) / (playerscore.inn3 / 3)
                else:
                    playerscore.ERA = None
                    playerscore.WHIP = None

                if playerscore.TBF != 0:
                    playerscore.AVG = playerscore.H / playerscore.TBF 
                else:
                    playerscore.AVG = None

                if playerscore.TPAF != 0:
                    playerscore.OBA = (playerscore.H + playerscore.BB + playerscore.IBB + playerscore.DB) / playerscore.TPAF
                else:
                    playerscore.OBA = None

                playerscore.save()
                box.delete()
                return redirect('/boxadd/' + str(game.year) + '/' + str(gameid) + '/' + itemtype + '/')
            elif edittype == 'edit':
                if request.method == 'POST':
                    if box.conseq == 'W' and request.POST['conseq'] != 'W':
                        playerscore.W -= 1
                    elif box.conseq != 'W' and request.POST['conseq'] == 'W':
                        playerscore.W += 1
                    if box.conseq == 'L' and request.POST['conseq'] != 'L':
                        playerscore.L -= 1
                    elif box.conseq != 'L' and request.POST['conseq'] == 'L':
                        playerscore.L += 1
                    if box.conseq == 'H' and request.POST['conseq'] != 'H':
                        playerscore.HO -= 1
                    elif box.conseq != 'H' and request.POST['conseq'] == 'H':
                        playerscore.HO += 1
                    if box.conseq == 'S' and request.POST['conseq'] != 'S':
                        playerscore.S -= 1
                    elif box.conseq != 'S' and request.POST['conseq'] == 'S':
                        playerscore.S += 1
                    if box.conseq == 'BS' and request.POST['conseq'] != 'BS':
                        playerscore.BS -= 1
                    elif box.conseq != 'BS' and request.POST['conseq'] == 'BS':
                        playerscore.BS += 1
                    playerscore.inn3 = playerscore.inn3 - (box.inn_int * 3 + box.inn_float) + (int(request.POST['inn_int']) * 3 + int(request.POST['inn_float']))
                    playerscore.TPAF = playerscore.TPAF - box.TPAF + int(request.POST['TPAF'])
                    playerscore.TBF = playerscore.TBF - box.TBF + int(request.POST['TBF'])
                    playerscore.P = playerscore.P - box.P + int(request.POST['P'])
                    if box.CG == True and request.POST['CG'] == 'no':
                        playerscore.CG -= 1
                    elif box.CG == False and request.POST['CG'] == 'yes':
                        playerscore.CS += 1
                    if box.SHO == True and request.POST['SHO'] == 'no':
                        playerscore.SHO -= 1
                    elif box.SHO == False and request.POST['SHO'] == 'yes':
                        playerscore.SHO += 1
                    if box.no_walks == True and request.POST['no_walks'] == 'no':
                        playerscore.no_walks -= 1
                    elif box.no_walks == False and request.POST['no_walks'] == 'yes':
                        playerscore.no_walks += 1
                    playerscore.H = playerscore.H - box.H + int(request.POST['H'])
                    playerscore.HR = playerscore.HR - box.HR + int(request.POST['HR'])
                    playerscore.SH = playerscore.SH - box.SH + int(request.POST['SH'])
                    playerscore.SF = playerscore.SF - box.SF + int(request.POST['SF'])
                    playerscore.BB = playerscore.BB - box.BB + int(request.POST['BB'])
                    playerscore.IBB = playerscore.IBB - box.IBB + int(request.POST['IBB'])
                    playerscore.DB = playerscore.DB - box.DB + int(request.POST['DB'])
                    playerscore.K = playerscore.K - box.K + int(request.POST['K'])
                    playerscore.WP = playerscore.WP - box.WP + int(request.POST['WP'])
                    playerscore.BK = playerscore.BK - box.BK + int(request.POST['BK'])
                    playerscore.R = playerscore.R - box.R + int(request.POST['R'])
                    playerscore.ER = playerscore.ER - box.ER + int(request.POST['ER'])

                    if playerscore.inn3 != 0:
                        playerscore.ERA = playerscore.ER * 5 / (playerscore.inn3 / 3)
                        playerscore.WHIP = (playerscore.H + playerscore.BB) / (playerscore.inn3 / 3)
                    else:
                        playerscore.ERA = None
                        playerscore.WHIP = None

                    if playerscore.TBF != 0:
                        playerscore.AVG = playerscore.H / playerscore.TBF 
                    else:
                        playerscore.AVG = None

                    if playerscore.TPAF != 0:
                        playerscore.OBA = (playerscore.H + playerscore.BB + playerscore.IBB + playerscore.DB) / playerscore.TPAF
                    else:
                        playerscore.OBA = None

                    playerscore.save()

                    box.conseq = request.POST['conseq']
                    box.inn_int = request.POST['inn_int']
                    box.int_float = request.POST['inn_float']
                    box.TPAF = request.POST['TPAF']
                    box.TBF = request.POST['TBF']
                    box.P = request.POST['P']
                    if request.POST['CG'] == 'yes':
                        box.CG = True
                    else:
                        box.CG = False
                    if request.POST['SHO'] == 'yes':
                        box.SHO = True
                    else:
                        box.SHO = False
                    if request.POST['no_walks'] == 'yes':
                        box.no_walks = True
                    else:
                        box.no_walks = False
                    box.H = request.POST['H']
                    box.HR = request.POST['HR']
                    box.SH = request.POST['SH']
                    box.SF = request.POST['SF']
                    box.BB = request.POST['BB']
                    box.IBB = request.POST['IBB']
                    box.DB = request.POST['DB']
                    box.K = request.POST['K']
                    box.WP = request.POST['WP']
                    box.BK = request.POST['BK']
                    box.R = request.POST['R']
                    box.ER = request.POST['ER']
                    box.save()
                    return redirect('/boxadd/' + str(game.year) + '/' + str(gameid) + '/' + itemtype + '/')
        elif itemtype == 'fielder':
            box = models.FielderUnit.objects.get(id=boxid)
            playerscore = models.PlayerFielderUnit.objects.get(player__id=box.player.id, pos=box.pos)

            if edittype == 'delete':
                delfielderscore(playerscore, box)

                if playerscore.PO + playerscore.A + playerscore.E != 0:
                    playerscore.FLD = (playerscore.PO + playerscore.A) / (playerscore.PO + playerscore.A + playerscore.E)
                else:
                    playerscore.FLD = None

                playerscore.save()
                box.delete()
                return redirect('/boxadd/' + str(game.year) + '/' + str(gameid) + '/' + itemtype + '/')
            elif edittype == 'edit':
                if request.method == 'POST':
                    delfielderscore(playerscore, box)

                    if playerscore.PO + playerscore.A + playerscore.E != 0:
                        playerscore.FLD = (playerscore.PO + playerscore.A) / (playerscore.PO + playerscore.A + playerscore.E)
                    else:
                        playerscore.FLD = None

                    playerscore.save()

                    box.pos = request.POST['pos']
                    box.PO = request.POST['PO']
                    box.A = request.POST['A']
                    box.E = request.POST['E']
                    box.DP = request.POST['DP']
                    box.save()

                    try:
                        playerscore1 = models.PlayerFielderUnit.objects.get(player__id=box.player.id, pos=box.pos)
                    except:
                        playerscore1 = models.PlayerFielderUnit.objects.create(player=box.player, pos=box.pos)

                    playerscore1.PO += int(request.POST['PO'])
                    playerscore1.A += int(request.POST['A'])
                    playerscore1.E += int(request.POST['E'])
                    playerscore1.DP += int(request.POST['DP'])
                    
                    if playerscore1.PO + playerscore1.A + playerscore1.E != 0:
                        playerscore1.FLD = (playerscore1.PO + playerscore1.A) / (playerscore1.PO + playerscore1.A + playerscore1.E)
                    else:
                        playerscore1.FLD = None

                    playerscore1.save()
                    return redirect('/boxadd/' + str(game.year) + '/' + str(gameid) + '/' + itemtype + '/')
        elif itemtype == 'catcher':
            box = models.CatcherUnit.objects.get(id=boxid)
            playerscore = models.PlayerCatcherUnit.objects.get(player__id=box.player.id)

            if edittype == 'delete':
                delcatcherscore(playerscore, box)

                if playerscore.stolen != 0:
                    playerscore.CSP = playerscore.CS / playerscore.stolen
                else:
                    playerscore.CSP = None

                playerscore.save()
                box.delete()
                return redirect('/boxadd/' + str(game.year) + '/' + str(gameid) + '/' + itemtype + '/')
            elif edittype == 'edit':
                if request.method == 'POST':
                    playerscore.PB = playerscore.PB - box.PB + int(request.POST['PB'])
                    playerscore.interference = playerscore.interference - box.interference + int(request.POST['interference'])
                    playerscore.stolen = playerscore.stolen - box.stolen + int(request.POST['stolen'])
                    playerscore.CS = playerscore.CS - box.CS + int(request.POST['CS'])

                    if playerscore.stolen != 0:
                        playerscore.CSP = playerscore.CS / playerscore.stolen
                    else:
                        playerscore.CSP = None

                    playerscore.save()

                    box.PB = request.POST['PB']
                    box.interference = request.POST['interference']
                    box.stolen = request.POST['stolen']
                    box.CS = request.POST['CS']
                    box.save()
                    return redirect('/boxadd/' + str(game.year) + '/' + str(gameid) + '/' + itemtype + '/')
    else:
        return redirect('/option/')
    return render(request, 'boxedit.html', locals())

def allnews(request):
    if request.user.has_perm('auth.member'):
        newslist = models.NewsUnit.objects.all().order_by('-date')
    else:
        return redirect('/option/')
    return render(request, 'allnews.html', locals())

def newsadd(request):
    if request.user.has_perm('auth.member'):
        if request.method == 'POST':
            title = request.POST['title']
            # Date process begin
            dateRes = request.POST['date'].split('-')
            date = datetime.date(int(dateRes[0]), int(dateRes[1]), int(dateRes[2]))
            # Date process END
            publish = request.POST['publish']
            content = request.POST['content']

            if publish == 'yes':
                unit = models.NewsUnit.objects.create(title=title, content=content, date=date, publish=True, press=0)
            else:
                unit = models.NewsUnit.objects.create(title=title, content=content, date=date, publish=False, press=0)
            
            unit.save()
            return redirect('/allnews/')
    else:
        return redirect('/option/')
    return render(request, 'newsadd.html', locals())

def newsedit(request, newsid=None, edittype=None):
    if request.user.has_perm('auth.member'):
        if edittype == 'delete':
            news = models.NewsUnit.objects.get(id=newsid)
            news.delete()
            return redirect('/allnews/')
        elif edittype == 'edit':
            news = models.NewsUnit.objects.get(id=newsid)
            datestr = str(news.date)

            if request.method == 'POST':
                news.title = request.POST['title']
                # Date process begin
                dateRes = request.POST['date'].split('-')
                news.date = datetime.date(int(dateRes[0]), int(dateRes[1]), int(dateRes[2]))
                # Date process END
                # Publish process BEGIN
                if request.POST['publish'] == 'yes':
                    news.publish = True
                else:
                    news.publish = False
                # Publish process END
                news.content = request.POST['content']
                news.save()
                return redirect('/allnews/')
    else:
        return redirect('/optoin/')
    return render(request, 'newsedit.html', locals())

def orderlist(request, teamid=None):
    if request.user.has_perm('auth.team'):
        games = models.GameUnit.objects.filter(Q(postpone=False) & (Q(guest__id=teamid) | Q(home__id=teamid))).order_by('date')
        return render(request, 'orderlist.html', locals())
    return redirect('/optoin/')

def order(request, gameid=None, team=None):
    if request.user.has_perm('auth.team'):
        game = models.GameUnit.objects.get(id=gameid)
        now = datetime.datetime.now()

        if datetime.datetime(game.date.year, game.date.month, game.date.day, 11, 0, 0, 0) - datetime.datetime.now() < datetime.timedelta(seconds=0):
            game = None
            return render(request, 'orderadd.html', locals())
        else:
            number = range(1, 10)
            if team == 'guest':
                players = models.PlayerUnit.objects.filter(team__id=game.guest.id).order_by('id')
                try:
                    order = models.OrderGuestUnit.objects.get(game__id=gameid)
                except:
                    order = None
            elif team == 'home':
                players = models.PlayerUnit.objects.filter(team__id=game.home.id).order_by('id')
                try:
                    order = models.OrderHomeUnit.objects.get(game__id=gameid)
                except:
                    order = None

            if request.method == 'POST':
                try:
                    player = models.PlayerUnit.objects.get(id=int(request.POST['starting1']))
                    first = str(player.id) + '_' + str(player.number) + '_' + player.player.name + '_' + request.POST['position1']

                    player = models.PlayerUnit.objects.get(id=int(request.POST['starting2']))
                    second = str(player.id) + '_' + str(player.number) + '_' + player.player.name + '_' + request.POST['position2']

                    player = models.PlayerUnit.objects.get(id=int(request.POST['starting3']))
                    third = str(player.id) + '_' + str(player.number) + '_' + player.player.name + '_' + request.POST['position3']

                    player = models.PlayerUnit.objects.get(id=int(request.POST['starting4']))
                    fourth = str(player.id) + '_' + str(player.number) + '_' + player.player.name + '_' + request.POST['position4']

                    player = models.PlayerUnit.objects.get(id=int(request.POST['starting5']))
                    fifth = str(player.id) + '_' + str(player.number) + '_' + player.player.name + '_' + request.POST['position5']

                    player = models.PlayerUnit.objects.get(id=int(request.POST['starting6']))
                    sixth = str(player.id) + '_' + str(player.number) + '_' + player.player.name + '_' + request.POST['position6']

                    player = models.PlayerUnit.objects.get(id=int(request.POST['starting7']))
                    seventh = str(player.id) + '_' + str(player.number) + '_' + player.player.name + '_' + request.POST['position7']

                    player = models.PlayerUnit.objects.get(id=int(request.POST['starting8']))
                    eighth = str(player.id) + '_' + str(player.number) + '_' + player.player.name + '_' + request.POST['position8']

                    player = models.PlayerUnit.objects.get(id=int(request.POST['starting9']))
                    nineth = str(player.id) + '_' + str(player.number) + '_' + player.player.name + '_' + request.POST['position9']

                    player = models.PlayerUnit.objects.get(id=int(request.POST['SP']))
                    SP = str(player.id) + '_' + str(player.number) + '_' + player.player.name
                except:
                    return redirect('/order/' + str(gameid) + '/' + team + '/')

                try:
                    player = models.PlayerUnit.objects.get(id=int(request.POST['substitute1']))
                    substitute1 = str(player.id) + '_' + str(player.number) + '_' + player.player.name
                except:
                    substitute1 = None

                try:
                    player = models.PlayerUnit.objects.get(id=int(request.POST['substitute2']))
                    substitute2 = str(player.id) + '_' + str(player.number) + '_' + player.player.name
                except:
                    substitute2 = None

                try:
                    player = models.PlayerUnit.objects.get(id=int(request.POST['substitute3']))
                    substitute3 = str(player.id) + '_' + str(player.number) + '_' + player.player.name
                except:
                    substitute3 = None

                try:
                    player = models.PlayerUnit.objects.get(id=int(request.POST['substitute4']))
                    substitute4 = str(player.id) + '_' + str(player.number) + '_' + player.player.name
                except:
                    substitute4 = None

                try:
                    player = models.PlayerUnit.objects.get(id=int(request.POST['substitute5']))
                    substitute5 = str(player.id) + '_' + str(player.number) + '_' + player.player.name
                except:
                    substitute5 = None

                try:
                    player = models.PlayerUnit.objects.get(id=int(request.POST['substitute6']))
                    substitute6 = str(player.id) + '_' + str(player.number) + '_' + player.player.name
                except:
                    substitute6 = None

                try:
                    player = models.PlayerUnit.objects.get(id=int(request.POST['substitute7']))
                    substitute7 = str(player.id) + '_' + str(player.number) + '_' + player.player.name
                except:
                    substitute7 = None

                try:
                    player = models.PlayerUnit.objects.get(id=int(request.POST['substitute8']))
                    substitute8 = str(player.id) + '_' + str(player.number) + '_' + player.player.name
                except:
                    substitute8 = None

                try:
                    player = models.PlayerUnit.objects.get(id=int(request.POST['substitute9']))
                    substitute9 = str(player.id) + '_' + str(player.number) + '_' + player.player.name
                except:
                    substitute9 = None

                if order == None:
                    if team == 'guest':
                        order = models.OrderGuestUnit.objects.create(game=game, first=first, second=second, third=third, fourth=fourth,
                                fifth=fifth, sixth=sixth, seventh=seventh, eighth=eighth, nineth=nineth, SP=SP,
                                substitute1=substitute1, substitute2=substitute2, substitute3=substitute3, substitute4=substitute4,
                                substitute5=substitute5, substitute6=substitute6, substitute7=substitute7, substitute8=substitute8,
                                substitute9=substitute9)
                    elif team == 'home':
                        order = models.OrderHomeUnit.objects.create(game=game, first=first, second=second, third=third, fourth=fourth,
                                fifth=fifth, sixth=sixth, seventh=seventh, eighth=eighth, nineth=nineth, SP=SP,
                                substitute1=substitute1, substitute2=substitute2, substitute3=substitute3, substitute4=substitute4,
                                substitute5=substitute5, substitute6=substitute6, substitute7=substitute7, substitute8=substitute8,
                                substitute9=substitute9)
                    order.save()
                else:
                    order.first = first
                    order.second = second
                    order.third = third
                    order.fourth = fourth
                    order.fifth = fifth
                    order.sixth = sixth
                    order.seventh = seventh
                    order.eighth = eighth
                    order.nineth = nineth
                    order.SP = SP
                    order.substitute1 = substitute1
                    order.substitute2 = substitute2
                    order.substitute3 = substitute3
                    order.substitute4 = substitute4
                    order.substitute5 = substitute5
                    order.substitute6 = substitute6
                    order.substitute7 = substitute7
                    order.substitute8 = substitute8
                    order.substitute9 = substitute9
                    order.save()
                return redirect('/order/' + str(gameid) + '/' + team + '/')

            if order == None:
                return render(request, 'orderadd.html', locals())
            else:
                lineupSP = {'player': int(order.SP.split('_', 1)[0])}
                lineup1 = {'player': int(order.first.split('_', 1)[0]), 'position': order.first.split('_', 3)[3]}
                lineup2 = {'player': int(order.second.split('_', 1)[0]), 'position': order.second.split('_', 3)[3]}
                lineup3 = {'player': int(order.third.split('_', 1)[0]), 'position': order.third.split('_', 3)[3]}
                lineup4 = {'player': int(order.fourth.split('_', 1)[0]), 'position': order.fourth.split('_', 3)[3]}
                lineup5 = {'player': int(order.fifth.split('_', 1)[0]), 'position': order.fifth.split('_', 3)[3]}
                lineup6 = {'player': int(order.sixth.split('_', 1)[0]), 'position': order.sixth.split('_', 3)[3]}
                lineup7 = {'player': int(order.seventh.split('_', 1)[0]), 'position': order.seventh.split('_', 3)[3]}
                lineup8 = {'player': int(order.eighth.split('_', 1)[0]), 'position': order.eighth.split('_', 3)[3]}
                lineup9 = {'player': int(order.nineth.split('_', 1)[0]), 'position': order.nineth.split('_', 3)[3]}

                if order.substitute1 != None:
                    substitution1 = int(order.substitute1.split('_', 1)[0])
                else:
                    substitution1 = None

                if order.substitute2 != None:
                    substitution2 = int(order.substitute2.split('_', 1)[0])
                else:
                    substitution2 = None

                if order.substitute3 != None:
                    substitution3 = int(order.substitute3.split('_', 1)[0])
                else:
                    substitution3 = None

                if order.substitute4 != None:
                    substitution4 = int(order.substitute4.split('_', 1)[0])
                else:
                    substitution4 = None

                if order.substitute5 != None:
                    substitution5 = int(order.substitute5.split('_', 1)[0])
                else:
                    substitution5 = None

                if order.substitute6 != None:
                    substitution6 = int(order.substitute6.split('_', 1)[0])
                else:
                    substitution6 = None

                if order.substitute7 != None:
                    substitution7 = int(order.substitute7.split('_', 1)[0])
                else:
                    substitution7 = None

                if order.substitute8 != None:
                    substitution8 = int(order.substitute8.split('_', 1)[0])
                else:
                    substitution8 = None

                if order.substitute9 != None:
                    substitution9 = int(order.substitute9.split('_', 1)[0])
                else:
                    substitution9 = None
                return render(request, 'orderedit.html', locals())
    return redirect('/optoin/')

def allevents(request):
    if request.user.has_perm('auth.member'):
        events = models.EventUnit.objects.all().order_by('-id')
    else:
        return redirect('/option/')
    return render(request, 'allevents.html', locals())

def eventadd(request):
    if request.user.has_perm('auth.member'):
        if request.method == 'POST':
            title = request.POST['title']
            startDate = datetime.datetime.strptime(request.POST['startDate'], '%Y-%m-%d').date()
            endDate = datetime.datetime.strptime(request.POST['endDate'], '%Y-%m-%d').date()
            description = request.POST['description']
            if request.POST['public'] == 'yes':
                public = True
            else:
                public = False
            
            if request.POST['type'] == 'selection':
                unit = models.EventUnit.objects.create(title=title, description=description, startDate=startDate, endDate=endDate, eventSelection=True, public=public)
            else:
                unit = models.EventUnit.objects.create(title=title, description=description, startDate=startDate, endDate=endDate, eventChoice=True, public=public)
            unit.save()
            return redirect('/allevents/')
    else:
        return redirect('/option/')
    return render(request, 'eventadd.html', locals())

def eventedit(request, eventid=None, edittype=None):
    if request.user.has_perm('auth.member'):
        if edittype == 'delete':
            event = models.EventUnit.objects.get(id=eventid)
            event.delete()
            return redirect('/allevents/')
        elif edittype == 'edit':
            event = models.EventUnit.objects.get(id=eventid)
            start = str(event.startDate)
            end = str(event.endDate)

            if request.method == 'POST':
                event.title = request.POST['title']
                event.startDate = datetime.datetime.strptime(request.POST['startDate'], '%Y-%m-%d').date()
                event.endDate = datetime.datetime.strptime(request.POST['endDate'], '%Y-%m-%d').date()
                event.description = request.POST['description']
                if request.POST['public'] == 'yes':
                    event.public = True
                else:
                    event.public = False
                if request.POST['type'] == 'selection':
                    event.eventSelection = True
                    event.eventChoice = False
                else:
                    event.eventSelection = False
                    event.eventChoice = True

                event.save()
                return redirect('/allevents/')
    else:
        return redirect('/optoin/')
    return render(request, 'eventedit.html', locals())

def itemadd(request, eventid=None):
    if request.user.has_perm('auth.member'):
        event = models.EventUnit.objects.get(id=eventid)
        items = models.OptionUnit.objects.filter(event__id=eventid)

        if request.method == 'POST':
            title = request.POST['title']
            description = request.POST['description']
            
            option = models.OptionUnit.objects.create(event=event, title=title, description=description)
            option.save()
            return redirect('/itemadd/' + str(eventid) + '/')
    else:
        return redirect('/option/')
    return render(request, 'itemadd.html', locals())

def itemedit(request, eventid=None, itemid=None):
    if request.user.has_perm('auth.member'):
        item = models.OptionUnit.objects.get(id=itemid)

        if request.method == 'POST':
            item.title = request.POST['title']
            item.description = request.POST['description']
            item.save()
            return redirect('/itemadd/' + str(eventid) + '/')
    else:
        return redirect('/option/')
    return render(request, 'itemedit.html', locals())

def itemdelete(request, eventid=None, itemid=None):
    if request.user.has_perm('auth.member'):
        item = models.OptionUnit.objects.get(id=itemid)
        item.delete()
        return redirect('/itemadd/' + str(eventid) + '/')
    return redirect('/option/')

def download_csv(request, teamid=None, itemtype=None):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="filename.csv"'

    writer = csv.writer(response)

    if itemtype == 'players':
        players = models.PlayerUnit.objects.filter(team__id=teamid).order_by('player__studentID')
        writer.writerow(['姓名', '系級', '球隊', '背號', '投打'])

        for player in players:
            lst = list()
            lst.append(player.player.name)
            lst.append(player.dept)
            lst.append(player.team.team)
            lst.append(player.number)
            lst.append(player.bt)
            writer.writerow(lst)

    if itemtype == 'hitters':
        players = models.PlayerHitterUnit.objects.filter(player__team__id=teamid).order_by('player__player__studentID')
        titles = ['姓名', '打席', '打數', '打點', '得分', '安打', '二安', '三安', '全壘打', '壘打數',
                '雙殺打', '犧短', '犧飛', '四死球', '三振', '盜壘', '盜壘刺', '殘壘', '打擊率', '上壘率',
                '盜壘成功率']
        writer.writerow(titles)

        for player in players:
            lst = list()
            lst.append(player.player.player.name)
            lst.append(player.PA)
            lst.append(player.AB)
            lst.append(player.RBI)
            lst.append(player.R)
            lst.append(player.H)
            lst.append(player.TwoBH)
            lst.append(player.ThreeBH)
            lst.append(player.HR)
            lst.append(player.TB)
            lst.append(player.DP)
            lst.append(player.SH)
            lst.append(player.SF)
            lst.append(player.Walks)
            lst.append(player.SO)
            lst.append(player.SB)
            lst.append(player.CS)
            lst.append(player.LOB)
            lst.append(player.AVG)
            lst.append(player.OBP)
            lst.append(player.SLG)
            writer.writerow(lst)

    if itemtype == 'picatchers':
        players = models.PlayerPitcherUnit.objects.filter(player__team__id=teamid).order_by('player__player__studentID')
        titles = ['姓名', '勝', '敗', '中繼點', '救援成功', '救援失敗', '局數', '面對打席', '面對打數', '投球數',
                '完投', '完封', '無四死', '被安打', '被全壘打', '犧牲短打', '犧牲飛球', '四壞球', '敬遠', '觸身球',
                '奪三振', '暴投', '犯規', '失分', '責失分', '防禦率', 'WHIP', '被打擊率', '被上壘率']
        writer.writerow(titles)

        for player in players:
            lst = list()
            lst.append(player.player.player.name)
            lst.append(player.W)
            lst.append(player.L)
            lst.append(player.HO)
            lst.append(player.S)
            lst.append(player.BS)
            lst.append(player.inn3 // 3 + (player.inn3 % 3) / 10)
            lst.append(player.TPAF)
            lst.append(player.TBF)
            lst.append(player.P)
            lst.append(player.CG)
            lst.append(player.SHO)
            lst.append(player.no_walks)
            lst.append(player.H)
            lst.append(player.HR)
            lst.append(player.SH)
            lst.append(player.SF)
            lst.append(player.BB)
            lst.append(player.IBB)
            lst.append(player.DB)
            lst.append(player.K)
            lst.append(player.WP)
            lst.append(player.BK)
            lst.append(player.R)
            lst.append(player.ER)
            lst.append(player.ERA)
            lst.append(player.WHIP)
            lst.append(player.AVG)
            lst.append(player.OBA)
            writer.writerow(lst)

        players = models.PlayerCatcherUnit.objects.filter(player__team__id=teamid).order_by('player__player__studentID')
        titles = ['姓名', '捕逸', '妨礙打擊', '被盜壘', '盜壘阻殺', '阻殺率']
        writer.writerow(titles)

        for player in players:
            lst = list()
            lst.append(player.player.player.name)
            lst.append(player.PB)
            lst.append(player.interference)
            lst.append(player.stolen)
            lst.append(player.CS)
            lst.append(player.CSP)
            writer.writerow(lst)

    if itemtype == 'fielders':
        players = models.PlayerFielderUnit.objects.filter(player__team__id=teamid).order_by('player__player__studentID')
        titles = ['姓名', '守備位置', '刺殺', '助殺', '失誤', '雙殺參與', '守備率']
        writer.writerow(titles)

        for player in players:
            lst = list()
            lst.append(player.player.player.name)
            lst.append(player.pos)
            lst.append(player.PO)
            lst.append(player.A)
            lst.append(player.E)
            lst.append(player.DP)
            lst.append(player.FLD)
            writer.writerow(lst)
    return response

def download_data(request, year=None, itemtype=None):
    if request.user.has_perm('auth.member'):
        if year != None and itemtype != None:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="filename.csv"'

            writer = csv.writer(response)

            if itemtype == 'games':
                games = models.GameUnit.objects.filter(year=year, postpone=False).order_by('date')

                for game in games:
                    writer.writerow([game.year, game.number, game.date])

                    scores = models.ScoreUnit.objects.filter(game__id=game.id)

                    for score in scores:
                        writer.writerow(['球隊', 1, 2, 3, 4, 5, 6, 7, 'R'])
                        writer.writerow([game.guest.team, score.guest1, score.guest2, score.guest3, score.guest4, score.guest5, score.guest6, score.guest7, game.guestScore])
                        writer.writerow([game.home.team, score.home1, score.home2, score.home3, score.home4, score.home5, score.home6, score.home7, game.homeScore])

                    # GUEST BOX
                    writer.writerow(['GUEST'])

                    titles = ['姓名', '打席', '打數', '打點', '得分', '安打', '二安', '三安', '全壘打', '壘打數',
                            '雙殺打', '犧短', '犧飛', '四死球', '三振', '盜壘', '盜壘刺', '殘壘']
                    writer.writerow(titles)

                    for player in models.HitterUnit.objects.filter(number__id=game.id, player__team__id=game.guest.id).order_by('id'):
                        lst = list()
                        lst.append(player.player.player.name)
                        lst.append(player.PA)
                        lst.append(player.AB)
                        lst.append(player.RBI)
                        lst.append(player.R)
                        lst.append(player.H)
                        lst.append(player.TwoBH)
                        lst.append(player.ThreeBH)
                        lst.append(player.HR)
                        lst.append(player.TB)
                        lst.append(player.DP)
                        lst.append(player.SH)
                        lst.append(player.SF)
                        lst.append(player.Walks)
                        lst.append(player.SO)
                        lst.append(player.SB)
                        lst.append(player.CS)
                        lst.append(player.LOB)
                        writer.writerow(lst)

                    titles = ['姓名', '勝負', '局數(整)', '局數(分)', '面對打席', '面對打數', '投球數', '完投', '完封', '無四死',
                            '被安打', '被全壘打', '犧牲短打', '犧牲飛球', '四壞球', '敬遠', '觸身球', '奪三振', '暴投', '犯規',
                            '失分', '責失分']
                    writer.writerow(titles)

                    for player in models.PitcherUnit.objects.filter(number__id=game.id, player__team__id=game.guest.id).order_by('id'):
                        lst = list()
                        lst.append(player.player.player.name)
                        lst.append(player.conseq)
                        lst.append(player.inn_int)
                        lst.append(player.inn_float)
                        lst.append(player.TPAF)
                        lst.append(player.TBF)
                        lst.append(player.P)
                        lst.append(player.CG)
                        lst.append(player.SHO)
                        lst.append(player.no_walks)
                        lst.append(player.H)
                        lst.append(player.HR)
                        lst.append(player.SH)
                        lst.append(player.SF)
                        lst.append(player.BB)
                        lst.append(player.IBB)
                        lst.append(player.DB)
                        lst.append(player.K)
                        lst.append(player.WP)
                        lst.append(player.BK)
                        lst.append(player.R)
                        lst.append(player.ER)
                        writer.writerow(lst)
                    
                    titles = ['姓名', '捕逸', '妨礙打擊', '被盜壘', '盜壘阻殺']
                    writer.writerow(titles)

                    for player in models.CatcherUnit.objects.filter(number__id=game.id, player__team__id=game.guest.id).order_by('id'):
                        lst = list()
                        lst.append(player.player.player.name)
                        lst.append(player.PB)
                        lst.append(player.interference)
                        lst.append(player.stolen)
                        lst.append(player.CS)
                        writer.writerow(lst)
                
                    titles = ['姓名', '守備位置', '刺殺', '助殺', '失誤', '雙殺參與']
                    writer.writerow(titles)

                    for player in models.FielderUnit.objects.filter(number__id=game.id, player__team__id=game.guest.id).order_by('id'):
                        lst = list()
                        lst.append(player.player.player.name)
                        lst.append(player.pos)
                        lst.append(player.PO)
                        lst.append(player.A)
                        lst.append(player.E)
                        lst.append(player.DP)
                        writer.writerow(lst)

                    # HOME BOX
                    writer.writerow(['HOME'])

                    titles = ['姓名', '打席', '打數', '打點', '得分', '安打', '二安', '三安', '全壘打', '壘打數',
                            '雙殺打', '犧短', '犧飛', '四死球', '三振', '盜壘', '盜壘刺', '殘壘']
                    writer.writerow(titles)

                    for player in models.HitterUnit.objects.filter(number__id=game.id, player__team__id=game.home.id).order_by('id'):
                        lst = list()
                        lst.append(player.player.player.name)
                        lst.append(player.PA)
                        lst.append(player.AB)
                        lst.append(player.RBI)
                        lst.append(player.R)
                        lst.append(player.H)
                        lst.append(player.TwoBH)
                        lst.append(player.ThreeBH)
                        lst.append(player.HR)
                        lst.append(player.TB)
                        lst.append(player.DP)
                        lst.append(player.SH)
                        lst.append(player.SF)
                        lst.append(player.Walks)
                        lst.append(player.SO)
                        lst.append(player.SB)
                        lst.append(player.CS)
                        lst.append(player.LOB)
                        writer.writerow(lst)

                    titles = ['姓名', '勝負', '局數(整)', '局數(分)', '面對打席', '面對打數', '投球數', '完投', '完封', '無四死',
                            '被安打', '被全壘打', '犧牲短打', '犧牲飛球', '四壞球', '敬遠', '觸身球', '奪三振', '暴投', '犯規',
                            '失分', '責失分']
                    writer.writerow(titles)

                    for player in models.PitcherUnit.objects.filter(number__id=game.id, player__team__id=game.home.id).order_by('id'):
                        lst = list()
                        lst.append(player.player.player.name)
                        lst.append(player.conseq)
                        lst.append(player.inn_int)
                        lst.append(player.inn_float)
                        lst.append(player.TPAF)
                        lst.append(player.TBF)
                        lst.append(player.P)
                        lst.append(player.CG)
                        lst.append(player.SHO)
                        lst.append(player.no_walks)
                        lst.append(player.H)
                        lst.append(player.HR)
                        lst.append(player.SH)
                        lst.append(player.SF)
                        lst.append(player.BB)
                        lst.append(player.IBB)
                        lst.append(player.DB)
                        lst.append(player.K)
                        lst.append(player.WP)
                        lst.append(player.BK)
                        lst.append(player.R)
                        lst.append(player.ER)
                        writer.writerow(lst)

                    titles = ['姓名', '捕逸', '妨礙打擊', '被盜壘', '盜壘阻殺']
                    writer.writerow(titles)

                    for player in models.CatcherUnit.objects.filter(number__id=game.id, player__team__id=game.home.id).order_by('id'):
                        lst = list()
                        lst.append(player.player.player.name)
                        lst.append(player.PB)
                        lst.append(player.interference)
                        lst.append(player.stolen)
                        lst.append(player.CS)
                        writer.writerow(lst)
                
                    titles = ['姓名', '守備位置', '刺殺', '助殺', '失誤', '雙殺參與']
                    writer.writerow(titles)

                    for player in models.FielderUnit.objects.filter(number__id=game.id, player__team__id=game.home.id).order_by('id'):
                        lst = list()
                        lst.append(player.player.player.name)
                        lst.append(player.pos)
                        lst.append(player.PO)
                        lst.append(player.A)
                        lst.append(player.E)
                        lst.append(player.DP)
                        writer.writerow(lst)

                    writer.writerow([])

            if itemtype == 'players':
                players = models.PlayerUnit.objects.filter(team__year=year).order_by('team__id', 'player__studentID')
                writer.writerow(['姓名', '系級', '球隊', '背號', '投打'])

                for player in players:
                    lst = list()
                    lst.append(player.player.name)
                    lst.append(player.dept)
                    lst.append(player.team.team)
                    lst.append(player.number)
                    lst.append(player.bt)
                    writer.writerow(lst)

            if itemtype == 'hitters':
                players = models.PlayerHitterUnit.objects.filter(player__team__year=year).order_by('player__team__id', 'player__player__studentID')
                titles = ['姓名', '打席', '打數', '打點', '得分', '安打', '二安', '三安', '全壘打', '壘打數',
                        '雙殺打', '犧短', '犧飛', '四死球', '三振', '盜壘', '盜壘刺', '殘壘', '打擊率', '上壘率',
                        '盜壘成功率']
                writer.writerow(titles)

                for player in players:
                    lst = list()
                    lst.append(player.player.player.name)
                    lst.append(player.PA)
                    lst.append(player.AB)
                    lst.append(player.RBI)
                    lst.append(player.R)
                    lst.append(player.H)
                    lst.append(player.TwoBH)
                    lst.append(player.ThreeBH)
                    lst.append(player.HR)
                    lst.append(player.TB)
                    lst.append(player.DP)
                    lst.append(player.SH)
                    lst.append(player.SF)
                    lst.append(player.Walks)
                    lst.append(player.SO)
                    lst.append(player.SB)
                    lst.append(player.CS)
                    lst.append(player.LOB)
                    lst.append(player.AVG)
                    lst.append(player.OBP)
                    lst.append(player.SLG)
                    writer.writerow(lst)

            if itemtype == 'pitchers':
                players = models.PlayerPitcherUnit.objects.filter(player__team__year=year).order_by('player__team__id', 'player__player__studentID')
                titles = ['姓名', '勝', '敗', '中繼點', '救援成功', '救援失敗', '局數', '面對打席', '面對打數', '投球數',
                        '完投', '完封', '無四死', '被安打', '被全壘打', '犧牲短打', '犧牲飛球', '四壞球', '敬遠', '觸身球',
                        '奪三振', '暴投', '犯規', '失分', '責失分', '防禦率', 'WHIP', '被打擊率', '被上壘率']
                writer.writerow(titles)

                for player in players:
                    lst = list()
                    lst.append(player.player.player.name)
                    lst.append(player.W)
                    lst.append(player.L)
                    lst.append(player.HO)
                    lst.append(player.S)
                    lst.append(player.BS)
                    lst.append(player.inn3 // 3 + (player.inn3 % 3) / 10)
                    lst.append(player.TPAF)
                    lst.append(player.TBF)
                    lst.append(player.P)
                    lst.append(player.CG)
                    lst.append(player.SHO)
                    lst.append(player.no_walks)
                    lst.append(player.H)
                    lst.append(player.HR)
                    lst.append(player.SH)
                    lst.append(player.SF)
                    lst.append(player.BB)
                    lst.append(player.IBB)
                    lst.append(player.DB)
                    lst.append(player.K)
                    lst.append(player.WP)
                    lst.append(player.BK)
                    lst.append(player.R)
                    lst.append(player.ER)
                    lst.append(player.ERA)
                    lst.append(player.WHIP)
                    lst.append(player.AVG)
                    lst.append(player.OBA)
                    writer.writerow(lst)

            if itemtype == 'catchers':
                players = models.PlayerCatcherUnit.objects.filter(player__team__year=year).order_by('player__team__id', 'player__player__studentID')
                titles = ['姓名', '捕逸', '妨礙打擊', '被盜壘', '盜壘阻殺', '阻殺率']
                writer.writerow(titles)

                for player in players:
                    lst = list()
                    lst.append(player.player.player.name)
                    lst.append(player.PB)
                    lst.append(player.interference)
                    lst.append(player.stolen)
                    lst.append(player.CS)
                    lst.append(player.CSP)
                    writer.writerow(lst)

            if itemtype == 'fielders':
                players = models.PlayerFielderUnit.objects.filter(player__team__year=year).order_by('player__team__id', 'player__player__studentID')
                titles = ['姓名', '守備位置', '刺殺', '助殺', '失誤', '雙殺參與', '守備率']
                writer.writerow(titles)

                for player in players:
                    lst = list()
                    lst.append(player.player.player.name)
                    lst.append(player.pos)
                    lst.append(player.PO)
                    lst.append(player.A)
                    lst.append(player.E)
                    lst.append(player.DP)
                    lst.append(player.FLD)
                    writer.writerow(lst)
            return response

        else:
            teams = models.TeamUnit.objects.all().order_by('id')
            years = []

            for team in teams:
                if team.year not in years:
                    years.append(team.year)
            return render(request, 'downloadpage.html', locals())
    return redirect('/option/')

