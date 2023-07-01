from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from datetime import datetime
from .filters import PostFilter
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect

from django.views import View
from .tasks import *

import logging

logger = logging.getLogger(__name__)


class PostList(ListView):
    model = Post
    ordering = 'text'
    template_name = 'post.html'
    queryset = Post.objects.order_by('-date_time')
    context_object_name = 'post'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.datetime.utcnow()

        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'link.html'
    context_object_name = 'post_link'


class SearchList(ListView):
    model= Post
    template_name = 'search.html'
    context_object_name = 'search'
    paginate_by = 5

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.get_filter()
        return context


class PostAdd(PermissionRequiredMixin, CreateView):
    raise_exception = True
    model = Post
    template_name = 'post_create.html'
    context_object_name = 'Create'
    form_class = PostForm
    permission_required = ('news.add_post',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Добавление статьи на сайт'
        return context

    def form_valid(self, form):
        form.instance.Author = self.request.user
        form.save()
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    model = Post
    template_name = 'post_update.html'
    context_object_name = 'post_update'
    form_class = PostForm
    permission_required = ('news.change_post',)
    login_url = 'home'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = f'Обновление статьи: {self.object.heading}'
        return context

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('home')
    context_object_name = 'post_delete'
    template_name = 'post_delete.html'
    permission_required = ('news.delete_post',)
    login_url = 'home'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = f'Удаление статьи: {self.object.heading}'
        return context


class CategoryList(PostList):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self, ):
        self.postCategory = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(postCategory=self.postCategory).order_by('-date_time')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.postCategory.subscriber.all()
        context['there_are_subscriber'] = self.request.user in self.postCategory.subscriber.all()
        context['category'] = self.postCategory
        return context


@login_required
@csrf_protect
def subscriber(request, pk):
    user = request.user
    postCategory = Category.objects.get(id=pk)
    postCategory.subscriber.add(user)
    message = 'Вы успешно подписались на рассылку новостей категории'
    return render(request, 'subscriber.html', {'category': postCategory, 'message': message})

@login_required
@csrf_protect
def unsubscriber(request, pk):
    user = request.user
    postCategory = Category.objects.get(id=pk)
    postCategory.subscriber.remove(user)
    message = 'Вы успешно отписались на рассылку новостей категории'
    return render(request, 'subscriber.html', {'category': postCategory, 'message': message})


class WeekView(View):
    def get(self, request):
        notify_about_new_post.delay()
        print('celery working')
        return redirect("/")


class WeekViews(View):
    def get(self, request):
        notify_weekly.delay()
        print('celery work')
        return redirect("/")