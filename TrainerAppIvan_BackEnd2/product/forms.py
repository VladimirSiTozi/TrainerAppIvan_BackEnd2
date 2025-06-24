import json

from django import forms
from TrainerAppIvan_BackEnd2.product.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'type',
            'category',
            'image',
            'brief_description',
            'description',
            'will_learn',
            'price',
            'discount',
            'is_active',
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name of the product',
            }),
            'will_learn': forms.Textarea(attrs={
                'placeholder': 'E.g., Basics of nutrition\nMeal planning skills\nUnderstanding macronutrients\n...',
                'rows': 4,
            }),
            'description': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Provide a detailed course or plan description '
                               '(e.g., This program covers meal timing, portion control, and sustainable habits)...',
            }),
            'brief_description': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'A short summary (e.g., Learn how to build a balanced, sustainable nutrition plan)...',
            }),
            'price': forms.NumberInput(attrs={
                'placeholder': 'e.g., 20.00',
            }),
            'discount': forms.NumberInput(attrs={
                'placeholder': 'e.g. 5',
            })
        }

        help_texts = {
            'will_learn': 'Add every item in a new line',
            'brief_description': 'A short summary of the item, up to 500 characters.',
            'description': 'A detailed, full description of the item or content. '
                           'This can include key features, purpose, usage, and any other relevant information.'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # When editing an existing product, image is not required
        if self.instance and self.instance.pk:
            self.fields['image'].required = False
