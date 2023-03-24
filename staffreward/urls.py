"""staffreward URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rewards.views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',adminview),
    path('logout',signout),
    path('adminview',adminview),
    path('login',signin),
    path('employee_admin',employee_admin),
    path('employee_add',employee_add),
    path('active',active,name='active'),
    path('shiftview',shift_view),
    path('shift_add',shift_add),
    path('shiftdelete/<int:id>/',shiftdelete),
    path('reward_view',reward_view),
    path('reward_add',reward_add),
    path('rewarddelete/<int:id>/',rewarddelete),
    path('attendance',attendance),
    path('timeout',timeout,name='timeout'),
    path('employee_view',employee_view),
    path('employee_award_view',employee_award_view),
    path('emprewarddelete/<int:id>',emprewarddelete),
    path('leader_view',leader_view),
    path('approval_view',approval_view),
    path('rejected',approval_rejected,name='rejected'),
    path('approved',approval_approve,name='approved'),
    path('leader_attendance',leader_attendance),
    path('treasure',wallet_view),
    path('make_award/<int:id>/',make_award),
    path('admin_reports/',admin_reports),
    path('emp_reports/',emp_reports),
    path('leader_reports/',leader_reports),
    path('create_shifts',create_shifts),
    path('createshiftdelete/<int:id>',createshiftdelete),
    path('create_tasks',create_tasks),
    path('taskdelete/<int:id>',taskdelete),
    path('user_wallet',user_wallet),
    path('task_view',task_view),
    path('accepted',accepted,name='accepted'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
