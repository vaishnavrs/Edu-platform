from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Faculty(AbstractUser):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    emailid = models.EmailField(max_length=100,unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    user_type = models.CharField(max_length=100,default='teacher')
    q_options = (
                ('Graduate','Graduate'),
                ('Post Graduate','Post Graduate'),
                ('Diploma','Diploma'),
                
    )
    qualification = models.CharField(max_length=100,choices=q_options,default='Graduate')
    subject_options = (('Computer Science','Computer Science'),
                        ('Electronics & Communications','Electronics & Communications'),
                        ('Electrical & Electronics','Electrical & Electronics'),
                        ('Mechanical','Mechanical'),
                        ('Civil','Civil'),
                        ('Chemical','Chemical'),
                        ('Physics','Physics'),
                        ('Mathematics','Mathematics'),
                        ('Chemistry','Chemistry'),
                        ('English','English'),
                        ('Hindi','Hindi'),
                        ('Economics','Economics'),
                        ('Commerce','Commerce'),
                        ('History','History'),
                        ('Geography','Geography'),
                        ('Political Science','Political Science'),
                        ('Sociology','Sociology'),
                        ('Psychology','Psychology'),
                        ('Botany','Botany'),
                        ('Zoology','Zoology'),
                        ('Microbiology','Microbiology'),
                        ('Biochemistry','Biochemistry'),
                        ('Biotechnology','Biotechnology'),
                        ('Agriculture','Agriculture'),
                        ('Home Science','Home Science'),
                        ('Physical Education','Physical Education'),
                        ('Sports','Sports'),    
                        ('Music','Music'),
                        ('Fine Arts','Fine Arts'),
                        ('Dance','Dance'),
                        ('Arts','Arts'),
                        ('Law','Law'),
                        ('Journalism','Journalism'),
                        ('Library Science','Library Science'),

    )
    subject = models.CharField(max_length=200,choices=subject_options,default='subject')
    status = ( ('Pending','Pending'),
                    ('Approved','Approved'),
                    ('Rejected','Rejected')              
    )
    
    verification = models.CharField(max_length=100,choices=status,default='Pending')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='faculty_user_set',
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='faculty_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.'
    )
    def __str__(self) -> str:
        return self.name

class Course(models.Model):

    faculty = models.ForeignKey(Faculty,on_delete=models.CASCADE)
    cat_options = (
        ('Development','Development'),
        ('Business','Business'),
        ('Finance and Accounting ','Finance and Accounting '),
        ('IT & Software','IT & Software'),
        ('Marketing','Marketing'),
        ('Photography','Photography'),
        ('Health and Fitness','Helath and Fitness'),
        ('Music','Music')
    )
    category = models.CharField(max_length=200,choices=cat_options,default='Choose Your Category')
    course_name = models.CharField(max_length=200)
    course_desc = models.CharField(max_length=5000)
    course_duration = models.IntegerField()
    course_fee = models.DecimalField(max_digits=10,decimal_places=2)
    syllabus = models.CharField(max_length=50000)
    course_image = models.ImageField(upload_to='course_image')

    def __str__(self) -> str:
        return  self.course_name



class CourseModule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    module_name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return  self.module_name


class Video(models.Model):
    course_module = models.ForeignKey(CourseModule, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    video = models.FileField(upload_to='videos/')



class Student(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    user_type = models.CharField(max_length =100,default='Student')
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='student_user_set',
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='student_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.'
    )
    course_enrolled = models.ForeignKey(Course,on_delete=models.CASCADE,null=True)


class Cart(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)

class Order(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending') 