from django.contrib import admin
from .models import MembershipPlan, Member, Payment

admin.site.register(MembershipPlan)
admin.site.register(Member)
admin.site.register(Payment)
