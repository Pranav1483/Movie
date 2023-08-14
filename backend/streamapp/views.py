from streamapp.serializers import UserSerializer, MovieSerializer
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from streamapp.models import User, Movie
from rest_framework.decorators import api_view
import json
from hashlib import sha256
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse, FileResponse
from django.core.exceptions import ValidationError
import random
from collections import Counter
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib
import os
from imdb import IMDb, IMDbDataAccessError
import logging
import re
from urllib.parse import quote
from wsgiref.util import FileWrapper

def recommend(movie_ids, n):
    DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    df_processed = pd.read_csv(DATA_DIR + '\processed_data.csv')
    countVectorizer = joblib.load(DATA_DIR + '\countVectorizer-model.pkl')
    tfIdfVectorizer = joblib.load(DATA_DIR + '/tfIdfVectorizer-model.pkl')
    matrix1 = countVectorizer.transform(df_processed['companies'])
    matrix2 = countVectorizer.transform(df_processed['cast'] + ' ' + df_processed['director'])
    matrix3 = countVectorizer.transform(df_processed['country codes'] + ' ' + df_processed['language codes'])
    matrix4 = tfIdfVectorizer.transform(df_processed['plot'] + ' ' + df_processed['genres'])
    grp = Counter()
    movie_ids = list(map(lambda x: int(x), movie_ids))
    for x in movie_ids:
        try:
            idx = df_processed.loc[df_processed['imdbID'] == x].index[0]
            cosine_sim1 = cosine_similarity(matrix1, matrix1)
            sim_scores1 = list(enumerate(cosine_sim1[idx]))
            sim_scores1 = sorted(sim_scores1, key=lambda x: x[1], reverse=True)
            cosine_sim2 = cosine_similarity(matrix2, matrix2)
            sim_scores2 = list(enumerate(cosine_sim2[idx]))
            sim_scores2 = sorted(sim_scores2, key=lambda x: x[1], reverse=True)
            cosine_sim3 = cosine_similarity(matrix3, matrix3)
            sim_scores3 = list(enumerate(cosine_sim3[idx]))
            sim_scores3 = sorted(sim_scores3, key=lambda x: x[1], reverse=True)
            cosine_sim4 = cosine_similarity(matrix4, matrix4)
            sim_scores4 = list(enumerate(cosine_sim4[idx]))
            sim_scores4 = sorted(sim_scores4, key=lambda x: x[1], reverse=True)
            w1, w2, w3, w4 = 0.5, 0.8, 0.1, 1
            sim_scores1, sim_scores2, sim_scores3, sim_scores4 = {key: w1*value for key, value in sim_scores1}, {key: w2*value for key, value in sim_scores2}, {key: w3*value for key, value in sim_scores3}, {key: w4*value for key, value in sim_scores4}
            d = Counter(dict(sim_scores1)) + Counter(dict(sim_scores2)) + Counter(dict(sim_scores3)) + Counter(dict(sim_scores4))
            grp += d
        except:
            pass
    res = sorted(grp.items(), key=lambda x: x[1], reverse=True)
    movie_indices = [i[0] for i in res]
    if not movie_indices:
        return []
    movies = list(df_processed.iloc[movie_indices]['imdbID'])
    ret_movies = []
    cntr = 0
    for idx in movies:
        if idx not in movie_ids:
            ret_movies.append(df_processed.loc[df_processed['imdbID'] == idx, 'long imdb title'].values[0])
            cntr += 1
            if cntr >= n:
                break
    return ret_movies

@api_view(['POST'])
def get_user(request):
    data = json.loads(request.body.decode('utf-8'))
    username = data['username']
    password = data['password']
    status = data['status']
    if status == 'no':
        try:
            user = User.objects.get(username=username)
            userSerializer = UserSerializer(user).data
            return JsonResponse(userSerializer, status=200)
        except User.DoesNotExist:
            return HttpResponse(status=404)
    try:
        user = User.objects.get(username=username)
        if user.password == sha256(password.encode()).hexdigest():
            userSerializer = UserSerializer(user).data
            return JsonResponse(userSerializer, status=200)
        else:
            return HttpResponse(status=401)
    except User.DoesNotExist:
        return HttpResponse(status=404)

