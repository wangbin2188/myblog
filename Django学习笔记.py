Django学习笔记
****************************************************************************windows*****************************************************************
# django-admin.py路径
/usr/local/python27/bin
/usr/local/python27/bin/myblog


# 在mysql新增库chart
 CREATE DATABASE chart DEFAULT CHARSET=utf8;
# 模型models.py的更新
python manage.py makemigrations push
python manage.py migrate
# 静态文件部署bug解决
# 在源urls.py中加入如下语句
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    url(r'^admin/', admin.site.urls),　　 
	url(r'^$', blogs_views.index),
] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
# 在html文件中使用如下方式引入静态文件
	{% load staticfiles %}
	<script  src="{% static "js/jquery.base64.js" %}"></script>

# 数据库的导入导出
python manage.py dumpdata push > push.json
python manage.py loaddata push.json


#创建超级管理员
python manage.py createsuperuser
username:wangbin;
password:******



服务器ip

# 启动测试服务
python manage.py runserver 8001
python manage.py runserver 0.0.0.0:8000
http://172.20.4.64:8000/push/app_active/

# 进入uwsgi目录运行
./uwsgi --http :8000 --chdir /usr/local/python27/bin/myblog  --module myblog.wsgi
# uwsgi的目录
/usr/local/python27/bin/uwsgi
/usr/local/python27/bin/

# 安装命令行浏览器
yum  install w3m w3m-img
w3m http://127.0.0.1:8001/push/app_active
# supervisord目录
/etc

# 检测端口占用情况
netstat -apn | grep 8000




# 修改了版本，需要考虑静态文件的路径问题

sudo vim /etc/nginx/sites-available/myblog.conf

server {
listen      8000;
server_name ip.*.*.*;
charset     utf-8;
 
client_max_body_size 75M;
 
location /media  {
alias /usr/local/python27/bin/myblog/push/media;
}
 
location /static {
alias /usr/local/python27/bin/myblog.6.12.26/static;
}
 
location / {
uwsgi_pass  unix:///tmp/myblog.sock;
include     /etc/nginx/uwsgi_params;
}
}

server {
listen      8001;
server_name ip.*.*.*;
charset     utf-8;
 
 client_max_body_size 75M;
  
  location /media  {
  alias /usr/local/monitor/media;
  }
   
location /static {
  alias /usr/local/monitor/static;
  }
    
location / {
  uwsgi_pass  unix:///tmp/monitor.sock;
  include     /etc/nginx/uwsgi_params;
  }
}

sudo ln -s /etc/nginx/sites-available/myblog.conf /etc/nginx/sites-enabled/myblog.conf


17423
django默认是UTC时间，在settings.py中把
TIME_ZONE = 'UTC'，修改为TIME_ZONE = 'Asia/Shanghai'就可以了



sudo supervisord -c /etc/supervisord.conf


# 开启
cd /usr/local/python27/bin
./gunicorn -w4 -b0.0.0.0:8000 --chdir /usr/local/python27/bin/myblog myblog.wsgi
/usr/local/python27/bin/gunicorn -w4 -b0.0.0.0:8000 --chdir /usr/local/python27/bin/myblog myblog.wsgi


sudo ln -s /etc/nginx/sites-available/monitor.conf /etc/nginx/sites-enabled/monitor.conf
./gunicorn -w4 -b0.0.0.0:8001 --chdir /usr/local/monitor monitor.wsgi
sudo service nginx restart
# 关闭占用80端口的程序
sudo fuser -k 8000/tcp
# 重启nginx服务器
sudo service nginx restart
sudo service nginx reload
大功告成！一切OK！
# echarts折线图节点大小及是否展示
symbolSize: 6,
showSymbol: true | false
 color: '#660099'



######################################################Django常用命令######################################################
# -*- coding: utf-8 -*-
#进入django:
C:\Python34\Lib\site-packages\django\bin\myblog
# 发布到局域网
http://192.168.4.21:8000/push/app_active/
python manage.py runserver 0.0.0.0:8000
#新建项目：
django-admin.py startproject myblog
#新建APP：
python manage.py startapp blog
#运行程序
python2 manage.py runserver
#进入命令行：
python manage.py shell
#将这些改变更新到数据库中
python manage.py makemigrations push
python manage.py migrate

###################################################### Django模板######################################################
# 模板文件的默认路径
默认配置下，Django 的模板系统会自动找到app下面的templates文件夹中的模板文件。
#过滤器：模板过滤器可以在变量被显示前修改它，过滤器使用管道字符，如下所示：
{{ name|lower }}
{{ my_list|first|upper }}：将第一个元素并将其转化为大写。
{{ bio|truncatewords:"30" }}：显示变量 bio 的前30个词。
{{ pub_date|date:"F j, Y" }}：日期格式化
length : 返回变量的长度
{% include %} 标签允许在模板中包含其它的模板的内容。
#html遍历字典：
在views函数中传入的参数必须声明是字典，即便本来是列表也不除外，列表可以直接for循环引用，字段通过如下方法遍历：
return render(request, 'home.html', {'info_dict': info_dict})
方法1：
<p>{{ context.label }},{{ context.name }},{{ context.word }}</p>
方法2：
{% for key, value in info_dict.items %}
    {{ key }}: {{ value }}
{% endfor %}
#html的选择判断：
{% if condition1 %}
   ... display 1
{% elif condiiton2 %}
   ... display 2
{% else %}
   ... display 3
{% endif %}

{% ifequal %} 标签比较两个值，当他们相等时，显示在 {% ifequal %} 和 {% endifequal %} 之中所有的值。
下面的例子比较两个模板变量 user 和 currentuser :
{% ifequal user currentuser %}
    <h1>Welcome!</h1>
	{% ifequal flow_state.executor request.user %}
{% endifequal %}
和 {% if %} 类似， {% ifequal %} 支持可选的 {% else%} 标签：8
{% ifequal section 'sitenews' %}
    <h1>Site News</h1>
{% else %}
    <h1>No News Here</h1>
{% endifequal %}
********************************************
{% for item in result %}
<p>{{ item.name }},{{ item.value }}</p>
{% endfor %}

<table border=1>
{% for item in result %}
<tr>
<td>{{ item.name }}</td>
<td>{{ item.value}}</td>
</tr>
{% endfor %}
<table>

在html 获取表单的值{{ request.POST.date_format }}
{{request.path_info}}主机名之后的url
django模板中的日期格式化 |date:"Y-m-d"   带时间的格式：date|"Y-m-d H:i:s"
保留2位小数 {{ 13.414121241|floatformat:"2" }}

