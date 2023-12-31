from django.db import models
from user.models import Student

# Create your models here.


class EnrolledCourses(models.Model):
    """model for enrolled courses by students"""
    # ========FOREIGN KEY AND RELATIONSHIPS=======#
    course = models.ForeignKey(
        "instructor.Course", on_delete=models.CASCADE)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE)

    def __str__(self):
        return f"Course Enrolled {self.course.title}-{self.student}"

    class Meta:
        # Ensure that each combination of course and student is unique
        unique_together = ('course', 'student')


class SaveForLater(models.Model):
    """model for save for later feature"""
    saved_at = models.DateTimeField(auto_now_add=True)
    # ========FOREIGN KEY AND RELATIONSHIPS=======#
    course = models.ForeignKey(
        "instructor.Course", on_delete=models.CASCADE)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.course.title}"

    class Meta:
        unique_together = ('course', 'student')


class Cart(models.Model):
    """model to store the courses added to cart"""
    # ========FOREIGN KEY AND RELATIONSHIPS=======#
    course = models.ForeignKey(
        "instructor.Course", on_delete=models.CASCADE)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart {self.course.title}"

    class Meta:
        unique_together = ('course', 'student')
        

class Order(models.Model):
    """model to store details of order"""
    order_no = models.CharField(max_length=200, default=0, unique=True)
    total_price = models.IntegerField(null=True, default=0)
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    pdf_receipt = models.FileField(
        upload_to='receipts/', null=True, blank=True)
    # ========FOREIGN KEY AND RELATIONSHIPS=======#
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order No:{self.order_no}"


class OrderItems(models.Model):
    """model for storing items in the order"""

    item_price = models.IntegerField(null=True, default=0)
    # ========FOREIGN KEY AND RELATIONSHIPS=======#
    course = models.ForeignKey(
        "instructor.Course", on_delete=models.CASCADE)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, default=2)

    def __str__(self):
        return f"Order Item by {self.order.student}-{self.course} in the {self.order}"

    class Meta:
        unique_together = ('course', 'order', 'student')


class PlayingVideo(models.Model):
    """Keep track of playing video"""
    pause_time = models.FloatField(null=True, blank=True)
    updated_time = models.DateTimeField(auto_now_add=True)
    # ======FOREIGN KEY AND RELATIONSHIPS=======
    course = models.ForeignKey(
        "instructor.Course", on_delete=models.CASCADE)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(
        "instructor.Lesson", on_delete=models.CASCADE)
    video = models.ForeignKey("instructor.Video", on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('course', 'student', 'lesson', 'video')


# Store videos that are already watched
class WatchedVideo(models.Model):
    completed_time = models.DateTimeField(auto_now_add=True)
    # ======FOREIGN KEY AND RELATIONSHIPS=======
    course = models.ForeignKey(
        "instructor.Course", on_delete=models.CASCADE)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(
        "instructor.Lesson", on_delete=models.CASCADE)
    video = models.ForeignKey("instructor.Video", on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Watched Video - {self.course.title}-{self.video.title}"
    
    class Meta:
        unique_together = ('course', 'student', 'lesson', 'video')
    