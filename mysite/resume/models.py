from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ProfileCard(models.Model):
	"""
	Class to define developer's profile cards for the about section. This will
	be for all of our developers
	"""
	name = models.CharField(max_length=100, unique=True)
	skills = models.CharField(max_length=100, unique=False, blank=True)
	undergrad = models.CharField(max_length=100, unique=False, blank=True)
	grad = models.CharField(max_length=100, unique=False, blank=True)
	languages = models.TextField()
	summary = models.TextField()
	years_exp = models.IntegerField()

	# user's github / social media / website
	github = models.CharField(max_length=100, blank=True)
	twitter = models.TextField(blank=True)
	linkedin = models.TextField(blank=True)
	facebook = models.TextField(blank=True)
	website = models.TextField(blank=True)

	def __str__(self):
		"""Used in django admin site, to reference this object"""
		return self.name


class Post(models.Model):
	"""
	Class to define a post for each blog. This class will inherit from models
	which will provide an easy interface for connecting with the sqlite db

	The TextField() method will generate each post as HTML content 
	"""
	STATUS = (
		(0, "Draft"),
		(1, "Publish")
	)

	title = models.CharField(max_length=200, unique=True)
	slug = models.SlugField(max_length=200, unique=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
	updated_on = models.DateTimeField(auto_now=True)
	content = models.TextField()
	created_on = models.DateTimeField(auto_now_add=True)
	status = models.IntegerField(choices=STATUS, default=0)

	class Meta:
		# set the ordering to descending based on the created date
		ordering = ['-created_on']

	def __str__(self):
		"""Used in django admin site, to reference this object"""
		return self.title

# class Visualizations(models.Model):
# 	"""
# 	Class that defines visualizations generated for D3.js charts in HTML/CSS/Javscript
# 	This is a lightweight implementation for storing data related to certain visualizations we want
# 	to efficiently load when the user visits our website.
#
# 	Examples will involve things like:
# 		Data Science Visualizations
# 		Dashboards
# 		App Demos (iOS -> Django/D3.js/Python/HTML/CSS)
# 	"""
# 	title = models.CharField(max_length=200, unique=True)
# 	slug = models.SlugField(max_length=200, unique=True)  # slug = shorthand name for a specific entry in the sqlite db
# 	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
# 	updated_on = models.DateTimeField(auto_now=True)
# 	content = models.TextField()
# 	created_on = models.DateTimeField(auto_now_add=True)
# 	status = models.IntegerField(choices=STATUS, default=0)
#
# 	class Meta:
# 		# set the ordering to descending based on the created date
# 		ordering = ['-created_on']
#
# 	def __str__(self):
# 		"""Used in django admin site, to reference this object"""
# 		return self.title
