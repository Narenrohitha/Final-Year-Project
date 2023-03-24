from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from datetime import datetime,date
from dateutil.relativedelta import relativedelta
from django.urls import resolve
from random import *
# Create your views here.
today = date.today()
def signin(request):	
	if request.method=="POST":
		username=request.POST.get('un')
		password=request.POST.get('pwd')
		user=authenticate(username=username,password=password)
		if user is not None:
			login(request,user)
			use=request.user
			u=str(use)
			if u == 'admin':
				return redirect('/adminview')
			l=Employee.objects.get(user=use)
			role=l.role
			if role == 'leader':
				return redirect('/leader_view')
			else:
				return redirect('/employee_view')
			
		else:
			return redirect('/login')
	return render(request,"login.html")
def signout(request):
	logout(request)
	try:
		del request.session['attendance']
		return redirect("/login")
	except:
		return redirect("/login")
def index(request):
	return render(request,'admin_panel/base.html')
@staff_member_required(login_url='/login')
def adminview(request):
	totalemp=Employee.objects.all().count()
	pending=Emprewards.objects.filter(status=0)
	emp=Emprewards.objects.all()
	return render(request,'admin_panel/admin_view.html',{'totalemp':totalemp,'pending':pending,'emp':emp})
@staff_member_required(login_url='/login')
def employee_admin(request):
	emp=Employee.objects.all()
	return render(request,'admin_panel/employee_admin.html',{'emp':emp})
@staff_member_required(login_url='/login')
def employee_add(request):
	dept=Department.objects.all()
	leader=Employee.objects.filter(role='Leader')
	if request.method=='POST':
		name=request.POST.get('empname')
		email=request.POST.get('email')
		password=request.POST.get('pwd')
		conf=request.POST.get('repwd')
		phone=request.POST.get('phone')
		qualification=request.POST.get('qualification')
		address=request.POST.get('address')
		role=request.POST.get('role')
		dept=request.POST.get('dept')
		leader=request.POST.get('leader')
		profile=request.FILES['profile']
		doj=request.POST.get('doj')
		salary=request.POST.get('salary')
		dep=Department.objects.get(dept_name=dept)
		print(dep)
		if(password==conf):
			pwd=make_password(password)
			User.objects.create(username=name,email=email,password=pwd)
			empname=User.objects.get(username=name)
			Employee.objects.create(user=empname,phone=phone,qualification=qualification,address=address
				,role=role,dept=dep,leader=leader,profile=profile,doj=doj,salary=salary)
	return render(request,'admin_panel/employee_add.html',{'dept':dept,'leader':leader})
@staff_member_required(login_url='/login')
def active(request):
	status = request.GET.get('status')
	id = request.GET.get('id')
	emp=Employee.objects.get(id=id)
	try:
		emp.status=status
		emp.save()
		return JsonResponse({"success":True})
	except Exception as e:
		return JsonResponse({"success":False})
	return JsonResonse(data)
@staff_member_required(login_url='/login')
def shift_view(request):
	shift=Shift.objects.all()
	return render(request,'admin_panel/shift_view.html',{'shift':shift})
@staff_member_required(login_url='/login')
def shift_add(request):
	if request.method=='POST':
		shiftname=request.POST.get('sn')
		start=request.POST.get('starttime')
		end=request.POST.get('endtime')
		Shift.objects.create(shiftname=shiftname,starttime=start,endtime=end)
	return render(request,'admin_panel/shift_add.html')
@staff_member_required(login_url='/login')
def shiftdelete(request,id):
	shift=Shift.objects.get(id=id)
	shift.delete()
	return redirect('/shiftview')
@staff_member_required(login_url='/login')
def reward_view(request):
	reward=Rewards.objects.all()
	return render(request,'admin_panel/reward_view.html',{'reward':reward})
@staff_member_required(login_url='/login')
def reward_add(request):
	if request.method=='POST':
		rewardname=request.POST.get('rn')
		rewardtype=request.POST.get('rtype')
		rewardbenifit=request.POST.get('rb')
		points=request.POST.get('points')
		valid=request.POST.get('valid')
		Rewards.objects.create(rewardname=rewardname,rewardtype=rewardtype,rewardbenifit=rewardbenifit,point=points,valid_to=valid)
	return render(request,'admin_panel/reward_add.html')
@staff_member_required(login_url='/login')
def rewarddelete(request,id):
	reward=Rewards.objects.get(id=id)
	reward.delete()
	return redirect('/reward_view')
