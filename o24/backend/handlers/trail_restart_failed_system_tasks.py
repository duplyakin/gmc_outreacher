import o24.backend.models.shared as shared
import o24.backend.dashboard.models as models
from o24.globals import *
import datetime
from mongoengine.queryset.visitor import Q

def restart_system_failed_tasks():
    shared.TaskQueue.objects(result_data__code__lte=TRAIL_UNKNOWN_ERROR).update(status=NEW)

if __name__ == '__main__':
    restart_system_failed_tasks()
