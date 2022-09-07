from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'md-textarea form-control',
        'placeholder': 'Comment on the Post here!...',
        'rows': '4',
    }))
    
    #Add a Meta to show the model we are working with and the field we want to display
    class Meta:
        model = Comment
        fields = ('comment', )


