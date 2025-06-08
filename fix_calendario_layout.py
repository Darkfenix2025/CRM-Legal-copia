#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CORRECCIÓN ESPECÍFICA: LAYOUT DEL CALENDARIO
==========================================

Problema: row=1 del calendario es muy ancha
Solución: Proporción 2/3 para casos y 1/3 para calendario con valores FIJOS

El usuario quiere:
- row=0: 2/3 del total (casos)
- row=1: 1/3 del total (calendario)
- Valores fijos, no variables
"""

import os

def crear_layout_calendario_corregido():
    """Crea el layout corregido para la columna del calendario"""
    
    layout_corregido = '''        # --- Columna 1: Casos / Calendario (LAYOUT CORREGIDO) ---
        self.col2_frame = ttk.Frame(crm_main_frame)
        self.col2_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        
        # CONFIGURACIÓN FIJA DE PROPORCIONES 2/3 y 1/3
        # NO usar weight variable, usar valores FIJOS
        self.col2_frame.rowconfigure(0, weight=0, minsize=400)  # Casos - ALTURA FIJA 2/3
        self.col2_frame.rowconfigure(1, weight=0)  # Botones casos - altura mínima
        self.col2_frame.rowconfigure(2, weight=0, minsize=200)  # Calendario - ALTURA FIJA 1/3
        self.col2_frame.rowconfigure(3, weight=0)  # Botón audiencia - altura mínima
        self.col2_frame.columnconfigure(0, weight=1)
        
        # ALTURA TOTAL FIJA para la columna
        self.col2_frame.configure(height=650)  # Altura total controlada
        self.col2_frame.grid_propagate(False)  # NO permitir que se redimensione

        # Frame para casos (2/3 = ~400px del total 600px)
        self.casos_frame = ttk.LabelFrame(self.col2_frame, text="Casos Cliente", padding="5")
        self.casos_frame.grid(row=0, column=0, sticky='nsew', pady=(0, 5))
        self.casos_frame.configure(height=400)  # ALTURA FIJA
        self.casos_frame.grid_propagate(False)  # Mantener altura fija
        self.casos_frame.columnconfigure(0, weight=1)
        self.casos_frame.rowconfigure(0, weight=1)

        # Frame para botones de casos (altura mínima ~30px)
        self.casos_buttons_frame = ttk.Frame(self.col2_frame)
        self.casos_buttons_frame.grid(row=1, column=0, sticky='ew', pady=2)
        self.casos_buttons_frame.configure(height=30)
        self.casos_buttons_frame.grid_propagate(False)

        # Frame para calendario (1/3 = ~200px del total 600px)
        self.calendario_frame = ttk.LabelFrame(self.col2_frame, text="Calendario", padding="5")
        self.calendario_frame.grid(row=2, column=0, sticky='nsew', pady=5)
        self.calendario_frame.configure(height=200)  # ALTURA FIJA 1/3
        self.calendario_frame.grid_propagate(False)  # Mantener altura fija
        self.calendario_frame.columnconfigure(0, weight=1)
        self.calendario_frame.rowconfigure(0, weight=1)

        # Frame para botón audiencia (altura mínima ~30px)
        self.audiencia_button_frame = ttk.Frame(self.col2_frame)
        self.audiencia_button_frame.grid(row=3, column=0, sticky='ew', pady=(5, 0))
        self.audiencia_button_frame.configure(height=30)
        self.audiencia_button_frame.grid_propagate(False)'''
    
    return layout_corregido

def crear_layout_alternativo_con_pesos():
    """Crea un layout alternativo usando pesos pero de forma más controlada"""
    
    layout_alternativo = '''        # --- Columna 1: Casos / Calendario (LAYOUT ALTERNATIVO) ---
        self.col2_frame = ttk.Frame(crm_main_frame)
        self.col2_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        
        # PROPORCIONES CONTROLADAS: 2 partes casos, 1 parte calendario
        self.col2_frame.rowconfigure(0, weight=2, minsize=350)  # Casos - 2/3 (mínimo 350px)
        self.col2_frame.rowconfigure(1, weight=0, minsize=30)   # Botones - altura fija
        self.col2_frame.rowconfigure(2, weight=1, minsize=180)  # Calendario - 1/3 (mínimo 180px)
        self.col2_frame.rowconfigure(3, weight=0, minsize=30)   # Botón - altura fija
        self.col2_frame.columnconfigure(0, weight=1)

        # Frame para casos (peso 2 = 2/3 del espacio disponible)
        self.casos_frame = ttk.LabelFrame(self.col2_frame, text="Casos Cliente", padding="5")
        self.casos_frame.grid(row=0, column=0, sticky='nsew', pady=(0, 5))
        self.casos_frame.columnconfigure(0, weight=1)
        self.casos_frame.rowconfigure(0, weight=1)

        # Frame para botones de casos
        self.casos_buttons_frame = ttk.Frame(self.col2_frame)
        self.casos_buttons_frame.grid(row=1, column=0, sticky='ew', pady=2)

        # Frame para calendario (peso 1 = 1/3 del espacio disponible)
        self.calendario_frame = ttk.LabelFrame(self.col2_frame, text="Calendario", padding="5")
        self.calendario_frame.grid(row=2, column=0, sticky='nsew', pady=5)
        self.calendario_frame.columnconfigure(0, weight=1)
        self.calendario_frame.rowconfigure(0, weight=1)
        
        # Limitar altura máxima del calendario
        self.calendario_frame.bind('<Configure>', lambda e: self.limitar_altura_calendario())

        # Frame para botón audiencia
        self.audiencia_button_frame = ttk.Frame(self.col2_frame)
        self.audiencia_button_frame.grid(row=3, column=0, sticky='ew', pady=(5, 0))

    def limitar_altura_calendario(self):
        """Limita la altura del calendario para que no sea muy grande"""
        try:
            altura_total = self.col2_frame.winfo_height()
            if altura_total > 100:  # Solo si la ventana ya se renderizó
                altura_calendario = min(200, altura_total // 3)  # Máximo 200px o 1/3
                self.calendario_frame.configure(height=altura_calendario)
        except:
            pass'''
    
    return layout_alternativo

def aplicar_correccion_calendario():
    """Aplica la corrección del layout del calendario"""
    print("🔧 APLICANDO CORRECCIÓN DEL LAYOUT DEL CALENDARIO")
    print("=" * 60)
    
    try:
        # Verificar si existe el archivo
        if not os.path.exists('main_app_refactorizado.py'):
            print("❌ main_app_refactorizado.py no encontrado")
            return False
        
        # Leer archivo actual
        with open('main_app_refactorizado.py', 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Crear backup
        with open('main_app_backup_calendario.py', 'w', encoding='utf-8') as f:
            f.write(contenido)
        print("✅ Backup creado: main_app_backup_calendario.py")
        
        # Buscar la sección de col2_frame (columna del calendario)
        inicio_col2 = contenido.find('# --- Columna 1: Casos / Calendario')
        if inicio_col2 == -1:
            inicio_col2 = contenido.find('self.col2_frame = ttk.Frame(crm_main_frame)')
        
        if inicio_col2 == -1:
            print("❌ No se encontró la sección de col2_frame")
            return False
        
        # Buscar el final de la sección
        fin_col2 = contenido.find('# --- Columna 2:', inicio_col2)
        if fin_col2 == -1:
            fin_col2 = contenido.find('self.col3_frame', inicio_col2)
        
        if fin_col2 == -1:
            print("❌ No se encontró el final de la sección col2_frame")
            return False
        
        # Obtener layout corregido
        layout_nuevo = crear_layout_calendario_corregido()
        
        # Reemplazar la sección
        nuevo_contenido = contenido[:inicio_col2] + layout_nuevo + '\n' + contenido[fin_col2:]
        
        # Escribir archivo corregido
        with open('main_app_refactorizado.py', 'w', encoding='utf-8') as f:
            f.write(nuevo_contenido)
        
        print("✅ Layout del calendario corregido aplicado")
        return True
        
    except Exception as e:
        print(f"❌ Error aplicando corrección: {e}")
        return False

def crear_archivos_de_referencia():
    """Crea archivos de referencia con las diferentes opciones de layout"""
    print("\n📁 CREANDO ARCHIVOS DE REFERENCIA")
    print("=" * 40)
    
    # Layout con alturas fijas
    with open('layout_calendario_fijo.py', 'w', encoding='utf-8') as f:
        f.write(crear_layout_calendario_corregido())
    print("✅ layout_calendario_fijo.py creado")
    
    # Layout con pesos controlados
    with open('layout_calendario_pesos.py', 'w', encoding='utf-8') as f:
        f.write(crear_layout_alternativo_con_pesos())
    print("✅ layout_calendario_pesos.py creado")
    
    # Documentación
    documentacion = '''# OPCIONES DE LAYOUT PARA CALENDARIO

## Opción 1: Alturas Fijas (layout_calendario_fijo.py)
- Casos: 400px fijos (2/3)
- Calendario: 200px fijos (1/3)
- No se redimensiona automáticamente
- Control total sobre las proporciones

## Opción 2: Pesos Controlados (layout_calendario_pesos.py)
- Casos: weight=2 (2/3 del espacio)
- Calendario: weight=1 (1/3 del espacio)
- Se adapta al tamaño de ventana
- Más flexible pero controlado

## Recomendación
Para el problema específico mencionado (row=1 muy ancha),
usar la Opción 1 con alturas fijas es la mejor solución.
'''
    
    with open('README_layout_calendario.md', 'w', encoding='utf-8') as f:
        f.write(documentacion)
    print("✅ README_layout_calendario.md creado")

def main():
    """Función principal para corregir el layout del calendario"""
    print("📅 CORRECCIÓN DEL LAYOUT DEL CALENDARIO")
    print("=" * 60)
    print("Problema: row=1 del calendario muy ancha")
    print("Solución: Proporciones fijas 2/3 casos, 1/3 calendario\n")
    
    # Aplicar corrección
    if aplicar_correccion_calendario():
        print("\n✅ LAYOUT DEL CALENDARIO CORREGIDO")
        print("=" * 40)
        print("🎯 CAMBIOS APLICADOS:")
        print("   • Altura de casos: 400px FIJOS (2/3)")
        print("   • Altura de calendario: 200px FIJOS (1/3)")
        print("   • grid_propagate(False) para mantener tamaños")
        print("   • Altura total de columna controlada")
        
        print("\n📐 PROPORCIONES CORREGIDAS:")
        print("   • Total: 650px de altura")
        print("   • Casos: 400px (61%) - MÁS ESPACIO")
        print("   • Botones: 30px (5%) - mínimo")
        print("   • Calendario: 200px (31%) - CONTROLADO")
        print("   • Botón audiencia: 30px (5%) - mínimo")
        
        print("\n🔧 CÓMO FUNCIONA:")
        print("   • NO usa weight variable")
        print("   • Alturas completamente FIJAS")
        print("   • grid_propagate(False) previene redimensionado")
        print("   • Proporciones 2:1 exactas")
        
        # Crear archivos de referencia
        crear_archivos_de_referencia()
        
        print("\n🚀 PRUEBA AHORA:")
        print("1. Ejecuta: python main_app_refactorizado.py")
        print("2. Observa la columna central (casos/calendario)")
        print("3. El calendario ahora debe ser 1/3 del tamaño")
        print("4. Los casos deben tener 2/3 del espacio")
        
        print("\n📋 SI NECESITAS AJUSTAR:")
        print("• Edita las alturas en las líneas:")
        print("  - casos_frame.configure(height=400)")  
        print("  - calendario_frame.configure(height=200)")
        print("• Mantén la proporción 2:1")
        
    else:
        print("\n❌ Error aplicando corrección del layout")
        print("🔧 Solución manual:")
        print("1. Abre main_app_refactorizado.py")
        print("2. Busca la sección 'col2_frame'")
        print("3. Usa el código en layout_calendario_fijo.py")

if __name__ == "__main__":
    main()
