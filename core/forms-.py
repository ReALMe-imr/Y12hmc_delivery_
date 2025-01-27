from django import forms
from django.utils import timezone
from .models import DeliveryRecord
from datetime import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .ethiopian_date_converter import EthiopianDateConverter

class ExportForm(forms.Form):
    export_min_date = forms.DateField(
        required=True, 
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    export_max_date = forms.DateField(
        required=True, 
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        min_date = cleaned_data.get('export_min_date')
        max_date = cleaned_data.get('export_max_date')
        
        if min_date and max_date:
            # Convert dates to timezone-aware datetimes
            min_datetime = timezone.make_aware(
                datetime.combine(min_date, datetime.min.time())
            )
            max_datetime = timezone.make_aware(
                datetime.combine(max_date, datetime.max.time())
            )
            
            cleaned_data['export_min_date'] = min_datetime
            cleaned_data['export_max_date'] = max_datetime
            
        return cleaned_data



# class DeliveryRecordForm(forms.ModelForm):
#     class Meta:
#         model = DeliveryRecord
#         exclude = ['created_at', 'updated_at', 'created_by', 'edited_by']
#         widgets = {
#             'ethiopian_date': forms.TextInput(attrs={'placeholder': 'DD/MM/YYYY'}),
#         }
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields:
#             self.fields[field].widget.attrs.update({'class': 'form-control'})
        
#         for field in self.fields.values():
#             if isinstance(field, forms.ChoiceField):
#                 field.widget.attrs['class'] += ' custom-select'

#         if self.instance.pk and self.instance.delivery_date:
#             local_dt = timezone.localtime(self.instance.delivery_date)
#             self.initial['delivery_date'] = local_dt.date()
#             if self.instance.delivery_time:
#                 self.initial['delivery_time'] = self.instance.delivery_time

#     def clean(self):
#         cleaned_data = super().clean()
#         ethiopian_date_str = cleaned_data.get('ethiopian_date')
#         if ethiopian_date_str:
#             try:
#                 if not EthiopianDateConverter.is_valid_date(ethiopian_date_str):
#                     raise ValueError("Invalid Ethiopian date format or value.")
                
#                 gregorian_date_str = EthiopianDateConverter.convert_date(ethiopian_date_str)
#                 gregorian_date = datetime.strptime(gregorian_date_str, '%Y-%m-%d').date()
#                 cleaned_data['delivery_date'] = timezone.make_aware(datetime.combine(gregorian_date, datetime.min.time()))
#                 self.instance.ethiopian_date = ethiopian_date_str
#             except ValueError as e:
#                 self.add_error('ethiopian_date', str(e))
#         return cleaned_data

#     def clean_weight_in_grams(self):
#         weight = self.cleaned_data.get('weight_in_grams')
#         if weight and weight > 9999:
#             raise forms.ValidationError("Weight cannot exceed 9999 grams.")
#         return weight






class DeliveryRecordForm(forms.ModelForm):
    class Meta:
        model = DeliveryRecord
        exclude = ['created_at', 'updated_at', 'created_by', 'edited_by']
        widgets = {
            'delivery_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        
        for field in self.fields.values():
            if isinstance(field, forms.ChoiceField):
                field.widget.attrs['class'] += ' custom-select'

        if self.instance.pk and self.instance.delivery_date:
            local_dt = timezone.localtime(self.instance.delivery_date)
            self.initial['delivery_date'] = local_dt.strftime('%Y-%m-%d')


    def clean(self):
        cleaned_data = super().clean()
        ethiopian_date_str = cleaned_data.get('ethiopian_date')
        if ethiopian_date_str:
            try:
                # Validate the Ethiopian date format
                if not EthiopianDateConverter.is_valid_date(ethiopian_date_str):
                    raise forms.ValidationError("Invalid Ethiopian date format or value.")
                
                # Convert Ethiopian date to Gregorian date
                gregorian_date_str = EthiopianDateConverter.convert_date(ethiopian_date_str)
                gregorian_date = datetime.strptime(gregorian_date_str, '%Y-%m-%d').date()
                
                # Combine the Gregorian date with the time (if provided)
                delivery_time = cleaned_data.get('delivery_time', datetime.min.time())
                cleaned_data['delivery_date'] = timezone.make_aware(
                    datetime.combine(gregorian_date, delivery_time)
                )
                
                # Save the Ethiopian date to the instance
                self.instance.ethiopian_date = ethiopian_date_str
            except ValueError as e:
                self.add_error('ethiopian_date', str(e))
        return cleaned_data

class SearchForm(forms.Form):
    search_query = forms.CharField(required=False, label='Search')
    min_date = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    max_date = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    managed_by = forms.CharField(required=False, label = "Managed physician")
    serial_number = forms.IntegerField(required=False, label = 'serial number')

    def clean(self):
        cleaned_data = super().clean()
        min_date = cleaned_data.get('min_date')
        max_date = cleaned_data.get('max_date')
        
        # Convert dates to timezone-aware datetimes
        if min_date:
            min_datetime = timezone.make_aware(
                timezone.datetime.combine(min_date, timezone.datetime.min.time())
            )
            cleaned_data['min_date'] = min_datetime
        
        if max_date:
            max_datetime = timezone.make_aware(
                timezone.datetime.combine(max_date, timezone.datetime.max.time())
            )
            cleaned_data['max_date'] = max_datetime
        
        return cleaned_data

# class UserRegistrationForm(forms.Form):
#     username = forms.CharField(required=True)
#     password = forms.CharField(widget=forms.PasswordInput(), required=True)
#     password_confirm = forms.CharField(widget=forms.PasswordInput(), required=True)

#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get('password')
#         password_confirm = cleaned_data.get('password_confirm')
#         username = cleaned_data.get('username')

#         if password and password_confirm and password != password_confirm:
#             raise forms.ValidationError("Passwords do not match.")
        
#         if username:
#             if User.objects.filter(username=username).exists():
#                 raise forms.ValidationError("Username already exists.")
        
#         return cleaned_data

class RestoreForm(forms.Form):
    csv_file = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
