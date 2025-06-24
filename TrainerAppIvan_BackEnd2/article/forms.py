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
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name of the Article',
                }),
            'brief_description': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'A short summary of the article '
                               '(e.g., This article explores the fundamentals of strength training)...',
            }),
            **{
                f'paragraph{i}': forms.Textarea(attrs={
                    'rows': 4,
                    'placeholder': 'Write a section of the article here...',
                }) for i in range(1, 11)
            }
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
