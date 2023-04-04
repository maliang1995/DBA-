from django.shortcuts import render
import hashlib
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PasswordRecord
import datetime
from django.utils import timezone
from datetime import datetime ,time

def generate_password(instance_id: str, username: str, length: int = 15) -> str:
    combined_input = f"{instance_id}-{username}"
    hashed_input = hashlib.sha256(combined_input.encode()).hexdigest()

    uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lowercase = 'abcdefghijklmnopqrstuvwxyz'
    digits = '0123456789'
    special_chars = '!@#$%^&*_()'

    password = []
    for i in range(length):
        if i % 4 == 0:
            password.append(uppercase[int(hashed_input[i], 16) % 26])
        elif i % 4 == 1:
            password.append(lowercase[int(hashed_input[i], 16) % 26])
        elif i % 4 == 2:
            password.append(digits[int(hashed_input[i], 16) % 10])
        else:
            password.append(special_chars[int(hashed_input[i], 16) % 10])

    return ''.join(password)
from datetime import timedelta
@login_required
def index(request):
    # 在这里使用默认值初始化变量
    instance_id = ""
    username = ""
    password = ""

    if request.method == 'POST':
        instance_id = request.POST['instance_id'].strip()
        username = request.POST['username']
        password = generate_password(instance_id, username)

        if instance_id == "":
            instance_id = None

        existing_record = PasswordRecord.objects.filter(instance_id=instance_id, username=username).first()

        if existing_record:
            existing_record.generated_password = password
            existing_record.created_at = timezone.now()  # 使用 timezone.now() 代替 datetime.datetime.now()
            existing_record.save()
        else:
            record = PasswordRecord(instance_id=instance_id, username=username, generated_password=password, created_at=timezone.now())  # 使用 timezone.now() 代替 datetime.datetime.now()
            record.save()

    # 获取当天的记录
    today = timezone.now().date()  # 使用 timezone.now().date()
    start_of_today = timezone.make_aware(datetime.combine(today, time.min))
    end_of_today = timezone.make_aware(datetime.combine(today, time.max))

    records_today = PasswordRecord.objects.filter(created_at__range=(start_of_today, end_of_today))
    return render(request, 'index.html', {'instance_id': instance_id, 'username': username, 'password': password, 'records': records_today})

def view_records(request):
    records = PasswordRecord.objects.all()
    return render(request, 'records.html', {'records': records})

def delete_record(request, record_id):
    if request.method == 'POST':
        record = PasswordRecord.objects.get(id=record_id)
        record.delete()
        return redirect('index')
    else:
        return redirect('index')
