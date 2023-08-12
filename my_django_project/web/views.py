from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
# Create your views here.
# from django.shortcuts import render
from .models import WorkflowType, CustomUser,Status,Projects, UserAttendance, Break,DesignationMaster,RoleMaster
from django.db.models import F, ExpressionWrapper, DurationField
from django.db.models.functions import TruncDate
from django.db.models import Sum
    
from datetime import datetime   
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.hashers import make_password, check_password

def create_user(request):
    if request.method == 'GET':
        designations = DesignationMaster.objects.all()
        roles = RoleMaster.objects.all()
        status = Status.objects.all()
        context = {'designations': designations, 'roles': roles,'status': status}
        return render(request, 'createuser.html',context)
    elif request.method == 'POST':
        userTypeId = request.POST.get('userTypeId')
        emp_id = request.POST.get('emp_id')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        # workflow_id= WorkflowType.objects.get(id=proj_workflowType)
        # status_id= Status.objects.get(id=proj_status)
        password= request.POST.get('password')
        # date_joined = request.POST.get('date_joined')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        email = request.POST.get('email')
        primary_phn = request.POST.get('primary_phn')
        secondary_phn = request.POST.get('secondary_phn')
        designationid = request.POST.get('designation')
        roleid = request.POST.get('role')
        org_name = request.POST.get('org_name')
        statusid = request.POST.get('status')
        designation = DesignationMaster.objects.get(id=designationid)
        role=RoleMaster.objects.get(id=roleid)
        status=Status.objects.get(id=statusid)
        try:

            user = CustomUser.objects.create(userTypeId=userTypeId,emp_id=emp_id,username=username,
                                             password=make_password(password),
                                             first_name=first_name,last_name=last_name,gender=gender,date_of_birth=date_of_birth,
                                             email=email,primary_phn=primary_phn,secondary_phn=secondary_phn,
                                             designation=designation,role=role,status=status,org_name=org_name)
        except Exception as e:
            raise e

        return redirect('users_view')


def edit_user(request,id):
    if request.method == 'GET':
        users= CustomUser.objects.get(id=id)
        designations = DesignationMaster.objects.all()
        roles = RoleMaster.objects.all()
        status = Status.objects.all()
        context = {'userdata':users,'designations': designations, 'roles': roles,'status': status}
        return render(request, 'edituser.html',context)
    elif request.method == 'POST':
        userTypeId = request.POST.get('userTypeId')
        emp_id = request.POST.get('emp_id')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        password= request.POST.get('password')
        # date_joined = request.POST.get('date_joined')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('date_of_birth')
        email = request.POST.get('email')
        primary_phn = request.POST.get('primary_phn')
        secondary_phn = request.POST.get('secondary_phn')
        designationid = request.POST.get('designation')
        roleid = request.POST.get('role')
        org_name = request.POST.get('org_name')
        statusid = request.POST.get('status')
        designation = DesignationMaster.objects.get(id=designationid)
        role=RoleMaster.objects.get(id=roleid)
        status=Status.objects.get(id=statusid)
        try:

            CustomUser.objects.filter(id=id).update(userTypeId=userTypeId,emp_id=emp_id,username=username,
                                             password=make_password(password),
                                             first_name=first_name,last_name=last_name,gender=gender,date_of_birth=date_of_birth,
                                             email=email,primary_phn=primary_phn,secondary_phn=secondary_phn,
                                             designation=designation,role=role,status=status,org_name=org_name)
        except Exception as e:
            raise e

        return redirect('users_view')

def users_view(request):
    users = CustomUser.objects.all()
    context = {"users":users}
    return render(request, 'user.html',context)

def delete_user(request,id):
    user =CustomUser.objects.get(id=id)
    user.delete()
    return redirect('users_view')

def userInOut(user):
    try:
        UserAttendance.objects.filter(user=user, logout_time=None).latest('login_time')
    except UserAttendance.DoesNotExist:
        UserAttendance.objects.create(user=user, login_time=timezone.now())

