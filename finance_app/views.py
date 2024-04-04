from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView,CreateView,UpdateView,DetailView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from account_app.views import *
from django.utils.decorators import method_decorator





################## Finance team section
from django.utils import timezone

from .models import Employee

@finance_login_required
def finance_dashboard(request):
    current_date = timezone.now().date()
    # Define a threshold, e.g., 7 days before the end date
    threshold_date = current_date + timedelta(days=7)
    # Filter employees whose end_date_of_work_order is within the threshold
    employees = Employee.objects.filter(end_date_of_work_order__gte=current_date, end_date_of_work_order__lte=threshold_date)[:4]

    return render(request,'finance/finance_dashboard.html',context={'employees':employees})



from django.urls import reverse
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from celery_once import QueueOnce



############# email sending to user before 15 days of end work date
@shared_task
def send_notification(employee_id,finance_user_email):  # Default delay is 180 seconds (3 minutes)
    try:    
        employee = Employee.objects.get(pk=employee_id)
        subject = f'Remainder: Contract Expiry Notification for {employee.name}'
        context = {'employee': employee}
        html_message = render_to_string('finance/expiry_mail.html',context)
        text_message = strip_tags(html_message)

        from_email = settings.EMAIL_HOST_USER
        recipient_list =  [finance_user_email]
        email_message = EmailMultiAlternatives(subject, text_message, from_email, recipient_list)
        email_message.attach_alternative(html_message, "text/html")
        email_message.send()

        return f'Notification email sent for employee {employee.name}'

    except Employee.DoesNotExist:
        return f'Employee with id {employee_id} does not exist'
    except CustomUser.DoesNotExist:
        return 'Finance user does not exist'
    except Exception as e:
        return f'An error occurred: {str(e)}'
        


from django.core.exceptions import ValidationError

@finance_login_required
def add_employee(request):
     
     if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        mobile=request.POST.get('mobile')
        alternate=request.POST.get('alternate')
        position=request.POST.get('position')
        clientName=request.POST.get('clientName')
        clientLocation=request.POST.get('clientLocation')
        projectDirector=request.POST.get('projectDirector')
        projectPartner=request.POST.get('projectPartner')
        fees=request.POST.get('fees')
        active_inactive = request.POST.get('active_inactive')
        employeeStatus=request.POST.get('employeeStatus')
        woDetail=request.POST.get('woDetail')
        uploadWorkOrder=request.FILES.get('uploadWorkOrder')
        uploadNDA=request.FILES.get('uploadNDA')
        uploadResume=request.FILES.get('uploadResume')

        joiningDate_str = request.POST.get('joiningDate')
        lastWorkingDate_str = request.POST.get('lastWorkingDate')
        workOrderStartDate_str = request.POST.get('workOrderStartDate')
        workOrderEndDate_str = request.POST.get('workOrderEndDate')

        # Convert joiningDate to a date object if it's not None
        if joiningDate_str:
            try:
                joiningDate = datetime.datetime.strptime(joiningDate_str, '%Y-%m-%d').date()
            except ValueError:
                raise ValidationError('Invalid joining date format. Date must be in YYYY-MM-DD format.')
        else:
            joiningDate = None

        if lastWorkingDate_str:
            try:
                lastWorkingDate = datetime.datetime.strptime(lastWorkingDate_str, '%Y-%m-%d').date()
            except ValueError:
                raise ValidationError('Invalid last working date format. Date must be in YYYY-MM-DD format.')
        else:
            lastWorkingDate = None

        # Convert workOrderStartDate to a date object if it's not None
        if workOrderStartDate_str:
            try:
                workOrderStartDate = datetime.datetime.strptime(workOrderStartDate_str, '%Y-%m-%d').date()
            except ValueError:
                raise ValidationError('Invalid work order start date format. Date must be in YYYY-MM-DD format.')
        else:
            workOrderStartDate = None

        # Convert workOrderEndDate to a date object if it's not None
        if workOrderEndDate_str:
            try:
                workOrderEndDate = datetime.datetime.strptime(workOrderEndDate_str, '%Y-%m-%d').date()
            except ValueError:
                raise ValidationError('Invalid work order end date format. Date must be in YYYY-MM-DD format.')
        else:
            workOrderEndDate = None


        if Employee.objects.filter(email=email).exists():
                return HttpResponse({'Employee with current Email address already exists'})

        employee = Employee(user=request.user,
                            name=name,
                            email=email,
                            mobile=mobile,
                            alt_mobile=alternate,
                            position=position,
                            client_name=clientName,
                            client_location=clientLocation,
                            project_director=projectDirector,
                            project_partner=projectPartner,
                            fees=fees,
                            active_inactive = active_inactive,
                            employee_status=employeeStatus,
                            joining_date=joiningDate,
                            last_working_date=lastWorkingDate,
                            start_date_of_work_order=workOrderStartDate,
                            end_date_of_work_order=workOrderEndDate,
                            work_order_detail=woDetail,
                            upload_work_order=uploadWorkOrder,
                            upload_nda=uploadNDA,
                            upload_resume=uploadResume
                            )
        
        employee.save()

        if workOrderEndDate:

        
            workOrderEndDate_aware = timezone.make_aware(timezone.datetime.combine(workOrderEndDate, datetime.time()))
                
        
            finance_user = request.user.email

            # Calculate the notification date (15 days before end_date_of_work_order)
            notification_date = workOrderEndDate_aware - timedelta(days=15)
            
            send_notification.apply_async(args=[employee.pk, finance_user], eta=notification_date)
        else:
            # Handle the case where workOrderEndDate is None (no calculation or notification needed)
            pass
        
        return redirect('finance_dashboard')
              
     return render(request,'finance/add_employee.html')



