# AOD_Temas-Organizaciones
Aplicación web que mostrará los temas y organizaciones de nuestro portal de [Aragón Open Data](http://opendata.aragon.es)

##Información técnica

Nuestra app es una aplicación web Python usando el framework [Flask](http://flask.pocoo.org/), y PostgreSQL como base de datos. En el ecosistema de Aragón Open Data hacemos uso del servidor web Apache2. Al hacer uso de la base de datos del portal [Aragón Open Data](http://opendata.aragon.es) no es necesario haber hecho la instalación de nuestro [CKAN](https://github.com/aragonopendata/Aragon-Open-data-Website) con tener la base de datos instalada sería suficiente, pero recomendamos hacer la instalación.

La app es una aplicación web Python usando el framework [Flask](http://flask.pocoo.org/), y [PostgreSQL](http://www.postgresql.org/) como base de datos. En el ecosistema de Aragón Open Data hacemos uso del servidor web Apache2.

Para gestionar las depencias, usamos el gestor de dependencias `pip`, que puedes instalar en Linux con:

```
curl https://bootstrap.pypa.io/get-pip.py > get-pip.py
sudo python get-pip.py
```

Recomendamos aislar el entorno de desarrollo Python con `virtualenv`:

```
sudo pip install virtualenv
cd /path_de_app
virtualenv AOD_Rules
```


```
No olvides modificar el fichero `app/config.py` con tus datos de conexión a base de datos si los has modificado.

Creamos el entorno para con el que se instalaran las dependencias, en el directorio donde tenemos la app

`virtualenv AOD_Rules`

Para poder instalar la dependecia y manejar bases de datos de PostgreSQL se necesita instalar un software especifico:

```
sudo apt-get install libpq-dev
sudo apt-get install libevent-dev
sudo apt-get install build-essential autoconf libtool pkg-config python-opengl python-imaging python-pyrex python-pyside.qtopengl idle-python2.7 qt4-dev-tools qt4-designer libqtgui4 libqtcore4 libqt4-xml libqt4-test libqt4-script libqt4-network libqt4-dbus python-qt4 python-qt4-gl libgle3 python-dev

```

Para instalar las dependencias de las librerías Python:

```
AOD_Rules/bin/pip install requisites/argparse-1.4.0.tar.gz
AOD_Rules/bin/pip install requisites/itsdangerous-0.24.tar.gz
AOD_Rules/bin/pip install requisites/MarkupSafe-0.23.tar.gz
AOD_Rules/bin/pip install requisites/Werkzeug-0.11.3.tar.gz
AOD_Rules/bin/pip install requisites/Jinja2-2.8.tar.gz
AOD_Rules/bin/pip install requisites/wsgiref-0.1.2.zip
AOD_Rules/bin/pip install requisites/Flask-0.10.1.tar.gz
AOD_Rules/bin/pip install requisites/psycopg2-2.6.1.tar.gz

```

###Arrancar la aplicación

Arrancamos la aplicación con:

```

/path_de_app/AOD_Rules/bin/python /path_de_app/run.py &

```

Ojo que el run.py esta la aplicación para que arranque en modo debug, se recomienda quitarlo para entornos de producción.

####Cerrar la aplicación

Ejecutamos el siguiente comando para cerrar la app:

```

killall /path_de_app/AOD_Rules/bin/python

```


