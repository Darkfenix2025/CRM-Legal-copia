# main_app_refactorizado.py
import tkinter as tk
from tkinter import ttk, messagebox
import crm_database as db
import os
import datetime
import sys
import threading
import webbrowser
from PIL import Image, ImageTk
import plyer
from pystray import MenuItem as item, Icon as icon

# --- Imports de módulos modulares ---
from seguimiento_ui import SeguimientoTab
from partes_ui import PartesTab
from tareas_ui import TareasTab
from clientes_ui import ClientesTab
from casos_ui import CasosTab
from audiencias_ui import AudienciasTab
from documentos_ui import DocumentosTab
from casos_detalles_ui import CasosDetallesTab
from ia_ui import IAMenu
from etiquetas_ui import EtiquetasTab
from financiero_ui import FinancieroTab

# --- Helper para Rutas Relativas (PyInstaller) ---
def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso, funciona para desarrollo y para PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)

class CRMLegalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CRM Legal Local - Gestor Integral v2.0     Powered by Legal-IT-Ø")
        
        # Configurar ventana principal
        try:
            self.root.state('zoomed')
        except tk.TclError:
            print("Advertencia: root.state('zoomed') falló. Intentando alternativa o usando tamaño por defecto.")
            self.root.attributes('-zoomed', True)

        # --- Variables de estado CRM ---
        self.selected_client = None
        self.selected_case = None

        # --- Referencia al módulo de base de datos ---
        self.db_crm = db

        # --- Variables para notificaciones y bandeja ---
        self.recordatorios_mostrados_hoy = set()
        self.logo_image_tk = None
        self.tray_icon = None
        self.hilo_recordatorios = None
        self.hilo_bandeja = None
        self.stop_event = threading.Event()

        # --- Crear barra de menú ---
        self.create_menu()

        # --- Crear widgets principales ---
        self.create_widgets()

        # --- Inicializar módulos ---
        self.initialize_modules()

        # --- Cargar datos iniciales ---
        self.load_initial_data()

        # --- Iniciar hilos para notificaciones y bandeja ---
        self.start_background_threads()

        # --- Manejar cierre de ventana ---
        self.root.protocol("WM_DELETE_WINDOW", self.ocultar_a_bandeja)

    def create_menu(self):
        """Crear la barra de menú"""
        menubar = tk.Menu(self.root)

        # Menú Archivo
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Mostrar Ventana", command=self._mostrar_ventana_callback)
        filemenu.add_separator()
        filemenu.add_command(label="Ocultar a Bandeja", command=self.ocultar_a_bandeja)
        filemenu.add_separator()
        filemenu.add_command(label="Salir (Cerrar Aplicación)", command=self.cerrar_aplicacion_directamente)
        menubar.add_cascade(label="Archivo", menu=filemenu)

        # Menú IA (usando el módulo ia_ui)
        self.ia_menu = IAMenu(menubar, self)

        # Menú Administración
        adminmenu = tk.Menu(menubar, tearoff=0)
        adminmenu.add_command(label="Crear Copia de Seguridad...", command=self.crear_copia_de_seguridad)
        adminmenu.add_command(label="Configuración del Sistema", command=self.open_config_dialog)
        menubar.add_cascade(label="Administración", menu=adminmenu)

        self.root.config(menu=menubar)

    def create_widgets(self):
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
        self.create_notebook_tabs()
    def create_notebook_tabs(self):
        """Crear todas las pestañas del notebook principal"""
        # Pestaña Detalles del Caso
        self.casos_detalles_tab = CasosDetallesTab(self.main_notebook, self)
        self.main_notebook.add(self.casos_detalles_tab, text='Detalles del Caso')

        # Pestaña Documentos
        self.documentos_tab = DocumentosTab(self.main_notebook, self)
        self.main_notebook.add(self.documentos_tab, text='Documentación')

        # Pestaña Tareas/Plazos
        self.tareas_tab = TareasTab(self.main_notebook, self)
        self.main_notebook.add(self.tareas_tab, text="Tareas/Plazos")

        # Pestaña Partes
        self.partes_tab = PartesTab(self.main_notebook, self)
        self.main_notebook.add(self.partes_tab, text="Partes")

        # Pestaña Seguimiento
        self.seguimiento_tab = SeguimientoTab(self.main_notebook, self)
        self.main_notebook.add(self.seguimiento_tab, text="Seguimiento")

        # Pestaña Etiquetas Globales
        self.etiquetas_tab = EtiquetasTab(self.main_notebook, self)
        self.main_notebook.add(self.etiquetas_tab, text="Etiquetas")

        # Pestaña Financiero
        self.financiero_tab = FinancieroTab(self.main_notebook, self)
        self.main_notebook.add(self.financiero_tab, text="Financiero")

    def initialize_modules(self):
        """Inicializar los módulos en los frames correspondientes"""
        # Módulo de Clientes
        self.clientes_module = ClientesTab(self.clientes_frame, self)
        self.clientes_module.pack(fill=tk.BOTH, expand=True)

        # Módulo de Casos
        self.casos_module = CasosTab(self.casos_frame, self)
        self.casos_module.pack(fill=tk.BOTH, expand=True)

        # Módulo de Audiencias
        self.audiencias_module = AudienciasTab(self.audiencias_frame, self)
        self.audiencias_module.pack(fill=tk.BOTH, expand=True)

    def load_initial_data(self):
        """Cargar datos iniciales en todos los módulos"""
        self.clientes_module.load_clients()
        self.audiencias_module.cargar_audiencias_fecha_actual()
        self.audiencias_module.marcar_dias_audiencias_calendario()

    def start_background_threads(self):
        """Iniciar hilos de fondo para notificaciones y bandeja"""
        self.hilo_recordatorios = threading.Thread(target=self.verificar_recordatorios_periodicamente, daemon=True)
        self.hilo_recordatorios.start()

        self.hilo_bandeja = threading.Thread(target=self.setup_tray_icon, daemon=True)
        self.hilo_bandeja.start()

    # --- Métodos de comunicación entre módulos ---

    def on_client_selected(self, client_data):
        """Manejar selección de cliente desde el módulo de clientes"""
        self.selected_client = client_data
        # Cargar casos del cliente seleccionado
        self.casos_module.on_client_changed(client_data)
        
        # Si no hay caso seleccionado, limpiar pestañas
        if not self.selected_case:
            self.on_case_selected(None)

    def on_client_deleted(self):
        """Manejar eliminación de cliente"""
        self.selected_client = None
        self.selected_case = None
        self.casos_module.clear_case_list()
        self.on_case_selected(None)

    def on_case_selected(self, case_data):
        """Manejar selección de caso desde el módulo de casos"""
        self.selected_case = case_data
        
        # Notificar a todas las pestañas sobre el cambio de caso
        tabs_with_case_awareness = [
            self.casos_detalles_tab,
            self.documentos_tab,
            self.tareas_tab,
            self.partes_tab,
            self.seguimiento_tab,
            self.financiero_tab
        ]
        
        for tab in tabs_with_case_awareness:
            if hasattr(tab, 'on_case_changed'):
                tab.on_case_changed(case_data)

        # Habilitar/deshabilitar pestañas según si hay caso seleccionado
        self.enable_detail_tabs_for_case() if case_data else self.disable_detail_tabs_for_case()

    def on_case_deleted(self):
        """Manejar eliminación de caso"""
        self.selected_case = None
        self.on_case_selected(None)

    def on_case_folder_updated(self, case_data):
        """Manejar actualización de carpeta de caso"""
        self.selected_case = case_data
        # Refrescar la pestaña de documentos
        if hasattr(self.documentos_tab, 'on_case_changed'):
            self.documentos_tab.on_case_changed(case_data)

    def enable_detail_tabs_for_case(self):
        """Habilitar pestañas de detalles cuando hay un caso seleccionado"""
        sensitive_tabs = [
            ('Detalles del Caso', self.casos_detalles_tab),
            ('Documentación', self.documentos_tab),
            ('Tareas/Plazos', self.tareas_tab),
            ('Partes', self.partes_tab),
            ('Seguimiento', self.seguimiento_tab),
            ('Financiero', self.financiero_tab)
        ]
        
        for tab_name, tab_widget in sensitive_tabs:
            # Buscar el índice de la pestaña y habilitarla
            for i in range(self.main_notebook.index('end')):
                if self.main_notebook.tab(i, 'text') == tab_name:
                    self.main_notebook.tab(i, state='normal')
                    break

    def disable_detail_tabs_for_case(self):
        """Deshabilitar pestañas de detalles cuando no hay caso seleccionado"""
        sensitive_tabs = [
            'Detalles del Caso',
            'Documentación', 
            'Tareas/Plazos',
            'Partes',
            'Seguimiento',
            'Financiero'
        ]
        
        for tab_name in sensitive_tabs:
            # Buscar el índice de la pestaña y deshabilitarla
            for i in range(self.main_notebook.index('end')):
                if self.main_notebook.tab(i, 'text') == tab_name:
                    self.main_notebook.tab(i, state='disabled')
                    break

    # --- Métodos de configuración y administración ---

    def crear_copia_de_seguridad(self):
        """Crear copia de seguridad de la base de datos"""
        try:
            import shutil
            from tkinter import filedialog
            
            # Seleccionar ubicación para el backup
            backup_filename = f"crm_legal_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            backup_path = filedialog.asksaveasfilename(
                title="Guardar Copia de Seguridad",
                initialfile=backup_filename,
                defaultextension=".db",
                filetypes=[("Base de datos", "*.db"), ("Todos los archivos", "*.*")]
            )
            
            if backup_path:
                # Copiar archivo de base de datos
                shutil.copy2(self.db_crm.DATABASE_FILE, backup_path)
                messagebox.showinfo("Copia de Seguridad", 
                                  f"Copia de seguridad creada exitosamente en:\n{backup_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear copia de seguridad:\n{e}")

    def open_config_dialog(self):
        """Abrir diálogo de configuración del sistema"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Configuración del Sistema")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.geometry("400x300")

        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Información del sistema
        ttk.Label(main_frame, text="CRM Legal v2.0 - Configuración", font=('', 14, 'bold')).pack(pady=(0, 20))

        # Estado de módulos
        ttk.Label(main_frame, text="Estado de Módulos:", font=('', 12, 'bold')).pack(anchor=tk.W)
        
        modules_status = [
            ("✅ Gestión de Clientes", "Operativo"),
            ("✅ Gestión de Casos", "Operativo"),
            ("✅ Sistema de Tareas", "Operativo"),
            ("✅ Gestión de Partes", "Operativo"),
            ("✅ Sistema de Seguimiento", "Operativo"),
            ("✅ Gestión de Audiencias", "Operativo"),
            ("✅ Sistema de Documentos", "Operativo"),
            ("✅ Sistema de Etiquetas", "Operativo"),
            ("✅ Sistema Financiero", "Operativo"),
            ("✅ Asistente de IA", "Disponible" if hasattr(self, 'ia_menu') else "No disponible")
        ]

        for module, status in modules_status:
            ttk.Label(main_frame, text=f"{module}: {status}").pack(anchor=tk.W, pady=1)

        # Botón de cerrar
        ttk.Button(main_frame, text="Cerrar", command=dialog.destroy).pack(pady=20)

    # --- Métodos de notificaciones y bandeja ---

    def verificar_recordatorios_periodicamente(self):
        """Verificar recordatorios de audiencias periódicamente"""
        while not self.stop_event.is_set():
            try:
                self._check_audiencia_reminders()
                self._check_tarea_reminders()
            except Exception as e:
                print(f"Error en verificación de recordatorios: {e}")
            
            # Esperar 5 minutos antes de la próxima verificación
            self.stop_event.wait(300)

    def _check_audiencia_reminders(self):
        """Verificar recordatorios de audiencias"""
        try:
            # Obtener audiencias con recordatorios activos para hoy y mañana
            today = datetime.date.today()
            tomorrow = today + datetime.timedelta(days=1)
            
            # Esta lógica se puede expandir según las necesidades específicas
            audiencias_hoy = self.db_crm.get_audiencias_by_date(today.strftime("%Y-%m-%d"))
            
            for audiencia in audiencias_hoy:
                if audiencia.get('recordatorio_activo') and audiencia['id'] not in self.recordatorios_mostrados_hoy:
                    self.mostrar_recordatorio_audiencia(audiencia)
                    self.recordatorios_mostrados_hoy.add(audiencia['id'])
                    
        except Exception as e:
            print(f"Error verificando recordatorios de audiencias: {e}")

    def _check_tarea_reminders(self):
        """Verificar recordatorios de tareas"""
        try:
            # Lógica para verificar tareas con vencimiento próximo
            # Esto se puede expandir según las necesidades específicas
            pass
        except Exception as e:
            print(f"Error verificando recordatorios de tareas: {e}")

    def mostrar_recordatorio_audiencia(self, audiencia):
        """Mostrar recordatorio de audiencia"""
        try:
            titulo = "Recordatorio de Audiencia"
            mensaje = f"Audiencia programada:\n{audiencia.get('descripcion', 'Sin descripción')}\n"
            mensaje += f"Hora: {audiencia.get('hora', 'Sin hora')}"
            
            # Mostrar notificación nativa
            plyer.notification.notify(
                title=titulo,
                message=mensaje,
                timeout=10
            )
        except Exception as e:
            print(f"Error mostrando recordatorio: {e}")

    def setup_tray_icon(self):
        """Configurar icono de bandeja del sistema"""
        try:
            # Intentar cargar el icono
            icon_path = resource_path("assets/icono.png")
            if os.path.exists(icon_path):
                image = Image.open(icon_path)
            else:
                # Crear un icono simple si no se encuentra el archivo
                image = Image.new('RGB', (64, 64), color='blue')
            
            # Crear menú de la bandeja
            menu = (
                item('Mostrar', self._mostrar_ventana_callback),
                item('Salir', self._salir_app_callback)
            )
            
            # Crear icono de bandeja
            self.tray_icon = icon("CRM Legal", image, menu=menu)
            self.tray_icon.run()
            
        except Exception as e:
            print(f"Error configurando icono de bandeja: {e}")

    def _mostrar_ventana_callback(self, icon=None, item=None):
        """Callback para mostrar ventana desde bandeja"""
        self.root.after(0, self._mostrar_ventana)

    def _mostrar_ventana(self):
        """Mostrar la ventana principal"""
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def _salir_app_callback(self, icon=None, item=None):
        """Callback para salir desde bandeja"""
        self.root.after(0, self.cerrar_aplicacion_directamente)

    def ocultar_a_bandeja(self):
        """Ocultar aplicación a la bandeja del sistema"""
        self.root.withdraw()

    def cerrar_aplicacion_directamente(self):
        """Cerrar la aplicación completamente"""
        self.stop_event.set()
        if self.tray_icon:
            self.tray_icon.stop()
        self.root.quit()
        self.root.destroy()

    # --- Métodos de actualización global ---

    def refresh_all_data(self):
        """Refrescar todos los datos en todos los módulos"""
        modules_to_refresh = [
            self.clientes_module,
            self.casos_module,
            self.audiencias_module,
            self.casos_detalles_tab,
            self.documentos_tab,
            self.tareas_tab,
            self.partes_tab,
            self.seguimiento_tab,
            self.etiquetas_tab,
            self.financiero_tab
        ]
        
        for module in modules_to_refresh:
            if hasattr(module, 'refresh_data'):
                try:
                    module.refresh_data()
                except Exception as e:
                    print(f"Error refrescando módulo {module.__class__.__name__}: {e}")

def main():
    """Función principal para ejecutar la aplicación"""
    root = tk.Tk()
    app = CRMLegalApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
