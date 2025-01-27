from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime

class DeliveryRecord(models.Model):
    serial_number = models.AutoField(primary_key=True)
    mrn = models.CharField(max_length=6, blank=True, null=True, db_index=True)
    name = models.CharField(max_length=255, db_index=True)
    age = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(999)])
    kebele = models.CharField(max_length=255, blank=True, null=True)
    ethiopian_date = models.CharField(max_length=20, null=True, blank=True)
    delivery_date = models.DateField(null=False, blank=False)
    delivery_time = models.TimeField(null=False, blank=False)
    
    
    MODE_CHOICES = [
        ('svd', 'SVD'),
        ('cs', 'Caesarean Section (C/S)'),
        ('forceps', 'Forceps/Vacuum Extraction'),
        ('episiotomy', 'Episiotomy'),
        ('other', 'Other Procedures'),
    ]
    mode_of_delivery = models.CharField(max_length=20, choices=MODE_CHOICES)
    
    MATERNAL_STATUS_CHOICES = [
        ('unstable', 'Unstable/Deteriorated and Referred'),
        ('stable', 'Stable'),
        ('died', 'Died'),
    ]
    maternal_status = models.CharField(max_length=20, choices=MATERNAL_STATUS_CHOICES)
    
    OBSTETRIC_COMPLICATION_CHOICES = [
        ('pre_eclampsia', 'Pre-eclampsia'),
        ('eclampsia', 'Eclampsia'),
        ('aph', 'APH'),
        ('pph', 'PPH'),
        ('other', 'Other Obstetric Complications'),
        ('referred', 'Referred'),
    ]
    obstetric_complications = models.CharField(max_length=20, choices=OBSTETRIC_COMPLICATION_CHOICES, blank=True, null=True)
    
    alive = models.BooleanField()
    APGAR_score_1_5 = models.CharField(max_length=7)  # Format: "X/Y"
    
    SEX_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    sex = models.CharField(max_length=6, choices=SEX_CHOICES)
    
    weight_in_grams = models.PositiveIntegerField(validators=[MaxValueValidator(9999)])
    stillbirth = models.PositiveIntegerField(choices=[(1, 'Fresh'), (2, 'Macerated')], blank=True, null=True)
    live_birth_died_before_arrival = models.BooleanField(blank=True, null=True)
    live_birth_died_after_arrival_or_delivery = models.BooleanField(blank=True, null=True)
    mrn_newborn = models.PositiveIntegerField(validators=[MaxValueValidator(999999)], blank=True, null=True)
    vitamin_k = models.BooleanField(blank=True, null=True)
    ttc_eye_ointment = models.BooleanField(blank=True, null=True)
    # chlorhexidine = models.BooleanField(blank=True, null=True)
    bcg_given = models.BooleanField(blank=True, null=True)
    opv_given = models.BooleanField(blank=True, null=True)
    
    hiv_test_accepted = models.BooleanField()
    hiv_retesting_accepted = models.BooleanField(blank=True, null=True)
    hiv_test_result = models.CharField(max_length=8, choices=[('positive', 'Positive'), ('negative', 'Negative'), ('unknown', 'Unknown')], blank=True, null=True)
    known_hiv_positive = models.BooleanField(blank=True, null=True)
    target_population_category = models.CharField(max_length=255, blank=True, null=True)
    hiv_positive_delivery_link = models.CharField(max_length=1, choices=[('1', 'Same Facility'), ('2', 'Other Facility')], blank=True, null=True)
    counseled_on_feeding_options = models.BooleanField(blank=True, null=True)
    mothers_art_regimen = models.CharField(max_length=255, blank=True, null=True)
    newborn_nvp = models.CharField(max_length=255, blank=True, null=True)
    managed_by = models.CharField(max_length=255)
    remark = models.CharField(max_length= 200, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_records')
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='edited_records')

    def save(self, *args, **kwargs):
        # Ensure created_at and updated_at are timezone-aware
        if not self.pk:  # If this is a new record
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        
        # Make sure delivery_date is just a date (not a datetime)
        if isinstance(self.delivery_date, datetime):
            self.delivery_date = self.delivery_date.date()
            
        super().save(*args, **kwargs)

    # def __str__(self):
    #     return f"{self.mrn} - {self.delivery_date.strftime('%Y-%m-%d')}"

    class Meta:
        indexes = [
            models.Index(fields=['mrn']),
            models.Index(fields=['name']),
            models.Index(fields=['mode_of_delivery']),
            models.Index(fields=['maternal_status']),
            models.Index(fields=['delivery_date']),
            models.Index(fields=['alive']),
            models.Index(fields=['sex']),
            models.Index(fields=['hiv_test_result']),
            # Composite index for date and status combinations
            models.Index(fields=['delivery_date', 'maternal_status']),
            models.Index(fields=['delivery_date', 'mode_of_delivery']),
        ]
        ordering = ['serial_number']
        verbose_name = 'Delivery Record'
        verbose_name_plural = 'Delivery Records'
