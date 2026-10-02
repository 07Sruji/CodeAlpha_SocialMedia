from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
class Profile(models.Model):
 user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
 bio=models.TextField(blank=True)
 profile_image=models.ImageField(upload_to="profiles/",blank=True,null=True)
 def __str__(self): return self.user.username
class Challenge(models.Model):
 title=models.CharField(max_length=200)
 description=models.TextField()
 start_date=models.DateTimeField(default=timezone.now)
 end_date=models.DateTimeField()
 is_active=models.BooleanField(default=True)
 def __str__(self): return self.title
 @property
 def participant_count(self): return self.participants.count()
class Post(models.Model):
 TYPES=[("text","Text"),("image","Image"),("video","Video"),("link","Link"),("poll","Poll"),("location","Location"),("event","Event / Announcement")]
 user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="posts")
 post_type=models.CharField(max_length=20,choices=TYPES,default="text")
 content=models.TextField(blank=True)
 image=models.ImageField(upload_to="posts/images/",blank=True,null=True)
 video=models.FileField(upload_to="posts/videos/",blank=True,null=True)
 link_url=models.URLField(blank=True)
 link_title=models.CharField(max_length=200,blank=True)
 location_name=models.CharField(max_length=200,blank=True)
 event_title=models.CharField(max_length=200,blank=True)
 event_date=models.DateTimeField(blank=True,null=True)
 event_location=models.CharField(max_length=200,blank=True)
 challenge=models.ForeignKey(Challenge,on_delete=models.SET_NULL,null=True,blank=True,related_name="posts")
 created_at=models.DateTimeField(auto_now_add=True)
 class Meta: ordering=["-created_at"]
class PollOption(models.Model):
 post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="poll_options")
 text=models.CharField(max_length=200)
class PollVote(models.Model):
 user=models.ForeignKey(User,on_delete=models.CASCADE)
 option=models.ForeignKey(PollOption,on_delete=models.CASCADE,related_name="votes")
 class Meta: constraints=[models.UniqueConstraint(fields=["user","option"],name="unique_poll_vote")]
class Comment(models.Model):
 user=models.ForeignKey(User,on_delete=models.CASCADE)
 post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")
 content=models.TextField()
 created_at=models.DateTimeField(auto_now_add=True)
 class Meta: ordering=["created_at"]
class Like(models.Model):
 user=models.ForeignKey(User,on_delete=models.CASCADE)
 post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="likes")
 class Meta: constraints=[models.UniqueConstraint(fields=["user","post"],name="unique_like")]
class Follow(models.Model):
 follower=models.ForeignKey(User,on_delete=models.CASCADE,related_name="following")
 following=models.ForeignKey(User,on_delete=models.CASCADE,related_name="followers")
 class Meta: constraints=[models.UniqueConstraint(fields=["follower","following"],name="unique_follow")]
class Bookmark(models.Model):
 user=models.ForeignKey(User,on_delete=models.CASCADE)
 post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="bookmarks")
 class Meta: constraints=[models.UniqueConstraint(fields=["user","post"],name="unique_bookmark")]
class ChallengeParticipant(models.Model):
 challenge=models.ForeignKey(Challenge,on_delete=models.CASCADE,related_name="participants")
 user=models.ForeignKey(User,on_delete=models.CASCADE)
 class Meta: constraints=[models.UniqueConstraint(fields=["challenge","user"],name="unique_challenge_participant")]
class ChallengeSubmission(models.Model):
 challenge=models.ForeignKey(Challenge,on_delete=models.CASCADE)
 user=models.ForeignKey(User,on_delete=models.CASCADE)
 post=models.OneToOneField(Post,on_delete=models.CASCADE,related_name="challenge_submission")
 class Meta: constraints=[models.UniqueConstraint(fields=["challenge","user"],name="unique_challenge_submission")]


 
