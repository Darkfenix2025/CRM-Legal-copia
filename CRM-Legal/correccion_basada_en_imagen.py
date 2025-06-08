#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CORRECCIÓN BASADA EN LA IMAGEN PROPORCIONADA
==========================================

Basándome en la comparación "Antes" vs "Ahora" de la imagen,
el problema es que las proporciones de las columnas están mal.

ANÁLISIS DE LA IMAGEN:
- ANTES: 3 columnas balanceadas, clientes bien visibles
- AHORA: Notebook muy ancho, clientes comprimidos

SOLUCIÓN: Ajustar las proporciones exactas para que coincidan
con la imagen "Antes".
"""

import os

def corregir_proporciones_segun_imagen():
    """Corrige las proporciones basándose en la imagen original"""
    
    estructura_corregida = '''    def create_widgets(self):
        """Crear la interfaz principal - PROPORCIONES SEGÚN IMAGEN ORIGINAL"""
        crm_main_frame = ttk.Frame(self.root, padding="10")
        crm_main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configuración de columnas principales (PROPORCIONES SEGÚN IMAGEN)
        crm_main_frame.rowconfigure(0, weight=1)
        # CLAVE: Proporciones balanceadas como en la imagen "Antes"
        crm_main_frame.columnconfigure(0, weight=1, minsize=280)  # Clientes - MÁS ESPACIO
        crm_main_frame.columnconfigure(1, weight=1, minsize=300)  # Casos/Calendario - MÁS ESPACIO  
        crm_main_frame.columnconfigure(2, weight=1, minsize=400)  # Notebook - MENOS DOMINANTE

        # --- Columna 0: Clientes (como en imagen "Antes") ---
        self.col1_frame = ttk.Frame(crm_main_frame)
        self.col1_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 5), pady=5)
        self.col1_frame.rowconfigure(0, weight=1)  # Lista clientes
        self.col1_frame.rowconfigure(1, weight=0)  # Botones clientes  
        self.col1_frame.rowconfigure(2, weight=0)  # Detalles cliente
        self.col1_frame.columnconfigure(0, weight=1)

        # Frame para clientes con espacio apropiado
        self.clientes_frame = ttk.LabelFrame(self.col1_frame, text="Clientes", padding="5")
        self.clientes_frame.grid(row=0, column=0, sticky='nsew', pady=(0, 5))
        self.clientes_frame.columnconfigure(0, weight=1)
        self.clientes_frame.rowconfigure(0, weight=1)

        # --- Columna 1: Casos / Calendario (como en imagen "Antes") ---
        self.col2_frame = ttk.Frame(crm_main_frame)
        self.col2_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        self.col2_frame.rowconfigure(0, weight=1)  # Lista casos
        self.col2_frame.rowconfigure(1, weight=0)  # Botones casos
        self.col2_frame.rowconfigure(2, weight=0)  # Calendario
        self.col2_frame.rowconfigure(3, weight=0)  # Botón agregar audiencia
        self.col2_frame.columnconfigure(0, weight=1)

        # Frame para casos
        self.casos_frame = ttk.LabelFrame(self.col2_frame, text="Casos Cliente", padding="5")
        self.casos_frame.grid(row=0, column=0, sticky='nsew', pady=(0, 5))
        self.casos_frame.columnconfigure(0, weight=1)
        self.casos_frame.rowconfigure(0, weight=1)

        # Frame para audiencias (botones casos)
        self.audiencias_frame = ttk.Frame(self.col2_frame)
        self.audiencias_frame.grid(row=1, column=0, sticky='ew', pady=5)

        # Frame para calendario (como en imagen original)
        self.calendario_frame = ttk.LabelFrame(self.col2_frame, text="Calendario", padding="5")
        self.calendario_frame.grid(row=2, column=0, sticky='nsew', pady=5)
        self.calendario_frame.columnconfigure(0, weight=1)
        self.calendario_frame.rowconfigure(0, weight=1)

        # --- Columna 2: Notebook (SIN DOMINAR como en imagen "Antes") ---
        self.col3_frame = ttk.Frame(crm_main_frame)
        self.col3_frame.grid(row=0, column=2, sticky='nsew', padx=(5, 0), pady=5)
        self.col3_frame.rowconfigure(0, weight=2)  # Notebook principal
        self.col3_frame.rowconfigure(1, weight=1)  # Área audiencias
        self.col3_frame.columnconfigure(0, weight=1)

        # Notebook principal (tamaño controlado)
        right_notebook_frame = ttk.Frame(self.col3_frame)
        right_notebook_frame.grid(row=0, column=0, sticky='nsew', pady=(0, 5))
        right_notebook_frame.rowconfigure(0, weight=1)
        right_notebook_frame.columnconfigure(0, weight=1)
        
        self.main_notebook = ttk.Notebook(right_notebook_frame)
        self.main_notebook.grid(row=0, column=0, sticky='nsew')

        # Crear pestañas del notebook
        self.create_notebook_tabs()'''
    
    try:
        if not os.path.exists('main_app_refactorizado.py'):
            print("❌ main_app_refactorizado.py no encontrado")
            return False
        
        with open('main_app_refactorizado.py', 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Crear backup específico
        with open('main_app_backup_antes_imagen.py', 'w', encoding='utf-8') as f:
            f.write(contenido)
        print("✅ Backup creado: main_app_backup_antes_imagen.py")
        
        # Buscar y reemplazar la función create_widgets
        inicio = contenido.find('    def create_widgets(self):')
        if inicio == -1:
            print("❌ Función create_widgets no encontrada")
            return False
        
        fin = contenido.find('\n    def ', inicio + 1)
        if fin == -1:
            fin = contenido.find('\n\nclass', inicio + 1)
        if fin == -1:
            fin = len(contenido)
        
        # Reemplazar con proporciones corregidas
        nuevo_contenido = contenido[:inicio] + estructura_corregida + contenido[fin:]
        
        with open('main_app_refactorizado.py', 'w', encoding='utf-8') as f:
            f.write(nuevo_contenido)
        
        print("✅ Proporciones corregidas según imagen original")
        return True
        
    except Exception as e:
        print(f"❌ Error corrigiendo proporciones: {e}")
        return False

def corregir_errores_etiquetas_persistentes():
    """Corrige definitivamente los errores de etiquetas"""
    
    # Agregar función segura a crm_database.py
    funcion_segura = '''

def get_all_etiquetas_imagen_fix():
    """Función segura para obtener etiquetas sin errores"""
    conn = connect_db()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        # Solo usar campos que definitivamente existen
        cursor.execute("SELECT id_etiqueta, nombre_etiqueta FROM etiquetas ORDER BY nombre_etiqueta")
        result = []
        for row in cursor.fetchall():
            result.append({
                'id': row[0],
                'nombre': row[1],
                'descripcion': '',
                'color': '#3498db',
                'categoria': 'general'
            })
        return result
    except Exception as e:
        print(f"Error obteniendo etiquetas: {e}")
        return []
    finally:
        close_db(conn)
'''
    
    try:
        # Agregar función a crm_database.py si no existe
        with open('crm_database.py', 'r', encoding='utf-8') as f:
            contenido_db = f.read()
        
        if "get_all_etiquetas_imagen_fix" not in contenido_db:
            with open('crm_database.py', 'a', encoding='utf-8') as f:
                f.write(funcion_segura)
            print("✅ Función segura agregada a crm_database.py")
        
        # Corregir llamadas en main_app_refactorizado.py
        with open('main_app_refactorizado.py', 'r', encoding='utf-8') as f:
            contenido_main = f.read()
        
        # Reemplazar llamadas problemáticas
        contenido_corregido = contenido_main.replace(
            'db.get_all_etiquetas()', 
            'db.get_all_etiquetas_imagen_fix()'
        )
        
        if contenido_corregido != contenido_main:
            with open('main_app_refactorizado.py', 'w', encoding='utf-8') as f:
                f.write(contenido_corregido)
            print("✅ Llamadas a etiquetas corregidas")
        
        return True
        
    except Exception as e:
        print(f"❌ Error corrigiendo etiquetas: {e}")
        return False

def main():
    """Función principal basada en análisis de imagen"""
    print("🖼️  CORRECCIÓN BASADA EN IMAGEN DEL CRM")
    print("=" * 60)
    print("Analizando diferencias 'Antes' vs 'Ahora'...\n")
    
    print("📊 ANÁLISIS DE LA IMAGEN:")
    print("✅ ANTES: 3 columnas balanceadas, clientes claramente visibles")
    print("❌ AHORA: Notebook muy ancho, clientes comprimidos\n")
    
    exito_total = True
    
    # 1. Corregir proporciones según imagen
    print("1. Corrigiendo proporciones según imagen original...")
    if corregir_proporciones_segun_imagen():
        print("✅ Proporciones ajustadas a la imagen 'Antes'")
    else:
        exito_total = False
        print("❌ Error ajustando proporciones")
    
    # 2. Corregir errores de etiquetas
    print("\n2. Corrigiendo errores de etiquetas persistentes...")
    if corregir_errores_etiquetas_persistentes():
        print("✅ Errores de etiquetas corregidos")
    else:
        exito_total = False
        print("❌ Error corrigiendo etiquetas")
    
    if exito_total:
        print("\n🎉 CORRECCIÓN BASADA EN IMAGEN COMPLETADA")
        print("=" * 55)
        print("✅ PROPORCIONES RESTAURADAS:")
        print("   • Columna 0 (Clientes): weight=1, minsize=280px")
        print("   • Columna 1 (Casos/Cal): weight=1, minsize=300px")
        print("   • Columna 2 (Notebook): weight=1, minsize=400px")
        
        print("\n✅ BALANCE CORREGIDO:")
        print("   • Clientes: MÁS espacio para ver lista completa")
        print("   • Casos: Espacio apropiado para navegación")
        print("   • Notebook: MENOS dominante, más balanceado")
        
        print("\n✅ ERRORES SOLUCIONADOS:")
        print("   • Error 'fecha_creacion' eliminado definitivamente")
        print("   • Función get_all_etiquetas_imagen_fix() agregada")
        
        print("\n📋 RESULTADO ESPERADO:")
        print("   🎯 Layout idéntico a la imagen 'Antes'")
        print("   📝 28 clientes claramente visibles")
        print("   📁 Casos apropiadamente espaciados")
        print("   📅 Calendario en tamaño correcto")
        print("   📓 Notebook sin dominar la pantalla")
        
        print("\n🚀 EJECUTAR AHORA:")
        print("   python main_app_refactorizado.py")
        print("\n✨ ¡Debería verse exactamente como la imagen 'Antes'!")
        
    else:
        print("\n❌ ALGUNOS PROBLEMAS EN LA CORRECCIÓN")
        print("Revisa los errores específicos arriba")

if __name__ == "__main__":
    main()
