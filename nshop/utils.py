from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class AppTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active)+text_type(user.pk)+text_type(timestamp))

token_generator = AppTokenGenerator()

def send_auth_mail(user, username, passw, email, request):
    
    domain = get_current_site(request).domain
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    link = reverse('activate', kwargs={'uidb64' : uidb64,
                   'token' : token_generator.make_token(user)}) 
    url =  'http://' + domain + link
    text_message = f"Hi {user}, you register on FuckingNakazShop.\n\
Your login - {user}\nYour password - {passw}\nPlease, visit next \
link to activate your account {url}"
    email = EmailMessage('Activation code', text_message, 'mediandrey@gmail.com',[email,])
    email.send()