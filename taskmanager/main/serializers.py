from rest_framework.serializers import ModelSerializer, SerializerMethodField, IntegerField, DecimalField, CharField
from .models import Task, SubTaskTaskRelations, SubTask


class SubTaskSerializer(ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'


class VueSerializer(ModelSerializer):
    # bool_count = SerializerMethodField()
    annotated_bool = IntegerField(read_only=True)
    timestamp = DecimalField(max_digits=3, decimal_places=2, read_only=True)
    final_price = IntegerField(read_only=True)
    subtask = SubTaskSerializer(many=True)
    owner_name = CharField(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'task', 'owner_name', 'subtask', 'annotated_bool', 'timestamp', 'final_price']

    # def get_bool_count(self, instance):
    #     return SubTaskTaskRelations.objects.filter(task=instance, bool=True).count()


class SubTaskTaskSerializer(ModelSerializer):
    class Meta:
        model = SubTaskTaskRelations
        fields = "__all__"


