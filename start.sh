mkdir pictures
JWT_SECRET_KEY=njhkgjfhjklhkjg FS_HOST=http://81.94.150.144:9000 DATABASE_PORT=5432 PICTURES_FOLDER=/home/ubuntu/gazburns/pictures DATABASE_USER=myuser DATABASE_PASSWORD=mypassword DATABASE_HOST=localhost DATABASE_NAME=mydb uvicorn main:app --host 0.0.0.0
