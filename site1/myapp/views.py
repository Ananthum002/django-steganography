import os
import traceback
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render, redirect

from . import steg as lsbsteg
from .models import User, Share


def time_in_millisecond():
    import time
    return str(int(time.time() * 1000))


def upload_file(my_file):
    """Saves the uploaded file and returns its absolute filesystem path."""
    fs = FileSystemStorage()
    extension = os.path.splitext(my_file.name)[1]
    filename = fs.save(time_in_millisecond() + extension, my_file)
    return fs.path(filename)


def to_media_url(abs_path):
    """Convert an absolute path under MEDIA_ROOT into a /media/... URL."""
    rel_path = os.path.relpath(abs_path, settings.MEDIA_ROOT)
    return settings.MEDIA_URL + rel_path.replace(os.sep, '/')


def get_current_user(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return None
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None


# ---------- Auth ----------

def login(request):
    if request.method == 'POST':
        username = request.POST.get('email', '').strip()
        password = request.POST.get('pass', '').strip()

        try:
            user = User.objects.get(username=username, password=password)
            request.session['user_id'] = user.id
            return redirect('index')
        except User.DoesNotExist:
            return render(request, 'login/index.html', {
                'message': 'Invalid username or password'
            })

    return render(request, 'login/index.html', {'message': ''})


def logout(request):
    request.session.flush()
    return redirect('login')


# ---------- Pages ----------

def index(request):
    if not get_current_user(request):
        return redirect('login')
    return render(request, 'index.html', {})


def encode(request):
    if not get_current_user(request):
        return redirect('login')
    return render(request, 'encode.html', {})


def decode(request):
    if not get_current_user(request):
        return redirect('login')
    return render(request, 'decode.html', {})


def share(request):
    user = get_current_user(request)
    if not user:
        return redirect('login')
    other_users = User.objects.exclude(id=user.id)
    return render(request, 'share.html', {'data': other_users})


def recieved(request):
    user = get_current_user(request)
    if not user:
        return redirect('login')
    shares = Share.objects.filter(shareTo=user)
    images = [s.imagelink for s in shares]
    return render(request, 'recieved.html', {'data': images})


# ---------- Encoding / Decoding ----------

def process_encoding_data(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'false', 'message': 'Invalid request method'}, status=405)

    try:
        cover_file = (
            request.FILES.get('coverimage') or
            request.FILES.get('encodeimg')
        )
        if not cover_file:
            return JsonResponse({'status': 'false', 'message': 'Please select a cover image'})

        coverimage_path = upload_file(cover_file)
        message = request.POST.get('message', '').strip() or 'no text found'

        stegImage = lsbsteg.encodeLSB(message, coverimage_path)
        if not stegImage:
            return JsonResponse({
                'status': 'false',
                'message': 'Encoding failed: message too large for this image'
            })

        location = to_media_url(stegImage)

        # 'to' is only present on the Share page. app.js sends the literal
        # string "undefined" when #to doesn't exist on the page (e.g. Encode
        # page), so guard with isdigit() rather than trusting truthiness.
        to_id = request.POST.get('to')
        if to_id and to_id.isdigit() and to_id != '0':
            user = get_current_user(request)
            if user:
                try:
                    recipient = User.objects.get(id=to_id)
                    rel_path = os.path.relpath(stegImage, settings.BASE_DIR).replace(os.sep, '/')
                    Share.objects.create(
                        shareTo=recipient,
                        sharedBy=user,
                        imagelink=rel_path
                    )
                except User.DoesNotExist:
                    pass

        return JsonResponse({'status': 'true', 'location': location})

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'status': 'false', 'message': f'Server error: {e}'}, status=500)


def process_decoding_data(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'false', 'message': 'Invalid request method'}, status=405)

    try:
        steg_file = request.FILES.get('stegimage')
        if not steg_file:
            return JsonResponse({'status': 'false', 'message': 'Please select an image to decode'})

        steg_path = upload_file(steg_file)
        message = lsbsteg.decodeLSB(steg_path)

        if message is None:
            return JsonResponse({'status': 'false', 'message': 'No hidden message found in this image'})

        return JsonResponse({'status': 'true', 'message': message})

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'status': 'false', 'message': f'Server error: {e}'}, status=500)


def decode_image_url(request):
    image = request.GET.get('image')
    if not image:
        return JsonResponse({'status': 'false', 'message': 'No image specified'})

    try:
        image_path = os.path.join(settings.BASE_DIR, image)
        message = lsbsteg.decodeLSB(image_path)
        if message is None:
            return JsonResponse({'status': 'false', 'message': 'No hidden message found'})
        return JsonResponse({'status': 'true', 'message': message})
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'status': 'false', 'message': f'Server error: {e}'}, status=500)