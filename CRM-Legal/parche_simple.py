#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PARCHE SIMPLE SIN ERRORES - CRM LEGAL
====================================

Versión simplificada que agrega solo las funciones esenciales
para corregir los errores inmediatamente.
"""

import os

def agregar_funciones_simples():
    """Agrega funciones básicas sin consultas complejas"""
    
    codigo_simple = """

# === FUNCIONES DE COMPATIBILIDAD SIMPLES ===

def get_dates_with_audiencias():
    return get_fechas_con_audiencias()

def get_audiencias_by_date(fecha):
    return get_audiencias_by_fecha(fecha)

def get_all_etiquetas_simple():
    conn = connect_db()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_etiqueta, nombre_etiqueta FROM etiquetas ORDER BY nombre_etiqueta")
        return cursor.fetchall()
    except:
        return []
    finally:
        close_db(conn)

# === FIN FUNCIONES COMPATIBILIDAD ===
"""
    
    try:
        # Verificar archivo
        if not os.path.exists('crm_database.py'):
            print("❌ crm_database.py no encontrado")
            return False
        
        # Leer contenido
        with open('crm_database.py', 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Verificar si ya existe
        if "get_dates_with_audiencias" in contenido:
            print("✅ Ya está patcheado")
            return True
        
        # Crear backup
        with open('backup_crm_database.py', 'w', encoding='utf-8') as f:
            f.write(contenido)
        print("✅ Backup creado")
        
        # Agregar funciones
        with open('crm_database.py', 'a', encoding='utf-8') as f:
            f.write(codigo_simple)
        
        print("✅ Funciones agregadas")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🔧 PARCHE SIMPLE PARA CRM LEGAL")
    print("=" * 40)
    
    if agregar_funciones_simples():
        print("\n🎉 ¡PARCHE APLICADO!")
        print("✅ Funciones básicas agregadas")
        print("✅ Backup de seguridad creado")
        print("\n🚀 Ejecuta ahora:")
        print("python main_app_refactorizado.py")
    else:
        print("\n❌ Error aplicando parche")

if __name__ == "__main__":
    main()
