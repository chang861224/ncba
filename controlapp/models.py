from django.db import models

class TeamUnit(models.Model):
    team = models.CharField(max_length=20, null=False)
    group = models.CharField(max_length=2, default='')
    captain1 = models.CharField(max_length=30, null=False)
    captain2 = models.CharField(max_length=30, default='')
    G = models.IntegerField(default=0)
    W = models.IntegerField(default=0)
    L = models.IntegerField(default=0)
    PCT = models.FloatField(null=True)
    def __str__(self):
        return self.team

class PlayerUnit(models.Model):
    team = models.ForeignKey('TeamUnit', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    studentID = models.CharField(max_length=20, null=False)
    dept = models.CharField(max_length=100, null=False)
    number = models.IntegerField(default=0)
    bt = models.CharField(max_length=50, null=False)
    def __str__(self):
        return self.team.team + '_' + self.name

class GameUnit(models.Model):
    number = models.IntegerField(default=0)
    date = models.DateField()
    guest = models.ForeignKey('TeamUnit', related_name='guest', on_delete=models.CASCADE)
    home = models.ForeignKey('TeamUnit', related_name='home', on_delete=models.CASCADE)
    umpire1 = models.CharField(max_length=50, default='')
    umpire2 = models.CharField(max_length=50, default='')
    umpire3 = models.CharField(max_length=50, default='')
    playoff = models.BooleanField(default=False)
    regular = models.BooleanField(default=True)
    postpone = models.BooleanField(default=False)
    finish = models.BooleanField(default=False)
    ps = models.CharField(max_length=100, default='')
    guestScore = models.IntegerField(null=True)
    homeScore = models.IntegerField(null=True)
    def __str__(self):
        return str(self.date) + '_' + str(self.number) + '_' + self.guest.team + 'vs.' + self.home.team

class OrderGuestUnit(models.Model):
    game = models.ForeignKey('GameUnit', on_delete=models.CASCADE)
    first = models.CharField(max_length=100, null=False)
    second = models.CharField(max_length=100, null=False)
    third = models.CharField(max_length=100, null=False)
    fourth = models.CharField(max_length=100, null=False)
    fifth = models.CharField(max_length=100, null=False)
    sixth = models.CharField(max_length=100, null=False)
    seventh = models.CharField(max_length=100, null=False)
    eighth = models.CharField(max_length=100, null=False)
    nineth = models.CharField(max_length=100, null=False)
    SP = models.CharField(max_length=100, null=False)
    substitute1 = models.CharField(max_length=100, null=True)
    substitute2 = models.CharField(max_length=100, null=True)
    substitute3 = models.CharField(max_length=100, null=True)
    substitute4 = models.CharField(max_length=100, null=True)
    substitute5 = models.CharField(max_length=100, null=True)
    substitute6 = models.CharField(max_length=100, null=True)
    substitute7 = models.CharField(max_length=100, null=True)
    substitute8 = models.CharField(max_length=100, null=True)
    substitute9 = models.CharField(max_length=100, null=True)
    submitTime = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.game.date) + ' ' + self.game.guest.team

class OrderHomeUnit(models.Model):
    game = models.ForeignKey('GameUnit', on_delete=models.CASCADE)
    first = models.CharField(max_length=100, null=False)
    second = models.CharField(max_length=100, null=False)
    third = models.CharField(max_length=100, null=False)
    fourth = models.CharField(max_length=100, null=False)
    fifth = models.CharField(max_length=100, null=False)
    sixth = models.CharField(max_length=100, null=False)
    seventh = models.CharField(max_length=100, null=False)
    eighth = models.CharField(max_length=100, null=False)
    nineth = models.CharField(max_length=100, null=False)
    SP = models.CharField(max_length=100, null=False)
    substitute1 = models.CharField(max_length=100, null=True)
    substitute2 = models.CharField(max_length=100, null=True)
    substitute3 = models.CharField(max_length=100, null=True)
    substitute4 = models.CharField(max_length=100, null=True)
    substitute5 = models.CharField(max_length=100, null=True)
    substitute6 = models.CharField(max_length=100, null=True)
    substitute7 = models.CharField(max_length=100, null=True)
    substitute8 = models.CharField(max_length=100, null=True)
    substitute9 = models.CharField(max_length=100, null=True)
    submitTime = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.game.date) + ' ' + self.game.home.team

