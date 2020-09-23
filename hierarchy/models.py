from django.db import models


class DepartmentType(models.Model):
    name = models.CharField(max_length=32, null=False, unique=True)

    def __str__(self):
        return f"{self.name}"


class Department(models.Model):
    department_type = models.ForeignKey(DepartmentType, null=True, blank=True, on_delete=models.SET_NULL)
    parent_department = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=256, null=False)
    short_name = models.CharField(max_length=64, null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    logo = models.ImageField(
        upload_to="resources/logo/",
        default="resources/default/department.png",
        null=True,
        blank=True,
    )
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"({self.short_name}) {self.name}"

    def as_dict(self):
        return {
            "type": None if self.department_type is None else self.department_type.name,
            "parent_id": None if self.parent_department is None else self.parent_department.pk,
            "name": self.name,
            "short_name": self.short_name,
            "link": self.link,
            "logo": self.logo.url,
            "is_approved": self.is_approved,
        }


class Subject(models.Model):
    departments = models.ManyToManyField(Department)
    name = models.CharField(max_length=256, null=False)
    short_name = models.CharField(max_length=16, null=True, blank=True)
    semester = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.displayed_title()

    def displayed_title(self):
        return f"{self.name} ({self.semester} сем.)" if self.semester != 0 else self.name

    def as_dict(self):
        return {
            "department_id": None if self.departments is None else self.departments.pk,
            "name": self.name,
            "short_name": self.short_name,
            "semester": None if not self.semester else self.semester,
        }