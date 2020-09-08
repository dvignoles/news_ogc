from django.shortcuts import render, redirect
from .forms import data_select, data_download
from datetime import datetime

def wms_test(request, model="hadgem2es_rcp8p5_bau-elec_v000", year="2000"):
    template = 'wms.html'

    if request.method == 'POST':
        form = data_select(request.POST)
        if form.is_valid():
            gcm = form.cleaned_data['gcm']
            rcp = form.cleaned_data['rcp']
            energy_scenario = form.cleaned_data['energy_scenario']
            v = form.cleaned_data['v']
            year = form.cleaned_data['year']

            new_slug = '_'.join((gcm, rcp, energy_scenario, v))

            return redirect(wms_test, model=new_slug, year=year)
    else:
        form = data_select()

    context = {'form': form, 'download_form': data_download(), 'slug': model, 'year': year}
    return render(request, template, context)

def wcs(request):
    wcs_template = "http://10.16.12.61:9999/geoserver/news/wcs?service=WCS&version=2.0.1&request=GetCoverage&CoverageId= \
    {gcm}_{rcp}_{energy_scenario}_{v}_{variable}_Daily_{year}&format={fformat}&SUBSET= \
    time(\"{start_time}‌​Z\",\"{end_time}‌​Z\")&"

    if request.method == 'POST':
        form = data_download(request.POST)
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

            wcs_url = wcs_template.format(gcm=gcm, rcp=rcp, energy_scenario=energy_scenario, v=v, variable=variable,
                                          year=year, start_time=true_start, end_time=true_end, fformat=fformat)
            return redirect(wcs_url)
