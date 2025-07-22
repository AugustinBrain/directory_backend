from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import AdminAccount, Member, AcademicBackground, FamilyDetail, PublicMissionPost, WorkExperience, TrainingCourse, Qualification, AwardsRecognition, DisciplinaryAction, SpecialNote
from .serializers import AdminAccountSerializer, LoginSerializer, CreateAdminAccountSerializer, MemberSerializer, AcademicBackgroundSerializer, FamilyDetailSerializer, PublicMissionPostSerializer, WorkExperienceSerializer, TrainingCourseSerializer,  QualificationSerializer, AwardsRecognitionSerializer, DisciplinaryActionSerializer, SpecialNoteSerializer
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from .authentication import JWTAuthentication
from .permissions import IsSuperAdminOrReadOnly, IsAdminOrSuperAdmin, CanManageAdmins

# Authentication Views
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([CanManageAdmins])
def getAccounts(request):
    admins = AdminAccount.objects.all()
    serializer = AdminAccountSerializer(admins, many=True)
    return Response(serializer.data)

@api_view(['POST'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([CanManageAdmins])
def createAccount(request):
    serializer = CreateAdminAccountSerializer(data=request.data)
    if serializer.is_valid():
        admin = serializer.save()
        return Response(AdminAccountSerializer(admin).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        try:
            admin = AdminAccount.objects.get(email=email)
            if admin.check_password(password):
                # Generate JWT token
                payload = {
                    'account_id': admin.account_id,
                    'email': admin.email,
                    'permission': admin.permission,
                    'exp': datetime.utcnow() + timedelta(hours=24)
                }
                token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
                
                return Response({
                    'token': token,
                    'user': AdminAccountSerializer(admin).data
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except AdminAccount.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminOrSuperAdmin])
def logout(request):
    # In a real app, you might want to blacklist the token
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminOrSuperAdmin])
def profile(request):
    serializer = AdminAccountSerializer(request.user)
    return Response(serializer.data)

# Dashboard View

@api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAdminOrSuperAdmin])
def getDashboard(request):
    return Response('Hello, this is the dashboard!')

# Member Views
@api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAdminOrSuperAdmin])
def getMembers(request):
    members = Member.objects.filter(is_deleted=False)
    serializer = MemberSerializer(members, many=True)
    return Response(serializer.data)

@api_view(['POST'])  
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsSuperAdminOrReadOnly])
def createMember(request):
    serializer = MemberSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAdminOrSuperAdmin])
