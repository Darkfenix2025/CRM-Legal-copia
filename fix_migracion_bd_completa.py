#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CORRECCIÓN COMPLETA: MIGRACIÓN DE BASE DE DATOS
==============================================

Problema: Cuando se migra la base de datos anterior, en la nueva tabla "etiquetas"
no se crea la columna fecha_creacion, causando errores.

Solución: Script completo de migración que asegura todas las columnas necesarias.
"""

import sqlite3
import os
from datetime import datetime

def verificar_estado_bd():
    """Verifica el estado actual de la base de datos"""
    print("🔍 VERIFICANDO ESTADO ACTUAL DE LA BASE DE DATOS")
    print("=" * 55)
    
    if not os.path.exists('crm_legal.db'):
        print("❌ Base de datos crm_legal.db no existe")
        return False
    
    try:
        conn = sqlite3.connect('crm_legal.db')
        cursor = conn.cursor()
        
        # Verificar tabla etiquetas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='etiquetas'")
        if cursor.fetchone():
            print("✅ Tabla 'etiquetas' existe")
            
            # Verificar estructura de la tabla
            cursor.execute("PRAGMA table_info(etiquetas)")
            columnas = cursor.fetchall()
            
            print(f"📋 Estructura actual de tabla etiquetas:")
            for col in columnas:
                print(f"   • {col[1]} ({col[2]}) - {col[5] if col[5] else 'NULL'}")
            
            # Verificar columnas específicas
            nombres_columnas = [col[1] for col in columnas]
            columnas_requeridas = ['fecha_creacion', 'descripcion', 'color', 'categoria', 'activa']
            
            print(f"\n📊 Estado de columnas requeridas:")
            for col_req in columnas_requeridas:
                estado = "✅ EXISTE" if col_req in nombres_columnas else "❌ FALTA"
                print(f"   • {col_req}: {estado}")
            
            return nombres_columnas
        else:
            print("❌ Tabla 'etiquetas' NO existe")
            return None
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error verificando BD: {e}")
        return None

def migrar_tabla_etiquetas_completa():
    """Migra la tabla etiquetas con todas las columnas necesarias"""
    print("\n🔧 MIGRANDO TABLA ETIQUETAS COMPLETA")
    print("=" * 45)
    
    try:
        conn = sqlite3.connect('crm_legal.db')
        cursor = conn.cursor()
        
        # Crear backup de datos existentes
        cursor.execute("SELECT * FROM etiquetas")
        datos_existentes = cursor.fetchall()
        print(f"💾 Respaldando {len(datos_existentes)} registros existentes")
        
        # Obtener estructura actual
        cursor.execute("PRAGMA table_info(etiquetas)")
        estructura_actual = cursor.fetchall()
        nombres_columnas_actuales = [col[1] for col in estructura_actual]
        
        # Crear nueva tabla con estructura completa
        cursor.execute("DROP TABLE IF EXISTS etiquetas_temp")
        cursor.execute("""
            CREATE TABLE etiquetas_temp (
                id_etiqueta INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_etiqueta TEXT NOT NULL UNIQUE COLLATE NOCASE,
                descripcion TEXT DEFAULT '',
                color TEXT DEFAULT '#3498db',
                categoria TEXT DEFAULT 'general',
                activa INTEGER DEFAULT 1,
                fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP,
                creado_por TEXT DEFAULT 'Sistema'
            )
        """)
        print("✅ Tabla temporal con estructura completa creada")
        
        # Migrar datos existentes
        if datos_existentes:
            for registro in datos_existentes:
                # Mapear datos según estructura actual
                id_etiqueta = registro[0]
                nombre_etiqueta = registro[1] if len(registro) > 1 else f"Etiqueta_{id_etiqueta}"
                
                # Obtener otros campos si existen, sino usar defaults
                descripcion = ''
                color = '#3498db'
                categoria = 'general'
                activa = 1
                fecha_creacion = datetime.now().isoformat()
                creado_por = 'Migración'
                
                # Si hay más columnas en el registro original, intentar mapearlas
                if len(registro) > 2:
                    for i, nombre_col in enumerate(nombres_columnas_actuales[2:], 2):
                        if i < len(registro):
                            if nombre_col == 'descripcion':
                                descripcion = registro[i] or ''
                            elif nombre_col == 'color':
                                color = registro[i] or '#3498db'
                            elif nombre_col == 'categoria':
                                categoria = registro[i] or 'general'
                            elif nombre_col == 'activa':
                                activa = registro[i] if registro[i] is not None else 1
                            elif nombre_col == 'fecha_creacion':
                                fecha_creacion = registro[i] or datetime.now().isoformat()
                
                # Insertar en tabla temporal
                cursor.execute("""
                    INSERT INTO etiquetas_temp 
                    (id_etiqueta, nombre_etiqueta, descripcion, color, categoria, activa, fecha_creacion, creado_por)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (id_etiqueta, nombre_etiqueta, descripcion, color, categoria, activa, fecha_creacion, creado_por))
            
            print(f"✅ {len(datos_existentes)} registros migrados")
        
        # Reemplazar tabla original
        cursor.execute("DROP TABLE etiquetas")
        cursor.execute("ALTER TABLE etiquetas_temp RENAME TO etiquetas")
        print("✅ Tabla etiquetas reemplazada con estructura completa")
        
        # Crear índices
        indices = [
            "CREATE INDEX IF NOT EXISTS idx_etiquetas_nombre ON etiquetas(nombre_etiqueta)",
            "CREATE INDEX IF NOT EXISTS idx_etiquetas_categoria ON etiquetas(categoria)",
            "CREATE INDEX IF NOT EXISTS idx_etiquetas_activa ON etiquetas(activa)"
        ]
        
        for indice in indices:
            cursor.execute(indice)
        print("✅ Índices creados")
        
        conn.commit()
        conn.close()
        
        print("✅ Migración de tabla etiquetas completada")
        return True
        
    except Exception as e:
        print(f"❌ Error en migración: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False

def agregar_etiquetas_predefinidas():
    """Agrega etiquetas predefinidas si la tabla está vacía"""
    print("\n📋 AGREGANDO ETIQUETAS PREDEFINIDAS")
    print("=" * 40)
    
    try:
        conn = sqlite3.connect('crm_legal.db')
        cursor = conn.cursor()
        
        # Verificar si hay etiquetas
        cursor.execute("SELECT COUNT(*) FROM etiquetas")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("📝 Tabla etiquetas vacía, agregando etiquetas predefinidas...")
            
            etiquetas_predefinidas = [
                ('Urgente', 'Casos que requieren atención inmediata', '#e74c3c', 'Prioridad'),
                ('Alta', 'Casos de alta prioridad', '#f39c12', 'Prioridad'),
                ('Media', 'Casos de prioridad media', '#f1c40f', 'Prioridad'),
                ('Baja', 'Casos de baja prioridad', '#2ecc71', 'Prioridad'),
                ('En Proceso', 'Casos actualmente en tramitación', '#3498db', 'Estado'),
                ('Finalizado', 'Casos terminados exitosamente', '#27ae60', 'Estado'),
                ('Suspendido', 'Casos temporalmente suspendidos', '#95a5a6', 'Estado'),
                ('Civil', 'Casos de derecho civil', '#34495e', 'Tipo'),
                ('Penal', 'Casos de derecho penal', '#c0392b', 'Tipo'),
                ('Laboral', 'Casos de derecho laboral', '#16a085', 'Tipo'),
                ('Familia', 'Casos de derecho de familia', '#e67e22', 'Tipo'),
                ('VIP', 'Cliente de alta importancia', '#f39c12', 'Cliente'),
                ('Empresarial', 'Cliente empresarial', '#3498db', 'Cliente'),
                ('Particular', 'Cliente particular', '#95a5a6', 'Cliente')
            ]
            
            for nombre, desc, color, categoria in etiquetas_predefinidas:
                cursor.execute("""
                    INSERT INTO etiquetas 
                    (nombre_etiqueta, descripcion, color, categoria, activa, fecha_creacion, creado_por)
                    VALUES (?, ?, ?, ?, 1, ?, 'Sistema')
                """, (nombre, desc, color, categoria, datetime.now().isoformat()))
            
            print(f"✅ {len(etiquetas_predefinidas)} etiquetas predefinidas agregadas")
        else:
            print(f"✅ Tabla etiquetas ya tiene {count} registros")
        
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error agregando etiquetas predefinidas: {e}")
        return False

def crear_funcion_segura_etiquetas():
    """Crea función segura para obtener etiquetas sin errores"""
    print("\n🛠️  CREANDO FUNCIÓN SEGURA PARA ETIQUETAS")
    print("=" * 50)
    
    funcion_segura = '''

# === FUNCIÓN SEGURA PARA ETIQUETAS - MIGRACIÓN COMPLETA ===

def get_all_etiquetas_migradas():
    """
    Obtiene todas las etiquetas usando la estructura migrada completa.
    Esta función maneja tanto la estructura antigua como la nueva.
    """
    conn = connect_db()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        
        # Verificar qué columnas existen
        cursor.execute("PRAGMA table_info(etiquetas)")
        columnas_info = cursor.fetchall()
        columnas_existentes = [col[1] for col in columnas_info]
        
        # Construir query según columnas disponibles
        if 'fecha_creacion' in columnas_existentes:
            # Estructura completa
            cursor.execute("""
                SELECT 
                    id_etiqueta, nombre_etiqueta, descripcion, color, 
                    categoria, activa, fecha_creacion, creado_por
                FROM etiquetas 
                WHERE activa = 1
                ORDER BY categoria, nombre_etiqueta
            """)
        else:
            # Estructura básica
            cursor.execute("""
                SELECT 
                    id_etiqueta, nombre_etiqueta, 
                    '' as descripcion, '#3498db' as color,
                    'general' as categoria, 1 as activa,
                    '' as fecha_creacion, 'Sistema' as creado_por
                FROM etiquetas 
                ORDER BY nombre_etiqueta
            """)
        
        resultados = []
        for row in cursor.fetchall():
            resultados.append({
                'id': row[0],
                'nombre': row[1],
                'descripcion': row[2] or '',
                'color': row[3] or '#3498db',
                'categoria': row[4] or 'general',
                'activa': row[5] if row[5] is not None else 1,
                'fecha_creacion': row[6] or '',
                'creado_por': row[7] or 'Sistema'
            })
        
        return resultados
        
    except Exception as e:
        print(f"Error obteniendo etiquetas migradas: {e}")
        return []
    finally:
        close_db(conn)

# === FIN FUNCIÓN SEGURA ETIQUETAS ===
'''
    
    try:
        # Agregar función a crm_database.py
        if os.path.exists('crm_database.py'):
            with open('crm_database.py', 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            if 'get_all_etiquetas_migradas' not in contenido:
                with open('crm_database.py', 'a', encoding='utf-8') as f:
                    f.write(funcion_segura)
                print("✅ Función segura agregada a crm_database.py")
            else:
                print("✅ Función segura ya existe")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando función segura: {e}")
        return False

def verificar_migracion_exitosa():
    """Verifica que la migración se completó exitosamente"""
    print("\n✅ VERIFICANDO MIGRACIÓN COMPLETADA")
    print("=" * 40)
    
    try:
        conn = sqlite3.connect('crm_legal.db')
        cursor = conn.cursor()
        
        # Verificar estructura final
        cursor.execute("PRAGMA table_info(etiquetas)")
        columnas_finales = cursor.fetchall()
        
        columnas_requeridas = ['id_etiqueta', 'nombre_etiqueta', 'descripcion', 
                              'color', 'categoria', 'activa', 'fecha_creacion']
        
        nombres_finales = [col[1] for col in columnas_finales]
        
        print("📋 Verificación final:")
        todas_ok = True
        for col_req in columnas_requeridas:
            if col_req in nombres_finales:
                print(f"   ✅ {col_req}: OK")
            else:
                print(f"   ❌ {col_req}: FALTA")
                todas_ok = False
        
        # Verificar datos
        cursor.execute("SELECT COUNT(*) FROM etiquetas")
        total_etiquetas = cursor.fetchone()[0]
        print(f"\n📊 Total de etiquetas: {total_etiquetas}")
        
        # Probar consulta con fecha_creacion
        try:
            cursor.execute("SELECT nombre_etiqueta, fecha_creacion FROM etiquetas LIMIT 1")
            test_result = cursor.fetchone()
            print("✅ Consulta con fecha_creacion: OK")
        except Exception as e:
            print(f"❌ Error en consulta fecha_creacion: {e}")
            todas_ok = False
        
        conn.close()
        return todas_ok
        
    except Exception as e:
        print(f"❌ Error en verificación: {e}")
        return False

def main():
    """Función principal de migración completa"""
    print("🗄️  MIGRACIÓN COMPLETA DE BASE DE DATOS - TABLA ETIQUETAS")
    print("=" * 70)
    print("Solucionando: columna fecha_creacion no se crea en migración\n")
    
    # Crear backup completo
    if os.path.exists('crm_legal.db'):
        backup_name = f"crm_legal_backup_migracion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        import shutil
        shutil.copy2('crm_legal.db', backup_name)
        print(f"💾 Backup completo creado: {backup_name}")
    
    exito_total = True
    
    # Paso 1: Verificar estado actual
    estado_actual = verificar_estado_bd()
    if estado_actual is None:
        print("❌ No se puede continuar sin tabla etiquetas")
        return
    
    # Paso 2: Migrar tabla si es necesario
    if 'fecha_creacion' not in estado_actual:
        print("\n🔄 Iniciando migración de tabla etiquetas...")
        if not migrar_tabla_etiquetas_completa():
            exito_total = False
    else:
        print("\n✅ Tabla etiquetas ya tiene estructura completa")
    
    # Paso 3: Agregar etiquetas predefinidas
    if not agregar_etiquetas_predefinidas():
        exito_total = False
    
    # Paso 4: Crear función segura
    if not crear_funcion_segura_etiquetas():
        exito_total = False
    
    # Paso 5: Verificación final
    if not verificar_migracion_exitosa():
        exito_total = False
    
    # Resultado final
    if exito_total:
        print("\n🎉 MIGRACIÓN COMPLETA EXITOSA")
        print("=" * 40)
        print("✅ PROBLEMAS SOLUCIONADOS:")
        print("   • Columna fecha_creacion creada")
        print("   • Estructura completa de etiquetas")
        print("   • Datos existentes preservados")
        print("   • Etiquetas predefinidas agregadas")
        print("   • Función segura disponible")
        
        print("\n📋 ESTRUCTURA FINAL DE ETIQUETAS:")
        print("   • id_etiqueta (PRIMARY KEY)")
        print("   • nombre_etiqueta (TEXT UNIQUE)")
        print("   • descripcion (TEXT)")
        print("   • color (TEXT)")
        print("   • categoria (TEXT)")
        print("   • activa (INTEGER)")
        print("   • fecha_creacion (TEXT) ← SOLUCIONADO")
        print("   • creado_por (TEXT)")
        
        print("\n🚀 RESULTADO:")
        print("   ✅ Error 'no such column: fecha_creacion' eliminado")
        print("   ✅ Sistema de etiquetas completamente funcional")
        print("   ✅ Backward compatibility mantenida")
        
        print("\n🧪 PRUEBA AHORA:")
        print("   python main_app_refactorizado.py")
        print("   (Ya no deberían aparecer errores de fecha_creacion)")
        
    else:
        print("\n❌ MIGRACIÓN INCOMPLETA")
        print("Revisa los errores específicos arriba")
        print("El backup está disponible para restaurar si es necesario")

if __name__ == "__main__":
    main()
