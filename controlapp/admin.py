from django.contrib import admin
from controlapp import models

admin.site.register(models.TeamUnit)
admin.site.register(models.PlayerUnit)
admin.site.register(models.GameUnit)
admin.site.register(models.OrderGuestUnit)
admin.site.register(models.OrderHomeUnit)

admin.site.register(models.ScoreUnit)
admin.site.register(models.HitterUnit)
admin.site.register(models.PitcherUnit)
admin.site.register(models.FielderUnit)
admin.site.register(models.CatcherUnit)

admin.site.register(models.PlayerHitterUnit)
admin.site.register(models.PlayerPitcherUnit)
admin.site.register(models.PlayerCatcherUnit)
admin.site.register(models.PlayerFielderUnit)

admin.site.register(models.NewsUnit)

admin.site.register(models.EventUnit)
admin.site.register(models.OptionUnit)
admin.site.register(models.VoterUnit)
