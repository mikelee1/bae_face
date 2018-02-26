# -*- coding: UTF-8 -*-
# coding=UTF-8
from django.shortcuts import render_to_response
from django import template
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.http import HttpResponseRedirect

from hill1895.models import Blog, Tag, Category1, Category2, Profile, Profile_Tag, Friend, Friend_Tag,Message,People
import cv2
from .forms import UploadFileForm
import time
import face_recognition
import sys,os
cwd = os.getcwd()
# sys.path.append(cwd)
# Create your views here.

# some function would be used in views


__category1 = {
    'geek': '技术博客',
    'essay': '随笔',
    'joke': '吐槽'
}
__category2 = {
    'Develop': '开发',
    'website': 'Web',
    'SRE': '运维',
    'book': '读书',
    'movie': '影评',
    'sports': '运动',
    'tour': '游记',
    'joke': '吐槽'
}


def __get_latest(objs, max_num=8):
    obj_num = objs.count()
    latest = []

    if obj_num > max_num:
        for i in range(max_num):
            latest.append({'title': objs[i].title, 'id': objs[i].id})
    else:
        for i in range(obj_num):
            latest.append({'title': objs[i].title, 'id': objs[i].id})

    return latest


def __get_blog_info(objs):
    # exclude blog content!
    blog_info = []

    for blog in objs:
        category1 = blog.category1.category_1
        category2 = blog.category2.category_2
        blog_info.append({'title': blog.title,
                          'id': blog.id,
                          'head_pic_url': blog.head_pic_url,
                          'pub_time': blog.pub_time,
                          'page_views': blog.page_views,
                          'category1': __category1[category1],
                          'category2': __category2[category2]})

    return blog_info


# pagination
def __my_pagination(request, objs, display_num=10, after_range=10, before_range=9):
    paginator = Paginator(objs, display_num)

    try:
        page = int(request.GET.get('page'))
    except:
        page = 1
    try:
        objects = paginator.page(page)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
    except:
        objects = paginator.page(1)

    if page > after_range:
        page_range = list(paginator.page_range)[page - after_range:page + before_range]
    else:
        page_range = list(paginator.page_range)[0:page + before_range]

    return objects, page_range


def __get_blog_list(request, obj_list):
    obj_latest = __get_latest(obj_list)
    obj_infos_all = __get_blog_info(obj_list)
    obj_infos, obj_page_range = __my_pagination(request, obj_infos_all)

    return obj_latest, obj_infos, obj_page_range


def __blog_by_category2(request, objs, category):
    obj_category = Category2.objects.get(category_2=category)
    obj_list = objs.filter(category2=obj_category)
    obj_infos_all = __get_blog_info(obj_list)
    obj_infos, obj_page_range = __my_pagination(request, obj_infos_all)

    return obj_infos, obj_page_range


###the views of the page


def index(request):
    blogs = Blog.objects.all()
    tags = Tag.objects.all()
    latest, blog_infos, page_range = __get_blog_list(request, blogs)
    friends = Friend.objects.all()
    content = {'blog_infos': blog_infos,
               'page_range': page_range,
               'tags': tags,
               'latest': latest,
               'friends': friends}
    return render_to_response('index.html', content)


