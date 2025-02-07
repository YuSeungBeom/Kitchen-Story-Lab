from django import forms
from tinymce.widgets import TinyMCE
from .models import Post, Recipe

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE())
    
    serving_size = forms.CharField(
        max_length=50, 
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    cooking_time = forms.IntegerField(
        required=False, 
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    difficulty = forms.ChoiceField(
        choices=Recipe.difficulty.field.choices, 
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    ingredients = forms.CharField(
        required=False, 
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    instructions = forms.CharField(
        required=False, 
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5})
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            recipe = Recipe.objects.filter(post=self.instance).first()
            if recipe:
                self.fields['serving_size'].initial = recipe.serving_size
                self.fields['cooking_time'].initial = recipe.cooking_time
                self.fields['difficulty'].initial = recipe.difficulty
                self.fields['ingredients'].initial = recipe.ingredients
                self.fields['instructions'].initial = recipe.instructions