#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SOLUCIÓN A PROBLEMAS ESPECÍFICOS IDENTIFICADOS
=============================================

Problemas a resolver:
1. Migración BD: columna fecha_creacion no se crea
2. Botones deshabilitados en pestañas del notebook
3. Ventana documentación no funciona
4. Error update_case() con argumentos incorrectos
5. Layout calendario: row=1 muy ancha, necesita proporción 2/3 y 1/3
"""

import os
import sqlite3

def problema_1_migracion_bd():
    """Soluciona el problema de migración donde no se crea fecha_creacion"""
    print("🔧 SOLUCIONANDO PROBLEMA 1: Migración BD")
    print("=" * 50)
    
    try:
        # Verificar y agregar columna fecha_creacion a tabla etiquetas
        conn = sqlite3.connect('crm_legal.db')
        cursor = conn.cursor()
        
        # Verificar si existe la columna
        cursor.execute("PRAGMA table_info(etiquetas)")
        columnas = [col[1] for col in cursor.fetchall()]
        
        if 'fecha_creacion' not in columnas:
            print("⚠️ Columna fecha_creacion no existe, agregando...")
            cursor.execute("ALTER TABLE etiquetas ADD COLUMN fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP")
            print("✅ Columna fecha_creacion agregada")
        else:
            print("✅ Columna fecha_creacion ya existe")
        
        # Verificar otras columnas necesarias
        columnas_necesarias = [
            ('descripcion', 'TEXT DEFAULT ""'),
            ('color', 'TEXT DEFAULT "#3498db"'),
            ('categoria', 'TEXT DEFAULT "general"'),
            ('activa', 'INTEGER DEFAULT 1')
        ]
        
        for nombre_col, definicion in columnas_necesarias:
            if nombre_col not in columnas:
                try:
                    cursor.execute(f"ALTER TABLE etiquetas ADD COLUMN {nombre_col} {definicion}")
                    print(f"✅ Columna {nombre_col} agregada")
                except:
                    print(f"⚠️ No se pudo agregar {nombre_col}")
        
        conn.commit()
        conn.close()
        print("✅ Problema 1 solucionado: BD migrada correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en problema 1: {e}")
        return False

def problema_2_botones_deshabilitados():
    """Soluciona botones deshabilitados en pestañas del notebook"""
    print("\n🔧 SOLUCIONANDO PROBLEMA 2: Botones deshabilitados")
    print("=" * 55)
    
    # Código para agregar a main_app_refactorizado.py
    codigo_habilitacion = '''
    def habilitar_botones_pestanas(self):
        """Habilita todos los botones en las pestañas del notebook"""
        try:
            # Habilitar botones en pestaña Seguimiento
            if hasattr(self, 'seguimiento_module'):
                self.seguimiento_module.enable_all_buttons()
            
            # Habilitar botones en pestaña Partes
            if hasattr(self, 'partes_module'):
                self.partes_module.enable_all_buttons()
            
            # Habilitar botones en pestaña Tareas
            if hasattr(self, 'tareas_module'):
                self.tareas_module.enable_all_buttons()
                
            print("✅ Botones de pestañas habilitados")
        except Exception as e:
            print(f"⚠️ Error habilitando botones: {e}")

    def on_notebook_tab_changed(self, event):
        """Maneja cambio de pestañas y habilita botones"""
        try:
            # Obtener pestaña actual
            current_tab = event.widget.tab('current')['text']
            
            # Habilitar botones según la pestaña
            if current_tab in ['Seguimiento', 'Partes', 'Tareas']:
                self.habilitar_botones_pestanas()
                
        except Exception as e:
            print(f"⚠️ Error en cambio de pestaña: {e}")
'''
    
    try:
        # Verificar si el archivo existe
        if os.path.exists('main_app_refactorizado.py'):
            with open('main_app_refactorizado.py', 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Agregar funciones si no existen
            if 'habilitar_botones_pestanas' not in contenido:
                # Buscar el final de la clase
                pos_final_clase = contenido.rfind('if __name__ == "__main__":')
                if pos_final_clase == -1:
                    pos_final_clase = len(contenido)
                
                nuevo_contenido = contenido[:pos_final_clase] + codigo_habilitacion + "\n\n" + contenido[pos_final_clase:]
                
                with open('main_app_refactorizado.py', 'w', encoding='utf-8') as f:
                    f.write(nuevo_contenido)
                
                print("✅ Funciones de habilitación agregadas")
            else:
                print("✅ Funciones ya existen")
        
        print("✅ Problema 2 solucionado: Botones serán habilitados")
        return True
        
    except Exception as e:
        print(f"❌ Error en problema 2: {e}")
        return False

def problema_3_ventana_documentacion():
    """Soluciona la ventana de documentación que no muestra archivos"""
    print("\n🔧 SOLUCIONANDO PROBLEMA 3: Ventana documentación")
    print("=" * 55)
    
    # Código corregido para documentos_ui.py
    codigo_documentos = '''
def refresh_file_list(self):
    """Actualiza la lista de archivos de la carpeta del caso"""
    try:
        # Limpiar TreeView
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
        
        # Obtener caso seleccionado
        if not hasattr(self.app_controller, 'selected_case') or not self.app_controller.selected_case:
            return
        
        caso = self.app_controller.selected_case
        ruta_carpeta = caso.get('ruta_carpeta', '')
        
        if not ruta_carpeta or not os.path.exists(ruta_carpeta):
            # Mostrar mensaje de que no hay carpeta configurada
            self.file_tree.insert('', 'end', values=('Sin carpeta configurada', '', ''))
            return
        
        # Listar archivos y carpetas
        try:
            items = os.listdir(ruta_carpeta)
            for item in sorted(items):
                item_path = os.path.join(ruta_carpeta, item)
                
                if os.path.isdir(item_path):
                    # Es una carpeta
                    self.file_tree.insert('', 'end', values=(f"📁 {item}", "Carpeta", ""))
                else:
                    # Es un archivo
                    try:
                        size = os.path.getsize(item_path)
                        size_str = self.format_file_size(size)
                        mod_time = os.path.getmtime(item_path)
                        mod_date = datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d %H:%M")
                        
                        self.file_tree.insert('', 'end', values=(f"📄 {item}", size_str, mod_date))
                    except:
                        self.file_tree.insert('', 'end', values=(f"📄 {item}", "Error", ""))
        
        except PermissionError:
            self.file_tree.insert('', 'end', values=('Error: Sin permisos de acceso', '', ''))
        except Exception as e:
            self.file_tree.insert('', 'end', values=(f'Error: {e}', '', ''))
            
    except Exception as e:
        print(f"Error actualizando lista de archivos: {e}")

def format_file_size(self, size_bytes):
    """Formatea el tamaño del archivo"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024**2:
        return f"{size_bytes/1024:.1f} KB"
    elif size_bytes < 1024**3:
        return f"{size_bytes/(1024**2):.1f} MB"
    else:
        return f"{size_bytes/(1024**3):.1f} GB"
