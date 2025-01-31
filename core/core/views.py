from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password
from .utils import round_robin_prioritization
from django.contrib import messages
from .models import *

def login_view(request):

    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username.isdigit():
            messages.error(request, "شناسه باید یک عدد معتبر باشد.")
            return render(request, 'Login.html', {'username': username})

        if len(password) < 6:
            messages.error(request, "رمز عبور باید حداقل ۶ کاراکتر باشد.")
            return render(request, 'Login.html', {'username': username})

        username = int(username)
        try:
            facility = FacilitiesManager.objects.get(identifier=username)
            if check_password(password, facility.password):
                request.session['facility_id'] = facility.identifier
                messages.success(request, "ورود با موفقیت انجام شد.")
                return redirect('facilities_tasks', fac_id=facility.identifier)
            else:
                messages.error(request, "رمز عبور اشتباه است.")
        except FacilitiesManager.DoesNotExist:
            messages.error(request, "شناسه یافت نشد.")


    return render(request, 'Login.html')


@login_required
def list_of_tasks_view(request, fac_id):
    if not fac_id:
        return redirect('facility_login', fac_id)

    facility = get_object_or_404(FacilitiesManager, identifier=fac_id)
    tasks = Task.objects.filter(facility=facility)

    prioritized_tasks = round_robin_prioritization(tasks)

    return render(request, 'Task_List.html', {
        'facility': facility,
        'tasks': prioritized_tasks
    })
