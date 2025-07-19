from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import (
    AdminAccount, Member, AcademicBackground, FamilyDetail, 
    PublicMissionPost, WorkExperience, TrainingCourse, 
    Qualification, AwardsRecognition, DisciplinaryAction, SpecialNote
)


class AdminAccountAdmin(admin.ModelAdmin):
    list_display = ['account_id', 'email', 'name', 'permission', 'get_img_preview']
    list_filter = ['permission']
    search_fields = ['account_id', 'email', 'name']
    readonly_fields = ['password', 'get_img_preview']
    fieldsets = (
        ('Account Information', {
            'fields': ('account_id', 'email', 'name', 'permission')
        }),
        ('Profile', {
            'fields': ('img_path', 'get_img_preview')
        }),
        ('Security', {
            'fields': ('password',),
            'description': 'Password is automatically hashed. Use the change password form to update.'
        })
    )
    
    def get_img_preview(self, obj):
        if obj.img_path:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 25px;" />', obj.img_path.url)
        return "No Image"
    get_img_preview.short_description = 'Profile Image'
    
    def save_model(self, request, obj, form, change):
        if not change:  # Creating new admin
            if 'password' in form.cleaned_data and form.cleaned_data['password']:
                obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)


class MemberAdmin(admin.ModelAdmin):
    list_display = [
        'member_id', 'full_name', 'email', 'department', 
        'organization', 'region', 'get_profile_preview', 
        'is_deleted', 'get_actions'
    ]
    list_filter = ['is_deleted', 'gender', 'region', 'department', 'organization']
    search_fields = ['member_id', 'full_name', 'email', 'phone_no']
    readonly_fields = ['get_profile_preview']
    actions = ['soft_delete_members', 'restore_members']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('member_id', 'full_name', 'profile_photo_url', 'get_profile_preview')
        }),
        ('Personal Details', {
            'fields': ('birthday', 'gender', 'nationality')
        }),
        ('Location', {
            'fields': ('region', 'nation', 'address')
        }),
        ('Organization Details', {
            'fields': ('department', 'organization', 'current_post', 'position', 'blessing', 'date_of_joining')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone_no')
        }),
        ('Status', {
            'fields': ('is_deleted',)
        })
    )
    
    def get_profile_preview(self, obj):
        if obj.profile_photo_url:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 25px;" />', obj.profile_photo_url.url)
        return "No Image"
    get_profile_preview.short_description = 'Profile Photo'
    
    def get_actions(self, obj):
        if isinstance(obj, Member):
            if obj.is_deleted:
                return format_html(
                    '<a class="button" href="/admin/directory/member/restore_member/{}/" '
                    'style="background-color: #28a745; color: white; padding: 5px 10px; '
                    'text-decoration: none; border-radius: 3px;">Restore</a>',
                    obj.member_id
                )
            else:
                return format_html(
                    '<a class="button" href="/admin/directory/member/soft_delete_member/{}/" '
                    'style="background-color: #dc3545; color: white; padding: 5px 10px; '
                    'text-decoration: none; border-radius: 3px;">Soft Delete</a>',
                    obj.member_id
                )
        return ""
    get_actions.short_description = 'Actions'
    
    def soft_delete_members(self, request, queryset):
        updated = queryset.update(is_deleted=True)
        self.message_user(request, f'{updated} members were soft deleted.')
    soft_delete_members.short_description = "Soft delete selected members"
    
    def restore_members(self, request, queryset):
        updated = queryset.update(is_deleted=False)
        self.message_user(request, f'{updated} members were restored.')
    restore_members.short_description = "Restore selected members"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('soft_delete_member/<str:member_id>/', self.soft_delete_member, name='soft_delete_member'),
            path('restore_member/<str:member_id>/', self.restore_member, name='restore_member'),
        ]
        return custom_urls + urls
    
    def soft_delete_member(self, request, member_id):
        try:
            member = Member.objects.get(member_id=member_id)
            member.is_deleted = True
            member.save()
            messages.success(request, f'Member {member.full_name} has been soft deleted.')
        except Member.DoesNotExist:
            messages.error(request, 'Member not found.')
        return HttpResponseRedirect('/admin/directory/member/')
    
    def restore_member(self, request, member_id):
        try:
            member = Member.objects.get(member_id=member_id)
            member.is_deleted = False
            member.save()
            messages.success(request, f'Member {member.full_name} has been restored.')
        except Member.DoesNotExist:
            messages.error(request, 'Member not found.')
        return HttpResponseRedirect('/admin/directory/member/')


class AcademicBackgroundAdmin(admin.ModelAdmin):
    list_display = ['academic_record_id', 'get_member_name', 'school', 'degree', 'period', 'graduation']
    list_filter = ['graduation', 'degree']
    search_fields = ['academic_record_id', 'member_id1__full_name', 'school', 'degree']
    autocomplete_fields = ['member_id1']
    
    def get_member_name(self, obj):
        return obj.member_id1.full_name
    get_member_name.short_description = 'Member Name'
    get_member_name.admin_order_field = 'member_id1__full_name'


class FamilyDetailAdmin(admin.ModelAdmin):
    list_display = ['family_member_id', 'get_member_name', 'name', 'relation', 'birthday', 'blessing']
    list_filter = ['relation', 'blessing']
    search_fields = ['family_member_id', 'member_id__full_name', 'name', 'relation']
    autocomplete_fields = ['member_id']
    
    def get_member_name(self, obj):
        return obj.member_id.full_name
    get_member_name.short_description = 'Member Name'
    get_member_name.admin_order_field = 'member_id__full_name'


