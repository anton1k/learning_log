from django.shortcuts import render, get_object_or_404
from .models import Topic, Entry
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import TopicForm, EntryForm

# Create your views here.

def index(request):
    '''Домашняя страница приложения learning_logs'''
    return render(request, 'learning_logs/index.html')

def topics(request):
    '''Выводит список всех тем'''
    
    if request.user.is_anonymous:
        topics = Topic.objects.filter(public=True).order_by('date_added')
    else:
        topics = Topic.objects.filter(owner=request.user).order_by('date_added') | Topic.objects.filter(public=True).order_by('date_added')

    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    '''Выводит одну тему и все ее записи'''
    topic = get_object_or_404(Topic, id=topic_id)
    # Проверка того, что тема принадлежит текущему пользователю.
    check_topic_owner(request, topic)

    entries = topic.entry_set.order_by('-date_added')
    context = {
        'topic': topic,
        'entries': entries
        }
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    '''Определяет новую тему'''
    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма.
        form = TopicForm()
    else:
        # Отправлены данные POST; обработать данные.
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    '''Добавляет новую запись про конкретной теме'''
    topic = get_object_or_404(Topic, id=topic_id)

    check_topic_owner(request, topic)
    
    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма.
        form = EntryForm()
    else:
        # Отправлены данные POST; обработать данные.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))
    context = {
        'topic': topic,
        'form': form
    }
    return render(request, 'learning_logs/new_entry.html', context) 

@login_required
def edit_entry(request, entry_id):
    '''Рудактирует существущую запись'''
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    check_topic_owner(request, topic)

    if request.method != 'POST':
        # Исходный запрос; форма заполняется данными текущей записи.
        form = EntryForm(instance=entry)
    else:
        # Отправлены данные POST; обработать данные.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))
    context = {
        'entry': entry,
        'topic': topic,
        'form': form
    }
    return render(request, 'learning_logs/edit_entry.html', context) 

# @login_required
def del_entry(request, entry_id):
    '''Удаляет запись в теме'''
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    
    check_topic_owner(request, topic)

    entry.delete()
    return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))

@login_required
def del_topic(request, topic_id):
    '''Удаляет тему'''
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(request, topic)
    topic.delete()
    return HttpResponseRedirect(reverse('learning_logs:topics'))
    

def check_topic_owner(request, topic):
    # Проверка того, что тема принадлежит текущему пользователю.
    if topic.owner != request.user:
        raise Http404

