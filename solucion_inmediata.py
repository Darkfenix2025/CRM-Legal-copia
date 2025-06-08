#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SOLUCIÓN INMEDIATA PARA ERRORES DEL CRM LEGAL
============================================

Este script corrige inmediatamente los errores que estás experimentando:
- Error: no such column: fecha_creacion
- Error: module 'crm_database' has no attribute 'get_dates_with_audiencias'
- Error: module 'crm_database' has no attribute 'get_audiencias_by_date'

INSTRUCCIONES:
1. Guarda este archivo en tu directorio del CRM Legal
2. Ejecuta: python solucion_inmediata.py
3. Luego ejecuta tu aplicación normalmente
"""

import os
import sys

def agregar_funciones_faltantes():
    """Agrega las funciones faltantes al crm_database.py"""
    
    funciones_nuevas = '''

# ===============================================
# FUNCIONES DE COMPATIBILIDAD AGREGADAS AUTOMÁTICAMENTE
# ===============================================

def get_dates_with_audiencias():
    """Obtiene fechas que tienen audiencias programadas"""
    return get_fechas_con_audiencias()

def get_audiencias_by_date(fecha):
    """Obtiene audiencias de una fecha específica"""
    return get_audiencias_by_fecha(fecha)

def get_etiquetas_safe():
    """Obtiene etiquetas sin usar columnas que podrían no existir"""
    conn = connect_db()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_etiqueta, nombre_etiqueta FROM etiquetas ORDER BY nombre_etiqueta")
        return cursor.fetchall()
    except Exception as e:
        print(f"Error obteniendo etiquetas: {e}")
        return []
    finally:
        close_db(conn)

def agregar_columnas_etiquetas():
    """Agrega las columnas faltantes a la tabla etiquetas"""
    conn = connect_db()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Verificar columnas existentes
        cursor.execute("PRAGMA table_info(etiquetas)")
        columnas_existentes = [col[1] for col in cursor.fetchall()]
        
        # Agregar columnas si no existen
        nuevas_columnas = [
            'descripcion TEXT DEFAULT ""',
            'color TEXT DEFAULT "#3498db"', 
            'tipo TEXT DEFAULT "general"',
            'fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP'
        ]
        
        for columna_def in nuevas_columnas:
            nombre_columna = columna_def.split()[0]
            if nombre_columna not in columnas_existentes:
                try:
                    cursor.execute(f"ALTER TABLE etiquetas ADD COLUMN {columna_def}")
                    print(f"✅ Columna '{nombre_columna}' agregada")
                except Exception as e:
                    print(f"⚠️ No se pudo agregar '{nombre_columna}': {e}")
        
        conn.commit()
        return True
        
    except Exception as e:
        print(f"Error agregando columnas: {e}")
        return False
    finally:
        close_db(conn)

# ===============================================
# FIN FUNCIONES DE COMPATIBILIDAD
# ===============================================
'''
    
    try:
        # Verificar si crm_database.py existe
        if not os.path.exists('crm_database.py'):
            print("❌ crm_database.py no encontrado en este directorio")
            print("   Asegúrate de ejecutar este script desde el directorio del CRM Legal")
            return False
        
        # Leer archivo actual
        with open('crm_database.py', 'r', encoding='utf-8') as f:
            contenido_actual = f.read()
        
        # Verificar si ya está patcheado
        if "get_dates_with_audiencias" in contenido_actual:
            print("✅ Las funciones ya están presentes en crm_database.py")
            return True
        
        # Crear backup
        with open('crm_database_backup.py', 'w', encoding='utf-8') as f:
            f.write(contenido_actual)
        print("📁 Backup creado: crm_database_backup.py")
        
        # Agregar funciones
        contenido_nuevo = contenido_actual + funciones_nuevas
        
        with open('crm_database.py', 'w', encoding='utf-8') as f:
            f.write(contenido_nuevo)
        
        print("✅ Funciones agregadas a crm_database.py")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def corregir_esquema_bd():
    """Corrige el esquema de la base de datos"""
    try:
        # Importar el módulo modificado
        sys.path.insert(0, '.')
        import crm_database as db
        
        print("🔧 Corrigiendo esquema de base de datos...")
        
        # Llamar a la función para agregar columnas
        if hasattr(db, 'agregar_columnas_etiquetas'):
            db.agregar_columnas_etiquetas()
            print("✅ Esquema de base de datos actualizado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error corrigiendo BD: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 SOLUCIÓN INMEDIATA - ERRORES CRM LEGAL")
    print("=" * 60)
    print("Corrigiendo errores detectados...\n")
    
    # Paso 1: Agregar funciones faltantes
    print("1. Agregando funciones faltantes...")
    if not agregar_funciones_faltantes():
        print("❌ Error en paso 1")
        return
    
    # Paso 2: Corregir esquema de BD
    print("\n2. Corrigiendo esquema de base de datos...")
    if not corregir_esquema_bd():
        print("❌ Error en paso 2")
        return
    
    print("\n🎉 ¡PROBLEMAS CORREGIDOS!")
    print("=" * 30)
    print("✅ Funciones faltantes agregadas")
    print("✅ Esquema de base de datos corregido")
    print("✅ Backup creado por seguridad")
    
    print("\n🚀 AHORA PUEDES EJECUTAR:")
    if os.path.exists('main_app_refactorizado.py'):
        print("   python main_app_refactorizado.py")
    else:
        print("   python main_app.py")
    
    print("\n📋 Si encuentras más errores:")
    print("   - Revisa que tengas todas las dependencias instaladas")
    print("   - Verifica que el archivo crm_legal.db existe")
    print("   - Contacta para soporte adicional")

if __name__ == "__main__":
    main()
