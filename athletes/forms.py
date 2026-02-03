from django import forms
from emoji_picker.widgets import EmojiPickerTextInputAdmin, EmojiPickerTextareaAdmin
from .models import Profile

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = '__all__'