#ifequal/ifnotequal 标签
###################################################### Django视图######################################################
url配置：
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^articles/2003/$', views.special_case_2003),
    url(r'^articles/([0-9]{4})/$', views.year_archive),
    url(r'^articles/([0-9]{4})/([0-9]{2})/$', views.month_archive),
    url(r'^articles/([0-9]{4})/([0-9]{2})/([0-9]+)/$', views.article_detail),
]
上面最后一个url将调用views.article_detail(request, '2003', '03', '03')，函数参数按顺序来，如果想对参数命名可以采用下面的方式：
from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^articles/2003/$', views.special_case_2003),
    url(r'^articles/(?P<year>[0-9]{4})/$', views.year_archive),
    url(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.month_archive),
    url(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', views.article_detail),
]
这个时候会调用views.article_detail(request, year='2003', month='03', day='03')，更加明晰且不容易产生参数顺序问题的错误
# URL 的反向解析，在需要URL 的地方，对于不同层级，Django 提供不同的工具用于URL 反查：
from django.conf.urls import url
urlpatterns = [
    url(r'^articles/([0-9]{4})/$', views.year_archive, name='news-year-archive'),
]
1.在模板中：使用url 模板标签。例：<a href="{% url 'news-year-archive' 2012 %}">2012 Archive</a>
2.在Python 代码中：使用django.core.urlresolvers.reverse() 函数。
在Python 代码中，这样使用：
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
def redirect_to_year(request):
	...
    year = ***
    return HttpResponseRedirect(reverse('news-year-archive', args=(year,)))
3.在处理Django 模型实例相关的代码中：使用get_absolute_url() 方法。

class ModelName(models.Model):
	...
	def get_absolute_url(self):
		from django.core.urlresolvers import reverse
		return reverse('people.views.details', args=[str(self.id)])
# 在模板中这样使用，相对于给模型中的每个实例绑定了一个url属性：
<a href="{{ object.get_absolute_url }}">{{ object.name }}</a>
# urls中的参数
直接第一个匹配的传递给nid，第二个匹配的传递给uid，这样和views里的函数形参位置没有关系了。
urls.py：url(r'^detail-(?P<nid>\d+)-(?P<uid>\d+).html/', views.detail),
views.py：def detail(request, nid, uid):
访问网址：127.0.0.1/detail-key1-9.html
分组时，个数不确定*args，**kwargs也能使用
url(r'^detail-(key\d+)-(\d+).html/', views.detail), ——> def detail(request, *args):
url(r'^detail-(?P<nid>\d+)-(?P<uid>\d+).html/', views.detail), ——> def detail(request, **kwargs):


# name ：django 简便用法
对URL路由关系进行命名， 以后可以根据此名称生成自己想要的URL
urls.py
url(r'^home/', views.home, name="homeee"),
home.html

    <form action="{% url 'homeee' %}" method="POST">
        <input type="text" name="user" />
        <input type="submit" />
    </form>
#views
def investigate(request):
    if request.POST:
        submitted  = request.POST['staff']
        submitted1=request.POST['age']
        #new_record = Person(name = submitted,age=submitted1)
        #new_record.save()
    ctx ={}
    ctx.update(csrf(request))
    all_records = Person.objects.filter(name__startswith = submitted,age=submitted1)
    ctx['staff'] = all_records
    return render(request, "investigate.htm", ctx)
#html
    <form action="/learn/investigate/" method="post">
  {% csrf_token %}
  name:<input type="text" name="staff">
  age:<input type="text" name="age">
  <input type="submit" value="Submit">
</form>
<table border=1>
{% for person in staff %}
<tr>
<td>{{ person.name }}</td>
<td> {{person.age}}</td>
<td> {{person.region}}</td>
</tr>
{% endfor %}
</table>
# 上下文渲染器
用户名和IP地址：{{ request.user.username}}:{{ request.META['REMOTE_ADDR'] }}

# 视图中的request对象和response对象，request是用户的一次请求，response是服务器对用户请求的一次相应。
request有如下属性：
request.path_info
request.user
request.method
request.COOKIES
request.META.REMOTE_ADDR(用户的IP地址)
request.session
# 常用的response对象
# HttpResponse 对象
# response有如下属性和方法：
response.set_cookie()
response.delete_cookie()
# JsonResponse 对象，返回一个json,可用于传递数据
>>> from django.http import JsonResponse
>>> response = JsonResponse({'foo': 'bar'})
>>> response.content
'{"foo": "bar"}'
# FileResponse 对象，返回一个文件
>>> from django.http import FileResponse
>>> response = FileResponse(open('myfile.png', 'rb'))
# 视图的基础函数——HttpResponse
from django.http import HttpResponse
def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)
# 视图的快捷函数——render
from django.shortcuts import render
def my_view(request):
    ...
    return render(request, 'template.html', {"foo": "bar"},content_type="application/xhtml+xml")
# 这个示例等同于：
from django.http import HttpResponse
from django.template import RequestContext, loader
def my_view(request):
    ...
    t = loader.get_template('template.html')
    c = RequestContext(request, {'foo': 'bar'})
    return HttpResponse(t.render(c),content_type="application/xhtml+xml")
# 视图的快捷函数——render_to_response	
from django.shortcuts import render_to_response
def my_view(request):
    ...
    return render_to_response('myapp/index.html', {"foo": "bar"},content_type="application/xhtml+xml")
# 视图的快捷函数——redirect
你可以用多种方式使用redirect() 函数。
# 通过传递一个对象；将调用get_absolute_url() 方法来获取重定向的URL：
from django.shortcuts import redirect
def my_view(request):
    ...
    object = MyModel.objects.get(...)
    return redirect(object)
# 通过传递一个视图的名称，可以带有位置参数和关键字参数；将使用reverse() 方法反向解析URL：
def my_view(request):
    ...
    return redirect('some-view-name', foo='bar')
# 传递要重定向的一个硬编码的URL：
def my_view(request):
    ...
    return redirect('/some/url/')
# 也可以是一个完整的URL：
def my_view(request):
    ...
    return redirect('http://example.com/')
默认情况下，redirect() 返回一个临时重定向。以上所有的形式都接收一个permanent 参数；如果设置为True，将返回一个永久的重定向：
def my_view(request):
    ...
    object = MyModel.objects.get(...)
    return redirect(object, permanent=True)
