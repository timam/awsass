from django import forms
from .models import Person
from django.core.exceptions import ValidationError


def ForbiddenUsernamesValidator(value):
    forbidden_usernames = ['admin', 'settings', 'news', 'about', 'help',
                           'signin', 'signup', 'signout', 'terms', 'privacy',
                           'cookie', 'new', 'login', 'logout', 'administrator',
                           'join', 'account', 'username', 'root', 'blog',
                           'user', 'users', 'billing', 'subscribe', 'reviews',
                           'review', 'blog', 'blogs', 'edit', 'mail', 'email',
                           'home', 'job', 'jobs', 'contribute', 'newsletter',
                           'shop', 'profile', 'register', 'auth',
                           'authentication', 'campaign', 'config', 'delete',
                           'remove', 'forum', 'forums', 'download',
                           'downloads', 'contact', 'blogs', 'feed', 'feeds',
                           'faq', 'intranet', 'log', 'registration', 'search',
                           'explore', 'rss', 'support', 'status', 'static',
                           'media', 'setting', 'css', 'js', 'follow',
                           'activity', 'questions', 'articles', 'network', ]

    if value.lower() in forbidden_usernames:
        raise ValidationError('This is a reserved word.')


def InvalidUsernameValidator(value):
    if '@' in value or '+' in value or '-' in value:
        raise ValidationError('Enter a valid name.')


def UniqueEmailValidator(value):
    if Person.objects.filter(email__iexact=value).exists():
        raise ValidationError('User with this Email already exists.')

def UniquePhoneValidator(value):
    if Person.objects.filter(phone__iexact=value).exists():
        raise ValidationError('User with this Phone Number already exists.')


def UniqueUsernameIgnoreCaseValidator(value):
    if Person.objects.filter(user_id__iexact=value).exists():
        raise ValidationError('User with this User_Id already exists.')


class SignUpForm(forms.ModelForm):
    user_id = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=15,
        required=True,
        help_text='user_id may contain <strong>alphanumeric</strong>, <strong>_</strong> and <strong>.</strong> characters')  # noqa: E261
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        required=True,
        help_text='first_name may contain <strong>alphanumeric</strong>, <strong>_</strong> and <strong>.</strong> characters')  # noqa: E261
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        required=False,
        help_text='last_name may contain <strong>alphanumeric</strong>, <strong>_</strong> and <strong>.</strong> characters')  # noqa: E261
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm your password",
        required=True)
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        required=True,
        max_length=75)
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
        max_length=11)

    class Meta:
        model = Person
        exclude = ['last_login', 'date_joined']
        fields = ['user_id', 'first_name', 'last_name', 'department', 'email', 'phone', 'password', 'confirm_password', ]

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['user_id'].validators.append(ForbiddenUsernamesValidator)
        self.fields['first_name'].validators.append(ForbiddenUsernamesValidator)
        self.fields['last_name'].validators.append(ForbiddenUsernamesValidator)
        self.fields['first_name'].validators.append(InvalidUsernameValidator)
        self.fields['user_id'].validators.append(
            UniqueUsernameIgnoreCaseValidator)
        self.fields['email'].validators.append(UniqueEmailValidator)
        self.fields['phone'].validators.append(UniquePhoneValidator)

    def clean(self):
        super(SignUpForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and password != confirm_password:
            self._errors['password'] = self.error_class(
                ['Passwords don\'t match'])
        return self.cleaned_data
