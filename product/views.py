from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from product.models import CommentForm, Comment, Product


def index(request):
   return HttpResponse("My Product Page")


def addcomment(request, id):
   url = request.META.get('HTTP_REFERER')  # get last url
   
   # Ensure that the product exists
   product = get_object_or_404(Product, id=id)

   if request.method == 'POST':  # check post
      form = CommentForm(request.POST)
      if form.is_valid():
         data = Comment()  # create relation with model
         data.subject = form.cleaned_data['subject']
         data.comment = form.cleaned_data['comment']
         data.rate = form.cleaned_data['rate']
         data.ip = request.META.get('REMOTE_ADDR')
         data.product = product  # Link the comment to the product
         current_user = request.user
         data.user = current_user  # Assign the logged-in user to the comment
         data.save()  # save data to the table

         # Success message
         messages.success(request, "Your review has been sent. Thank you for your interest.")
         return HttpResponseRedirect(url)
      else:
         # Handle form errors
         messages.error(request, "There was an error with your submission. Please try again.")
         return HttpResponseRedirect(url)

   return HttpResponseRedirect(url)


def colors(request):
    return render(request, 'product_color.html')
