# 💰 Módulo Financiero Completo - CRM Legal

## 📋 Descripción General

El **Módulo Financiero** es un sistema integral de gestión financiera para el CRM Legal que permite manejar todo el ciclo financiero de los casos legales: desde la creación de presupuestos hasta el registro de pagos, pasando por la gestión de facturas y el control de estados de cuenta.

## ✨ Características Principales

### 🎯 Funcionalidades Core
- **Gestión de Conceptos**: Catálogo completo de servicios legales con precios y categorías
- **Presupuestos Inteligentes**: Creación de presupuestos detallados con items y cálculos automáticos
- **Facturación Integrada**: Conversión de presupuestos a facturas y facturación directa
- **Control de Pagos**: Registro de pagos con actualización automática de saldos
- **Reportes Financieros**: Resúmenes y estadísticas financieras por caso
- **Estados y Workflow**: Flujo completo desde borrador hasta pago completado

### 📊 Capacidades Avanzadas
- **Cálculo Automático**: Subtotales, impuestos y totales calculados automáticamente
- **Numeración Consecutiva**: Generación automática de números de presupuestos y facturas
- **Múltiples Monedas**: Soporte para diferentes monedas
- **Auditoría Completa**: Tracking de cambios y timestamps en todas las operaciones
- **Integración Total**: Vinculación completa con casos y clientes existentes
- **Validaciones Robustas**: Controles de integridad y validaciones de datos financieros

## 🏗️ Arquitectura Técnica

### 📁 Estructura de Archivos

```
CRM-Legal/
├── financiero_ui.py                    # Módulo de interfaz de usuario
├── crm_database.py                     # Funciones CRUD (modificado)
├── main_app.py                         # Integración principal (modificado)
├── migration_sistema_financiero.sql    # Script de migración BD
├── init_conceptos_facturacion.py       # Inicialización de conceptos
├── test_financiero.py                  # Script de pruebas
└── docs/
    └── modulo_financiero_completo.md   # Esta documentación
```

### 🗄️ Esquema de Base de Datos

#### Tabla: `conceptos_facturacion`
Catálogo de servicios legales y sus tarifas.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | INTEGER PRIMARY KEY | ID único del concepto |
| `codigo` | TEXT UNIQUE | Código único (ej: CONS001, AUD001) |
| `nombre` | TEXT NOT NULL | Nombre del concepto |
| `descripcion` | TEXT | Descripción detallada |
| `categoria` | TEXT DEFAULT 'General' | Categoría del servicio |
| `precio_sugerido` | DECIMAL(12,2) | Precio sugerido por defecto |
| `unidad_medida` | TEXT DEFAULT 'Servicio' | Unidad de medida |
| `activo` | INTEGER DEFAULT 1 | Estado activo/inactivo |
| `created_at` | INTEGER | Timestamp de creación |
| `updated_at` | INTEGER | Timestamp de actualización |

