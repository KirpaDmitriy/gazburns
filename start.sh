mkdir pictures
JWT_SECRET_KEY=njhkgjfhjklhkjg FS_HOST=http://81.94.150.144:8000/files DATABASE_PORT=5432 PICTURES_FOLDER=/home/ubuntu/gazburns/pictures FONT_PATH=/home/ubuntu/gazburns/arial.ttf DATABASE_USER=myuser DATABASE_PASSWORD=mypassword DATABASE_HOST=localhost DATABASE_NAME=mydb uvicorn main:app --host 0.0.0.0
