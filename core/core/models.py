from django.db import models
from django.contrib.auth.hashers import make_password

class TaskCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Worker(models.Model):
    personnel_number = models.PositiveIntegerField(primary_key=True)
    password = models.CharField(max_length=50, null=False, blank=False)
    firstname = models.CharField(max_length=100, null=False, blank=False)
    lastname = models.CharField(max_length=150, null=False, blank=False)
    phone_number = models.CharField(max_length=11, null=False, blank=False)
    expertise = models.CharField(max_length=100, null=True, blank=True)
    current_tasks = models.PositiveIntegerField(default=0, null=False, blank=True)
    satisfaction = models.PositiveIntegerField(default=5, choices=[(i, i) for i in range(1, 11)])

    def __str__(self):
        return f"{self.firstname} {self.lastname} (ID: {self.personnel_number})"

class FacilitiesManager(models.Model):
    identifier = models.PositiveIntegerField(primary_key=True)
    password = models.CharField(max_length=50, null=False, blank=False)
    organization = models.CharField(max_length=200, null=False, blank=False)
    branch = models.CharField(max_length=100, null=False, blank=False)
    workers = models.ManyToManyField(Worker)
    task_categories = models.ManyToManyField(TaskCategory)
    image = models.ImageField(upload_to='Facilities_images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('organization', 'branch')

    def __str__(self):
        return f"{self.organization} - {self.branch} (ID: {self.identifier})"


class Applicant(models.Model):
    department = models.CharField(max_length=100, primary_key=True)
    organization = models.CharField(max_length=200, null=False, blank=False)
    password = models.CharField(max_length=50, null=False, blank=False)
    firstname = models.CharField(max_length=100, null=False, blank=False)
    lastname = models.CharField(max_length=100, null=False, blank=False)
    phone_number = models.CharField(max_length=11, null=False, blank=False)

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.department} - {self.organization}"

class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, null=False, blank=False)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    facility = models.ForeignKey(FacilitiesManager, on_delete=models.CASCADE)
    category = models.ForeignKey(TaskCategory, on_delete=models.CASCADE)
    registration_time = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    estimated_time = models.DurationField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=[
        ('Pending', 'در انتظار'),
        ('In Progress', 'در حال انجام'),
        ('Completed', 'تکمیل شده')
    ])
    requester_description = models.TextField(blank=False, null=False)
    worker_description = models.TextField(blank=True, null=True)
    # current_worker = models.ForeignKey(Worker, on_delete=models.SET_NULL, blank=True, null=True)
    current_worker = models.ManyToManyField(Worker, blank=True, related_name='current_worker')

    def __str__(self):
        return f"Task {self.task_id} - {self.status}"