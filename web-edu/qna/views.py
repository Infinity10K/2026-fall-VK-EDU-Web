from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.

QUESTION_LIST = [
    {
        'id': i,
        'title': f'Title {i}',
        'text': f'Text {i}' * 10,
    }
    for i in range(30)
]

def index(request):
    page_number = int(request.GET.get('page', 1))

    page = Paginator(QUESTION_LIST, 5)
    page_obj = page.page(page_number)

    return render(request, 'qna/index.html', context={'questions': page_obj.object_list, 'page_obj': page_obj})

def hot(request):
    return render(request, 'qna/hot.html', context={'questions': QUESTION_LIST[::-1]})