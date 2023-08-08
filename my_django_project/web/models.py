from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class WorkflowType(models.Model):
    id = models.AutoField(primary_key=True)
    workflow_name = models.CharField(max_length=100, null=True, blank=True)
    workflow_code = models.CharField(max_length=25, null=True, blank=True)

    def  __str__(self):
        return self.workflow_name
    
class Status(models.Model):
    status_name = models.CharField(max_length=100, null=True, blank=True)

    def  __str__(self):
        return self.status_name
    
class DesignationMaster(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def  __str__(self):
        return self.name

class RoleMaster(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def  __str__(self):
        return self.name

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not id:
            raise ValueError("The ID field must be set")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    # id = models.AutoField(primary_key=True)
    userTypeId = models.CharField(max_length=100,null=True)
    emp_id =  models.CharField(max_length=100, unique=True,null=True)
    username = models.CharField(max_length=100, unique=True,db_index=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=50,blank=True)
    date_joined=models.DateField(auto_now=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    date_of_birth = models.DateField(null=True)
    email=models.EmailField(null=True, blank=True)
    primary_phn= models.CharField(max_length=20,blank=True)
    secondary_phn = models.CharField(max_length=20,blank=True)
    designation = models.ForeignKey(DesignationMaster, on_delete=models.CASCADE,null=True)
    role = models.ForeignKey(RoleMaster, on_delete=models.CASCADE,null=True)
    org_name =  models.CharField(max_length=100,null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE,null=True)
    ###########################################################
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='customuser_set',
        related_query_name='customuser',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='customuser_set',
        related_query_name='customuser',
    )
    created_at = models.DateTimeField(auto_now_add=True,null=True)


    # Add other fields from your CustomUser model here

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    # Add other required fields for authentication (e.g., 'password', 'username', etc.)

    def __str__(self):
        return self.username
    

class Projects(models.Model):
    
    proj_name = models.CharField(max_length=50, null=True, verbose_name='Project Name')
    # project_count = models.IntegerField(null=True)
    proj_isbn = models.CharField(max_length=50, null=True)
    proj_workflowType = models.ForeignKey(WorkflowType,on_delete=models.CASCADE)
    proj_status = models.ForeignKey(Status,on_delete=models.CASCADE)
    proj_no_of_chapters = models.IntegerField(null=True)
    due_date=models.DateField(null=True,blank=True)

    def __str__(self) -> str:
        return self.proj_name

class UserAttendance(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    login_time = models.DateTimeField()
    logout_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField(null=True, blank=True)

    def __str__(self):
        formatted_login_time = self.login_time.strftime('%b %d, %Y %I:%M %p')
        formatted_create_time = self.created_at.strftime('%b %d, %Y %I:%M %p')
        if self.logout_time:
            formatted_logout_time = self.logout_time.strftime('%b %d, %Y %I:%M %p')
            return f"{self.user.username} - {formatted_login_time} to {formatted_logout_time} at {formatted_create_time}"
        else:
            return f"{self.user.username} - {formatted_login_time} (still logged in) at {formatted_create_time}"
        


class Break(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
