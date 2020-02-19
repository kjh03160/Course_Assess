from django import forms
from .model import Assessment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ('star','context',)

        widgets={
            "context":forms.Textarea(attrs={'placeholder':'.','class':'form-control','rows':5}),
        }
        labels={
            "context":""
        }