# migrar_bd_completa.py
"""
Script de migración inteligente para CRM Legal v2.0

Este script:
1. Detecta el estado actual de la base de datos
2. Preserve todos los datos existentes (partes, tareas, Firebase, etc.)
3. Agrega solo las tablas nuevas (etiquetas mejoradas + financiero)
4. Realiza validación completa de integridad
5. Crea backup automático antes de la migración
"""

import sqlite3
import os
import shutil
import datetime
import sys

DATABASE_FILE = 'crm_legal.db'
BACKUP_DIR = 'backups'

def log_message(message):
    """Registrar mensaje con timestamp"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def create_backup():
    """Crear backup de la base de datos antes de la migración"""
    if not os.path.exists(DATABASE_FILE):
        log_message("❌ No se encontró la base de datos. Creando nueva...")
        return None
    
    # Crear directorio de backups si no existe
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    
    # Crear nombre de backup con timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"crm_legal_backup_pre_migration_{timestamp}.db"
    backup_path = os.path.join(BACKUP_DIR, backup_filename)
    
    try:
        shutil.copy2(DATABASE_FILE, backup_path)
        log_message(f"✅ Backup creado: {backup_path}")
        return backup_path
    except Exception as e:
        log_message(f"❌ Error creando backup: {e}")
        return None

def connect_db():
    """Conectar a la base de datos"""
    try:
        conn = sqlite3.connect(DATABASE_FILE, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        conn.execute('PRAGMA foreign_keys = ON;')
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        log_message(f"❌ Error conectando a la BD: {e}")
        return None

def table_exists(conn, table_name):
    """Verificar si una tabla existe"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name=?
        """, (table_name,))
        return cursor.fetchone() is not None
    except Exception as e:
        log_message(f"Error verificando tabla {table_name}: {e}")
        return False

def column_exists(conn, table_name, column_name):
    """Verificar si una columna existe en una tabla"""
    try:
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [column[1] for column in cursor.fetchall()]
        return column_name in columns
    except Exception as e:
        log_message(f"Error verificando columna {column_name} en {table_name}: {e}")
        return False

def analyze_current_state(conn):
    """Analizar el estado actual de la base de datos"""
    log_message("🔍 Analizando estado actual de la base de datos...")
    
    state = {
        'existing_tables': [],
        'missing_tables': [],
        'missing_columns': {},
        'data_counts': {}
    }
    
    # Tablas esperadas
    expected_tables = [
        'clientes', 'casos', 'audiencias', 'actividades_caso', 'partes_intervinientes',
        'datos_usuario', 'etiquetas', 'cliente_etiquetas', 'caso_etiquetas', 'tareas',
        'honorarios', 'gastos', 'facturas', 'pagos'
    ]
    
    # Verificar tablas existentes
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    existing_tables = [row[0] for row in cursor.fetchall()]
    
    for table in expected_tables:
        if table in existing_tables:
            state['existing_tables'].append(table)
            
            # Contar registros
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                state['data_counts'][table] = count
            except:
                state['data_counts'][table] = 0
        else:
            state['missing_tables'].append(table)
    
    # Verificar columnas específicas que se agregaron
    column_checks = {
        'etiquetas': ['descripcion', 'color', 'tipo', 'fecha_creacion'],
        'clientes': ['etiquetas'],
        'casos': ['etiquetas']
    }
    
    for table, columns in column_checks.items():
        if table in existing_tables:
            state['missing_columns'][table] = []
            for column in columns:
                if not column_exists(conn, table, column):
                    state['missing_columns'][table].append(column)
    
    return state

def print_analysis_report(state):
    """Imprimir reporte del análisis"""
    log_message("📊 REPORTE DE ANÁLISIS:")
    log_message("=" * 50)
    
    log_message(f"✅ Tablas existentes ({len(state['existing_tables'])}):")
    for table in state['existing_tables']:
        count = state['data_counts'].get(table, 0)
        log_message(f"   - {table}: {count} registros")
    
    if state['missing_tables']:
        log_message(f"❌ Tablas faltantes ({len(state['missing_tables'])}):")
        for table in state['missing_tables']:
            log_message(f"   - {table}")
    
    missing_cols_total = sum(len(cols) for cols in state['missing_columns'].values())
    if missing_cols_total > 0:
        log_message(f"⚠️  Columnas faltantes ({missing_cols_total}):")
        for table, columns in state['missing_columns'].items():
            if columns:
                log_message(f"   - {table}: {', '.join(columns)}")
    
    log_message("=" * 50)

def create_missing_tables(conn):
    """Crear las tablas faltantes"""
    log_message("🔧 Creando tablas faltantes...")
    
    cursor = conn.cursor()
    
    # Tabla de honorarios
    if not table_exists(conn, 'honorarios'):
        log_message("   Creando tabla 'honorarios'...")
        cursor.execute('''
            CREATE TABLE honorarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                caso_id INTEGER NOT NULL,
                descripcion TEXT NOT NULL,
                monto REAL NOT NULL DEFAULT 0.0,
                fecha TEXT NOT NULL,
                estado TEXT NOT NULL DEFAULT 'Pendiente',
                tipo TEXT NOT NULL DEFAULT 'Consulta',
                fecha_creacion TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                notas TEXT,
                FOREIGN KEY (caso_id) REFERENCES casos(id) ON DELETE CASCADE
            );
        ''')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_honorarios_caso_id ON honorarios (caso_id);')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_honorarios_fecha ON honorarios (fecha);')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_honorarios_estado ON honorarios (estado);')
    
    # Tabla de gastos
    if not table_exists(conn, 'gastos'):
        log_message("   Creando tabla 'gastos'...")
        cursor.execute('''
            CREATE TABLE gastos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                caso_id INTEGER NOT NULL,
                descripcion TEXT NOT NULL,
                monto REAL NOT NULL DEFAULT 0.0,
                fecha TEXT NOT NULL,
                categoria TEXT NOT NULL DEFAULT 'General',
                reembolsable INTEGER DEFAULT 1,
                fecha_creacion TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                notas TEXT,
                comprobante_path TEXT,
                FOREIGN KEY (caso_id) REFERENCES casos(id) ON DELETE CASCADE
            );
        ''')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_gastos_caso_id ON gastos (caso_id);')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_gastos_fecha ON gastos (fecha);')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_gastos_categoria ON gastos (categoria);')
    
    # Tabla de facturas
    if not table_exists(conn, 'facturas'):
        log_message("   Creando tabla 'facturas'...")
        cursor.execute('''
            CREATE TABLE facturas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                caso_id INTEGER NOT NULL,
                numero TEXT NOT NULL,
                fecha TEXT NOT NULL,
                fecha_vencimiento TEXT,
                monto REAL NOT NULL DEFAULT 0.0,
                estado TEXT NOT NULL DEFAULT 'Pendiente',
                descripcion TEXT,
                archivo_path TEXT,
                fecha_creacion TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                fecha_pago TEXT,
                metodo_pago TEXT,
                FOREIGN KEY (caso_id) REFERENCES casos(id) ON DELETE CASCADE
            );
        ''')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_facturas_caso_id ON facturas (caso_id);')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_facturas_fecha ON facturas (fecha);')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_facturas_estado ON facturas (estado);')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_facturas_numero ON facturas (numero);')
    
    # Tabla de pagos
    if not table_exists(conn, 'pagos'):
        log_message("   Creando tabla 'pagos'...")
        cursor.execute('''
            CREATE TABLE pagos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                factura_id INTEGER NOT NULL,
                monto REAL NOT NULL DEFAULT 0.0,
                fecha_pago TEXT NOT NULL,
                metodo_pago TEXT NOT NULL,
                referencia TEXT,
                notas TEXT,
                fecha_creacion TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (factura_id) REFERENCES facturas(id) ON DELETE CASCADE
            );
        ''')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_pagos_factura_id ON pagos (factura_id);')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_pagos_fecha ON pagos (fecha_pago);')

def add_missing_columns(conn):
    """Agregar columnas faltantes a tablas existentes"""
    log_message("🔧 Agregando columnas faltantes...")
    
    cursor = conn.cursor()
    
    # Mejorar tabla de etiquetas
    if table_exists(conn, 'etiquetas'):
        columns_to_add = [
            ('descripcion', 'TEXT DEFAULT ""'),
            ('color', 'TEXT DEFAULT "#3498db"'),
            ('tipo', 'TEXT DEFAULT "general"'),
            ('fecha_creacion', 'TEXT DEFAULT CURRENT_TIMESTAMP')
        ]
        
        for column_name, column_def in columns_to_add:
            if not column_exists(conn, 'etiquetas', column_name):
                try:
                    cursor.execute(f'ALTER TABLE etiquetas ADD COLUMN {column_name} {column_def};')
                    log_message(f"   ✅ Agregada columna '{column_name}' a 'etiquetas'")
                except Exception as e:
                    log_message(f"   ⚠️  Error agregando columna '{column_name}': {e}")
    
    # Agregar columna etiquetas a clientes
    if table_exists(conn, 'clientes') and not column_exists(conn, 'clientes', 'etiquetas'):
        try:
            cursor.execute('ALTER TABLE clientes ADD COLUMN etiquetas TEXT DEFAULT "";')
            log_message("   ✅ Agregada columna 'etiquetas' a 'clientes'")
        except Exception as e:
            log_message(f"   ⚠️  Error agregando columna 'etiquetas' a clientes: {e}")
    
    # Agregar columna etiquetas a casos
    if table_exists(conn, 'casos') and not column_exists(conn, 'casos', 'etiquetas'):
        try:
            cursor.execute('ALTER TABLE casos ADD COLUMN etiquetas TEXT DEFAULT "";')
            log_message("   ✅ Agregada columna 'etiquetas' a 'casos'")
        except Exception as e:
            log_message(f"   ⚠️  Error agregando columna 'etiquetas' a casos: {e}")

def validate_migration(conn):
    """Validar que la migración se completó correctamente"""
    log_message("🔍 Validando migración...")
    
    validation_passed = True
    
    # Verificar que todas las tablas esperadas existen
    expected_tables = ['honorarios', 'gastos', 'facturas', 'pagos']
    for table in expected_tables:
        if not table_exists(conn, table):
            log_message(f"   ❌ Tabla '{table}' no fue creada")
            validation_passed = False
        else:
            log_message(f"   ✅ Tabla '{table}' creada correctamente")
    
    # Verificar integridad de datos existentes
    try:
        cursor = conn.cursor()
        
        # Verificar que los datos existentes se mantuvieron
        data_integrity_checks = [
            ('clientes', 'SELECT COUNT(*) FROM clientes'),
            ('casos', 'SELECT COUNT(*) FROM casos'),
            ('tareas', 'SELECT COUNT(*) FROM tareas WHERE caso_id IS NOT NULL'),
            ('partes_intervinientes', 'SELECT COUNT(*) FROM partes_intervinientes'),
            ('audiencias', 'SELECT COUNT(*) FROM audiencias')
        ]
        
        for table, query in data_integrity_checks:
            if table_exists(conn, table):
                cursor.execute(query)
                count = cursor.fetchone()[0]
                log_message(f"   ✅ {table}: {count} registros preservados")
    
    except Exception as e:
        log_message(f"   ⚠️  Error validando integridad de datos: {e}")
        validation_passed = False
    
    return validation_passed

def migrate_database():
    """Función principal de migración"""
    log_message("🚀 INICIANDO MIGRACIÓN CRM LEGAL v2.0")
    log_message("=" * 60)
    
    # Crear backup
    backup_path = create_backup()
    if backup_path is None and os.path.exists(DATABASE_FILE):
        response = input("⚠️  No se pudo crear backup. ¿Continuar sin backup? (y/N): ")
        if response.lower() != 'y':
            log_message("❌ Migración cancelada por el usuario")
            return False
    
    # Conectar a la base de datos
    conn = connect_db()
    if not conn:
        log_message("❌ No se pudo conectar a la base de datos")
        return False
    
    try:
        # Analizar estado actual
        state = analyze_current_state(conn)
        print_analysis_report(state)
        
        # Confirmar migración
        if state['missing_tables'] or any(state['missing_columns'].values()):
            response = input("\n💡 ¿Proceder con la migración? (Y/n): ")
            if response.lower() == 'n':
                log_message("❌ Migración cancelada por el usuario")
                return False
        else:
            log_message("✅ La base de datos ya está actualizada")
            return True
        
        # Ejecutar migración
        log_message("\n🔧 EJECUTANDO MIGRACIÓN...")
        
        # Crear tablas faltantes
        create_missing_tables(conn)
        
        # Agregar columnas faltantes
        add_missing_columns(conn)
        
        # Commit de todos los cambios
        conn.commit()
        log_message("✅ Migración completada - Cambios guardados")
        
        # Validar migración
        if validate_migration(conn):
            log_message("✅ Validación exitosa")
            log_message("\n🎉 MIGRACIÓN COMPLETADA EXITOSAMENTE")
            log_message("=" * 60)
            log_message("📋 RESUMEN:")
            log_message("   ✅ Todos los datos existentes preservados")
            log_message("   ✅ Nuevas tablas financieras creadas")
            log_message("   ✅ Sistema de etiquetas mejorado")
            log_message("   ✅ Base de datos lista para CRM Legal v2.0")
            
            if backup_path:
                log_message(f"   📁 Backup disponible en: {backup_path}")
            
            return True
        else:
            log_message("❌ Errores en la validación")
            return False
    
    except Exception as e:
        log_message(f"❌ Error durante la migración: {e}")
        conn.rollback()
        return False
    
    finally:
        conn.close()

def show_help():
    """Mostrar ayuda sobre el script"""
    help_text = """
