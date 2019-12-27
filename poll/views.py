from django.http import HttpResponse
from django.shortcuts import get_object_or_404,render
#from django.template import loader

from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # LONGER WAY:
    '''
    template = loader.get_template('poll/index.html')
    context = {
        'latest_question_list': latest_questions_list,
    }
    return HttpResponse(template.render(context, request))
    '''
    #SHORTER WAY:
    context = {'latest_question_list': latest_question_list}
    return render(request, 'poll/index.html', context)

def detail(request, question_id):
    # METHOD:1 =>
    """
    try:
        question = Question.objects.get(pk = question_id)
    except Question.DoesNotExist:
        raise Http404("Question Doesn't Exist")
    return render(request, 'poll/detail.html', {'question': question})
    """
    # METHOD:2 => 
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'poll/detail.html', {'question':question})

def results(request, question_id):
    response = "You are looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)