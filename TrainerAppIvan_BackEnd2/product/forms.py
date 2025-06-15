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
            'author',
            'price',
            'discount',
            'is_active',
        ]
        widgets = {
            'will_learn': forms.Textarea(attrs={'placeholder': 'Enter a JSON array like ["Point 1", "Point 2"]'}),
            'description': forms.Textarea(attrs={'rows': 5}),
            'brief_description': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # When editing an existing product, image is not required
        if self.instance and self.instance.pk:
            self.fields['image'].required = False

    def clean_will_learn(self):
        import json
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
