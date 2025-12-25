import os
import requests
from django.shortcuts import render
from .forms import WeatherForm
from django.core.cache import cache
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='20/m', block=True) # server-side controlling for requests
def get_weather_data(request):
    weather_data = None
    form = WeatherForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        city = form.cleaned_data['city'].lower()
        cache_key = f'weather:{city}'
        weather_data = cache.get(cache_key)

        if not weather_data:
            api_key = os.getenv('WEATHER_API_KEY')
            url = os.getenv('WEATHER_BASE_URL') + f"{city}?unitGroup=metric&key={api_key}"

            try:
                # timeout here is client-side controlling for request
                response = requests.get(url, timeout=5)
                response.raise_for_status()  # Raises HTTPError for 4xx/5xx

                data = response.json()

                # Check if API returned expected fields
                if 'days' in data and len(data['days']) > 0:
                    weather_data = {
                        'city': data.get('resolvedAddress', city),
                        'description': data.get('description', 'No description available'),
                        'date': data['days'][0].get('datetime'),
                        'temp_max': data['days'][0].get('tempmax'),
                        'temp_min': data['days'][0].get('tempmin'),
                        'temp': data['days'][0].get('temp'),
                    }
                    # Store in Redis for 12 hours
                    cache.set(cache_key, weather_data, timeout=43200)
                else:
                    weather_data = {'error': 'Invalid city name or no data returned.'}

            except requests.exceptions.HTTPError as e:
                weather_data = {'error': f'API returned an error: {e.response.status_code}'}
            except requests.exceptions.RequestException:
                weather_data = {'error': 'Weather service is currently unavailable. Please try again later.'}

    return render(request, 'weather_api/weather_api.html', context={'form': form,
                                                                    'weather_data': weather_data})
