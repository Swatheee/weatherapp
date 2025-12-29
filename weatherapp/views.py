from django.shortcuts import render
import requests
from .models import City

def home(request):
    weather_data = None

    if request.method == "POST":
        city = request.POST.get("city")

        # save city to DB (SQL usage)
        if city:
            City.objects.create(name=city)

        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": "5bdb50ee6d26e883f4f077b0b3da6bbc",
            "units": "metric"
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()

            weather_data = {
                "city": city,
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "icon": data["weather"][0]["icon"]
            }

        else:
            weather_data = {
                "city": city,
                "temperature": "N/A",
                "description": "City not found"
            }

    return render(request, "home.html", {"weather": weather_data})
