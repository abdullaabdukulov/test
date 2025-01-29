# from django.contrib.auth import login, authenticate
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect

from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, FormView, UpdateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm, MessageForm
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.conf import settings


class MessageSendView(FormView):
    template_name = 'accounts/email-form.html'
    form_class = MessageForm
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        super().form_valid(form)
        # text_content = 'Bu oddiy matn versiyasi.'
        # html_content = """
        #     <h1>{}</h1>
        #     <p>{}</p>
        #     <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQasKPDCewT1v2j4mJjfCN1rqH2SczejiwkoA&s" width=400 height=500>
        # """.format(form.cleaned_data['subject'], form.cleaned_data['message'])
        #
        # email = EmailMultiAlternatives(form.cleaned_data['subject'], text_content, settings.EMAIL_HOST_USER, [form.cleaned_data['to_email']])
        # email.attach_alternative(html_content, 'text/html')
        # email.send()
        msg = f"Salom bu xabar {form.cleaned_data['from_email']} dan\n{form.cleaned_data['message']}"
        email = EmailMessage(
            form.cleaned_data['subject'],
            msg,
            settings.EMAIL_HOST_USER,
            [form.cleaned_data['to_email']]
        )
        email.send()
        # send_mail(
        #     subject=form.cleaned_data['subject'],
        #     message=msg,
        #     from_email=settings.EMAIL_HOST_USER,
        #     recipient_list=[form.cleaned_data['to_email']],
        #     fail_silently=True
        # )
        return HttpResponseRedirect(self.success_url)



class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response

class UserLoginView(FormView):
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        email = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        return self.form_invalid(form)

class ProfileView(LoginRequiredMixin, UpdateView):
    form_class = UserProfileForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self, queryset=None):
        return self.request.user.profile

# def signup(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('accounts:profile')
#     else:
#         form = CustomUserCreationForm()
#     return render(request, 'accounts/signup.html', {'form': form})
#
# def user_login(request):
#     if request.method == 'POST':
#         form = CustomAuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(email=email, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('accounts:profile')
#     else:
#         form = CustomAuthenticationForm()
#     return render(request, 'accounts/login.html', {'form': form})
#
# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, instance=request.user.profile)
#         if form.is_valid():
#             form.save()
#             return redirect('accounts:profile')
#     else:
#         form = UserProfileForm(instance=request.user.profile)
#     return render(request, 'accounts/profile.html', {'form': form})
#
