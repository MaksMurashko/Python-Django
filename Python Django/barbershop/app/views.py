from django.shortcuts import render,redirect, get_object_or_404
from app.models import Barber,Shift,Client
from app.templates.forms import BarberForm,ShiftForm,ClientForm
from django.db.models import Count
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required, user_passes_test
 
def index(request):
    return render(request, "index.html")

class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

#БАРБЕРЫ
@login_required
def barbers(request):
    year = request.GET.get('year')  # Получаем год из параметров запроса
    barbers = Barber.objects.all()
    most_shifts_barber = None
    error_message = None
    
    if year:
        try:
            year = int(year)
            if year < 1000 or year > 9999:
                raise ValueError('Неверный формат года.')
            barbers = barbers.filter(shifts__date__year=year)
            barbers = barbers.distinct()  # Применяем метод .distinct() для получения уникальных записей барберов
            most_shifts_barber = barbers.annotate(num_shifts=Count('shifts')).order_by('-num_shifts').first()
        except ValueError as e:
            error_message = str(e)
    
    return render(request, 'barbers.html', {'barbers': barbers, 'most_shifts_barber': most_shifts_barber, 'year': year, 'error_message': error_message})

@login_required
def barber_create(request):
    if request.method == 'POST':
        form = BarberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('barbers')
    else:
        form = BarberForm()
    return render(request, 'barber_create.html', {'form': form, 'errors': form.errors})

@login_required
def barber_update(request, pk):
    barber = get_object_or_404(Barber, pk=pk)
    if request.method == 'POST':
        form = BarberForm(request.POST, instance=barber)
        if form.is_valid():
            form.save()
            return redirect('barbers')
    else:
        form = BarberForm(instance=barber)
    return render(request, 'barber_update.html', {'form': form, 'barber': barber, 'errors': form.errors})

@login_required
def barber_delete(request, pk):
    barber = get_object_or_404(Barber, pk=pk)
    if request.method == 'POST':
        barber.delete()
        return redirect('barbers')
    return render(request, 'barber_delete.html', {'barber': barber})

@login_required
def barber_shifts(request, pk):
    barber = Barber.objects.get(pk=pk)
    shifts = Shift.objects.filter(barber=pk)
    return render(request, 'barber_shifts.html', {'shifts': shifts, 'barber': barber})

#СМЕНЫ
@login_required
def shifts(request):
    shifts=Shift.objects.order_by('id')
    return render(request,'shifts.html',{'shifts':shifts})

@login_required
def shift_create(request):
    if request.method == 'POST':
        form = ShiftForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shifts')
    else:
        form = ShiftForm()
    return render(request, 'shift_create.html', {'form': form})

@login_required
def shift_update(request, pk):
    shift = get_object_or_404(Shift, pk=pk)
    if request.method == 'POST':
        form = ShiftForm(request.POST, instance=shift)
        if form.is_valid():
            form.save()
            return redirect('shifts')
    else:
        form = ShiftForm(instance=shift)
    return render(request, 'shift_update.html', {'form': form, 'shift': shift})

@login_required
def shift_delete(request, pk):
    shift = get_object_or_404(Shift, pk=pk)
    if request.method == 'POST':
        shift.delete()
        return redirect('shifts')
    return render(request, 'shift_delete.html', {'shift': shift})

#КЛИЕНТЫ
@login_required
def clients(request):
    clients=Client.objects.order_by('id')
    return render(request,'clients.html',{'clients':clients})

@login_required
def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clients')
    else:
        form = ClientForm()
    return render(request, 'client_create.html', {'form': form})

@login_required
def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('clients')
    else:
        form = ClientForm(instance=client)
    return render(request, 'client_update.html', {'form': form, 'client': client})

@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client.delete()
        return redirect('clients')
    return render(request, 'client_delete.html', {'client': client})
