from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def logout_view(request):
    '''Завершает сеанс работы с приложением'''
    logout(request)
    return HttpResponseRedirect(reverse('learning_logs:index'))


def register(request):
    '''Регистрирует нового пользователя'''
    if request.method != 'POST':
        # Отпрвака пустой регистрационной формы
        form = UserCreationForm()
    else:
        # Обработка заполненой формы
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # Выполнение входа и перенаправление на домашнюю страницу
            authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('learning_logs:index'))

    context = {'form': form}
    return render(request, 'users/register.html', context)