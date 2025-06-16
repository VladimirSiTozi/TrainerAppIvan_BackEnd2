from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'name',
            'brief_description',
            'image1', 'image2', 'image3',
            'paragraph1', 'paragraph2', 'paragraph3', 'paragraph4', 'paragraph5',
            'paragraph6', 'paragraph7', 'paragraph8', 'paragraph9', 'paragraph10',
        ]
        widgets = {
            'brief_description': forms.Textarea(attrs={'rows': 3}),
            'paragraph1': forms.Textarea(attrs={'rows': 4}),
            'paragraph2': forms.Textarea(attrs={'rows': 4}),
            'paragraph3': forms.Textarea(attrs={'rows': 4}),
            'paragraph4': forms.Textarea(attrs={'rows': 4}),
            'paragraph5': forms.Textarea(attrs={'rows': 4}),
            'paragraph6': forms.Textarea(attrs={'rows': 4}),
            'paragraph7': forms.Textarea(attrs={'rows': 4}),
            'paragraph8': forms.Textarea(attrs={'rows': 4}),
            'paragraph9': forms.Textarea(attrs={'rows': 4}),
            'paragraph10': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'name': 'Title',
            'brief_description': 'Short Summary',
            'image1': 'Main Image',
            'image2': 'Additional Image 1',
            'image3': 'Additional Image 2',
        }
        help_texts = {
            'image1': 'Preferred orientation: landscape',
            'image2': 'Preferred orientation: landscape',
            'image3': 'Preferred orientation: landscape',
        }

