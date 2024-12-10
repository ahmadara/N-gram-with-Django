from django import forms

class NgramForm(forms.Form):
    group_id = forms.CharField(label='Group ID', max_length=100)
    frequency_threshold = forms.IntegerField(label='Frequency Threshold')
