from django import forms

class ProductFilterForm(forms.Form):
    search = forms.CharField(
        required=False,
        label="Buscar",
        widget=forms.TextInput(attrs={"placeholder": "Buscar..."})
    )
    category = forms.ModelChoiceField(
        label= "Categoria",
        queryset=None,
        required=False,
        empty_label="Todas las categorías"
    )

    def __init__(self, *args, **kwargs):
        categories = kwargs.pop("categories")
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = categories