@api_view(['POST'])
def reg_user(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        user = User(fname=data['fname'],
                    lname=data['lname'],
                    email=data['email'],
                    username=data['username'],
                    password=sha256(data['password'].encode()).hexdigest(),
                    DOB=data['DOB'],
                    likes=data['likes'],
                    watched=data['watched'],
                    watch_list=data['watch_list'])
        user.full_clean()
        user.save()
        return HttpResponse(status=204)
    except ValidationError as e:
        errors = {}
        for field, error in e.message_dict.items():
            errors[field] = ', '.join(error)
        field, error = next(iter(errors.items()))
        return HttpResponse(error, status=409)

@api_view(['POST'])
def edit_user(request):
    data = json.loads(request.body.decode('utf-8'))
    print(data)
    user = User.objects.get(username=data['username'])
    user.likes = data['likes']
    user.watched = data['watched']
    user.watch_list = data['watch_list']
    user.save()
    return HttpResponse(status=204)

@api_view(['POST'])
def send_otp(request):
    data = json.loads(request.body.decode('utf-8'))
    try:
        user = User.objects.get(email=data['email'])
        otp = str(random.randint(100000, 999999))
        send_mail('Reset Password', 'Here is your OTP to reset your password :\n' + otp, settings.EMAIL_HOST_USER, [user.email, ])
        return HttpResponse(otp, status=200)
    except User.DoesNotExist:
        return HttpResponse(status=404)

@api_view(['PUT'])
def change_password(request):
    data = json.loads(request.body.decode('utf-8'))
    user = User.objects.get(email=data['email'])
    user.password = sha256(data['password'].encode()).hexdigest()
    user.save()
    return HttpResponse(status=204)

@api_view(['POST'])
def add_movie(request):
    data = json.loads(request.body.decode('utf-8'))
    logging.getLogger("imdbpy").disabled = True
    try:
        obj = IMDb()
        movie = obj.get_movie(data['id'][2:])
        if 'movie' not in movie['kind']:
            return HttpResponse(status=422)
        movie_columns = ['imdbID', 'long imdb title', 'cast', 'genres', 'runtimes', 'country codes', 'language codes', 'year', 'director', 'rating', 'votes', 'production companies', 'full-size cover url', 'plot']
        j = {}
        for key in movie_columns:
            if key == 'cast':
                j['cast'] = list(map(lambda x: x['long imdb name'], movie['cast']))
            elif key == 'director':
                j['director'] = list(map(lambda x: x['long imdb name'], movie['director']))
            elif key == 'production companies':
                j['companies'] = list(map(lambda x: x['long imdb name'], movie['production companies']))
            elif key == 'runtimes':
                j['runtimes'] = int(movie['runtimes'][0])
            else:
                j[key] = movie[key]
        movie = Movie(*j.values())
        movie.full_clean()
        movie.save()
        return HttpResponse(status=204)
    except IMDbDataAccessError as e:
        if 'connection failed' in str(e):
            return HttpResponse(status=504)
        elif 'HTTPError 404' in str(e):
            return HttpResponse(status=404)
        else:
            return HttpResponse(status=500)
    except ValidationError as e:
        errors = {}
        for field, error in e.message_dict.items():
            errors[field] = ', '.join(error)
        field, error = next(iter(errors.items()))
        return HttpResponse(error, status=409)

@api_view(['DELETE'])
def del_movie(request, id):
    try:
        movie = Movie.objects.get(id=id[2:])
        movie.delete()
        return HttpResponse(status=204)
    except Movie.DoesNotExist:
        return HttpResponse(status=404)

@api_view(['POST'])
def get_rec(request):
    data = json.loads(request.body.decode('utf-8'))
    user = User.objects.get(username=data['username'])
    movie_list = [i for i in user.watched.keys() if user.watched[i] == '1']
    rec_movie_names = recommend(movie_list, 100)
    res = []
    for title in rec_movie_names:
        try:
            movie = Movie.objects.get(title=title)
            res.append({'title': movie.title, 'cover': movie.cover, 'id': movie.id, 'watch_list': user.watch_list.get(movie.id,'0'), 'liked': user.likes.get(movie.id, '0'), 'watched': user.watched.get(movie.id, '0')})
        except Movie.DoesNotExist:
            pass
    return JsonResponse(res, status=200, safe=False)

@api_view(['POST'])
def get_rec_for_movie(request):
    data = json.loads(request.body.decode('utf-8'))
    id = data['id']
    user = User.objects.get(username=data['username'])
    rec_movie_names = recommend([id], 20)
    res = []
    for title in rec_movie_names:
        try:
            movie = Movie.objects.get(title=title)
            res.append({'title': movie.title, 'cover': movie.cover, 'id': movie.id, 'watch_list': user.watch_list.get(movie.id,'0'), 'liked': user.likes.get(movie.id, '0'), 'watched': user.watched.get(movie.id, '0')})
        except Movie.DoesNotExist:
            pass
    return JsonResponse(res, status=200, safe=False)

@api_view(['GET'])
def get_movie(request, id):
    try:
        movie = Movie.objects.get(id=id)
        res = MovieSerializer(movie).data
        return JsonResponse(res, status=200)
    except Movie.DoesNotExist:
        return HttpResponse(status=404)

def parse_range_header(range_header):
    range_match = re.match(r'bytes=(\d+)-(\d*)', range_header)
    if range_match:
        start = int(range_match.group(1))
        end = int(range_match.group(2)) if range_match.group(2) else None
        return start, end
    else:
        raise ValueError('Invalid Range header')

@api_view(['GET'])
def get_movie_path(request, id):
    try:
        movie = Movie.objects.get(id=id)
        path_to_movie_folder = settings.MEDIA_PATH + '/' + re.sub(r'[<>:"/\\|?*]', '', movie.title)
        path_to_movie = ''
        path_to_subs = ''
        for file in os.listdir(path_to_movie_folder):
            if file.startswith('Movie'):
                path_to_movie = path_to_movie_folder + '/' + file
            elif file.startswith('subtitles'):
                path_to_subs = path_to_movie_folder + '/' + file
        if 'HTTP_RANGE' in request.META:
            range_header = request.META['HTTP_RANGE']
            start, end = parse_range_header(range_header)
            file_size = os.path.getsize(path_to_movie)
            if end is None:
                end = file_size - 1
            length = end - start + 1
            file = open(path_to_movie, 'rb')
            file.seek(start)
            response = FileResponse(FileWrapper(file), content_type='video/mp4', status=206)
            response['Content-Length'] = str(length)
            response['Content-Range'] = f'bytes {start}-{end}/{file_size}'
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(path_to_subs)
            response['X-Accel-Redirect'] = os.path.join(settings.MEDIA_URL, path_to_subs)
            return response
        return FileResponse(open(path_to_movie, 'rb'), content_type='video/mp4')
    except Movie.DoesNotExist:
        return HttpResponse(status=404)

@api_view(['POST'])
def search_res(request):
    data = json.loads(request.body.decode('utf-8'))
    id = data['id']
    user = User.objects.get(username=data['username'])
    res = []
    movies = Movie.objects.all().values()
    for movie in movies:
        if id in movie['title'].lower():
            res.append({'title': movie['title'], 'cover': movie['cover'], 'id': movie['id'], 'watch_list': user.watch_list.get(movie['id'],'0'), 'liked': user.likes.get(movie['id'], '0'), 'watched': user.watched.get(movie['id'], '0')})
    return JsonResponse(res, safe=False)

@api_view(['POST'])
def user_movie(request):
    data = json.loads(request.body.decode('utf-8'))
    user = User.objects.get(username=data['username'])
    id = data['id']
    target = data['target']
    value = "0"
    if data['value'] == "0":
        value = "1"
    if target == 'likes':
        obj = user.likes
    elif target == 'watch_list':
        obj = user.watch_list
    elif target == 'watched':
        obj = user.watched
    else:
        return HttpResponse(status=404)
    obj[id] = value
    if target == 'likes':
        user.likes = obj
    elif target == 'watch_list':
        user.watch_list = obj
    elif target == 'watched':
        user.watched = obj
    user.save()
    return HttpResponse(status=204)

@api_view(['GET'])
def get_subs(request, id):
    movie = Movie.objects.get(id=id)
    path_to_movie_folder = settings.MEDIA_PATH + '/' + re.sub(r'[<>:"/\\|?*]', '', movie.title)
    subtitle_filename = ''
    subtitle_filename = path_to_movie_folder + '/' + 'subtitles.vtt'
    subtitle_path = subtitle_filename
    print(subtitle_path)
    if os.path.exists(subtitle_path):
        response = FileResponse(open(subtitle_path, 'rb'), content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format('subtitles.vtt')
        return response
    return HttpResponse(status=404)

@api_view(['GET'])
def get_subs_temp(request, id):
    try:
        movie = Movie.objects.get(id=id)
        path_to_movie_folder = settings.MEDIA_PATH + '/' + re.sub(r'[<>:"/\\|?*]', '', movie.title)
        subtitle_filename = 'subtitles.srt'
        subtitle_path = path_to_movie_folder + '/' + subtitle_filename
        subtitles = []
        with open(subtitle_path, 'r') as srt_file:
            srt_content = srt_file.read()
        subtitle_entries = re.split(r'\n\s*\n', srt_content.strip())
        for entry in subtitle_entries:
            lines = entry.strip().split('\n')
            time_match = re.match(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})', lines[1])
            start_time = time_match.group(1)
            end_time = time_match.group(2)
            text = '\n'.join(lines[2:])
            subtitle = {
                'startTime': start_time,
                'endTime': end_time,
                'text': text,
            }
            subtitles.append(subtitle)
        return JsonResponse(subtitles, safe=False)
    except:
        return HttpResponse(status=404)
    
@api_view(['POST'])
def get_movies_user(request):
    data = json.loads(request.body.decode('utf-8'))
    username = data['username']
    target = data['target']
    try:
        user = User.objects.get(username=username)
        res = []
        if target == "likes":
            obj = user.likes
        elif target == "watch_list":
            obj = user.watch_list
        else:
            obj = user.watched
        for key in obj.keys():
            if obj[key] == "1":
                movie = Movie.objects.get(id = key)
                res.append({'title': movie.title, 'cover': movie.cover, 'id': movie.id, 'watch_list': user.watch_list.get(movie.id,'0'), 'liked': user.likes.get(movie.id, '0'), 'watched': user.watched.get(movie.id, '0')})
        return JsonResponse(res, safe=False)
    except:
        return HttpResponse(status=404)        