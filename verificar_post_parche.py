#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VERIFICADOR POST-PARCHE - CRM LEGAL
==================================

Este script verifica que el parche se haya aplicado correctamente
y que todas las funciones estén disponibles.
"""

import os
import sys

def verificar_funciones_crm_database():
    """Verifica que todas las funciones necesarias estén disponibles"""
    print("🔍 VERIFICANDO FUNCIONES EN CRM_DATABASE.PY")
    print("=" * 50)
    
    try:
        # Importar el módulo modificado
        sys.path.insert(0, '.')
        import crm_database as db
        
        # Lista de funciones que deben existir
        funciones_requeridas = [
            'get_dates_with_audiencias',
            'get_audiencias_by_date', 
            'get_all_etiquetas_compatible',
            'get_actividades_compatible',
            'connect_db',
            'get_clients',
            'get_cases_by_client'
        ]
        
        funciones_disponibles = []
        funciones_faltantes = []
        
        for func_name in funciones_requeridas:
            if hasattr(db, func_name):
                funciones_disponibles.append(func_name)
                print(f"✅ {func_name}")
            else:
                funciones_faltantes.append(func_name)
                print(f"❌ {func_name}")
        
        print(f"\n📊 RESUMEN:")
        print(f"✅ Funciones disponibles: {len(funciones_disponibles)}")
        print(f"❌ Funciones faltantes: {len(funciones_faltantes)}")
        
        if funciones_faltantes:
            print(f"\n⚠️ FUNCIONES FALTANTES:")
            for func in funciones_faltantes:
                print(f"   • {func}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error importando crm_database: {e}")
        return False

def probar_funciones_nuevas():
    """Prueba que las funciones nuevas funcionen correctamente"""
    print("\n🧪 PROBANDO FUNCIONES NUEVAS")
    print("=" * 40)
    
    try:
        import crm_database as db
        
        # Probar función de etiquetas
        print("Probando get_all_etiquetas_compatible()...")
        etiquetas = db.get_all_etiquetas_compatible()
        print(f"✅ Obtenidas {len(etiquetas)} etiquetas")
        
        # Probar función de audiencias (si existen datos)
        print("Probando get_dates_with_audiencias()...")
        fechas = db.get_dates_with_audiencias()
        print(f"✅ Obtenidas {len(fechas)} fechas con audiencias")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando funciones: {e}")
        return False

def verificar_main_app_sintaxis():
    """Verifica que main_app_refactorizado.py tenga sintaxis correcta"""
    print("\n📝 VERIFICANDO SINTAXIS DE MAIN_APP")
    print("=" * 45)
    
    if not os.path.exists('main_app_refactorizado.py'):
        print("⚠️ main_app_refactorizado.py no encontrado")
        return True
    
    try:
        # Compilar para verificar sintaxis
        with open('main_app_refactorizado.py', 'r', encoding='utf-8') as f:
            code = f.read()
        
        compile(code, 'main_app_refactorizado.py', 'exec')
        print("✅ Sintaxis de main_app_refactorizado.py es correcta")
        return True
        
    except SyntaxError as e:
        print(f"❌ Error de sintaxis en main_app: {e}")
        print(f"   Línea {e.lineno}: {e.text}")
        return False
    except Exception as e:
        print(f"❌ Error verificando sintaxis: {e}")
        return False

def verificar_base_datos():
    """Verifica conectividad y estructura básica de la BD"""
    print("\n🗄️ VERIFICANDO BASE DE DATOS")
    print("=" * 35)
    
    try:
        import sqlite3
        
        if not os.path.exists('crm_legal.db'):
            print("❌ Base de datos crm_legal.db no encontrada")
            return False
        
        conn = sqlite3.connect('crm_legal.db')
        cursor = conn.cursor()
        
        # Verificar conexión
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
        num_tablas = cursor.fetchone()[0]
        print(f"✅ Conectado - {num_tablas} tablas encontradas")
        
        # Verificar tablas críticas
        tablas_criticas = ['clientes', 'casos', 'audiencias', 'etiquetas_globales']
        for tabla in tablas_criticas:
            cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
            count = cursor.fetchone()[0]
            print(f"✅ Tabla {tabla}: {count} registros")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error verificando base de datos: {e}")
        return False

def generar_reporte_completo():
    """Genera un reporte completo del estado del sistema"""
    print("\n📋 REPORTE COMPLETO DEL SISTEMA")
    print("=" * 45)
    
    try:
        import crm_database as db
        
        # Obtener estadísticas
        clientes = db.get_clients()
        print(f"👥 Clientes: {len(clientes)}")
        
        if clientes:
            casos_total = 0
            for cliente in clientes:
                casos = db.get_cases_by_client(cliente['id'])
                casos_total += len(casos)
            print(f"📁 Casos total: {casos_total}")
        
        etiquetas = db.get_all_etiquetas_compatible()
        print(f"🏷️ Etiquetas: {len(etiquetas)}")
        
        fechas_audiencias = db.get_dates_with_audiencias()
        print(f"📅 Fechas con audiencias: {len(fechas_audiencias)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generando reporte: {e}")
        return False

def main():
    """Función principal de verificación"""
    print("🔬 VERIFICACIÓN POST-PARCHE CRM LEGAL")
    print("=" * 60)
    print("Verificando que todas las correcciones funcionen...\n")
    
    todos_los_tests = []
    
    # Test 1: Verificar funciones
    todos_los_tests.append(verificar_funciones_crm_database())
    
    # Test 2: Probar funciones nuevas
    todos_los_tests.append(probar_funciones_nuevas())
    
    # Test 3: Verificar sintaxis
    todos_los_tests.append(verificar_main_app_sintaxis())
    
    # Test 4: Verificar BD
    todos_los_tests.append(verificar_base_datos())
    
    # Test 5: Reporte completo
    todos_los_tests.append(generar_reporte_completo())
    
    # Resultados finales
    tests_pasados = sum(todos_los_tests)
    tests_totales = len(todos_los_tests)
    
    print(f"\n🎯 RESULTADOS FINALES")
    print("=" * 30)
    print(f"✅ Tests pasados: {tests_pasados}/{tests_totales}")
    
    if tests_pasados == tests_totales:
        print("\n🎉 ¡TODOS LOS TESTS PASARON!")
        print("🚀 Tu CRM Legal está listo para usar")
        print("\n📋 PRÓXIMOS PASOS:")
        print("1. Ejecuta: python main_app_refactorizado.py")
        print("2. Prueba las nuevas funcionalidades")
        print("3. Reporta cualquier problema adicional")
        
    else:
        print(f"\n⚠️ {tests_totales - tests_pasados} TESTS FALLARON")
        print("Revisa los errores específicos arriba")
        print("Puede que necesites aplicar el parche nuevamente")

if __name__ == "__main__":
    main()
