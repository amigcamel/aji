"""Contact views."""
# -*-coding:utf8-*-
from datetime import datetime

from django.shortcuts import render_to_response, RequestContext, HttpResponse
import requests

from .gmail import send_mail

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
        g = request.POST.get('g')
        resp = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            {
                'secret': '6LewJxMUAAAAALFRHD-2Fy1gqv-_ocr4ZpxitJcg',
                'response': g
            }
        )
        assert resp.status_code == 200
        g_response = resp.json()
        print('------------------------------------')
        print(g_response)
        print('------------------------------------')
        if not resp.json()['success']:
            return HttpResponse('error', status=401)
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
        send_mail(
            to='amigcamel@gmail.com',
            subject='aji.tw 聯絡訊息',
            message_text=mail_content,
        )
        return HttpResponse('ok')
    else:
        return render_to_response(
            'contact.html',
            {},
            context_instance=RequestContext(request)
        )
