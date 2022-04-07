import functools
import itertools
import json
import requests
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse, HttpRequest
from django.shortcuts import render
from .models import *
from django.urls import reverse
from django.db.models import Sum

class Counter():

    def __init__(self):
        self.count = 1

    def increase(self):
        return self.count + 1



def index(request, message = None):
    last_search_courses = []
    query = ''
    if request.user.is_authenticated:
        query = Student.objects.get(user=request.user).last_search
        if query:
            all_course = Course.objects.all()
            for course in all_course:
                if query.upper() in course.title.upper() or query.upper() == course.category.category.upper() or query.upper() in course.subtitle.upper():
                    last_search_courses.append(course)
    return render(request, "onlineCourses/index.html", {
        'courses': Course.objects.all(),
        'categories': Category.objects.all(),
        'last_search_courses': last_search_courses,
        'query': query,
        'message': message
    })


def getQA(request, course_id):
    course = Course.objects.get(pk = int(course_id))

    return JsonResponse({"qa": [question.serialize() for question in course.aq.all().order_by('-id')]})

def rate_view(request, course_id):
    if request.method == "POST":
        rate = request.POST['rate']
        why = request.POST['why']
        course = Course.objects.get(pk = int(course_id))
        review = Review()
        review.review = rate
        review.review_text = why
        review.reviewer = Student.objects.get(user = request.user)
        review.save()
        course.review.add(review)
        course.save()
        return HttpResponseRedirect(reverse("viewcoursecontent", args=(course_id, )))

    student = Student.objects.get(user=request.user)
    course = Course.objects.get(pk=int(course_id))
    if course.review.filter(reviewer=student) or not course in student.course.all():
        return index(request, "You need to take the course in order to rate or you have already rated!")

    return render(request, "onlineCourses/rate.html", {
        "course":  Course.objects.get(pk = int(course_id)),
    })

def addAnswer(request, question_id):
    if request.method == "POST":
        data = json.loads(request.body)
        body = data.get("body", "")
        new_answer = Answer()
        new_answer.body = body
        new_answer.user = Student.objects.get(user = request.user)
        new_answer.save()
        question = Question.objects.get(pk = int(question_id))
        question.answers.add(new_answer)
        question.save()
        return JsonResponse({"message":"completed", "answer": new_answer.serialize()}, status=201)
    else:
        return JsonResponse({"error": "not completed"}, status=201)

def addQuestion(request, course_id):
    if request.method == "POST":
        data = json.loads(request.body)
        title = data.get("title", "")
        body = data.get("body", "")
        course = Course.objects.get(pk = int(course_id))
        new_question = Question()
        new_question.title = title
        new_question.body = body
        new_question.user = Student.objects.get(user = request.user)
        new_question.save()
        course.aq.add(new_question)
        course.save()
        return JsonResponse({"message":"completed"}, status=201)
    else:
        return JsonResponse({"error": "not completed"}, status=201)


def instructorDasboard(request):
    return render(request, "onlineCourses/instructor.html", {
        "my_courses": Instructor.objects.get(user=request.user).in_courses.all()
    })

def completePayment(request):
    student = Student.objects.get(user = request.user)
    if student.payment.filter(completed = False):
        payment_ = student.payment.get(completed=False)
    else:
        return index(request, "Please add to card items firstly!")

    payment_.applyDiscount()
    print(payment_.total_price)

    if payment_.total_price == 0.0:
        for course_ in payment_.courses.all():
            student.course.add(course_)
        payment_.completed = True
        payment_.save()
        student.card.clear()
        student.save()
        return index(request, "Payment was completed! You can find the course in 'my courses'")

    return index(request, "Payment is not complete!")


def applyCoupon(request):
    if request.method == "POST":
        name_ = request.POST['coupon']

        if Coupon.objects.filter(name = name_):
            coupon = Coupon.objects.get(name = name_)
        else:
            return HttpResponseRedirect(reverse('mycourses', args=('card',)))

        student = Student.objects.get(user = request.user)
        payment_ = student.payment.get(completed = False)
        payment_.coupon.add(coupon)

        return HttpResponseRedirect(reverse('mycourses', args=('card',)))


