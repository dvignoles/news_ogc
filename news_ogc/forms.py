from django import forms
from django.core.exceptions import ValidationError

gcm_choices = [
    ('hadgem2-es', 'hadgem2-es'), ('gfdl-esm2m', 'gfdl-esm2m'), ('ipsl-cm5a-lr', 'ipsl-cm5a-lr'),
    ('miroc-esm-chem', 'miroc-esm-chem'), ('noresm1-m', 'noresm1-m')
]

rcp_choices = [
    ('rcp8p5', 'rcp8p5'),
]

es_choices = [
    ('bau-elec', 'bau-elec'), ('bau-refd', 'bau-refd'), ('cap-elec', 'cap-elec'), ('cap-refd', 'cap-refd')
]

v_choices = [
    ('v000', 'v000'),
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
    year = forms.IntegerField(min_value=2000, max_value=2050)

    # Download only
    variable = forms.ChoiceField(choices=variable_choices)
    start_date = forms.DateField(input_formats=["%m/%d", "%m-%d"], required=False)
    end_date = forms.DateField(input_formats=["%m/%d", "%m-%d"], required=False)
    format = forms.ChoiceField(choices=format_choices)

    ## spatial subsetting
    spatial_subset = forms.BooleanField(required=False)
    lat_start = forms.FloatField(required=False, min_value=-90.0, max_value=90.0, widget=forms.NumberInput(attrs={'id': 'lat_start'}))
    lat_end = forms.FloatField(required=False, min_value=-90.0, max_value=90.0, widget=forms.NumberInput(attrs={'id': 'lat_end'}))

    lon_start = forms.FloatField(required=False, min_value=-180.0, max_value=180.0, widget=forms.NumberInput(attrs={'id': 'lon_start'}))
    lon_end = forms.FloatField(required=False, min_value=-180.0, max_value=180.0, widget=forms.NumberInput(attrs={'id': 'lon_end'}))

    def clean(self):
        cleaned_data = super().clean()
        lat_start = cleaned_data.get("lat_start")
        lat_end = cleaned_data.get("lat_end")
        lon_start = cleaned_data.get("lon_start")
        lon_end = cleaned_data.get("lon_end")

        if lat_start and lat_end:
            # Only do something if both fields are valid so far.
            if lat_start > lat_end:
                raise ValidationError(('lat_start must be less than lat_end'), code='invalid')
            if lon_start > lon_end:
                raise ValidationError(('lon_start must be less than lon_end'), code='invalid')
