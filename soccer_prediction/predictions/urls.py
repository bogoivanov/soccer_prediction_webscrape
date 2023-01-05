from django.urls import path

from soccer_prediction.predictions.views import PredictionsListView, index_view, scrape_data

urlpatterns = [
    path('', index_view, name='index'),
    path('scrape/', scrape_data, name='scrape'),
    path('predictions/', PredictionsListView.as_view(), name='predictions'),

]
