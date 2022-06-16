import re
from collections import Counter
import random
import cv2
import face_recognition
from turtle import pen
from django.shortcuts import render
from .models import II,USER,SEANS,DATA_ALL_SEANSES
from django.http import Http404
from validate_email import validate_email
from .forms import UploadFileForm
from django.http import HttpResponseRedirect
from django.http import HttpResponse
grade_list = (
    [1, 'Тематический концерт']
    , [2, 'Спектакль']
    , [3, 'Концерная программа']
    , [4, 'Выставка']
    , [5, 'Театрализированное представление']
    , [6, 'Народное гуляние']
    , [7, 'Конкурс, смотр']
    , [8, 'Дискотека']
    , [9, 'Шествие']
    , [10, 'Кино']
)

# user_all = USER.objects.all()
# user_ii_all = II.objects.all()
# user_seans_all = SEANS.objects.all()
seans_all = DATA_ALL_SEANSES.objects.all()
for x in seans_all:
    x.class_seans_name = grade_list[x.class_seans-1][1]

def delete_None(mas):
    new_words = []
    for i in mas:
        if i != "":
            new_words.append(i)
    return new_words

def password_create(sours):
    import hashlib
    h = hashlib.sha1(f"{sours}".encode('utf-8'))
    h.digest()
    return h.hexdigest()
      
def checher(email,password):
    user_all_data = [f'{el.email}|{el.password}' for el in USER.objects.all()]
    print(password_create(password) )
    if email+"|"+password_create(password) in user_all_data:
        return [True,user_all_data.index(email+"|"+password_create(password))]
    else:
        return [False,'-']

def make_po_foto_code(img_str):
    import numpy as np
    img_str.seek(0)
    img_array = np.asarray(bytearray(img_str.read()), dtype=np.uint8)
    
    image = cv2.imdecode(img_array, 0) 
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb, model='hog')
    encodings = face_recognition.face_encodings(rgb, boxes)
    knownEncodings = []
    for encoding in encodings:
        knownEncodings.append(encoding)
    print('&'.join([str(x) for x in knownEncodings[0]]))
    return '&'.join([str(x) for x in knownEncodings[0]])

