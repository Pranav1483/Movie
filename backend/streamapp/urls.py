from django.urls import path
from . import views

urlpatterns = [
    path('bf1e2a1a0e5ed9da4b836e8d75d490d13e3ae8d46ae048bc961f7bfb358416b3/', views.get_user, name='get_user'),
    path('efc15bcefb949f752816a2581bd50e73cd519f0335af98c5f3147041af440db9/', views.reg_user, name='reg_user'),
    path('75c176a60370bae8ad556e416ff53722e61adf01a54a5febfe31e7c49fd443a9/', views.edit_user, name='edit_user'),
    path('d80917ad9f6bb5a07c5c385b6cd80bbc9add75fb8f2be02b9a2886f7f8830080/', views.send_otp, name='send_otp'),
    path('1edc89fdde56d7d70adbfce09c10409cafca6e0316d6f0ba47787b0a3faf8e15/', views.change_password, name='change_password'),
    path('0d304f45648599acb97c52716a4e90a4d01285548071ff51301ca7de791f7034/', views.add_movie, name='add_movie'),
    path('8b91e5cff5d1e8ce83993c681b0f917bd3a2d9255f8eef7ff345936fa149888a/<id>', views.del_movie, name='del_movie'),
    path('96988ddb6e64fa47529930795dd84106d948b6da215e0836406cac7574f72a24/', views.get_rec, name='get_rec'),
    path('e4160e2ceae9b331c2208cd92e29c67fe8177795eb337338b93ac7ee0cadd99b/<id>', views.get_movie, name='get_movie'),
    path('98eb11b4c48e22645a9fa336a2bb9989aa53ddea634bc80b6e732a3b8d84a0bd/<id>', views.get_movie_path, name='get_movie_path'),
    path('aaa121090b1fd7761e5408638ed7f186f751f93b4a60c6ff197fc568bcd18766/', views.get_rec_for_movie, name='get_rec_for_movie'),
    path('d865f867710aa8df79171f697b072356f768b934a1bc1c648263eedfdf259201/', views.search_res, name='search_res'),
    path('523a5039c4785c323b530f27de38794b44559b2bbd2c00e3f0e67e4c5438137a/', views.user_movie, name='user_movie'),
    path('257f0036b086851f30acc4850ac4ea1ab4904a126cd9710d5177d4dbe16ba226/<id>', views.get_subs, name='get_subs'),
    path('61e98b8eeb5ad0d3ad9338ddfe0ee35b7535929e9a6084fac92742858e1bba84/', views.get_movies_user, name='get_movies_user'),
]