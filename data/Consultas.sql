--Preparar la base de datos

sudo -u postgres psql postgres

CREATE user ckan_default password 'ckan_default';

ALTER ROLE ckan_default WITH SUPERUSER;

CREATE DATABASE ckan_default WITH OWNER ckan_default;

GRANT ALL PRIVILEGES ON DATABASE ckan_default TO ckan_default;
\q

psql -h localhost -d ckan_default -U ckan_default -f dump.sql


DROP DATABASE ckan_default;



OPENDATA_POSTGRE_CONEXION_BD="host='localhost' dbname='ckan_default'  port='5432' user='ckan_default' password='ckan_default'"


--Hay que corregir algunos datos
SELECT * FROM public.user WHERE fullname='Secretaría General Técnica de Educación, Universidad, Cultura y Deporte';


UPDATE public.user
SET fullname='Secretaría General Técnica de Educación, Cultura y Deporte'
WHERE fullname='Secretaría General Técnica de Educación, Universidad, Cultura y Deporte';

SELECT * FROM public.group_revision WHERE name = 'secretaria_general_tecnica_de_educacion_cultura_y_deportes';
SELECT * FROM public.group WHERE name = 'secretaria_general_tecnica_de_educacion_cultura_y_deportes';

UPDATE public.group_revision
SET title='Secretaría General Técnica de Educación, Cultura y Deporte',name = 'secretaria_general_tecnica_de_educacion_cultura_y_deporte'
WHERE name = 'secretaria_general_tecnica_de_educacion_cultura_y_deportes';

UPDATE public.group
SET title='Secretaría General Técnica de Educación, Cultura y Deporte', name = 'secretaria_general_tecnica_de_educacion_cultura_y_deporte'
WHERE name = 'secretaria_general_tecnica_de_educacion_cultura_y_deportes';


--Consultas para la aplicacion

--Toda las organizaciones
SELECT 
* 
FROM 
  public.group_revision
WHERE group_revision.state='active' AND group_revision.current=TRUE AND is_organization=TRUE;

--Todo los datos que necesitamos para pintar las plantillas. Necesitamos el nombre, la descripcion, nº de datasets, contacto (mail)
SELECT 
  group_revision.title, CONCAT('/organizacion/',group_revision.name), 
  group_revision.description,
  COUNT(package_revision.*)
FROM 
  public.group_revision, 
  public.package_revision, 
  public."user"
WHERE 
  group_revision.id = package_revision.owner_org AND package_revision.current=TRUE AND package_revision.state='active' AND
  public.group_revision.title = "user".fullname AND group_revision.state='active' AND group_revision.current=TRUE AND is_organization=TRUE
GROUP BY  group_revision.title, group_revision.name,  group_revision.description
ORDER BY group_revision.title DESC;


--Los datos para una organizacion.
--Los datos referentes a la organizacion
SELECT 
  group_revision.title, group_revision.description, "user".email, COUNT (package_revision.*)
FROM 
  public.group_revision, 
  public."user", public.package_revision
WHERE
  group_revision.id = package_revision.owner_org AND public.group_revision.title = "user".fullname AND group_revision.state='active' AND group_revision.current=TRUE AND is_organization=TRUE AND package_revision.current=TRUE AND package_revision.state='active' AND package_revision.type='dataset'  AND public.group_revision.name ='direccion_general_de_administracion_electronica_y_sociedad_de_la_informacion'
GROUP BY group_revision.title, group_revision.description, "user".email;

--Los datasets necesarios para una organizacion
--Revisar que pasa con las que no se han visto y las fechas
SELECT 
  package_revision.title, CONCAT('http://opendata.aragon.es/catalogo/',package_revision.name), TO_CHAR(package_revision.revision_timestamp, 'DD.MM.YYYY'), tracking_summary.running_total 
FROM 
  public.package_revision, 
  public.group_revision, public.tracking_summary
WHERE 
  group_revision.id = package_revision.owner_org AND group_revision.state='active' AND group_revision.current=TRUE AND is_organization=TRUE AND
  package_revision.current=TRUE AND package_revision.state='active' AND package_revision.type='dataset' AND package_revision.id = "tracking_summary".package_id AND tracking_date =( SELECT MAX(tracking_date) FROM tracking_summary WHERE package_id = package_revision.id) AND group_revision.name = 'direccion_general_de_administracion_electronica_y_sociedad_de_la_informacion' 
 ORDER BY package_revision.revision_timestamp DESC;


SELECT 
  package_revision.title, CONCAT('http://opendata.aragon.es/catalogo/',package_revision.name), tracking_summary.running_total, TO_CHAR(package_revision.revision_timestamp, 'DD.MM.YYYY')
FROM 
  public.package_revision, 
  public.group_revision, public.tracking_summary