class ScoreUnit(models.Model):
    game = models.ForeignKey('GameUnit', on_delete=models.CASCADE)
    guest1 = models.IntegerField(null=True)
    guest2 = models.IntegerField(null=True)
    guest3 = models.IntegerField(null=True)
    guest4 = models.IntegerField(null=True)
    guest5 = models.IntegerField(null=True)
    guest6 = models.IntegerField(null=True)
    guest7 = models.IntegerField(null=True)
    home1 = models.IntegerField(null=True)
    home2 = models.IntegerField(null=True)
    home3 = models.IntegerField(null=True)
    home4 = models.IntegerField(null=True)
    home5 = models.IntegerField(null=True)
    home6 = models.IntegerField(null=True)
    home7 = models.IntegerField(null=True)
    def __str__(self):
        return str(self.game.number) + '_' + self.game.guest.team + 'vs.' + self.game.home.team

class HitterUnit(models.Model):
    player = models.ForeignKey('PlayerUnit', on_delete=models.CASCADE)
    number = models.ForeignKey('GameUnit', on_delete=models.CASCADE)
    PA = models.IntegerField(default=0)
    AB = models.IntegerField(default=0)
    RBI = models.IntegerField(default=0)
    R = models.IntegerField(default=0)
    H = models.IntegerField(default=0)
    TwoBH = models.IntegerField(default=0)
    ThreeBH = models.IntegerField(default=0)
    HR = models.IntegerField(default=0)
    TB = models.IntegerField(default=0)
    DP = models.IntegerField(default=0)
    SH = models.IntegerField(default=0)
    SF = models.IntegerField(default=0)
    Walks = models.IntegerField(default=0)
    SO = models.IntegerField(default=0)
    SB = models.IntegerField(default=0)
    CS = models.IntegerField(default=0)
    LOB = models.IntegerField(default=0)
    def __str__(self):
        return str(self.number.number) + '_' + self.player.name

class PitcherUnit(models.Model):
    player = models.ForeignKey('PlayerUnit', on_delete=models.CASCADE)
    number = models.ForeignKey('GameUnit', on_delete=models.CASCADE)
    conseq = models.CharField(max_length=10, default='')
    inn_int = models.IntegerField(default=0)
    inn_float = models.IntegerField(default=0)
    TPAF = models.IntegerField(default=0)
    TBF = models.IntegerField(default=0)
    P = models.IntegerField(default=0)
    CG = models.BooleanField(default=False)
    SHO = models.BooleanField(default=False)
    no_walks = models.BooleanField(default=False)
    H = models.IntegerField(default=0)
    HR = models.IntegerField(default=0)
    SH = models.IntegerField(default=0)
    SF = models.IntegerField(default=0)
    BB = models.IntegerField(default=0)
    IBB = models.IntegerField(default=0)
    DB = models.IntegerField(default=0)
    K = models.IntegerField(default=0)
    WP = models.IntegerField(default=0)
    BK = models.IntegerField(default=0)
    R = models.IntegerField(default=0)
    ER = models.IntegerField(default=0)
    def __str__(self):
        return str(self.number.number) + '_' + self.player.name

class FielderUnit(models.Model):
    player = models.ForeignKey('PlayerUnit', on_delete=models.CASCADE)
    number = models.ForeignKey('GameUnit', on_delete=models.CASCADE)
    pos = models.CharField(max_length=50, null=False)
    PO = models.IntegerField(default=0)
    A = models.IntegerField(default=0)
    E = models.IntegerField(default=0)
    DP = models.IntegerField(default=0)
    def __str__(self):
        return str(self.number.number) + '_' + self.player.name + '_' + self.pos

class CatcherUnit(models.Model):
    player = models.ForeignKey('PlayerUnit', on_delete=models.CASCADE)
    number = models.ForeignKey('GameUnit', on_delete=models.CASCADE)
    PB = models.IntegerField(default=0)
    interference = models.IntegerField(default=0)
    stolen = models.IntegerField(default=0)
    CS = models.IntegerField(default=0)
    def __str__(self):
        return str(self.number.number) + '_' + self.player.name