# 视图的快捷函数——get_object_or_404
from django.shortcuts import get_object_or_404
def my_view(request):
    my_object = get_object_or_404(MyModel, pk=1)
# 视图的快捷函数——get_list_or_404
from django.shortcuts import get_list_or_404
def my_view(request):
    my_objects = get_list_or_404(MyModel, published=True)
# 内置错误视图

在根目录的urls.py中增加最下面四行即可
from django.views import defaults
urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'^push/',include('push.urls')),
        url(r'^blog/',include('blog.urls')),
        url(r'^accounts/login/$', auth_views.login),
]+ static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)

handler404=defaults.page_not_found
handler500=defaults.server_error
handler403=defaults.permission_denied
handler400=defaults.bad_request

# 基于类的视图
# urls.py
from push.views import UserCreate,UserUpdate,UserDelete,UserListList,UserListDetail
urlpatterns = [
url(r'^userlist/add/$', UserCreate.as_view(), name='user_create'),
url(r'^userlist/(?P<pk>[0-9]+)/update/$', UserUpdate.as_view(), name='user_update'),
url(r'^userlist/(?P<pk>[0-9]+)/delete/$', UserDelete.as_view(), name='user_delete'),
url(r'^userlist/$', UserListList.as_view(),name='userlist'),
url(r'^userlist/(?P<pk>[0-9]+)/$', UserListDetail.as_view(),name='userdetail'),
]

# models.py
class UserList(models.Model):
        username = models.CharField(max_length=20)
        password=models.CharField(max_length=20)
		
# views.py
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from push.models import UserList
from django.core.urlresolvers import reverse_lazy
class UserListList(ListView):
        model=UserList
class UserListDetail(DetailView):
        model=UserList
		def get_context_data(self, **kwargs):
			context = super(UserListDetail, self).get_context_data(**kwargs)
			context['now'] = timezone.now()
			return context		
class UserCreate(CreateView):
        model=UserList
        fields=['username','password']
        success_url = '/push/userlist/'
class UserUpdate(UpdateView):
        model=UserList
        fields=['username','password']
        success_url = '/push/userlist/'
        template_name_suffix = '_update_form'
class UserDelete(DeleteView):
        model=UserList
        success_url = reverse_lazy('userlist')
		
# push/userlist_confirm_delete.html
<form action="" method="post">
{% csrf_token %}
<p>Are you sure you want to delete "{{ object }}"?</p>
<input type="submit" value="Confirm" />

# push/userlist_detail.html
<ul>
<li>{{ object.username }},{{ object.password }},{{now|date}}</li>
</ul>

# push/userlist_form.html
<form action="" method="post">
{% csrf_token %}
{{ form.as_p }}
<input type="submit" value="Create" />
</form>

# push/userlist_list.html
<ul>
{% for publisher in object_list %}
<li>
<a href="{% url 'userdetail' publisher.id %}">{{ publisher.username }}</a>
<a href="{% url 'user_update' publisher.id  %}">update</a>
<a href="{% url 'user_delete' publisher.id  %}">delete</a>
</li>
{% endfor %}
</ul>
<a href="{% url 'user_create'   %}">add</a>
# push/userlist_update_form.html
<form action="" method="post">
{% csrf_token %}
{{ form.as_p }}
<input type="submit" value="Update" />
</form>

