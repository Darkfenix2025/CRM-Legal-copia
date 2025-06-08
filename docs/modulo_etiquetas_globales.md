# 🏷️ Módulo de Etiquetas Globales - CRM Legal

## 📋 Descripción General

El módulo de **Etiquetas Globales** es un sistema completo de gestión de etiquetas reutilizables para el CRM Legal. Permite clasificar, organizar y filtrar casos y clientes mediante etiquetas personalizadas con colores y categorías, mejorando significativamente la organización y búsqueda de información.

## ✨ Características Principales

### 🎯 Funcionalidades Core
- **Gestión de Etiquetas**: Crear, editar, eliminar y gestionar etiquetas globales
- **Categorización**: Organizar etiquetas en categorías (Tipo de Caso, Estado, Prioridad, etc.)
- **Colores Personalizados**: Asignar colores hexadecimales para identificación visual
- **Asignación Flexible**: Aplicar etiquetas tanto a casos como a clientes
- **Búsqueda y Filtrado**: Localizar registros por etiquetas asignadas
- **Reutilización**: Una vez creadas, las etiquetas pueden aplicarse múltiples veces

### 📊 Capacidades Avanzadas
- **Vista Estadística**: Contador de casos y clientes por etiqueta
- **Asignación Rápida**: Botones contextuales para asignar al registro actual
- **Visualización Detallada**: Ventanas emergentes con listas de registros etiquetados
- **Filtros por Categoría**: Filtrar vista por categorías de etiquetas
- **Prevención de Duplicados**: Sistema que evita asignaciones duplicadas

## 🏗️ Arquitectura Técnica

### 📁 Estructura de Archivos

```
CRM-Legal/
├── etiquetas_ui.py                    # Módulo de interfaz de usuario
├── crm_database.py                    # Funciones CRUD (modificado)
├── main_app.py                        # Integración principal (modificado)
├── migration_etiquetas_globales.sql   # Script de migración BD
└── docs/
    └── modulo_etiquetas_globales.md   # Esta documentación
```

### 🗄️ Esquema de Base de Datos

#### Tabla: `etiquetas_globales`
Almacena las definiciones de etiquetas globales.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | INTEGER PRIMARY KEY | ID único de la etiqueta |
| `nombre` | TEXT NOT NULL UNIQUE | Nombre único de la etiqueta |
| `descripcion` | TEXT | Descripción opcional |
| `color_hex` | TEXT DEFAULT '#0066CC' | Color en formato hexadecimal |
| `categoria` | TEXT DEFAULT 'General' | Categoría de organización |
| `activa` | INTEGER DEFAULT 1 | Estado (1=activa, 0=desactivada) |
| `created_at` | INTEGER | Timestamp de creación |

#### Tabla: `caso_etiquetas`
Relación muchos-a-muchos entre casos y etiquetas.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | INTEGER PRIMARY KEY | ID único de la relación |
| `caso_id` | INTEGER NOT NULL | Referencia a casos.id |
| `etiqueta_id` | INTEGER NOT NULL | Referencia a etiquetas_globales.id |
| `fecha_asignacion` | INTEGER | Timestamp de asignación |
| `asignado_por` | TEXT | Usuario que asignó la etiqueta |

#### Tabla: `cliente_etiquetas`
Relación muchos-a-muchos entre clientes y etiquetas.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | INTEGER PRIMARY KEY | ID único de la relación |
| `cliente_id` | INTEGER NOT NULL | Referencia a clientes.id |
| `etiqueta_id` | INTEGER NOT NULL | Referencia a etiquetas_globales.id |
| `fecha_asignacion` | INTEGER | Timestamp de asignación |
| `asignado_por` | TEXT | Usuario que asignó la etiqueta |

### 🔗 Relaciones y Constraints
- **Foreign Keys**: Integridad referencial con CASCADE DELETE
- **Unique Constraints**: Prevención de nombres duplicados y asignaciones duplicadas
- **Índices**: Optimización para búsquedas por nombre, categoría, caso_id, etiqueta_id

## 🎨 Interfaz de Usuario

### 📑 Pestaña Principal: "Etiquetas"

