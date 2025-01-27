from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from core.models import DeliveryRecord  


# Create your views here.

@login_required

def dashboard(request):
    # Get the current user
    user = request.user

    # Calculate counts based on the user's records
    today = timezone.now().date()
    daily_count = DeliveryRecord.objects.filter(created_by=user, created_at__date=today).count()
    weekly_count = DeliveryRecord.objects.filter(created_by=user, created_at__gte=today - timezone.timedelta(days=7)).count()
    monthly_count = DeliveryRecord.objects.filter(
        created_by=user,
        created_at__year=today.year,
        created_at__month=today.month
    ).count()
    total_count = DeliveryRecord.objects.filter(created_by=user).count()

    return render(request, 'account/dashboard.html', {
        'section': 'dashboard',
        'daily_count': daily_count,
        'weekly_count': weekly_count,
        'monthly_count': monthly_count,
        'total_count': total_count,
    })
    
def forgot_password(request):
    return render(request, 'account/forgot_password.html', {'section': 'forgot_password'})