from django import forms
from .models import ScraperSource


class ScraperSourceForm(forms.ModelForm):
    manual_mode = forms.BooleanField(
        required=False, label="Inserir conteúdo manualmente"
    )
    manual_title = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    manual_content = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 6}),
    )

    class Meta:
        model = ScraperSource
        fields = [
            "name",
            "url",
            "title_selector",
            "content_selector",
            "image_selector",
            "status",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: Portal G1 - Tecnologia",
                }
            ),
            "url": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://exemplo.com/noticias/tecnologia/artigo-1",
                }
            ),
            "title_selector": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: h1.article-title, .post-title",
                }
            ),
            "content_selector": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: div.article-content, .post-body",
                }
            ),
            "image_selector": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: img.featured-image (opcional)",
                }
            ),
            "status": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["title_selector"].required = False
        self.fields["content_selector"].required = False
        self.fields["image_selector"].required = False

    def clean(self):
        cleaned_data = super().clean()
        manual = cleaned_data.get("manual_mode")

        title_selector = cleaned_data.get("title_selector")
        content_selector = cleaned_data.get("content_selector")
        manual_title = cleaned_data.get("manual_title")
        manual_content = cleaned_data.get("manual_content")

        if manual:
            if not manual_title:
                self.add_error("manual_title", "Obrigatório no modo manual.")
            if not manual_content:
                self.add_error("manual_content", "Obrigatório no modo manual.")
        else:
            if not title_selector:
                self.add_error(
                    "title_selector", "Obrigatório quando o modo manual não está ativo."
                )
            if not content_selector:
                self.add_error(
                    "content_selector",
                    "Obrigatório quando o modo manual não está ativo.",
                )

        return cleaned_data
