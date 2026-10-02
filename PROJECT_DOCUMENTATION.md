# Connectly Project Documentation

## Purpose
Connectly is the user's CodeAlpha Full Stack Development Internship Task 2 social media platform.

## Requirements implemented
1. User Profiles — profile photo, username, name, bio, post/follower/following counts, edit profile, view posts, follow/unfollow.
2. Posts — text, image, video, link, poll, location, event/announcement, publish, username/avatar, date/time, delete own post, community feed.
3. Comments — write, submit, commenter name, time, display below post.
4. Likes — like/unlike, count, unique user/post like.
5. Follows — follow/unfollow, counts, cannot follow self.
6. Bookmarks — save/remove and Saved Posts page.
7. Community Challenges — current/past challenges, join, participant count, challenge-specific posts, duration, submission, completion.

## Authentication
Django built-in authentication provides login, registration, logout and protected actions. Login and registration include JavaScript show/hide password controls.

## Project structure
manage.py; requirements.txt; README.md; PROJECT_DOCUMENTATION.md; social_media/; social/; templates/; static/.

## Demo flow
Register → Login → Show/Hide Password → Create different post types → Like → Comment → Follow → Bookmark → Community Challenges → Join → Submit challenge post → Challenge Completed.

## Run
Activate venv, install requirements, run makemigrations, migrate, createsuperuser, and runserver. Use /admin/ to create challenges.
