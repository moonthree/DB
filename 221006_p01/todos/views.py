from django.shortcuts import render, redirect
from .models import Todo
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.contrib.auth.decorators import login_required
from .forms import TodoForm
# Create your views here.
def index(request):
    todos = Todo.objects.order_by('-pk')
    context = {
        'todos': todos,
    }
    return render(request, 'todos/index.html', context)

@login_required
@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            # 작성 시 작성자 정보가 함께 저장될 수 있도록 save의 commit옵션을 활용
            print('--------------------', request.user)
            todo = form.save(commit=False)
            todo.author = request.user
            todo.save()
            return redirect('todos:index')
    else:
        form = TodoForm()
    context = {
        'form': form,
    }
    return render(request, 'todos/create.html', context)

@require_POST
def delete(request, pk):
    todo = Todo.objects.get(pk=pk)
    if request.user.is_authenticated:
        if request.user == todo.author:
            todo.delete()
            return redirect('todos:index')
    return redirect('todos:index')


@require_POST
def update(request, pk):
    todo = Todo.objects.get(pk=pk)
    print(todo.completed)
    if request.user.is_authenticated:
        if request.user == todo.author:
            if todo.completed:
                todo.completed = False
            else:
                todo.completed = True
            todo.save()
            return redirect('todos:index')
    return redirect('todos:index')