def payment(request, type):
    buy_courses = []
    if type == "card":
        total = Student.objects.get(user=request.user).card.aggregate(Sum('price'))['price__sum']
        if total:
            total = round(total, 2)

        if Student.objects.get(user = request.user).payment.filter(completed=False):
            payment_detail = Student.objects.get(user = request.user).payment.get(completed=False)
        else:
            payment_detail = Payment()
        payment_detail.total_price = total
        payment_detail.save()
        student = Student.objects.get(user=request.user)
        if payment_detail.coupon.all():
            payment_detail.applyDiscount()
        for course in student.card.all():
            payment_detail.courses.add(course)
        student.payment.add(payment_detail)
        student.save()
        for course in student.card.all():
            buy_courses.append(course)
    else:
        if not request.user.is_authenticated:
            return  HttpResponseRedirect(reverse("login"))
        course = Course.objects.get(pk = int(type))
        total = course.price
        if total:
            total = round(total, 2)

        if Payment.objects.filter(completed=False):
            payment_detail = Payment.objects.get(completed=False)
        else:
            payment_detail = Payment()
        payment_detail.total_price = total
        payment_detail.save()
        student = Student.objects.get(user=request.user)
        if payment_detail.coupon.all():
            payment_detail.coupon.clear()
        if payment_detail.courses.all():
            payment_detail.courses.clear()
        payment_detail.courses.add(course)
        student.payment.add(payment_detail)
        student.save()
        buy_courses.append(course)

    return render(request, "onlineCourses/payment.html",{
        "courses": buy_courses,
        "payment": payment_detail,
        "total": round(total,2),
        'discount': round(total-payment_detail.roundedPrice(), 2)
    })


def userprofile(request, user_id):
    puser = User.objects.get(pk = int(user_id))
    instructor = Instructor.objects.get(user = puser)
    student = Student.objects.get(user = puser)
    if instructor.in_courses.all().count() == 0:
        is_student = True
    else:
        is_student = False
    return render(request, "onlineCourses/profile.html",{
        "instructor": instructor,
        "is_student": is_student,
        "student": student
    })

def editCourse(request, course_id):
    if request.method == 'POST':
        new_course = Course.objects.get(pk=int(course_id))
        title = request.POST['title']
        image = request.POST['image']
        level = request.POST['level']
        subtitle_language = request.POST.getlist('subtitle_language')
        course_message = request.POST['course_message']
        subtitle = request.POST['subtitle']
        price = request.POST['price']
        language = request.POST['language']
        category = request.POST['category']
        description = request.POST['description']
        new_course.title = title
        new_course.subtitle = subtitle
        new_course.image_link = image
        new_course.description = description
        new_course.level = Level.objects.get(pk=int(level))
        new_course.language = Language.objects.get(pk=int(language))
        new_course.category = Category.objects.get(pk=int(category))
        new_course.price = price
        new_course.course_message = course_message
        new_course.updated = datetime.today().strftime('%Y-%m-%d')
        new_course.save()
        # course.subtitle_language.e
        new_course.subtitle_language.remove(*new_course.subtitle_language.all())
        for sl in subtitle_language:
            lang = Language.objects.get(pk=int(sl))
            new_course.subtitle_language.add(lang)
        return HttpResponseRedirect(reverse('instructor'))

    course = Course.objects.get(pk=int(course_id))
    if not Instructor.objects.get(user = request.user) in course.instructor.all():
        return index(request, f"{course.title} titled is not yours")
    return render(request, "onlineCourses/edit.html", {
        "course": course,
        "levels": Level.objects.all(),
        "languages": Language.objects.all(),
        'categories': Category.objects.all(),
    })


def deleteCourse(request, course_id):
    Course.objects.get(pk=int(course_id)).delete()
    return HttpResponseRedirect(reverse('instructor'))

def getContent(request, course_id):
    course = Course.objects.get(pk = int(course_id))

    return JsonResponse({"content": [lecture.serialize() for lecture in course.content.all()]}, status=201)


def deleteSection(request, section_id):
    section = Section.objects.get(pk = int(section_id))
    section.lecture.all().delete()
    section.delete()
    return JsonResponse({"message": "Section was deleted"}, status=201)

def editSection(request, section_id):
    return JsonResponse({"message": "Section was editted"}, status=201)


