# Creación aplicaciones en odoo
carpeta(en Windows):
C:\Program Files (x86)\Odoo 9.0-20161104\server\openerp\addons
crear  carpeta(nombre aplicacion)
crear fichero __init__.py
Luego necesitamos crear el archivo descriptor. Debe contener únicamente un diccionario Python y puede contener alrededor de una docena de atributos, de los cuales solo el atributo name es obligatorio. Son recomendados los atributos description, para una descripción más larga, y author. Ahora agregamos un archivo __openerp__.py:
~~~
{
    'name': 'Aplicacion Application',
    'description': 'Manage your personal Tasks with this module.',
    'author': 'Daniel Reis',
    'depends': ['mail'],
    'application': True,
}
~~~
El atributo depends puede tener una lista de otros módulos requeridos. Odoo los instalará automáticamente cuando este módulo sea instalado.

Los modelos describen los objetos de negocio, como una oportunidad, una orden de venta, o un socio (cliente, proveedor, etc). Un modelo tiene una lista de atributos y también puede definir su negocio específico.

Los modelos son implementados usando clases Python derivadas de una plantilla de clase de Odoo. Estos son traducidos directamente a objetos de base de datos, y Odoo se encarga de esto automáticamente cuando el módulo es instalado o actualizado.
Creamos el fichero app01_model.py:
~~~
#-*- coding: utf-8 -*-
from openerp import models, fields

class App01Task(models.Model):
    _name = 'app01.task'
    name = fields.Char('Description', required=True)
    is_done = fields.Boolean('Done?')
    active = fields.Boolean('Active?', default=True)
~~~
La primera línea es un marcador especial que le dice al interprete de Python que ese archivo es UTF-8, por lo que puede manejar y esperarse caracteres non-ASCII. No usaremos ninguno, pero es mas seguro usarlo.

La segunda línea hace que estén disponibles los modelos y los objetos campos del núcleo de Odoo.

la tercera línea declara nuestro nuevo modelo.    

Todavía, este archivo, no es usado por el módulo. Debemos decirle a Odoo que lo cargue con el módulo en el archivo __init__.py. Editemos el archivo para agregar la siguiente línea:

from . import app01_model


Ahora podemos revisar el modelo recién creado en el menú Técnico. Vaya a Estructura de la Base de Datos | Modelos y busque el modelo todo.task en la lista. Luego haga clic en este para ver su definición:

Si no hubo ningún problema, esto nos confirmará que el modelo y nuestros campos fueron creados. Si hizo algunos cambios y no son reflejados, intente reiniciar el servidor, como fue descrito anteriormente, para obligar que todo el código Python sea cargado nuevamente.

También podemos ver algunos campos adicionales que no declaramos. Estos son cinco campos reservados que Odoo agrega automáticamente a cualquier modelo. Son los siguientes: - id: Este es el identificador único para cada registro en un modelo en particular. - create_date y create_uid: Estos nos indican cuando el registro fue creado y quien lo creó, respectivamente. - write_date y write_uid: Estos nos indican cuando fue la última vez que el registro fue modificado y quien lo modificó, respectivamente.

al cual almacenar nuestros datos, hagamos que este disponible en la interfaz con el usuario y la usuaria.

Todo lo que necesitamos hacer es agregar una opción de menú para abrir el modelo de "Aplicacion Task" para que pueda ser usado. Esto es realizado usando un archivo XML. Igual que en el caso de los modelos, algunas personas consideran como una buena practica mantener las definiciones de vistas en en un subdirectorio separado.

Crearemos un archivo nuevo aplicacion_view.xml en el directorio raíz del módulo, y este tendrá la declaración de un ítem de menú y la acción ejecutada por este:
~~~
<?xml version="1.0" encoding="UTF-8"?>
    <openerp>
        <data>
            <!-- Action to open To-do Task list -->
            <act_window
                id="action_aplicacion_task"
                name="Aplicacion Task"
                res_model="aplicacion.task"
                view_mode="tree,form"
            />
            <!-- Menu item to open aplicacion Task list -->
            <menuitem
                id="menu_aplicacion_task"
                name="aplicacion Tasks"
                parent="mail.mail_feeds"
                sequence="20"
                action="action_aplicacion_task"
            />
        </data>
    </openerp>
