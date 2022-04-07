from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.
import markdown
from datetime import datetime

from django.db.models import Sum


class User(AbstractUser):
    pass

# Not completed
class Student(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="student")
    language = models.ForeignKey('Language', blank=True, on_delete=models.CASCADE, related_name='l_students')
    course = models.ManyToManyField('Course', blank=True, related_name='students')
    wishlist = models.ManyToManyField('Course', blank=True, related_name='wishlist')
    card = models.ManyToManyField('Course', blank=True, related_name='card')
    payment = models.ManyToManyField('Payment', blank=True, related_name='students')
    last_search = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.user.first_name}"

class Instructor(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="instructor")
    status = models.CharField(max_length=255, blank=True)
    about = models.TextField(blank=True)
    student = models.ManyToManyField('Student',blank=True, related_name='instructors')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def getReview(self):
        total = 0
        average = 0.0
        for course in self.in_courses.all():
            total = total + course.review.all().count()
            for review in course.review.all():
                average = average + review.review

        if total == 0:
            average = 0
        else:
            average = round(average/total, 1)
        return {
            "total":total,
            "rate": average

        }

    def tomarkdown(self):
        return markdown.markdown(self.about)

    def getStudentCount(self):
        total = 0
        for course in self.in_courses.all():
            total = total + course.students.all().count()

        return total


class Level(models.Model):
    level_text = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.level_text}"

class Answer(models.Model):
    user = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='answers')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"{self.body}"

    def serialize(self):
        return {
            "id":self.id,
            "body": self.body,
            "user":{
                "id": self.user.user.id,
                "first_name": self.user.user.first_name,
                "last_name": self.user.user.last_name,
            },
            "created": self.created.strftime("%m/%d/%Y, %H:%M:%S")
        }


class Question(models.Model):
    user = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    answers = models.ManyToManyField('Answer',blank=True, related_name='questions')
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "user": {
                "id": self.user.user.id,
                "first_name": self.user.user.first_name,
                "last_name": self.user.user.last_name,
            },
            "answers": [answer.serialize() for answer in self.answers.all()],
            "created": self.created.strftime("%m/%d/%Y, %H:%M:%S")
        }

    def __str__(self):
        return f"{self.title}"

class Course(models.Model):
    content = models.ManyToManyField('Section', blank=True, related_name='courses')
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    image_link = models.CharField(max_length=255)
    description = models.TextField(default='## Requirements\n\n## Description\n\n## Who this course is for')
    instructor = models.ManyToManyField('Instructor', related_name='in_courses')
    level = models.ForeignKey('Level', on_delete=models.CASCADE, related_name='courses')
    language = models.ForeignKey('Language',on_delete=models.CASCADE, related_name='l_courses')
    price = models.FloatField()
    subtitle_language = models.ManyToManyField('Language',blank=True, related_name='my_courses')
    category = models.ForeignKey('Category',on_delete=models.CASCADE, related_name='courses')
    pubhlised = models.BooleanField(default=False)
    course_message = models.TextField(blank=True)
    created = models.CharField(max_length=255, default=datetime.today().strftime('%Y-%m-%d'))
    updated = models.CharField(max_length=255, default=datetime.today().strftime('%Y-%m-%d'))
    review = models.ManyToManyField('Review',blank=True, related_name='r_courses')
    aq = models.ManyToManyField('Question', blank=True, related_name='courses')

    def getRateCode(self):
        code = []
        rate = self.averageRate()
        if int(rate) == rate:
            tam_eded = True
        else:
            tam_eded = False

        if tam_eded:
            for i in range(int(rate)):
                code.append("+")
            for i in range(5-int(rate)):
                code.append("-")
        else:
            for i in range(int(rate)):
                code.append("+")
            code.append("?")
            for i in range(4-int(rate)):
                code.append("-")

        return code

    def averageRate(self):
        average = 0.0
        count = 0
        for review in self.review.all():
            average = average + review.review
            count = count + 1
        if count == 0:
            return 0
        else:
            return round(average/count, 1)

    def normalupdatedtime(self):
        return self.updated[:10]


    def getLectureCount(self):
        count = 0
        for section in self.content.all():
            for lecture in section.lecture.all():
                count = count + 1
        return count

    def getTotalHours(self):
        total = 0
        for section in self.content.all():
            for lecture in section.lecture.all():
                dot_index = lecture.video_duration.index(':')
                min = int(lecture.video_duration[0:dot_index])
                second = int(lecture.video_duration[dot_index + 1:])
                total = total + min * 60 + second

        if int(total / 3600) != 0:
            total_time_string = f"{int(total / 3600)} total hours"
        else:
            total_time_string = f"{int(total / 60)} total minutes"

        return total_time_string

    def __str__(self):
        return f"{self.title} {self.subtitle}"

    def tomarkdown(self):
        return markdown.markdown(self.description)

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "subtitle":self.subtitle,
            "image":self.image_link,
            "instructor": [f"{ins.user.first_name} {ins.user.last_name}" for ins in self.instructor.all()],
            "level": self.level.level_text,
            "price":self.price,
            "category": self.category.category,
            "lecturecount": self.getLectureCount(),
            "totaltime": self.getTotalHours(),
            "averageRate": self.averageRate(),
            "codeRate": self.getRateCode(),
            "totalRate":self.review.all().count(),
        }

