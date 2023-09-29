from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404
import json
from django.contrib.auth.decorators import login_required
from django.core import serializers

from user.custom_auth_backend import EmailBackend
# Models
from student.models import EnrolledCourses, PlayingVideo,WatchedVideo
from instructor.models import Lesson, Course, Video

# forms
from user import forms as user_forms
from .forms import UpdateProfileForm

from django.db.models import Sum


@login_required
def dashboard(request):
    enrolled_courses = []
    watched_duration = 0
    print("you are in dashboard")
    user = request.user
    enrolled_course_by_student = Course.objects.filter(enrolledcourses__student=user.student)
    
    watched_video = WatchedVideo.objects.filter(student=user.student)
    
    for my_course in enrolled_course_by_student:
        course_dict = {}
        course_dict['title'] = my_course.title
        course_dict['slug'] = my_course.slug
        course_dict['image'] = my_course.featured_image.url
        course_dict['course_duration'] = my_course.course_duration
        
        for video in watched_video:
            if (my_course.title == video.course.title):
                watched_duration += video.video.time_duration
                course_dict['watched_duration'] = watched_duration
            else:
                course_dict['watched_duration'] = 0.0

        enrolled_courses.append(course_dict)
    print(enrolled_courses)
                
    
    if user:
        context = {
            'user': user,
            'enrolled_courses': enrolled_courses,
        }
        return render(request, 'student/dashboard.html', context)
    return Http404


# View:lists all the enrolled courses by the logged in student
@login_required
def my_course(request):
    user = request.user
    my_courses = EnrolledCourses.objects.filter(student=user.student)

    context = {
        'my_courses': my_courses,
    }
    print(context)

    for course in my_courses:
        print(course)
    return render(request, 'student/my_course.html', context)


# View for detailed course for enrolled course
@login_required
def my_course_detail_view(request, slug):
    context = {}
    course_video = Video.objects.filter(course__slug=slug)
    lessons = Lesson.objects.filter(course__slug=slug)
    watched_video = WatchedVideo.objects.filter(course__slug=slug,student=request.user.student)
    
    last_played_video = PlayingVideo.objects.filter(course__slug=slug,student=request.user.student).latest('updated_time')
    print(last_played_video.video.video_file.url)
    if not last_played_video:
        last_played_video = None
        
    context = {
        'videos': course_video,
        'lessons':lessons,
        'watched_video': watched_video,
        'last_played_video':last_played_video
    }
    print(context)
    return render(request,'student/my_course_detail.html', context)


# view for posting the playback time
@login_required
def track_video(request):
    data = {}
    if request.method == "POST" and request.is_ajax():
        data['success'] = True
        req_obj = json.load(request)
        suspend_time = req_obj['suspended_time']
        current_video_url = req_obj['currentVideoUrl']
        # print(suspend_time)
        # print(current_video_url)
        # print(request.user.student)
        video = Video.objects.filter(video_file=current_video_url).first()
        # print(type(video.lesson))

        # Create/update Instance in model "PlayingVideo"
        try:
            # Define the criteria
            criteria = {
                'video': video,
                'lesson': video.lesson,
                'course': video.course,
                'student': request.user.student,
            }

            # Try to retrieve an existing record
            existing_record = PlayingVideo.objects.filter(**criteria).first()

            # Update the 'pause_time' if the record exists, or create a new one
            if existing_record:
                existing_record.pause_time = suspend_time
                existing_record.save()
            else:
                # Create a new record with the specified criteria and 'pause_time'
                criteria['pause_time'] = suspend_time
                PlayingVideo.objects.create(**criteria)
        except Exception as e:
            print("Error: ", e)

        return HttpResponse(json.dumps(data), content_type='application/json')
    return JsonResponse({'status:200'})


# view for posting the watched video
@login_required
def save_watched_video(request):
    data = {}
    if request.method == "POST" and request.is_ajax():
        data['success'] = True
        req_obj = json.load(request)
        current_video_url = req_obj['currentVideoUrl']
        print(current_video_url)
        print(request.user.student)
        video = Video.objects.filter(
            video_file=current_video_url).first()
    

        
        # Check existence
        watched_video = WatchedVideo.objects.filter(course__slug=slug,video__video_file=current_video_url).exists()
        # Create Instance in model "Watched Video"
        if not watched_video:
            try:
                # Define the criteria
                criteria = {
                    'video': video,
                    'lesson': video.lesson,
                    'course': video.course,
                    'student': request.user.student,
                }

                # Try to save data to watchedvideo model
                watched_video = WatchedVideo.objects.create(**criteria)

            except Exception as e:
                print("Error Ocuured on saving Watched_Video")
                print(e)
            else:
                print("succesfully saved data")

        return HttpResponse(json.dumps(data), content_type='application/json')
    return JsonResponse({'status:200'})




@login_required
def update_student_profile(request):
    """views function to update the user profile"""
    user = request.user
    if user:
        update_user_info = user_forms.SignUpForm(
            request.POST or None, instance=user)
        update_profile_image = UpdateProfileForm(
            request.POST or None, request.FILES or None, instance=user.student)

        # Disable the email field for the signup form
        update_user_info.fields['email'].widget.attrs['readonly'] = True

        data = {}

        if request.method == 'POST' and request.is_ajax():
            if update_user_info.is_valid() and update_profile_image.is_valid():
                obj = update_user_info.save(commit=False)
                obj1 = update_profile_image.save(commit=False)

                obj.first_name = request.POST['first_name']
                obj.last_name = request.POST['last_name']

                update_user_info.save()
                update_profile_image.save()

                login(request, request.user,
                      backend='user.custom_auth_backend.EmailBackend')

                updated_data = {
                    'user_firstname': user.first_name,
                    'user_email': user.email,

                }
                data['success'] = True
                data['new_data'] = updated_data
                return HttpResponse(json.dumps(data), content_type='application/json')
            else:

                data['success'] = False
                data['u_form_errors'] = update_user_info.errors
                data['p_form_errors'] = update_profile_image.errors
                print(data['u_form_errors'])
                print(data['p_form_errors'])

                return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        return redirect('lms_main:home')
    context = {
        'user': user,
        'u_form': update_user_info,
        'p_form': update_profile_image
    }
    return render(request, 'student/user_profile.html', context)
