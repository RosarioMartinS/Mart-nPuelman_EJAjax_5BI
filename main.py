from flask import Flask, render_template, jsonify, request
import sqlite3
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/preguntas',methods=['GET', "POST"])
def obtener():
  if request.method=="GET":
    conn = sqlite3.connect('dataBase.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(f"""SELECT pregunta
            FROM Preguntas""")
    rows = cur.fetchall()
    
    lista=[]
    for fila in rows:
        pregfila = {}
        pregfila['pregunta']=fila[0]
        lista.append(pregfila)
    return jsonify(lista)

#------------------------------------------
@app.route('/agregar')
def pantallaAgregar():
  return render_template("post.html")
  
@app.route('/ingresarPreg',methods=['GET', "POST"])
def agregar():
  if request.method=="POST":
    preg=request.form["pregunta"]
    print(preg)
    conn = sqlite3.connect('dataBase.db')
    conn.execute(f"""INSERT INTO Preguntas(pregunta, categoria,nivel)
      VALUES('{preg}','categoria','3');""")
    cur=conn.cursor()
    cur.execute(f"""SELECT id_pregunta
    FROM Preguntas
    WHERE pregunta = '{preg}';""")
    id = cur.fetchone()
    i = 0
    for i in range(3):
      if i == 0:
        conn.execute(f"""INSERT INTO Respuestas(es_correcta,respuesta,id_pregunta)
      VALUES(0,'Respuesta{i+1}',{id[0]});""")
      else:
        conn.execute(f"""INSERT INTO Respuestas(es_correcta,respuesta,id_pregunta)
      VALUES(1,'Respuesta{i+1}',{id[0]});""")
    conn.commit()
    conn.close()
    estado = "True"
    return jsonify(estado)
  else:
    estado = "False"
    return jsonify(estado) 
#------------------------------------------------------
def listaPreguntas():
  conn = sqlite3.connect('dataBase.db')
  conn.row_factory = sqlite3.Row
  cur = conn.cursor()
  cur.execute(f"""SELECT pregunta
            FROM Preguntas""")
  rows = cur.fetchall()
  lista=[]
  for fila in rows:
      pregfila = {}
      pregfila['pregunta']=fila[0]
      lista.append(pregfila)
  return lista

@app.route('/modficar') 
def pantallaModificar():
  preguntas=listaPreguntas();
  return render_template("put.html", preguntas=preguntas)
  
@app.route('/modificarPreg',methods=['PUT'])
def modificar():
  if request.method=="PUT":
    modif=request.form["respuesta"]
    preg=request.form["pregunta"]
    print(modif)
    conn = sqlite3.connect('dataBase.db')
    cur=conn.cursor()
    cur.execute(f"""SELECT id_pregunta
    FROM Preguntas
    WHERE pregunta = '{preg}';""")
    resp = cur.fetchone()
    print(resp[0])
    if modif!=" ":
      cur.execute(f"""UPDATE Respuestas
      SET respuesta='{modif}'
      WHERE id_pregunta={resp[0]} AND es_correcta=0;""")
    conn.commit()
    conn.close()
    estado = "True"
    return jsonify([estado, modif])
  else:
    estado = "False"
    return jsonify(estado) 
#--------------------------------------
@app.route('/borrar') 
def pantallaBorrar():
  preguntas=listaPreguntas()
  return render_template("delete.html", preguntas=preguntas)

@app.route('/eliminarPreg', methods=['DELETE']) 
def eliminar():
  if request.method=="DELETE":
    elim=request.form["pregunta"]
    conn = sqlite3.connect('dataBase.db')
    cur = conn.cursor()
    cur.execute(f"""DELETE FROM Preguntas
      WHERE pregunta='{elim}';""")
    conn.commit()
    conn.close()
    estado = "True"
    return jsonify(estado)
  else:
    estado = "False"
    return jsonify(estado) 

    
app.run(host='0.0.0.0', port=81)