def blog_detail(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    blog.page_views += 1
    blog.save()
    blog_tags = blog.tags.all()
    category1 = blog.category1.category_1
    category2 = blog.category2.category_2
    category2_url = category1.lower() + '#' + category2
    return render_to_response('detail.html',
                              {'blog': blog,
                               'blog_tags': blog_tags,
                               'category1': __category1[category1],
                               'category2': __category2[category2],
                               'category1_url': category1.lower(),
                               'category2_url': category2_url
                               })


def tag(request, tag_id):
    get_tag = Tag.objects.get(id=tag_id)
    blogs = Blog.objects.filter(tags=get_tag)
    tags = Tag.objects.all()
    tag_latest, tag_infos, page_range = __get_blog_list(request, blogs)
    friends = Friend.objects.all()
    content = {'tag_infos': tag_infos,
               'page_range': page_range,
               'tag_latest': tag_latest,
               'get_tag': get_tag,
               'tags': tags,
               'friends': friends}

    return render_to_response('tag.html', content)


def geek(request):
    geek = Category1.objects.get(category_1='geek')
    blogs_geek = Blog.objects.filter(category1=geek)

    tags = Tag.objects.all()

    geek_latest, geek_infos, geek_page_range = __get_blog_list(request, blogs_geek)

    develop_infos, develop_page_range = __blog_by_category2(request, blogs_geek, 'Develop')
    website_infos, website_page_range = __blog_by_category2(request, blogs_geek, 'website')
    SRE_infos, SRE_page_range = __blog_by_category2(request, blogs_geek, 'SRE')

    friends = Friend.objects.all()
    content = {'geek_infos': geek_infos,
               'geek_page_range': geek_page_range,
               'develop_infos': develop_infos,
               'develop_page_range': develop_page_range,
               'website_infos': website_infos,
               'website_page_range': website_page_range,
               'SRE_infos': SRE_infos,
               'SRE_page_range': SRE_page_range,
               'geek_latest': geek_latest,
               'tags': tags,
               'friends': friends}

    return render_to_response('geek.html', content)


def essay(request):
    essay = Category1.objects.get(category_1='essay')
    blogs_essay = Blog.objects.filter(category1=essay)

    tags = Tag.objects.all()

    essay_latest, essay_infos, essay_page_range = __get_blog_list(request, blogs_essay)

    book_infos, book_page_range = __blog_by_category2(request, blogs_essay, 'book')
    movie_infos, movie_page_range = __blog_by_category2(request, blogs_essay, 'movie')
    sports_infos, sports_page_range = __blog_by_category2(request, blogs_essay, 'sports')
    tour_infos, tour_page_range = __blog_by_category2(request, blogs_essay, 'tour')

    friends = Friend.objects.all()
    content = {'essay_infos': essay_infos,
               'essay_page_range': essay_page_range,
               'book_infos': book_infos,
               'book_page_range': book_page_range,
               'movie_infos': movie_infos,
               'movie_page_range': movie_page_range,
               'sports_infos': sports_infos,
               'sports_page_range': sports_page_range,
               'tour_infos': tour_infos,
               'tour_page_range': tour_page_range,
               'essay_latest': essay_latest,
               'tags': tags,
               'friends': friends}

    return render_to_response('essay.html', content)


def joke(request):
    joke = Category2.objects.get(category_2='joke')
    blogs_joke = Blog.objects.filter(category2=joke)

    tags = Tag.objects.all()

    joke_latest, joke_infos, joke_page_range = __get_blog_list(request, blogs_joke)

    friends = Friend.objects.all()
    content = {'joke_infos': joke_infos,
               'joke_page_range': joke_page_range,
               'joke_latest': joke_latest,
               'tags': tags,
               'friends': friends}

    return render_to_response('joke.html', content)


def profile(request):
    profile = Profile.objects.get(title='Profile')
    updates = Profile.objects.get(title='Updates')
    profile_tags = profile.tags.all()
    return render_to_response('profile.html',
                              {'profile': profile,
                               'updates': updates,
                               'profile_tags': profile_tags
                               })


def face(request):
    if request.method == 'POST':

        form = UploadFileForm(request.POST, request.FILES)
        a = request.FILES['imgpath']
        b = request.FILES['audio']
        name = request.POST['receivername']
        with open(cwd+'/mysite/'+name,'wb') as f1:
            for i in a.chunks():
                f1.write(i)
        with open(cwd+'/mysite/'+b._name,'wb') as f2:
            for i in b.chunks():
                f2.write(i)
        receiver = Message(img = name,audio =cwd+'/mysite/'+b._name )
        receiver.save()

        personcheck = People.objects.filter(name = name)
        if personcheck:
            pass
        else:
            person = People(name = name)
            person.save()

        return HttpResponseRedirect('/face')
    else:
        tags = Tag.objects.all()



        return render_to_response('face_recog.html',
                                  {
                                      'tags':tags
                                  },context_instance=RequestContext(request))

def invoke_camera(request):

    # This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
    # other example, but it includes some basic performance tweaks to make things run a lot faster:
    #   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
    #   2. Only detect faces in every other frame of video.

    # PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
    # OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
    # specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)
    persons = People.objects.all()
    messages = Message.objects.all()
    known_face_encodings = []
    known_face_names = []
    for i in persons:
        obama_image = face_recognition.load_image_file(cwd+"/mysite/"+i.name+".jpg")
        obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
        known_face_encodings.append(obama_face_encoding)
        known_face_names.append(i.name)


    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        terminal = False
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]
                    personmess = messages.filter(img = name)
                    os.system('play '+str(personmess[0].audio))
                    terminal = True
                    break

            if terminal:
                break
                face_names.append(name)

        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

    return HttpResponseRedirect('/face')

    # tags = Tag.objects.all()
    #
    # return render_to_response('face_recog.html',
    #                           {
    #                               'tags':tags
    #                           },context_instance=RequestContext(request))







