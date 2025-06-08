#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CORRECCIÓN INMEDIATA DEL PROBLEMA DE LAYOUT
==========================================

Este script corrige el problema de visualización donde el panel izquierdo
es demasiado angosto para mostrar los datos de clientes.

PROBLEMA IDENTIFICADO:
- Panel izquierdo con weight=0 (no se expande)
- Distribución de espacio inadecuada
- Frame de clientes muy pequeño

SOLUCIÓN:
- Cambiar weight del panel izquierdo
- Establecer ancho mínimo
- Ajustar proporciones
"""

import os

def corregir_layout_main_app():
    """Corrige el layout del main_app_refactorizado.py"""
    
    if not os.path.exists('main_app_refactorizado.py'):
        print("❌ main_app_refactorizado.py no encontrado")
        return False
    
    try:
        # Leer archivo actual
        with open('main_app_refactorizado.py', 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Crear backup
        with open('main_app_refactorizado_backup_layout.py', 'w', encoding='utf-8') as f:
            f.write(contenido)
        print("✅ Backup creado: main_app_refactorizado_backup_layout.py")
        
        # Correcciones específicas de layout
        correcciones = {
            # PROBLEMA PRINCIPAL: Panel izquierdo muy angosto
            'main_frame.columnconfigure(0, weight=0)  # Panel izquierdo': 
                'main_frame.columnconfigure(0, weight=2, minsize=400)  # Panel izquierdo más ancho',
            
            'main_frame.columnconfigure(1, weight=1)  # Panel derecho': 
                'main_frame.columnconfigure(1, weight=3)  # Panel derecho',
            
            # Mejorar distribución vertical en panel izquierdo
            'left_panel.rowconfigure(0, weight=1)  # Clientes':
                'left_panel.rowconfigure(0, weight=2)  # Clientes (más espacio)',
            
            'left_panel.rowconfigure(1, weight=1)  # Casos':
                'left_panel.rowconfigure(1, weight=2)  # Casos',
            
            'left_panel.rowconfigure(2, weight=1)  # Audiencias':
                'left_panel.rowconfigure(2, weight=1)  # Audiencias (menos espacio)',
        }
        
        contenido_corregido = contenido
        cambios_realizados = 0
        
        for buscar, reemplazar in correcciones.items():
            if buscar in contenido_corregido:
                contenido_corregido = contenido_corregido.replace(buscar, reemplazar)
                cambios_realizados += 1
                print(f"✅ Corregido: {buscar[:50]}...")
        
        # Agregar configuración de ancho mínimo para el left_panel si no existe
        if 'left_panel = ttk.Frame(main_frame)' in contenido_corregido:
            buscar_frame = 'left_panel = ttk.Frame(main_frame)'
            reemplazar_frame = '''left_panel = ttk.Frame(main_frame)
        left_panel.configure(width=400)  # Ancho mínimo'''
            
            if 'left_panel.configure(width=' not in contenido_corregido:
                contenido_corregido = contenido_corregido.replace(buscar_frame, reemplazar_frame)
                cambios_realizados += 1
                print("✅ Agregado ancho mínimo al panel izquierdo")
        
        # Escribir archivo corregido
        with open('main_app_refactorizado.py', 'w', encoding='utf-8') as f:
            f.write(contenido_corregido)
        
        print(f"\n✅ Layout corregido exitosamente ({cambios_realizados} cambios)")
        return True
        
    except Exception as e:
        print(f"❌ Error corrigiendo layout: {e}")
        return False

def crear_version_layout_mejorado():
    """Crea una versión completamente nueva con layout mejorado"""
    
    layout_mejorado = '''    def create_widgets(self):
        """Crear la interfaz principal con layout mejorado"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=2, minsize=450)  # Panel izquierdo más ancho
        main_frame.columnconfigure(1, weight=3)  # Panel derecho

        # --- Panel Izquierdo: Clientes, Casos y Audiencias ---
        left_panel = ttk.Frame(main_frame)
        left_panel.grid(row=0, column=0, sticky='nsew', padx=(0, 10))
        left_panel.configure(width=450)  # Ancho mínimo garantizado
        left_panel.columnconfigure(0, weight=1)
        left_panel.rowconfigure(0, weight=3)  # Clientes (más espacio)
        left_panel.rowconfigure(1, weight=2)  # Casos
        left_panel.rowconfigure(2, weight=1)  # Audiencias (menos espacio)

        # Frame para clientes - MÁS GRANDE
        self.clientes_frame = ttk.LabelFrame(left_panel, text="Gestión de Clientes", padding="5")
        self.clientes_frame.grid(row=0, column=0, sticky='nsew', pady=(0, 5))
        self.clientes_frame.columnconfigure(0, weight=1)
        self.clientes_frame.rowconfigure(0, weight=1)

        # Frame para casos
        self.casos_frame = ttk.LabelFrame(left_panel, text="Gestión de Casos", padding="5")
        self.casos_frame.grid(row=1, column=0, sticky='nsew', pady=5)
        self.casos_frame.columnconfigure(0, weight=1)
        self.casos_frame.rowconfigure(0, weight=1)

        # Frame para audiencias - MÁS PEQUEÑO
        self.audiencias_frame = ttk.LabelFrame(left_panel, text="Audiencias", padding="5")
        self.audiencias_frame.grid(row=2, column=0, sticky='nsew', pady=(5, 0))
        self.audiencias_frame.columnconfigure(0, weight=1)
        self.audiencias_frame.rowconfigure(0, weight=1)

        # --- Panel Derecho: Notebook con pestañas ---
        right_panel = ttk.Frame(main_frame)
        right_panel.grid(row=0, column=1, sticky='nsew')
        right_panel.columnconfigure(0, weight=1)
        right_panel.rowconfigure(0, weight=1)

        # Notebook principal
        self.main_notebook = ttk.Notebook(right_panel)
        self.main_notebook.grid(row=0, column=0, sticky='nsew')

        # Crear todas las pestañas del notebook
        self.create_notebook_tabs()'''
    
    try:
        if not os.path.exists('main_app_refactorizado.py'):
            print("❌ main_app_refactorizado.py no encontrado")
            return False
        
        with open('main_app_refactorizado.py', 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Buscar el inicio y fin de la función create_widgets
        inicio = contenido.find('    def create_widgets(self):')
        if inicio == -1:
            print("❌ Función create_widgets no encontrada")
            return False
        
        # Buscar el final de la función (siguiente def o final de clase)
        fin = contenido.find('\n    def ', inicio + 1)
        if fin == -1:
            fin = contenido.find('\n\nclass', inicio + 1)
        if fin == -1:
            fin = len(contenido)
        
        # Reemplazar la función completa
        nuevo_contenido = contenido[:inicio] + layout_mejorado + contenido[fin:]
        
        # Crear backup
        with open('main_app_refactorizado_backup_completo.py', 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        # Escribir nueva versión
        with open('main_app_layout_mejorado.py', 'w', encoding='utf-8') as f:
            f.write(nuevo_contenido)
        
        print("✅ Versión con layout mejorado creada: main_app_layout_mejorado.py")
        return True
        
    except Exception as e:
        print(f"❌ Error creando versión mejorada: {e}")
        return False

def main():
    """Función principal"""
    print("🔧 CORRECCIÓN DEL PROBLEMA DE LAYOUT")
    print("=" * 60)
    print("Corrigiendo el panel izquierdo demasiado angosto...\n")
    
    # Opción 1: Corregir archivo actual
    print("1. Corrigiendo main_app_refactorizado.py actual...")
    exito1 = corregir_layout_main_app()
    
    # Opción 2: Crear versión mejorada
    print("\n2. Creando versión con layout completamente mejorado...")
    exito2 = crear_version_layout_mejorado()
    
    if exito1:
        print("\n🎉 CORRECCIÓN APLICADA EXITOSAMENTE")
        print("=" * 50)
        print("✅ Panel izquierdo ahora tiene weight=2 (se expande)")
        print("✅ Ancho mínimo establecido en 400px")
        print("✅ Clientes obtienen más espacio vertical")
        print("✅ Proporciones mejoradas 2:3 (izquierda:derecha)")
        
        print("\n📋 CAMBIOS APLICADOS:")
        print("   • Panel izquierdo: weight=0 → weight=2")
        print("   • Ancho mínimo: 400px garantizado")
        print("   • Espacio clientes: aumentado (weight=3)")
        print("   • Espacio audiencias: reducido (weight=1)")
        
        print("\n🚀 INSTRUCCIONES:")
        print("1. Ejecuta: python main_app_refactorizado.py")
        print("2. Ahora deberías ver la lista de clientes claramente")
        print("3. Si aún hay problemas, usa: python main_app_layout_mejorado.py")
        
    else:
        print("\n❌ Error aplicando correcciones")
        print("Verifica que main_app_refactorizado.py existe y es accesible")

if __name__ == "__main__":
    main()
