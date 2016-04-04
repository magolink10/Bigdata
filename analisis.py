import couchdb
import re
listaCandidatos=[]#lista necesaria para leer los candidatos del documento de texto candidatos
# se lee la base de datos analizar
couch = couchdb.Server()
couch = couchdb.Server('http://localhost:5984/')
db = couch['ecuador_sentimiento']
lista=[] # lista necesaria para guardar los campos de cada documento de la base de datos
listaCiudades=[]
contador= 0
#se crear un objeto para los tweets
class Tuit:
    def __init__(self, iden, texto, ciudad,usuario,fecha,candidato,sentimiento):
        self.iden = iden
        self.texto = texto
        self.ciudad = ciudad
        self.usuario = usuario
        self.fecha = fecha
        self.candidato=candidato
        self.sentimiento=sentimiento
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
        #se guardan los documentos en una lista para posteriormente ser procesada
        t = Tuit(doc['_id'],doc['texto'], doc['ciudad'], doc['usuario'],doc['fecha'],doc['candidato'],doc['sentimiento'])
        lista.append(t)
        # se toma atencion el campo ciudades y se los guarda en una ista aparte
        listaCiudades.append(doc['ciudad'])
    except:
        print "error en leer datos, documento omitido"
print "Base de datos cargada"
# se abre el archivo candidatos.txt
archi0=open('candidatos.txt') 
lineas0=archi0.read()
nombre= lineas0.split('\n')
archi0.close()
#se diiden los campos de cada linea del documento de texto
for n in nombre:
    temporal=n.split(',')
    c = Candidato(temporal[0], temporal[1], temporal[2],temporal[3])
    listaCandidatos.append(c)
    
# se crea una base de datos para almacenar los resultados
try:
    db1 = couch.create('ecuador_resultados')
except:
    print "Base da datos ya existe"
db1 = couch['ecuador_resultados']


for n in listaCandidatos:
        #se declaran ariables para los contadores de positios, negativos y nueutros de cada ciudad
        contadorQPos=0
        contadorQNeg=0
        contadorQNeu=0
        contadorGPos=0
        contadorGNeg=0
        contadorGNeu=0
        contadorCPos=0
        contadorCNeg=0
        contadorCNeu=0
        contadorEPos=0
        contadorENeg=0
        contadorENeu=0
        for c in lista:
            #se compara la ciudad Quito
            if (c.ciudad=='Quito'):
                if (c.candidato==n.clave):
                    #se verifica el tipo se de sentimiento
                    if (c.sentimiento=='negativo'):
                        contadorQNeg=contadorQNeg+1
                    if (c.sentimiento=='positivo'):
                        contadorQPos=contadorQPos+1
                    if (c.sentimiento=='neutral'):
                        contadorQNeu=contadorQNeu+1
            #se compara la ciudad Guayaquil
            elif (c.ciudad=='Guayaquil'):
                if (c.candidato==n.clave):
                    #se verifica el tipo se de sentimiento
                    if (c.sentimiento=='negativo'):
                        contadorGNeg=contadorGNeg+1
                    if (c.sentimiento=='positivo'):
                        contadorGPos=contadorGPos+1
                    if (c.sentimiento=='neutral'):
                        contadorGNeu=contadorGNeu+1
            #se compara la ciudad Cuenca
            elif (c.ciudad=='Cuenca'):
                if (c.candidato==n.clave):
                    #se verifica el tipo se de sentimiento
                    if (c.sentimiento=='negativo'):
                        contadorCNeg=contadorCNeg+1
                    if (c.sentimiento=='positivo'):
                        contadorCPos=contadorCPos+1
                    if (c.sentimiento=='neutral'):
                        contadorCNeu=contadorCNeu+1
            else:
            #se compara la ciudad Ecuador
                if (c.candidato==n.clave):
                    #se verifica el tipo se de sentimiento
                    if (c.sentimiento=='negativo'):
                        contadorENeg=contadorENeg+1
                    if (c.sentimiento=='positivo'):
                        contadorEPos=contadorEPos+1
                    if (c.sentimiento=='neutral'):
                        contadorENeu=contadorENeu+1
        # se guardan los resultados en la base de datos
        doc1 = {'nombre':  n.nombre,'Quito': {'Positivos':contadorQPos,'Negativos':contadorQNeg,'Neutros':contadorQNeu},'Guayaquil': {'Positivos':contadorGPos,'Negativos':contadorGNeg,'Neutros':contadorGNeu},'Cuenca': {'Positivos':contadorCPos,'Negativos':contadorCNeg,'Neutros':contadorCNeu},'Ecuador': {'Positivos':contadorEPos,'Negativos':contadorENeg,'Neutros':contadorENeu}}
        db1.save(doc1)
        print '/////////////////////////////////////////////////////'
        print n.nombre
        print '/////////////////////////////////////////////////////'
        print 'Quito'
        print 'positivo:'+str(contadorQPos)+' negativo:' +str(contadorQNeg)+ ' Neutral:'+str(contadorQNeu)
        print 'Guayaquil'
        print 'positivo:'+str(contadorGPos)+' negativo:' +str(contadorGNeg)+ ' Neutral:'+str(contadorGNeu)
        print 'Cuenca'
        print 'positivo:'+str(contadorCPos)+' negativo:' +str(contadorCNeg)+ ' Neutral:'+str(contadorCNeu)
        print 'Resto del Ecuador'
        print 'positivo:'+str(contadorEPos)+' negativo:' +str(contadorENeg)+ ' Neutral:'+str(contadorENeu)
        print 'TOTAL'
        print 'positivo:'+str(contadorEPos+contadorCPos+contadorGPos+contadorQPos)+' negativo:' +str(contadorENeg+contadorCNeg+contadorGNeg+contadorQNeg)+ ' Neutral:'+str(contadorENeu+contadorCNeu+contadorGNeu+contadorQNeu)
print "Listo!!"

