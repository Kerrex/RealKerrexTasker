from django.contrib.auth.models import User
from django.db.models import Q

from kerrex_tasker.models import UserProjectPermission, Project


def get_filter_params_for_available_project_query(user):
    return Q(owner=user) | (Q(userprojectpermission__user=user) & Q(userprojectpermission__permission_id__in=[1, 3]))


def has_permissions(project_id: int, user: User):
    project_query = Project.objects.filter(id=project_id)
    is_owner = project_query.filter(owner=user).exists()
    has_given_permission = UserProjectPermission.objects.filter(
        Q(project_id=project_id)
        & Q(user_id=user.id)
        & (Q(permission_id=1)
           | Q(permission_id=3))).exists()
    return is_owner or has_given_permission or (allowed_by_default_permission(project_query.first())
                                                and not is_user_blocked(project_id, user))


def is_user_blocked(project_id: int, user: User):
    return UserProjectPermission.objects.filter(project_id=project_id, user_id=user.id, permission_id=4).exists()


def allowed_by_default_permission(project):
    return project.default_permission_id == 1 or project.default_permission_id == 3


def has_permission_to_edit(project: Project, user: User):
    default_edit_permission = project.default_permission_id == 1
    has_perm_to_edit = UserProjectPermission.objects.filter(project=project, user_id=user.id,
                                                            permission_id=1).exists()

    return not ((not default_edit_permission and not has_perm_to_edit)
                or (default_edit_permission and is_user_blocked(project.id, user)))