def employee_view(request):
	u=request.user
	totalawards=Emprewards.objects.filter(employee=u)
	pending=Emprewards.objects.filter(employee=u,status=0).count()
	rejected=Emprewards.objects.filter(employee=u,status=2).count()
	em=Employee.objects.get(user=u)
	profile=em.profile
	print(profile)
	try:
		points=Points.objects.get(employee=u)
		p=points.points
		
	except:
		p = 0
	emp=Emprewards.objects.filter(employee=u).order_by('createdate')
	return render(request,'employee_panel/employee_view.html',{'totalawards':totalawards,'pending':pending,'rejected':rejected,'emp':emp,'points':p,'profile':profile})
def attendance(request):
	us=request.user
	try:
		points=Points.objects.get(employee=us)
		p=points.points
	except:
		p = 0
	em=Employee.objects.get(user=us)
	profile=em.profile
	user=request.user
	u=Attendance.objects.filter(employee=user)
	if request.method=='POST':
		now = datetime.now()
		u=request.user
		sh=Shift.objects.last()
		s=int(1)
		request.session['attendance'] = 'a'
		a=Attendance.objects.create(employee=u,shift=sh,intime=now,outtime=now,status=s)
	status=request.session.get('attendance')
	print(status)
	return render(request,'employee_panel/attendance.html',{'u':u,'profile':profile,'points':p,'status':status})
def timeout(request):
	status = request.GET.get('status')
	out=datetime.now()
	show=1
	id = request.GET.get('id')
	print('id',id,status)
	a = Attendance.objects.get(employee=id)
	print(a)
	try:
		a.status=status
		a.outtime=out
		a.show=show
		a.save()
		del request.session['attendance']
		request.session['attendance'] = 'b'
		print('false',request.session.get('attendance'))
		return JsonResponse({"success":True})
	except Exception as e:
		return JsonResponse({"success":False})
	return JsonResonse(data)
def employee_award_view(request):
	u=request.user
	em=Employee.objects.get(user=u)
	profile=em.profile
	try:
		points=Points.objects.get(employee=u)
		p=points.points
	except:
		p = 0
	if request.method == 'POST':
		emp=request.user
		reason=request.POST.get('reason')
		description=request.POST.get('desc')
		proof=request.FILES['proof']
		Emprewards.objects.create(employee=emp,reason=reason,description=description,proff=proof)
	emp=Emprewards.objects.filter(employee=u).order_by('createdate')
	return render(request,'employee_panel/employee_award_view.html',{'emp':emp,'points':p,'profile':profile})
def emprewarddelete(request,id):
	reward=Emprewards.objects.get(id=id)
	reward.delete()
	pre_url = request.META.get('HTTP_REFERER')
	return redirect(pre_url)
def leader_view(request):
	t=Challenges.objects.filter(enddate__lt=today)[:5]
	u=request.user
	em=Employee.objects.get(user=u)
	profile=em.profile
	totalemp=Employee.objects.all().count()
	pending=Emprewards.objects.filter(status=0)
	emp=Emprewards.objects.all()
	return render(request,'leader_panel/leader_view.html',{'t':t,'profile':profile,'totalemp':totalemp,'pending':pending,'emp':emp})
def approval_view(request):
	u=request.user
	em=Employee.objects.get(user=u)
	profile=em.profile
	u=request.user
	u=str(u)
	emp=Emprewards.objects.filter(status=0)
	return render(request,'leader_panel/approval.html',{'profile':profile,'emp':emp})
def approval_approve(request):
	u=request.user
	status = request.GET.get('status')
	id = request.GET.get('id')
	emp=Emprewards.objects.get(id=id)
	p=Points.objects.filter(employee=emp.employee).count()
	x = randint(100, 1000)
	points=x
	try:
		emp.status=status
		emp.save()
		if p < 1:
			employee=emp.employee
			Points.objects.create(employee=employee,points=points)
		else:
			n=Points.objects.get(employee=emp.employee)
			tp=n.points+x
			point=Points.objects.get(employee=n.employee)
			point.points=tp
			point.save()
		return JsonResponse({"success":True})
	except Exception as e:
		return JsonResponse({"success":False})
	return JsonResonse(data)
def approval_rejected(request):
	status = request.GET.get('status')
	id = request.GET.get('id')
	emp=Emprewards.objects.get(id=id)
	try:
		emp.status=status
		emp.save()
		return JsonResponse({"success":True})
	except Exception as e:
		return JsonResponse({"success":False})
	return JsonResonse(data)
def leader_attendance(request):
	us=request.user
	em=Employee.objects.get(user=us)
	profile=em.profile
	user=request.user
	u=Attendance.objects.filter(employee=user).last()
	if request.method=='POST':
		now = datetime.now()
		u=request.user
		sh=Shift.objects.last()
		s=int(1)
		a=Attendance.objects.create(employee=u,shift=sh,intime=now,outtime=now,status=s)
	return render(request,'leader_panel/leader_attendance.html',{'u':u,'profile':profile})
