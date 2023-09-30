from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

#Create post message model

class Yeet(models.Model):
    user = models.ForeignKey(
        User, related_name="yeets",
        on_delete=models.DO_NOTHING
        )
    body = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="yeet_like", blank=True)

    #Count likes
    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return(
            f"{self.user}"
            f"({self.created_at:%Y-%m-%d %H:%M}): "
            f"{self.body}..."
            )

#Create user profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self',
        related_name='followed_by',
        symmetrical=False,
        blank=True)
    
    date_modified = models.DateTimeField(User, auto_now=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/")
    
    def __str__(self):
        return self.user.username

#Create profile when signUp
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        #User follow himself
        user_profile.follows.set([instance.profile.id])
        user_profile.save()
#another way would be:
#post_save.connect(create_profile, sender=User)