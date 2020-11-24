from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from bootstrap_datepicker_plus import DatePickerInput, YearPickerInput
from .forms import data_select


class Index(View):
    template_name = 'index.html'

    def get(self, request):
        today_year = str(datetime.today().year)
        context = {'today_year': today_year}
        return render(request, self.template_name, context)


@csrf_exempt
def wms(request, model="hadgem2-es_rcp8p5", year="2000"):
    template = 'wms.html'

    if request.method == 'POST':
        if 'download' in request.POST:
            return wcs(request)

        form = data_select(request.POST)
        if form.is_valid():
            gcm = form.cleaned_data['gcm']
            rcp = form.cleaned_data['rcp']
            year = form.cleaned_data['year']

            new_slug = '_'.join((gcm, rcp))

            return redirect(wms, model=new_slug, year=year)
    else:
        # GET
        form = data_select()
        form_selected = model.split('_')
        form.fields['gcm'].initial = form_selected[0]
        form.fields['rcp'].initial = form_selected[1]

        year_widget = YearPickerInput(format='%Y', options={
            'minDate': "01/01/1980",
            'maxDate': "12/31/2060",
            'defaultDate': "01/01/{}".format(year)
        })

        form.fields['year'].widget = year_widget

        date_widget = DatePickerInput(format='%m/%d/%Y', options={
            'minDate': "01/01/1980",
            'maxDate': "12/31/2060",
            'defaultDate': "01/01/{}".format(year)
        })

        form.fields['start_date'].widget = date_widget
        form.fields['end_date'].widget = date_widget



    gcm,rcp = model.split('_')
    context = {'form': form, 'slug': model, 'gcm':gcm, 'rcp': rcp, 'year': year}
    return render(request, template, context)

@csrf_exempt
def wcs(request):
    wcs_template = "http://10.16.12.61:9999/geoserver/newswbm/wcs?service=WCS&version=2.0.1&request=GetCoverage&CoverageId=\
multiscenario_{gcm}_{rcp}_{variable}_daily_{year}&format={fformat}&SUBSET=\
time(\"{start_time}‌​Z\",\"{end_time}‌​Z\")&"

    wcs_template_spatial = wcs_template + "subset=Lat({lat_start},{lat_end})&subset=Long({lon_start},{lon_end})&"

    if request.method == 'POST':
        form = data_select(request.POST)
        if form.is_valid():
            gcm = form.cleaned_data['gcm']
            rcp = form.cleaned_data['rcp']

            variable = form.cleaned_data['variable']
            year = form.cleaned_data['year']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            true_start = datetime(year, start_date.month, start_date.day).isoformat()
            true_end = datetime(year, end_date.month, end_date.day).isoformat()

            fformat = form.cleaned_data['format']

            lat_start = form.cleaned_data['lat_start']
            lat_end = form.cleaned_data['lat_end']
            lon_start = form.cleaned_data['lon_start']
            lon_end = form.cleaned_data['lon_end']

            if form.cleaned_data['spatial_subset'] is False:
                wcs_url = wcs_template.format(gcm=gcm, rcp=rcp, variable=variable,
                                              year=year, start_time=true_start, end_time=true_end, fformat=fformat)
                return redirect(wcs_url)
            else:
                wcs_url = wcs_template_spatial.format(gcm=gcm, rcp=rcp, variable=variable,
                                              year=year, start_time=true_start, end_time=true_end, fformat=fformat, lat_start=lat_start, lat_end=lat_end, lon_start=lon_start, lon_end=lon_end)
                return redirect(wcs_url)
        else:
            return JsonResponse(status=404, data={'status': 'invalid', 'message': form.errors})
