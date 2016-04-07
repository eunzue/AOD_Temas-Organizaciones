# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template
from flask import session
from app import app
import config as configuracion
import json
#import requests
from flask import Response
import urllib2
import BBDDAODTemasOrganizaciones as dao
from flask import request
from flask.ext.paginate import Pagination


def __init__():
	conexionBBDD=configuracion.conexion()
	

def __total_datasets_por_organizacion(organizacion, cursor):
	consulta= "SELECT COUNT (package_revision.*) FROM public.package_revision, public.group_revision WHERE group_revision.id = package_revision.owner_org AND group_revision.state='active' AND group_revision.current=TRUE AND is_organization=TRUE AND package_revision.current=TRUE AND package_revision.state='active' AND package_revision.type='dataset' AND group_revision.name = '"+organizacion.strip()+"';"
	q=cursor.execute(consulta)
	resultado = cursor.fetchone()
	if resultado is not None:
		return int(resultado[0])
	return 0

def __total_datasets_por_tema(tema, cursor):
	consulta= "SELECT COUNT (package_revision.*) FROM public.package_revision, public.group_revision, public.member_revision WHERE group_revision.id = member_revision.group_id AND member_revision.state='active' AND group_revision.state='active' AND group_revision.current=TRUE AND is_organization=FALSE AND member_revision.table_id = package_revision.id AND member_revision.table_name='package' AND member_revision.state='active' AND package_revision.current=TRUE AND package_revision.state='active' AND package_revision.type='dataset'  AND group_revision.name = '"+tema.strip()+"';"
	q=cursor.execute(consulta)
	resultado = cursor.fetchone()
	if resultado is not None:
		return int(resultado[0])
	return 0


'''
	Devuelve en json todo los datos necesarios para la página de home de las organizaciones contiene cada elemento del array {'titulo':TituloOrganizacion, 'URL':urlInternaOrganizacion, 'descripcion':descripcionOrganizacion, 'numeroDatasets':220}
'''
@app.route("/api/organizaciones_home")
def organizacionesHome():
	conexionBBDD=configuracion.conexion()
	cursor= conexionBBDD.cursor()
	
	consulta= "SELECT group_revision.title, group_revision.name, group_revision.description, COUNT(package_revision.*) FROM public.group_revision, public.package_revision, public.\"user\" WHERE group_revision.id = package_revision.owner_org AND package_revision.current=TRUE AND package_revision.state='active' AND public.group_revision.title = \"user\".fullname AND group_revision.state='active' AND group_revision.current=TRUE AND is_organization=TRUE GROUP BY  group_revision.title, group_revision.name,  group_revision.description ORDER BY group_revision.title DESC;"
	
	q=cursor.execute(consulta)
	organizaciones = cursor.fetchall()
	devolver = []
	if organizaciones is not None:
			for organizacion in organizaciones:
				org_home_json = {
					'titulo':organizacion[0],
					'name': organizacion[1],
					'descripcion':organizacion[2],
					'numeroDatasets':organizacion[3]
				}
				devolver.append(org_home_json)
	cursor.close()
	conexionBBDD.close()
	
	js = json.dumps(devolver)
	resp = Response(js, status=200, mimetype='application/json')
	return resp

'''
	Devuelve en json todo los datos necesarios para la página de home de los temas contiene cada elemento del array {'titulo':TituloTema, 'URL':urlInternaTema, 'descripcion':descripcionTema, 'numeroDatasets':220}
'''
@app.route("/api/temas_home")
def temasHome():
	conexionBBDD=configuracion.conexion()
	cursor= conexionBBDD.cursor()
	
	consulta= "SELECT group_revision.title, group_revision.name, group_revision.description, COUNT(package_revision.*) FROM public.group_revision, public.member_revision, public.package_revision WHERE group_revision.id = member_revision.group_id AND member_revision.state='active' AND group_revision.state='active' AND group_revision.is_organization = FALSE AND   group_revision.current=TRUE AND member_revision.current=TRUE AND package_revision.current=TRUE AND member_revision.table_id = package_revision.id AND member_revision.table_name='package' AND package_revision.state='active' GROUP BY  group_revision.title, group_revision.name,  group_revision.description ORDER BY group_revision.title ASC;"
	
	q=cursor.execute(consulta)
	temas = cursor.fetchall()
	devolver = []
	if temas is not None:
			for tema in temas:
				tema_home_json = {
					'titulo':tema[0],
					'name': tema[1],
					'descripcion':tema[2],
					'numeroDatasets':tema[3]
				}
				devolver.append(tema_home_json)
	cursor.close()
	conexionBBDD.close()
	js = json.dumps(devolver)
	resp = Response(js, status=200, mimetype='application/json')
	return resp
	

