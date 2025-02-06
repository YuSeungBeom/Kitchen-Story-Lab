from django import forms
from django.core.validators import FileExtensionValidator
from .models import Post, Recipe

def validate_file_size(value):
    filesize = value.size
    if filesize > 5 * 1024 * 1024:  # 5MB 제한
        raise forms.ValidationError("이미지 크기는 5MB를 초과할 수 없습니다.")

class PostForm(forms.ModelForm):
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

    thumbnail = forms.ImageField(
        required=False,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg', 'png', 'gif'],
                message='허용되는 이미지 형식은 jpg, jpeg, png, gif입니다.'
            ),
            validate_file_size
        ],
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/jpeg,image/png,image/gif'
        })
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'thumbnail', 'status']
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