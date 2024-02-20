from django import forms

from .models import Auction, Category, Bid, Comment

class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'description', 'image', 'category', 'start_value']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'start_value': forms.NumberInput(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        time = kwargs.pop('time', None)
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].required = False
        if user:
            self.instance.user_id = user.id
        self.instance.time = time

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['value']
        widgets = {
            'value': forms.NumberInput(attrs={'step': '0.01'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        auction = kwargs.pop('auction', None)
        
        super().__init__(*args, **kwargs)
        if user:
            self.instance.user_id = user.id
        self.instance.auction = auction

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': "Write your comment here",
                'class': 'form-control',
                'rows': '4',
                'maxlength': '255',
                })
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        time = kwargs.pop('time', None)
        auction = kwargs.pop('auction', None)
        super().__init__(*args, **kwargs)
        if user:
            self.instance.user_id = user.id
        self.instance.time = time
        self.instance.auction = auction