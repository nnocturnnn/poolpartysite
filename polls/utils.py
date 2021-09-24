import pyqrcode
import png
from pyqrcode import QRCode
from PIL import Image
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
import os
import monobank
import datetime

class AppTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active)+text_type(user.pk)+text_type(timestamp))

token_generator = AppTokenGenerator()


def url_generate(user,request, types):
    domain = get_current_site(request).domain
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    if types == "reg":
        link = reverse('activate', kwargs={'uidb64' : uidb64,
                    'token' : token_generator.make_token(user)}) 
    else:
        link = reverse('buy', kwargs={'uidb64' : uidb64,
                    'token' : token_generator.make_token(user)}) 
    url =  'http://' + domain + link
    return url

def send_auth_mail(user, username, passw, email, request, types):
    text_message = f"Hi {user}, you register on PoolPartySite.\n\
Your login - {user}\nYour password - {passw}\nPlease, visit next \
link to activate your account {url_generate(user,request,types).replace('nakaz','polls')}"
    email = EmailMessage('Activation code', text_message, 'mediandrey@gmail.com',[email,])
    email.send()

def create_phys_ticket(link, email_to):
    paths = "static/polls/images/"

    url = pyqrcode.create(link)
    url.png(paths + 'myqr.png', scale = 6)
    front_img = Image.open(paths + '1.png')
    back_img = Image.open(paths + '2.png')
    qr = Image.open(paths + 'myqr.png')
    front_img.paste(qr, (1575, 100), qr)
    front_img.save("new_img.png")
    back_img.paste(qr, (100, 100), qr)
    back_img.save("new_img2.png")
    email = EmailMessage('Ticket', 'Your ticket', 'mediandrey@gmail.com',[email_to,])
    with open("polls/static/polls/images/new_img.png", "rb") as read_f:
        with open("polls/static/polls/images/new_img2.png", "rb") as read_s:
            filec = read_f.read()
            filec2 = read_s.read()
            email.attach("new_img.png", filec)
            email.attach("new_img2.png", filec2)
            email.send()
    os.remove("polls/static/polls/images/new_img.png")
    os.remove("polls/static/polls/images/new_img2.png")


def mono_check(username):
    token = 'uW7eDIX9HvtSmLNJWH_foBFQv6ojJgwurB4a0rJWK_5A'
    mono = monobank.Client(token)
    user_info = mono.get_client_info()
    id_w = ""
    for i in user_info['accounts']:
        if i['type'] == 'white':
            id_w = i['id']
    time_now = datetime.datetime.now()
    time_p = datetime.datetime.now() - datetime.timedelta(days=1)
    stat = mono.get_statements(id_w, time_p, time_now)
    last_tr = stat[0]
    # if 350 <= last_tr['amount'] / 100:
    #     if last_tr['comment'].lower() == username.lower():
    return True
    # return False





