from django.contrib import admin
from .models import MembershipPlan, Member, Payment, Attendance

admin.site.register(MembershipPlan)
admin.site.register(Member)
admin.site.register(Payment)
admin.site.register(Attendance)