def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)

        try:
            user = CustomUser.objects.get(username=username)
            print(user.check_password(password))
            if user.check_password(password):
                user = authenticate(username=username, password=password)
                login(request, user)
                userInOut(user) #seperate logic for check in checkout
                return redirect('dashboard_view')
            messages.error(request, 'Invalid credentials. Please try again.')
            
            return render(request, 'login.html')
        except CustomUser.DoesNotExist:
            # Authentication failed
            messages.error(request, 'Invalid credentials. Please try again.')

    return render(request, 'login.html')

# @login_required
def logout_view(request):
    if request.user.is_authenticated:
        try:
            user_session = UserAttendance.objects.filter(user=request.user, logout_time=None).latest('created_at')
            user_session.logout_time = timezone.now()
            user_session.duration=(timezone.now() - user_session.login_time)
            user_session.save()
        except UserAttendance.DoesNotExist:
            pass

        logout(request)
    
    return redirect('login') 


@login_required
def project_view(request):
    if request.method == 'GET':
        projects = Projects.objects.filter(proj_manager=request.user.id)
        print(request.user.id)
        context = {'projects':projects,}
        return render(request, 'project.html',context)
    elif request.method == 'POST':
        return render(request, 'project.html')
    

# @login_required
def addProject(request):
    if request.method == 'GET':
        workflow_items= WorkflowType.objects.all()
        status_items= Status.objects.all()
        context ={
            'workflows':workflow_items,
            'status':status_items,
        }
        return render(request, 'createproject.html',context)
    elif request.method == 'POST':
        proj_name = request.POST.get('proj_name')
        proj_isbn = request.POST.get('proj_isbn')
        proj_workflowType = request.POST.get('proj_workflowType')
        proj_status = request.POST.get('proj_status')
        workflow_id= WorkflowType.objects.get(id=proj_workflowType)
        status_id= Status.objects.get(id=proj_status)
        proj_no_of_chapters= request.POST.get('proj_no_of_chapters')
        due_date = request.POST.get('due_date')
        proj_manager = request.POST.get('selected_value')
        user_proj_manager =CustomUser.objects.get(id=proj_manager)
        try:

            project = Projects.objects.create(
            proj_name=proj_name,
            proj_isbn=proj_isbn,
            proj_workflowType=workflow_id,
            proj_status=status_id,
            proj_no_of_chapters=proj_no_of_chapters,
            due_date=due_date,
            proj_manager=user_proj_manager

            )
        except Exception as e:
            raise e
        return redirect('project_view')
    

def editProject(request,id):
    if request.method == 'GET':
        workflow_items= WorkflowType.objects.all()
        status_items= Status.objects.all()
        project = Projects.objects.get(id=id)
        context ={
            'workflows':workflow_items,
            'status':status_items,
            'item':project
        }
        return render(request, 'createproject.html',context)
    elif request.method == 'POST':
        proj_name = request.POST.get('proj_name')
        proj_isbn = request.POST.get('proj_isbn')
        proj_workflowType = request.POST.get('proj_workflowType')
        proj_status = request.POST.get('proj_status')
        proj_manager = request.POST.get('selected_value')
        user_proj_manager =CustomUser.objects.get(id=proj_manager)
        workflow_id= WorkflowType.objects.get(id=proj_workflowType)
        status_id= Status.objects.get(id=proj_status)
        proj_no_of_chapters= request.POST.get('proj_no_of_chapters')
        due_date = request.POST.get('due_date')
        try:
            

            Projects.objects.filter(id=id).update(
            proj_name=proj_name,
            proj_isbn=proj_isbn,
            proj_workflowType=workflow_id,
            proj_status=status_id,
            proj_no_of_chapters=proj_no_of_chapters,
            due_date=due_date,
            proj_manager=user_proj_manager
            )
        except Exception as e:
            raise e
        return redirect('project_view')

def delete_project(request, id):
    project = Projects.objects.get(id=id)
    project.delete()
    return redirect('project_view')