#### Área Superior: Controles y Filtros
- **Filtro por Categoría**: ComboBox para filtrar etiquetas por categoría
- **Botones de Acción**:
  - `Nueva Etiqueta`: Abre diálogo de creación
  - `Editar`: Modifica etiqueta seleccionada
  - `Eliminar`: Desactiva etiqueta (soft delete)

#### Área Central: TreeView de Etiquetas
Columnas mostradas:
- **ID**: Identificador único
- **Nombre**: Nombre de la etiqueta
- **Descripción**: Descripción (truncada a 50 caracteres)
- **Categoría**: Categoría de organización
- **Color**: Indicador visual del color
- **# Casos**: Cantidad de casos asignados
- **# Clientes**: Cantidad de clientes asignados

#### Área Inferior: Detalles y Asignaciones
**Panel Izquierdo - Detalles**:
- Nombre completo
- Descripción completa (Text widget)
- Categoría

**Panel Derecho - Asignación Rápida**:
- `Asignar a Caso Actual`: Asigna etiqueta al caso seleccionado
- `Asignar a Cliente Actual`: Asigna etiqueta al cliente seleccionado
- `Ver Casos con Esta Etiqueta`: Ventana emergente con lista de casos
- `Ver Clientes con Esta Etiqueta`: Ventana emergente con lista de clientes

### 🔧 Diálogo de Etiqueta

#### Campos del Formulario
- **Nombre*** (requerido): Campo de texto único
- **Descripción**: Área de texto multilínea
- **Categoría*** (requerido): ComboBox con categorías existentes y predefinidas
- **Color**: Selector de color con preview visual

#### Categorías Predefinidas
- `General`: Etiquetas generales
- `Tipo de Caso`: Clasificación por área del derecho
- `Estado`: Estado procesal o de tramitación
- `Prioridad`: Nivel de urgencia o importancia
- `Cliente`: Características del cliente
- `Especialidad`: Área de especialización

