from django import forms
from .model import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

        widgets={
            "text":forms.Textarea(attrs={'placeholder':'.','class':'form-control','rows':5}),
        }
        labels={
            "text":""
        }