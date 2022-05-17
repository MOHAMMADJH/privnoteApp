import datetime

from django.http import QueryDict
from django.shortcuts import render
from django.core.mail import send_mail
# Create your views here.
from django.template.loader import render_to_string
from .tasks import send_feedback_email_task
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, api_view
from rest_framework.views import APIView
from django.core.mail import EmailMessage
import hashlib
from heroo.models import Note
from heroo.serializers import NoteSerializer
from rest_framework.response import Response
import datetime
from heroo.utilities.aes_crypto import AESCipher
from privnoteApp import settings
from privnoteApp.settings import KEY_AES


class MarketingMeetingPagination(generics.ListAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


class NoteList(APIView):

    """
        this Class save note and encrypt the note
        and return uuid fot this Note
    """

    def post(self, request):
        print(request.data)

        Qdata = request.data  # save request data in Qdata

        # save data whit serializer
        serializer = NoteSerializer(data=Qdata)
        if serializer.is_valid():
            serializer.save()

            # encrypt note AESCipher
            dataNote = request.data['note']
            C = AESCipher(KEY_AES)
            d = C.encrypt(dataNote)
            note = Note.objects.latest('id')  # get last Op from DB
            note.note = d  # save note encrypted on Note Op

            # md5 hash password encrypt
            if note.password:  # check if password is enter from user
                md5pass = hashlib.md5(note.password.encode())
                note.password = md5pass.hexdigest()
            note.save()  # save password hashed
            # end md5 code
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # end class


@api_view(['GET', ' OPTIONS'])
def reNote(request, pk):
    """

    """
    ms = 'reNote scsses'
    C = AESCipher(KEY_AES)

    try:
        noteOp = Note.objects.get(note_id=pk)
        if is_date(noteOp) == 1:
            noteOp.is_d = True
        if not noteOp.is_d:
            d_note = noteOp.note  # حفظ النوت
            # print(d_note)
            noted = C.decrypt(d_note)  # النوت غير مشقرة
            # print(noted)
            noteOp.is_d = True

            if is_password(noteOp, ms, request, noted) == 4:
                notee = noted
            elif is_password(noteOp, ms, request, noted) == 1:
                notee = noted
            else:
                return Response({'status': 'invalid password'}, status=status.HTTP_403_FORBIDDEN)
            noteOp.note = ''
            noteOp.save()
            is_email(noteOp,ms)
            return Response({'status': ms, 'note': notee}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Note is d'}, status=status.HTTP_403_FORBIDDEN)
    except Note.DoesNotExist:
        return Response({'status': 'object not exists ! '}, status=status.HTTP_403_FORBIDDEN)


def is_password(noteOp=None, ms=None, request=None, noted=None):
    print('is_password_no')
    if noteOp.password:
        print('is_password_yes')
        ms += ' :: password'
        try:
            pas = request.data['password']
            md5pass = hashlib.md5(pas.encode())
            pas = md5pass.hexdigest()
            if noteOp.password == pas:
                print('is_password_is_True')
                return 1  # is pass
            else:
                return 2  # is not pass
        except:
            return 3  # pass is ''
    else:
        return 4  # pass = Null


def is_email(noteOp=None, ms=None):
    if noteOp.email:
        if noteOp.note_name:
            ms += ' :: note_name'
        ms = 'email'
        if noteOp.note_name:
            name = noteOp.note_name
        else:
            name = 'Note'
        # send_mail('The note "' + name + '" has been read ',
        #           'his is an automatic notification to let you know that the note you created referred as "' + name + '" has been read and was destroyed immediately after.Do you want to send another note?',
        #           settings.EMAIL_HOST,
        #           [noteOp.email])
        send_feedback_email_task.delay(noteOp.email, name)


def is_date(noteOp=None):
    # is_date = None
    try:
        d1 = noteOp.date_c
        d2 = noteOp.self_d
        if d1 > d2:
            print(d1 > d2)
            print('is_date')
            return 1
        else:
            print('is_Not_date')  #
            return 2
    except:
        print('not_expt')
        return False
