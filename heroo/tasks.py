
from django.core.mail import send_mail
from privnoteApp import settings
from celery import Celery, shared_task
# from .heroo.views import is_date
from heroo.models import Note
import datetime
import pytz

timezonegaza = pytz.timezone('Asia/Gaza')


app = Celery()


@shared_task(name="send_feedback_email_task")
def send_feedback_email_task(email, name):
    """sends an email when feedback form is filled successfully"""
    print('hi*********************')

    send_mail('The note "' + name + '" has been read ',
              'his is an automatic notification to let you know that the note you created referred as "'
              + name + '" has been read and was destroyed immediately after.Do you want to send another note?',
              settings.EMAIL_HOST,
              [email])

    # @shared_task(name="send_feedback_email_task")
    # def send_feedback_email_task(email, message):
    #     """sends an email when feedback form is filled successfully"""
    #     send_mail('aaaaaaaaaa', message, settings.EMAIL_HOST, [email])


@app.task
def testa():
    print('@ app.taskdef testa(): hi')
    print("hiiiiiiiiii")
    return True
        
    

# return True
# this functhion
def is_date(noteOp=None): 
    # is_date = None
    #note.date_c.astimezone(timezonegaza).strftime("%Y-%m-%d %I:%M")
    try:
        # d1 = noteOp.date_c.astimezone(timezonegaza).strftime("%Y-%m-%d %I:%M")
        d2 = noteOp.self_d.strftime("%Y-%m-%d %I:%M")
        dNow = datetime.now().astimezone(timezonegaza).strftime("%Y-%m-%d %I:%M")
        # print('d1 '+ str(d1))
        # print('d2 '+ str(d2))
        # print('dNow ' + str(dNow))
        if dNow > d2:
            print(dNow > d2)
            print('is_date')
            return 1
        else:
            print('is_Not_date')  #
            return 2
    except:
        print('not_expt')
        return False
