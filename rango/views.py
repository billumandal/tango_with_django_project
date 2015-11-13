from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm


def index(request):
	# This is the dictionary to pass to the template engine as its context
	category_list = Category.objects.order_by('-likes')[:5]
	page_list = Page.objects.order_by('-views')[:5]
	context_dict = {'boldmessage': "I am bold font from the context",
					'categories': category_list,
					'pages': page_list,
					'topfivepages': page_list}

	visits = request.session.get('visits')
	if not visits:
		visits = 1
	reset_last_visit_time = False

	last_visit = request.session.get('last_visit')
	if last_visit:
		last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

		if (datetime.now() - last_visit_time).seconds > 0:
			visits = visits + 1
			reset_last_visit_time = True

	else:
		reset_last_visit_time = True

	if reset_last_visit_time:
		request.session['last_visit'] = str(datetime.now())
		request.session['visits'] = visits
	context_dict['visits'] = visits

	# Return a rendered response to send to the client 
	# We make use of the shortcut function to make our lives easier
	# Note that the first parameter is the template we wish to use
	return render(request, './rango/index.html', context_dict)

def about(request):

	if request.session.get('visits'):
		count = request.session.get('visits')
	else:
		count = 0
		
	context_dict = {'clueless': "I don't get why this dictionary needs to be here",
					'answertocontext': "Ok got this, this is to put various variables in the template by calling on the key",
					'whataboutnontext': "But what to do if it's not a text, let's put aboutold via this dictionary",
					'aboutold': 'Press <a href="./aboutold/">Old About</a> to see page which uses HttpResponse of "django.http"',
					'nontextdoesntwork': "Ok this HTML above didn't work, will see when we go further.",
					'visits': count}

	return render(request, './rango/about.html', context_dict)

def aboutold(request):
	return HttpResponse("""
		Rango says here is the about page
		<br><br><br>
		Press <a href="..">here</a> to go back to home page. <br />
		Press <a href="../about">here</a> to go to about page.
		""")

def category(request, category_name_slug):
	context_dict = {}

	try:
		# Can we find a category name slug with the given name?
		# If we can't, the .get() method raises a DoesNotExist exception.
		# So the .get() method returns one model instance or raises an exception
		category = Category.objects.get(slug=category_name_slug)
		context_dict['category_name'] = category.name
		context_dict['category_name_slug'] = category_name_slug

		# Retrieve all of the associated pages
		# Note that the filter returns >= 1 model instance.
		pages = Page.objects.filter(category=category)

		# Adds our results list to the template context under name pages.
		context_dict['pages'] = pages
		context_dict['category'] = category

	except Category.DoesNotExist:
		print "Nothing Happens"

	return render(request, './rango/category.html', context_dict)

def add_category(request):
	# A HTTP Post?
	if request.method == 'POST':
		form = CategoryForm(request.POST)

		# Have we been provided with a valid form?
		if form.is_valid():
			# Save the new category to the database.
			form.save(commit=True)
			# cat = form.save(commit=True)
			# print cat, cat.slug

			# Now call the index() view.
			# The user will be shown the homepage
			return index(request)
		else:
			# The supplied form contained errors - just print them to the terminal
			print form.errors
	else:
		# If the request was not a POST, display the form to enter details.
		form = CategoryForm()

	# Bad form (or form details), no form supplied ..
	# Render the form with error messages (if any).
	return render(request, './rango/add_category.html', { 'form': form })

def add_page(request, category_name_slug):
	
	try:
		cat = Category.objects.get(slug = category_name_slug)
	except Category.DoesNotExist:
		cat = None

	if request.method == 'POST':
		form = PageForm(request.POST)
		if form.is_valid():
			if cat:
				page = form.save(commit=False)
				page.category = cat
				page.views = 0
				page.save()
				# Better to use a redirect here
				return category(request, category_name_slug)
		else:
			print form_errors
	else:
		form = PageForm()

	context_dict = {'form': form, 'category': cat}

	return render(request, './rango/add_page.html', context_dict)

# def register(request):

# 	# A boolean value for telling the template whether the registration was successful.
# 	# Set to Fasle initially. Code changes value to True when registration succeeds.
# 	registered = False

# 	# if it's a HTTP POST, we're interested in processing form data.
# 	if request.method == 'POST':
# 		# Attempt to grab informaiton from the raw form information.
# 		# Note that we make use of both UserForm and UserProfileForm
# 		user_form = UserForm(data=request.POST)
# 		profile_form = UserProfileForm(data=request.POST)

# 		# If the two forms are valid...
# 		if user_form.is_valid() and profile_form.is_valid():
# 			# Save the user's form data to the database.
# 			user = user_form.save()

# 			# Now we hash the password with the set_password method.
# 			# Once hasehd, we can update the user object.
# 			user.set_password(user.password)
# 			user.save()

# 			# Now sort out the UserProfile instance.
# 			# Since we need to set the user attribute outselves, we set commit=False
# 			# This delays saving the model until we're ready to avoid integrity problems. 
# 			profile = profile_form.save(commit=False)
# 			profile.user = user 

# 			if 'picture' in request.FILES:
# 				profile.picture = request.FILES['picture']

# 			profile.save()
# 			registered = True

# 		else:
# 			print user_form.errors, profile_form.errors
	
# 	# If it's not a HTTP POST, then we render our form using two ModelForm instances.
# 	# These forms will be blank, ready for user input
# 	else:
# 		user_form = UserForm()
# 		profile_form = UserProfileForm()

# 	# Render the template depending upon the context.
# 	return render(request,
# 				'rango/register.html',
# 				{'user_form' : user_form, 'profile_form': profile_form, 'registered': registered})

# def user_login(request):

# 	if request.method == 'POST':
# 		username = request.POST.get('username')
# 		password = request.POST.get('password')

# 		user = authenticate(username=username, password=password)

# 		if user:
# 			if user.is_active:
# 				login(request, user)
# 				return HttpResponseRedirect('/rango/')
# 			else:
# 				return HttpResponseRedirect('Your Rango account is disabled')
# 		else:
# 			print "Invalid login details: {0}, {1}".format(username, password)
# 			# return HttpResponseRedirect("Invalid Login details supplied")
# 			return HttpResponseRedirect("/rango/login/")
# 			# return HttpResponse("Invalid login details: {0}, {1}".format(username, password))
# 	else:
# 		return render(request, 'rango/login.html', {})

@login_required
def restricted(request):
	# return HttpResponse("Since you're logged in, you can see this text! <br><br/> Btw I find it difficult why we've kept this page.")
	# Here I use the login_required() decorator to ensure only those logged in can access the view
	context_dict = {"newpagesetup": "Ok, this seems to be to practice setting up new pages.",
					"whathappens": "What happens if a dictionary is not given with the page?",
					"whythispage": "You can see this page cause it's to be seen only by logged in people."} 
	return render(request, './rango/restricted.html', context_dict)

# @login_required
# def user_logout(request):
# 	# Since we know the user is logged in, we can now just log them out.
# 	logout(request)

# 	# The the user back to homepage
# 	return HttpResponseRedirect('/rango/')

def base(request):
	context_dict = {"baseclass": "this is base template",}

	return render(request, './rango/base.html', context_dict)