def addSection(request, course_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get("title", "")
        course = Course.objects.get(pk = int(course_id))
        new_section = Section()
        new_section.title = title
        new_section.save()
        course.content.add(new_section)
        return JsonResponse({'message':"succesfully added"}, status=201)
    else:
        return JsonResponse({'error':"Method must be a post"}, status=201)

def deleteLecture(request, lecture_id):
    Lecture.objects.get(pk = int(lecture_id)).delete()
    return JsonResponse({"message":"Lecture was deleted"}, status=201)

def addLecture(request, section_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get("title", "")
        video_link = data.get("link", "")
        id_index_start = video_link.index("embed/")
        id_index_finish = video_link.index("?")
        video_id = video_link[id_index_start+6:id_index_finish]
        response = requests.get(f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&key=AIzaSyDr_nUnCKGKz8PDnxW0zvR52Oqf6SU-nAg&part=contentDetails")
        response = response.json()
        duration = response["items"][0]["contentDetails"]["duration"]
        duration = duration.replace('M',':').replace('S','').replace('PT','')
        section = Section.objects.get(pk = int(section_id))
        lecture = Lecture()
        lecture.title = title
        lecture.video_duration = duration
        lecture.video_link = video_link

        lecture.save()
        section.lecture.add(lecture)
        return JsonResponse({'message':"succesfully added"}, status=201)
    else:
        return JsonResponse({'error':"Method must be a post"}, status=201)


def viewCourseContent(request, course_id):
    if request.user.is_authenticated:
        student = Student.objects.get(user = request.user)
        course = Course.objects.get(pk = int(course_id))
        if course in student.course.all() or Instructor.objects.get(user = request.user) in course.instructor.all():
            student = Student.objects.get(user=request.user)
            course = Course.objects.get(pk=int(course_id))
            if course.review.filter(reviewer=student):
                is_rate = True
            else:
                is_rate = False
            return render(request, "onlineCourses/coursecontent.html",{
                'course': course,
                'section_counter': functools.partial(next, itertools.count(start=1)),
                'lecture_counter': functools.partial(next, itertools.count(start=1)),
                "is_rate": is_rate
            })
        else:
            return index(request, "You need to buy the course in order to open it")
    else:
        return HttpResponseRedirect(reverse('login'))

def getLecture(request, lecture_id):
    return JsonResponse({"lecture": Lecture.objects.get(pk = int(lecture_id)).serialize()}, status=201)

def createCourse(request):
    if request.method == 'POST':
        title = request.POST['title']
        image = request.POST['image']
        level = request.POST['level']
        subtitle_language = request.POST.getlist('subtitle_language')
        course_message = request.POST['course_message']
        subtitle = request.POST['subtitle']
        price = request.POST['price']
        language = request.POST['language']
        category = request.POST['category']
        description = request.POST['description']
        print(course_message)
        new_course = Course()
        new_course.title = title
        new_course.subtitle = subtitle
        new_course.image_link = image
        new_course.description = description
        ins = Instructor.objects.get(user=request.user)
        new_course.level = Level.objects.get(pk=int(level))
        new_course.language = Language.objects.get(pk=int(language))
        new_course.category = Category.objects.get(pk=int(category))
        new_course.price = price
        new_course.course_message = course_message
        new_course.save()
        for sl in subtitle_language:
            lang = Language.objects.get(pk=int(sl))
            new_course.subtitle_language.add(lang)
        new_course.instructor.add(ins)

        return HttpResponseRedirect(reverse('instructor'))
    return render(request, "onlineCourses/create.html", {
        "levels": Level.objects.all(),
        "languages": Language.objects.all(),
        'categories': Category.objects.all(),
    })


def editProfile(request):
    if request.method == "POST":
        firstname = request.POST["first_name"]
        lastname = request.POST["last_name"]
        status = request.POST["status"]
        about = request.POST["about"]
        user = request.user
        user.first_name = firstname
        user.last_name = lastname
        user.save()
        student = Student.objects.get(user=user)
        student.save()
        ins = Instructor.objects.get(user=user)
        ins.status = status
        ins.about = about
        ins.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "onlineCourses/editProfile.html", {
        "user": request.user,
        "student": Student.objects.get(user=request.user),
        "instructor": Instructor.objects.get(user=request.user),
        "languages": Language.objects.all(),
    })


def course(request, course_id):
    if request.user.is_authenticated:
        student = Student.objects.get(user=request.user)
        course = Course.objects.get(pk=int(course_id))
        print(course.students.all().count())
        if course in student.wishlist.all():
            is_in_wishlist = True
        else:
            is_in_wishlist = False

        if course in student.card.all():
            is_in_card = True
        else:
            is_in_card = False

        if course in student.course.all():
            is_in_course = True
        else:
            is_in_course = False

        if course.price == 0:
            free = True
        else:
            free = False

        if Instructor.objects.get(user =request.user) in course.instructor.all():
            mine = True
        else:
            mine = False
    else:
        is_in_wishlist = False
        is_in_card = False
        is_in_course = False
        free = False
        mine = False

    return render(request, "onlineCourses/course.html", {
        'course': Course.objects.get(pk=int(course_id)),
        'wishlist': is_in_wishlist,
        'is_in_card': is_in_card,
        'is_in_course': is_in_course,
        'free': free,
        'mine': mine
    })



def myCourses(request, which):
    total = Student.objects.get(user=request.user).card.aggregate(Sum('price'))['price__sum']
    if total:
        total = round(total, 2)
    else:
        total = 0

    if Student.objects.get(user=request.user).payment.filter(completed=False):
        payment_ = Student.objects.get(user=request.user).payment.get(completed=False)
    else:
        payment_ = Payment()
    payment_.total_price = total
    payment_.save()
    student = Student.objects.get(user = request.user)
    if payment_.coupon.all():
        payment_.applyDiscount()
    if payment_.courses.all():
        payment_.courses.clear()
    for course in student.card.all():
        payment_.courses.add(course)
    student.payment.add(payment_)
    student.save()
    return render(request, "onlineCourses/mycourses.html",{
        'student':Student.objects.get(user = request.user),
         'payment_information': payment_,
        'total': total
    })

def addToCard(request, course_id):
    if request.user.is_authenticated:
        student = Student.objects.get(user =request.user)
        course = Course.objects.get(pk=int(course_id))
        student.card.add(course)
        student.save()
        return JsonResponse({'is_in_card':True}, status=201)
    else:
        return JsonResponse({"error": "User is not logged in"}, status=201)



def toggleWishlist(request, course_id):
    if request.user.is_authenticated:
        student = Student.objects.get(user=request.user)
        course = Course.objects.get(pk=int(course_id))
        if course in student.wishlist.all():
            student.wishlist.remove(course)
            student.save()
            is_in_wishlist = False
        else:
            student.wishlist.add(course)
            student.save()
            is_in_wishlist = True
        return JsonResponse({"wishlist": is_in_wishlist}, status=201)
    else:
        return JsonResponse({"error": 'User is not logged in'}, status=201)


def FromCard(request, what, course_id):
    student = Student.objects.get(user = request.user)
    course = Course.objects.get(pk = int(course_id))
    if what == 'move':
        if course in student.card.all():
            student.card.remove(course)
        else:
            return HttpResponseRedirect(reverse('mycourses', args=('card',)))
        student.wishlist.add(course)
    elif what == 'remove':
        student.card.remove(course)
    return HttpResponseRedirect(reverse('mycourses', args=('card',)))

def addcourse(request, course_id):
    course = Course.objects.get(pk = int(course_id))
    student = Student.objects.get(user=request.user)
    student.course.add(course)

    return HttpResponseRedirect(reverse('viewcoursecontent', args=(course_id, )))


def search(request):
    query = request.GET.get('q')
    print(query)
    if query == '':
        return HttpResponseRedirect(reverse('index'))
    for category in Category.objects.all():
        if query.upper() == category.category.upper():
            query = category.category
            break
    if request.user.is_authenticated:
        student = Student.objects.get(user=request.user)
        student.last_search = query
        student.save()
    result_courses = []
    if query:
        all_course = Course.objects.all()
        for course in all_course:
            if query.upper() in course.title.upper() or query.upper() == course.category.category.upper() or query.upper() in course.subtitle.upper():
                result_courses.append(course)
    return render(request, "onlineCourses/search.html", {
        'search': query,
        'languages': Language.objects.all(),
        'levels': Level.objects.all(),
        'categories': Category.objects.all(),
        'course_len': len(result_courses)
    })



def searchResult(request, query):
    filter_obj = Filter.objects.all().first()
    result_courses = []
    filter = {}
    lan = []
    cate = []
    lev = []
    for language in Language.objects.all():
        lan.append(False)
    filter['language_boolean'] = lan
    lan = []
    for language in Language.objects.all():
        lan.append(language.language_text)
    filter['language'] = lan
    for category in Category.objects.all():
        cate.append(False)
    filter['category_boolean'] = cate
    cate = []
    for category in Category.objects.all():
        cate.append(category.category)
    filter['category'] = cate
    for level in Level.objects.all():
        lev.append(False)

    filter['level_boolean'] = lev
    lev = []
    for level in Level.objects.all():
        lev.append(level.level_text)
    filter['level'] = lev
    if query:
        all_course = Course.objects.all()
        for course in all_course:
            if query.upper() in course.title.upper() or query.upper() == course.category.category.upper() or query.upper() in course.subtitle.upper():
                result_courses.append(course)

    if request.method == 'POST':
        res = []
        data = json.loads(request.body)
        filter_subject = data.get("filter", "")
        filter_type = data.get('type', "")
        if filter_type == 'language':
            language = Language.objects.get(language_text=filter_subject)
            if language in filter_obj.language.all():
                filter_obj.language.remove(language)
            else:
                filter_obj.language.add(language)
        elif filter_type == 'category':
            category = Category.objects.get(category=filter_subject)
            if category in filter_obj.category.all():
                filter_obj.category.remove(category)
            else:
                filter_obj.category.add(category)
        elif filter_type == 'level':
            level = Level.objects.get(level_text=filter_subject)
            if level in filter_obj.level.all():
                filter_obj.level.remove(level)
            else:
                filter_obj.level.add(level)

        for i in range(len(filter['language_boolean'])):
            if not (Language.objects.get(language_text=filter['language'][i]) in filter_obj.language.all()):
                filter['language_boolean'][i] = True

        for i in range(len(filter['category_boolean'])):
            if not (Category.objects.get(category=filter['category'][i]) in filter_obj.category.all()):
                filter['category_boolean'][i] = True

        for i in range(len(filter['level_boolean'])):
            if not (Level.objects.get(level_text=filter['level'][i]) in filter_obj.level.all()):
                filter['level_boolean'][i] = True

        level_list = []
        category_list = []
        language_list = []
        for level in Level.objects.all():
            if not (level in filter_obj.level.all()):
                level_list.append(level)
        for category in Category.objects.all():
            if not (category in filter_obj.category.all()):
                category_list.append(category)
        for language in Language.objects.all():
            if not (language in filter_obj.language.all()):
                language_list.append(language)


        if len(level_list) != 0:
            for course in result_courses:
                for level in level_list:
                    if course.level == level:
                        res.append(course)
        else:
            res = result_courses
        new_res = []
        if len(category_list) !=0:
            for course in res:
                for category in category_list:
                    if course.category == category:
                        new_res.append(course)
                        break
        else:
            new_res = res


        new_res, res = res, new_res
        new_res = []
        if len(language_list) != 0:
            for course in res:
                for language in language_list:
                    if course.language == language:
                        new_res.append(course)
        else:
            new_res = res

        new_res, res = res, new_res



        return JsonResponse({"result": [course.serialize() for course in res], 'filter': filter}, status=201)

    for langauge in Language.objects.all():
        filter_obj.language.add(langauge)
    for category in Category.objects.all():
        filter_obj.category.add(category)
    for level in Level.objects.all():
        filter_obj.level.add(level)

    return JsonResponse({"result": [course.serialize() for course in result_courses], 'filter': filter}, status=201)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "onlineCourses/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "onlineCourses/login.html")


def logout_view(request):
    logout(request)
    return index(request, "Logged out Succesfully!")


def register(request):
    if request.method == "POST":
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        email = request.POST["email"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "onlineCourses/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, email, password, first_name=firstname, last_name=lastname)
            user.save()
        except IntegrityError:
            return render(request, "onlineCourses/register.html", {
                "message": "Username already taken."
            })
        s = Student()
        s.user = user
        i = Instructor()
        i.user = user
        s.language = Language.objects.order_by("?").first()
        s.save()
        i.save()
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "onlineCourses/register.html")
