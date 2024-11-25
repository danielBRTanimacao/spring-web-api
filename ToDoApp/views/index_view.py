from django.shortcuts import render, redirect, get_object_or_404
from ToDoApp.models import Task
from ToDoApp.task_form import TaskForm

# Create your views here.
def index(request):
    if request.user.is_anonymous:
        return redirect('login')
    
    tasks = Task.objects.filter(user=request.user)
    form = TaskForm()

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('index')

    context = {
        'title': 'index',
        'tasks': tasks,
        'form': form
    }
    return render(request, 'pages/index.html', context)

def task_view(request, name, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    form = TaskForm(instance=task)

    if request.method == "POST":
        form = TaskForm(data=request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('index')

    context = {
        'title': f'task de {name}',
        'form': form
    }
    return render(request, 'pages/task.html', context)