#### Validaciones
- Nombre único (no duplicados)
- Longitud máxima: 100 caracteres
- Color en formato hexadecimal válido (#RRGGBB)
- Campos requeridos marcados con asterisco

## 🔧 API de Funciones (crm_database.py)

### 📝 Funciones CRUD para Etiquetas Globales

#### `add_etiqueta_global(nombre, descripcion="", color_hex="#0066CC", categoria="General")`
Crea una nueva etiqueta global.
- **Retorna**: ID de la nueva etiqueta o None si falla
- **Maneja**: Duplicados (IntegrityError)

#### `get_etiquetas_globales(solo_activas=True)`
Obtiene todas las etiquetas globales.
- **Parámetros**: `solo_activas` - Filtrar solo etiquetas activas
- **Retorna**: Lista de diccionarios con datos de etiquetas

#### `get_etiqueta_global_by_id(etiqueta_id)`
Obtiene una etiqueta específica por ID.
- **Retorna**: Diccionario con datos de la etiqueta o None

#### `update_etiqueta_global(etiqueta_id, nombre, descripcion, color_hex, categoria)`
Actualiza una etiqueta existente.
- **Retorna**: True si exitoso, False si falla

#### `delete_etiqueta_global(etiqueta_id)`
Desactiva una etiqueta (soft delete).
- **Retorna**: True si exitoso, False si falla

#### `get_categorias_etiquetas()`
Obtiene todas las categorías únicas de etiquetas activas.
- **Retorna**: Lista de strings con nombres de categorías

### 🔗 Funciones de Relaciones Caso-Etiquetas

#### `asignar_etiqueta_a_caso(caso_id, etiqueta_id, asignado_por="Sistema")`
Asigna una etiqueta a un caso.
- **Maneja**: Duplicados automáticamente
- **Actualiza**: last_activity_timestamp del caso

#### `desasignar_etiqueta_de_caso(caso_id, etiqueta_id)`
Remueve una etiqueta de un caso.

#### `get_etiquetas_by_caso(caso_id)`
Obtiene todas las etiquetas de un caso.
- **Retorna**: Lista con datos de etiquetas y metadata de asignación

#### `get_casos_by_etiqueta(etiqueta_id)`
Obtiene todos los casos que tienen una etiqueta específica.

### 🔗 Funciones de Relaciones Cliente-Etiquetas

#### `asignar_etiqueta_a_cliente(cliente_id, etiqueta_id, asignado_por="Sistema")`
Asigna una etiqueta a un cliente.

#### `desasignar_etiqueta_de_cliente(cliente_id, etiqueta_id)`
Remueve una etiqueta de un cliente.

#### `get_etiquetas_by_cliente(cliente_id)`
Obtiene todas las etiquetas de un cliente.

#### `get_clientes_by_etiqueta(etiqueta_id)`
Obtiene todos los clientes que tienen una etiqueta específica.

### 🔍 Funciones de Búsqueda y Filtrado

#### `buscar_casos_por_etiquetas(etiquetas_ids, operador='AND')`
Busca casos por múltiples etiquetas.
- **operador**: 'AND' (todos) o 'OR' (alguno)

#### `buscar_clientes_por_etiquetas(etiquetas_ids, operador='AND')`
Busca clientes por múltiples etiquetas.

## 🚀 Integración con Sistema Principal

### 📱 Integración en main_app.py

#### Importaciones Agregadas
```python
from etiquetas_ui import EtiquetasTab
```

#### Nueva Pestaña en Notebook
```python
self.etiquetas_tab_frame = EtiquetasTab(self.main_notebook, self)
self.main_notebook.add(self.etiquetas_tab_frame, text="Etiquetas")
```

#### Función de Actualización de Estado
```python
def update_etiquetas_buttons_state(self):
    if hasattr(self, 'etiquetas_tab_frame'):
        self.etiquetas_tab_frame.actualizar_estado_botones()
```

#### Llamadas en Eventos de Contexto
- `load_clients()`: Al cargar clientes
- `on_client_select()`: Al seleccionar cliente
- `on_case_select()`: Al seleccionar caso

### 🔄 Flujo de Integración

1. **Inicio de Aplicación**:
   - Se crea pestaña de etiquetas
   - Se cargan etiquetas existentes
   - Botones en estado inicial

2. **Selección de Cliente**:
   - Se actualiza estado de botones
   - Se habilita "Asignar a Cliente Actual"

3. **Selección de Caso**:
   - Se actualiza estado de botones
   - Se habilita "Asignar a Caso Actual"

4. **Gestión de Etiquetas**:
   - Creación/edición independiente del contexto
   - Asignación contextual según selección actual

## 🗂️ Etiquetas Predefinidas

El sistema incluye etiquetas predefinidas para comenzar inmediatamente:

### 🚨 Prioridad
- **Urgente** (#FF3333): Casos que requieren atención inmediata

### ⚖️ Tipo de Caso
- **Laboral** (#0066CC): Derecho laboral
- **Penal** (#8B0000): Derecho penal
- **Civil** (#006600): Derecho civil
- **Familia** (#FF6600): Derecho de familia

### 📊 Estado
- **En Proceso** (#3366CC): Tramitación activa
- **Finalizado** (#666666): Casos cerrados
- **Suspendido** (#FF9900): Temporalmente suspendidos

### 👥 Cliente
- **VIP** (#FF0066): Alta prioridad
- **Empresarial** (#0099CC): Clientes corporativos
- **Particular** (#009966): Clientes individuales

## 📈 Casos de Uso Principales

### 1. 📋 Gestión de Etiquetas
**Escenario**: Administrador del sistema crea nuevas etiquetas
1. Accede a pestaña "Etiquetas"
2. Clic en "Nueva Etiqueta"
3. Completa formulario (nombre, descripción, categoría, color)
4. Guarda etiqueta
5. Etiqueta aparece en lista principal

### 2. 🏷️ Asignación de Etiquetas a Casos
**Escenario**: Usuario etiqueta un caso específico
1. Selecciona cliente en lista principal
2. Selecciona caso en lista de casos
3. Va a pestaña "Etiquetas"
4. Selecciona etiqueta deseada
5. Clic en "Asignar a Caso Actual"
6. Etiqueta se asigna al caso

### 3. 🔍 Búsqueda por Etiquetas
**Escenario**: Usuario busca todos los casos de tipo "Laboral"
1. Va a pestaña "Etiquetas"
2. Selecciona etiqueta "Laboral"
3. Clic en "Ver Casos con Esta Etiqueta"
4. Se abre ventana con lista filtrada de casos laborales

### 4. 📂 Organización por Categorías
**Escenario**: Usuario organiza etiquetas por tipo
1. Usa filtro de categoría en parte superior
2. Selecciona "Tipo de Caso"
3. Vista se filtra mostrando solo etiquetas de esa categoría
4. Puede gestionar etiquetas específicas del tipo

## 🔧 Configuración y Mantenimiento

### 📥 Instalación
1. **Automática**: El módulo se integra automáticamente al ejecutar main_app.py
2. **Base de Datos**: Las tablas se crean automáticamente en primera ejecución
3. **Etiquetas Predefinidas**: Se insertan automáticamente si no existen

### 🔄 Migración de Datos
- **Script SQL**: `migration_etiquetas_globales.sql` contiene migración completa
- **Compatibilidad**: 100% compatible con versiones anteriores
- **Rollback**: Incluye instrucciones de reversión en caso necesario

### 🧹 Mantenimiento
- **Soft Delete**: Las etiquetas se desactivan, no se eliminan físicamente
- **Integridad**: Foreign keys mantienen consistencia de datos
- **Índices**: Optimizan consultas frecuentes automáticamente

## 🎯 Mejores Prácticas

### 📝 Nomenclatura de Etiquetas
- **Nombres Descriptivos**: Usar nombres claros y específicos
- **Consistencia**: Mantener convenciones de naming
- **Categorización**: Agrupar etiquetas relacionadas en misma categoría

### 🎨 Gestión de Colores
- **Contraste**: Usar colores que contrasten bien con fondo blanco
- **Significado**: Asignar colores con significado (rojo=urgente, verde=completado)
- **Accesibilidad**: Considerar usuarios con daltonismo

### 🗂️ Organización de Categorías
- **Específicas**: Crear categorías específicas en lugar de "General"
- **Consistentes**: Mantener categorías coherentes entre etiquetas similares
- **Escalables**: Pensar en crecimiento futuro del sistema

### 🔍 Estrategias de Búsqueda
- **Combinaciones**: Usar múltiples etiquetas para búsquedas específicas
- **Jerarquías**: Crear etiquetas que se complementen (ej: "Civil" + "Urgente")
- **Actualizaciones**: Mantener etiquetas actualizadas según evolución de casos

## 🚀 Extensiones Futuras

### 🔮 Funcionalidades Potenciales
- **Etiquetas Anidadas**: Jerarquías de etiquetas padre-hijo
- **Auto-etiquetado**: Asignación automática basada en palabras clave
- **Reportes**: Estadísticas y reportes por etiquetas
- **Exportación**: Exportar datos filtrados por etiquetas
- **Plantillas**: Conjuntos predefinidos de etiquetas por tipo de caso
- **Alertas**: Notificaciones basadas en combinaciones de etiquetas

### 🔧 Mejoras Técnicas
- **Performance**: Cache de consultas frecuentes
- **Audit Trail**: Historial de cambios en etiquetas
- **Permisos**: Control de acceso por roles de usuario
- **Sincronización**: Backup y restore de configuración de etiquetas

## 📚 Referencias Técnicas

### 🔗 Dependencias
- **tkinter**: Interfaz gráfica (built-in)
- **sqlite3**: Base de datos (built-in)
- **time**: Timestamps (built-in)

### 📖 Patrones Implementados
- **MVC**: Separación modelo-vista-controlador
- **Observer**: Actualización de estado entre componentes
- **Factory**: Creación de diálogos reutilizables
- **Soft Delete**: Desactivación en lugar de eliminación física

### 🎯 Convenciones de Código
- **PEP 8**: Estilo de código Python
- **Docstrings**: Documentación de funciones
- **Type Hints**: Tipado implícito mediante comentarios
- **Error Handling**: Manejo robusto de excepciones

---

> **Nota**: Este módulo fue diseñado siguiendo los patrones arquitectónicos existentes del CRM Legal, garantizando máxima compatibilidad e integración seamless con el sistema existente.
