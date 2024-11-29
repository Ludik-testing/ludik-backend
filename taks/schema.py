import graphene
from graphene_django import DjangoObjectType
from .models import Task

class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        fields = ("id", "title", "description", "status", "created_at", "updated_at")

class Query(graphene.ObjectType):
    all_tasks = graphene.List(TaskType)
    task_by_status = graphene.List(TaskType, status=graphene.String())

    def resolve_all_tasks(root, info):
        return Task.objects.all()

    def resolve_task_by_status(root, info, status):
        return Task.objects.filter(status=status)

schema = graphene.Schema(query=Query)