import os
print(os.getcwd())
os.chdir('MyProject')
print(os.getcwd())
os.system('python manage.py runserver')
