from django.db import models
from django.core.validators import MinLengthValidator

# Create your models here.

class Tag(models.Model):
  caption = models.CharField(max_length=20,null=True)
  
  def __str__(self):
      return f"{self.caption}"

class Author(models.Model):
    first_name = models.CharField(max_length=100,null=True)
    last_name = models.CharField(max_length=100,null=True)
    email_address = models.EmailField()

    def __str__(self):
        return f"{self.first_name}"


class Post(models.Model):
    title = models.CharField(max_length=150,null=True)
    excerpt = models.CharField(max_length=200,null=True)
    # image_name = models.CharField(max_length=100,null=True)
    #The place where you have to store the uploaded image(in this case posts folder in uploads folder)
    image=models.ImageField(upload_to="posts",null=True)
    date = models.DateField(auto_now=True,null=True)
    slug = models.SlugField(unique=True, db_index=True,null=True)
    content = models.TextField(validators=[MinLengthValidator(10)],null=True)
    author = models.ForeignKey(
        Author, on_delete=models.SET_NULL,null=True , related_name="posts")
    tags = models.ManyToManyField(Tag)


class Comments(models.Model):
    user_name=models.CharField(max_length=120)
    email=models.EmailField()
    body=models.TextField(max_length=400)

    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')