#### Tabla: `presupuestos`
Presupuestos de servicios legales por caso.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | INTEGER PRIMARY KEY | ID único del presupuesto |
| `caso_id` | INTEGER NOT NULL | Referencia al caso |
| `numero_presupuesto` | TEXT UNIQUE | Número único (PRES-YYYY-####) |
| `fecha_creacion` | TEXT NOT NULL | Fecha de creación |
| `fecha_vencimiento` | TEXT | Fecha de vencimiento |
| `estado` | TEXT DEFAULT 'Borrador' | Estado del presupuesto |
| `moneda` | TEXT DEFAULT 'COP' | Moneda del presupuesto |
| `subtotal` | DECIMAL(12,2) | Subtotal antes de impuestos |
| `impuestos` | DECIMAL(12,2) | Valor de impuestos |
| `total` | DECIMAL(12,2) | Total final |
| `notas` | TEXT | Notas adicionales |
| `condiciones_pago` | TEXT | Condiciones de pago |
| `validez_dias` | INTEGER DEFAULT 30 | Días de validez |
| `created_by` | TEXT | Usuario creador |
| `approved_by` | TEXT | Usuario aprobador |
| `approved_at` | INTEGER | Timestamp de aprobación |
| `created_at` | INTEGER | Timestamp de creación |
| `updated_at` | INTEGER | Timestamp de actualización |

#### Tabla: `items_presupuesto`
Detalles de items por presupuesto.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | INTEGER PRIMARY KEY | ID único del item |
| `presupuesto_id` | INTEGER NOT NULL | Referencia al presupuesto |
| `concepto_id` | INTEGER | Referencia al concepto (opcional) |
| `descripcion` | TEXT NOT NULL | Descripción del item |
| `cantidad` | DECIMAL(10,2) | Cantidad |
| `precio_unitario` | DECIMAL(12,2) | Precio unitario |
| `subtotal` | DECIMAL(12,2) | Subtotal calculado |
| `orden` | INTEGER DEFAULT 1 | Orden de presentación |
| `notas` | TEXT | Notas del item |
| `created_at` | INTEGER | Timestamp de creación |

#### Tabla: `facturas`
Facturas generadas desde presupuestos o directamente.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | INTEGER PRIMARY KEY | ID único de la factura |
| `presupuesto_id` | INTEGER | Referencia al presupuesto origen |
| `caso_id` | INTEGER NOT NULL | Referencia al caso |
| `numero_factura` | TEXT UNIQUE | Número único (FACT-YYYY-####) |
| `fecha_emision` | TEXT NOT NULL | Fecha de emisión |
| `fecha_vencimiento` | TEXT | Fecha de vencimiento |
| `estado` | TEXT DEFAULT 'Pendiente' | Estado de la factura |
| `moneda` | TEXT DEFAULT 'COP' | Moneda |
| `subtotal` | DECIMAL(12,2) | Subtotal |
| `impuestos` | DECIMAL(12,2) | Impuestos |
| `total` | DECIMAL(12,2) | Total de la factura |
| `total_pagado` | DECIMAL(12,2) | Total pagado |
| `saldo_pendiente` | DECIMAL(12,2) | Saldo pendiente |
| `notas` | TEXT | Notas de la factura |
| `condiciones_pago` | TEXT | Condiciones de pago |
| `created_by` | TEXT | Usuario creador |
| `created_at` | INTEGER | Timestamp de creación |
| `updated_at` | INTEGER | Timestamp de actualización |

#### Tabla: `pagos`
Registro de pagos recibidos por facturas.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | INTEGER PRIMARY KEY | ID único del pago |
| `factura_id` | INTEGER NOT NULL | Referencia a la factura |
| `numero_pago` | TEXT | Número de referencia del pago |
| `fecha_pago` | TEXT NOT NULL | Fecha del pago |
| `metodo_pago` | TEXT | Método de pago |
| `referencia` | TEXT | Referencia del pago |
| `monto` | DECIMAL(12,2) NOT NULL | Monto del pago |
| `moneda` | TEXT DEFAULT 'COP' | Moneda del pago |
| `notas` | TEXT | Notas del pago |
| `comprobante_ruta` | TEXT | Ruta al comprobante |
| `registrado_por` | TEXT | Usuario que registró |
| `created_at` | INTEGER | Timestamp de creación |
| `updated_at` | INTEGER | Timestamp de actualización |

### 🔗 Relaciones y Constraints
- **Foreign Keys**: Integridad referencial con CASCADE DELETE
- **Unique Constraints**: Números únicos de presupuestos y facturas
- **Índices**: Optimización para búsquedas frecuentes
- **Triggers**: Actualización automática de timestamps

## 🎨 Interfaz de Usuario

### 📑 Pestaña Principal: "Financiero"

La interfaz está organizada en un notebook con 4 pestañas principales:

#### 1. 📋 Pestaña "Presupuestos"

**Área Superior: Información y Controles**
- **Información del Caso**: Muestra el caso actualmente seleccionado
- **Botones de Acción**:
  - `Nuevo Presupuesto`: Crea un presupuesto para el caso actual
  - `Editar`: Modifica el presupuesto seleccionado
  - `Generar Factura`: Convierte presupuesto aprobado en factura

**Área Central: Lista de Presupuestos**
- TreeView con columnas: ID, Número, Fecha, Estado, Moneda, Total, Vencimiento
- Selección simple con doble clic para editar
- Actualización automática al seleccionar caso

**Área Inferior: Detalles del Presupuesto**
- **Items del Presupuesto**: TreeView con descripción, cantidad, precio unit., subtotal
- **Totales**: Subtotal, impuestos y total final resaltados
- **Actualización Dinámica**: Se actualiza al seleccionar presupuesto

#### 2. 💰 Pestaña "Facturas y Pagos"

**Sección Superior: Facturas**
- Lista de facturas del caso con: ID, Número, Fecha, Estado, Total, Pagado, Saldo
- Botón para crear facturas directas (sin presupuesto previo)
- Estados: Pendiente, Pagada, Vencida, Anulada

**Sección Inferior: Pagos**
- Lista de pagos de la factura seleccionada
- Botón `Registrar Pago` para agregar nuevos pagos
- Actualización automática de saldos

#### 3. 🏷️ Pestaña "Conceptos"

**Área Superior: Filtros y Controles**
- **Filtro por Categoría**: ComboBox para filtrar conceptos
- **Botones de Gestión**:
  - `Nuevo Concepto`: Crea concepto de facturación
  - `Editar`: Modifica concepto seleccionado
  - `Eliminar`: Desactiva concepto

**Área Principal: Catálogo de Conceptos**
- TreeView con: ID, Código, Nombre, Categoría, Precio Sugerido, Unidad
- Gestión completa de conceptos de facturación
- Filtrado en tiempo real por categoría

#### 4. 📊 Pestaña "Reportes"

**Controles Superiores**
- Botón `Resumen del Caso Actual`: Genera reporte financiero completo

**Área de Resultados**
- Text widget con reporte detallado:
  - Estadísticas de presupuestos
  - Resumen de facturas y pagos
  - Tasa de cobro y estado financiero

### 🔧 Diálogos Especializados

#### Diálogo de Presupuesto
- **Información Básica**: Fecha vencimiento, estado, notas
- **Gestión de Items**: TreeView editable con items del presupuesto
- **Botones de Items**: Agregar y eliminar items
- **Validaciones**: Datos requeridos y formatos correctos

#### Diálogo de Item
- **Campos**: Descripción, cantidad, precio unitario
- **Cálculo Automático**: Subtotal calculado dinámicamente
- **Validaciones**: Cantidades positivas y precios válidos

#### Diálogo de Concepto
- **Datos Completos**: Código, nombre, descripción, categoría
- **Configuración**: Precio sugerido y unidad de medida
- **Categorías Predefinidas**: Lista de categorías comunes

#### Diálogo de Pago
- **Información de Factura**: Resumen de la factura seleccionada
- **Datos del Pago**: Fecha, monto, método, referencia
- **Validaciones**: Monto positivo y fechas válidas
- **Actualización Automática**: Recalcula saldos al confirmar

## 🔧 API de Funciones (crm_database.py)

### 📝 Funciones CRUD para Conceptos de Facturación

#### `add_concepto_facturacion(codigo, nombre, descripcion, categoria, precio_sugerido, unidad_medida)`
Crea un nuevo concepto de facturación.
- **Validaciones**: Código único, datos requeridos
- **Retorna**: ID del nuevo concepto o None si falla

#### `get_conceptos_facturacion(solo_activos=True)`
Obtiene todos los conceptos de facturación.
- **Filtros**: Solo activos o todos
- **Retorna**: Lista de diccionarios con conceptos

#### `update_concepto_facturacion(concepto_id, codigo, nombre, descripcion, categoria, precio_sugerido, unidad_medida)`
Actualiza un concepto existente.
- **Validaciones**: Código único, integridad de datos

#### `delete_concepto_facturacion(concepto_id)`
Desactiva un concepto (soft delete).
- **Manejo**: Preserva relaciones existentes

#### `get_categorias_conceptos()`
Obtiene categorías únicas de conceptos activos.

### 💰 Funciones de Presupuestos

#### `generate_numero_presupuesto()`
Genera número único consecutivo (PRES-YYYY-####).
- **Formato**: Año actual + secuencial de 4 dígitos
- **Automatización**: Incremento automático

#### `add_presupuesto(caso_id, fecha_vencimiento, estado, moneda, notas, condiciones_pago, validez_dias, created_by)`
Crea un nuevo presupuesto para un caso.
- **Automatización**: Número consecutivo automático
- **Integración**: Actualiza actividad del caso

#### `get_presupuestos_by_caso(caso_id)`
Obtiene todos los presupuestos de un caso.
- **Ordenamiento**: Por fecha de creación descendente

#### `update_presupuesto(presupuesto_id, ...)`
Actualiza datos básicos del presupuesto.

#### `recalcular_totales_presupuesto(presupuesto_id)`
Recalcula subtotal, impuestos y total automáticamente.
- **Cálculos**: IVA 19% automático
- **Triggers**: Se ejecuta al modificar items

### 📄 Funciones de Items de Presupuesto

#### `add_item_presupuesto(presupuesto_id, descripcion, cantidad, precio_unitario, concepto_id, notas, orden)`
Agrega un item al presupuesto.
- **Cálculos**: Subtotal automático
- **Triggers**: Recalcula totales del presupuesto

#### `get_items_presupuesto(presupuesto_id)`
Obtiene items de un presupuesto con datos de conceptos.

#### `update_item_presupuesto(item_id, ...)`
Actualiza un item existente.

#### `delete_item_presupuesto(item_id)`
Elimina un item y recalcula totales.

### 🧾 Funciones de Facturas

#### `generate_numero_factura()`
Genera número único consecutivo (FACT-YYYY-####).

#### `create_factura_from_presupuesto(presupuesto_id, fecha_vencimiento, notas, condiciones_pago, created_by)`
Convierte presupuesto aprobado en factura.
- **Validaciones**: Solo presupuestos aprobados
- **Copia**: Traslada totales del presupuesto

#### `get_facturas_by_caso(caso_id)`
Obtiene facturas de un caso con datos del presupuesto origen.

#### `get_factura_by_id(factura_id)`
Obtiene factura con datos de caso y cliente.

### 💳 Funciones de Pagos

#### `add_pago(factura_id, fecha_pago, monto, metodo_pago, referencia, notas, registrado_por)`
Registra un pago para una factura.
- **Automatización**: 
  - Genera número de pago automático
  - Actualiza totales de factura
  - Cambia estado si queda saldada
  - Actualiza actividad del caso

#### `get_pagos_by_factura(factura_id)`
Obtiene todos los pagos de una factura.

### 📊 Funciones de Reportes

#### `get_resumen_financiero_caso(caso_id)`
Genera resumen financiero completo de un caso.

**Estructura del resumen**:
```python
{
    'presupuestos': {
        'total': int,
        'aprobados': int,
        'valor_aprobado': float
    },
    'facturas': {
        'total': int,
        'pagadas': int,
        'pendientes': int,
        'valor_total': float,
        'valor_pagado': float,
        'saldo_pendiente': float
    },
    'pagos': {
        'total': int,
        'valor_total': float
    }
}
```

## 🚀 Integración con Sistema Principal

### 📱 Integración en main_app.py

#### Importaciones Agregadas
```python
from financiero_ui import FinancieroTab
```

#### Nueva Pestaña en Notebook
```python
self.financiero_tab_frame = FinancieroTab(self.main_notebook, self)
self.main_notebook.add(self.financiero_tab_frame, text="Financiero")
```

#### Estados de Pestaña
- **Deshabilitada**: Cuando no hay caso seleccionado
- **Habilitada**: Al seleccionar un caso válido
- **Actualización**: Automática al cambiar de caso

#### Llamadas en Eventos de Contexto
- `enable_detail_tabs_for_case()`: Habilita pestaña financiera
- `disable_detail_tabs_for_case()`: Deshabilita y limpia datos
- `on_case_select()`: Actualiza datos financieros del caso

### 🔄 Flujo de Integración

1. **Inicio de Aplicación**:
   - Se crea pestaña financiera deshabilitada
   - Se cargan conceptos de facturación
   - Pestañas en estado inicial

2. **Selección de Caso**:
   - Se habilita pestaña financiera
   - Se cargan presupuestos del caso
   - Se cargan facturas del caso
   - Se actualizan botones contextuales

3. **Desselección de Caso**:
   - Se deshabilita pestaña financiera
   - Se limpian todos los datos
   - Se restablecen estados iniciales

## 🗂️ Conceptos de Facturación Predefinidos

El sistema incluye 38 conceptos organizados en 8 categorías:

### 💬 Consultas (4 conceptos)
- **CONS001** - Consulta Legal Inicial ($150,000)
- **CONS002** - Consulta de Seguimiento ($100,000)
- **CONS003** - Consulta Especializada ($250,000)
- **CONS004** - Consulta Virtual ($120,000)

### 🏛️ Audiencias (5 conceptos)
- **AUD001** - Audiencia de Conciliación ($300,000)
- **AUD002** - Audiencia de Juicio ($500,000)
- **AUD003** - Audiencia Preparatoria ($250,000)
- **AUD004** - Audiencia de Alegatos ($400,000)
- **AUD005** - Audiencia de Apelación ($450,000)

### ✍️ Redacciones (6 conceptos)
- **RED001** - Redacción de Demanda ($400,000)
- **RED002** - Redacción de Contestación ($350,000)
- **RED003** - Redacción de Recurso ($300,000)
- **RED004** - Redacción de Contrato ($250,000)
- **RED005** - Redacción de Memorial ($200,000)
- **RED006** - Revisión de Documento ($100,000)

### ⚖️ Litigios (5 conceptos)
- **LIT001** - Representación en Juicio Civil ($1,500,000)
- **LIT002** - Representación en Juicio Penal ($2,000,000)
- **LIT003** - Representación en Juicio Laboral ($1,200,000)
- **LIT004** - Representación en Familia ($1,000,000)
- **LIT005** - Proceso de Tutela ($300,000)

### 🏢 Gestiones (5 conceptos)
- **GEST001** - Gestión Notarial ($150,000)
- **GEST002** - Gestión Registral ($200,000)
- **GEST003** - Gestión DIAN ($300,000)
- **GEST004** - Gestión Bancaria ($100,000)
- **GEST005** - Apostille y Legalización ($250,000)

### 💼 Asesorías (4 conceptos)
- **ASES001** - Asesoría Jurídica por Hora ($200,000)
- **ASES002** - Asesoría Empresarial ($300,000)
- **ASES003** - Asesoría en Compliance ($350,000)
- **ASES004** - Asesoría en Contratos ($250,000)

### 📚 Estudios (4 conceptos)
- **EST001** - Estudio de Títulos ($500,000)
- **EST002** - Análisis Legal ($400,000)
- **EST003** - Due Diligence Legal ($800,000)
- **EST004** - Concepto Jurídico ($300,000)

### 📎 Otros (5 conceptos)
- **OTROS001** - Desplazamiento ($50,000/km)
- **OTROS002** - Fotocopias ($100/página)
- **OTROS003** - Courier ($25,000/envío)
- **OTROS004** - Certificados ($15,000/certificado)
- **OTROS005** - Derechos de Petición ($100,000)

## 📈 Casos de Uso Principales

### 1. 📋 Creación de Presupuesto Completo
**Escenario**: Abogado crea presupuesto para nuevo caso
1. Selecciona cliente y caso en aplicación principal
2. Va a pestaña "Financiero" → "Presupuestos"
3. Clic en "Nuevo Presupuesto"
4. Completa información básica (fecha vencimiento, notas)
5. Agrega items desde conceptos predefinidos o personalizados
6. Sistema calcula automáticamente subtotal, impuestos y total
7. Guarda presupuesto en estado "Borrador"
8. Puede cambiar estado a "Enviado" cuando se envía al cliente

### 2. 💰 Facturación desde Presupuesto Aprobado
**Escenario**: Cliente aprueba presupuesto y se genera factura
1. Selecciona presupuesto aprobado en lista
2. Clic en "Generar Factura"
3. Sistema crea factura automáticamente con:
   - Número consecutivo único
   - Todos los datos del presupuesto
   - Estado inicial "Pendiente"
4. Factura aparece en pestaña "Facturas y Pagos"

### 3. 🧾 Registro de Pagos
**Escenario**: Cliente realiza pago de factura
1. Va a pestaña "Facturas y Pagos"
2. Selecciona factura pendiente
3. Clic en "Registrar Pago"
4. Completa datos del pago (fecha, monto, método, referencia)
5. Sistema actualiza automáticamente:
   - Total pagado de la factura
   - Saldo pendiente
   - Estado de la factura (si queda saldada)
6. Pago aparece en lista de pagos de la factura

### 4. 📊 Generación de Reportes Financieros
**Escenario**: Análisis financiero de un caso
1. Selecciona caso de interés
2. Va a pestaña "Reportes"
3. Clic en "Resumen del Caso Actual"
4. Sistema genera reporte completo mostrando:
   - Estadísticas de presupuestos
   - Estado de facturas y pagos
   - Tasa de cobro
   - Estado financiero general

### 5. 🏷️ Gestión de Conceptos de Facturación
**Escenario**: Actualización de tarifas de servicios
1. Va a pestaña "Conceptos"
2. Selecciona concepto a actualizar
3. Clic en "Editar"
4. Modifica precio sugerido o descripción
5. Guarda cambios
6. Concepto actualizado está disponible para nuevos presupuestos

## 🔧 Configuración y Mantenimiento

### 📥 Instalación
1. **Automática**: El módulo se integra automáticamente al ejecutar main_app.py
2. **Base de Datos**: Las tablas se crean automáticamente en primera ejecución
3. **Conceptos Predefinidos**: Se cargan ejecutando `init_conceptos_facturacion.py`

### 🔄 Migración de Datos
- **Script SQL**: `migration_sistema_financiero.sql` contiene migración completa
- **Compatibilidad**: 100% compatible con versiones anteriores
- **Triggers**: Incluye triggers para automatización de timestamps

### 🧹 Mantenimiento
- **Soft Delete**: Los conceptos se desactivan, no se eliminan físicamente
- **Integridad**: Foreign keys mantienen consistencia de datos
- **Triggers**: Automatizan actualización de timestamps
- **Auditoría**: Todos los cambios quedan registrados

## 🎯 Mejores Prácticas

### 💰 Gestión Financiera
- **Presupuestos Detallados**: Usar items específicos en lugar de conceptos generales
- **Estados Claros**: Mantener workflow correcto (Borrador → Enviado → Aprobado)
- **Registro Oportuno**: Registrar pagos inmediatamente al recibirlos
- **Revisión Regular**: Monitorear saldos pendientes y facturas vencidas

### 🏷️ Conceptos de Facturación
- **Códigos Consistentes**: Usar convención clara para códigos (TIPO###)
- **Precios Actualizados**: Revisar y actualizar precios periódicamente
- **Categorización**: Mantener categorías específicas y coherentes
- **Unidades Claras**: Especificar unidades de medida apropiadas

### 📊 Reportes y Análisis
- **Revisión Mensual**: Generar reportes regulares para análisis
- **Indicadores Clave**: Monitorear tasa de cobro y tiempos de pago
- **Proyecciones**: Usar datos históricos para proyecciones futuras

### 🔧 Mantenimiento del Sistema
- **Backup Regular**: Respaldar base de datos regularmente
- **Validación de Datos**: Verificar integridad periódicamente
- **Limpieza**: Limpiar conceptos obsoletos (desactivar, no eliminar)

## 🚀 Extensiones Futuras

### 🔮 Funcionalidades Potenciales
- **Facturación Electrónica**: Integración con DIAN para facturación electrónica
- **Reportes Avanzados**: Dashboards con gráficos y métricas avanzadas
- **Plantillas**: Plantillas de presupuestos por tipo de caso
- **Recordatorios**: Alertas de facturas por vencer o vencidas
- **Múltiples Impuestos**: Soporte para diferentes tipos de impuestos
- **Descuentos**: Sistema de descuentos y promociones
- **Cuentas por Cobrar**: Módulo avanzado de cartera
- **Integración Bancaria**: Conciliación automática con extractos bancarios

### 🔧 Mejoras Técnicas
- **Performance**: Optimización de consultas para grandes volúmenes
- **Export/Import**: Exportación a Excel y otros formatos
- **API**: Servicios web para integración con otros sistemas
- **Roles**: Permisos específicos por tipo de usuario
- **Workflow**: Flujos de aprobación configurables

## 📚 Referencias Técnicas

### 🔗 Dependencias
- **tkinter**: Interfaz gráfica (built-in)
- **sqlite3**: Base de datos (built-in)
- **time**: Timestamps (built-in)
- **datetime**: Manejo de fechas (built-in)
- **decimal**: Precisión monetaria (built-in)

### 📖 Patrones Implementados
- **MVC**: Separación modelo-vista-controlador
- **Observer**: Actualización de estado entre componentes
- **Factory**: Creación de diálogos reutilizables
- **Strategy**: Diferentes métodos de cálculo de impuestos
- **Template Method**: Flujo común de creación de documentos

### 🎯 Convenciones de Código
- **PEP 8**: Estilo de código Python
- **Docstrings**: Documentación de funciones
- **Type Safety**: Validaciones robustas de tipos
- **Error Handling**: Manejo comprehensivo de excepciones
- **Logging**: Registro de operaciones críticas

### 💱 Consideraciones Monetarias
- **Precisión Decimal**: Uso de DECIMAL(12,2) para evitar errores de redondeo
- **Validaciones**: Control estricto de valores monetarios
- **Consistency**: Manejo consistente de monedas
- **Auditoría**: Registro completo de cambios monetarios

---

> **Nota**: Este módulo fue diseñado siguiendo las mejores prácticas de desarrollo de software financiero, garantizando precisión, seguridad e integridad en el manejo de datos monetarios.
