"""Contact views."""
# -*-coding:utf8-*-
from datetime import datetime

from django.shortcuts import render_to_response, RequestContext, HttpResponse
from django.core.mail import send_mail

EMAIL_TEMPLATE = '''
[ 注意！這是一封由AjiBlog「自動寄發」的郵件 ]
+ 發送時間： {sent_time}
+ 發信人：   {sender}
+ Email：   {from_email}
+ 訊息內容：
{message}
'''


def contact(request):
    """Contact form handler."""
    if request.method == 'POST':
        from_email = request.POST['email']
        message = request.POST['message']
        name = request.POST['name']
        now = datetime.now().strftime('%Y年%m月%d號 %H點%M分%S秒')
        mail_content = EMAIL_TEMPLATE.format(
            sent_time=now,
            sender=name,
            from_email=from_email,
            message=message,
        )
        subject = 'AjiBlog 聯絡訊息'
        to_mail = ['amigcamel@gmail.com']
        send_mail(
            subject=subject,
            message=mail_content,
            from_email=from_email,
            recipient_list=to_mail,
            fail_silently=False,
        )
        return HttpResponse('ok')
    else:
        return render_to_response(
            'contact.html',
            {},
            context_instance=RequestContext(request)
        )
