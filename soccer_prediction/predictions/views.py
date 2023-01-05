from django.contrib.sites import requests
from django.http import request
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from django.views.generic import ListView
import bs4
import requests
from datetime import timedelta
from django.utils import timezone

from soccer_prediction.predictions.models import MatchGamePrediction


def add_two_hours_to_time(time):
    hour = int(time[0]) + 2
    minutes = time[1]
    time_to_join = list()
    time_to_join.append(str(hour))
    time_to_join.append(str(minutes))
    time = ":".join(time_to_join)
    return time


def scrape_data(request):
    # url = 'https://www.prosoccer.gr/en/football/predictions/yesterday.html'
    url = 'https://www.prosoccer.gr/en/football/predictions/'
    # url = 'https://www.prosoccer.gr/en/football/predictions/tomorrow.html'
    # url = 'https://www.prosoccer.gr/en/football/predictions/Friday.html'
    # url = 'https://www.prosoccer.gr/en/football/predictions/Saturday.html'
    # url = 'https://www.prosoccer.gr/en/football/predictions/Sunday.html'
    # url = 'https://www.prosoccer.gr/en/football/predictions/Monday.html'
    req = requests.get(url)


    soup = bs4.BeautifulSoup(req.content, 'html.parser')

    table = soup.find(id='tblPredictions')
    rows = table.find_all('tr')[1:]
    top_predictions = []
    for row in rows:
        cols = row.find_all('td')
        league = cols[0].text
        # time = cols[1].text
        time = add_two_hours_to_time(cols[1].text.split(":"))
        match_game = cols[2].text
        prediction_for_1 = int(cols[3].text)
        prediction_for_x = int(cols[4].text)
        prediction_for_2 = int(cols[5].text)
        general_prediction = cols[6].text.strip('a')
        if cols[7].text and cols[8].text and cols[9].text:
            odds_1 = float(cols[7].text)
            odds_X = float(cols[8].text)
            odds_2 = float(cols[9].text)
            if (odds_1 >= 1.5 and odds_X >= 1.5 and odds_2 >= 1.5) and (
                    prediction_for_1 >= 70 or prediction_for_x >= 70 or prediction_for_2 >= 70):
                prediction = {
                    "league": league,
                    "time": time,
                    "match_game": match_game,
                    "prediction_for_1": prediction_for_1,
                    "prediction_for_x": prediction_for_x,
                    "prediction_for_2": prediction_for_2,
                    "general_prediction": general_prediction,
                    "odds_1": odds_1,
                    "odds_X": odds_X,
                    "odds_2": odds_2,
                }

                top_predictions.append(prediction)
                # print(
                #     f'{league} | {time} | {match_game}: {prediction_for_1}|{prediction_for_x}|{prediction_for_2} || {general_prediction} || {odds_1} | {odds_X} | {odds_2}'
                # )
    add_data_to_database(top_predictions)
    return render(request, 'scrape.html')


def add_data_to_database(top_predictions):
    two_days_ago = timezone.now() - timedelta(days=1)
    print(two_days_ago)
    for prediction in top_predictions:
        match_game = prediction["match_game"]
        print(match_game)
        games_from_last_day = MatchGamePrediction.objects.filter(time_added__lt=two_days_ago)
        obj, game_to_add = MatchGamePrediction.objects.get_or_create(
            league=prediction["league"],
            time=prediction["time"],
            match_game=prediction["match_game"],
            prediction_for_1=prediction["prediction_for_1"],
            prediction_for_x=prediction["prediction_for_x"],
            prediction_for_2=prediction["prediction_for_2"],
            general_prediction=prediction["general_prediction"],
            odds_1=prediction["odds_1"],
            odds_X=prediction["odds_X"],
            odds_2=prediction["odds_2"],
         )



def index_view(request):

    # data = scrape_data(request)
    # add_data_to_database(data)
    return render(request, 'index.html')


# class IndexViewListView(View):
#     template_name = 'index.html'


# model = UserModel
# context_object_name = 'profile'
# template_name = 'common/index.html'
#
# def get_context_data(self, *args, **kwargs):
#     context = super().get_context_data(*args, **kwargs)
#     context['alcoholic_cocktails'] = Cocktail.objects.exclude(main_ingredient='non-alcoholic').count()
#     context['non_alcoholic_cocktails'] = Cocktail.objects.filter(main_ingredient='non-alcoholic').count()
#     context['all_cocktails'] = Cocktail.objects.all().count()
#     context['all_recipes'] = Recipe.objects.all().count()
#     context['all_articles'] = Cocktail.objects.all().count() + Recipe.objects.all().count()
#     if self.request.user.is_anonymous:
#         context['age_of_user'] = 16
#     else:
#         context['age_of_user'] = self.request.user.age
#     context['all_articles_without_alcohol'] = Cocktail.objects.filter(
#         main_ingredient='non-alcoholic').count() + Recipe.objects.all().count()
#     return context
# Create your views here.

class PredictionsListView(ListView):
    model = MatchGamePrediction
    context_object_name = 'match_game_prediction'
    template_name = 'predictions.html'
