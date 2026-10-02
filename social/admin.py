from django.contrib import admin
from .models import *
admin.site.register([Profile,Post,PollOption,PollVote,Comment,Like,Follow,Bookmark,Challenge,ChallengeParticipant,ChallengeSubmission])
