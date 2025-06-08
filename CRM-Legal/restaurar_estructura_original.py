#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RESTAURAR ESTRUCTURA ORIGINAL DE 3 COLUMNAS
==========================================

Este script restaura la estructura original del CRM Legal:
- Columna 0: Gestión de Clientes
- Columna 1: Gestión de Casos + Audiencias
- Columna 2: Pestañas (Notebook)

Esta es la distribución que funcionaba correctamente.
"""

import os

def restaurar_estructura_3_columnas():
    """Restaura la estructura original de 3 columnas"""
    
    nueva_estructura = '''    def create_widgets(self):
        """Crear la interfaz principal con estructura original de 3 columnas"""
        # Frame principal
        crm_main_frame = ttk.Frame(self.root, padding="10")
        crm_main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configuración de columnas principales del CRM (ESTRUCTURA ORIGINAL)
        crm_main_frame.rowconfigure(0, weight=1)
        crm_main_frame.columnconfigure(0, weight=0, minsize=250)  # Clientes (ancho fijo)
        crm_main_frame.columnconfigure(1, weight=0, minsize=300)  # Casos/Calendario (ancho fijo)
        crm_main_frame.columnconfigure(2, weight=2)  # Notebook y pestañas (más espacio)

        # --- Columna 0: Clientes ---
        self.col1_frame = ttk.Frame(crm_main_frame)
        self.col1_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 5), pady=5)
        self.col1_frame.rowconfigure(0, weight=1)  # Lista clientes
        self.col1_frame.columnconfigure(0, weight=1)

        # Frame para clientes (ahora en su propia columna)
        self.clientes_frame = ttk.LabelFrame(self.col1_frame, text="Gestión de Clientes", padding="5")
        self.clientes_frame.grid(row=0, column=0, sticky='nsew')
        self.clientes_frame.columnconfigure(0, weight=1)
        self.clientes_frame.rowconfigure(0, weight=1)

        # --- Columna 1: Casos y Audiencias ---
        self.col2_frame = ttk.Frame(crm_main_frame)
        self.col2_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        self.col2_frame.rowconfigure(0, weight=1)  # Casos
        self.col2_frame.rowconfigure(1, weight=1)  # Audiencias
        self.col2_frame.columnconfigure(0, weight=1)

        # Frame para casos
        self.casos_frame = ttk.LabelFrame(self.col2_frame, text="Gestión de Casos", padding="5")
        self.casos_frame.grid(row=0, column=0, sticky='nsew', pady=(0, 5))
        self.casos_frame.columnconfigure(0, weight=1)
        self.casos_frame.rowconfigure(0, weight=1)

        # Frame para audiencias
        self.audiencias_frame = ttk.LabelFrame(self.col2_frame, text="Audiencias", padding="5")
        self.audiencias_frame.grid(row=1, column=0, sticky='nsew', pady=(5, 0))
        self.audiencias_frame.columnconfigure(0, weight=1)
        self.audiencias_frame.rowconfigure(0, weight=1)

        # --- Columna 2: Notebook con pestañas ---
        self.col3_frame = ttk.Frame(crm_main_frame)
        self.col3_frame.grid(row=0, column=2, sticky='nsew', padx=(5, 0), pady=5)
        self.col3_frame.rowconfigure(0, weight=1)
        self.col3_frame.columnconfigure(0, weight=1)

        # Notebook principal
        self.main_notebook = ttk.Notebook(self.col3_frame)
        self.main_notebook.grid(row=0, column=0, sticky='nsew')

        # Crear todas las pestañas del notebook
        self.create_notebook_tabs()'''
    
    try:
        if not os.path.exists('main_app_refactorizado.py'):
            print("❌ main_app_refactorizado.py no encontrado")
            return False
        
        # Leer archivo actual
        with open('main_app_refactorizado.py', 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Crear backup
        with open('main_app_refactorizado_backup_estructura.py', 'w', encoding='utf-8') as f:
            f.write(contenido)
        print("✅ Backup creado: main_app_refactorizado_backup_estructura.py")
        
        # Buscar la función create_widgets
        inicio = contenido.find('    def create_widgets(self):')
        if inicio == -1:
            print("❌ Función create_widgets no encontrada")
            return False
        
        # Buscar el final de la función
        fin = contenido.find('\n    def ', inicio + 1)
        if fin == -1:
            fin = contenido.find('\n\nclass', inicio + 1)
        if fin == -1:
            fin = len(contenido)
        
        # Reemplazar la función completa
        nuevo_contenido = contenido[:inicio] + nueva_estructura + contenido[fin:]
        
        # Escribir archivo corregido
        with open('main_app_refactorizado.py', 'w', encoding='utf-8') as f:
            f.write(nuevo_contenido)
        
        print("✅ Estructura de 3 columnas restaurada exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error restaurando estructura: {e}")
        return False

def crear_version_estructura_corregida():
    """Crea una versión completamente nueva con la estructura correcta"""
    
    try:
        if not os.path.exists('main_app_refactorizado.py'):
            print("❌ main_app_refactorizado.py no encontrado")
            return False
        
        with open('main_app_refactorizado.py', 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Reemplazar la función create_widgets con la estructura correcta
        inicio = contenido.find('    def create_widgets(self):')
        if inicio == -1:
            return False
        
        fin = contenido.find('\n    def ', inicio + 1)
        if fin == -1:
            fin = contenido.find('\n\nclass', inicio + 1)
        if fin == -1:
            fin = len(contenido)
        
        nueva_estructura = '''    def create_widgets(self):
        """Crear la interfaz principal con estructura original de 3 columnas"""
        # Frame principal
        crm_main_frame = ttk.Frame(self.root, padding="10")
        crm_main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configuración de columnas principales del CRM (ESTRUCTURA ORIGINAL)
        crm_main_frame.rowconfigure(0, weight=1)
        crm_main_frame.columnconfigure(0, weight=0, minsize=280)  # Clientes
        crm_main_frame.columnconfigure(1, weight=0, minsize=320)  # Casos/Audiencias
        crm_main_frame.columnconfigure(2, weight=2)  # Notebook (expansible)

        # --- Columna 0: Clientes ---
        self.col1_frame = ttk.Frame(crm_main_frame)
        self.col1_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 5), pady=5)
        self.col1_frame.rowconfigure(0, weight=1)
        self.col1_frame.columnconfigure(0, weight=1)

        self.clientes_frame = ttk.LabelFrame(self.col1_frame, text="Gestión de Clientes", padding="5")
        self.clientes_frame.grid(row=0, column=0, sticky='nsew')
        self.clientes_frame.columnconfigure(0, weight=1)
        self.clientes_frame.rowconfigure(0, weight=1)

        # --- Columna 1: Casos y Audiencias ---
        self.col2_frame = ttk.Frame(crm_main_frame)
        self.col2_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        self.col2_frame.rowconfigure(0, weight=1)  # Casos
        self.col2_frame.rowconfigure(1, weight=1)  # Audiencias
        self.col2_frame.columnconfigure(0, weight=1)

        self.casos_frame = ttk.LabelFrame(self.col2_frame, text="Gestión de Casos", padding="5")
        self.casos_frame.grid(row=0, column=0, sticky='nsew', pady=(0, 5))
        self.casos_frame.columnconfigure(0, weight=1)
        self.casos_frame.rowconfigure(0, weight=1)

        self.audiencias_frame = ttk.LabelFrame(self.col2_frame, text="Audiencias", padding="5")
        self.audiencias_frame.grid(row=1, column=0, sticky='nsew', pady=(5, 0))
        self.audiencias_frame.columnconfigure(0, weight=1)
        self.audiencias_frame.rowconfigure(0, weight=1)

        # --- Columna 2: Notebook ---
        self.col3_frame = ttk.Frame(crm_main_frame)
        self.col3_frame.grid(row=0, column=2, sticky='nsew', padx=(5, 0), pady=5)
        self.col3_frame.rowconfigure(0, weight=1)
        self.col3_frame.columnconfigure(0, weight=1)

        self.main_notebook = ttk.Notebook(self.col3_frame)
        self.main_notebook.grid(row=0, column=0, sticky='nsew')

        # Crear pestañas
        self.create_notebook_tabs()'''
        
        nuevo_contenido = contenido[:inicio] + nueva_estructura + contenido[fin:]
        
        with open('main_app_estructura_corregida.py', 'w', encoding='utf-8') as f:
            f.write(nuevo_contenido)
        
        print("✅ Versión con estructura corregida creada: main_app_estructura_corregida.py")
        return True
        
    except Exception as e:
        print(f"❌ Error creando versión corregida: {e}")
        return False

def main():
    """Función principal"""
    print("🔧 RESTAURANDO ESTRUCTURA ORIGINAL DE 3 COLUMNAS")
    print("=" * 60)
    print("Cambiando de 2 columnas problemáticas a 3 columnas funcionales...\n")
    
    # Opción 1: Restaurar estructura en archivo actual
    print("1. Restaurando estructura en main_app_refactorizado.py...")
    exito1 = restaurar_estructura_3_columnas()
    
    # Opción 2: Crear versión corregida
    print("\n2. Creando versión con estructura completamente corregida...")
    exito2 = crear_version_estructura_corregida()
    
    if exito1:
        print("\n🎉 ESTRUCTURA RESTAURADA EXITOSAMENTE")
        print("=" * 50)
        print("✅ Columna 0: Gestión de Clientes (ancho fijo 280px)")
        print("✅ Columna 1: Gestión de Casos + Audiencias (ancho fijo 320px)")  
        print("✅ Columna 2: Pestañas (expansible)")
        
        print("\n📋 BENEFICIOS DE LA ESTRUCTURA ORIGINAL:")
        print("   • Cada sección tiene espacio dedicado apropiado")
        print("   • Clientes visibles en su propia columna")
        print("   • Casos y audiencias bien organizados")
        print("   • Pestañas con espacio expansible")
        print("   • Layout balanceado y funcional")
        
        print("\n🚀 INSTRUCCIONES:")
        print("1. Ejecuta: python main_app_refactorizado.py")
        print("2. Verifica que se vean los 28 clientes en la columna izquierda")
        print("3. Si hay problemas, usa: python main_app_estructura_corregida.py")
        
    else:
        print("\n❌ Error restaurando estructura")
        print("Verifica que main_app_refactorizado.py existe")

if __name__ == "__main__":
    main()
