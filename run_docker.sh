#!/usr/bin/env bash

docker run myocsaf

#docker run -e [FLASK_APP=run.py,PYTHONUNBUFFERED=1,SQLALCHEMY_DATABASE_URI=mysql://root:password@127.0.0.1/flask01,FLASK_CONFIG=production,SECRET_KEY=myverylongsecretkey] myocsaf

#docker exec 614c0fb7d36b python run.py

#docker exec -e [FLASK_APP=run.py,PYTHONUNBUFFERED=1,SQLALCHEMY_DATABASE_URI=mysql://root:password@127.0.0.1/flask01,FLASK_CONFIG=production,SECRET_KEY=myverylongsecretkey] myocsaf python run.py

#docker run -e [FLASK_APP=run.py,PYTHONUNBUFFERED=1,SQLALCHEMY_DATABASE_URI=mysql://root:password@127.0.0.1/flask01,FLASK_CONFIG=production,SECRET_KEY=myverylongsecretkey] -d -p 90:90 myocsaf

#docker exec -it -e [FLASK_APP=run.py,PYTHONUNBUFFERED=1,SQLALCHEMY_DATABASE_URI=mysql://root:password@127.0.0.1/flask01,FLASK_CONFIG=production,SECRET_KEY=myverylongsecretkey] myocsaf bash

