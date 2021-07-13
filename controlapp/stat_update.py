from controlapp import models
from django.db.models import Q

def hitter_statistic_update(year=None):
    players = models.PlayerHitterUnit.objects.filter(player__team__year=year)

    for player in players:
        items = modesl.HitterUnit.objects.filter(player__id=player.player.id)

        print("Player:", player.player.name)
        for item in items:
            print(item.player.name)
        return


if __name__ == "__main__":
    hitter_statistic_update(109)

