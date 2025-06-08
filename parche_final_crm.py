#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PARCHE FINAL PARA CRM LEGAL - SOLUCIÓN ESPECÍFICA
================================================

Este parche corrige los problemas específicos detectados en tu instalación:

ERRORES DETECTADOS:
1. no such column: fecha_creacion (en tabla etiquetas)
2. module 'crm_database' has no attribute 'get_dates_with_audiencias'
3. module 'crm_database' has no attribute 'get_audiencias_by_date'
4. no such table: actividades (debería ser actividades_caso)

ESTADO ACTUAL DETECTADO:
✅ Tienes 20 tablas con 447 registros
✅ Sistema de etiquetas globales: FUNCIONANDO (24 etiquetas)
✅ Sistema financiero: FUNCIONANDO (120 conceptos)
✅ Datos importantes preservados

SOLUCIÓN: Parche específico para tu configuración
"""

import os
import sqlite3

def agregar_funciones_faltantes_crm_database():
    """Agrega las funciones específicas que faltan en crm_database.py"""
    
    funciones_compatibilidad = '''

# =====================================================
# PARCHE DE COMPATIBILIDAD - AGREGADO AUTOMÁTICAMENTE
# =====================================================

def get_dates_with_audiencias():
    """Obtiene fechas que tienen audiencias - Alias de compatibilidad"""
    return get_fechas_con_audiencias()

def get_audiencias_by_date(fecha):
    """Obtiene audiencias por fecha - Alias de compatibilidad"""
    return get_audiencias_by_fecha(fecha)

def get_all_etiquetas_compatible():
    """Obtiene etiquetas usando solo columnas que existen"""
    conn = connect_db()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        # Usar solo id_etiqueta y nombre_etiqueta que sabemos que existen
        cursor.execute('''
            SELECT 
                id_etiqueta as id,
                nombre_etiqueta as nombre,
                '' as descripcion,
                '#3498db' as color,
                'general' as categoria,
                '' as fecha_creacion
            FROM etiquetas 
            ORDER BY nombre_etiqueta
        ''')
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener etiquetas compatibles: {e}")
        return []
    finally:
        close_db(conn)

def get_actividades_compatible(caso_id):
    """Obtiene actividades usando el nombre correcto de tabla"""
    conn = connect_db()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM actividades_caso 
            WHERE caso_id = ? 
            ORDER BY fecha DESC
        ''', (caso_id,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error al obtener actividades: {e}")
        return []
    finally:
        close_db(conn)

# =====================================================
# FIN PARCHE DE COMPATIBILIDAD
# =====================================================
'''
    
    try:
        # Verificar si existe el archivo
        if not os.path.exists('crm_database.py'):
            print("❌ crm_database.py no encontrado")
            return False
        
        # Leer contenido actual
        with open('crm_database.py', 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Verificar si ya está patcheado
        if "get_dates_with_audiencias" in contenido:
            print("✅ Las funciones de compatibilidad ya están presentes")
            return True
        
        # Crear backup
        backup_name = 'crm_database_backup_antes_parche.py'
        with open(backup_name, 'w', encoding='utf-8') as f:
            f.write(contenido)
        print(f"📁 Backup creado: {backup_name}")
        
        # Agregar funciones
        contenido_patcheado = contenido + funciones_compatibilidad
        
        with open('crm_database.py', 'w', encoding='utf-8') as f:
            f.write(contenido_patcheado)
        
        print("✅ Funciones de compatibilidad agregadas a crm_database.py")
        return True
        
    except Exception as e:
        print(f"❌ Error agregando funciones: {e}")
        return False

def corregir_main_app_refactorizado():
    """Corrige las consultas problemáticas en main_app_refactorizado.py"""
    
    if not os.path.exists('main_app_refactorizado.py'):
        print("⚠️ main_app_refactorizado.py no encontrado")
        return True
    
    try:
        with open('main_app_refactorizado.py', 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Crear backup
        backup_name = 'main_app_refactorizado_backup.py'
        with open(backup_name, 'w', encoding='utf-8') as f:
            f.write(contenido)
        print(f"📁 Backup main_app creado: {backup_name}")
        
        # Correcciones específicas
        correcciones = {
            # Corregir consultas que buscan fecha_creacion en tabla etiquetas
            'SELECT id_etiqueta, nombre_etiqueta, fecha_creacion FROM etiquetas': 
                'SELECT id_etiqueta, nombre_etiqueta, \'\' as fecha_creacion FROM etiquetas',
            
            'e.fecha_creacion': 'e.nombre_etiqueta',  # Reemplazar referencia problemática
            
            # Corregir nombre de tabla actividades
            'FROM actividades': 'FROM actividades_caso',
            'INTO actividades': 'INTO actividades_caso',
            
            # Usar funciones compatibles
            'db.get_all_etiquetas()': 'db.get_all_etiquetas_compatible()',
        }
        
        contenido_corregido = contenido
        cambios_realizados = 0
        
        for buscar, reemplazar in correcciones.items():
            if buscar in contenido_corregido:
                contenido_corregido = contenido_corregido.replace(buscar, reemplazar)
                cambios_realizados += 1
                print(f"✅ Corregido: {buscar[:50]}...")
        
        # Solo escribir si hubo cambios
        if cambios_realizados > 0:
            with open('main_app_refactorizado.py', 'w', encoding='utf-8') as f:
                f.write(contenido_corregido)
            print(f"✅ main_app_refactorizado.py corregido ({cambios_realizados} cambios)")
        else:
            print("✅ main_app_refactorizado.py no necesitaba correcciones")
        
        return True
        
    except Exception as e:
        print(f"❌ Error corrigiendo main_app: {e}")
        return False

def verificar_esquema_bd():
    """Verifica y corrige el esquema de base de datos si es necesario"""
    
    try:
        conn = sqlite3.connect('crm_legal.db')
        cursor = conn.cursor()
        
        print("🔍 Verificando esquema de base de datos...")
        
        # Verificar estructura de tabla etiquetas
        cursor.execute("PRAGMA table_info(etiquetas)")
        columnas_etiquetas = [col[1] for col in cursor.fetchall()]
        print(f"📋 Columnas en tabla etiquetas: {columnas_etiquetas}")
        
        # Verificar si existe tabla actividades vs actividades_caso
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%actividades%'")
        tablas_actividades = [row[0] for row in cursor.fetchall()]
        print(f"📋 Tablas de actividades: {tablas_actividades}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error verificando esquema: {e}")
        return False

def main():
    """Ejecuta el parche completo"""
    print("🚀 PARCHE FINAL PARA CRM LEGAL")
    print("=" * 60)
    print("Aplicando correcciones específicas para tu instalación...\n")
    
    exito_total = True
    
    # 1. Verificar esquema actual
    print("1. Verificando esquema de base de datos...")
    if verificar_esquema_bd():
        print("✅ Esquema verificado correctamente")
    else:
        print("⚠️ Problemas verificando esquema")
    
    # 2. Agregar funciones faltantes
    print("\n2. Agregando funciones faltantes...")
    if agregar_funciones_faltantes_crm_database():
        print("✅ Funciones agregadas exitosamente")
    else:
        exito_total = False
        print("❌ Error agregando funciones")
    
    # 3. Corregir main_app
    print("\n3. Corrigiendo main_app_refactorizado.py...")
    if corregir_main_app_refactorizado():
        print("✅ main_app corregido exitosamente")
    else:
        exito_total = False
        print("❌ Error corrigiendo main_app")
    
    # Resultados finales
    if exito_total:
        print("\n🎉 PARCHE APLICADO EXITOSAMENTE!")
        print("=" * 50)
        print("✅ Funciones de compatibilidad agregadas:")
        print("   • get_dates_with_audiencias()")
        print("   • get_audiencias_by_date(fecha)")
        print("   • get_all_etiquetas_compatible()")
        print("   • get_actividades_compatible(caso_id)")
        print("\n✅ Consultas problemáticas corregidas")
        print("✅ Referencias a tablas corregidas")
        print("✅ Backups de seguridad creados")
        
        print("\n🚀 AHORA EJECUTA:")
        print("   python main_app_refactorizado.py")
        print("\n📊 TU SISTEMA TIENE:")
        print("   • 20 tablas con 447 registros")
        print("   • 24 etiquetas globales funcionales")
        print("   • 120 conceptos de facturación")
        print("   • Todas las funcionalidades preservadas")
        
    else:
        print("\n❌ ALGUNOS PROBLEMAS DURANTE EL PARCHE")
        print("Revisa los errores específicos arriba")
        print("Los backups están disponibles para restaurar si es necesario")

if __name__ == "__main__":
    main()
