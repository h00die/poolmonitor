from django.shortcuts import render
from django.http import Http404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import matplotlib.pyplot
from django import forms
import re
from django.core.urlresolvers import reverse_lazy

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

#based on http://stackoverflow.com/questions/11163485/serving-generated-charts-via-ajax
# def chart(request, *args):
#     # ...extract chart parameters from request.GET and/or args...
#     fig = matplotlib.pyplot.figure(...)
#     # ...draw your chart, invoking methods on fig...
#     response = django.http.HttpResponse(content_type='image/png')
#     fig.savefig(response, format='png')
#     return response

class SensorForm(forms.ModelForm):
    '''Add in a clean file system location to double check its in the right format'''
    
    def clean_file_system_location(self):
        fsl = self.cleaned_data['file_system_location']
        regmatch = re.search(r'[0-9\-]+',fsl)
        if not regmatch:
            raise forms.ValidationError("Invalid file.  Check example.")
        else:
            if regmatch.group(0) != fsl:
                raise forms.ValidationError("Invalid file.  Check example.")
        print('success %s' %(fsl))
        return fsl

    class Meta:
        model = Sensor
        fields = ('description_text', 'file_system_location', 'polling_interval', 'reading_type', 'location_image')

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