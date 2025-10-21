# student_management_system_in_django
student_management_system_in_django


<h4>Login</h4>
<pre>
adminx2@gmail.com
adminx2
</pre>

<p>Project Dependency :</p>
<pre>
pip install requests
pip install Django
pip install mysql-client
pip install mysqlclient
</pre>
<hr>
<ul>
<ol>Change Database Setting in settings.py </ol>
<ol>
Run Migration Command 
<pre>
python manage.py makemigrations
python manage.py migrate
</pre>
 <ul>     
<li>In login_page.html Replace <pre>CAPTCHA_CLIENT_KEY</pre> with Captcha Client Side Key</li>
<li>In views.py Replace <pre>CAPTCHA_SERVER_KEY</pre> with Captcha SERVER Side Key</li>
<li>For Captcha Key Visit <a href="https://www.google.com/recaptcha/intro/v3.html">https://www.google.com/recaptcha/intro/v3.html</a></li>
</ul>
</ol>
<ol>
Run Project python runserver
</ol>
</ul>
<hr>