class PublicMissionPostAdmin(admin.ModelAdmin):
    list_display = ['mission_id', 'get_member_name', 'organization', 'final_position', 'department', 'period']
    list_filter = ['organization', 'final_position', 'department']
    search_fields = ['mission_id', 'member__full_name', 'organization', 'final_position']
    autocomplete_fields = ['member']
    
    def get_member_name(self, obj):
        return obj.member.full_name
    get_member_name.short_description = 'Member Name'
    get_member_name.admin_order_field = 'member__full_name'


class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ['experience_id', 'get_member_name', 'organization_name', 'final_position', 'department', 'period']
    list_filter = ['organization_name', 'final_position', 'department']
    search_fields = ['experience_id', 'member__full_name', 'organization_name', 'final_position']
    autocomplete_fields = ['member']
    
    def get_member_name(self, obj):
        return obj.member.full_name
    get_member_name.short_description = 'Member Name'
    get_member_name.admin_order_field = 'member__full_name'


class TrainingCourseAdmin(admin.ModelAdmin):
    list_display = ['training_id', 'get_member_name', 'name_of_course', 'type', 'organization', 'status', 'period']
    list_filter = ['type', 'status', 'organization']
    search_fields = ['training_id', 'member__full_name', 'name_of_course', 'organization']
    autocomplete_fields = ['member']
    
    def get_member_name(self, obj):
        return obj.member.full_name
    get_member_name.short_description = 'Member Name'
    get_member_name.admin_order_field = 'member__full_name'


class QualificationAdmin(admin.ModelAdmin):
    list_display = ['qualification_id', 'get_member_name', 'name_qualification', 'date_acquisition', 'get_remarks_preview']
    list_filter = ['date_acquisition']
    search_fields = ['qualification_id', 'member__full_name', 'name_qualification']
    autocomplete_fields = ['member']
    
    def get_member_name(self, obj):
        return obj.member.full_name
    get_member_name.short_description = 'Member Name'
    get_member_name.admin_order_field = 'member__full_name'
    
    def get_remarks_preview(self, obj):
        if obj.remarks:
            return obj.remarks[:50] + '...' if len(obj.remarks) > 50 else obj.remarks
        return "No remarks"
    get_remarks_preview.short_description = 'Remarks Preview'


class AwardsRecognitionAdmin(admin.ModelAdmin):
    list_display = ['award_id', 'get_member_name', 'type', 'organization', 'date', 'get_description_preview']
    list_filter = ['type', 'organization', 'date']
    search_fields = ['award_id', 'member__full_name', 'type', 'organization']
    autocomplete_fields = ['member']
    
    def get_member_name(self, obj):
        return obj.member.full_name
    get_member_name.short_description = 'Member Name'
    get_member_name.admin_order_field = 'member__full_name'
    
    def get_description_preview(self, obj):
        if obj.description:
            return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
        return "No description"
    get_description_preview.short_description = 'Description Preview'


class DisciplinaryActionAdmin(admin.ModelAdmin):
    list_display = ['penalty_id', 'get_member_name', 'date', 'get_reason_preview']
    list_filter = ['date']
    search_fields = ['penalty_id', 'member__full_name', 'reason']
    autocomplete_fields = ['member']
    
    def get_member_name(self, obj):
        return obj.member.full_name
    get_member_name.short_description = 'Member Name'
    get_member_name.admin_order_field = 'member__full_name'
    
    def get_reason_preview(self, obj):
        return obj.reason[:50] + '...' if len(obj.reason) > 50 else obj.reason
    get_reason_preview.short_description = 'Reason Preview'


class SpecialNoteAdmin(admin.ModelAdmin):
    list_display = ['note_id', 'get_member_name', 'date_written', 'get_details_preview']
    list_filter = ['date_written']
    search_fields = ['note_id', 'member__full_name', 'details']
    autocomplete_fields = ['member']
    
    def get_member_name(self, obj):
        return obj.member.full_name
    get_member_name.short_description = 'Member Name'
    get_member_name.admin_order_field = 'member__full_name'
    
    def get_details_preview(self, obj):
        if obj.details:
            return obj.details[:50] + '...' if len(obj.details) > 50 else obj.details
        return "No details"
    get_details_preview.short_description = 'Details Preview'


# Register all models with their respective admin classes
admin.site.register(AdminAccount, AdminAccountAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(AcademicBackground, AcademicBackgroundAdmin)
admin.site.register(FamilyDetail, FamilyDetailAdmin)
admin.site.register(PublicMissionPost, PublicMissionPostAdmin)
admin.site.register(WorkExperience, WorkExperienceAdmin)
admin.site.register(TrainingCourse, TrainingCourseAdmin)
admin.site.register(Qualification, QualificationAdmin)
admin.site.register(AwardsRecognition, AwardsRecognitionAdmin)
admin.site.register(DisciplinaryAction, DisciplinaryActionAdmin)
admin.site.register(SpecialNote, SpecialNoteAdmin)

# Customize admin site header and title
admin.site.site_header = "Member Management System"
admin.site.site_title = "MMS Admin"
admin.site.index_title = "Welcome to Member Management System Administration"