# 通用日期视图
1.所有年份列表 2.某年列表 3.某年的某月列表 4.某年的第几周列表 5.某年某月某天列表 6.当天列表 7.具体详情
# urls.py
from django.conf.urls import url
from django.views.generic.dates import ArchiveIndexView,DateDetailView
from myapp.views import ArticleYearArchiveView,ArticleMonthArchiveView,ArticleWeekArchiveView,ArticleDayArchiveView,ArticleTodayArchiveView
urlpatterns = [
	url(r'^archive/$',ArchiveIndexView.as_view(model=Article, date_field="pub_date"),name="article_archive"),
	url(r'^(?P<year>[0-9]{4})/$',ArticleYearArchiveView.as_view(),name="article_year_archive"),
	url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]+)/$',ArticleMonthArchiveView.as_view(month_format='%m'),name="archive_month_numeric"),
	url(r'^(?P<year>[0-9]{4})/week/(?P<week>[0-9]+)/$',ArticleWeekArchiveView.as_view(),name="archive_week"),
	url(r'^(?P<year>[0-9]{4})/(?P<month>[-\w]+)/(?P<day>[0-9]+)/$',ArticleDayArchiveView.as_view(),name="archive_day"),
	url(r'^today/$',ArticleTodayArchiveView.as_view(),name="archive_today"),
	url(r'^(?P<year>[0-9]{4})/(?P<month>[-\w]+)/(?P<day>[0-9]+)/(?P<pk>[0-9]+)/$',DateDetailView.as_view(model=Article, date_field="pub_date"),name="archive_date_detail"),
]
# models.py
from django.db import models
from django.core.urlresolvers import reverse
class Article(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateField()

    def get_absolute_url(self):
        return reverse('article-detail', kwargs={'pk': self.pk})
# views.py	
from django.views.generic.dates import YearArchiveView,MonthArchiveView,WeekArchiveView,DayArchiveView,TodayArchiveView
from myapp.models import Article
class ArticleYearArchiveView(YearArchiveView):
    queryset = Article.objects.all()
    date_field = "pub_date"
    make_object_list = True
    allow_future = True

class ArticleMonthArchiveView(MonthArchiveView):
    queryset = Article.objects.all()
    date_field = "pub_date"
    allow_future = True	
	
class ArticleWeekArchiveView(WeekArchiveView):
    queryset = Article.objects.all()
    date_field = "pub_date"
    week_format = "%W"
    allow_future = True
class ArticleDayArchiveView(DayArchiveView):
    queryset = Article.objects.all()
    date_field = "pub_date"
    allow_future = True
class ArticleTodayArchiveView(TodayArchiveView):
    queryset = Article.objects.all()
    date_field = "pub_date"
    allow_future = True
	
# myapp/article_archive.html：
<ul>
    {% for article in latest %}
        <li>{{ article.pub_date }}: {{ article.title }}</li>
    {% endfor %}
</ul>

# myapp/article_archive_year.html：
<ul>
    {% for date in date_list %}
        <li>{{ date|date }}</li>
    {% endfor %}
</ul>
<div>
    <h1>All Articles for {{ year|date:"Y" }}</h1>
    {% for obj in object_list %}
        <p>
            {{ obj.title }} - {{ obj.pub_date|date:"F j, Y" }}
        </p>
    {% endfor %}
</div>

# myapp / article_archive_month.html：

<ul>
    {% for article in object_list %}
        <li>{{ article.pub_date|date:"F j, Y" }}: {{ article.title }}</li>
    {% endfor %}
</ul>

<p>
    {% if previous_month %}
        Previous Month: {{ previous_month|date:"F Y" }}
    {% endif %}
    {% if next_month %}
        Next Month: {{ next_month|date:"F Y" }}
    {% endif %}
</p>

# myapp / article_archive_week.html：

<h1>Week {{ week|date:'W' }}</h1>

<ul>
    {% for article in object_list %}
        <li>{{ article.pub_date|date:"F j, Y" }}: {{ article.title }}</li>
    {% endfor %}
</ul>
<p>
    {% if previous_week %}
        Previous Week: {{ previous_week|date:"F Y" }}
    {% endif %}
    {% if previous_week and next_week %}--{% endif %}
    {% if next_week %}
        Next week: {{ next_week|date:"F Y" }}
    {% endif %}
</p>
# myapp / article_archive_day.html：

<h1>{{ day }}</h1>

<ul>
    {% for article in object_list %}
        <li>{{ article.pub_date|date:"F j, Y" }}: {{ article.title }}</li>
    {% endfor %}
</ul>

<p>
    {% if previous_day %}
        Previous Day: {{ previous_day }}
    {% endif %}
    {% if previous_day and next_day %}--{% endif %}
    {% if next_day %}
        Next Day: {{ next_day }}
    {% endif %}
</p>

# myapp/article_detail.html：

<h1>{{ object.title }}</h1>
###################################################### Django模型######################################################
# 日期时间的自动更新参数
DateField.auto_now¶
每次保存对象时，自动设置该字段为当前时间。用于"最后一次修改"的时间戳。注意，它总是使用当前日期；它不只是一个默认值，你可以覆盖。

DateField.auto_now_add¶
当对象第一次被创建时自动设置当前时间。用于创建时间的时间戳. 它总是使用当前日期；和你可以覆盖的那种默认值不一样。
#插入一条数据：
Blog.objects.create(title="The first blog of my site",content="I am writing my blog on Terminal")
Blog.objects.all()
#插入一条数据：
Blog.objects.create(title=title,content=content)
#避免重复可以用下面的格式：
Blog.objects.get_or_create(title=title,content=content)
#导出文件/导入文件，数据导入不需要知道APPname
python manage.py dumpdata blog > blog_dump.json
python manage.py loaddata blog_dump.json
#批量导入数据，参数是一个列表，类似excutemany()
 Blog.objects.bulk_create(BlogList)
#为这些修改创建迁移文件
django不认识mysqlDB，安装pymysql替代，并在__init__.py中加上如下两句：
import pymysql
pymysql.install_as_MySQLdb()
# django自带的迁移命令
# 从原来的整个数据库导出所有数据
python manage.py dumpdata > mysite_all_data.json
# 将mysite_all_data.json传送到另一个服务器或电脑上导入
python manage.py loaddata mysite_all_data.json
# mysql本身的备份命令
# mysql导出数据库 blog 到 blog.sql 文件中
mysqldump -u username -p --database blog > blog.sql
# mysql导入数据库到 新的服务器
mysql -u username -p输入密码进入 MySQL 命令行
> source /path/to/blog.sql
#创建超级管理员
python manage.py createsuperuser
username:wb.wang;
password:******
username:wangbin/******

#django自带查询：
filter:过滤
exclude:排除
Person.objects.all()[5:15]：切片
list=Person.objects.filter(name=name,age__lt=age)
__gt:大于
__lt:小于
__gte:表示 大于或等于
聚合运算
Dict = AppPosts.objects.filter(date__gte=start_date,date__lte=end_date).values(date_format).annotate(posts=Avg('posts'),replies=Avg('replies'),likes=Avg('likes'),attentions=Avg('attentions'),votes=Avg('votes'))
Person.objects.filter(name__contains="abc") # 名称中包含 "abc"的人
Person.objects.filter(name__icontains="abc") #名称中包含 "abc"，且abc不区分大小写
Person.objects.filter(name__regex="^abc") # 正则表达式查询
Person.objects.filter(name__iregex="^abc")# 正则表达式不区分大小写
Person.objects.exclude(name__contains="WZ") # 排除包含 WZ 的Person对象
Person.objects.filter(name__contains="abc").exclude(age=23) # 找出名称含有abc, 但是排除年龄是23岁的
Person.objects.filter(name__startswith='Paul')名字开头是paul
Person.objects.count() ：聚合函数计数
Person.objects.order_by('date')[:10]：升序
Person.objects.order_by('-date')[:10]：降序
dict=AppKeyValue.objects.filter(dt__gte='2017-07-01',dt__lte='2017-07-05',c_key__in=['headline','community','car','service','my'])
Django各种条件查询关键字：

__exact 精确等于 like ‘aaa’ 
__iexact 精确等于 忽略大小写 ilike ‘aaa’ 
__contains 包含 like ‘%aaa%’ 
__icontains 包含 忽略大小写 ilike ‘%aaa%’，但是对于sqlite来说，contains的作用效果等同于icontains。 
__gt 大于 
__gte 大于等于 
__lt 小于 
__lte 小于等于 
__in 存在于一个list范围内 
__startswith 以…开头 
__istartswith 以…开头 忽略大小写 
__endswith 以…结尾 
__iendswith 以…结尾，忽略大小写 
__range 在…范围内 
__year 日期字段的年份 
__month 日期字段的月份 
__day 日期字段的日 
__isnull=True/False
#更新数据
test1 = Test.objects.get(id=1)
    test1.name = 'w3cschool菜鸟教程'
    test1.save()
# 另外一种方式
Test.objects.filter(id=1).update(name='w3cschool菜鸟教程')

#修改所有的列
Test.objects.all().update(name='w3cschool菜鸟教程')
#删除数据
test1 = Test.objects.get(id=1)
    test1.delete()
# 另外一种方式
Test.objects.filter(id=1).delete()
# 删除所有数据
Test.objects.all().delete()
# django ORM增删改查
from app01 import models  # 导入models模块
def orm(request):
# 创建数据
# 第一种方式
models.UserInfo.objects.create(username="root",password="123")
# 第二种方式
obj = models.UserInfo(username='fzh', password="iajtag")
obj.save()
# 第三种方式
dic = {'username':'fgf', 'password':'666'}
models.UserInfo.objects.create(**dic)

# 查询数据
result = models.UserInfo.objects.all()  # 查询所有，为QuerySet类型，可理解成列表
result = models.UserInfo.objects.filter(username="fgf",password="666")  # 列表
result = models.UserInfo.objects.filter(username="fgf").first()  # 对象
条件查询。filter 相当于where查询条件，里面的","会组成and条件
for row in result:  # 打印查询到数据。
    print(row.id,row.username,row.password)

查看QuerySet类型具体做了什么事情，可以： print(result.query)

# 删除数据
    models.UserInfo.objects.all().delete()  # 删除所有
    models.UserInfo.objects.filter(id=4).delete()  # 删除所有

# 更新数据
    models.UserInfo.objects.all().update(password=8888)
    models.UserInfo.objects.filter(id=3).update(password=888888)

    
# 获取单表数据的三种方式
v1 = models.Business.objects.all() QuerySet类型 ,内部元素都是对象（对象内类似字典结构）
[obj(id,caption,code), obj(id,caption,code), obj(id,caption,code)]
v2 = models.Business.objects.all().values('id','caption') QuerySet ,内部元素都是字典，可以用list转化为列表
[{'id':1,'caption':'运维'},{'id':1,'caption':'运维'},{'id':1,'caption':'运维'}]
v3 = models.Business.objects.all().values_list('id','caption') QuerySet ,内部元素都是元组
[（1，运维），（2，开发）]
obj = Business.objects.get(id=1) 获取到的一个对象，如果不存在就报错DoesNotExist
obj = Business.objects.filter(id=1).first() 对象或者None

# 获取个数
models.Tb1.objects.filter(name='seven').count()
# 大于，小于
models.Tb1.objects.filter(id__gt=1)      # 获取id大于1的值
models.Tb1.objects.filter(id__gte=1)      # 获取id大于等于1的值
models.Tb1.objects.filter(id__lt=10)     # 获取id小于10的值
models.Tb1.objects.filter(id__lte=10)     # 获取id小于10的值
models.Tb1.objects.filter(id__lt=10, id__gt=1)   # 获取id大于1 且 小于10的值
# in
models.Tb1.objects.filter(id__in=[11, 22, 33])   # 获取id等于11、22、33的数据
models.Tb1.objects.exclude(id__in=[11, 22, 33])  # not in
# isnull
Entry.objects.filter(pub_date__isnull=True)
# contains
models.Tb1.objects.filter(name__contains="ven")
models.Tb1.objects.filter(name__icontains="ven") # icontains大小写不敏感
models.Tb1.objects.exclude(name__icontains="ven")
# range
models.Tb1.objects.filter(id__range=[1, 2])   # 范围bettwen and
# 其他类似
startswith，istartswith, endswith, iendswith,
# order by
models.Tb1.objects.filter(name='seven').order_by('id')    # asc
models.Tb1.objects.filter(name='seven').order_by('-id')   # desc
# group by
from django.db.models import Count, Min, Max, Sum
models.Tb1.objects.filter(c1=1).values('id').annotate(c=Count('num'))
SELECT "app01_tb1"."id", COUNT("app01_tb1"."num") AS "c" FROM "app01_tb1" WHERE "app01_tb1"."c1" = 1 GROUP BY "app01_tb1"."id"

# limit 、offset
# Python中的切片也可以用在模型的查询结果中：
models.Tb1.objects.all()[10:20]

# regex正则匹配，iregex 不区分大小写
Entry.objects.get(title__regex=r'^(An?|The) +')
Entry.objects.get(title__iregex=r'^(an?|the) +')
# date
Entry.objects.filter(pub_date__date=datetime.date(2005, 1, 1))
Entry.objects.filter(pub_date__date__gt=datetime.date(2005, 1, 1))
# year
Entry.objects.filter(pub_date__year=2005)
Entry.objects.filter(pub_date__year__gte=2005)
# month
Entry.objects.filter(pub_date__month=12)
Entry.objects.filter(pub_date__month__gte=6)
# day
Entry.objects.filter(pub_date__day=3)
Entry.objects.filter(pub_date__day__gte=3)
# week_day
Entry.objects.filter(pub_date__week_day=2)
Entry.objects.filter(pub_date__week_day__gte=2)
# hour
Event.objects.filter(timestamp__hour=23)
Event.objects.filter(time__hour=5)
Event.objects.filter(timestamp__hour__gte=12)
# minute
Event.objects.filter(timestamp__minute=29)
Event.objects.filter(time__minute=46)
Event.objects.filter(timestamp__minute__gte=29)
# second
Event.objects.filter(timestamp__second=31)
Event.objects.filter(time__second=2)
Event.objects.filter(timestamp__second__gte=31)

###################################################### Django表单######################################################

单选按钮组
grade=forms.ChoiceField(label='grade',required=True,widget=forms.RadioSelect,choices=GRADE_CHOICES)
下拉列表框
grade=forms.ChoiceField(label='grade',required=True,widget=forms.Select,choices=GRADE_CHOICES)
复选按钮组
grade=forms.MultipleChoiceField(label='grade',required=True,widget=forms.CheckboxSelectMultiple(),choices=((1, 'shanghai'), (2, 'beijing'),))
RadioSelect 单选按钮组
CheckboxInput 单个复选框
CheckboxSelectMultiple()复选框组
SelectMultiple,下拉列表框,可多选，功能强大，占地大不太好看
select 下拉列表框,单选
<p>
{% for radio in form.grade %}
<div class="form-group">
    {{ radio }}
</div>
{% endfor %}
</p>
文本域
message = forms.CharField(label='留言内容',widget=forms.Textarea)
表单和model联动，单选下拉对象manager,多选对象databases,上传文件attachment
class CreatetaskForm(forms.Form):
    creater = forms.CharField(label=u"创建者",widget=BootstrapUneditableInput())
    manager = forms.ModelChoiceField(queryset=Manager.objects.all(),required=True,label=u"项目负责人",error_messages={'required': u'必选项'},)  
    databases = forms.ModelMultipleChoiceField(queryset=Database.objects.order_by('id'),required=True,label=u"数据库",error_messages={'required': u'至少选择一个'},widget=forms.CheckboxSelectMultiple,)    
    sql = forms.CharField(required=False,label=u"执行SQL",widget=forms.Textarea(attrs={'placeholder':"请在表名前加上schema，如hospital要写成p95169.hospital",'rows':5,'style':"width:100%",}),)
    desc = forms.CharField(required=False,label=u"描述",widget=forms.Textarea(attrs={'placeholder':"如果不是执行SQL(如数据的导入导出等)，一定要在描述里说清楚",'rows':5,'style':"width:100%",}),) 
    attachment = forms.FileField(required=False,label=u"附件",help_text=u"如果SQL文本过长，超过2000个字符，请上传附件")
    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"以下红色标记部分为必选项")
        elif self.cleaned_data['sql'] == u'' and self.cleaned_data['desc'] == u'' :
            raise forms.ValidationError(u"如果执行SQL为空，描述为必填项")
        else:
            cleaned_data = super(CreatetaskForm, self).clean() 
        return cleaned_data
# 单radio，值为字符串
user = fields.CharField(initial=2,widget=widgets.RadioSelect(choices=((1,'上海'),(2,'北京'),)))
# 单radio，值为字符串
user = fields.ChoiceField(choices=((1, '上海'), (2, '北京'),),initial=2,widget=widgets.RadioSelect)
# 单select，值为字符串
user = fields.CharField(initial=2,widget=widgets.Select(choices=((1,'上海'),(2,'北京'),)))
# 单select，值为字符串
user = fields.ChoiceField(choices=((1, '上海'), (2, '北京'),),initial=2,widget=widgets.Select)
# 多选select，值为列表
user = fields.MultipleChoiceField(choices=((1,'上海'),(2,'北京'),),initial=[1,],widget=widgets.SelectMultiple)
# 单checkbox
user = fields.CharField(widget=widgets.CheckboxInput())
# 多选checkbox,值为列表
user = fields.MultipleChoiceField(initial=[2, ],choices=((1, '上海'), (2, '北京'),),widget=widgets.CheckboxSelectMultiple



###################################################### Django日志######################################################
# settings.py 加入配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
	'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/root/bin/myblog/myblog/debug.log',
        },
		'browse_handler': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/root/bin/myblog/myblog/browse.log',
			'formatter': 'simple'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
		'browse': {
            'handlers': ['browse_handler'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# views.py 中：
import logging
logger = logging.getLogger('browse')
def function(request):
	logger.info('type=app_active&user=%s&ip=%s' %(request.user.username,request.META['REMOTE_ADDR']))
# 非常好的django博客
http://blog.csdn.net/fgf00/article/details/53649820


   <tbody id="show">
{% for item in result %}
      <tr>
         <td>{% ifequal  date_format  'date' %}
		 {{ item.date}} 
		 {% else %}
		 {{ item.week}}  {{ item.month}} 
		 {% endifequal %}
		 </td>
         <td>{{ item.adr_active |floatformat:"0"}}</td>
		 <td>{{ item.ios_active |floatformat:"0"}}</td>
		 <td>{{ item.ipad_active |floatformat:"0"}}</td>
			 
      </tr>
	  {% endfor %}
   </tbody>
  
###################################################### django的定时任务 ###################################################### 
pip install django-crontab
添加app名称到 settings.py中

INSTALLED_APPS = (
        'django_crontab',
        ...
    ) 
在 settings.py中的最后增加

CRONJOBS = [
    ('*/5 * * * *', 'myproject.myapp.mails.car_daily','>>/home/test.log')
]	
以上都完成后，需要执行 
Python manage.py crontab add 
将任务添加并生效

