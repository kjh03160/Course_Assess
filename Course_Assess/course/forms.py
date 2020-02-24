from django import forms
from .models import Assessment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ('star','contents',)

        widgets={
            "contents":forms.Textarea(attrs={'placeholder':'.','class':'form-control','rows':5}),
        }
        labels={
            "contents":""
        }