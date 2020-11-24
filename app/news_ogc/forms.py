from django import forms
from django.core.exceptions import ValidationError

gcm_choices = [
    ('hadgem2-es', 'hadgem2-es'), ('gfdl-esm2m', 'gfdl-esm2m'), ('ipsl-cm5a-lr', 'ipsl-cm5a-lr'),
    ('miroc-esm-chem', 'miroc-esm-chem'), ('noresm1-m', 'noresm1-m')
]

rcp_choices = [
    ('rcp2p6', 'rcp2p6'), ('rcp4p5', 'rcp4p5'),  ('rcp6p0', 'rcp6p0'), ('rcp8p5', 'rcp8p5'),
]

es_choices = [
    ('bau-elec', 'bau-elec'), ('bau-refd', 'bau-refd'), ('cap-elec', 'cap-elec'), ('cap-refd', 'cap-refd')
]

v_choices = [
    ('v000', 'v000'),
]

variable_choices = [
    ('discharge', 'Discharge'), ('qxt_watertemp', 'Water Temperature'), ('airtemperature','Air Temperature'),
    ('wetbulbtemp', 'Wetbulb Temperature')
]

format_choices = [
    ('application/x-netcdf','netcdf'), ('image/tiff','tiff')
]


class data_select(forms.Form):

    gcm = forms.ChoiceField(choices=gcm_choices)
    rcp = forms.ChoiceField(choices=rcp_choices)
    #energy_scenario = forms.ChoiceField(choices=es_choices)
    #v = forms.ChoiceField(choices=v_choices)
    year = forms.IntegerField(min_value=1980, max_value=2060)

    # Download only
    variable = forms.ChoiceField(choices=variable_choices)
    start_date = forms.DateField(input_formats=["%m/%d/%Y", "%m-%d-%Y"], required=False)
    end_date = forms.DateField(input_formats=["%m/%d/%Y", "%m-%d-%Y"], required=False)
    format = forms.ChoiceField(choices=format_choices)

    ## spatial subsetting
    spatial_subset = forms.BooleanField(required=False, label="Clip download to extents?")
    lat_start = forms.FloatField(required=False, label="Latitude S",
                                 widget=forms.NumberInput(attrs={'id': 'lat_start'}))
    lat_end = forms.FloatField(required=False, label="Latitude N",
                               widget=forms.NumberInput(attrs={'id': 'lat_end'}))

    lon_start = forms.FloatField(required=False, label="Longitude W",
                                 widget=forms.NumberInput(attrs={'id': 'lon_start'}))
    lon_end = forms.FloatField(required=False, label="Longitude E",
                               widget=forms.NumberInput(attrs={'id': 'lon_end'}))

    def clean(self):
        cleaned_data = super().clean()
        lat_start = cleaned_data.get("lat_start")
        lat_end = cleaned_data.get("lat_end")
        lon_start = cleaned_data.get("lon_start")
        lon_end = cleaned_data.get("lon_end")
        spatial_subset = cleaned_data.get("spatial_subset")

        if spatial_subset:
            if lat_start and lat_end:
                if lat_start > lat_end:
                    raise ValidationError(('lat_start must be less than lat_end'), code='invalid')
            if lon_start and lon_end:
                if lon_start > lon_end:
                    raise ValidationError(('lon_start must be less than lon_end'), code='invalid')

        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if end_date and start_date:
            if end_date < start_date:
                raise ValidationError(("start date must be equal to or less than end date"), code='invalid')

            td = end_date - start_date
            # if greater than 6 months of data, throw error
            if td.total_seconds() > 16070400:
                raise ValidationError(("queries are limitted to a maximum interval of 186 days (~6 months)"), code='invalid')