from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse




class Author(models.Model):

    author_user = models.OneToOneField(User, on_delete=models.CASCADE,)
    rating = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.all().aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.author_user.comment_set.all().aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat*3+cRat
        self.save()






class Category(models.Model):
    sport = 'SP'
    culture = 'CU'
    technologies = 'TE'
    science = 'SC'
    animals = 'AN'
    society = 'SO'

    CATEGORY = [
        (sport, 'Спорт'),
        (culture, 'Культура'),
        (technologies, 'Технологии'),
        (science, 'Наука'),
        (animals, 'Животные'),
        (society, 'Общество')
    ]

    name = models.CharField(max_length=2, choices=CATEGORY, default=society)


class Post(models.Model):

    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True)

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOCE =[
    (NEWS, 'Новость'),
    (ARTICLE, 'Статья')
    ]

    CategoryType = models.CharField(max_length=2, choices=CATEGORY_CHOCE, default=NEWS)
    date_time = models.DateTimeField(auto_now_add=True)
    heading = models.CharField(max_length=64)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    postCategory = models.ManyToManyField(Category, through='PostCategory')



    def __str__(self):
        return self.heading


    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


    def likes(self):
        self.rating +=1
        self.save()

    def dislikes(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123]+'...'

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)

    text = models.TextField(max_length=254)
    date_time = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0.0)

    def likes(self):
        self.rating +=1
        self.save()

    def dislikes(self):
        self.rating -= 1
        self.save()