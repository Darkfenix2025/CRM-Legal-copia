#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT DE DEBUGGING PARA PROBLEMA DE CLIENTES
===========================================

Este script verifica paso a paso qué está pasando con la carga de clientes.
"""

import sqlite3
import os

def debug_database_connection():
    """Verifica la conexión a la base de datos"""
    print("🔍 DEBUGGING: CONEXIÓN A BASE DE DATOS")
    print("=" * 50)
    
    try:
        # Verificar si existe el archivo
        if not os.path.exists('crm_legal.db'):
            print("❌ Base de datos crm_legal.db NO EXISTE")
            return False
        
        # Intentar conectar
        conn = sqlite3.connect('crm_legal.db')
        print("✅ Conexión exitosa a crm_legal.db")
        
        # Verificar tabla clientes
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='clientes'")
        if cursor.fetchone():
            print("✅ Tabla 'clientes' existe")
        else:
            print("❌ Tabla 'clientes' NO EXISTE")
            return False
        
        # Contar registros
        cursor.execute("SELECT COUNT(*) FROM clientes")
        count = cursor.fetchone()[0]
        print(f"📊 Total de clientes en BD: {count}")
        
        # Mostrar algunos clientes
        cursor.execute("SELECT id, nombre, email FROM clientes LIMIT 5")
        clientes = cursor.fetchall()
        print(f"📋 Primeros {len(clientes)} clientes:")
        for cliente in clientes:
            print(f"   ID: {cliente[0]} - Nombre: {cliente[1]} - Email: {cliente[2]}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error en conexión: {e}")
        return False

def debug_crm_database_function():
    """Verifica la función get_clients() del módulo crm_database"""
    print("\n🔍 DEBUGGING: FUNCIÓN get_clients()")
    print("=" * 45)
    
    try:
        # Importar el módulo
        import crm_database as db
        print("✅ Módulo crm_database importado correctamente")
        
        # Verificar si existe la función
        if hasattr(db, 'get_clients'):
            print("✅ Función get_clients() existe")
        else:
            print("❌ Función get_clients() NO EXISTE")
            return False
        
        # Llamar a la función
        print("🔄 Llamando a db.get_clients()...")
        clientes = db.get_clients()
        
        if clientes is None:
            print("❌ get_clients() retornó None")
            return False
        elif isinstance(clientes, list):
            print(f"✅ get_clients() retornó lista con {len(clientes)} elementos")
            
            # Mostrar estructura de los primeros clientes
            for i, cliente in enumerate(clientes[:3]):
                print(f"📋 Cliente {i+1}: {type(cliente)} - {cliente}")
            
            return True
        else:
            print(f"⚠️ get_clients() retornó tipo inesperado: {type(clientes)}")
            return False
        
    except Exception as e:
        print(f"❌ Error probando get_clients(): {e}")
        import traceback
        traceback.print_exc()
        return False

def debug_clientes_module():
    """Verifica si el módulo de clientes puede cargarse"""
    print("\n🔍 DEBUGGING: MÓDULO clientes_ui")
    print("=" * 40)
    
    try:
        # Intentar importar el módulo
        from clientes_ui import ClientesTab
        print("✅ Módulo clientes_ui importado correctamente")
        
        # Crear un mock del app_controller
        class MockAppController:
            def __init__(self):
                import crm_database as db
                self.db_crm = db
        
        # Crear un tkinter dummy
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Ocultar ventana
        
        mock_controller = MockAppController()
        
        # Intentar crear el módulo
        print("🔄 Creando instancia de ClientesTab...")
        clientes_tab = ClientesTab(root, mock_controller)
        print("✅ ClientesTab creado exitosamente")
        
        # Intentar cargar clientes
        print("🔄 Llamando a load_clients()...")
        clientes_tab.load_clients()
        print("✅ load_clients() ejecutado sin errores")
        
        # Verificar cuántos items hay en el TreeView
        children = clientes_tab.client_tree.get_children()
        print(f"📊 Items en TreeView: {len(children)}")
        
        if len(children) > 0:
            print("✅ ¡Hay datos en el TreeView!")
            for i, child in enumerate(children[:3]):
                values = clientes_tab.client_tree.item(child, 'values')
                print(f"   Fila {i+1}: {values}")
        else:
            print("❌ TreeView está vacío")
        
        root.destroy()
        return len(children) > 0
        
    except Exception as e:
        print(f"❌ Error en módulo clientes_ui: {e}")
        import traceback
        traceback.print_exc()
        return False

def debug_main_app_structure():
    """Verifica la estructura del main_app_refactorizado"""
    print("\n🔍 DEBUGGING: ESTRUCTURA MAIN_APP")
    print("=" * 45)
    
    try:
        # Verificar que el archivo existe
        if not os.path.exists('main_app_refactorizado.py'):
            print("❌ main_app_refactorizado.py NO EXISTE")
            return False
        
        print("✅ main_app_refactorizado.py existe")
        
        # Verificar imports
        with open('main_app_refactorizado.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'from clientes_ui import ClientesTab' in content:
            print("✅ Import de ClientesTab encontrado")
        else:
            print("❌ Import de ClientesTab NO encontrado")
        
        if 'self.clientes_module.load_clients()' in content:
            print("✅ Llamada a load_clients() encontrada")
        else:
            print("❌ Llamada a load_clients() NO encontrada")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando main_app: {e}")
        return False

def main():
    """Función principal de debugging"""
    print("🐛 DEBUGGING COMPLETO - PROBLEMA DE CLIENTES")
    print("=" * 60)
    print("Verificando paso a paso dónde está el problema...\n")
    
    # Test 1: Conexión a BD
    test1 = debug_database_connection()
    
    # Test 2: Función get_clients()
    test2 = debug_crm_database_function()
    
    # Test 3: Módulo clientes_ui
    test3 = debug_clientes_module()
    
    # Test 4: Estructura main_app
    test4 = debug_main_app_structure()
    
    # Resumen final
    print(f"\n🎯 RESUMEN DE DEBUGGING")
    print("=" * 30)
    print(f"✅ Conexión a BD: {'OK' if test1 else 'FALLO'}")
    print(f"✅ Función get_clients(): {'OK' if test2 else 'FALLO'}")
    print(f"✅ Módulo clientes_ui: {'OK' if test3 else 'FALLO'}")
    print(f"✅ Estructura main_app: {'OK' if test4 else 'FALLO'}")
    
    if all([test1, test2, test3, test4]):
        print("\n🎉 ¡TODOS LOS TESTS PASARON!")
        print("El problema podría ser de inicialización o timing.")
        print("Intenta ejecutar main_app_refactorizado.py nuevamente.")
    else:
        print(f"\n❌ {4 - sum([test1, test2, test3, test4])} TESTS FALLARON")
        print("Revisa los errores específicos arriba para identificar el problema.")

if __name__ == "__main__":
    main()