class Category(models.Model):
    category = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.category}"


class Language(models.Model):
    language_text = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.language_text}"

class Review(models.Model):
    reviewer = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='reviews')
    review_text = models.TextField(blank=True)
    review = models.FloatField()
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def getRateCode(self):
        code = []
        if int(self.review) == self.review:
            tam_eded = True
        else:
            tam_eded = False

        if tam_eded:
            for i in range(int(self.review)):
                code.append("+")
            for i in range(5-int(self.review)):
                code.append("-")
        else:
            for i in range(int(self.review)):
                code.append("+")
            code.append("?")
            for i in range(4-int(self.review)):
                code.append("-")

        return code


    def getTime(self):
        return f"{self.created.strftime('%m/%d/%Y, %H:%M:%S')}"


class Filter(models.Model):
    language = models.ManyToManyField(Language,blank=True, related_name='filter')
    category = models.ManyToManyField(Category,blank=True, related_name='filter')
    level = models.ManyToManyField(Level,blank=True, related_name='filter')

class Section(models.Model):
    title = models.CharField(max_length=255)
    lecture = models.ManyToManyField('Lecture', blank=True, related_name='sections')

    def getTotalTime(self):
        total = 0
        for lecture in self.lecture.all():
            dot_index = lecture.video_duration.index(':')
            min = int(lecture.video_duration[0:dot_index])
            second = int(lecture.video_duration[dot_index + 1:])
            total = total + min * 60 + second

        total_time_string = ""
        if int(total / 3600) != 0:
            total_time_string = f"{int(total / 3600)} hours "
        if int(total / 60) != 0:
            total_time_string = f"{total_time_string}{int(total / 60)} min "
        if total % 60 != 0:
            total_time_string = f"{total_time_string}{total % 60} sec"

        return total_time_string

    def serialize(self):
        return {
            "id":self.id,
            "title":self.title,
            "lecture": [lec.serialize() for lec in self.lecture.all()]
        }

    def __str__(self):
        return f"{self.title}"

class Lecture(models.Model):
    title = models.CharField(max_length=255)
    video_link = models.CharField(max_length=255)
    video_duration = models.CharField(max_length=25, blank=True)

    def serialize(self):
        return {
            "id":self.id,
            "title":self.title,
            "video":self.video_link
        }

    def __str__(self):
        return f"{self.title}"


class Coupon(models.Model):
    name = models.CharField(max_length=64,unique=True, blank=True)
    percentage = models.FloatField(blank=True)

    def __str__(self):
        return f"{self.name}"

class Payment(models.Model):
    total_price = models.FloatField(default=0)
    coupon = models.ManyToManyField('Coupon', blank=True, related_name='payment')
    completed = models.BooleanField(default=False)
    created = models.CharField(max_length=64, default=datetime.today().strftime('%Y-%m-%d'))
    courses = models.ManyToManyField('Course', blank=True, related_name='payments')
    def __str__(self):
        return f"{self.total_price}"

    def applyDiscount(self):
        if self.coupon.all():
            coupon = self.coupon.all().last()
            self.total_price = self.total_price - self.total_price*self.coupon.all().first().percentage/100

    def roundedPrice(self):
        return round(self.total_price, 2)