def autocomplete(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest': 
        role = RoleMaster.objects.get(id=request.user.role.id)
        query = request.GET.get('term', '')
        queryset = CustomUser.objects.filter(username__icontains=query,role=role)
        print(queryset)
        suggestions = [{'id': obj.pk, 'label': str(obj)} for obj in queryset]
        return JsonResponse(suggestions, safe=False)
    
def autocomplete_userid(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest': 
        # role = RoleMaster.objects.get(id=request.user.role.id)
        query = request.GET.get('term', '')
        queryset = CustomUser.objects.filter(username__icontains=query)
        print(queryset)
        suggestions = [{'id': obj.pk, 'label': str(obj)} for obj in queryset]
        return JsonResponse(suggestions, safe=False)

def start_break(request):
    if request.method == 'GET':
        user = CustomUser.objects.get(id= request.user.id)
        try:
            break_start = Break.objects.filter(user=user, end_time=None).latest('start_time')
        except Break.DoesNotExist:
            Break.objects.create(user=user, start_time=timezone.now())
            return redirect('dashboard_view')

        
        if break_start is not None:
            break_start.end_time=timezone.now()
            break_start.duration=(timezone.now() - break_start.start_time)
            break_start.save()

        return redirect('dashboard_view')
    
def dashboard_view(request):
    if request.method == 'GET':
        user = CustomUser.objects.get(id= request.user.id)
        try:
            break_obj = Break.objects.filter(user= user,end_time=None,).latest('created_at')
            
        except Break.DoesNotExist:
            print("break does not exost 1")
            context ={'clssname':"btn btn-success",'break_txt':"Start Break"}
            request.session["break_data"]=context
            return render(request,'dashboard.html',context)
        context ={'clssname':"btn btn-danger",'break_txt':"End Break"}
        request.session["break_data"]=context
        return render(request,'dashboard.html',context)



def report_view(request):
    if request.method == 'GET':
        return render(request,'report.html')
    
def user_progress_view(request):
    try:

        user= CustomUser.objects.get(id=request.user.id)
        inout_queryset = UserAttendance.objects.filter(user=user,logout_time__isnull=False).annotate(
        date=TruncDate('login_time')
            ).annotate(
                duration1=ExpressionWrapper(F('logout_time') - F('login_time'), output_field=DurationField())
            ).values('date').annotate(
                inout_duration=Sum('duration1')
            ).order_by('date')
        
        break_queryset = Break.objects.filter(user=user,end_time__isnull=False).annotate(
        date=TruncDate('start_time')
            ).annotate(
                duration1=ExpressionWrapper(F('end_time') - F('start_time'), output_field=DurationField())
            ).values('date').annotate(
                break_duration=Sum('duration1')
            ).order_by('date')

    
        result = calculate_total_durations(break_queryset,inout_queryset)
        context = {'breaks':break_queryset,
               'userinout':inout_queryset,"result":result}
    except Exception as e:
        print(e)
    # print(result,"dsdkajsdkljasdlk")
    
    
    return render(request, 'user_report.html',context)

import datetime
def calculate_total_durations(list1, list2):
    total_durations = {}

    for entry in list1:
        date = entry['date']
        break_duration = entry.get('break_duration', datetime.timedelta())
        if date in total_durations:
            total_durations[date]['break_duration'] += break_duration
        else:
            total_durations[date] = {'date': date, 'inout_duration': datetime.timedelta(), 'break_duration': break_duration}

    for entry in list2:
        date = entry['date']
        inout_duration = entry.get('inout_duration', datetime.timedelta())
        if date in total_durations:
            total_durations[date]['inout_duration'] += inout_duration
        else:
            total_durations[date] = {'date': date, 'inout_duration': inout_duration, 'break_duration': datetime.timedelta()}
    for date, data in total_durations.items():
        data['difference'] = data['inout_duration'] - data['break_duration']
    return list(total_durations.values())



def handler404(request, *args, **argv):
    response = render('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response