~~~
La interfaz con el usuario y usuaria, incluidas las opciones del menú y las acciones, son almacenadas en tablas de la base de datos. El archivo XML es un archivo de datos usado para cargar esas definiciones dentro de la base de datos cuando el módulo es instalado o actualizado. Esto es un archivo de datos de Odoo, que describe dos registros para ser agregados a Odoo: - El elemento <act_window> define una Acción de Ventana del lado del cliente para abrir el modelo aplicacion.task definido en el archivo Python, con las vistas de árbol y formulario habilitadas, en ese orden. - El elemento <menuitem> define un ítem de menú bajo el menú Mensajería (identificado por mail.mail_feeds), llamando a la acción action_aplicacion_task, que fue definida anteriormente. el atributo sequence nos deja fijar el orden de las opciones del menú.

Ahora necesitamos decirle al módulo que use el nuevo archivo de datos XML. Esto es hecho en el archivo __openerp__.py usando el atributo data. Este define la lista de archivos que son cargados por el módulo. Agregue este atributo al diccionario del descriptor:

'data' : ['aplicacion_view.xml'],

Se generará un formulario, aunque Odoo  lo hace automáticamente, si no queremos, entonces podemos trabajar con nuestro modelo, sin tener ningún formulario o vistas definidas aún.

Odoo soporta varios tipos de vistas, pero las tres principales son: list (lista, también llamada árbol), form (formulario), y search (búsqueda).

Todas las vistas son almacenadas en la base de datos, en el modelo ir.model.view. Para agregar una vista en un módulo, declaramos un elemento <record> describiendo la vista en un archivo XML que será cargado dentro de la base de datos cuando el modelo sea instalado.


Añadir al fichero aplicacion_view.xml:
~~~

<record    id="view_form_aplicacion_task" model="ir.ui.view">
    <field name="name">Aplicacion Task Form</field>
    <field name="model">aplicacion.task</field>
    <field name="arch" type="xml">
        <form string="Aplicacion Task">
            <field name="name"/>
            <field name="is_done"/>
            <field name="active" readonly="1"/>
        </form>
    </field>
</record>
~~~
Esto agregará un registro al modelo ir.ui.view con el identificador view_form_aplicacion_task. Para el modelo la vista es todo.task y nombrada Aplicacion Task Form. El nombre es solo para información, no tiene que ser único, pero debe permitir identificar fácilmente a que registro se refiere.

El atributo más importante es arch, que contiene la definición de la vista. Aquí decimos que es un formulario, y que contiene tres campos, y que decidimos hacer al campo active de solo lectura.

Lo anterior proporciona una vista de formulario básica, pero podemos hacer algunos cambios para mejorar su apariencia. Para los modelos de documentos Odoo tiene un estilo de presentación que asemeja una hoja de papel. El formulario contiene dos elementos: una <head>, que contiene botones de acción, y un <sheet>, que contiene los campos de datos

los formularios pueden tener botones que ejecuten acciones. Estos son capaces de desencadenar acciones de flujo de trabajo, ejecutar Acciones de Ventana, como abrir otro formulario, o ejecutar funciones Python definidas en el modelo.

Estos pueden ser colocados en cualquier parte dentro de un formulario, pero para formularios con estilo de documentos, el sitio recomendado es en la sección <header>.

Los atributos básicos para un botón son: string con el texto que se muestra en el botón, type que hace referencia al tipo de acción que ejecuta, y name que es el identificador para esa acción. El atributo class puede aplicar estilos CSS, como un HTML común.

La etiqueta <group> permite organizar el contenido del formulario. Colocando los elementos <group> dentro de un elemento <group> crea una disposición de dos columnas dentro del grupo externo. Se recomienda que los elementos Group tengan un nombre para hacer más fácil su extensión en otros módulos.

Usaremos esto para mejorar la organización de nuestro contenido.
~~~
<record id="view_form_aplicacion_ejemplo01_task" model="ir.ui.view">
                <field name="name">Aplicaión ejemplo01  Form</field>
                <field name="model">aplicacionejemplo01.task</field>
                <field name="arch" type="xml">
                <form>
                    <header>
                        <button name="do_toggle_done" type="object" string="Toggle Done" class="oe_highlight" />
                        <button name="do_clear_done" type="object" string="Clear All Done" />
                    </header>
                    <sheet>
                        <group name="group_top">
                            <group name="group_left">
                                <field name="name"/>
                            </group>
                            <group name="group_right">
                                <field name="is_done"/>
                                <field name="active" readonly="1" />
                            </group>
                        </group>
                    </sheet>
                </form>
                </field>
            </record>
~~~
Ahora agregaremos lógica a nuestros botones. Edite el archivo Python aplicacion_model.py para agregar a la clase los métodos llamados por los botones.


