from django.test import TestCase
from main.models import Task, SubTask, SubTaskTaskRelations
from main.serializers import SubTaskSerializer, VueSerializer
from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg, F


class VueSerializerTestCase(TestCase):
    def setUp(self):
        self.User = User.objects.create_user(username='User_test')

    def test_ok(self):
        sub_1 = SubTask.objects.create(title='sub_1', desc='abc', execute_time=50)
        sub_2 = SubTask.objects.create(title='sub_2', desc='abc', execute_time=50)
        sub_3 = SubTask.objects.create(title='sub_3', desc='abc', execute_time=50)

        task_1 = Task.objects.create(title='task1', task='task1', owner_id=self.User.id, discount=15)
        task_2 = Task.objects.create(title='task2', task='task2', owner_id=self.User.id, discount=25)

        SubTaskTaskRelations.objects.create(subtask=sub_1, task=task_1, bool=True,
                                            time=4)
        SubTaskTaskRelations.objects.create(subtask=sub_2, task=task_1, bool=True,
                                            time=5)
        SubTaskTaskRelations.objects.create(subtask=sub_3, task=task_1, bool=True,
                                            time=2)

        SubTaskTaskRelations.objects.create(subtask=sub_1, task=task_2, bool=True,
                                            time=3)
        SubTaskTaskRelations.objects.create(subtask=sub_2, task=task_2, bool=True,
                                            time=5)
        Ss_3 = SubTaskTaskRelations.objects.create(subtask=sub_3, task=task_2, bool=False)
        Ss_3.time = 4
        Ss_3.save()

        tasks = Task.objects.all().annotate(annotated_bool=Count(Case(When(subtasktaskrelations__bool=True, then=1))),
                                            final_price=F('base_count') - F('discount'),
                                            owner_name=F('owner__username')
                                            ).prefetch_related('subtask').order_by('id')
        data = VueSerializer(tasks, many=True).data

        expected_data = [
            {
                'id': task_1.id,
                'title': 'task1',
                'task': 'task1',
                'owner_name': task_1.owner.username,
                'subtask': [
                    {
                      'id': sub_1.id,
                      'title': 'sub_1',
                      'desc': 'abc',
                      'execute_time': 50
                    },
                    {
                      'id': sub_2.id,
                      'title': 'sub_2',
                      'desc': 'abc',
                      'execute_time': 50
                    },
                    {
                      'id': sub_3.id,
                      'title': 'sub_3',
                      'desc': 'abc',
                      'execute_time': 50
                    }
                ],
                'annotated_bool': 3,
                'timestamp': '3.67',
                'final_price': 85
            },
            {
                'id': task_2.id,
                'title': 'task2',
                'task': 'task2',
                'owner_name': task_1.owner.username,
                'subtask': [
                    {
                        'id': sub_1.id,
                        'title': 'sub_1',
                        'desc': 'abc',
                        'execute_time': 50
                    },
                    {
                        'id': sub_2.id,
                        'title': 'sub_2',
                        'desc': 'abc',
                        'execute_time': 50
                    },
                    {
                        'id': sub_3.id,
                        'title': 'sub_3',
                        'desc': 'abc',
                        'execute_time': 50
                    }
                ],
                'annotated_bool': 2,
                'timestamp': '4.00',
                'final_price': 75
            }
        ]
        # print(expected_data)
        # print(data)
        self.assertEqual(expected_data, data)
