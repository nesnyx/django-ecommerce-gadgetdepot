from django import forms
from accounts.models import Account,UserProfile


class RegistrationForm(forms.ModelForm):
    classAttrs = {
        'class' : 'form-control'
    }
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Enter Password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class' : 'form-control',
        'placeholder' : "Confirm Password"
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : "First Name"
        
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : "Last Name",
        
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class' : 'form-control',
        'placeholder' : "Email"
    }))
    phone_number = forms.CharField(widget=forms.NumberInput(attrs={
        'class' : 'form-control',
        'placeholder' : "Phone Number"
    }))
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number','email','password']

    
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!!"
            )
        


class UserForm(forms.ModelForm):
    
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : "First Name"
        
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : "Last Name",
        
    }))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : "Phone Number"
    }))
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number']

class UserProfileForm(forms.ModelForm):
    
    address_line_1 = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : "address_line_1"
        
    }))
    address_line_2 = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : "address_line_2",
        
    }))
    city= forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : "city"
    }))
    country= forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : "country"
    }))
    state= forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : "state"
    }))
    class Meta:
        model = UserProfile
        fields = ['address_line_1','address_line_2','city','state','country','profile_picture']
