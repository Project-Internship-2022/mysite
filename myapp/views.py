# @Import required modules here.......
from typing import Any, Dict
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from .Driver import Driver
from .models import *
from django.contrib import messages
from django.core.cache import cache
from mysite.settings import  STATIC_ROOT, DEBUG
import pickle
from .LogDriver import LogDriver

# ------------------------------------------------------------------------------------------------------------------------


logDriver: LogDriver 
CarPricePredictionModel: Driver
LaptopPricePredictionModel: Driver

def setEnviron():
    global logDriver
    global CarPricePredictionModel
    global LaptopPricePredictionModel
    logDriver = LogDriver()
    logDriver.set_record_handler()
    if DEBUG == False:
        CarPricePredictionModel = pickle.load(STATIC_ROOT + "resources\CarPricePredictionModel.pkl", "rb")
        LaptopPricePredictionModel = pickle.load(STATIC_ROOT + "resources\LaptopPricePredictionModel.pkl", "rb")
    else:
        LaptopPricePredictionModel = Driver(STATIC_ROOT + "resources\LaptopDataAsCsv.csv")
        LaptopPricePredictionModel.parse()
        CarPricePredictionModel = Driver(STATIC_ROOT + "resources\CarDataAsCsv.csv")
        CarPricePredictionModel.parse()

#This is the HomePage of our website
# link : http://127.0.0.1:8000/
def main(request: object) -> Any:
    """
        ** It is the starting point of our server.it is executed only once as per driver code...
    """
    try:
        setEnviron()
        cache.set("user", None)
        cache.set("is_registered", False)
        logDriver.record.info(f"< OnApplicationLaunchEvent: Application Launch Successfull > ")
        return redirect("myapp:HomePageView")
    except Exception as e:
        return render(request, "ApplicationNotConfiguredPage.html", {"Exception": e})

# ---------------------------------------------------------------------------------------------------------------------
# This is the HomePage of our website
# link : http://127.0.0.1:8000/home/
class HomePage(TemplateView):
    template_name: str = "IndexPage.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        kwargs["main_template"] = "HomePage.html"
        kwargs["is_registered"] = cache.get("is_registered")
        kwargs["user"] = cache.get("user")
        return super().get_context_data(**kwargs)

# ----------------------------------------------------------------------------------------------------------------------
# link : http://127.0.0.1:8000/register/
class RegistrationPage(TemplateView):
    """
        *** This class Template is used to register the user ***
    """
    template_name: str = "IndexPage.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        kwargs["main_template"] = "RegistrationPage.html"
        kwargs["is_registered"] = cache.get("is_registered")
        kwargs["user"] = cache.get("user")
        return super().get_context_data(**kwargs)

    def post(self, request) -> Any:
        user: Dict = {
            "username": request.POST["username"],
            "emailAddr": request.POST["emailAddr"],
            "updatesFrequency": int(request.POST["updatesFrequency"])
        }
        try:
            user = UserModel.objects.create(**user)
            cache.set("user", user)
            cache.set("is_registered", True)
            messages.add_message(request,20,'Account created successfully!!!')
            logDriver.record.info(f"< RegistrationOnSuccessEvent :: User Registered Successfully")
            return redirect("myapp:HomePage")
        except:
            messages.add_message(request,40,'Account already exists on given username or email address')
            logDriver.record.info(f"< RegistrationOnFailureEvent :: User Registered Failed")
            return redirect("myapp:RecieveUpdatesView")

# ----------------------------------------------------------------------------------------------------------------------
# link : http://127.0.0.1:8000/login/
class LoginPage(TemplateView):
    template_name: str = "IndexPage.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        kwargs["main_template"] = "LoginPage.html"
        kwargs["is_registered"] = cache.get("is_registered")
        kwargs["user"] = cache.get("user")
        return super().get_context_data(**kwargs)

    def post(self, request) -> Any:
        user: Dict = {
            "username": request.POST["username"],
            "emailAddr": request.POST["emailAddr"],
        }
        try:
            user = UserModel.objects.get(**user)
            cache.set("user", user)
            cache.set("is_registered", True)
            messages.add_message(request,20,'Login successfull!!!')
            logDriver.record.info(f"< OnLoginSuccess :: User Login Successfully")
            return redirect("myapp:HomePageView")
        except Exception as e:
            messages.add_message(request,40,'Account doesnot Exist!!!')
            logDriver.record.info(f"< OnLoginFailureEvent :: User Registered Successfully")
            return redirect("myapp:LoginPageView")


