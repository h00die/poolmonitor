from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django import forms
import re
from django.core.urlresolvers import reverse_lazy

import tempfile, os
os.environ['MPLCONFIGDIR'] = tempfile.mkdtemp()
import matplotlib
#solve the no display name and no $DISPLAY environment variable issue
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from .models import Sensor, Reading

def index(request):
    sensors= Sensor.objects.all()
    context = {'sensors': sensors}
    return render(request, 'index.html', context)

def detail(request, sensor_file_system_location):
    try:
        s = Sensor.objects.get(pk=sensor_file_system_location)
    except Sensor.DoesNotExist:
        raise Http404("Sensor does not exist")
    return render(request, 'sensor_details.html', {'sensor': s})

def graph(request):
     #based on http://stackoverflow.com/questions/11163485/serving-generated-charts-via-ajax
     dateRange = int(request.GET.get("count",5))
     sensor = request.GET.get("sensor","")
     toPlot = Reading.objects.filter(sensor=sensor)[:dateRange]
     dates = [d.reading_date for d in toPlot]
     values = [d.reading for d in toPlot]
     plt.plot(dates,values, marker='o', linestyle='--', linewidth=2.0, color='b')
     plt.xlabel('Dates')
     plt.ylabel(Sensor.objects.get(file_system_location=sensor).reading_type)
     plt.tight_layout()
     # ...draw your chart, invoking methods on fig...
     response = HttpResponse(content_type='image/png')
     plt.savefig(response, format='png')
     return response

def chart(request):
     #based on http://stackoverflow.com/questions/11163485/serving-generated-charts-via-ajax
     dateRange = int(request.GET.get("count",5))
     sensor = request.GET.get("sensor","")
     toPlot = Reading.objects.filter(sensor=sensor)[:dateRange]
     result = "<table border=1><tr><th>Date</th><th>Reading</th></tr>"
     for r in toPlot:
        result += "<tr><td>%s</td><td>%s</td></tr>" %(r.reading_date.strftime("%d/%m/%y %H:%M"), r.reading)
     return HttpResponse(result + "</table>")

class SensorForm(forms.ModelForm):
    '''Add in a clean file system location to double check its in the right format'''
    
    def clean_file_system_location(self):
        fsl = self.cleaned_data['file_system_location']
        regmatch = re.search(r'[0-9\-a-f]+',fsl)
        if not regmatch:
            raise forms.ValidationError("Invalid file.  Check example.")
        else:
            if regmatch.group(0) != fsl:
                raise forms.ValidationError("Invalid file.  Check example.")
        print('success %s' %(fsl))
        return fsl

    class Meta:
        model = Sensor
        fields = ('description_text', 'file_system_location', 'polling_interval', 'reading_type', 'reading_units')

class SensorCreate(CreateView):
    template_name = 'sensor_form.html'
    form_class = SensorForm
    
class SensorUpdate(UpdateView):
    model = Sensor
    template_name = 'sensor_form.html'
    form_class = SensorForm
    
class SensorDelete(DeleteView):
    model = Sensor
    template_name = 'sensor_confirm_delete.html'
    form_class = SensorForm
    success_url = reverse_lazy('index')