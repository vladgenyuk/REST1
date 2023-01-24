from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from .models import Task, SubTask, SubTaskTaskRelations
from .forms import TaskForm
from .permissons import IsOwnerOrReadOnly
from .serializers import VueSerializer, SubTaskTaskSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Case, Count, When, Avg, F, Q


def index(request):
    tasks = Task.objects.prefetch_related('subtask').order_by('id')[:]
    return render(request, 'main/index.html', {'title': 'главная страница сайта', 'tasks': tasks})


def about(request):

    return render(request, 'main/about.html')


def admin(request):
    return render(request, 'main/admin.html')


class create(CreateView):
    model = Task
    form_class = TaskForm
    context_object_name = "form"
    template_name = 'main/create.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(create, self).form_valid(form)


class VueApi(viewsets.ModelViewSet):
    queryset = Task.objects.all().annotate(annotated_bool=Count(Case(When(subtasktaskrelations__bool=True, then=1))),
                                        final_price=F('base_count') - F('discount'),
                                        owner_name=F('owner__username')
                                           ).prefetch_related('subtask').order_by('id')
    permission_classes = []
    serializer_class = VueSerializer

    def list(self, request):
        queryset = self.queryset
        serializer = VueSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.queryset
        user = get_object_or_404(queryset, pk=pk)
        serializer = VueSerializer(user)
        return Response(serializer.data)


class SubTaskTaskView(UpdateModelMixin, GenericViewSet):
    permission_classes = []
    queryset = SubTaskTaskRelations.objects.all()
    serializer_class = SubTaskTaskSerializer

    def list(self, request):
        queryset = self.queryset
        serializer = SubTaskTaskSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.queryset
        user = get_object_or_404(queryset, pk=pk)
        serializer = SubTaskTaskSerializer(user)
        return Response(serializer.data)


def auth(request):
    return render(request, 'main/oauth.html')
