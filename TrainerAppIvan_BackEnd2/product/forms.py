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
            'will_learn': forms.Textarea(attrs={'placeholder': 'Enter a JSON array like '
                                                               '["Improve strength", "Increase flexibility"]'}),
            'description': forms.Textarea(attrs={'rows': 5},),
            'brief_description': forms.Textarea(attrs={'rows': 2}),
        }

        help_texts = {
            'will_learn': 'Enter a JSON array of learning points, e.g. ["Improve strength", "Increase flexibility"]. '
                          'Use square brackets [] with double quotes"".',
            'brief_description': 'A short summary of the item, up to 500 characters.',
            'description': 'A detailed, full description of the item or content. '
                           'This can include key features, purpose, usage, and any other relevant information.'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # When editing an existing product, image is not required
        if self.instance and self.instance.pk:
            self.fields['image'].required = False

    def clean_will_learn(self):
        data = self.cleaned_data['will_learn']
        if isinstance(data, str):
            try:
                parsed = json.loads(data)
                if not isinstance(parsed, list):
                    raise forms.ValidationError("Must be a list of learning points.")
                return parsed
            except json.JSONDecodeError:
                raise forms.ValidationError("Enter valid JSON.")
        return data
