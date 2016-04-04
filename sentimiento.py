import couchdb
import re
# se lee la base de datos analizar
couch = couchdb.Server()
couch = couchdb.Server('http://localhost:5984/')
db = couch['ecuador_reducido']
lista=[] # lista necesaria para guardar los campos de cada documento de la base de datos
listaCandidatos=[] #lista necesaria para leer los candidatos del documento de texto candidatos
contador= 0
#se crear un objeto para los tweets
class Tuit:
    def __init__(self, iden, texto, ciudad,usuario,fecha):
        self.iden = iden
        self.texto = texto
        self.ciudad = ciudad
        self.usuario = usuario
        self.fecha = fecha
#se crea un onjeto para los candidatos
class Candidato:
    def __init__(self, nombre, clave,usuario, hashtag):
        self.nombre = nombre
        self.usuario = usuario
        self.clave = clave
        self.hashtag = hashtag
#se leen los ducumentos de la base de datos
for id in db:
    try: 
        doc = db[id]
        ciudad = doc['ciudad'].split(',')
        #se guardan los documentos en una lista para posteriormente ser procesada
        t = Tuit(doc['_id'],doc['texto'], ciudad[0], doc['usuario'],doc['fecha'])
        lista.append(t)
    except:
        print "error en leer datos, documento omitido"
print "Base de datos cargada"
# se abre el archivo candidatos.txt
archi0=open('candidatos.txt') 
lineas0=archi0.read()
nombre= lineas0.split('\n')
archi0.close()
#se dividen los campos de cada linea del documento de texto
for n in nombre:
    temporal=n.split(',')
    #se guardan los campos en una lista
    c = Candidato(temporal[0], temporal[1], temporal[2],temporal[3])
    listaCandidatos.append(c)

#se lee el archivo de palabras positivas
archi=open('positivas.txt') 
lineas=archi.read()
palabras_positivas= lineas.split('\n')
archi.close()
#se lee el archivo de palabras negatias
archi1=open('negativas.txt') 
lineas1=archi1.read()
palabras_negativas= lineas1.split('\n')
archi1.close()
# se crea una base de datos para almacenar los tweets con sentimiento
try:
    db1 = couch.create('ecuador_sentimiento4')
except:
    print "Base da datos ya existe"
db1 = couch['ecuador_sentimiento4']
for a in lista:
    try:
         minuscula=a.texto.lower()
         for n in listaCandidatos:
            #se compara el texto con los candidatos 
             if (n.clave.lower() in minuscula) or (n.usuario.lower() in minuscula):
                 sentimiento = 'neutral';
                 #si se encuentra una coincidencia se procede a comparar con las palabras positivas
                 for pn in palabras_negativas:  
                     if(pn.decode('utf-8') in minuscula):
                         sentimiento='negativo'
                 #si se encuentra una coincidencia se procede a comparar con las palabras negativas       
                 for pn in palabras_positivas:  
                     if(pn.decode('utf-8') in minuscula):
                         sentimiento='positivo'
                         
                 #finalmente se guarda el documento
                 doc1 = {'_id': a.iden,'candidato': n.nombre,'texto':a.texto,'ciudad': a.ciudad,'usuario': a.usuario,'fecha':a.fecha,'sentimiento': sentimiento}
                 db1.save(doc1)
    except:
        
        print "error en ver sentimiento"


print "Listo!!"    



