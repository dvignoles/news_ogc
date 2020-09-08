from django import forms

gcm_choices = [
    ('hadgem2-es', 'hadgem2-es'), ('gfdl-esm2m', 'gfdl-esm2m')
]

rcp_choices = [
    ('rcp8p5', 'rcp8p5'),
]

es_choices = [
    ('bau-elec', 'bau-elec'), ('bau-refd', 'bau-refd'), ('cap-elec', 'cap-elec'), ('cap-refd', 'cap-refd')
]

v_choices = [
    ('v000', 'v000'), ('v001', 'v001')
]

variable_choices = [
    ('Discharge', 'discharge'), ('qxt_watertemp', 'qxt_watertemp'), ('Runoff', 'runoff'),
]

format_choices = [
    ('application/x-netcdf','netcdf'), ('image/tiff','tiff')
]


class data_select(forms.Form):
    gcm = forms.ChoiceField(choices=gcm_choices)
    rcp = forms.ChoiceField(choices=rcp_choices)
    energy_scenario = forms.ChoiceField(choices=es_choices)
    v = forms.ChoiceField(choices=v_choices)
    year = forms.IntegerField(min_value=2000, max_value=2005)


class data_download(forms.Form):
    gcm = forms.ChoiceField(choices=gcm_choices)
    rcp = forms.ChoiceField(choices=rcp_choices)
    energy_scenario = forms.ChoiceField(choices=es_choices)
    v = forms.ChoiceField(choices=v_choices)
    variable = forms.ChoiceField(choices=variable_choices)
    year = forms.IntegerField(min_value=2000, max_value=2005)
    start_date = forms.DateField(input_formats=["%m/%d", "%m-%d"])
    end_date = forms.DateField(input_formats=["%m/%d", "%m-%d"])
    format = forms.ChoiceField(choices=format_choices)