显示当前的定时任务 
python manage.py crontab show

删除所有定时任务 
python manage.py crontab remove

重启django服务。 
执行 
corntab -e 
应该是可以看到系统中创建了该定时任务。 
###################################################### Django认证######################################################
Django的权限是基于模型的，分为add/change/delete 从后台管理来看，是否方便，可以指定某个用户对某一种对象的增删改查权限。
为了方便，Django设置了组(group),组是权限的一种集合，一个user拥有了某一个组，则有了组内的所有权限。
# 在manage命令行创建账户，并设置密码
from django.contrib.auth.models import User
user = User.objects.create_user('liuqian3', 'liuqian3@yiche.com', 'liuqian3')
user.groups = [1,2,3,4,6,7]
user.save()

# 修改密码，由于密码是要加密后存储的，所以只能用set_password()：
from django.contrib.auth.models import User,Group
u = User.objects.get(username='fancq')
u.set_password('fancq758857')
u.save()
# 设置权限
u.groups = [1,2,3,4,6,7]
u.groups.add(group, group, ...)
u.groups.remove(group, group, ...)
u.groups.clear()
u.user_permissions = [61,62,63]
u.user_permissions.add(permission, permission, ...)
u.user_permissions.remove(permission, permission, ...)
u.user_permissions.clear()