def wallet_view(request):
	u=request.user
	em=Employee.objects.get(user=u)
	profile=em.profile
	try:
		points=Points.objects.get(employee=u)
		p=points.points
	except:
		p = 0
	m=makeawards.objects.filter(employee=u)
	a=[]
	k=[]
	for i in m:
		a.append(i.awards)
	for n in a:
		k.append(n.rewardname)
	w=Rewards.objects.filter(~Q(rewardname__in=k))
	return render(request,'employee_panel/wallet.html',{'w':w,'points':p,'profile':profile})
def make_award(request,id):
	print('award added')
	f=Rewards.objects.get(id=id)
	u=request.user
	a=f
	makeawards.objects.create(awards=a,employee=u)
	n=Points.objects.get(employee=u)
	tp=n.points-f.point
	point=Points.objects.get(employee=u)
	point.points=tp
	print(tp)
	point.save()
	pre_url = request.META.get('HTTP_REFERER')
	return redirect(pre_url)
def emp_reports(request):
	u=request.user
	em=Employee.objects.get(user=u)
	profile=em.profile
	if request.method=='POST':
		sd=request.POST.get('sd')
		ed=request.POST.get('ed')
		result=Emprewards.objects.filter(createdate__gte=sd,createdate__lte=ed)
		return render(request,'employee_panel/reports.html',{'profile':profile,'result':result})
	return render(request,'employee_panel/reports.html',{'profile':profile})
def admin_reports(request):
	if request.method=='POST':
		sd=request.POST.get('sd')
		ed=request.POST.get('ed')
		result=Emprewards.objects.filter(createdate__gte=sd,createdate__lte=ed)
		return render(request,'admin_panel/reports.html',{'result':result})
	return render(request,'admin_panel/reports.html')
def leader_reports(request):
	u=request.user
	em=Employee.objects.get(user=u)
	profile=em.profile
	if request.method=='POST':
		sd=request.POST.get('sd')
		ed=request.POST.get('ed')
		result=Challenges.objects.filter(startdate__gte=sd,enddate__lte=ed)
		return render(request,'leader_panel/reports.html',{'profile':profile,'result':result})
	return render(request,'leader_panel/reports.html')
def create_shifts(request):
	u=request.user
	em=Employee.objects.get(user=u)
	profile=em.profile
	try:
		points=Points.objects.get(employee=u)
		p=points.points
	except:
		p = 0
	emp=Employee.objects.filter(role='employee')
	shift=Shift.objects.all()
	cs=Createshift.objects.all()
	if request.method=='POST':
		e=request.POST.get('empname')
		s=request.POST.get('shift')
		em=Employee.objects.get(id=e)
		sh=Shift.objects.get(id=s)
		Createshift.objects.create(employee=em,shift=sh)
	return render(request,'leader_panel/create_shifts.html',{'emp':emp,'profile':profile,'cs':cs,'shift':shift})
def createshiftdelete(request,id):
	shift=Createshift.objects.get(id=id)
	shift.delete()
	return redirect('/create_shifts')
def create_tasks(request):
	u=request.user
	em=Employee.objects.get(user=u)
	profile=em.profile
	emp=Employee.objects.filter(role='employee')
	task=Challenges.objects.all()
	if request.method=='POST':
		user=request.user
		e=request.POST.get('empname')
		job=request.POST.get('job')
		em=Employee.objects.get(id=e)
		sd=request.POST.get('starttime')
		ed=request.POST.get('endtime')
		Challenges.objects.create(creator=user,employee=em,job=job,startdate=sd,enddate=ed)
	return render(request,'leader_panel/create_tasks.html',{'emp':emp,'profile':profile,'task':task})
def taskdelete(request,id):
	tsk=Challenges.objects.get(id=id)
	tsk.delete()
	return redirect('/create_tasks')
def user_wallet(request):
	u=request.user
	em=Employee.objects.get(user=u)
	profile=em.profile
	print(profile)
	try:
		points=Points.objects.get(employee=u)
		p=points.points
	except:
		p = 0
	a=makeawards.objects.filter(employee=u)
	print(a)
	return render(request,'employee_panel/user_wallet.html',{'profile':profile,'a':a,'points':p})
def task_view(request):
	u=request.user
	em=Employee.objects.get(user=u)
	profile=em.profile
	print(profile)
	try:
		points=Points.objects.get(employee=u)
		p=points.points
	except:
		p = 0
	task=Challenges.objects.filter(employee=em)
	return render(request,'employee_panel/task_view.html',{'task':task,'profile':profile,'points':p})
def accepted(request):
	status = request.GET.get('status')
	id = request.GET.get('id')
	a=Challenges.objects.get(id=id)
	try:
		a.status=status
		a.save()
		return JsonResponse({"success":True})
	except Exception as e:
		return JsonResponse({"success":False})
	return JsonResonse(data)