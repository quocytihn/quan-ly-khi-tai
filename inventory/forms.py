from django import forms
from .models import Asset, Transaction, Stocktake
class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['code','name','category','serial_number','quantity','unit','status','location','assigned_to','purchase_date','price','description']
        widgets = {'purchase_date': forms.DateInput(attrs={'type':'date'}), 'description': forms.Textarea(attrs={'rows':3})}
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['asset','action','quantity','from_person','to_person','note']
        widgets = {'note': forms.Textarea(attrs={'rows':2})}
class StocktakeForm(forms.ModelForm):
    class Meta:
        model = Stocktake
        fields = ['asset','actual_quantity','note']
