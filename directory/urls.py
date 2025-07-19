from django.urls import path
from . import views

urlpatterns = [
    # Authentication routes
    path('auth/login/', views.login, name='login'),
    path('auth/logout/', views.logout, name='logout'),
    path('auth/profile/', views.profile, name='profile'),
    path('accounts/', views.getAccounts, name='get-accounts'),  # view all accounts
    path('create-account/', views.createAccount, name='create-admin'),  # admin creation

    path('', views.getDashboard, name='get-dashboard'),
    path('members/', views.getMembers, name='get-members'),
    path('members/create/', views.createMember, name='create-member'), # member creation
    path('members/<str:member_id>/', views.getMember, name='get-member'), # member selection
    path('members/<str:member_id>/update/', views.updateMember, name='update-member'), # member update
    path('members/<str:member_id>/delete/', views.deleteMember, name='delete-member'), # member soft delete

    path('members/<str:member_id>/academic-background/', views.getAcademicBackgrounds, name='get-academic-background'),
    path('members/<str:member_id>/academic-background/create/', views.createAcademicBackground, name='create-academic-backgrounds'), # academic background creation
    path('members/<str:member_id>/academic-background/<str:academic_record_id>/', views.getAcademicBackground, name='get-academic-background'),
    path('members/<str:member_id>/academic-background/<str:academic_record_id>/update/', views.updateAcademicBackground, name='update-academic-background'), # academic background update
    path('members/<str:member_id>/academic-background/<str:academic_record_id>/delete/', views.deleteAcademicBackground, name='delete-academic-background'), # academic background soft delete
    
    path('members/<str:member_id>/family-details/', views.getFamilyDetails, name='get-family-details'), # view family details
    path('members/<str:member_id>/family-details/create/', views.createFamilyDetail, name='create-family-detail'), # family detail creation
    path('members/<str:member_id>/family-details/<str:family_member_id>/', views.getFamilyDetail, name='get-family-detail'), # family detail selection
    path('members/<str:member_id>/family-details/<str:family_member_id>/update/', views.updateFamilyDetail, name='update-family-detail'), # family detail update
    path('members/<str:member_id>/family-details/<str:family_member_id>/delete/', views.deleteFamilyDetail, name='delete-family-detail'), # family detail  delete

    path('members/<str:member_id>/public-mission-posts/', views.getPublicMissionPosts, name='get-public-mission-posts'), # view public mission posts
    path('members/<str:member_id>/public-mission-posts/create/', views.createPublicMissionPost, name='create-public-mission-post'), # public mission post creation
    path('members/<str:member_id>/public-mission-posts/<str:mission_id>/', views.getPublicMissionPost, name='get-public-mission-post'), # public mission post selection
    path('members/<str:member_id>/public-mission-posts/<str:mission_id>/update/', views.updatePublicMissionPost, name='update-public-mission-post'), # public mission post update
    path('members/<str:member_id>/public-mission-posts/<str:mission_id>/delete/', views.deletePublicMissionPost, name='delete-public-mission-post'), # public mission post delete

    path('members/<str:member_id>/work-experiences/', views.getWorkExperiences, name='get-work-experiences'), # view work experiences
    path('members/<str:member_id>/work-experiences/create/', views.createWorkExperience, name='create-work-experience'), # work experience creation
    path('members/<str:member_id>/work-experiences/<str:experience_id>/', views.getWorkExperience, name='get-work-experience'), # work experience selection
    path('members/<str:member_id>/work-experiences/<str:experience_id>/update/', views.updateWorkExperience, name='update-work-experience'), # work experience update
    path('members/<str:member_id>/work-experiences/<str:experience_id>/delete/', views.deleteWorkExperience, name='delete-work-experience'), # work experience delete

    path('members/<str:member_id>/training-courses/', views.getTrainingCourses, name='get-training-courses'), # view training courses
    path('members/<str:member_id>/training-courses/create/', views.createTrainingCourse, name='create-training-course'), # training course creation
    path('members/<str:member_id>/training-courses/<str:training_id>/', views.getTrainingCourse, name='get-training-course'), # training course selection
    path('members/<str:member_id>/training-courses/<str:training_id>/update/', views.updateTrainingCourse, name='update-training-course'), # training course update
    path('members/<str:member_id>/training-courses/<str:training_id>/delete/', views.deleteTrainingCourse, name='delete-training-course'), # training course delete

    path('members/<str:member_id>/qualifications/', views.getQualifications, name='get-qualifications'), # view qualifications
    path('members/<str:member_id>/qualifications/create/', views.createQualification, name='create-qualification'), # qualification creation
    path('members/<str:member_id>/qualifications/<str:qualification_id>/', views.getQualification, name='get-qualification'), # qualification selection
    path('members/<str:member_id>/qualifications/<str:qualification_id>/update/', views.updateQualification, name='update-qualification'), # qualification update
    path('members/<str:member_id>/qualifications/<str:qualification_id>/delete/', views.deleteQualification, name='delete-qualification'), # qualification delete

    path('members/<str:member_id>/awards-recognition/', views.getAwardsRecognitions, name='get-awards-recognition'), # view awards and recognition
    path('members/<str:member_id>/awards-recognition/create/', views.createAwardsRecognition, name='create-award-recognition'), # awards and recognition creation
    path('members/<str:member_id>/awards-recognition/<str:award_id>/', views.getAwardsRecognition, name='get-award-recognition'), # awards and recognition selection
    path('members/<str:member_id>/awards-recognition/<str:award_id>/update/', views.updateAwardsRecognition, name='update-award-recognition'), # awards and recognition update
    path('members/<str:member_id>/awards-recognition/<str:award_id>/delete/', views.deleteAwardsRecognition, name='delete-award-recognition'), # awards and recognition delete

    path('members/<str:member_id>/disciplinary-actions/', views.getDisciplinaryActions, name='get-disciplinary-actions'), # view disciplinary actions
    path('members/<str:member_id>/disciplinary-actions/create/', views.createDisciplinaryAction, name='create-disciplinary-action'), # disciplinary action creation
    path('members/<str:member_id>/disciplinary-actions/<str:penalty_id>/', views.getDisciplinaryAction, name='get-disciplinary-action'), # disciplinary action selection
    path('members/<str:member_id>/disciplinary-actions/<str:penalty_id>/update/', views.updateDisciplinaryAction, name='update-disciplinary-action'), # disciplinary action update
    path('members/<str:member_id>/disciplinary-actions/<str:penalty_id>/delete/', views.deleteDisciplinaryAction, name='delete-disciplinary-action'), # disciplinary action delete

    path('members/<str:member_id>/special-note/', views.getSpecialNotes, name='get-special-notes'), # view special notes
    path('members/<str:member_id>/special-note/create/', views.createSpecialNote, name='create-special-note'), # special note creation
    path('members/<str:member_id>/special-note/<str:note_id>/', views.getSpecialNote, name='get-special-note'), # special note selection
    path('members/<str:member_id>/special-note/<str:note_id>/update/', views.updateSpecialNote, name='update-special-note'), # special note update
    path('members/<str:member_id>/special-note/<str:note_id>/delete/', views.deleteSpecialNote, name='delete-special-note'), # special note delete
]