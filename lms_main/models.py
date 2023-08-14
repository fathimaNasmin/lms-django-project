from django.db import models
from PIL import Image



class Category(models.Model):
    """Model to store category of course"""
    name = models.CharField(max_length=80)
    icon = models.ImageField(null=True, blank=True, upload_to='icons/category/')

    def __str__(self):
        return f"Category {self.name}"

    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.icon:
            img = Image.open(self.icon.path)
            width, height = img.size
            
            desired_width = 300  # Your desired width
            desired_height = 300  # Your desired height

            if width > desired_width or height > desired_height:
                img.thumbnail((desired_width, desired_height))
                img.save(self.icon.path)
                self.icon_width = img.width
                self.icon_height = img.height
                self.save()