# 创建组
group = Group.objects.create()
g1=Group.objects.get(id=2)
g1.permissions.add(permission_1,permission_2,...)

# 在视图层，Django已经有现成的权限控制组件，login_required()和permission_required()两个装饰器。顾名思义，前者验证是否登录，后者验证具体权限。
from django.contrib.auth.decorators import login_required,permission_required

@login_required(login_url='/accounts/login/')
def my_view(request):
    pass
	
@permission_required('push.add_headlines', login_url='/push/push_login/')
def my_view(request):
    pass

# 如果想自己写的权限控制那么Django提供了相应的视图权限控制API:user.is_staff/user.is_supperuser/user.is_active/user.has_perm()/user.has_module_perms()/user.get_all_permissions()
from django.contrib.auth.models import User
user=User.objects.get(username='hubo1')
user.has_perm('push.add_appindex')
True
user.has_module_perms('push')
True
user.get_all_permissions()
{u'push.add_appindex', u'push.add_channel'}
user.has_perms([u'push.add_appindex', u'push.add_channel'])
True
u.get_group_permissions()
# 同时还有模板中的权限控制，没有权限的用户不仅没有权限访问，甚至无法看到相关视图，这样用户的体验更好一些。下面是一些简单的例子。
当前登录的用户的权限存储在模板变量{{ perms }}中。这是个 django.contrib.auth.context_processors实例的封装，他是一个对于模板友好的权限代理。
在{{ perms }} 对象中，单一属性的查找是 User.has_module_perms的代理。如果已登录的用户在foo 应用中拥有任何许可，这个例子会显示 True：
{{ perms.foo }}
二级属性的查找是User.has_perm的代理。如果已登录的用户拥有foo.can_vote的许可，这个示例会显示True：
{{ perms.foo.can_vote }}
所以，你可以用模板的{% if %}语句检查权限：
{% if perms.foo %}
    <p>You have permission to do something in the foo app.</p>
    {% if perms.foo.can_vote %}
        <p>You can vote!</p>
    {% endif %}
    {% if perms.foo.can_drive %}
        <p>You can drive!</p>
    {% endif %}
{% else %}
    <p>You don't have permission to do anything in the foo app.</p>
{% endif %}
还可以通过{% if in %}语句查询权限。例如：
{% if 'foo' in perms %}
    {% if 'foo.can_vote' in perms %}
        <p>In lookup works, too.</p>
    {% endif %}
{% endif %}

