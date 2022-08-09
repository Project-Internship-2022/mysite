from django.urls import path
from .views import *


app_name = "myapp"

urlpatterns: list = [
    path("", main, name="main"),
    path("home/", HomePage.as_view(), name="HomePageView"), 
    path("login/", LoginPage.as_view(), name="LoginPageView"),
    path("logout/", LogoutPage.as_view(), name="LogoutPageView"),
     path("register/", RegistrationPage.as_view(), name="RecieveUpdatesView"),
    path("laptops/", LaptopPredictionPage.as_view(), name="PredictLaptopPriceView"),
    path("cars/", CarPredictionPage.as_view(), name="PredictCarPriceView"),
    path("feedback/", FeedbackFormPage.as_view(), name="FeedBackView"),
    path("error/", ApplicationNotConfiguredView.as_view(), name="AppNotConfigured")
]