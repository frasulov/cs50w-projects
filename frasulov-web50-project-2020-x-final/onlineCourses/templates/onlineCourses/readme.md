# CS50W Final Project - Online Course System, like www.Udemy.com
# Github name: frasulov

# What I have used?

* I have created many django model in db
* fetch data in some .html pages
* Use Youtube API in order to get video information

## Tool and Languages

* Python Django
* Javascript
    * Jquery
    * React
    * OWL Carusel
* Bootstrap
* Semantic UI
* TinyMCE Editor
* Font Awesome
* Youtube API


# login.html

Login page

# register.html

Register page

# index.html

There are all course for each category
There are courses for last search result of the current user
There is an search bar for searching course

# editProfile.html

User can edit (firstname, lastname, status, language, about) of profile

# profile.html

User can click the any user's name and go the user's page
Public user profile for all users. Any user can find any user's information in that page
If user is instructor which means if the user create at least one course, the page will display instructor information(all created course) of the user else student information (all bought courses) of the user

# instructor.html

User can switch to the course create page and see all the course that current user created. User can switch to edit page of the any created course and delete the any course that created previously

# create.html

Create new course. Each course has these attributes:
    * Title
    * Subtitle
    * Image link
    * Level
    * Video Subtitle languages
    * Language
    * Message
    * Price
    * Category
    * Description
    * Created date
    * Updated date

# edit.html

User can edit all information of the course that entered while creating the course. And add content to the page. In the add content part, user can create and delete section and can create and delete lectures in the sections.

# mycourses.html

In the mycourses.html, there are 3 section. Wihslist courses, bought courses and card courses.
In the card, user can apply the coupon to the course, and checkout the course. In the card, user can remove course from card or move course to wishlist.

# payment.html

If user come to payment page from the buy now button, there will be only one course in detail else if, user come to payment page from card, there will be all courses that exist in the card.
If price is 0, after applying coupon, user can complete payment directly. Else, user can't complete the payment.


# course.html

There are all information about the specific course. There is an also content of the course. All sections, lectures and lecture video durations exist in the part. 
User can add the course to wishlist and unwishlist the course.
User can add the course to the card or buy directly.
In the bottom of the page, there are all reviews of the course

# search.html

After searching, user will see all search result in this page. And can play with result which means user can filter the result by language, level and category.

# coursecontent.html

User can come to the page if user bought the course or created the course .User can see all content of the course and watch videos in the lectures. There is an also answer question part. User can ask a new question or reply to the existing question. Finally, user can rate the course. Each user can rate the one course only once.

# rate.html

User choose the star for rating and add comment for review.




## Specification
 
* All Users are both student and instructor
    * Students are able to take courses
    * Instructors are able to create course
    * It means any user can take the couse and also create the course for public
    * After registration, user can add extra information to him/her profile
* User can add the course to wishlist from course page and also from card and also unwishlist the course
* User can add the course to card and also remove from card
* User can apply coupon in the card
* User can but the course directly
* In the course page, there are all course information and course content titles
* When buy the course, user can able to see content of the course
* There is an Q&A part in the content page, User can ask new question and add reply to the exist questions
* After buying the course, user is able to rate the course
* User is able to search the course
    * After searching, user can filter the search result

### Create The Course

* User is able to create the course. The course has attributes that are below:
    * Title
    * Subtitle
    * ImageLink
    * Level
    * Subtitle Language of Course lecture video (multiple choice)
    * Message
    * Price, if price is 0, it means course is free
    * Language
    * Category
    * Description
    * Creation date
    * Updated date
* After create the course, user can add the content to course
    * Can create many Sections
        * Section has a title
    * Each lecture has a many Lectures
        * Lecture has a title and youtube video id


### Timestamps:

* (0:00) - Register and complete user profile
* (0:32) - Create Course
* (1:09) - Edit and Add content to Course
* (2:02) - Search and filter search result
* (2:48) - Wishlist, Unwishlist and wishlist page
* (3:02) - Add to card
* (3:20) - Checkout, Apply coupon and payment
* (3:43) - Course Content
* (3:57) - Q&A
* (4:29) - Rate
* (5:15) - Mobile Responsive