# 如果需要更细粒度的权限控制，比方细化到不同的视图而不是模型，那么可以考虑在模型中自定义权限
class AppIndex(models.Model):
        dt=models.DateField()
        c_key=models.CharField(max_length=30)
        c_value=JSONField()
        class Meta:
                permissions=(
                ("app_active","Can visit app_active"),
                ("app_add","Can visit app_add"),
                ("app_retain","Can visit app_retain"),
                ("app_starts","Can visit app_starts"),
                ("app_channel","Can visit app_channel"),
                ("moduleuser","Can visit moduleuser"),
                ("app_stay","Can visit app_stay"),
                ("app_core","Can visit app_core"),
                ("app_core2","Can visit app_core2"),
                ("business","Can visit business"),
                ("app_business","Can visit app_business"),
                ("app_video","Can visit app_video"),
                ("app_media","Can visit app_media"),
                ("news_data","Can visit news_data"),
                ("posts_app","Can visit posts_app"),
                ("post_detail","Can visit post_dtail"),
                ("car_coin","Can visit car_coin"),
                )
				
# 或者用程序创建权限
虽然自定义的权限可以定义在模型的Meta类中，你还可以直接创建权限。例如，你可以为myapp中的BlogPost 创建can_publish权限：
from myapp.models import BlogPost
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
# 指定模型
content_type = ContentType.objects.get_for_model(BlogPost)
permission = Permission.objects.create(codename='can_publish',name='Can Publish Posts',content_type=content_type)

###################################################### Django会话######################################################
# django session的使用
下面这个简单的视图在一个用户提交一个评论后设置has_commented 变量为True。它不允许一个用户多次提交评论：

def post_comment(request, new_comment):
    if request.session.get('has_commented', False):
        return HttpResponse("You've already commented.")
    c = comments.Comment(comment=new_comment)
    c.save()
    request.session['has_commented'] = True
    return HttpResponse('Thanks for your comment!')
	
登录站点一个“成员”的最简单的视图：

def login(request):
    m = Member.objects.get(username=request.POST['username'])
    if m.password == request.POST['password']:
        request.session['member_id'] = m.id
        return HttpResponse("You're logged in.")
    else:
        return HttpResponse("Your username and password didn't match.")
下面是登出一个成员的视图，基于上面的login()：

