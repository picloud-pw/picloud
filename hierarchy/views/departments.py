from django.http import JsonResponse

from hierarchy.models import Department, Subject


def get_all_departments(request):

    departments = [d.as_dict() for d in Department.objects.all()]

    return JsonResponse({
        "departments": departments,
    })


def get_department(request, department_id):

    if not request.user.is_authenticated:
        return JsonResponse({
            "message": {
                "text": "User is not authenticated.",
                "type": "error",
            }
        }, status=401)

    department = Department.objects.filter(pk=department_id)
    if len(department) != 1:
        return JsonResponse({
            "message": {
                "text": "Department not found.",
                "type": "error",
            }
        }, status=404)
    department = department.first()

    return JsonResponse({"department": department.as_dict()})


def approve_department(request, department_id):
    department = Department.objects.filter(pk=department_id)
    if len(department) != 1:
        return JsonResponse({
            "message": {
                "text": "Department not found.",
                "type": "error",
            }
        }, status=404)
    department = department.first()

    department.is_approved = True
    department.save()

    return JsonResponse({
        "message": {
            "text": "Department approved.",
            "type": "success",
        }
    })


def delete_department(request, department_id):
    if not request.user.is_staff and not request.user.is_superuser:
        return JsonResponse({
            "message": {
                "text": "To perform the operation, you must be staff or superuser.",
                "type": "error",
            }
        }, status=403)

    department = Department.objects.filter(pk=department_id)
    if len(department) != 1:
        return JsonResponse({
            "message": {
                "text": "Department not found.",
                "type": "error",
            }
        }, status=404)
    department = department.first()

    department.delete()

    return JsonResponse({
        "message": {
            "text": "Department deleted.",
            "type": "success",
        }
    })


def get_subjects_by_department(request, department_id):
    department = Department.objects.filter(pk=department_id)
    if len(department) != 1:
        return JsonResponse({
            "message": {
                "text": "Department not found.",
                "type": "error",
            }
        }, status=404)
    department = department.first()

    subjects = [s.as_dict() for s in Subject.objects.filter(department=department) if s.is_approved]

    return JsonResponse({
        "department_id": department.pk,
        "subjects": subjects,
    })