WHERE 
  group_revision.id = package_revision.owner_org AND group_revision.state='active' AND group_revision.current=TRUE AND is_organization=TRUE AND
  package_revision.current=TRUE AND package_revision.state='active' AND package_revision.type='dataset' AND package_revision.id = "tracking_summary".package_id AND tracking_date =( SELECT MAX(tracking_date) FROM tracking_summary WHERE package_id = package_revision.id) AND group_revision.name = 'direccion_general_de_administracion_electronica_y_sociedad_de_la_informacion' 
 ORDER BY package_revision.revision_timestamp DESC;



--Total de dataset para la organizacion
SELECT 
   COUNT (package_revision.*)
FROM 
  public.package_revision, 
  public.group_revision
WHERE 
  group_revision.id = package_revision.owner_org AND group_revision.state='active' AND group_revision.current=TRUE AND is_organization=TRUE AND
  package_revision.current=TRUE AND package_revision.state='active' AND package_revision.type='dataset'  AND group_revision.name = 'direccion_general_de_administracion_electronica_y_sociedad_de_la_informacion';

--Obtener los extras de una organizacion
SELECT 
  group_extra_revision.key, group_extra_revision.value 
FROM 
  public.group_extra_revision, 
  public.group_revision
WHERE 
  group_revision.state='active' AND group_revision.current=TRUE AND is_organization=TRUE AND
  group_extra_revision.state='active' AND group_extra_revision.current=TRUE AND 
  (group_extra_revision.key = 'webpage' OR group_extra_revision.key = 'address' OR group_extra_revision.key = 'person') AND
  group_extra_revision.group_id = group_revision.id AND group_revision.name = 'direccion_general_de_administracion_electronica_y_sociedad_de_la_informacion' ;




--Lo mismo para los temas
SELECT 
* 
FROM 
  public.group_revision
WHERE group_revision.state='active' AND group_revision.current=TRUE AND is_organization=FALSE;

--Todo los datos que necesitamos para pintar las plantillas. Necesitamos el nombre, la descripcion, nº de datasets
SELECT 
  group_revision.title, CONCAT('/tema/',group_revision.name),  
  group_revision.description,
  COUNT(package_revision.*)
FROM 
  public.group_revision, 
  public.member_revision, 
  public.package_revision
WHERE 
  group_revision.id = member_revision.group_id AND member_revision.state='active' AND group_revision.state='active' AND group_revision.is_organization = FALSE AND
  group_revision.current=TRUE AND member_revision.current=TRUE AND package_revision.current=TRUE AND
  member_revision.table_id = package_revision.id AND member_revision.table_name='package' AND package_revision.state='active' 
GROUP BY  group_revision.title, group_revision.name,  group_revision.description
ORDER BY group_revision.title ASC;


--Los datos referentes para un tema en concreto
SELECT 
  group_revision.title, group_revision.description
FROM 
  public.group_revision
WHERE 
  group_revision.state='active' AND group_revision.current=TRUE AND is_organization=FALSE AND public.group_revision.name ='ciencia-tecnologia';


--Total de dataset del tema
SELECT 
   COUNT (package_revision.*)
FROM 
  public.package_revision, 
  public.group_revision, public.member_revision
WHERE 
  group_revision.id = member_revision.group_id AND member_revision.state='active' AND group_revision.state='active' AND group_revision.current=TRUE AND is_organization=FALSE AND member_revision.table_id = package_revision.id AND member_revision.table_name='package' AND member_revision.state='active' AND
  package_revision.current=TRUE AND package_revision.state='active' AND package_revision.type='dataset'  AND group_revision.name = 'ciencia-tecnologia';
  
  
--Los datasets necesarios para un tema
--Revisar que pasa con las que no se han visto y las fechas
SELECT 
  package_revision.title, CONCAT('http://opendata.aragon.es/catalogo/',package_revision.name), tracking_summary.running_total, TO_CHAR(package_revision.revision_timestamp, 'DD.MM.YYYY')
FROM 
  public.package_revision, 
  public.group_revision, public.tracking_summary, public.member_revision
WHERE 
  group_revision.id = member_revision.group_id AND member_revision.state='active' AND group_revision.state='active' AND group_revision.current=TRUE AND is_organization=FALSE AND member_revision.table_id = package_revision.id AND member_revision.table_name='package' AND member_revision.state='active' AND
  package_revision.current=TRUE AND package_revision.state='active' AND package_revision.type='dataset' AND package_revision.id = "tracking_summary".package_id AND tracking_date =( SELECT MAX(tracking_date) FROM tracking_summary WHERE package_id = package_revision.id) AND group_revision.name = 'ciencia-tecnologia' 
 ORDER BY package_revision.revision_timestamp DESC;
