"""Contact views."""
# -*-coding:utf8-*-
from datetime import datetime

from django.shortcuts import render_to_response, RequestContext, HttpResponse
from django.core.mail import send_mail
from django.conf import settings


EMAIL_TEMPLATE = '''
[ aji.tw 聯絡信 ]
• 發送時間： {sent_time}
• 發信人：   {sender}
• Email：   {from_email}
• 訊息內容：
{message}
'''


def contact(request):
    """Contact form handler."""
    if request.method == 'POST':
        from_email = request.POST['email']
        message = request.POST['message']
        name = request.POST['name']
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        mail_content = EMAIL_TEMPLATE.format(
            sent_time=now,
            sender=name,
            from_email=from_email,
            message=message,
        )
        send_mail(subject='aji.tw 聯絡訊息',
                  message=mail_content,
                  from_email=settings.EMAIL_HOST_USER,
                  recipient_list=['amigcamel@gmail.com'])
        return HttpResponse('ok')
    else:
        return render_to_response(
            'contact.html',
            {},
            context_instance=RequestContext(request)
        )
