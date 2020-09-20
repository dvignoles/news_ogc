from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import data_select
from datetime import datetime
from bootstrap_datepicker_plus import DatePickerInput, YearPickerInput


def wms(request, model="hadgem2-es_rcp8p5_bau-elec_v000", year="2000"):
    template = 'wms.html'

    if request.method == 'POST':
        if 'download' in request.POST:
            return wcs(request)

        form = data_select(request.POST)
        if form.is_valid():
            gcm = form.cleaned_data['gcm']
            rcp = form.cleaned_data['rcp']
            energy_scenario = form.cleaned_data['energy_scenario']
            v = form.cleaned_data['v']
            year = form.cleaned_data['year']

            new_slug = '_'.join((gcm, rcp, energy_scenario, v))

            return redirect(wms, model=new_slug, year=year)
    else:
        # GET
        form = data_select()
        form_selected = model.split('_')
        form.fields['gcm'].initial = form_selected[0]
        form.fields['rcp'].initial = form_selected[1]
        form.fields['energy_scenario'].initial = form_selected[2]
        form.fields['v'].initial = form_selected[3]

        year_widget = YearPickerInput(format='%Y', options={
            'minDate': "01/01/2000",
            'maxDate': "12/31/2050",
            'defaultDate': "01/01/{}".format(year)
        })

        form.fields['year'].widget = year_widget

        date_widget = DatePickerInput(format='%m/%d/%Y', options={
            'minDate': "01/01/2000",
            'maxDate': "12/31/2050",
            'defaultDate': "01/01/{}".format(year)
        })

        form.fields['start_date'].widget = date_widget
        form.fields['end_date'].widget = date_widget




    context = {'form': form, 'slug': model, 'year': year}
    return render(request, template, context)

def wcs(request):
    wcs_template = "http://10.16.12.61:9999/geoserver/news/wcs?service=WCS&version=2.0.1&request=GetCoverage&CoverageId=\
{gcm}_{rcp}_{energy_scenario}_{v}_{variable}_Daily_{year}&format={fformat}&SUBSET=\
time(\"{start_time}‌​Z\",\"{end_time}‌​Z\")&"

    wcs_template_spatial = wcs_template + "subset=Lat({lat_start},{lat_end})&subset=Long({lon_start},{lon_end})&"

    if request.method == 'POST':
        form = data_select(request.POST)
        if form.is_valid():
            gcm = form.cleaned_data['gcm']
            rcp = form.cleaned_data['rcp']
            energy_scenario = form.cleaned_data['energy_scenario']
            v = form.cleaned_data['v']

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
                wcs_url = wcs_template.format(gcm=gcm, rcp=rcp, energy_scenario=energy_scenario, v=v, variable=variable,
                                              year=year, start_time=true_start, end_time=true_end, fformat=fformat)
                return redirect(wcs_url)
            else:
                wcs_url = wcs_template_spatial.format(gcm=gcm, rcp=rcp, energy_scenario=energy_scenario, v=v, variable=variable,
                                              year=year, start_time=true_start, end_time=true_end, fformat=fformat, lat_start=lat_start, lat_end=lat_end, lon_start=lon_start, lon_end=lon_end)
                return redirect(wcs_url)
        else:
            return JsonResponse(status=404, data={'status': 'invalid', 'message': form.errors})
