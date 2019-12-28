from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404,render
from django.urls import reverse
from django.views import generic
#from django.template import loader

from .models import Question, choice
# METHOD:1{SIMPLE BUT MORE_CODE}=>
"""
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
    '''
    try:
        question = Question.objects.get(pk = question_id)
    except Question.DoesNotExist:
        raise Http404("Question Doesn't Exist")
    return render(request, 'poll/detail.html', {'question': question})
    '''
    # METHOD:2 => 
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'poll/detail.html', {'question':question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'poll/results.html', {'question': question})
"""

# METHOD:2=>
class IndexView(generic.ListView):
    template_name = 'poll/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'poll/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'poll/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'poll/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('poll:results', args=(question.id,)))