'''
	Devuelve en un array toda los dataset de las organizaciones. Los datasets son {'titulo':TituloConjuntoDeDatos, 'URL': urlConjuntoDeDatosCKAN, 'numeroAccesos':325, 'ultimaActualizacion':04.04.2016}
'''
def __datasets_organizacion(organizacion, cursor):
	consulta= "SELECT package_revision.title, CONCAT('http://opendata.aragon.es/catalogo/',package_revision.name), tracking_summary.running_total, TO_CHAR(package_revision.revision_timestamp, 'DD.MM.YYYY') FROM public.package_revision, public.group_revision, public.tracking_summary WHERE group_revision.id = package_revision.owner_org AND group_revision.state='active' AND group_revision.current=TRUE AND is_organization=TRUE AND package_revision.current=TRUE AND package_revision.state='active' AND package_revision.type='dataset' AND package_revision.id = \"tracking_summary\".package_id AND tracking_date =( SELECT MAX(tracking_date) FROM tracking_summary WHERE package_id = package_revision.id) AND group_revision.name = '"+organizacion.strip()+"' ORDER BY package_revision.revision_timestamp DESC;"
	
	q=cursor.execute(consulta)
	datasets = cursor.fetchall()
	devolver = []
	if datasets is not None:
			for dataset in datasets:
				datasets_json = {
					'titulo':dataset[0],
					'URL':dataset[1],
					'numeroAccesos':dataset[2],
					'ultimaActualizacion':dataset[3]
				}
				devolver.append(datasets_json)
	cursor.close()
	js = json.dumps(devolver)
	resp = Response(js, status=200, mimetype='application/json')
	return resp

'''
	Devuelve en un json todo los datos necesarios para la página de una organización. El json contiene {'titulo': tituloOrganizacion, 'URL':urlDeLaOrganizacion, 'descripcion':Descripción, 'direccion':DirecciónFísica, 'responsable': PersonaResponsable, 'email':email, 'totalConjuntosDeDatos':33, 'conjuntosDeDatos':[{},...]}
'''
@app.route("/api/organizacion/<organizacion>")
def obtenOrganizacion(organizacion):
	conexionBBDD=configuracion.conexion()
	cursor= conexionBBDD.cursor()
	devolver =[]
	consulta1="SELECT group_revision.title, group_revision.description, \"user\".email, COUNT (package_revision.*) FROM public.group_revision, public.\"user\", public.package_revision WHERE group_revision.id = package_revision.owner_org AND public.group_revision.title = \"user\".fullname AND group_revision.state='active' AND group_revision.current=TRUE AND is_organization=TRUE AND package_revision.current=TRUE AND package_revision.state='active' AND package_revision.type='dataset'  AND public.group_revision.name ='"+organizacion.strip()+"' GROUP BY group_revision.title, group_revision.description, \"user\".email;"
	q=cursor.execute(consulta1)
	resultado1 = cursor.fetchone()
	if resultado1 is not None:
		consulta2 = "SELECT group_extra_revision.key, group_extra_revision.value FROM public.group_extra_revision, public.group_revision WHERE group_revision.state='active' AND group_revision.current=TRUE AND is_organization=TRUE AND group_extra_revision.state='active' AND group_extra_revision.current=TRUE AND (group_extra_revision.key = 'webpage' OR group_extra_revision.key = 'address' OR group_extra_revision.key = 'person') AND group_extra_revision.group_id = group_revision.id AND group_revision.name = '"+organizacion.strip()+"' ;";
		urlOrganizacion=''
		direccionOrganizacion=''
		responsableOrganizacion=''
		q=cursor.execute(consulta2)
		extras = cursor.fetchall()
		if extras is not None:
			for extra in extras:
				if extra[0]=='webpage':
					urlOrganizacion=extra[1]
				elif extra[0]=='person':
					responsableOrganizacion=extra[1]
				elif extra[0]=='address':
					direccionOrganizacion=extra[1]
		datasets=[]
		datasets =__datasets_organizacion(organizacion, cursor)
		organizacion_json = {
			'name': organizacion,
			'titulo': resultado1[0],
			'URL': urlOrganizacion,
			'descripcion':resultado1[1],
			'direccion': direccionOrganizacion,
			'responsable': responsableOrganizacion,
			'email': resultado1[2],
			'totalConjuntosDeDatos': resultado1[3],
			'conjuntosDeDatos': datasets
		}
		
	cursor.close()
	conexionBBDD.close()
	js = json.dumps(devolver)
	resp = Response(js, status=200, mimetype='application/json')
	return resp





