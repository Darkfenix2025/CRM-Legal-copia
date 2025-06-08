#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PARCHE DIRECTO PARA CRM_DATABASE.PY
=================================

Este script agrega directamente las funciones faltantes al archivo crm_database.py
para resolver los errores de compatibilidad de inmediato.
"""

import os

def patch_crm_database():
    """Agrega las funciones faltantes directamente al crm_database.py"""
    
    functions_to_add = '''

# ===============================================
# FUNCIONES DE COMPATIBILIDAD - AGREGADAS AUTOMÁTICAMENTE
# ===============================================

def get_dates_with_audiencias():
    """Alias para compatibilidad - Obtiene fechas que tienen audiencias"""
    return get_fechas_con_audiencias()

def get_audiencias_by_date(fecha):
    """Alias para compatibilidad - Obtiene audiencias por fecha específica"""
    return get_audiencias_by_fecha(fecha)

def get_all_etiquetas_safe():
    """Obtiene todas las etiquetas de forma segura"""
    conn = connect_db()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        # Usar solo las columnas que sabemos que existen
        cursor.execute('''
            SELECT 
                id_etiqueta as id,
                nombre_etiqueta as nombre,
                '' as descripcion,
                '#3498db' as color,
                'general' as tipo,
                '' as fecha_creacion
            FROM etiquetas 
            ORDER BY nombre_etiqueta
        ''')
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener etiquetas: {e}")
        return []
    finally:
        close_db(conn)

def ensure_etiquetas_columns():
    """Asegura que la tabla etiquetas tenga las columnas necesarias"""
    conn = connect_db()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Verificar qué columnas existen
        cursor.execute("PRAGMA table_info(etiquetas)")
        existing_columns = [col[1] for col in cursor.fetchall()]
        
        # Agregar columnas faltantes
        new_columns = [
            ('descripcion', 'TEXT DEFAULT ""'),
            ('color', 'TEXT DEFAULT "#3498db"'),
            ('tipo', 'TEXT DEFAULT "general"'),
            ('fecha_creacion', 'TEXT DEFAULT CURRENT_TIMESTAMP')
        ]
        
        for col_name, col_def in new_columns:
            if col_name not in existing_columns:
                try:
                    cursor.execute(f"ALTER TABLE etiquetas ADD COLUMN {col_name} {col_def}")
                    print(f"✅ Columna '{col_name}' agregada a tabla etiquetas")
                except Exception as e:
                    print(f"⚠️ No se pudo agregar columna '{col_name}': {e}")
        
        conn.commit()
        return True
        
    except Exception as e:
        print(f"Error verificando/agregando columnas: {e}")
        return False
    finally:
        close_db(conn)

# ===============================================
# FIN FUNCIONES DE COMPATIBILIDAD
# ===============================================
'''
    
    try:
        # Verificar si el archivo existe
        if not os.path.exists('crm_database.py'):
            print("❌ crm_database.py no encontrado")
            return False
        
        # Leer contenido actual
        with open('crm_database.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar si ya está patcheado
        if "get_dates_with_audiencias" in content:
            print("✅ crm_database.py ya está patcheado")
            return True
        
        # Crear backup
        with open('crm_database_original_backup.py', 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Backup creado: crm_database_original_backup.py")
        
        # Agregar funciones al final
        patched_content = content + functions_to_add
        
        with open('crm_database.py', 'w', encoding='utf-8') as f:
            f.write(patched_content)
        
        print("✅ crm_database.py patcheado exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error patcheando crm_database.py: {e}")
        return False

def fix_main_app_imports():
    """Corrige las consultas problemáticas en main_app_refactorizado.py"""
    
    try:
        if not os.path.exists('main_app_refactorizado.py'):
            print("⚠️ main_app_refactorizado.py no encontrado")
            return True  # No es error crítico
        
        with open('main_app_refactorizado.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Reemplazos para corregir las consultas problemáticas
        fixes = {
            # Corregir consultas de etiquetas que buscan fecha_creacion
            'fecha_creacion': 'nombre_etiqueta',
            # Agregar llamada a ensure_etiquetas_columns
            'self.db_crm = db': 'self.db_crm = db\n        # Asegurar que la tabla etiquetas tenga las columnas necesarias\n        db.ensure_etiquetas_columns()',
        }
        
        fixed_content = content
        for old, new in fixes.items():
            fixed_content = fixed_content.replace(old, new)
        
        # Solo escribir si hubo cambios
        if fixed_content != content:
            with open('main_app_refactorizado.py', 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print("✅ main_app_refactorizado.py corregido")
        
        return True
        
    except Exception as e:
        print(f"❌ Error corrigiendo main_app: {e}")
        return False

def main():
    """Aplica el parche completo"""
    print("🔧 APLICANDO PARCHE DIRECTO AL CRM DATABASE")
    print("=" * 60)
    
    success = True
    
    print("\n1. Patcheando crm_database.py...")
    if patch_crm_database():
        print("✅ crm_database.py patcheado exitosamente")
    else:
        success = False
        print("❌ Error patcheando crm_database.py")
    
    print("\n2. Corrigiendo main_app_refactorizado.py...")
    if fix_main_app_imports():
        print("✅ main_app_refactorizado.py corregido")
    else:
        success = False
        print("❌ Error corrigiendo main_app_refactorizado.py")
    
    if success:
        print("\n🎉 PARCHE APLICADO EXITOSAMENTE")
        print("=" * 40)
        print("📋 Funciones agregadas:")
        print("   • get_dates_with_audiencias()")
        print("   • get_audiencias_by_date(fecha)")
        print("   • get_all_etiquetas_safe()")
        print("   • ensure_etiquetas_columns()")
        print("\n🚀 Ahora puedes ejecutar:")
        print("   python main_app_refactorizado.py")
    else:
        print("\n❌ ALGUNOS PROBLEMAS DURANTE EL PARCHE")
        print("Revisa los errores anteriores")

if __name__ == "__main__":
    main()
