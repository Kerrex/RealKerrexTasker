from django.db.models import Q

from kerrex_tasker.models import UserProjectPermission, Project


def has_permissions(project_id, user):
    project_query = Project.objects.filter(id=project_id)
    is_owner = project_query.filter(owner=user).exists()
    has_given_permission = UserProjectPermission.objects.filter(
        Q(project_id=project_id)
        & Q(user_id=user.id)
        & (Q(permission_id=1)
           | Q(permission_id=3))).exists()
    return is_owner or has_given_permission or (allowed_by_default_permission(project_query.first())
                                                and not is_user_blocked(project_id, user))


def is_user_blocked(project_id, user):
    return UserProjectPermission.objects.filter(project_id=project_id, user_id=user.id, permission_id=4)


def allowed_by_default_permission(project):
    return project.default_permission_id == 1 or project.default_permission_id == 3
