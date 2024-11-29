import graphene
from graphene_django import DjangoObjectType
from .models import Task
from django.core.cache import cache 
class TaskType(DjangoObjectType):
    class Meta:
        model = Task
        fields = ("id", "title", "description", "status", "created_at", "updated_at")

class Query(graphene.ObjectType):
    all_tasks = graphene.List(TaskType)
    task_by_status = graphene.List(TaskType, status=graphene.String())

    def resolve_all_tasks(root, info):
        cache_key = "all_tasks"
        tasks = cache.get(cache_key)
        if tasks is None:
            tasks = list(Task.objects.all())
            cache.set(cache_key, tasks, timeout=60 * 5) 
        return tasks

    def resolve_task_by_status(root, info, status):
        cache_key = f"tasks_status_{status}"
        tasks = cache.get(cache_key) 
        if tasks is None:
            tasks = list(Task.objects.filter(status=status)) 
            cache.set(cache_key, tasks, timeout=60 * 5) 
        return tasks

schema = graphene.Schema(query=Query)
