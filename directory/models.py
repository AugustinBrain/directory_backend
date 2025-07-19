from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from cloudinary.models import CloudinaryField


class AdminAccount(models.Model):
    SUPERADMIN = 'superadmin'
    ADMIN = 'admin'
    
    PERMISSION_CHOICES = [
        (SUPERADMIN, 'Super Admin'),
        (ADMIN, 'Admin'),
    ]
    
    account_id = models.CharField(primary_key=True, max_length=255)
    email = models.EmailField(max_length=100, null=False, blank=False)
    name = models.CharField(max_length=100, default="Admin")
    password = models.CharField(max_length=255)
    img_path = CloudinaryField('image', null=True, blank=True)
    permission = models.CharField(max_length=50, choices=PERMISSION_CHOICES, default=ADMIN)
    
    class Meta:
        db_table = 'admin_account'
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def is_superadmin(self):
        return self.permission == self.SUPERADMIN
    
    def is_admin(self):
        return self.permission == self.ADMIN
    
    def __str__(self):
        return f"{self.name} ({self.permission})"

class Member(models.Model):
    MALE = 'Male'
    FEMALE = 'Female'

    GENDER = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]   

    member_id = models.CharField(primary_key=True, max_length=255)
    profile_photo_url = CloudinaryField('image', null=True, blank=True)
    full_name = models.CharField(max_length=100, null=False, blank=False)
    region = models.CharField(max_length=100, null=False, blank=False)
    nation = models.CharField(max_length=100, null=False, blank=False)
    nationality = models.CharField(max_length=100, null=False, blank=False)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER)
    department = models.CharField(max_length=100, null=True, blank=True) 
    organization = models.CharField(max_length=255, null=True, blank=True)
    current_post = models.CharField(max_length=100, null=True, blank=True)
    position = models.CharField(max_length=100, null=True, blank=True)
    blessing = models.CharField(max_length=100, null=False, blank=False)
    date_of_joining = models.DateField(null=False, blank=False)
    email = models.EmailField(max_length=100, null=False, blank=False)
    phone_no = models.CharField(max_length=20, null=False, blank=False)
    address = models.TextField(null=False, blank=False) 
    is_deleted = models.BooleanField(default=False)


    def __str__(self):
        return self.full_name
    
    class Meta:
        db_table = 'member'
        verbose_name = "Member"
        verbose_name_plural = "Members"

class AcademicBackground(models.Model):
    academic_record_id = models.CharField(primary_key=True, max_length=255)
    member_id1 = models.ForeignKey(Member, on_delete=models.CASCADE, null=False, blank=False, db_column='member_id')
    period = models.CharField(max_length=100, null=False, blank=False)
    school = models.CharField(max_length=255, null=False, blank=False)
    degree = models.CharField(max_length=255, null=False, blank=False)
    graduation = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return f"{self.degree} from {self.school} ({self.period})"
    
    class Meta:
        db_table = 'academic_background'
        verbose_name = "Academic Background"
        verbose_name_plural = "Academic Backgrounds"
    
class FamilyDetail(models.Model):
    family_member_id = models.CharField(primary_key=True, max_length=255)
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, db_column='member_id')
    relation = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    birthday = models.DateField(null=True, blank=True)
    blessing = models.CharField(max_length=100, null=False, blank=False)

    class Meta:
        db_table = 'family_detail'
        verbose_name = "Family Detail"
        verbose_name_plural = "Family Details"


class PublicMissionPost(models.Model):
    mission_id = models.CharField(primary_key=True, max_length=255)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, db_column='member_id')
    period = models.CharField(max_length=100, null=True, blank=True)
    organization = models.CharField(max_length=255, null=True, blank=True)
    final_position = models.CharField(max_length=100, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'public_mission_post'
        verbose_name = "Public Mission Post"
        verbose_name_plural = "Public Mission Posts"


class WorkExperience(models.Model):
    experience_id = models.CharField(primary_key=True, max_length=255)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, db_column='member_id')
    period = models.CharField(max_length=100, null=True, blank=True)
    organization_name = models.CharField(max_length=255, null=True, blank=True)
    final_position = models.CharField(max_length=100, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    job_description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'work_experience'
        verbose_name = "Work Experience"
        verbose_name_plural = "Work Experiences"


class TrainingCourse(models.Model):
    training_id = models.CharField(primary_key=True, max_length=255)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, db_column='member_id')
    type = models.CharField(max_length=100, null=True, blank=True)
    name_of_course = models.CharField(max_length=255, null=True, blank=True)
    period = models.CharField(max_length=100, null=True, blank=True)
    organization = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'training_course'
        verbose_name = "Training Course"
        verbose_name_plural = "Training Courses"


class Qualification(models.Model):
    qualification_id = models.CharField(primary_key=True, max_length=255)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, db_column='member_id')
    date_acquisition = models.DateField(null=True, blank=True)
    name_qualification = models.CharField(max_length=255, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'qualification'
        verbose_name = "Qualification"
        verbose_name_plural = "Qualifications"


class AwardsRecognition(models.Model):
    award_id = models.CharField(primary_key=True, max_length=255)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, db_column='member_id')
    date = models.DateField(null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    organization = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'awards_recognition'
        verbose_name = "Award/Recognition"
        verbose_name_plural = "Awards & Recognitions"


class DisciplinaryAction(models.Model):
    penalty_id = models.CharField(primary_key=True, max_length=255)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, db_column='member_id')
    date = models.DateField(null=True, blank=True)
    reason = models.TextField(null=False, blank=False)

    class Meta:
        db_table = 'disciplinary_action'
        verbose_name = "Disciplinary Action"
        verbose_name_plural = "Disciplinary Actions"


class SpecialNote(models.Model):
    note_id = models.CharField(primary_key=True, max_length=255)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, db_column='member_id')
    date_written = models.DateField(null=True, blank=True)
    details = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'special_note'
        verbose_name = "Special Note"
        verbose_name_plural = "Special Notes"


