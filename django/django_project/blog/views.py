from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
#from .models import Roll
from .yazee import dice

def home(request):
	context = {
		'posts': Post.objects.all()
	}
	return render(request, 'blog/home.html', context)


def about(request):
	return render(request,'blog/about.html', {'title':'About'})


def yazee(request):
	dice1 = dice()
	dice2 = dice()
	dice3 = dice()
	dice4 = dice()
	dice5 = dice()
	dice6 = dice()
	cup = {'dice1' : dice1.roll() , 
		'dice2' : dice2.roll() ,
		'dice3' : dice3.roll() ,
		'dice4' : dice4.roll() ,
		'dice5' : dice5.roll() , 
		'dice6' : dice6.roll() ,}

	return render(request, 'blog/yazee.html', cup)