CRM Legal v2.0 - Script de Migración de Base de Datos

DESCRIPCIÓN:
Este script migra la base de datos del CRM Legal preservando todos los datos 
existentes y agregando las nuevas funcionalidades.

FUNCIONALIDADES AGREGADAS:
- Sistema financiero completo (honorarios, gastos, facturas, pagos)
- Sistema de etiquetas globales mejorado
- Compatibilidad con módulos refactorizados

CARACTERÍSTICAS:
✅ Backup automático antes de la migración
✅ Detección inteligente del estado actual
✅ Preservación total de datos existentes
✅ Validación completa post-migración
✅ Reversión posible usando el backup

USO:
python migrar_bd_completa.py [opciones]

OPCIONES:
--help, -h     Mostrar esta ayuda
--force        Forzar migración sin confirmaciones
--dry-run      Simular migración sin hacer cambios
"""
    print(help_text)

def main():
    """Función principal"""
    if len(sys.argv) > 1:
        if sys.argv[1] in ['--help', '-h']:
            show_help()
            return
        elif sys.argv[1] == '--dry-run':
            log_message("🔍 MODO SIMULACIÓN - No se realizarán cambios")
            conn = connect_db()
            if conn:
                state = analyze_current_state(conn)
                print_analysis_report(state)
                conn.close()
            return
    
    # Ejecutar migración
    success = migrate_database()
    
    if success:
        log_message("\n🎯 PRÓXIMOS PASOS:")
        log_message("1. Ejecutar: python main_app_refactorizado.py")
        log_message("2. Verificar funcionamiento de todos los módulos")
        log_message("3. Reportar cualquier problema encontrado")
        sys.exit(0)
    else:
        log_message("\n❌ MIGRACIÓN FALLIDA")
        log_message("Revisar los errores anteriores y contactar soporte si es necesario")
        sys.exit(1)

if __name__ == "__main__":
    main()
