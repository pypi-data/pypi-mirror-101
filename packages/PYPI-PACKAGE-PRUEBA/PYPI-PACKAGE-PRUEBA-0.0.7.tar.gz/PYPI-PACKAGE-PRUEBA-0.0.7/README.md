# pypi-package-Prueba
 Prueba pypi

Este es un readme de ejemplo

Orden de pasos para crear y subir un paquete propio a PyPi:

1-Creo el paquete con todos los direcctorios y ficheros.
2-Creo el archivo __init__.py dentro del directorio general del paquete, o en los subdirectorios tambien puede ser
3-Genero, por fuera del directorio del paquete el fichero setup.py con sus parametros (aca pongo mis datos, vinculo al github, etc...)
4-Genero fichero setup.cfg donde vinculare el archivo README.MD (este archivo en este caso)
5-Genero el fichero LICENSE
6-Hago el commit y el push del repo en Git
7-Ubicado en la carpeta general donde arme el paquete, ejecuto "python setup.py sdist", se genera el archivo .tar con los ficheros dentro del directorio dist
8-Si no esta, instalar twine "pip install twine"
9-Luego usando twine subimos el paquete a PyPi con el comando "twine upload dist/* ", va a pedir usuario y clave de la cuenta de PyPi