def logout(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return HttpResponse("You're logged out.")
# echarts折线图和柱状图区别在于series.type=line | bar 
# 是簇状还是堆积在于有没有series.stack
# 是横向条形图还是纵向的区别在于xAxis.type=value |yAxis.type=category的配置
# 是环形图还是饼图的区别在于radius的取值范围


###################################################### Django管理######################################################
ModelAdmin.get_form(request, obj=None, **kwargs)¶
返回Admin中添加和更改视图使用的ModelForm 类，请参阅add_view() 和 change_view()。

其基本的实现是使用modelform_factory() 来子类化form，修改如fields 和exclude属性。所以，举个例子，如果你想要为超级用户提供额外的字段，你可以换成不同的基类表单，就像这样︰

# -- 更改表单显示
class MyModelAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            kwargs['form'] = MySuperuserForm
        return super(MyModelAdmin, self).get_form(request, obj, **kwargs)
		
		
# -- 更改外键查询集
def formfield_for_foreignkey(self, db_field, request, **kwargs):
       if db_field.name == "user_name":
               kwargs["queryset"] =User.objects.filter(username=request.user.username)
       return super(LogListAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

# -- 保存数据前加入数据
def save_model(self, request, obj, form, change):
		cleaned_data=form.clean()
		object_type= cleaned_data.get("object_type")
		object_name= cleaned_data.get("object_name")
		if object_type=='other' and object_name is null:
			from django import forms
			raise forms.ValidationError("对象为其他时，Name不可为空!")
		if object_type!='other':
			obj.object_id=1234
        obj.user_name = request.user
        obj.save()
	
# save_formset
ModelAdmin.save_formset(request, form, formset, change)
save_formset方法是给予HttpRequest，父ModelForm实例和基于是否添加或更改父对象的布尔值。

例如，要将request.user附加到每个已更改的formset模型实例：

class ArticleAdmin(admin.ModelAdmin):
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            instance.user = request.user
            instance.save()
        formset.save_m2m()
		
# -- 更改表单集	
class MyModelAdmin(admin.ModelAdmin):
    def get_changelist_formset(self, request, **kwargs):
        kwargs['formset'] = MyAdminFormSet
        return super(MyModelAdmin, self).get_changelist_formset(request, **kwargs)
	

# -- 验证相互依赖的字段
from django import forms
class ContactForm(forms.Form):
    # Everything as before.
    ...

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        cc_myself = cleaned_data.get("cc_myself")
        subject = cleaned_data.get("subject")

        if cc_myself and subject:
            # Only do something if both fields are valid so far.
            if "help" not in subject:
                raise forms.ValidationError("Did not send for 'help' in "
                        "the subject despite CC'ing yourself.")
						
						
workflow笔记
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# Create your models here.

class Employee(models.Model):
	user=models.ForeignKey(User,verbose_name='用户名',related_name='user_name')
	leader=models.ForeignKey(User,verbose_name='直接领导',related_name='leader_name')
	
	def __unicode__(self):
		return self.user
		
class Flow(models.Model):
	flow_type=models.CharField(max_length=20,verbose_name='流名称')
	c_dt=models.DateTimeField(auto_now=True,verbose_name='触发时间')
	initiator=models.ForeignKey(Employee,verbose_name='发起人',related_name='partner_name')
	remark=models.CharField(max_length=20,null=True,verbose_name='发起内容')
	state=models.CharField(max_length=20,verbose_name='流状态')
	executor=models.CharField(max_length=20,verbose_name='顺位审批人')
	
	def __unicode__(self):
		return self.flow_type

class FlowNode(models.Model):
	operator=models.ForeignKey(Employee,verbose_name='操作者',related_name='operator')
	c_dt=models.DateTimeField(auto_now=True,verbose_name='触发时间')
	operate=models.CharField(max_length=20,verbose_name='操作')
	remark=models.CharField(max_length=20,null=True,verbose_name='备注内容')
	flowid=models.ForeignKey(Flow,verbose_name='工作流ID')
	executor=models.CharField(max_length=20,verbose_name='顺位审批人')
	
	def __unicode__(self):
		return self.operator
		
	class Meta:
		ordering=['c_dt']


def flow_create(request):
	if request.method=='GET':
		form=FlowForm()
		return render(request,'flow_create.html',{'form':form})
	elif request.method=='POST':
		form=FlowForm(request.POST) 
		if form.is_valid():
			flow_type=form.cleaned_data['flow_type']
			remark=form.cleaned_data['remark']
			initiator=request.user
			executor=initiator.leader
			obj=models.Flow(flow_type=flow_type,
								initiator=request.user,
								remark=remark,
								state='init',
								executor=executor)
			obj.save()
			obj_node=obj.flownode_set.create(operator=initiator,
									operate='init',
									remark=remark,
									executor=executor)
									
def flow_list_0(request):
	data=Flow.objects.all(initiator=request.user)
	
def flow_list_1(request):
	data=Flow.objects.all(executor=request.user)
	
def flow_detail(request,id):
	data=FlowNode.object.filter(flow_id=id)
			

视图：
1.新建任务--add--
2.待审批的任务（等待审批的任务）
# 3.已审批的任务（我已审批的任务）
# 4.提交审批的任务（由我提交且未完成的任务）
# 5.审批完成的任务（由我提交且已完成的任务）

state:审批中、完成、驳回
operate:提交、同意、驳回
# 更新数据
class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Entry(models.Model):
    blog = models.ForeignKey(Blog)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    authors = models.ManyToManyField(Author)
    n_comments = models.IntegerField()
    n_pingbacks = models.IntegerField()
    rating = models.IntegerField()
	
b = Blog.objects.get(id=1)
e = b.entry_set.create(
    headline='Hello',
    body_text='Hi',
    pub_date=datetime.date(2005, 1, 1)
)

product = Product.objects.get(name='Venezuelan Beaver Cheese')
product.number_sold += 1
product.save()

from django.contrib.auth.models import User
from flow.models import Flow,FlowNode,Employee
# 发起人信息从request.user中获取,通过i获取employee对象

u=Employee.objects.get(user=request.user)
<Employee: Employee object>
u.user
<User: rencs>
u.leader
<User: wangbin>
# 分别保存工作流和工作流节点两个对象
obj=Flow(flow_type='work',initiator=u.user,remark='test',state='init',executor=u.leader)
obj.save()

obj_node=FlowNode(operator=u.user,operate='init',remark='test',flowid=obj,executor=u.leader)
obj_node.save()
# 以上是用户创建表单时候的初始化，用户和用户leader数据从request.user取
# 以下是用户leader的审批，工作流id从url中传入，obj=Flow.objects.get(id=obj.id)
u2=Employee.objects.get(user=request.user)
# 从url中获取当前审批工作流的id,获取工作流对象，leader审批后新增一条工作流节点信息。并更新当前工作流对象。
obj=Flow.objects.get(id=obj.id)
obj_node2=FlowNode(operator=u2.user,operate='ok',remark='test',flowid=obj,executor=u2.leader)
obj_node2.save()

obj.state='doing'
obj.executor=u2.leader
obj.save()

def get_absolute_url(self):
	return reverse('app_tem', args=(self.chart_key,))
	
class="table table-bordered table-hover table-responsive"

判断一个对象是否在一个多对多对象中:
# user_list是一个多用户对象，u是一个单用户对象
from push.models import AppDaily
obj=AppDaily.objects.get(daily_key='car_daily')
obj.daily_emails.all()
<QuerySet [<User: wangbin>, <User: wangshuai6>, <User: fancq>]>
user_list=obj.daily_emails.all()
from django.contrib.auth.models import User
u=User.objects.get(id=2)
u in user_list
True

###################################################### django自带分页功能 ###################################################### 
# views.py
后端分页		
def data_to_table():
	try:
		page=int(request.GET.get('page','1'))
		if page < 1:
			page=1
	except ValueError:
		page=1
	page=1
	winlog_list =AppAdd.objects.filter(date__gte=start_init.strftime('%Y-%m-%d'),date__lte=end_init.strftime('%Y-%m-%d'))
	paginator = Paginator(winlog_list, 10)
	try:
		winloglist = paginator.page(page)
	except (EmptyPage,InvalidPage,PageNotAnInteger):
		winloglist = paginator.page(1)
	except EmptyPage:
		winloglist = paginator.page(paginator.num_pages)
	return render_to_response('table_chart_tem.htm', {'winloglist':winloglist})

# table_chart_tem.htm

<table class="table table-hover">
   <thead>
      <tr>
         <th>日期</th>
         <th>adr_add</th>
		 <th>ios_add</th>
      </tr>
   </thead>
   <tbody>
{% for winlog in winloglist.object_list %}
      <tr>
         <td>{{ winlog.date  }}</td>
         <td>{{ winlog.adr_add }}</td>
		 <td>{{ winlog.ios_add }}</td>
      </tr>
	  {% endfor %}
   </tbody>
</table>
<ul class="pagination">
{% if winloglist.has_previous %}
<li><a href="?page={{ winloglist.previous_page_number }}" title="上一页"><span class="glyphicon glyphicon-backward"></span></a></li>
{% endif %}
{% for p in winloglist.paginator.page_range %}
{% ifequal p winloglist.number %}
<li><span>{{p}}</span></li>
{% else %}
<li><a href="?page={{p}}" title="第{{p}}页">{{p}}</a></li>
{% endifequal %}
{% endfor %}
{% if winloglist.has_next %}
<li><a href="?page={{ winloglist.next_page_number }}" title="下一页"><span class="glyphicon glyphicon-forward"></span></a> </li>
{% endif %}

# 关于表单的显示问题
{% if request.user in obj.executor_group or request.user == obj.executo %}
{% endif %}
if request.user==obj.executor or request.user==obj.executor_group
<p class="pull-right"> <span class="label label-default">创建者：{{flow.initiator.first_name}}</span></p>
# 百分数、小数的表示。
'%.1f'%(100*float(item['posts_entry'])/item['community_tab'])