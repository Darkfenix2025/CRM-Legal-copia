#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PARCHE DE COMPATIBILIDAD - CRM LEGAL
==================================

Este script corrige los problemas de compatibilidad entre el código refactorizado
y el esquema de base de datos existente.

PROBLEMAS DETECTADOS:
1. Tabla etiquetas no tiene columna 'fecha_creacion'
2. Funciones get_dates_with_audiencias / get_audiencias_by_date no existen
3. Incompatibilidad de nombres de funciones

SOLUCIÓN:
- Agrega las funciones faltantes como aliases
- Modifica el esquema de etiquetas si es necesario
- Corrige las consultas para usar las columnas existentes
"""

import sqlite3
import os
import sys

def fix_database_schema():
    """Corrige el esquema de la base de datos para compatibilidad"""
    print("🔧 CORRIGIENDO ESQUEMA DE BASE DE DATOS")
    print("=" * 50)
    
    db_path = 'crm_legal.db'
    if not os.path.exists(db_path):
        print(f"❌ Base de datos no encontrada: {db_path}")
        return False
    
    try:
        # Crear backup
        import shutil
        backup_path = f"backup_before_fix_{db_path}"
        shutil.copy2(db_path, backup_path)
        print(f"✅ Backup creado: {backup_path}")
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar estructura actual de etiquetas
        cursor.execute("PRAGMA table_info(etiquetas)")
        columnas_etiquetas = [col[1] for col in cursor.fetchall()]
        print(f"📋 Columnas actuales en etiquetas: {columnas_etiquetas}")
        
        # Agregar columnas faltantes a etiquetas si no existen
        columnas_nuevas = [
            ('descripcion', 'TEXT DEFAULT ""'),
            ('color', 'TEXT DEFAULT "#3498db"'),
            ('tipo', 'TEXT DEFAULT "general"'),
            ('fecha_creacion', 'TEXT DEFAULT CURRENT_TIMESTAMP')
        ]
        
        for nombre_columna, definicion in columnas_nuevas:
            if nombre_columna not in columnas_etiquetas:
                try:
                    cursor.execute(f"ALTER TABLE etiquetas ADD COLUMN {nombre_columna} {definicion}")
                    print(f"✅ Columna '{nombre_columna}' agregada a etiquetas")
                except sqlite3.OperationalError as e:
                    if "duplicate column name" not in str(e):
                        print(f"⚠️ Error agregando columna '{nombre_columna}': {e}")
        
        conn.commit()
        conn.close()
        
        print("✅ Esquema de base de datos corregido")
        return True
        
    except Exception as e:
        print(f"❌ Error corrigiendo esquema: {e}")
        return False

def add_missing_functions():
    """Agrega las funciones faltantes al módulo crm_database"""
    print("\n🔧 AGREGANDO FUNCIONES FALTANTES")
    print("=" * 40)
    
    functions_to_add = """

# === FUNCIONES DE COMPATIBILIDAD AGREGADAS AUTOMÁTICAMENTE ===

def get_dates_with_audiencias():
    \"\"\"Alias para compatibilidad con código refactorizado\"\"\"
    return get_fechas_con_audiencias()

def get_audiencias_by_date(fecha):
    \"\"\"Alias para compatibilidad con código refactorizado\"\"\"
    return get_audiencias_by_fecha(fecha)

def get_all_etiquetas_globales():
    \"\"\"Obtiene todas las etiquetas globales con información completa\"\"\"
    conn = connect_db()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT 
                id_etiqueta as id,
                nombre_etiqueta as nombre,
                COALESCE(descripcion, '') as descripcion,
                COALESCE(color, '#3498db') as color,
                COALESCE(tipo, 'general') as tipo,
                COALESCE(fecha_creacion, '') as fecha_creacion
            FROM etiquetas 
            ORDER BY nombre_etiqueta
        ''')
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener etiquetas globales: {e}")
        return []
    finally:
        close_db(conn)

def update_etiqueta_global(etiqueta_id, nombre, descripcion="", color="#3498db", tipo="general"):
    \"\"\"Actualiza una etiqueta global\"\"\"
    conn = connect_db()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE etiquetas 
            SET nombre_etiqueta = ?, descripcion = ?, color = ?, tipo = ?
            WHERE id_etiqueta = ?
        ''', (nombre, descripcion, color, tipo, etiqueta_id))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Error actualizando etiqueta: {e}")
        return False
    finally:
        close_db(conn)

def add_etiqueta_global(nombre, descripcion="", color="#3498db", tipo="general"):
    \"\"\"Agrega una nueva etiqueta global\"\"\"
    conn = connect_db()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO etiquetas (nombre_etiqueta, descripcion, color, tipo, fecha_creacion)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (nombre, descripcion, color, tipo))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Error agregando etiqueta: {e}")
        return None
    finally:
        close_db(conn)

