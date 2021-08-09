from django import forms

class CreateForm(forms.Form):
	CHOICES = (
		("1","Electronics"),
		("2","Fashion"),
		("3","Technology"),
		("4","Architecture"),
		("5","Others")
		)
	title = forms.CharField(label = "Title", max_length = 64)
	content = forms.CharField(label = "Content")
	category = forms.ChoiceField(choices = CHOICES)
	image = forms.URLField()