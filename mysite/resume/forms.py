from django import forms

from . import config


class CountryForm(forms.Form):
	"""Class that defines the form for which countries
	to view in the /covid/bokeh url
	"""
	input_country_1 = forms.CharField(label='Country 1', max_length=100)
	input_country_2 = forms.CharField(label='Country 2', max_length=100)

	def is_valid(self):
		"""validates choices"""
		if request.input_country_1 not in config.OWID_COUNTRIES or \
			request.input_country_2 not in config.OWID_COUNTRIES:
			return False
		else:
			return True

	def return_choices(self):
		return {'input_country_1': self.input_country_1, 'input_country_2': self.input_country_2}