# === FIN FUNCIONES DE COMPATIBILIDAD ===
"""
    
    try:
        # Leer el archivo actual
        with open('crm_database.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar si ya están las funciones
        if "get_dates_with_audiencias" in content:
            print("✅ Las funciones de compatibilidad ya están presentes")
            return True
        
        # Agregar las funciones al final
        with open('crm_database.py', 'a', encoding='utf-8') as f:
            f.write(functions_to_add)
        
        print("✅ Funciones de compatibilidad agregadas")
        return True
        
    except Exception as e:
        print(f"❌ Error agregando funciones: {e}")
        return False

def create_compatibility_wrapper():
    """Crea un wrapper de compatibilidad temporal"""
    print("\n🔧 CREANDO WRAPPER DE COMPATIBILIDAD")
    print("=" * 45)
    
    wrapper_code = '''# compatibility_wrapper.py
"""
Wrapper de compatibilidad temporal para el CRM Legal
Este archivo proporciona las funciones que faltan en crm_database.py
"""

import crm_database as db

# Crear aliases para las funciones con nombres diferentes
def get_dates_with_audiencias():
    """Alias para get_fechas_con_audiencias"""
    return db.get_fechas_con_audiencias()

def get_audiencias_by_date(fecha):
    """Alias para get_audiencias_by_fecha"""
    return db.get_audiencias_by_fecha(fecha)

def get_all_etiquetas_safe():
    """Obtiene etiquetas de forma segura sin columnas que podrían no existir"""
    try:
        return db.get_todas_las_etiquetas()
    except Exception as e:
        print(f"Error obteniendo etiquetas: {e}")
        return []

# Hacer que este módulo actúe como proxy de crm_database
def __getattr__(name):
    """Delega cualquier función no definida aquí al módulo original"""
    return getattr(db, name)
'''
    
    try:
        with open('compatibility_wrapper.py', 'w', encoding='utf-8') as f:
            f.write(wrapper_code)
        print("✅ Wrapper de compatibilidad creado")
        return True
    except Exception as e:
        print(f"❌ Error creando wrapper: {e}")
        return False

def patch_main_app():
    """Crea una versión patcheada del main_app_refactorizado.py"""
    print("\n🔧 CREANDO VERSIÓN PATCHEADA DE MAIN_APP")
    print("=" * 50)
    
    try:
        # Leer el archivo refactorizado
        if not os.path.exists('main_app_refactorizado.py'):
            print("❌ main_app_refactorizado.py no encontrado")
            return False
        
        with open('main_app_refactorizado.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Reemplazos necesarios
        replacements = {
            'import crm_database as db': 'import compatibility_wrapper as db',
            'get_dates_with_audiencias': 'get_dates_with_audiencias',
            'get_audiencias_by_date': 'get_audiencias_by_date',
            'fecha_creacion': 'nombre_etiqueta',  # Usar campo que sí existe
        }
        
        patched_content = content
        for old, new in replacements.items():
            patched_content = patched_content.replace(old, new)
        
        # Crear versión patcheada
        with open('main_app_compatible.py', 'w', encoding='utf-8') as f:
            f.write(patched_content)
        
        print("✅ main_app_compatible.py creado")
        return True
        
    except Exception as e:
        print(f"❌ Error creando versión patcheada: {e}")
        return False

def main():
    """Función principal del parche"""
    print("🚀 PARCHE DE COMPATIBILIDAD CRM LEGAL")
    print("=" * 60)
    print("Corrigiendo problemas detectados...\n")
    
    success = True
    
    # 1. Corregir esquema de BD
    if not fix_database_schema():
        success = False
    
    # 2. Crear wrapper de compatibilidad  
    if not create_compatibility_wrapper():
        success = False
    
    # 3. Crear versión patcheada del main_app
    if not patch_main_app():
        success = False
    
    if success:
        print("\n🎉 PARCHE APLICADO EXITOSAMENTE")
        print("=" * 40)
        print("✅ Esquema de base de datos corregido")
        print("✅ Wrapper de compatibilidad creado")
        print("✅ Versión compatible del main_app creada")
        print("\n📋 PRÓXIMOS PASOS:")
        print("1. Ejecuta: python main_app_compatible.py")
        print("2. Si todo funciona, reemplaza main_app_refactorizado.py")
        print("3. ¡Disfruta tu CRM Legal funcionando!")
    else:
        print("\n❌ ALGUNOS PROBLEMAS DURANTE EL PARCHE")
        print("Revisa los errores anteriores")

if __name__ == "__main__":
    main()
