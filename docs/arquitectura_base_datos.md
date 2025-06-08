# Arquitectura de Base de Datos - CRM Legal

## Diagrama de Entidades y Relaciones

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│    CLIENTES     │       │      CASOS      │       │   AUDIENCIAS    │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ id (PK)         │◄─────┐│ id (PK)         │◄─────┐│ id (PK)         │
│ nombre          │      ││ cliente_id (FK) │      ││ caso_id (FK)    │
│ direccion       │      ││ numero_expediente│      ││ fecha           │
│ email           │      ││ anio_caratula   │      ││ hora            │
│ whatsapp        │      ││ caratula        │      ││ descripcion     │
│ created_at      │      ││ juzgado         │      ││ link            │
└─────────────────┘      ││ jurisdiccion    │      ││ recordatorio_*  │
                         ││ etapa_procesal  │      ││ created_at      │
                         ││ notas           │      │└─────────────────┘
                         ││ ruta_carpeta    │      │
                         ││ inactivity_*    │      │
                         ││ created_at      │      │
                         ││ last_activity_* │      │
                         │└─────────────────┘      │
                         │                         │
                         │┌─────────────────┐      │
                         ││ ACTIVIDADES_CASO│      │
                         │├─────────────────┤      │
                         ││ id (PK)         │      │
                         └┤ caso_id (FK)    │      │
                          │ fecha_hora      │      │
                          │ tipo_actividad  │      │
                          │ descripcion     │      │
                          │ creado_por      │      │
                          │ referencia_doc  │      │
                          └─────────────────┘      │
                                                   │
                         ┌─────────────────┐       │
                         │PARTES_INTERVINT │       │
                         ├─────────────────┤       │
                         │ id (PK)         │       │
                         ├─caso_id (FK)    │◄──────┘
                         │ nombre          │
                         │ tipo            │
                         │ direccion       │
                         │ contacto        │
                         │ created_at      │
                         └─────────────────┘
```

## Análisis Detallado por Tabla

### 1. Tabla `clientes`

```sql
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    direccion TEXT,
    email TEXT,
    whatsapp TEXT,
    created_at INTEGER
);
```

**Características**:
- **Primary Key**: Auto-incremento para identificación única
- **Campos Obligatorios**: Solo `nombre` (flexibilidad en datos de contacto)
- **Timestamp**: Unix timestamp para created_at
- **Normalización**: Primera forma normal, datos atomicos

**Patrones Identificados**:
- **Soft Validation**: Campos opcionales para flexibilidad
- **Audit Trail**: Timestamp de creación para auditoría
- **Simplicity**: Estructura simple para facilitar CRUD

### 2. Tabla `casos`

```sql
CREATE TABLE casos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    numero_expediente TEXT,
    anio_caratula TEXT,
    caratula TEXT NOT NULL,
    juzgado TEXT,
    jurisdiccion TEXT,
    etapa_procesal TEXT,
    notas TEXT,
    ruta_carpeta TEXT,
    inactivity_threshold_days INTEGER DEFAULT 30,
    inactivity_enabled INTEGER DEFAULT 1,
    created_at INTEGER,
    last_activity_timestamp INTEGER,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
);
```

**Características Avanzadas**:
- **Relación 1:N**: Un cliente puede tener múltiples casos
- **CASCADE DELETE**: Integridad referencial automática
- **Activity Tracking**: Sistema de monitoreo de actividad
- **Flexibility**: Número de expediente opcional (casos en desarrollo)
- **Business Logic**: Sistema de inactividad configurable

**Patrones de Negocio**:
- **Workflow Support**: Etapa procesal para seguimiento
- **Document Management**: Ruta de carpeta integrada
- **Time-based Rules**: Umbral de inactividad personalizable
- **Audit Compliance**: Timestamps múltiples

### 3. Tabla `audiencias`

```sql
CREATE TABLE audiencias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    caso_id INTEGER NOT NULL,
    fecha TEXT NOT NULL, -- YYYY-MM-DD
    hora TEXT,           -- HH:MM (opcional)
    descripcion TEXT NOT NULL,
    link TEXT,
    recordatorio_activo INTEGER DEFAULT 0,
    recordatorio_minutos INTEGER DEFAULT 15,
    created_at INTEGER,
    FOREIGN KEY (caso_id) REFERENCES casos(id) ON DELETE CASCADE
);
```

**Diseño Temporal**:
- **Fecha Separada**: Permite audiencias sin hora específica
- **Formato Estándar**: YYYY-MM-DD para sorting automático
- **Time Zones**: Implicitly local time (single-user app)

**Sistema de Recordatorios**:
- **Flexible Timing**: Minutos configurables antes del evento
- **On/Off Switch**: Recordatorio activable por audiencia
- **Integration Ready**: Preparado para notificaciones push

### 4. Tabla `actividades_caso`

```sql
CREATE TABLE actividades_caso (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    caso_id INTEGER NOT NULL,
    fecha_hora TEXT NOT NULL, -- YYYY-MM-DD HH:MM:SS
    tipo_actividad TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    creado_por TEXT,
    referencia_documento TEXT,
    FOREIGN KEY (caso_id) REFERENCES casos(id) ON DELETE CASCADE
);
```

**Sistema de Auditoría**:
- **Timestamp Preciso**: Segundos para ordenamiento exacto
- **User Tracking**: Preparado para multi-usuario
- **Document Links**: Referencias opcionales a archivos
- **Activity Types**: Categorización flexible

**Índice Optimizado**:
```sql
CREATE INDEX idx_actividades_caso_id_fecha 
ON actividades_caso (caso_id, fecha_hora DESC);
```

### 5. Tabla `partes_intervinientes`

```sql
CREATE TABLE partes_intervinientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    caso_id INTEGER NOT NULL,
    nombre TEXT NOT NULL,
    tipo TEXT, -- 'testigo', 'abogado', 'perito', etc.
    direccion TEXT,
    contacto TEXT,
    created_at INTEGER,
    FOREIGN KEY (caso_id) REFERENCES casos(id) ON DELETE CASCADE
);
```

**Flexibilidad de Roles**:
- **Tipo Abierto**: Sin enum para permitir roles customizados
- **Contact Info**: Dirección y contacto unificados
- **Extensible**: Estructura preparada para campos adicionales

---

## Índices de Optimización

### Índices Implementados

```sql
-- Búsquedas por fecha en audiencias
CREATE INDEX idx_audiencias_fecha ON audiencias (fecha);

