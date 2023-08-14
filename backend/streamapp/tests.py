from django.test import TestCase
from hashlib import sha256
import os
import pandas as pd
import joblib

print(sha256('get_user'.encode()).hexdigest())
print(sha256('reg_user'.encode()).hexdigest())
print(sha256('edit_user'.encode()).hexdigest())
print(sha256('send_otp'.encode()).hexdigest())
print(sha256('change_password'.encode()).hexdigest())
print(sha256('add_movie'.encode()).hexdigest())
print(sha256('del_movie'.encode()).hexdigest())
print(sha256('get_rec'.encode()).hexdigest())
print(sha256('get_movie'.encode()).hexdigest())
print(sha256('get_movie_path'.encode()).hexdigest())
print(sha256('get_rec_for_movie'.encode()).hexdigest())
print(sha256('search_res'.encode()).hexdigest())
print(sha256('user_movie'.encode()).hexdigest())
print(sha256('get_subs'.encode()).hexdigest())
print(sha256('get_movies_user'.encode()).hexdigest())