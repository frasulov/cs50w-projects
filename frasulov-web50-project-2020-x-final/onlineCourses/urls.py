from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('course/<str:course_id>', views.course, name="course"),
    path('search', views.search, name='search'),
    path('profile/edit', views.editProfile, name="editProfile"),
    path('instuctor', views.instructorDasboard, name='instructor'),
    path('instuctor/create', views.createCourse, name='create'),
    path('instructor/course/<str:course_id>/edit', views.editCourse, name='editCourse'),
    path('delete/<str:course_id>', views.deleteCourse, name='deleteCourse'),
    path('mycourses/<str:which>', views.myCourses, name='mycourses'),
    path('card/<str:what>/<str:course_id>', views.FromCard, name='fromcard'),
    path('course/content/<str:course_id>', views.viewCourseContent, name='viewcoursecontent'),
    path('course/add/<str:course_id>', views.addcourse, name='addcourse'),
    path('user/<str:user_id>', views.userprofile, name='userprofile'),
    path('applycoupon', views.applyCoupon, name='coupon'),
    path("payment/completed", views.completePayment, name="completepayment"),
    path("payment/<str:type>", views.payment, name="payment"),
    path("rate/<str:course_id>", views.rate_view, name="rate"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),


    # Api paths
    path('instructor/course/<str:course_id>', views.getContent, name='coursecontent'),
    path('instructor/addsection/<str:course_id>', views.addSection, name='addsection'),
    path('instructor/deletesection/<str:section_id>', views.deleteSection, name='deletesection'),
    path('instructor/editsection/<str:section_id>', views.editSection, name='editsection'),
    path('instructor/addlecture/<str:section_id>', views.addLecture, name='addlecture'),
    path('instructor/deletelecture/<str:lecture_id>', views.deleteLecture, name='deletelecture'),
    path('course/addtocard/<str:course_id>', views.addToCard, name="addtocard"),
    path('course/content/lecture/<str:lecture_id>', views.getLecture, name="getlecture"),
    path('search/<str:query>', views.searchResult, name='searchresult'),
    path('course/togglewishlist/<str:course_id>', views.toggleWishlist, name="togglewishlist"),
    path("course/content/qa/<str:course_id>", views.getQA, name="qa"),
    path('course/content/addquestion/<str:course_id>', views.addQuestion, name='addquestion'),
    path('course/content/addanswer/<str:question_id>', views.addAnswer, name='addanswer')
]