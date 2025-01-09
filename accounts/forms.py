from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Users

class SignupForm(UserCreationForm):
    nickname = forms.CharField(initial="")
    age = forms.IntegerField(initial="")
    GENDER_CHOICES = [
        ('male', '남성'),
        ('female', '여성'),
        ('unspecified', '밝히지 않음'),
    ]
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.RadioSelect
    )
    PREFERENCE1_CHOICES = [
        ('action', '액션'),
        ('fps', '1인칭슈팅'),
        ('rts', '전략시뮬'),
        ('puzzle', '퍼즐'),
        ('horror', '호러'),
        ('arcade', '아케이드'),
        ('indie', '인디'),
    ]
    preference1 = forms.MultipleChoiceField(
        choices=PREFERENCE1_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label="장르취향"
    )
    PREFERENCE2_CHOICES = [
        ('2D', '2D'),
        ('3D', '3D'),
        ('dot', '도트'),
    ]
    preference2 = forms.MultipleChoiceField(
        choices=PREFERENCE2_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label="그래픽취향"
    )
    #프로필사진 미구현
    class Meta:
        model = Users
        fields = ['username', 'nickname', 'password1', 'password2', 'age', 'preference1', 'preference2']
        #widgets = {
        #    'password': forms.PasswordInput(),
        #}