from django.db import models


class MatchGamePrediction(models.Model):
    league = models.CharField(max_length=10)
    time = models.CharField(max_length=10)
    match_game = models.CharField(max_length=30)
    prediction_for_1 = models.PositiveIntegerField()
    prediction_for_x = models.PositiveIntegerField()
    prediction_for_2 = models.PositiveIntegerField()
    general_prediction = models.CharField(max_length=10)
    odds_1 = models.CharField(max_length=10)
    odds_X = models.CharField(max_length=10)
    odds_2 = models.CharField(max_length=10)
    general_prediction_and_outcome = models.CharField(max_length=10, default="UNKNOWN")
    # game_passed = models.BooleanField(default=False, null=True, blank=True)
    time_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-time_added", "match_game", ]