from pyaudio import PyAudio, paInt16
import numpy as np
from datetime import datetime
import wave

class recoder:
    NUM_SAMPLES = 2000      #pyaudio内置缓冲大小
    SAMPLING_RATE = 8000    #取样频率
    LEVEL = 500         #声音保存的阈值
    COUNT_NUM = 20      #NUM_SAMPLES个取样之内出现COUNT_NUM个大于LEVEL的取样则记录声音
    SAVE_LENGTH = 8         #声音记录的最小长度：SAVE_LENGTH * NUM_SAMPLES 个取样
    TIME_COUNT = 60     #录音时间，单位s

    Voice_String = []

    def savewav(self,filename):
        wf = wave.open(filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(self.SAMPLING_RATE)
        wf.writeframes(np.array(self.Voice_String).tostring())
        # wf.writeframes(self.Voice_String.decode())
        wf.close()

    def recoder(self):
        pa = PyAudio()
        stream = pa.open(format=paInt16, channels=1, rate=self.SAMPLING_RATE, input=True,
            frames_per_buffer=self.NUM_SAMPLES)
        save_count = 0
        save_buffer = []
        time_count = self.TIME_COUNT
        num = 0
        while True:
            num+=1
            time_count -= 1
            # print time_count
            # 读入NUM_SAMPLES个取样
            string_audio_data = stream.read(self.NUM_SAMPLES)
            # 将读入的数据转换为数组
            audio_data = np.fromstring(string_audio_data, dtype=np.short)
            # 计算大于LEVEL的取样的个数
            large_sample_count = np.sum( audio_data > self.LEVEL )
            print(np.max(audio_data))
            # 如果个数大于COUNT_NUM，则至少保存SAVE_LENGTH个块
            if large_sample_count > self.COUNT_NUM:
                save_count = self.SAVE_LENGTH
            else:
                save_count -= 1

            if save_count < 0:
                save_count = 0

            if save_count > 0 :
            # 将要保存的数据存放到save_buffer中
                #print  save_count > 0 and time_count >0
                save_buffer.append( string_audio_data )
            else:
            #print save_buffer
            # 将save_buffer中的数据写入WAV文件，WAV文件的文件名是保存的时刻
                #print "debug"
                if len(save_buffer) > 0 :
                    self.Voice_String = save_buffer
                    save_buffer = []
                    print("Recode a piece of  voice successfully!")
                    return True
            if time_count==0:
                if len(save_buffer)>0:
                    self.Voice_String = save_buffer
                    save_buffer = []
                    print("Recode a piece of  voice successfully!")
                    return True
                else:
                    return False
import uuid
def invoke_audio(request):
    r = recoder()
    r.recoder()
    randomstr = str(uuid.uuid1())
    r.savewav(randomstr+".wav")
    return HttpResponseRedirect('/face/?message='+randomstr)
    # tags = Tag.objects.all()
    #
    # return render_to_response('face_recog.html',
    #                           {
    #                               'tags':tags,
    #                               'message':randomstr
    #                           },context_instance=RequestContext(request))

def record(request):
    return render_to_response('record.html')