def getMember(request, member_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    serializer = MemberSerializer(member)
    return Response(serializer.data)

@api_view(['PUT'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsSuperAdminOrReadOnly])
def updateMember(request, member_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    serializer = MemberSerializer(member, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsSuperAdminOrReadOnly])
def deleteMember(request, member_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    # Soft delete
    member.is_deleted = True
    member.save()
    return Response({'message': 'Member deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# Academic Background Views
@api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAdminOrSuperAdmin])
def getAcademicBackgrounds(request, member_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    academic_backgrounds = AcademicBackground.objects.filter(member=member)
    serializer = AcademicBackgroundSerializer(academic_backgrounds, many=True)
    return Response(serializer.data)

@api_view(['POST'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsSuperAdminOrReadOnly])
def createAcademicBackground(request, member_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    serializer = AcademicBackgroundSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(member=member)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAdminOrSuperAdmin])
def getAcademicBackground(request,member_id, academic_record_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    serializer = MemberSerializer(member)
    academic_background = get_object_or_404(AcademicBackground, academic_record_id=academic_record_id, member_id=member)
    serializer = AcademicBackgroundSerializer(academic_background)
    return Response(serializer.data)

@api_view(['PUT'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsSuperAdminOrReadOnly])
def updateAcademicBackground(request, member_id, academic_record_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    academic_background = get_object_or_404(AcademicBackground, academic_record_id=academic_record_id)
    serializer = AcademicBackgroundSerializer(academic_background, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsSuperAdminOrReadOnly])
def deleteAcademicBackground(request, member_id, academic_record_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    academic_background = get_object_or_404(AcademicBackground, academic_record_id=academic_record_id)
    academic_background.delete()
    return Response({'message': 'Academic background deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# Family Detail Views
@api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAdminOrSuperAdmin])
def getFamilyDetails(request, member_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    family_details = FamilyDetail.objects.filter(member=member)
    serializer = FamilyDetailSerializer(family_details, many=True)
    return Response(serializer.data)

@api_view(['POST'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsSuperAdminOrReadOnly])
def createFamilyDetail(request, member_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    serializer = FamilyDetailSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(member=member)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAdminOrSuperAdmin])
def getFamilyDetail(request, member_id, family_member_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    family_detail = get_object_or_404(FamilyDetail, family_member_id=family_member_id, member=member)
    serializer = FamilyDetailSerializer(family_detail)
    return Response(serializer.data)

@api_view(['PUT'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsSuperAdminOrReadOnly])
def updateFamilyDetail(request, member_id, family_member_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    family_detail = get_object_or_404(FamilyDetail, family_member_id=family_member_id, member=member)
    serializer = FamilyDetailSerializer(family_detail, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsSuperAdminOrReadOnly])
def deleteFamilyDetail(request, member_id, family_member_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    family_detail = get_object_or_404(FamilyDetail, family_member_id=family_member_id, member=member)
    family_detail.delete()
    return Response({'message': 'Family detail deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# Public Mission Post Views
@api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAdminOrSuperAdmin])
def getPublicMissionPosts(request, member_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    public_mission_posts = PublicMissionPost.objects.filter(member=member)
    serializer = PublicMissionPostSerializer(public_mission_posts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsSuperAdminOrReadOnly])
def createPublicMissionPost(request, member_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    serializer = PublicMissionPostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(member=member)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAdminOrSuperAdmin])
def getPublicMissionPost(request, member_id, mission_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    public_mission_post = get_object_or_404(PublicMissionPost, mission_id=mission_id, member=member)
    serializer = PublicMissionPostSerializer(public_mission_post)
    return Response(serializer.data)

@api_view(['PUT'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsSuperAdminOrReadOnly])
def updatePublicMissionPost(request, member_id, mission_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    public_mission_post = get_object_or_404(PublicMissionPost, mission_id=mission_id, member=member)
    serializer = PublicMissionPostSerializer(public_mission_post, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsSuperAdminOrReadOnly])
def deletePublicMissionPost(request, member_id, mission_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    public_mission_post = get_object_or_404(PublicMissionPost, mission_id=mission_id, member=member)
    public_mission_post.delete()
    return Response({'message': 'Public mission post deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# Work Experience Views
@api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAdminOrSuperAdmin])
def getWorkExperiences(request, member_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    work_experiences = WorkExperience.objects.filter(member=member)
    serializer = WorkExperienceSerializer(work_experiences, many=True)
    return Response(serializer.data)

@api_view(['POST'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsSuperAdminOrReadOnly])
def createWorkExperience(request, member_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    serializer = WorkExperienceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(member=member)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAdminOrSuperAdmin])
def getWorkExperience(request, member_id, experience_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    work_experience = get_object_or_404(WorkExperience, experience_id=experience_id, member=member)
    serializer = WorkExperienceSerializer(work_experience)
    return Response(serializer.data)

@api_view(['PUT'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsSuperAdminOrReadOnly])
def updateWorkExperience(request, member_id, experience_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    work_experience = get_object_or_404(WorkExperience, experience_id=experience_id, member=member)
    serializer = WorkExperienceSerializer(work_experience, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsSuperAdminOrReadOnly])
def deleteWorkExperience(request, member_id, experience_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    work_experience = get_object_or_404(WorkExperience, experience_id=experience_id, member=member)
    work_experience.delete()
    return Response({'message': 'Work experience deleted successfully'}, status=status.HTTP_204_NO_CONTENT) 

# Training Course Views
@api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAdminOrSuperAdmin])
def getTrainingCourses(request, member_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    training_courses = TrainingCourse.objects.filter(member=member)
    serializer = TrainingCourseSerializer(training_courses, many=True)
    return Response(serializer.data)

@api_view(['POST'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsSuperAdminOrReadOnly])
def createTrainingCourse(request, member_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    serializer = TrainingCourseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(member=member)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAdminOrSuperAdmin])
def getTrainingCourse(request, member_id, training_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    training_course = get_object_or_404(TrainingCourse, training_id=training_id, member=member)
    serializer = TrainingCourseSerializer(training_course)
    return Response(serializer.data)

@api_view(['PUT'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsSuperAdminOrReadOnly])
def updateTrainingCourse(request, member_id, training_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    training_course = get_object_or_404(TrainingCourse, training_id=training_id, member=member)
    serializer = TrainingCourseSerializer(training_course, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsSuperAdminOrReadOnly])
def deleteTrainingCourse(request, member_id, training_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    training_course = get_object_or_404(TrainingCourse, training_id=training_id, member=member)
    training_course.delete()
    return Response({'message': 'Training course deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# Quification Views
@api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAdminOrSuperAdmin])
def getQualifications(request, member_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    qualifications = Qualification.objects.filter(member=member)
    serializer = QualificationSerializer(qualifications, many=True)
    return Response(serializer.data)

@api_view(['POST'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsSuperAdminOrReadOnly])
def createQualification(request, member_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    serializer = QualificationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(member=member)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAdminOrSuperAdmin])
def getQualification(request, member_id, qualification_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    qualification = get_object_or_404(Qualification, qualification_id=qualification_id, member=member)
    serializer = QualificationSerializer(qualification)
    return Response(serializer.data)

@api_view(['PUT'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsSuperAdminOrReadOnly])
def updateQualification(request, member_id, qualification_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    qualification = get_object_or_404(Qualification, qualification_id=qualification_id, member=member)
    serializer = QualificationSerializer(qualification, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsSuperAdminOrReadOnly])
def deleteQualification(request, member_id, qualification_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    qualification = get_object_or_404(Qualification, qualification_id=qualification_id, member=member)
    qualification.delete()
    return Response({'message': 'Qualification deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# Awards and Recognition Views
@api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAdminOrSuperAdmin])
def getAwardsRecognitions(request, member_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    awards_recognitions = AwardsRecognition.objects.filter(member=member)
    serializer = AwardsRecognitionSerializer(awards_recognitions, many=True)
    return Response(serializer.data)

@api_view(['POST'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsSuperAdminOrReadOnly])
def createAwardsRecognition(request, member_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    serializer = AwardsRecognitionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(member=member)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAdminOrSuperAdmin])
def getAwardsRecognition(request, member_id, award_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    awards_recognition = get_object_or_404(AwardsRecognition, award_id=award_id, member=member)
    serializer = AwardsRecognitionSerializer(awards_recognition)
    return Response(serializer.data)

@api_view(['PUT'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsSuperAdminOrReadOnly])
def updateAwardsRecognition(request, member_id, award_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    awards_recognition = get_object_or_404(AwardsRecognition, award_id=award_id, member=member)
    serializer = AwardsRecognitionSerializer(awards_recognition, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsSuperAdminOrReadOnly])
def deleteAwardsRecognition(request, member_id, award_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    awards_recognition = get_object_or_404(AwardsRecognition, award_id=award_id, member=member)
    awards_recognition.delete()
    return Response({'message': 'Awards recognition deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# Disciplinary Action Views
@api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAdminOrSuperAdmin])
def getDisciplinaryActions(request, member_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    disciplinary_actions = DisciplinaryAction.objects.filter(member=member)
    serializer = DisciplinaryActionSerializer(disciplinary_actions, many=True)
    return Response(serializer.data)

@api_view(['POST'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsSuperAdminOrReadOnly])
def createDisciplinaryAction(request, member_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    serializer = DisciplinaryActionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(member=member)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAdminOrSuperAdmin])
def getDisciplinaryAction(request, member_id, penalty_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    disciplinary_action = get_object_or_404(DisciplinaryAction, penalty_id=penalty_id, member=member)
    serializer = DisciplinaryActionSerializer(disciplinary_action)
    return Response(serializer.data)

@api_view(['PUT'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsSuperAdminOrReadOnly])
def updateDisciplinaryAction(request, member_id, penalty_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    disciplinary_action = get_object_or_404(DisciplinaryAction, penalty_id=penalty_id, member=member)
    serializer = DisciplinaryActionSerializer(disciplinary_action, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsSuperAdminOrReadOnly])
def deleteDisciplinaryAction(request, member_id, penalty_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    disciplinary_action = get_object_or_404(DisciplinaryAction, penalty_id=penalty_id, member=member)
    disciplinary_action.delete()
    return Response({'message': 'Disciplinary action deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# Special Note Views
@api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAdminOrSuperAdmin])
def getSpecialNotes(request, member_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    special_notes = SpecialNote.objects.filter(member=member)
    serializer = SpecialNoteSerializer(special_notes, many=True)
    return Response(serializer.data)

@api_view(['POST'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsSuperAdminOrReadOnly])
def createSpecialNote(request, member_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    serializer = SpecialNoteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(member=member)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAdminOrSuperAdmin])
def getSpecialNote(request, member_id, note_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    special_note = get_object_or_404(SpecialNote, note_id=note_id, member=member)
    serializer = SpecialNoteSerializer(special_note)
    return Response(serializer.data)

@api_view(['PUT'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsSuperAdminOrReadOnly])
def updateSpecialNote(request, member_id, note_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    special_note = get_object_or_404(SpecialNote, note_id=note_id, member=member)
    serializer = SpecialNoteSerializer(special_note, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsSuperAdminOrReadOnly])
def deleteSpecialNote(request, member_id, note_id):
    member = get_object_or_404(Member, member_id=member_id, is_deleted=False)
    special_note = get_object_or_404(SpecialNote, note_id=note_id, member=member)
    special_note.delete()
    return Response({'message': 'Special note deleted successfully'}, status=status.HTTP_204_NO_CONTENT)