class PlayerHitterUnit(models.Model):
    player = models.ForeignKey('PlayerUnit', on_delete=models.CASCADE)
    PA = models.IntegerField(default=0)
    AB = models.IntegerField(default=0)
    RBI = models.IntegerField(default=0)
    R = models.IntegerField(default=0)
    H = models.IntegerField(default=0)
    TwoBH = models.IntegerField(default=0)
    ThreeBH = models.IntegerField(default=0)
    HR = models.IntegerField(default=0)
    TB = models.IntegerField(default=0)
    DP = models.IntegerField(default=0)
    SH = models.IntegerField(default=0)
    SF = models.IntegerField(default=0)
    Walks = models.IntegerField(default=0)
    SO = models.IntegerField(default=0)
    SB = models.IntegerField(default=0)
    CS = models.IntegerField(default=0)
    LOB = models.IntegerField(default=0)
    AVG = models.FloatField(null=True)
    OBP = models.FloatField(null=True)
    SLG = models.FloatField(null=True)
    def __str__(self):
        return self.player.team.team + '_' + self.player.name

class PlayerPitcherUnit(models.Model):
    player = models.ForeignKey('PlayerUnit', on_delete=models.CASCADE)
    W = models.IntegerField(default=0)
    L = models.IntegerField(default=0)
    HO = models.IntegerField(default=0)
    S = models.IntegerField(default=0)
    BS = models.IntegerField(default=0)
    inn3 = models.IntegerField(default=0)
    TPAF = models.IntegerField(default=0)
    TBF = models.IntegerField(default=0)
    P = models.IntegerField(default=0)
    CG = models.IntegerField(default=0)
    SHO = models.IntegerField(default=0)
    no_walks = models.IntegerField(default=0)
    H = models.IntegerField(default=0)
    HR = models.IntegerField(default=0)
    SH = models.IntegerField(default=0)
    SF = models.IntegerField(default=0)
    BB = models.IntegerField(default=0)
    IBB = models.IntegerField(default=0)
    DB = models.IntegerField(default=0)
    K = models.IntegerField(default=0)
    WP = models.IntegerField(default=0)
    BK = models.IntegerField(default=0)
    R = models.IntegerField(default=0)
    ER = models.IntegerField(default=0)
    ERA = models.FloatField(null=True)
    WHIP = models.FloatField(null=True)
    AVG = models.FloatField(null=True)
    OBA = models.FloatField(null=True)
    def __str__(self):
        return self.player.team.team + '_' + self.player.name

class PlayerFielderUnit(models.Model):
    player = models.ForeignKey('PlayerUnit', on_delete=models.CASCADE)
    pos = models.CharField(max_length=50, null=False)
    PO = models.IntegerField(default=0)
    A = models.IntegerField(default=0)
    E = models.IntegerField(default=0)
    DP = models.IntegerField(default=0)
    FLD = models.FloatField(null=True)
    def __str__(self):
        return self.player.team.team + '_' + self.player.name + '_' + self.pos

class PlayerCatcherUnit(models.Model):
    player = models.ForeignKey('PlayerUnit', on_delete=models.CASCADE)
    PB = models.IntegerField(default=0)
    interference = models.IntegerField(default=0)
    stolen = models.IntegerField(default=0)
    CS = models.IntegerField(default=0)
    CSP = models.FloatField(null=True)
    def __str__(self):
        return self.player.team.team + '_' + self.player.name

class NewsUnit(models.Model):
    title = models.CharField(max_length=100, null=False)
    content = models.TextField(null=False)
    date = models.DateField(null=False)
    modify = models.DateTimeField(auto_now=True)
    press = models.IntegerField(default=0)
    publish = models.BooleanField(default=False)
    def __str__(self):
        return str(self.date) + ' ' + self.title

class EventUnit(models.Model):
    title = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=500, null=False)
    startDate = models.DateField(null=False)
    endDate = models.DateField(null=False)
    eventSelection = models.BooleanField(default=False)
    eventChoice = models.BooleanField(default=False)
    public = models.BooleanField(default=False)
    def __str__(self):
        return self.title

class OptionUnit(models.Model):
    event = models.ForeignKey('EventUnit', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=500, null=False)
    votes = models.IntegerField(default=0)
    percent = models.FloatField(null=True)
    def __str__(self):
        return self.event.title + ' - ' + self.title

class VoterUnit(models.Model):
    option = models.ForeignKey('OptionUnit', on_delete=models.CASCADE)
    email = models.EmailField(max_length=254)
    randomkey = models.CharField(max_length=50, null=False)
    confirm = models.BooleanField(default=False)
    def __str__(self):
        return str(self.email)

