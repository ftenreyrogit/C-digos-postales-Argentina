import requests
import json
import codecs

def get_localidades(provincia):
    r = requests.post(
        'https://www.correoargentino.com.ar/sites/all/modules/custom/ca_forms/api/wsFacade.php',
         data = {'action':"localidades",'provincia':provincia}
         )
    decode_data = codecs.decode(r.text.encode(), 'utf-8-sig')
    json_data = json.loads(decode_data)
    if json_data == None : return get_localidades(provincia)
    return json_data

provincias = (
    ("C","Ciudad Autonoma de Buenos Aires"),
    ("B","Buenos Aires"),
    ("K","Catamarca"),
    ("H","Chaco"),
    ("U","Chubut"),
    ("X","Cordoba"),
    ("W","Corrientes"),
    ("E","Entre Rios"),
    ("P","Formosa"),
    ("Y","Jujuy"),
    ("L","La Pampa"),
    ("F","La Rioja"),
    ("M","Mendoza"),
    ("N","Misiones"),
    ("Q","Neuquen"),
    ("R","Rio Negro"),
    ("A","Salta"),
    ("J","San Juan"),
    ("D","San Luis"),
    ("Z","Santa Cruz"),
    ("S","Santa Fe"),
    ("G","Santiago del Estero"),
    ("V","Tierra del Fuego"),
    ("T","Tucuman"),
)

file = open("postal_code_ar.sql","w",encoding="utf-8")
file.write("CREATE database postal_code_ar;")
file.write("USE postal_code_ar;")
file.write("CREATE TABLE provincia(id_p int(6) UNSIGNED PRIMARY KEY,p_name VARCHAR(100) NOT NULL);")
file.write("CREATE TABLE localidad(id_l int(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,id_p int(6) UNSIGNED NOT NULL,l_name VARCHAR(100) NOT NULL,postal_code VARCHAR(6),CONSTRAINT fk_localidad_provincia FOREIGN KEY (id_p) REFERENCES provincia (id_p) ON DELETE RESTRICT ON UPDATE CASCADE);")


for provincia in provincias:
    index = str(provincias.index(provincia) + 1)
    file.write("INSERT INTO PROVINCIA VALUES("+index+",'"+provincia[1]+"');\n")
    json_data = get_localidades(provincia[0])
    for my_dict in json_data:
        file.write("INSERT INTO LOCALIDAD VALUES(NULL,"+index+",'"+my_dict["nombre"]+"','"+my_dict["cp"]+"');\n")
    print("Progreso: " + index + " / " + str( len(provincias) ) )
    