La acción del botón Toggle  solo cambia de estado (marca o desmarca) la señal Is Done?. La forma más simple para agregar la lógica a un registro, es usar el decorador @api.one. Aquí self representara un registro. Si la acción es llamada para un conjunto de registros, la API gestionara esto lanzando el método para cada uno de los registros
~~~
@api.one
    def do_toggle_done(self):
        self.is_done = not self.is_done
        return True
~~~

Simplemente modifica el campo is_done, invirtiendo su valor. Luego los métodos pueden ser llamados desde el lado del client y siempre deben devolver algo. Si no devuelven nada, las llamadas del cliente usando el protocolo XMLRPC no funcionará. Si no tenemos nada que devolver, la práctica común es simplemente devolver True.


Para el botón Clear All Done queremos ir un poco más lejos. Este debe buscar todos los registros activos que estén finalizados, y desactivarlos. Se supone que los botones de formulario solo actúan sobre los registros seleccionados, pero para mantener las cosas simples haremos un poco de trampa, y también actuará sobre los demás botones:
~~~
@api.multi def do_clear_done(self):
    done_recs = self.search([('is_done', '=', True)])
    done_recs.write({'active': False})
    return True
~~~

En los métodos decorados con @api.multi el self representa un conjunto de registros. Puede contener un único registro, cuando se usa desde un formulario, o muchos registros, cuando se usa desde la vista de lista. Ignoraremos el conjunto de registros de self y construiremos nuestro propio conjunto done_recs que contiene todas la tareas marcadas como finalizadas. Luego fijamos la señal activa como False, en todas ellas.
~~~

@api.multi
    def do_clear_done(self):
        done_recs = self.search([('is_done', '=', True)])
        done_recs.write({'active': False})
        return True
~~~

El search es un método de la API que devuelve los registros que cumplen con algunas condiciones. Estas condiciones son escritas en un dominio, esto es una lista de tríos. 

El método write fija los valores de todos los elementos en el conjunto de una vez. Los valores a escribir son definidos usando un diccionario. Usar write aquí es más eficiente que iterar a través de un conjunto de registros para asignar el valor uno por uno.


# Configurando la seguridad en el control de acceso
En este momento, nuestro modelo nuevo no tiene reglas de acceso, por lo tanto puede ser usado por cualquiera, no solo por el administrador.
Para tener una muestra de la información requerida para agregar reglas de acceso a un modelo, use el cliente web y diríjase a:
Configuración | Técnico | Seguridad | Lista controles de acceso.
Esta información debe ser provista por el modelo, usando un archivo de datos para cargar las líneas dentro del modelo ir.model.access. Daremos acceso completo al modelo al grupo empleado. Empleado es el grupo básico de acceso, casi todos pertenecen a este grupo.
Esto es realizado usualmente usando un archivo CSV llamado security/ir.model.access.csv.
Crearemos el archivo nuevo con el siguiente contenido:

~~~
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_aplicacionejemplo01_task_group_user,aplicacionejemplo01.task.user,model_aplicacionejemplo01_task,base.group_user,1,1,1,1
~~~

 Agregaremos la referencia a este archivo nuevo en el atributo "data" del descriptor en __openerp__.py, de la siguiente manera:
 ~~~

    'data' : ['aplicacionEjemplo01View.xml', 'security/ir.model.access.csv',],
 ~~~


Odoo es un sistema multi-usuario, y queremos que la aplicación to-do task sea privada para cada usuario.
Debemos crear un archivo security/todo_access_rules.xml con el siguiente contenido:
~~~~
<?xml version="1.0" encoding="utf-8"?>
    <openerp>
        <data noupdate="1">
            <record id="aplicacioejemplo01_task_user_rule" model="ir.rule">
                <field name="name">Aplicacion ejemplo 01 Tasks only for owner</field>
                <field name="model_id" ref="model_aplicacionejemplo01_task"/>
                <field name="domain_force">
                    [('create_uid','=',user.id)]
                </field>
                <field name="groups" eval="[(4,ref('base.group_user'))]"/>
            </record>
        </data>
    </openerp>
~~~~

Como se hizo anteriormente, debemos agregar el archivo a __openerp__.py.

# Agregar un ícono al módulo

 Para esto solo debemos agregar al módulo el archivo static/description/icon.png con el ícono que usaremos.










[^ref1]: http://fundamentos-de-desarrollo-en-odoo.readthedocs.io/es/latest/capitulos/construyendo-tu-primera-aplicacion-odoo.html

