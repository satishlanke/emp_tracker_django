from django.contrib import admin
from .models import  *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Define a custom admin class for CustomUser model
class CustomUserAdmin(BaseUserAdmin):
    list_display = ['id', 'username', 'status']
    list_filter = ['status']
    search_fields = ['id', 'username']
    add_fieldsets = (
            (None, {'fields': ('first_name', 'last_name', 'email', 'password', 'role', 'country_code', 'country','status'
                               'is_active', 'verified')}),
        )
    # Add any other fields or settings specific to your CustomUser model


class WorkflowTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'workflow_name', 'workflow_code']
    # Other admin options and customizations can be added here.

# Register WorkflowType model with the custom admin class
admin.site.register(WorkflowType, WorkflowTypeAdmin)
# Register CustomUser model with the custom admin class
admin.site.register(Status)
admin.site.register(Projects)

admin.site.register(CustomUser)
admin.site.register(Break)

admin.site.register(UserAttendance)
admin.site.register(RoleMaster)
admin.site.register(DesignationMaster)



