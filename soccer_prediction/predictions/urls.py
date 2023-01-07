from django.urls import path

from soccer_prediction.predictions.views import PredictionsListView, scrape_data, check_data, IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('scrape/', scrape_data, name='scrape'),
    path('check/', check_data, name='check'),
    path('predictions/', PredictionsListView.as_view(), name='predictions'),

]
