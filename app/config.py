# -*- coding: utf-8 -*-
import psycopg2

AOD_TEMAS_ORGANIZACIONES_HOST						= 'localhost'
AOD_TEMAS_ORGANIZACIONES_DB_NAME 				= 'ckan_default'
AOD_TEMAS_ORGANIZACIONES_PORT						= '5432'
AOD_TEMAS_ORGANIZACIONES_USER						= 'ckan_default'
AOD_TEMAS_ORGANIZACIONES_PASSWORD				= 'ckan_default'

AOD_TEMAS_ORGANIZACIONES_CONEXION_BBDD	= "host='"+AOD_TEMAS_ORGANIZACIONES_HOST+"' dbname='"+AOD_TEMAS_ORGANIZACIONES_DB_NAME+"' port='"+AOD_TEMAS_ORGANIZACIONES_PORT+"' user='"+AOD_TEMAS_ORGANIZACIONES_USER+"' password='"+AOD_TEMAS_ORGANIZACIONES_PASSWORD+"'"

def conexion():
	return psycopg2.connect(AOD_TEMAS_ORGANIZACIONES_CONEXION_BBDD)
