from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK
from django.urls import reverse
from main.models import Task, SubTaskTaskRelations, SubTask
from main.serializers import VueSerializer
from django.db.models import Count, Case, When, Avg, Sum, F
from django.test.utils import CaptureQueriesContext
from django.db import connection


class ApiTestCase(APITestCase):
    def setUp(self):
        sub_1 = SubTask.objects.create(title='sub_1')
        self.task_1 = Task.objects.create(title='Task', task='Do smt', owner_id=None)
        self.task_2 = Task.objects.create(title='Sask', task='Do smt2', owner_id=None)
        self.task_3 = Task.objects.create(title='Task3', task='Do smt2', owner_id=None)
        SubTaskTaskRelations.objects.create(subtask=sub_1, task=self.task_1, bool=True,
                                            time=3)
        SubTaskTaskRelations.objects.create(subtask=sub_1, task=self.task_1, bool=True,
                                            time=5)

    def test_get(self):
        url = reverse('api-list')
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(url)
            self.assertEqual(2, len(queries))
            # print('queries ===', len(queries))
        tasks = Task.objects.all().annotate(annotated_bool=Count(Case(When(subtasktaskrelations__bool=True, then=1))),
                                            final_price=F('base_count') - F('discount'),
                                            owner_name=F('owner__username')
                                            ).prefetch_related('subtask').order_by('id')
        serializer_data = VueSerializer(tasks, many=True).data
        # print(serializer_data)
        # print(response.data)
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(serializer_data[0]['timestamp'], '4.00')
        self.assertEqual(HTTP_200_OK, response.status_code)



