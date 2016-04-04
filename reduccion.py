import couchdb
#abre la base de datos ecuado
couch = couchdb.Server()
couch = couchdb.Server('http://localhost:5984/')
db = couch['ecuador']
#crea una base de datos nuea donde se guardarám los campos reducidos
try:
    db1 = couch.create('ecuador_reducido')
except:
    print "Base da datos ya existe"
db1 = couch['ecuador_reducido']

print "empieza a guardar"
#lee los regitros de la base original 
for id in db:
    try: 
        doc = db[id]
        doc2=doc['place']
        doc3=doc['user']
        if(doc2['country']=='Ecuador'):
            try:
                # se guardan solo los campos necesarios para el analisis
                ciudad = doc2['full_name'].split(',')
                doc1 = {'_id': doc['_id'],'texto': doc['text'],'ciudad': ciudad[0],'usuario': doc3['screen_name'],'fecha':doc['created_at']}
                db1.save(doc1)
            except:
                print "Error en ciudad, documento ommitido"
    except:
        print "error en leer datos, documento omitido"
print "Listo!!"


    
