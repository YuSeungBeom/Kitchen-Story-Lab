from django import forms
from tinymce.widgets import TinyMCE
from .models import Post, Recipe, Comment

class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCE(attrs={
            'class': 'form-control',
            'cols': 80,
            'rows': 30
        }),
    )
    
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

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'serving_size', 
                 'cooking_time', 'difficulty']  # status 필드 제거
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            recipe = Recipe.objects.filter(post=self.instance).first()
            if recipe:
                self.fields['serving_size'].initial = recipe.serving_size
                self.fields['cooking_time'].initial = recipe.cooking_time
                self.fields['difficulty'].initial = recipe.difficulty

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': '댓글을 작성해주세요.'
            })
        }