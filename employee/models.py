from django.contrib.auth.models import User
from django.db import models

# Create your models here.
def Profile_directory_path(instance, filename):
    return 'ProfilesPic/{0}/profile/{1}'.format(instance.name, filename)
class EmployeeDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    urname = models.CharField(max_length=25, null=True, blank=True)
    pwd = models.CharField(max_length=25, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    salary = models.CharField(max_length=10, null=True, blank=True)
    emp_num = models.IntegerField(null=True, blank=True)
    owner = models.BooleanField(default=False,null=True,blank=True)
    photo = models.ImageField(blank=True, null=True, default="person.png", upload_to=Profile_directory_path)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.name} '

class EmpolyAttendence(models.Model):
    name = models.ForeignKey(EmployeeDetail, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    in_time = models.TimeField(null=True, blank=True)
    out_time = models.TimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    action = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return f'{self.name.emp_num} '


class EmpolySalary(models.Model):
    name = models.ForeignKey(EmployeeDetail, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    deducte = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    sal_adv = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    create = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.name.name} '

class EmpolyRequest(models.Model):
    name = models.ForeignKey(EmployeeDetail, on_delete=models.CASCADE, null=True, blank=True)
    request_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name="request")
    date = models.DateField(null=True, blank=True)
    d_from = models.DateField(null=True, blank=True)
    d_to = models.DateField(null=True, blank=True)
    vctn = models.BooleanField(default=False,null=True, blank=True)
    decription = models.CharField(max_length=150, null=True, blank=True)
    action = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    create = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.name.name} '

class EmpolyAdvance(models.Model):
    name = models.ForeignKey(EmployeeDetail, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    install = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    period = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    Remaining = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    status = models.CharField(max_length=50, blank=True, null=True, default='PENDING')
    create = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.name.name} '

class AdvanceAcc(models.Model):
    advnce = models.ForeignKey(EmpolyAdvance, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    install = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)


