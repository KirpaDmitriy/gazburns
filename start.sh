mkdir pictures
cd pictures
python -m http.server 9000 &
cd ..
JWT_SECRET_KEY=njhkgjfhjklhkjg FS_HOST=http://81.94.150.144:9000 DATABASE_PORT=5432 DATABASE_USER=myuser DATABASE_PASSWORD=mypassword DATABASE_HOST=localhost DATABASE_NAME=mydb uvicorn main:app --host 0.0.0.0
