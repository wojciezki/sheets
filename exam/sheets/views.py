from django_filters import rest_framework as dfilters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from url_filter.integrations.drf import DjangoFilterBackend

from sheets.models import ExamSheet, Task, Answer, Solution
from sheets.permissions import IsObjectOwnerPermissions
from sheets.serializers import ExamSheetSerializer, TaskSerializer, AnswerSerializer, SolutionSerializer


class BaseViewSet(viewsets.ModelViewSet):
    serializers = {
        'default': None,
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers['default'])

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def perform_update(self, serializer):
        serializer.save(editor=self.request.user)


class ExamSheetViewSet(BaseViewSet):
    queryset = ExamSheet.objects.all()
    serializers = {
        'default': ExamSheetSerializer, }
    permission_classes = (IsObjectOwnerPermissions,)
    filter_backends = (DjangoFilterBackend, OrderingFilter, dfilters.DjangoFilterBackend)

    filter_fields = ('creator', 'template')

    ordering_fields = ('creator', 'name', 'created', 'template')

    @action(methods=['get', ], detail=False)
    def exams(self, request):
        exams = ExamSheet.objects.filter(template=False)
        serializer = self.get_serializer(exams, many=True)
        return Response(serializer.data)

    @action(methods=['get', ], detail=False)
    def templates(self, request):
        exams = ExamSheet.objects.filter(template=True)
        serializer = self.get_serializer(exams, many=True)
        return Response(serializer.data)


class TaskViewSet(BaseViewSet):
    queryset = Task.objects.all()
    serializers = {
        'default': TaskSerializer,
    }
    permission_classes = (IsObjectOwnerPermissions,)


class SolutionViewSet(BaseViewSet):
    queryset = Solution.objects.all()
    serializers = {
        'default': SolutionSerializer,
    }
    permission_classes = (IsObjectOwnerPermissions,)


class AnswerViewSet(BaseViewSet):
    queryset = Answer.objects.all()
    serializers = {
        'default': AnswerSerializer,
    }
