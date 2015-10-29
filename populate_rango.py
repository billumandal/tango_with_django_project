import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')
# How to put this file in .gitignore
import django
django.setup()

from rango.models import Category, Page

def populate():
	python_cat = add_cat(name = 'Python',
						views = 64,
						likes = 32,
						)

	add_page(cat=python_cat,
		title="Official Python Tutorial",
		url="http://docs.python.org/2/tutorial/",
		views = 365)

	add_page(cat=python_cat,
		title="How to think like a computer scientist",
		url="http://www.greenteapress.com/thinkpython",
		views = 27)

	add_page(cat=python_cat,
		title="Learn Python in 10 minutes",
		url="http://www.korokithakis.net/tutorials/python/",
		views = 23)

	django_cat = add_cat(name = "Django",
						views = 32543,
						likes = 23)

	add_page(cat=django_cat,
		title="Official Django Tutorial",
		url="http://docs.djangoproject.com/en/1.5/intro/tutorial01",
		views = 58)

	add_page(cat=django_cat,
		title="Django Rocks",
		url="http://www.djangorocks.com/",
		views = 56)

	add_page(cat=django_cat,
		title="How to Tango with Django",
		url="http://www.tangowithdjango.com/",
		views = 434)

	frame_cat = add_cat(name = "Other Frameworks",
						views = 45,
						likes = 4)

	add_page(cat=frame_cat,
		title="Bottle",
		url="http://bottlepy.org/docs/dev/",
		views = 19)

	add_page(cat=frame_cat,
		title="Flask",
		url="http://flask.pocoo.org",
		views = 24)

# Print out what we've added to the user.
	for c in Category.objects.all():
		for p in Page.objects.filter(category=c):
			print "- {0} - {1}".format(str(c), str(p))

def add_page(cat, title, url, views=0):
	p = Page.objects.get_or_create(category=cat, title=title)[0]
	p.url = url
	p.views = views
	p.save()
	return p

def add_cat(name, views=23, likes=17):
	c = Category.objects.get_or_create(name=name)[0]
	c.views = views
	c.likes = likes
	c.save()
	return c

# Start execution here
if __name__ == '__main__':
	print "Starting Rango Population script...."
	populate()
