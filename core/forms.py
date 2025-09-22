from django import forms

class SearchForm(forms.Form):
	search = forms.CharField(
		label="Search",
		max_length=100,
		required=False,
		widget= forms.TextInput(
			attrs={'type':'search',
			'placeholder':"Search for posts...",
			"class": "w-full sm:w-full text-black px-3 py-2 border rounded focus:outline-none focus:ring focus:border-blue-300"})
)