import firebase_admin
from firebase_admin import credentials, db, storage
import requests
from datetime import datetime
import os
import json
from tkinter import *
from tkinter import ttk

# Configura las credenciales de Firebase
cred = credentials.Certificate('minihuellas-8dac0-firebase-adminsdk-f89sl-a2e011117e.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://minihuellas-8dac0-default-rtdb.firebaseio.com/',
    'storageBucket': 'minihuellas-8dac0.appspot.com'
})

class Ventana():
   def __init__(self):
       Main= Tk()
       Main.title('BackUp')
       Main.geometry('742x254')
       Main.config(bg='#358ebb')
       Main.resizable(0,0)
       self.text = Label( Main, text= 'Descargar Copia de Seguridad',bg= '#358ebb',fg= '#ffffff',font=('Times New Roman',30,'bold'),justify=LEFT)
       self.text.place(x =100, y = 30)
       button = Button( Main, width= '41',text='Subir BackUp',bg= '#b1a739',fg= '#ffffff',font=('Times New Roman',20,'normal'), command=self.Subir).place(x =60, y = 140)
       Main.mainloop()




   def Subir(self):




       ref = db.reference('/')

       # Obtén los datos de la base de datos
       datos = ref.get()


       self.extraer_urls(datos)


       fecha_actual = datetime.now().strftime('%Y-%m-%d')

       # Especifica la ruta para guardar la copia local
       ruta_copia_local = f'./Copia de Seguridad/RealTime/{fecha_actual}.json'

       # Guarda los datos en el archivo local
       with open(ruta_copia_local, 'w') as archivo:
           json.dump(datos, archivo)

       print(f'Copia de datos realizada en el archivo local: {ruta_copia_local}')
       print('Todas las imágenes y Realtime han sido exportadas de Firebase')



   def extraer_urls(self,datos, ruta_actual=''):

       for key, value in datos.items():
           nueva_ruta = f'{ruta_actual}/{key}' if ruta_actual else key

           if isinstance(value, dict):
               # Si el valor es un diccionario, es un nodo interno, así que llamamos a la función de manera recursiva
               self.extraer_urls(value, nueva_ruta)
           elif key == 'Foto':
               # Si la clave es 'Foto', mostramos la URL y la ruta sin 'Usuarios' y 'Mascotas' y termina con '.jpg'
               ruta_sin_usuarios_mascotas = nueva_ruta.replace('Usuarios/', '').replace('Mascotas/', '').replace('/',
                                                                                                                 '_')

               if 'Vacunas' in ruta_sin_usuarios_mascotas:
                   ruta_sin_usuarios_mascotas = nueva_ruta.replace('Usuarios/', '').replace('Mascotas/', '').replace(
                       '/', '_').replace('_Foto', '')

               # Obtener la fecha actual en formato YYYY-MM-DD
               fecha_actual = datetime.now().strftime('%Y-%m-%d')

               # Crear la carpeta con la fecha actual si no existe
               ruta_carpeta = f'./Copia de Seguridad/Imagenes/{fecha_actual}/'
               os.makedirs(ruta_carpeta, exist_ok=True)

               # Construir la ruta final del archivo
               ruta_final = f'{ruta_carpeta}{ruta_sin_usuarios_mascotas}.jpg'

               # URL de descarga de la imagen desde Firebase Storage
               imagen_url = value

               # Descargar la imagen desde Firebase Storage
               response = requests.get(imagen_url)

               # Guardar la imagen localmente
               with open(ruta_final, 'wb') as file:
                   file.write(response.content)

               print(f'Imagen descargada y guardada en {ruta_final}')


Ventana()