'''
	Devuelve en un array todo los dataset del tema. Los datasets son {'titulo':TituloConjuntoDeDatos, 'URL': urlConjuntoDeDatosCKAN, 'numeroAccesos':325, 'ultimaActualizacion':04.04.2016}
'''
def __datasets_temas(tema, cursor):
	
	consulta= "SELECT package_revision.title, CONCAT('http://opendata.aragon.es/catalogo/',package_revision.name), tracking_summary.running_total, TO_CHAR(package_revision.revision_timestamp, 'DD.MM.YYYY') FROM public.package_revision, public.group_revision, public.tracking_summary, public.member_revision WHERE group_revision.id = member_revision.group_id AND member_revision.state='active' AND group_revision.state='active' AND group_revision.current=TRUE AND is_organization=FALSE AND member_revision.table_id = package_revision.id AND member_revision.table_name='package' AND member_revision.state='active' AND   package_revision.current=TRUE AND package_revision.state='active' AND package_revision.type='dataset' AND package_revision.id = \"tracking_summary\".package_id AND tracking_date =( SELECT MAX(tracking_date) FROM tracking_summary WHERE package_id = package_revision.id) AND group_revision.name = '"+tema.strip()+"'  ORDER BY package_revision.revision_timestamp DESC;"
	q=cursor.execute(consulta)
	datasets = cursor.fetchall()
	devolver = []
	if datasets is not None:
			for dataset in datasets:
				datasets_json = {
					'titulo':dataset[0],
					'URL':dataset[1],
					'numeroAccesos':dataset[2],
					'ultimaActualizacion':dataset[3]
				}
				devolver.append(datasets_json)
	cursor.close()
	js = json.dumps(devolver)
	resp = Response(js, status=200, mimetype='application/json')
	return resp



'''
	Devuelve en un json todo los datos necesarios para la página de un tema. El json contiene {'titulo': tituloTema, 'descripcion':Descripción, 'totalConjuntosDeDatos':33, 'conjuntosDeDatos':[{},...]}
'''
@app.route("/api/tema/<tema>")
def obtenTema(tema):
	conexionBBDD=configuracion.conexion()
	cursor= conexionBBDD.cursor()
	consulta="SELECT group_revision.title, group_revision.description, COUNT (package_revision.*) FROM public.package_revision, public.group_revision, public.member_revision WHERE group_revision.id = member_revision.group_id AND member_revision.state='active' AND group_revision.state='active' AND group_revision.current=TRUE AND is_organization=FALSE AND member_revision.table_id = package_revision.id AND member_revision.table_name='package' AND member_revision.state='active' AND package_revision.current=TRUE AND package_revision.state='active' AND package_revision.type='dataset'  AND group_revision.name = '"+tema.strip()+"' GROUP BY group_revision.title, group_revision.description;"
	
	q=cursor.execute(consulta)
	temas = cursor.fetchone()
	if temas is not None:
		datasets = __datasets_temas(tema, cursor)
		tema_json = {
			'titulo': temas[0],
			'name': tema,
			'descripcion':temas[1],
			'totalConjuntosDeDatos': temas[2],
			'conjuntosDeDatos': datasets
		}
		
	cursor.close()
	conexionBBDD.close()
	js = json.dumps(devolver)
	resp = Response(js, status=200, mimetype='application/json')
	return resp





@app.route("/organizacion")
def homeOrganizacion():
	organizaciones = dao.home('organizacion')
	return render_template('indexOrganizacion.html', organizaciones=organizaciones)
	
@app.route("/tema")
def hometema():
	temas = dao.home('tema')
	return render_template('indexTema.html', temas=temas)

@app.route("/organizacion/<nombre_organizacion>")
def verOrganizacion(nombre_organizacion):
	
	
	organizacion = dao.obtenOrganizacion(nombre_organizacion)
	
	return render_template('verOrganizacion.html', organizacion=organizacion)

@app.route("/tema/<nombre_tema>")
def verTema(nombre_tema):
	
	
	tema = dao.obtenTema(nombre_tema)
	
	return render_template('verTema.html', tema=tema)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('error_document_template.html', elerror='No existe p&aacute;gina')








