# FAYG

1. **Create a Virtual Environment Initially**  
command: **python -m venv env**  

2. **Switch to Virtual Environment on Windows**  
command: **.\env\Scripts\activate**  

3. **Install all dependencies required for the project**  
command: **pip install -r requirements.txt**  

4. **Switch to app directory**  

5. **Initiate Db Migrations to Generate Tables**  
command: **python manage.py makemigrations**  
command: **python manage.py migrate**  

6. **Create Superuser (Admin)**  
command: **python manage.py createsuperuser**  

7. **Run Server**  
command: **python manage.py runserver**  
The above command will run django server on localhost i.e. 127.0.0.1:8000/  

8. **Access Admin Panel**  
command: **127.0.0.1:8000/admin**  
