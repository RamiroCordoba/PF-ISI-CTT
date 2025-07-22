![Lenguaje principal](https://img.shields.io/github/languages/top/RamiroCordoba/PF-ISI-CTT)
![Tamaño del repo](https://img.shields.io/github/repo-size/RamiroCordoba/PF-ISI-CTT)
![Licencia](https://img.shields.io/github/license/RamiroCordoba/PF-ISI-CTT)
![Estrellas](https://img.shields.io/github/stars/RamiroCordoba/PF-ISI-CTT?style=social)


# Proyecto final de carrera
En este repositorio se encuentra el código principal de nuestro proyecto final de la carrera de Ingeniería en Sistemas de Información de la UTN-Frro.
## Autores
- Córdoba, Ramiro Emiliano (L:46824)
- Tomas, Alexis José (L:47241)
- Tombolini, Santiago Alfredo (L:47431)
## Documentación del proyecto
[Documentación proyecto final](https://docs.google.com/document/d/1PzV5yPfaBflleSD59RS7iYweBbXODihujllTpp99GxU/edit?usp=sharing)

## Tabla de Contenidos
- [Descripción del proyecto](#Descripción)
- [Programas y bibliotecas necesarios](#Programas-y-bibliotecas-necesarios)
- [Credenciales](#credenciales)
- [Manual de usuario](#Manual-de-usuario)
- [Licencia](#Licencia)

## Descripción
El presente proyecto propone el desarrollo de un sistema de gestión de stock y recursos que integra modelos predictivos basados en inteligencia artificial. El objetivo principal es mejorar la eficiencia de la gestión de inventarios y reducir los costos asociados al almacenamiento y la pérdida de capital causada por el mismo, brindando sugerencias en base a lo pronosticado. Para lograrlo, se desarrollará un software ERP desde sus bases con las funciones de interés, tales como la gestión de stock, registro de materia prima, ventas, cartera de proveedores y un tablón de métricas con los productos más vendidos en determinado mes, entre otros.

Los modelos de predicción se enfocarán en pronosticar la cantidad de ventas y el stock óptimo a mantener, junto con su punto de pedido y la cantidad a pedir, permitiendo minimizar los costos de almacenamiento y satisfacer la demanda de manera eficiente. Se espera que este sistema permita a la empresa mejorar su gestión de inventarios, aumentar su rentabilidad y competitividad en el mercado, y servir como base para futuros proyectos de software empresarial

## Programas y bibliotecas necesarios
Dentro de repositorio se encuentra el script llamado "requirements.txt" en el cual se especifican las librerías que deben estar instaladas con su versión correspondiente. Así mismo se nombran a continuación los programas, lenguajes y bibliotecas utilizados en dicho desarrollo:
### Lenguaje de programacion
Backend :
- Python 3.12.9
- Django 5.0.4

Frontend :
- CSS
- HTML 5
- Bootstrap
- JS
### Bibliotecas
- django 5.0.4
- mssql-django 1.4

### Programas
- Visual Code
- Microsoft SQL Server
- Tailscale (VPN para el servidor)
- Drawio

## Credenciales
Actualmente hay 3 tipos de usuarios con diferentes permisos asignados:
- SuperAdmin: Tiene todos los permisos.
- Administrador: Tiene todos los permisos para las CRUDs pero no puede crear usuarios nuevos.
- Vendedor: Tiene el permiso de lectura.

### Credenciales para probar:
- SuperAdmin:
  - User: admin
  - Pass: admin
- Administrador:
  - User: administrador1
  - Pass: 123456789Admin
- Vendedor:
  - User: vendedor1
  - Pass: 123456789Vende

### Para acceder al "Administrador de Django"
Ingrese aca: [Administración de Django](http://127.0.0.1:8000/admin/)

## Manual de Usuario
Proximamente...

## Licencia

Este proyecto está licenciado bajo los términos de la [Licencia Pública General GNU v3](https://github.com/RamiroCordoba/PF-ISI-CTT/blob/main/LICENSE).
