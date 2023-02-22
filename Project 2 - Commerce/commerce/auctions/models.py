from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Max



class User(AbstractUser):
    pass



class Category(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return f'{self.name}'



class Listing(models.Model):
    title = models.CharField(max_length=25)
    description = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='listing')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listing')
    starter_price = models.IntegerField()
    current_price = models.IntegerField(null=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True)
    date_listed = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title}'



class Bid(models.Model):
    lot = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    price = models.IntegerField()
    date = models.DateTimeField(auto_now=True)
    final = models.BooleanField(default=False)

    def __str__(self):
        return f'Bid {self.id}: {self.bidder}-{self.lot}: {self.price}'
    


class Comment(models.Model):
    comment = models.CharField(max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    date_posted = models.DateTimeField(auto_now=True)



class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='watchlist')