def index(request):
    
    if request.META['PATH_INFO'] == '/':
        
        MINE =  request.COOKIES.get('user','').split('/') 
        print(MINE)  
        if MINE != [''] or len(MINE)>1:
            info = checher(MINE[0],MINE[1])
            if info[0]:
                user = USER.objects.all()[info[1]]
                seans = SEANS.objects.all()[info[1]]
                like_cat = [int(x) for x in user.likes.split(',') if x] + [int(x.split('!')[-1]) for x in seans.seanses.split('|') if x] 
                user.loock_like = max(Counter(like_cat).items() ,key=lambda i : i[1],default=str(user.loock_like))[0]
                user.save()
                
                old = seans_all
                new = []
                for i in old.reverse():
                    print(grade_list[0])
                    
                    print(user.loock_like)
                    if i.class_seans == user.loock_like:
                        new.insert(0,i)
                    else:
                        new.append(i)
                for x in new:
                    x.class_seans_name = grade_list[x.class_seans-1][1]
        else:
            print('Eror')
            return render(request,'ProDos/index.html',{'seanses':seans_all})
        
        # Поработать с фото лица
        # Красивые ошибки 
        # Супер стараница 404 
        for x in new:
            x.class_seans_name = grade_list[x.class_seans-1][1]
        
        return render(request,'ProDos/index.html',{'seanses':new})
    
    elif request.META['PATH_INFO'] == '/eror404/':
        return render(request,'ProDos/eror404.html')
    
    elif request.META['PATH_INFO'] == '/merop/':
        MINE =  request.COOKIES.get('user','').split('/') 
        print(MINE)  
        if MINE != [''] or len(MINE)>1:
            info = checher(MINE[0],MINE[1])
            if info[0]:
                user = USER.objects.all()[info[1]]
                seans = SEANS.objects.all()[info[1]]
                like_cat = [int(x) for x in user.likes.split(',') if x] + [int(x.split('!')[-1]) for x in seans.seanses.split('|') if x] 
                user.loock_like = max(Counter(like_cat).items() ,key=lambda i : i[1],default=str(user.loock_like))[0]
                user.save()
                
                old = seans_all
                new = []
                for i in old.reverse():
                    print(grade_list[0])
                    
                    print(user.loock_like)
                    if i.class_seans == user.loock_like:
                        new.insert(0,i)
                    else:
                        new.append(i)
                for x in new:
                    x.class_seans_name = grade_list[x.class_seans-1][1]
        else:
            print('Eror')
            num = len(seans_all)//10 if  len(seans_all) >= 10 else 1 
            return render(request,'ProDos/merop_all.html',{'seanses':seans_all,'range':range(num )})
        num = len(new)//10 if  len(new) >= 10 else 1
        
        return render(request,'ProDos/merop_all.html',{'seanses':new,'range':range(num)})
    
    elif request.META['PATH_INFO'] == '/logout/':
        return render(request,'ProDos/logout.html')
    
    elif request.META['PATH_INFO'] == '/prof/my_ine/edit':
        
        MINE =  request.COOKIES.get('user','').split('/')   
        idis = int(MINE[2])
        
        try:

            uaser = USER.objects.all()[idis]
            ii = II.objects.all()[idis]
            try:
                seans = SEANS.objects.all()[idis]
            except:
                seans = []
        except:
            raise Http404('Тут нет ничего ')
        

        USER_SOURS = str(uaser).split('/')
        

        if password_create(MINE[1]) == USER_SOURS[2] and MINE[0] == USER_SOURS[1]:
            isMine = True
        else:
            isMine = False
        list_seans =[]
        if seans != []:
            list_seans = [x.split('!') for x in list(filter(None, str(seans.seanses).split('|')))]
        
            
        
        return render(request,'profile/edit.html',{'uaser':uaser,'ii':ii,'seans':seans,'isMine':isMine,'id':idis,'list_seans':list_seans})
    
    elif request.META['PATH_INFO'] == '/prof/my_ine/edit/save':
        MINE =  request.COOKIES.get('red','').split('/')  
        MINE_user =  request.COOKIES.get('user','').split('/')  
        idis = int(MINE[-1])
        
        try:

            uaser = USER.objects.all()[idis]
            ii = II.objects.all()[idis]
            try:
                seans = SEANS.objects.all()[idis]
            except:
                seans = []
        except:
            raise Http404('Тут нет ничего ')
        

        USER_SOURS = str(uaser).split('/')
        

        if password_create(MINE_user[1]) == USER_SOURS[2] and MINE_user[0] == USER_SOURS[1]:
            print(MINE)
            name = MINE[0] if MINE[0] != uaser.login else uaser.login
            sopose = MINE[1] if len(MINE[1]) >= 2 else uaser.sopose
            email = MINE[2] if MINE[2] != uaser.email else uaser.email
            
            password = password_create(MINE[3]) if len(MINE[3]) > 3 else uaser.password
            password_clear = MINE[3] if len(MINE[3]) > 3  else MINE_user[1]
            
            
            tipe_new =  False if MINE[4]=='0' else True if MINE[4] == '0' or MINE[4] == '1' else uaser.isGreen
            
        
            
            
            
            
            word = list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
            
            code_Face_id = str(random.randint(100000000,99999999999)) if  not ii.code.isdigit() else ii.code
            code_Phone_id = ''.join(random.sample(word, len(word))[:11]) if  ii.code.isdigit() else ii.code
            finish_tip = code_Face_id if tipe_new else code_Phone_id
            
            print(name,sopose,email,finish_tip,password,password_clear)
            uaser.login = name
            uaser.email = email
            uaser.sopose = sopose
            uaser.password = password
            uaser.isGreen = tipe_new
            ii.code = finish_tip
            uaser.save()
            ii.save()
            
            return render(request,'profile/save.html',{'email':email,'pass':password_clear,'id':idis})
        
    elif request.META['PATH_INFO'] == '/login/':
        if request.GET != {}:
            
            if validate_email(request.GET["email"]) and len(request.GET['password']) >=8:
                print('AC')
                ans = checher(request.GET['email'],request.GET['password'])
                if ans[0]:
                    print(request.GET['email']+'/'+request.GET['password']+'/'+str(ans[1]))
                    print(request.COOKIES) 
                    return render(request,'ProDos/setCoke.html',{'name':'user','cok':request.GET['email']+'/'+request.GET['password']+'/'+str(ans[1])})
            else:
                print('EROR')
              
        return render(request,'ProDos/login.html')
    
    elif request.META['PATH_INFO'] == '/reg/':
        print(request.GET)
        user = USER()
        ii = II(id_user=user)
        seans = SEANS(id_user=user)
        if request.method == 'POST':
            if 'face' in request.FILES:
                print(request.FILES)
                file = request.FILES['face']
                print(file)
                info = make_po_foto_code(file)
                # ... обработка лица
                ii.info_photo = info
                ii.code = str(random.randint(100000000,99999999999)) 
            if 'ico' in request.FILES:
                print(request.FILES)
                ico = request.FILES['ico']
                print(ico)
                # ... обработка лица
                user.ico = ico
        
        if request.GET!={}:
            
            form = UploadFileForm(request.GET, request.FILES)
            print(form.is_valid())
            
            name = request.GET['name']
            if name == '':
                print(1)
                return render(request,'ProDos/register.html',{'eror':"Name"})
            
            category = request.GET['category']
            
            age = -1 if not request.GET['age'].isdigit() else int(request.GET['age'])
            if age<=0 or age>= 125 or age == '':
                print(2)
                return render(request,'ProDos/register.html',{'eror':"age"})
            
            email = request.GET['email']
            if not validate_email(email):
                print(3)
                return render(request,'ProDos/register.html',{'eror':"age"})
            
            password = request.GET['password']
            confirmPassword = request.GET['confirmPassword']
            
            if len(password) < 8 or len(confirmPassword) < 8 :
                return render(request,'ProDos/register.html',{'eror':"<8"})
            elif password != confirmPassword:
                return render(request,'ProDos/register.html',{'eror':"!="})
            
            print('0k')
 
            user.login = name
            user.password = password_create(password)
            user.age = age
            user.email=email
            user.isGreen = True if category == '2' else False
            if age<18:
                user.sopose = '18'
            
            
            print(request.FILES=={})
            
            if category == '2' and not request.method == 'POST':
                return render(request,'ProDos/register2.html',{'category':category})
            elif category == '1' and request.FILES == {}:
                return render(request,'ProDos/register2.html',{'category':category})
            
            elif category == '1':
                code_Phone_id = ''.join(random.sample(list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'), 52))[:11] 
                ii.code = code_Phone_id

            if not checher(email,password)[0]:
                print('save')
                seans.seanses = ''
                user.save()
                ii.save()
                seans.save()
                
            return HttpResponseRedirect('../login')
        
        
             
        return render(request,'ProDos/register.html')
    
    elif request.META['PATH_INFO'] == '/prof/my_ine':
        MINE =  request.COOKIES.get('user','').split('/')   
        idis = int(MINE[2])
        
        try:

            uaser = USER.objects.all()[idis]
            ii = II.objects.all()[idis]
            try:
                seans = SEANS.objects.all()[idis]
            except:
                seans = []
        except:
            raise Http404('Тут нет ничего ')
            
        
        USER_SOURS = str(uaser).split('/')
        if password_create(MINE[1]) == USER_SOURS[2] and MINE[0] == USER_SOURS[1]:
            isMine = True
            myFrend = False
        else:
            isMine = False
            print(frends_id,checher(MINE[0],MINE[1])[1])
            myFrend = True if checher(MINE[0],MINE[1])[1] in frends_id else False
            print(myFrend)
        list_seans =[]
        if seans != []:
            list_seans = [x.split('!') for x in list(filter(None, str(seans.seanses).split('|')))]
        frends =[USER.objects.all()[int(x)] for x in delete_None(uaser.list_frends.split(','))]
        frends_id=[int(x) for x in delete_None(uaser.list_frends.split(','))]
        
        frends_new = [USER.objects.all()[int(x)] for x in delete_None(uaser.list_req_frends.split(','))]
        frends_req_id=[int(x) for x in delete_None(uaser.list_req_frends.split(','))]
        print(frends_id,'----')
        for i in range(len(frends)):
            frends[i].ids = frends_id[i]
        for i in range(len(frends_new)):
            frends_new[i].ids = frends_req_id[i]
            
        return render(request,'profile/profile.html',{'uaser':uaser,'ii':ii,'seans':seans,'isMine':isMine,'id':idis,'list_seans':list_seans,'frends_new':frends_new,'frends':frends,'prof_id':idis,'myFrend':myFrend})

        
    else:
        return HttpResponseRedirect('../eror404')


def detail2(request,prof_id):
    try:
        uaser = USER.objects.all()[prof_id]
        ii = II.objects.all()[prof_id]
        try:
            seans = SEANS.objects.all()[prof_id]
        except:
            seans = []
    except:
        raise Http404('Тут нет ничего ')
    

    USER_SOURS = str(uaser).split('/')
    MINE =  request.COOKIES.get('user','').split('/')    
    print(MINE)
    list_seans = []
    if seans != []:
        list_seans = [x.split('!') for x in list(filter(None, str(seans.seanses).split('|')))]
    
    print(list_seans)
    isMine = False
    
    frends =[USER.objects.all()[int(x)] for x in delete_None(uaser.list_frends.split(','))]
    frends_id=[int(x) for x in delete_None(uaser.list_frends.split(','))]
    
    frends_new = [USER.objects.all()[int(x)] for x in delete_None(uaser.list_req_frends.split(','))]
    print(frends_new,'----')
    for i in range(len(frends)):
        frends[i].ids = frends_id[i]
    for i in range(len(frends_new)):
            
        frends_new[i].ids = frends_id[i]-1
    
    if MINE!=['']:
        print(frends_id,checher(MINE[0],MINE[1])[1])
        myFrend = True if checher(MINE[0],MINE[1])[1] in frends_id else False
        print(myFrend)
        if password_create(MINE[1]) == USER_SOURS[2] and MINE[0] == USER_SOURS[1]:
            isMine = True
            idis = MINE[2]
            myFrend = False
            return render(request,'profile/profile.html',{'uaser':uaser,'ii':ii,'seans':seans,'isMine':isMine,'id':idis,'list_seans':list_seans,'prof_id':prof_id,'frends':frends,'frends_new':frends_new,'myFrend':myFrend})
    
        
    return render(request,'profile/profile.html',{'uaser':uaser,'ii':ii,'seans':seans,'isMine':isMine,'list_seans':list_seans,'prof_id':prof_id,'frends':frends,'frends_new':frends_new,'myFrend':myFrend})



def buy_valet (request,seans_id):
    # if request.method == 'POST':
    #     print('ON')
    try:
        all = DATA_ALL_SEANSES.objects.all()
        info_po_cody = [str(x).split('|')[0] for x in all]
        id = info_po_cody.index(seans_id)
        info_po_id = all[id]
        MINE_user =  request.COOKIES.get('user','').split('/')  
        idis = int(MINE_user[-1])
        
        

        ii = II.objects.all()[idis]
        
        try:
            seans = SEANS.objects.all()[idis]
        except:
            seans = []
            raise Http404('Этого чисто физически не должно было произойти  ')
        
        
        
        print(str(info_po_id.img.name))
        seans.seanses = f'{str(seans.seanses)}{info_po_id.name.replace("!",".").replace("|",".")}!{info_po_id.discription.replace("!",".").replace("|",".")}!{str(info_po_id.img.name.replace("!",".").replace("|","."))}!{info_po_id.class_seans}|'
        
        
        ii.now=f'{ii.now}{info_po_id.name}!{info_po_id.discription.replace("!",".").replace("|",".")}!{info_po_id.img.name.replace("!",".").replace("|",".")}!{info_po_id.class_seans}|'
        ii.save()
        seans.save()
        return HttpResponse('Все гуд ')
    except Exception as e:
        print(e)
        print(info_po_id.class_seans)
        
        raise Http404('Войдите в аккакунт ')

def like(request,seans_id):
    cookie = request.COOKIES.get('user','').split('/') 
    print(cookie)
    
    
    if cookie[-1] == str(checher(cookie[0],cookie[1])[1]):
        user = USER.objects.all()[int(cookie[-1])]
        like =  user.likes
        
        user.likes= like + seans_id +','
        
        print(user.likes)
        user.save()
        return HttpResponseRedirect('../merop')
    else:
        print(4)
        return HttpResponseRedirect('../')
    
def addfrends(request,prof_id):
    MINE =  request.COOKIES.get('user','').split('/') 
    print(MINE)  
    if MINE != [''] or len(MINE)>1:
        info = checher(MINE[0],MINE[1])
        if info[0]:
            if -1<prof_id<=len(USER.objects.all()):
                user_1 = USER.objects.all()[prof_id]
                if prof_id not in user_1.list_req_frends.split(','):
                    
                    
                    user_1.list_req_frends = str(MINE[2])+','
                    print(user_1.list_req_frends)
                    user_1.save()
    return HttpResponseRedirect('../prof/'+str(prof_id))
    
def man_accept(request,prof_id):
    MINE =  request.COOKIES.get('user','').split('/') 
    print(MINE)  
    if MINE != [''] or len(MINE)>1:
        info = checher(MINE[0],MINE[1])
        if info[0]:
            all_user = USER.objects.all()
            user_1 = all_user[prof_id]
            user_2 = all_user[info[1]] 
            
            user_1.list_frends = user_1.list_frends  + str(info[1])+','
            user_2.list_frends = user_2.list_frends  + str(prof_id)+','
            print(user_1.list_frends ,user_2.list_frends )
            
            
            mass = delete_None(user_2.list_req_frends.split(','))
            print(mass,'------')
            print(prof_id)
            mass.remove(str(prof_id))
            
            user_2.list_req_frends=','+','.join(mass)+',' if mass != [] else ','.join(mass)
            
            
            user_1.save()
            user_2.save()
            
    return HttpResponseRedirect('../prof/my_ine')

def man_noaccept(request,prof_id):
    MINE =  request.COOKIES.get('user','').split('/') 
    print(MINE)  
    if MINE != [''] or len(MINE)>1:
        info = checher(MINE[0],MINE[1])
        if info[0]:
            user_2 = USER.objects.all()[info[1]] 
            mass = delete_None(user_2.list_req_frends.split(','))
            mass.remove(str(prof_id))
            
            user_2.list_req_frends=','.join(mass)+',' if mass != [] else ','.join(mass)
            
            
            
            user_2.save()
    return HttpResponseRedirect('../prof/my_ine')

def users(request):
    return render(request,'ProDos/category.html',{'user':USER.objects.all()})