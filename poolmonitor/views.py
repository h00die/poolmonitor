from django.shortcuts import render
from django.http import Http404

from .models import Sensor

def index(request):
    sensors= Sensor.objects.all()
    context = {'sensors': sensors}
    return render(request, 'index.html', context)

def detail(request, sensor_file_system_location):
    try:
        s = Sensor.objects.get(pk=sensor_file_system_location)
    except Question.DoesNotExist:
        raise Http404("Sensor does not exist")
    return render(request, 'sensor_details.html', {'sensor': s})

# Leave the rest of the views (detail, results, vote) unchanged