# ----------------------------------------------------------------------------------------------------------------------
# link : http://127.0.0.1:8000/logout/
class LogoutPage(TemplateView):
    template_name: str = "IndexPage.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        kwargs["main_template"] = "LogoutPage.html"
        kwargs["is_registered"] = cache.get("is_registered")
        kwargs["user"] = cache.get("user")
        return super().get_context_data(**kwargs)

    def post(self, request):
        messages.add_message(request,20,'Logged Out Successfully.....')
        logDriver.record.info(f"< OnLogoutSuccessEvent :: User Logout Successful > ")
        return main(request)

#---------------------------------------------------------------------------------------------------------------------------------------
# link : http://127.0.0.1:8000/laptops/
class LaptopPredictionPage(TemplateView):
    """
        This class is used to predict the price of the laptop.
        It serves the webpage by taking the input through the
        webpage....
    """
    template_name: str = "IndexPage.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        kwargs["main_template"] = "PredictLaptopPricePage.html"
        kwargs["is_registered"] = cache.get("is_registered")
        kwargs["user"] = cache.get("user")
        data = LaptopPricePredictionModel.getData()
        for key,value in data.items():
            kwargs[key] = value
        return super().get_context_data(**kwargs)

    def post(self, request, **kwargs) -> Any:
        parsedDataAsDict: Dict = {
                    "company": request.POST["company"],
                    "product": request.POST["product"],
                    "model": request.POST["model"],
                    "os": request.POST["os"],
                    "cpu": request.POST["cpu"],
                    "ram": request.POST["ram"],
                    "gpu": request.POST["gpu"],
                    "memory": request.POST["memory"],
                    "resolution": request.POST["resolution"],
                    "inch": request.POST["inch"],
                    "weight": request.POST["weight"]
                }
        if DEBUG == False:
            parsedDataAsDict["predictedPrice"] = LaptopPricePredictionModel.predict(**parsedDataAsDict)
        else:
            parsedDataAsDict["predictedPrice"] = "$ 1432.60"
        logDriver.record.info(f"< OnLaptopPricePredictionEvent :: Predicted Price :: {parsedDataAsDict['predictedPrice']} for <LaptopModel :: {parsedDataAsDict['company']} - {parsedDataAsDict['product']}>")
        return render(request, "LaptopResultPage.html", parsedDataAsDict)

#---------------------------------------------------------------------------------------------------------------------------------------
# link : http://127.0.0.1:8000/cars/
class CarPredictionPage(TemplateView):
    template_name = "IndexPage.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        kwargs["main_template"] = "PredictCarPricePage.html"
        kwargs["is_registered"] = cache.get("is_registered")
        kwargs["user"] = cache.get("user")
        data = CarPricePredictionModel.getData()
        for k,v in data.items():
            kwargs[k] = v
        return super().get_context_data(**kwargs)

    def post(self, request):
        parsedDataAsDict: Dict= {
            "name": request.POST["name"],
            "company": request.POST["company"],
            "year": request.POST["year"],
            "kms_driven": request.POST["kms_driven"],
            "fuel_type" : request.POST["fuel_type"]
        }
        if DEBUG == False:
            parsedDataAsDict["predictedPrice"] = CarPricePredictionModel.predict(**parsedDataAsDict)
        else:
            parsedDataAsDict["predictedPrice"] = "$ 1432.60"
        logDriver.record.info(f"< OnCarPricePredictionEvent :: Predicted Price :: {parsedDataAsDict['predictedPrice']} for <CarModel :: {parsedDataAsDict['company']} - {parsedDataAsDict['name']}>")
        return render(request, "CarResultPage.html", parsedDataAsDict)

#---------------------------------------------------------------------------------------------------------------------------------------
# link : http://127.0.0.1:8000/feedback/
class FeedbackFormPage(TemplateView):
    template_name: str = "IndexPage.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        kwargs["main_template"] = "FeedbackFormPage.html"
        kwargs["is_registered"] = cache.get("is_registered")
        kwargs["user"] = cache.get("user")
        return super().get_context_data(**kwargs)

    def post(self, request):
        feedback: Dict = {
            "review": request.POST["review"],
            "rating": int(request.POST["rating"]),
        }
        try:
            user = cache.get("user")
            feedback = FeedBack.objects.create(user = user, **feedback)
            messages.add_message(request,20,'Thanks for your feedback ***** ')
            logDriver.record.info(f"< OnFeedBackEvent :: Feedback given successfully >")
            return redirect("myapp:HomePageView")
        except:
            messages.add_message(request,40,'Please login to give your feedback')
            return redirect("myapp:FeedBackView")


class ApplicationNotConfiguredView(TemplateView):
    template_name: str = "ApplicationNotConfiguredPage.html"

