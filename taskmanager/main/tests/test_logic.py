from django.test import TestCase
from main.models import Task, SubTaskTaskRelations, SubTask
from main.logic import set_timestamp
from django.contrib.auth.models import User


class LogicTestCase(TestCase):
    def setUp(self):
        self.User = User.objects.create_user(username='User_test')

        sub_1 = SubTask.objects.create(title='sub_1', desc='abc', execute_time=50)
        sub_2 = SubTask.objects.create(title='sub_2', desc='abc', execute_time=50)
        sub_3 = SubTask.objects.create(title='sub_3', desc='abc', execute_time=50)

        self.task_1 = Task.objects.create(title='task1', task='task1', owner_id=self.User.id, discount=15)
        task_2 = Task.objects.create(title='task2', task='task2', owner_id=self.User.id, discount=25)

        SubTaskTaskRelations.objects.create(subtask=sub_1, task=self.task_1, bool=True,
                                            time=4)
        SubTaskTaskRelations.objects.create(subtask=sub_2, task=self.task_1, bool=True,
                                            time=5)
        SubTaskTaskRelations.objects.create(subtask=sub_3, task=self.task_1, bool=True,
                                            time=2)

        SubTaskTaskRelations.objects.create(subtask=sub_1, task=task_2, bool=True,
                                            time=3)
        SubTaskTaskRelations.objects.create(subtask=sub_2, task=task_2, bool=True,
                                            time=5)
        SubTaskTaskRelations.objects.create(subtask=sub_3, task=task_2, bool=False)

    def test_ok(self):
        set_timestamp(self.task_1)
        self.task_1.refresh_from_db()
        self.assertEqual(str(self.task_1.timestamp), '3.67')

