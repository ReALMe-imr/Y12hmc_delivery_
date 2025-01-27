from django import forms
from django.utils import timezone
from .models import DeliveryRecord
from datetime import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .ethiopian_date_converter import  EthiopianDateConverter

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



class DeliveryRecordForm(forms.ModelForm):
    class Meta:
        model = DeliveryRecord
        exclude = ['created_at', 'updated_at', 'created_by', 'edited_by']
        widgets = {
            'delivery_date': forms.DateInput(attrs={
                'type': 'hidden',
                'id': 'gregorianDate'
            }),
            'delivery_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'required': True
            }),
            'ethiopian_date': forms.TextInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            }),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'weight_in_grams': forms.NumberInput(attrs={'class': 'form-control'}),
            'alive': forms.Select(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'name': {
                'required': 'Please enter the patient\'s name',
                'max_length': 'Name is too long (maximum 255 characters)',
            },
            'age': {
                'required': 'Please enter the patient\'s age',
                'min_value': 'Age cannot be less than 1',
                'max_value': 'Age cannot be more than 70',
            },
            'sex': {
                'required': 'Please select the newborn\'s sex',
            },
            'weight_in_grams': {
                'required': 'Please enter the newborn\'s weight in grams',
                'min_value': 'Weight cannot be less than 0',
                'max_value': 'Weight seems too high, please check',
            },
            'alive': {
                'required': 'Please indicate if the newborn is alive',
            },
        
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        
        # Add Bootstrap custom-select class for choice fields
        for field_name, field in self.fields.items():
            if isinstance(field, forms.ChoiceField):
                field.widget.attrs['class'] += ' custom-select'

        # Set initial value for delivery_date if it exists
        # if self.instance.pk and self.instance.delivery_date:
        #     # Convert to local time for display
        #     local_dt = timezone.localtime(self.instance.delivery_date)
        #     self.initial['delivery_date'] = local_dt.strftime('%Y-%m-%dT%H:%M')

    # def clean_delivery_date(self):
    #     date = self.cleaned_data.get('delivery_date')
    #     if date:
    #         # If the date is naive (has no timezone info), make it timezone-aware
    #         if timezone.is_naive(date):
    #             # Make the datetime timezone-aware using the current timezone
    #             date = timezone.make_aware(date, timezone.get_current_timezone())
    #     return date

    def clean_weight_in_grams(self):
        weight = self.cleaned_data.get('weight_in_grams')
        if weight and weight > 9999:
            raise forms.ValidationError("Weight cannot exceed 9999 grams.")
        return weight

    def clean(self):
        cleaned_data = super().clean()
        delivery_date = cleaned_data.get('delivery_date')
        delivery_time = cleaned_data.get('delivery_time')
        ethiopian_date_str = cleaned_data.get('ethiopian_date')

        print("Initial delivery_date:", delivery_date)  # Debug print

        if delivery_date:
            # Convert the datetime to just a date
            if isinstance(delivery_date, datetime):
                delivery_date = delivery_date.date()
            cleaned_data['delivery_date'] = delivery_date
            print("Final delivery_date:", cleaned_data['delivery_date'])  # Debug print

        if delivery_date and delivery_time:
            # Combine date and time without setting to midnight
            try:
                combined_datetime = datetime.combine(delivery_date, delivery_time)
                cleaned_data['delivery_date'] = timezone.make_aware(combined_datetime)
                print("Combined datetime:", cleaned_data['delivery_date'])
            except Exception as e:
                print("Error combining date and time:", str(e))
                raise forms.ValidationError("Invalid date or time format")

        if ethiopian_date_str:
            try:
                # Validate Ethiopian date format and value
                if not EthiopianDateConverter.is_valid_date(ethiopian_date_str):
                    raise ValueError("Invalid Ethiopian date format or value.")
                
                # Convert Ethiopian date to Gregorian date
                gregorian_date_str = EthiopianDateConverter.convert_date(ethiopian_date_str)
                print(f"Converted Gregorian date: {gregorian_date_str}")  # Debugging statement
                
                # Parse the Gregorian date
                gregorian_date = datetime.strptime(gregorian_date_str, '%Y-%m-%d').date()
                cleaned_data['delivery_date'] = timezone.make_aware(datetime.combine(gregorian_date, datetime.min.time()))
                print(f"Set delivery_date: {cleaned_data['delivery_date']}")  # Debugging statement
                
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
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.csv'
        })
    )

    def clean_csv_file(self):
        csv_file = self.cleaned_data['csv_file']
        if not csv_file.name.endswith('.csv'):
            raise forms.ValidationError('File must be a CSV file')
        return csv_file
