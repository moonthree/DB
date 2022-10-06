from django.shortcuts import render, redirect
from .models import Question, Comment
from .forms import QuestionForm, CommentForm
from django.views.decorators.http import require_http_methods, require_POST, require_safe
import random
# Create your views here.
@require_safe
def index(request):
    questions = Question.objects.all()
    context = {
        'questions': questions,
    }
    return render(request, 'eithers/index.html', context)

@require_http_methods(['GET', 'POST'])
def create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.save()
            return redirect('eithers:index')
    else:
        form = QuestionForm()
    context = {
        'form': form,
    }
    return render(request, 'eithers/create.html', context)

@require_safe
def detail(request, pk):
    question = Question.objects.get(pk=pk)
    comment_form = CommentForm()
    comments = question.comment_set.all()
    cnt_comments = len(comments)
    cnt_red = 0
    cnt_blue = 0
    red_per = 0
    blue_per = 0
    if cnt_comments != 0:
        for i in comments:
            if i.pick:
                cnt_red += 1
            else:
                cnt_blue += 1
        red_per = round(cnt_red/cnt_comments*100, 1)
        blue_per = round(cnt_blue/cnt_comments*100, 1)
    context = {
        'question': question,
        'comment_form': comment_form,
        'comments': comments,
        'cnt_red': cnt_red,
        'cnt_blue': cnt_blue,
        'red_per': red_per,
        'blue_per': blue_per,
    }
    return render(request, 'eithers/detail.html', context)

def random2(request):
    questions = Question.objects.all()
    length = len(questions)
    random_pick = random.randrange(1,length+1)
    #print('---------------------',random_pick)
    question = Question.objects.get(pk=random_pick)
    
    return redirect('eithers:detail', random_pick)

def comments_create(request, pk):
    question = Question.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    #print(comment_form)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        print(comment_form)
        comment.question = question
        comment_form.save()
    return redirect('eithers:detail', question.pk)

@require_http_methods(['GET', 'POST'])
def update(request, pk):
    question = Question.objects.get(pk=pk)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('eithers:detail', question.pk)
    else:
        form = QuestionForm(instance=question)
        context = {
            'form': form,
            'question': question,
        }
    return render(request, 'eithers/update.html', context)

@require_POST
def delete(request, pk):
    question = Question.objects.get(pk=pk)
    question.delete()
    return redirect('eithers:index')

def comments_delete(request, question_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect('eithers:detail', question_pk)