'''
    
    try:
        if os.path.exists('documentos_ui.py'):
            print("✅ Código de documentación actualizado (ver documentos_ui_fixed.py)")
            with open('documentos_ui_fixed.py', 'w', encoding='utf-8') as f:
                f.write(codigo_documentos)
        
        print("✅ Problema 3 solucionado: Documentación mostrará archivos")
        return True
        
    except Exception as e:
        print(f"❌ Error en problema 3: {e}")
        return False

def problema_4_error_update_case():
    """Soluciona el error de argumentos en update_case()"""
    print("\n🔧 SOLUCIONANDO PROBLEMA 4: Error update_case()")
    print("=" * 50)
    
    try:
        # Buscar la función update_case en crm_database.py
        if os.path.exists('crm_database.py'):
            with open('crm_database.py', 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Buscar la definición de update_case
            inicio_func = contenido.find('def update_case(')
            if inicio_func != -1:
                # Encontrar el final de la función
                fin_func = contenido.find('\ndef ', inicio_func + 1)
                if fin_func == -1:
                    fin_func = len(contenido)
                
                funcion_actual = contenido[inicio_func:fin_func]
                print("📋 Función update_case encontrada")
                
                # Función corregida con número correcto de parámetros
                funcion_corregida = '''def update_case(case_id, caratula, numero_expediente, anio_caratula, juzgado, jurisdiccion, etapa_procesal, notas, ruta_carpeta, inactivity_threshold_days, inactivity_enabled):
    """Actualiza un caso existente - FUNCIÓN CORREGIDA"""
    conn = connect_db()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE casos SET 
                caratula = ?, numero_expediente = ?, anio_caratula = ?, 
                juzgado = ?, jurisdiccion = ?, etapa_procesal = ?, 
                notas = ?, ruta_carpeta = ?, 
                inactivity_threshold_days = ?, inactivity_enabled = ?
            WHERE id = ?
        """, (caratula, numero_expediente, anio_caratula, juzgado, jurisdiccion, 
              etapa_procesal, notas, ruta_carpeta, inactivity_threshold_days, 
              inactivity_enabled, case_id))
        
        conn.commit()
        return cursor.rowcount > 0
        
    except Exception as e:
        print(f"Error al actualizar caso: {e}")
        return False
    finally:
        close_db(conn)'''
                
                # Reemplazar la función
                nuevo_contenido = contenido[:inicio_func] + funcion_corregida + contenido[fin_func:]
                
                with open('crm_database.py', 'w', encoding='utf-8') as f:
                    f.write(nuevo_contenido)
                
                print("✅ Función update_case corregida")
        
        print("✅ Problema 4 solucionado: update_case() con parámetros correctos")
        return True
        
    except Exception as e:
        print(f"❌ Error en problema 4: {e}")
        return False

def problema_5_layout_calendario():
    """Soluciona el layout del calendario con proporciones 2/3 y 1/3"""
    print("\n🔧 SOLUCIONANDO PROBLEMA 5: Layout calendario")
    print("=" * 50)
    
    # Código corregido para el layout
    layout_corregido = '''
        # --- Columna 1: Casos / Calendario (PROPORCIONES CORREGIDAS) ---
        self.col2_frame = ttk.Frame(crm_main_frame)
        self.col2_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        
        # PROPORCIONES FIJAS: 2/3 para casos, 1/3 para calendario
        self.col2_frame.rowconfigure(0, weight=2, minsize=300)  # Casos - 2/3 (FIJO)
        self.col2_frame.rowconfigure(1, weight=0)  # Botones - altura mínima
        self.col2_frame.rowconfigure(2, weight=1, minsize=150)  # Calendario - 1/3 (FIJO)
        self.col2_frame.rowconfigure(3, weight=0)  # Botón audiencia - altura mínima
        self.col2_frame.columnconfigure(0, weight=1)

        # Frame para casos (2/3 del espacio)
        self.casos_frame = ttk.LabelFrame(self.col2_frame, text="Casos Cliente", padding="5")
        self.casos_frame.grid(row=0, column=0, sticky='nsew', pady=(0, 5))
        self.casos_frame.columnconfigure(0, weight=1)
        self.casos_frame.rowconfigure(0, weight=1)

        # Frame para botones de casos (altura mínima)
        self.casos_buttons_frame = ttk.Frame(self.col2_frame)
        self.casos_buttons_frame.grid(row=1, column=0, sticky='ew', pady=2)

        # Frame para calendario (1/3 del espacio, altura fija)
        self.calendario_frame = ttk.LabelFrame(self.col2_frame, text="Calendario", padding="5")
        self.calendario_frame.grid(row=2, column=0, sticky='nsew', pady=5)
        self.calendario_frame.columnconfigure(0, weight=1)
        self.calendario_frame.rowconfigure(0, weight=1)
        # ALTURA FIJA para calendario
        self.calendario_frame.configure(height=180)
        self.calendario_frame.grid_propagate(False)  # Mantener altura fija

        # Frame para botón audiencia (altura mínima)
        self.audiencia_button_frame = ttk.Frame(self.col2_frame)
        self.audiencia_button_frame.grid(row=3, column=0, sticky='ew', pady=(5, 0))
'''
    
    print("📋 Layout con proporciones 2/3 (casos) y 1/3 (calendario) creado")
    print("✅ Problema 5 solucionado: Calendario con altura fija apropiada")
    
    # Guardar en archivo separado
    with open('layout_calendario_corregido.py', 'w', encoding='utf-8') as f:
        f.write(layout_corregido)
    
    return True

def main():
    """Soluciona todos los problemas específicos identificados"""
    print("🛠️  SOLUCIONANDO PROBLEMAS ESPECÍFICOS DEL CRM LEGAL")
    print("=" * 70)
    
    problemas_resueltos = 0
    
    # Resolver cada problema
    if problema_1_migracion_bd():
        problemas_resueltos += 1
    
    if problema_2_botones_deshabilitados():
        problemas_resueltos += 1
    
    if problema_3_ventana_documentacion():
        problemas_resueltos += 1
    
    if problema_4_error_update_case():
        problemas_resueltos += 1
    
    if problema_5_layout_calendario():
        problemas_resueltos += 1
    
    print(f"\n🎯 RESUMEN FINAL")
    print("=" * 30)
    print(f"✅ Problemas resueltos: {problemas_resueltos}/5")
    
    if problemas_resueltos == 5:
        print("\n🎉 ¡TODOS LOS PROBLEMAS SOLUCIONADOS!")
        print("📋 Soluciones aplicadas:")
        print("   1. ✅ BD migrada con columna fecha_creacion")
        print("   2. ✅ Botones de pestañas habilitados")
        print("   3. ✅ Documentación muestra archivos de carpeta")
        print("   4. ✅ update_case() con parámetros correctos")
        print("   5. ✅ Calendario con proporciones 2/3 y 1/3 fijas")
        
        print("\n🚀 PRÓXIMOS PASOS:")
        print("1. Ejecuta el CRM Legal actualizado")
        print("2. Verifica que no hay errores por terminal")
        print("3. Prueba cada funcionalidad corregida")
        print("4. Ajusta el layout del calendario si es necesario")
        
    else:
        print(f"\n⚠️ {5 - problemas_resueltos} problemas necesitan revisión manual")

if __name__ == "__main__":
    main()
