
from flask import Flask, Blueprint, url_for, jsonify, make_response, request, render_template, redirect, abort
from controller.supermercado.SupermercadoControl import SuperMercadoControl
from controller.supermercado.SupermercadoGrafo import SuperMercadoGrafo
import os 
import json

from controller.tda.linked.calcular_dis_geo import calcular_distancia

router = Blueprint('router', __name__)

@router.route('/')
def home():
    return render_template('template.html')

@router.route('/supermercado')
def lista_negocios():
    smc = SuperMercadoControl()
    lista = smc._list()
    lista.sort_models("_id")
    return render_template('supermercado/lista.html', lista=smc.to_dic_lista(lista))

@router.route("/supermercado/agregar")
def agregar_negocio():
    return render_template('supermercado/guardar.html')

@router.route('/grafo')
def grafo():
    return render_template('d3/grafo.html')

@router.route("/supermercado/guardar_distancia/<int:origen>/<int:destino>", methods=['POST'])
def agregar_distancia(origen, destino):
    try:
        pd = SuperMercadoControl()
        lista = pd._list().sort_models("_id")
        
        inicio = lista.busqueda_binaria("_id", origen)
        final = lista.busqueda_binaria("_id", destino)
        
        lon1 = inicio._lng
        lat1 = inicio._lat
        
        lon2 = final._lng
        lat2 = final._lat

        lon1_float = float(lon1)
        lat1_float = float(lat1)
        lon2_float = float(lon2)
        lat2_float = float(lat2)
        
        distancia = calcular_distancia(lon1_float, lat1_float, lon2_float, lat2_float)
        
        distancia_redondeada = round(distancia, 2)
        
        return jsonify({"distancia": distancia_redondeada, "message": "Distancia guardada exitosamente."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@router.route('/supermercado/guardar', methods = ['POST'])  
def guardar_supermercado():
    print("\n\n\n\n\n")
    smc = SuperMercadoControl()
    data = request.form
    print(data)
    if not "nombre" in data.keys() or not "latitud" in data.keys() or not "longitud" in data.keys():
       abort(400)
    #TODO ...Validar 
    smc._supermercado._nombre = data['nombre']
    smc._supermercado._direccion = data['direccion']
    smc._supermercado._horario = data['horario']
    smc._supermercado._lat = request.form['latitud']
    smc._supermercado._lng = request.form['longitud']
    smc.save
    return redirect("/supermercado", code=302)

@router.route('/supermercado/grafo_ver')
def grafo_ver():
    smc = SuperMercadoControl()
    lista = smc._list()
    if not lista.isEmpty:
        lista.sort_models("_id")
    return render_template('supermercado/grafo.html', lista=smc.to_dic_lista(lista))

@router.route('/supermercado/caminos')
def grafo_caminos():
    pd = SuperMercadoControl()
    lista = pd._list()
    ng = SuperMercadoGrafo()
    ng.create_graph()
    if not lista.isEmpty:
        lista.sort_models("_id")
    return render_template('d3/grafo.html', lista=pd.to_dic_lista(lista))

@router.route('/supermercado/guardar_json', methods=['POST'])
def guardar_grafo_json():
    data = request.get_json()
    ruta_json = os.path.dirname(os.path.dirname(__file__))+"/data/grafo.json"
    with open(ruta_json, 'w') as f:
        json.dump(data, f)
    return jsonify({"message": "Guardado en JSON exitosamente."})

@router.route('/supermercado/cargar_json', methods=['GET'])
def cargar_grafo_json():
    ruta_json = os.path.dirname(os.path.dirname(__file__))+"/data/grafo.json"
    with open(ruta_json) as f:
        data = json.load(f)
    return jsonify(data)

@router.route('/supermercado/camino/<origen>/<destino>/<algoritmo>')
def ver_camino(origen, destino, algoritmo):
    smg = SuperMercadoGrafo()
    origen = int(origen) - 1
    destino = int(destino) - 1  
    smc = SuperMercadoControl()
    lista = smc._lista.toArray
    if algoritmo == 'djistra':
        camino_corto, tiempo = smg.camino_dijkstra(origen, destino)
        camino = " -> ".join(str(lista[i]) for i in camino_corto)
        data = {
            "camino_djistkra": camino,
            "tiempo_djistra": tiempo
        }
    elif algoritmo == 'floyd':
        camino_corto, tiempo = smg.camino_floyd(origen, destino)
        camino = " --> ".join(str(lista[i]) for i in camino_corto)
        data = {
            "camino_floyd": camino,
            "tiempo_floyd": tiempo
        }
    else:
        return jsonify({"error"}), 400

    return jsonify(data)