from django.db import IntegrityError

class Updateemployee(LoginRequiredMixin,UpdateView):
    model = Employee
    success_url = reverse_lazy('all_employee')
    template_name = 'finance/update_employee.html'
    login_url = 'login_default'

    @method_decorator(finance_login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        employee = get_object_or_404(Employee, pk=pk, user=request.user)
        return render(request, self.template_name, {'employee': employee})   

    def post(self, request, pk):
        if pk is None:
            # Creating a new candidate
            employee = Employee(user=request.user)
        else:
            # Updating an existing candidate
            employee = get_object_or_404(Employee, pk=pk, user=request.user)
        
        employee.name = request.POST.get("name")
        employee.email = request.POST.get("email")
        employee.mobile = request.POST.get("mobile")
        employee.alt_mobile = request.POST.get("alternate")
        employee.position = request.POST.get("position")
        employee.client_name = request.POST.get("clientName")
        employee.client_location = request.POST.get("clientLocation")
        employee.project_director = request.POST.get("projectDirector")
        employee.project_partner = request.POST.get("projectPartner")
        employee.fees = request.POST.get("fees")
        employee.active_inactive = request.POST.get("active_inactive")
        employee.employee_status = request.POST.get("employeeStatus")
        employee.work_order_detail = request.POST.get("woDetail")

        employee.save()
        
        def parse_date(date_str):
                if date_str:
                    try:
                        return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
                    except ValueError:
                        raise ValidationError('Invalid date format. Date must be in YYYY-MM-DD format.')
                return None
        
        employee.joining_date = parse_date(request.POST.get("joiningDate"))
        employee.last_working_date = parse_date(request.POST.get("lastWorkingDate"))
        employee.start_date_of_work_order = parse_date(request.POST.get("workOrderStartDate"))
        employee.end_date_of_work_order = parse_date(request.POST.get("workOrderEndDate"))

        employee_pk = employee.pk

        if Employee.objects.exclude(pk=employee_pk).filter(email=employee.email).exists():
            return HttpResponse({'Employee with current Email address already exists'})
        
        

        employees = Employee.objects.get(pk=employee_pk)
        current_employee_enddate = employees.end_date_of_work_order

        if current_employee_enddate == employee.end_date_of_work_order:
            pass

        elif employee.end_date_of_work_order == None:
            pass

        else :
            workOrderEndDate_aware = timezone.make_aware(timezone.datetime.combine(employee.end_date_of_work_order, datetime.time()))
            
            finance_user_email = request.user.email
            
            # Calculate the notification date (15 days before end_date_of_work_order)
            notification_date = workOrderEndDate_aware - timedelta(days=15)
            
            # Call the task with the calculated countdown
            send_notification.apply_async(args=[employee.pk, finance_user_email], eta=notification_date)
        # else:
        #     # Handle the case where workOrderEndDate is None (no calculation or notification needed)
        #     pass
        
        try:

            upload_work_order = request.FILES.get('uploadWorkorder')
            keep_workorder = request.POST.get('keep')
            if not keep_workorder and upload_work_order:
                employee.upload_work_order = upload_work_order

            upload_nda = request.FILES.get('uploadNDA')
            keep_nda = request.POST.get('keep')
            if not keep_nda and upload_nda:
                employee.upload_nda = upload_nda

            new_resume = request.FILES.get('uploadResume')
            keep_resume = request.POST.get('keep_resume')
            if not keep_resume and new_resume:
                employee.upload_resume = new_resume

            employee.save()
            # send_notification.apply_async(args=[employee.id], countdown=180)
            return redirect(self.success_url)

        except IntegrityError as e:
            if 'email' in str(e):
                error_message = 'An employee with this email already exists.'
            else:
                error_message = 'An error occurred while saving the employee.'
            return render(request, self.template_name, {'employee': employee, 'error_message': error_message})



@finance_login_required
def all_employee(request):
    employees = Employee.objects.all().order_by('-created')
    return render(request,'finance/all_employee.html',context={'employees':employees})



@finance_login_required
def detail_employee(request,pk):
    employees = Employee.objects.get(id=pk)
    return render(request,'finance/detail_employee.html',context={'detail':employees})


@finance_login_required
def delete_employee(request,pk):
    if request.method == 'POST':
        employees = Employee.objects.get(id=pk)
        employees.delete()
        return redirect('all_employee')
    return render(request,'finance/delete_employee.html')


######## active and inactive employees
@finance_login_required
def active_inactive(request,action):
    if action == 'active':
        heading = 'On Contract'
        employee_active = Employee.objects.filter(active_inactive='Active').order_by('-joining_date')
        # return render(request,'finance/active_inactive.html',context={'employee_active':employee_active})
    if action == 'inactive':
        heading = 'Contract Expired'
        employee_active = Employee.objects.filter(active_inactive='InActive').order_by('-joining_date')
    return render(request,'finance/active_inactive.html',context={'employee_active':employee_active,'heading':heading})




from django.db.models import F
from datetime import date,timedelta
########### display 5 employee have contract end date is approaching
@finance_login_required
def end_work_order(request):
    today = date.today()
    employees = Employee.objects.annotate(
        days_until_end=F('end_date_of_work_order') - today
    ).order_by('days_until_end')[:5]

    employee_names = [employee.name for employee in employees]
    return JsonResponse({'employee_names': employee_names})





################# export to excel
import os
from openpyxl import Workbook
from django.urls import reverse
import urllib.parse
from django.conf import settings
from openpyxl.worksheet.hyperlink import Hyperlink
from django.http import HttpResponse
from urllib.parse import urljoin


def export_selected_to_excel(request):

    wb = Workbook()
    ws = wb.active
    ws.title = "Candidates"

    headers = ["Name", "Email", "Phone", "Alt Phone", "Position", "Client Name", "Client Location", "Project Director", "Project Partner", "Fees", "Work Type", "Work Order Detail","Resume URL","Work Order","NDA","Active Status","Joining Date","Last Working Date ","Start Date of Work Order","End Date Work Order"]
    ws.append(headers)

    candidate_ids = request.GET.get('ids', '').split(',')
    candidates = Employee.objects.filter(pk__in=candidate_ids)

    for row_num, candidate in enumerate(candidates, start=2):

        MEDIA_URL = 'http://122.165.80.8:8080/media/'

        local_path_resume = f'/home/renjith/datapmi_recruitment/media/employeeresume/{candidate.upload_resume}'
        local_path_work_order = f'/home/renjith/datapmi_recruitment/media/work_order/{candidate.upload_work_order}'
        nda = f'/home/renjith/datapmi_recruitment/media/nda/{candidate.upload_nda}'

        relative_path = local_path_resume.replace('/home/renjith/datapmi_recruitment/media/employeeresume/', '')
        relative_path_work_order = local_path_work_order.replace('/home/renjith/datapmi_recruitment/media/work_order/', '')
        relative_path_nda = nda.replace('/home/renjith/datapmi_recruitment/media/nda/', '')

        resume_url = urljoin(MEDIA_URL, relative_path) if candidate.upload_resume else ''
        work_order_url = urljoin(MEDIA_URL, relative_path_work_order) if candidate.upload_work_order else ''
        nda_url = urljoin(MEDIA_URL, relative_path_nda) if candidate.upload_nda else ''

        row = [
            candidate.name,
            candidate.email,
            candidate.mobile,
            candidate.alt_mobile,
            candidate.position,
            candidate.client_name,
            candidate.client_location,
            candidate.project_director,
            candidate.project_partner,
            candidate.fees,
            candidate.employee_status,
            candidate.work_order_detail,
            resume_url,
            work_order_url,
            nda_url,
            candidate.active_inactive,
            candidate.joining_date,
            candidate.last_working_date,
            candidate.start_date_of_work_order,
            candidate.end_date_of_work_order,
        ]
        
        ws.append(row)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Employees.xlsx"'
    wb.save(response)
    return response




