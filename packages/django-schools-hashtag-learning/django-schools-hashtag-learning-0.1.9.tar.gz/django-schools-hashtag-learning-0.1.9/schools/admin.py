from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from schools.models import School, Authority, Faculty, Subscription
from users.models import User


class SchoolResource(resources.ModelResource):

    authority = fields.Field(
        column_name='authority',
        attribute='authority',
        widget=ForeignKeyWidget(Authority, 'authority_name')
    )

    class Meta:
        model = School

class SchoolAdmin(ImportExportModelAdmin):
    resource_class = SchoolResource
    readonly_fields = ('id',)

    def get_list_display(self, request):
        return('school_name', 'authority', 'account_expiry')

class FacultyAdmin(ImportExportModelAdmin):
    pass


class AuthorityAdmin(ImportExportModelAdmin):
    pass

class SubscriptionResource(resources.ModelResource):

    school = fields.Field(
        column_name='school_name',
        attribute='school',
        widget=ForeignKeyWidget(School, 'school_name')
    )

    user = fields.Field(
        column_name='user',
        attribute='user',
        widget=ForeignKeyWidget(User, 'username')
    )

    class Meta:
        model = Subscription

class SubscriptionAdmin(ImportExportModelAdmin):
    resource_class = SubscriptionResource

    def get_list_display(self, request):
        return '__str__', 'school', 'school_subscription', 'individual_subscription', 'is_paid', 'expiry'

    list_filter = ['school_subscription', 'individual_subscription', 'school', 'is_paid']

    search_fields = ['school__school_name', 'user__username']



admin.site.register(School, SchoolAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Authority, AuthorityAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
