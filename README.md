# Laboratorio---Python---Password-Evolution.-

## Terminal codes
iniciar servidor flask
```s
nohup python3 password-evolution.py &
```
kill servidor flask
```s
pkill -f password-evolution.py
```
### Registro de ususarios Text Plain
```
curl -k -X POST -F 'username=alice' -F 'password=myalicepassword' 'https://0.0.0.0:5000/signup/v1'
```
se cambia el user name y password para agregar otro
### Login usuarios con su passoord Text Plain
```
curl -k -X POST -F 'username=alice' -F 'password=myalicepassword' 'https://0.0.0.0:5000/signup/v1'
```
se cambia el user name y password para agregar otro

### Registro con hash 
```s
curl -k -X POST -F 'username=rick' -F 'password=samepassword' 'https://0.0.0.0:5000/signup/v2'
```
### Logeo con hash?
```s
curl -k -X POST -F 'username=rick' -F 'password=samepassword' 'https://0.0.0.0:5000/login/v2'
```

## Librerias
```py
import pyotp #Genera contrase;as de un solo uso?
import sqlite3 #data base para nombres de usuarios y contrase;as
import hashlib #seguridad para hash y resumenes de mensajes. 
import uuid #for para crear identificadores universales unicos de la importacion flask.
from flask import Flask, request
```
