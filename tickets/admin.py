from django.contrib import admin
from django import forms
from .models import Ticket, Department, News


class DepartmentForm(forms.ModelForm):
    """A form for creating new departments. Includes all the required
    fields"""

    allDepartments = Department.objects.all()


    parent_field = forms.ModelChoiceField(label="Родительское подразделение",
                                          queryset=allDepartments, empty_label=None)
    children_list = forms.CharField(label='Подчиненные подразделения:',
                                    help_text="ЗДесь отображаются подразделения, входящие в состав ",
                                    empty_value=None)

    class Meta:
        model = Department
        fields = ('departmentName', 'boss', 'parent_field', 'children_list')

    def save(self, commit=True):
        dep = self.instance
        parent = self.cleaned_data.get('parent_field')
        dep.save_to(parent=parent, )
        department = super(DepartmentForm, self).save(commit= False)
        department.save()
        return department


class DepartmentAdmin(admin.ModelAdmin):
    # The forms to add and change user instances
    form = DepartmentForm
    #save_on_top = True
    actions = ['move_to_department']

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('departmentName', 'boss', 'get_parent')
    list_filter = ('departmentName', )
    fieldsets = (
        (None, {'fields': ('departmentName',)}),
        ('Advanced', {'fields': ( 'boss', )}),
        ('Иерархия', {
            'classes': ('wide',),
            'fields': ( ('parent_field','path'), 'children_list')})
    )

    search_fields = ('departmentName',)
    readonly_fields = ['path',]
    ordering = ('path','departmentName')
    filter_horizontal = ()

    def move_to_department(self, request, queryset):
        print(dir(request))
        for department in queryset:
            print(department)
            #department.move_to(request.get['move_to_parent'])
    move_to_department.short_description = "Перевести подразделения в подчинение к ..."

# Now register the new UserAdmin...

admin.site.register(Ticket)
# admin.site.register(News)
admin.site.register(Department, DepartmentAdmin)

