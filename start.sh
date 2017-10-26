#!/usr/bin/env bash
export FLASK_CONFIG=production
export SQLALCHEMY_DATABASE_URI=mysql://manager:toor@localhost/flask01
export FLASK_APP=run.py
export SECRET_KEY=someverysecretkeyagainst
/usr/bin/python run.py

