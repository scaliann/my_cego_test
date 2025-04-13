from django import forms

class PublicLinkForm(forms.Form):
    public_key = forms.CharField(
        label="Публичная ссылка",
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Публичная ссылка"
        })
    )
    file_type = forms.ChoiceField(
        label="Тип файлов",
        choices=[
            ("all", "Все"),
            ("file", "Файлы"),
            ("dir", "Папки")
        ],
        required=False,
        initial="all",
        widget=forms.Select(attrs={
            "class": "form-select"
        })
    )