-- Búsquedas por caso en audiencias
CREATE INDEX idx_audiencias_caso_id ON audiencias (caso_id);

-- Filtrado de recordatorios activos
CREATE INDEX idx_audiencias_recordatorio ON audiencias (recordatorio_activo);

-- Actividades por caso ordenadas por fecha
CREATE INDEX idx_actividades_caso_id_fecha 
ON actividades_caso (caso_id, fecha_hora DESC);
```

### Análisis de Performance

**Consultas Optimizadas**:
1. **Lista de audiencias por fecha**: O(log n) con índice
2. **Actividades de caso**: O(log n) con índice compuesto
3. **Recordatorios pendientes**: O(log n) con índice filtrado
4. **Cascading deletes**: Automático con FK constraints

**Consultas Problemáticas** (futuras optimizaciones):
1. **Full-text search**: Requiere FTS extension
2. **Cross-table searches**: Necesitará índices adicionales
3. **Date range queries**: Beneficiaría de índices compuestos

---

## Patrones de Acceso a Datos

### 1. Connection Pattern

```python
def connect_db():
    conn = sqlite3.connect(DATABASE_FILE, 
                          detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    conn.execute('PRAGMA foreign_keys = ON;')
    conn.row_factory = sqlite3.Row
    return conn
```

**Beneficios**:
- **Type Safety**: Detección automática de tipos
- **Integrity**: Foreign keys habilitadas
- **Convenience**: Row factory para acceso por nombre

### 2. CRUD Pattern

```python
def add_entity(params...):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error: {e}")
            conn.rollback()
            return None
        finally:
            close_db(conn)
```

**Características**:
- **Error Handling**: Try/catch con rollback
- **Resource Management**: Finally block para cleanup
- **Return Values**: ID para inserts, boolean para updates
- **Logging**: Consistent error reporting

### 3. Query Enhancement Pattern

```python
def get_audiencia_by_id(audiencia_id):
    # JOIN múltiple para información contextual
    cursor.execute('''
        SELECT a.*, ca.caratula as caso_caratula, cl.nombre as cliente_nombre
        FROM audiencias a
        JOIN casos ca ON a.caso_id = ca.id
        JOIN clientes cl ON ca.cliente_id = cl.id
        WHERE a.id = ?
    ''', (audiencia_id,))
```

**Ventajas**:
- **Rich Data**: Información contextual en una consulta
- **Performance**: Menos round-trips a la BD
- **Usability**: Datos listos para UI sin post-processing

---

## Integridad y Constraints

### Foreign Key Constraints

```sql
-- Todas las tablas dependientes tienen CASCADE DELETE
FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
FOREIGN KEY (caso_id) REFERENCES casos(id) ON DELETE CASCADE
```

**Beneficios**:
- **Data Integrity**: No hay registros huérfanos
- **Simplified Logic**: No necesidad de cleanup manual
- **Atomicity**: Operaciones consistentes

### Business Rules en BD

1. **Casos requieren cliente**: NOT NULL constraint
2. **Actividades requieren caso**: NOT NULL constraint  
3. **Timestamps automáticos**: Defaults y triggers implícitos
4. **Inactividad configurable**: Defaults inteligentes

---

## Consideraciones de Migración

### Schema Evolution

**Archivos analizados sugieren**:
- Schema estable en main branch
- Modificaciones en feature branches
- Necesidad de migration scripts futuros

**Estrategias sugeridas**:
1. **Version tracking**: Tabla de schema versions
2. **Migration scripts**: Para updates automáticos
3. **Backup strategy**: Antes de cada migración
4. **Rollback capability**: Para recovery

### Compatibility

**SQLite Advantages**:
- **File-based**: Fácil backup y migración
- **Cross-platform**: Compatible multi-OS
- **Embedded**: No servidor externo requerido
- **Mature**: Estable y probado

**Limitations**:
- **Concurrency**: Limited concurrent writes
- **Size limits**: Prácticamente ilimitado para uso típico
- **No user management**: Single-user design

---

## Recomendaciones de Mejora

### 1. Índices Adicionales

```sql
-- Para búsqueda global futura
CREATE INDEX idx_casos_caratula ON casos (caratula);
CREATE INDEX idx_clientes_nombre ON clientes (nombre);

-- Para reporting y analytics
CREATE INDEX idx_casos_created_at ON casos (created_at);
CREATE INDEX idx_audiencias_fecha_recordatorio 
ON audiencias (fecha, recordatorio_activo);
```

### 2. Validaciones Adicionales

```sql
-- Check constraints para business rules
ALTER TABLE audiencias ADD CONSTRAINT 
chk_fecha_valida CHECK (fecha >= date('2020-01-01'));

ALTER TABLE casos ADD CONSTRAINT 
chk_threshold_valido CHECK (inactivity_threshold_days > 0);
```

### 3. Funciones Stored (SQLite UDF)

```python
# Custom functions para operaciones frecuentes
def calculate_case_age(created_at):
    return (time.time() - created_at) / (24 * 3600)

conn.create_function("case_age", 1, calculate_case_age)
```

### 4. Full-Text Search

```sql
-- Para búsqueda global futura
CREATE VIRTUAL TABLE casos_fts USING fts5(
    caratula, notas, numero_expediente,
    content='casos'
);
```

---

## Conclusiones Técnicas

### Fortalezas del Diseño

1. **Normalización Apropiada**: 3NF sin over-normalization
2. **Integridad Referencial**: FK constraints bien implementadas
3. **Índices Inteligentes**: Para consultas frecuentes
4. **Flexibilidad**: Campos opcionales donde apropiado
5. **Auditabilidad**: Timestamps y tracking de actividad
6. **Escalabilidad**: Preparado para crecimiento orgánico

### Áreas de Mejora

1. **Full-Text Search**: Para búsqueda global
2. **Schema Versioning**: Para migraciones futuras
3. **Business Rules**: Más constraints a nivel BD
4. **Performance Monitoring**: Herramientas de profiling
5. **Backup Strategy**: Automatización de respaldos

### Veredicto Técnico

**✅ Diseño Sólido**: La arquitectura de base de datos es robusta, bien pensada y apropiada para el dominio legal. Sigue buenas prácticas de diseño relacional y está optimizada para los patrones de acceso típicos de un CRM.

**🔧 Mejoras Incrementales**: Las mejoras sugeridas son evolutivas, no revolucionarias, lo que indica un diseño base sólido que puede crecer orgánicamente.

**📈 Preparado para Escalar**: La estructura actual puede soportar las funcionalidades pendientes sin cambios arquitectónicos mayores.
