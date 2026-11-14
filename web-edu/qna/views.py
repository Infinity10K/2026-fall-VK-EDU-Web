from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_POST

from qna.forms import LoginForm, RegisterForm, ImageForm
from qna.models import ImageModel, ImageLike

# Create your views here.

QUESTION_LIST = [
    {
        'id': i,
        'title': f'Title {i}',
        'text': f'Text {i}' * 10,
    }
    for i in range(30)
]


@login_required(login_url='/login')
def index(request):
    page_number = int(request.GET.get('page', 1))

    page = Paginator(QUESTION_LIST, 5)
    page_obj = page.page(page_number)

    return render(request, 'qna/index.html', context={'questions': page_obj.object_list, 'page_obj': page_obj})

def hot(request):
    return render(request, 'qna/hot.html', context={'questions': QUESTION_LIST[::-1]})

def login(request):
    print(f'{request.GET=}')
    print(f'{request.POST=}')


    if request.method == 'POST':
        form = LoginForm(request.POST)


        if form.is_valid():
            print(f"{form.cleaned_data=}")

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                form.add_error(None, 'Username or password is incorrect.')
    else:
        form = LoginForm()

    return render(request, 'qna/login.html', context={'form': form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return HttpResponseRedirect(reverse('index'))
    else:
        form = RegisterForm()

    return render(request, 'qna/register.html', context={'form': form})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required(login_url='/login')
def images(request):
    user = request.user
    image_objects = ImageModel.objects.annotate(likes_count=Count('image_like')).all()

    if request.method == 'POST':
        print(f"{request.POST=}")
        print(f"{request.FILES=}")
        form = ImageForm(user, request.POST, request.FILES)
        if form.is_valid():
            print(f"{form.cleaned_data=}")
            form.save()
            return HttpResponseRedirect(reverse('images'))
    else:
        form = ImageForm(user)

    return render(request, 'qna/images.html', context={'form': form, 'images': image_objects})

@login_required(login_url='/login')
def like(request, image_id):
    image = ImageModel.objects.filter(id=image_id).first()
    if image:
        image_like, created = ImageLike.objects.get_or_create(image=image, user=request.user)
        if not created:
            image_like.delete()

    return HttpResponseRedirect(reverse('images'))


@require_POST
@login_required(login_url='/login')
def like_async(request, image_id):
    image = ImageModel.objects.annotate(likes_count=Count('image_like')).filter(id=image_id).first()

    if image:
        image_like, created = ImageLike.objects.get_or_create(image=image, user=request.user)
        if not created:
            image_like.delete()

    return JsonResponse({'count': image.likes_count})
