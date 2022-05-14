from django.http import QueryDict
from django.shortcuts import render
from django.core.mail import send_mail
# Create your views here.
from django.template.loader import render_to_string
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, api_view
from rest_framework.views import APIView
from django.core.mail import EmailMessage
import hashlib
from heroo.models import Note
from heroo.serializers import NoteSerializer
from rest_framework.response import Response
from heroo.utilities.aes_crypto import AESCipher
from privnoteApp import settings
from privnoteApp.settings import KEY_AES


class MarketingMeetingPagination(generics.ListAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


class NoteList(APIView):

    # def get(self, request, format=None):
    #     snippets = Note.objects.all()
    #     serializer = NoteSerializer(snippets, many=True)
    #     return Response(serializer.data)

    def post(self, request):
        print(request.data)
        Qdata = request.data
        # dataNote = request.data['note']
        # dataEmail = request.data['email']
        # dataPassword = request.data['password']
        # dataSelf_d = request.data['self_d']

        serializer = NoteSerializer(data=Qdata)
        if serializer.is_valid():
            # print(data)
            serializer.save()
            dataNote = request.data['note']
            print(dataNote)
            C = AESCipher(KEY_AES)
            d = C.encrypt(dataNote)
            print(Qdata)
            note = Note.objects.latest('id')
            note.note = d
            md5pass = hashlib.md5(note.password.encode())
            note.password = md5pass.hexdigest()
            note.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ' OPTIONS'])
def reNote(request, pk):
    ms = 'reNote scsses'
    C = AESCipher(KEY_AES)
    try:

        noteOp = Note.objects.get(note_id=pk)
        if not noteOp.is_d:
            d_note = noteOp.note
            # print(d_note)
            noted = C.decrypt(d_note)
            # print(noted)
            noteOp.is_d = False
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
                # email F hare
            if noteOp.password:
                ms += ' :: password'
                try:
                    pas = request.data['password']
                    md5pass = hashlib.md5(pas.encode())
                    pas = md5pass.hexdigest()
                    if noteOp.password == pas:
                        notee = noted
                    else:
                        return Response({'status': 'invalid password'}, status=status.HTTP_403_FORBIDDEN)
                except:
                    return Response({'status': 'p Enter Pass'}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({'status': 'Ple enter a password'}, status=status.HTTP_403_FORBIDDEN)
            if noteOp.self_d:
                ms += ' :: self_d'
            return Response({'status': ms, 'note': notee}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Note is d'}, status=status.HTTP_403_FORBIDDEN)
    except Note.DoesNotExist:
        return Response({'status': 'object not exists ! '}, status=status.HTTP_403_FORBIDDEN)
