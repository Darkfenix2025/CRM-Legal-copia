# casos_detalles_ui.py
import tkinter as tk
from tkinter import ttk, messagebox
import datetime

class CasosDetallesTab(ttk.Frame):
    def __init__(self, parent, app_controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.app_controller = app_controller
        self.db_crm = self.app_controller.db_crm
        self.current_case = None
        self._create_widgets()

    def _create_widgets(self):
        # Configurar el frame principal
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Crear canvas y scrollbar para scroll vertical
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        # Configurar el frame scrollable
        self.scrollable_frame.columnconfigure(0, weight=1)

        # --- Frame de Estado ---
        self.status_frame = ttk.LabelFrame(self.scrollable_frame, text="Estado", padding="10")
        self.status_frame.grid(row=0, column=0, sticky='ew', pady=(0, 10))
        self.status_frame.columnconfigure(0, weight=1)

        self.status_label = ttk.Label(self.status_frame, text="Ningún caso seleccionado", 
                                     font=('', 12), foreground='gray')
        self.status_label.pack()

        # --- Información Básica ---
        self.info_frame = ttk.LabelFrame(self.scrollable_frame, text="Información Básica", padding="10")
        self.info_frame.grid(row=1, column=0, sticky='ew', pady=(0, 10))
        self.info_frame.columnconfigure(1, weight=1)

        # ID del Caso
        ttk.Label(self.info_frame, text="ID:", font=('', 9, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=3, padx=(0, 10))
        self.id_label = ttk.Label(self.info_frame, text="")
        self.id_label.grid(row=0, column=1, sticky=tk.EW, pady=3)

        # Carátula
        ttk.Label(self.info_frame, text="Carátula:", font=('', 9, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=3, padx=(0, 10))
        self.caratula_label = ttk.Label(self.info_frame, text="", wraplength=400)
        self.caratula_label.grid(row=1, column=1, sticky=tk.EW, pady=3)

        # Cliente
        ttk.Label(self.info_frame, text="Cliente:", font=('', 9, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=3, padx=(0, 10))
        self.cliente_label = ttk.Label(self.info_frame, text="", wraplength=400)
        self.cliente_label.grid(row=2, column=1, sticky=tk.EW, pady=3)

        # Número de Expediente
        ttk.Label(self.info_frame, text="Nº Expediente:", font=('', 9, 'bold')).grid(row=3, column=0, sticky=tk.W, pady=3, padx=(0, 10))
        self.num_exp_label = ttk.Label(self.info_frame, text="")
        self.num_exp_label.grid(row=3, column=1, sticky=tk.EW, pady=3)

        # Año
        ttk.Label(self.info_frame, text="Año:", font=('', 9, 'bold')).grid(row=4, column=0, sticky=tk.W, pady=3, padx=(0, 10))
        self.anio_label = ttk.Label(self.info_frame, text="")
        self.anio_label.grid(row=4, column=1, sticky=tk.EW, pady=3)

        # --- Información Jurisdiccional ---
        self.juris_frame = ttk.LabelFrame(self.scrollable_frame, text="Información Jurisdiccional", padding="10")
        self.juris_frame.grid(row=2, column=0, sticky='ew', pady=(0, 10))
        self.juris_frame.columnconfigure(1, weight=1)

        # Juzgado
        ttk.Label(self.juris_frame, text="Juzgado:", font=('', 9, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=3, padx=(0, 10))
        self.juzgado_label = ttk.Label(self.juris_frame, text="", wraplength=400)
        self.juzgado_label.grid(row=0, column=1, sticky=tk.EW, pady=3)

        # Jurisdicción
        ttk.Label(self.juris_frame, text="Jurisdicción:", font=('', 9, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=3, padx=(0, 10))
        self.jurisdiccion_label = ttk.Label(self.juris_frame, text="", wraplength=400)
        self.jurisdiccion_label.grid(row=1, column=1, sticky=tk.EW, pady=3)

        # Etapa Procesal
        ttk.Label(self.juris_frame, text="Etapa Procesal:", font=('', 9, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=3, padx=(0, 10))
        self.etapa_label = ttk.Label(self.juris_frame, text="", wraplength=400)
        self.etapa_label.grid(row=2, column=1, sticky=tk.EW, pady=3)

        # --- Gestión de Archivos ---
        self.files_frame = ttk.LabelFrame(self.scrollable_frame, text="Gestión de Archivos", padding="10")
        self.files_frame.grid(row=3, column=0, sticky='ew', pady=(0, 10))
        self.files_frame.columnconfigure(1, weight=1)

        # Ruta de Documentos
        ttk.Label(self.files_frame, text="Carpeta:", font=('', 9, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=3, padx=(0, 10))
        self.ruta_label = ttk.Label(self.files_frame, text="", wraplength=400, foreground="blue", cursor="hand2")
        self.ruta_label.grid(row=0, column=1, sticky=tk.EW, pady=3)
        self.ruta_label.bind("<Button-1>", self._open_case_folder)

        # --- Alertas y Notificaciones ---
        self.alerts_frame = ttk.LabelFrame(self.scrollable_frame, text="Alertas y Notificaciones", padding="10")
        self.alerts_frame.grid(row=4, column=0, sticky='ew', pady=(0, 10))
        self.alerts_frame.columnconfigure(1, weight=1)

        # Alerta de Inactividad
        ttk.Label(self.alerts_frame, text="Alerta Inactividad:", font=('', 9, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=3, padx=(0, 10))
        self.inactividad_label = ttk.Label(self.alerts_frame, text="")
        self.inactividad_label.grid(row=0, column=1, sticky=tk.EW, pady=3)

        # --- Etiquetas ---
        self.etiquetas_frame = ttk.LabelFrame(self.scrollable_frame, text="Etiquetas", padding="10")
        self.etiquetas_frame.grid(row=5, column=0, sticky='ew', pady=(0, 10))
        self.etiquetas_frame.columnconfigure(0, weight=1)

        # Frame para etiquetas con scroll horizontal si es necesario
        self.etiquetas_content_frame = ttk.Frame(self.etiquetas_frame)
        self.etiquetas_content_frame.grid(row=0, column=0, sticky='ew')
        self.etiquetas_content_frame.columnconfigure(0, weight=1)

        self.etiquetas_text = tk.Text(self.etiquetas_content_frame, height=3, wrap=tk.WORD, state=tk.DISABLED)
        self.etiquetas_text.grid(row=0, column=0, sticky='ew')

        # --- Notas ---
        self.notas_frame = ttk.LabelFrame(self.scrollable_frame, text="Notas del Caso", padding="10")
        self.notas_frame.grid(row=6, column=0, sticky='ew', pady=(0, 10))
        self.notas_frame.columnconfigure(0, weight=1)
        self.notas_frame.rowconfigure(0, weight=1)

        # Text widget para notas con scrollbar
        notas_container = ttk.Frame(self.notas_frame)
        notas_container.grid(row=0, column=0, sticky='ew')
        notas_container.columnconfigure(0, weight=1)
        notas_container.rowconfigure(0, weight=1)

        self.notas_text = tk.Text(notas_container, height=6, wrap=tk.WORD, state=tk.DISABLED)
        self.notas_text.grid(row=0, column=0, sticky='ew')

        notas_scrollbar = ttk.Scrollbar(notas_container, orient="vertical", command=self.notas_text.yview)
        self.notas_text.configure(yscrollcommand=notas_scrollbar.set)
        notas_scrollbar.grid(row=0, column=1, sticky='ns')

        # --- Estadísticas del Caso ---
        self.stats_frame = ttk.LabelFrame(self.scrollable_frame, text="Estadísticas", padding="10")
        self.stats_frame.grid(row=7, column=0, sticky='ew', pady=(0, 10))
        self.stats_frame.columnconfigure(1, weight=1)

        # Fecha de Creación
        ttk.Label(self.stats_frame, text="Creado:", font=('', 9, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=3, padx=(0, 10))
        self.fecha_creacion_label = ttk.Label(self.stats_frame, text="")
        self.fecha_creacion_label.grid(row=0, column=1, sticky=tk.EW, pady=3)

        # Número de Tareas
        ttk.Label(self.stats_frame, text="Tareas:", font=('', 9, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=3, padx=(0, 10))
        self.num_tareas_label = ttk.Label(self.stats_frame, text="")
        self.num_tareas_label.grid(row=1, column=1, sticky=tk.EW, pady=3)

        # Número de Partes
        ttk.Label(self.stats_frame, text="Partes:", font=('', 9, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=3, padx=(0, 10))
        self.num_partes_label = ttk.Label(self.stats_frame, text="")
        self.num_partes_label.grid(row=2, column=1, sticky=tk.EW, pady=3)

        # Número de Audiencias
        ttk.Label(self.stats_frame, text="Audiencias:", font=('', 9, 'bold')).grid(row=3, column=0, sticky=tk.W, pady=3, padx=(0, 10))
        self.num_audiencias_label = ttk.Label(self.stats_frame, text="")
        self.num_audiencias_label.grid(row=3, column=1, sticky=tk.EW, pady=3)

        # Número de Actividades de Seguimiento
        ttk.Label(self.stats_frame, text="Actividades:", font=('', 9, 'bold')).grid(row=4, column=0, sticky=tk.W, pady=3, padx=(0, 10))
        self.num_actividades_label = ttk.Label(self.stats_frame, text="")
        self.num_actividades_label.grid(row=4, column=1, sticky=tk.EW, pady=3)

        # Mostrar estado inicial (sin caso)
        self.display_no_case()

    def on_case_changed(self, case_data):
        """Manejar cambio de caso seleccionado"""
        self.current_case = case_data
        if case_data:
            self.display_case_details(case_data)
        else:
            self.display_no_case()

    def display_case_details(self, case_data):
        """Mostrar los detalles del caso"""
        try:
            # Actualizar estado
            self.status_label.config(text=f"Caso Seleccionado: {case_data.get('caratula', 'Sin carátula')}", 
                                    foreground='darkgreen', font=('', 12, 'bold'))

            # Información básica
            self.id_label.config(text=str(case_data.get('id', '')))
            self.caratula_label.config(text=case_data.get('caratula', 'N/A'))
            
            # Obtener información del cliente
            cliente_info = "N/A"
            if case_data.get('cliente_id'):
                try:
                    cliente = self.db_crm.get_client_by_id(case_data['cliente_id'])
                    if cliente:
                        cliente_info = f"{cliente.get('nombre', 'Sin nombre')} (ID: {cliente['id']})"
                except:
                    cliente_info = f"Cliente ID: {case_data['cliente_id']} (Error al cargar)"
            self.cliente_label.config(text=cliente_info)

            self.num_exp_label.config(text=case_data.get('num_expediente', 'N/A'))
            self.anio_label.config(text=case_data.get('anio_caratula', 'N/A'))

            # Información jurisdiccional
            self.juzgado_label.config(text=case_data.get('juzgado', 'N/A'))
            self.jurisdiccion_label.config(text=case_data.get('jurisdiccion', 'N/A'))
            self.etapa_label.config(text=case_data.get('etapa_procesal', 'N/A'))

            # Gestión de archivos
            ruta = case_data.get('ruta_documentos', '')
            if ruta:
                # Verificar si la ruta existe
                import os
                if os.path.exists(ruta):
                    self.ruta_label.config(text=ruta, foreground="blue")
                else:
                    self.ruta_label.config(text=f"{ruta} (No existe)", foreground="red")
            else:
                self.ruta_label.config(text="Sin carpeta asignada", foreground="gray")

            # Alertas y notificaciones
            inactividad_activa = case_data.get('alerta_inactividad', False)
            dias_inactividad = case_data.get('inactividad_dias', 0)
            if inactividad_activa:
                self.inactividad_label.config(text=f"Activa - {dias_inactividad} días", foreground="orange")
            else:
                self.inactividad_label.config(text="Desactivada", foreground="gray")

            # Etiquetas
            etiquetas = case_data.get('etiquetas', '')
            self.etiquetas_text.config(state=tk.NORMAL)
            self.etiquetas_text.delete(1.0, tk.END)
            if etiquetas:
                self.etiquetas_text.insert(1.0, etiquetas)
            else:
                self.etiquetas_text.insert(1.0, "Sin etiquetas asignadas")
            self.etiquetas_text.config(state=tk.DISABLED)

            # Notas
            notas = case_data.get('notas', '')
            self.notas_text.config(state=tk.NORMAL)
            self.notas_text.delete(1.0, tk.END)
            if notas:
                self.notas_text.insert(1.0, notas)
            else:
                self.notas_text.insert(1.0, "Sin notas registradas")
            self.notas_text.config(state=tk.DISABLED)

            # Estadísticas
            self.fecha_creacion_label.config(text=case_data.get('fecha_creacion', 'N/A'))
            
            # Cargar estadísticas relacionadas
            self._load_case_statistics(case_data['id'])

        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar detalles del caso: {e}")

    def _load_case_statistics(self, case_id):
        """Cargar estadísticas del caso"""
        try:
            # Contar tareas
            try:
                tareas = self.db_crm.get_tareas_by_case(case_id)
                num_tareas = len(tareas) if tareas else 0
                # Separar por estado
                tareas_pendientes = len([t for t in tareas if t.get('estado') == 'Pendiente']) if tareas else 0
                tareas_completadas = len([t for t in tareas if t.get('estado') == 'Completada']) if tareas else 0
                self.num_tareas_label.config(text=f"{num_tareas} total ({tareas_pendientes} pendientes, {tareas_completadas} completadas)")
            except:
                self.num_tareas_label.config(text="Error al cargar")

            # Contar partes
            try:
                partes = self.db_crm.get_partes_by_case(case_id)
                num_partes = len(partes) if partes else 0
                self.num_partes_label.config(text=f"{num_partes} parte(s)")
            except:
                self.num_partes_label.config(text="Error al cargar")

            # Contar audiencias
            try:
                audiencias = self.db_crm.get_audiencias_by_case(case_id)
                num_audiencias = len(audiencias) if audiencias else 0
                # Separar por fecha (pasadas/futuras)
                today = datetime.date.today()
                audiencias_futuras = 0
                audiencias_pasadas = 0
                if audiencias:
                    for aud in audiencias:
                        try:
                            fecha_aud = datetime.datetime.strptime(aud.get('fecha', ''), '%Y-%m-%d').date()
                            if fecha_aud >= today:
                                audiencias_futuras += 1
                            else:
                                audiencias_pasadas += 1
                        except:
                            continue
                self.num_audiencias_label.config(text=f"{num_audiencias} total ({audiencias_futuras} próximas, {audiencias_pasadas} pasadas)")
            except:
                self.num_audiencias_label.config(text="Error al cargar")

            # Contar actividades de seguimiento
            try:
                actividades = self.db_crm.get_actividades_by_case(case_id)
                num_actividades = len(actividades) if actividades else 0
                self.num_actividades_label.config(text=f"{num_actividades} actividad(es)")
            except:
                self.num_actividades_label.config(text="Error al cargar")

        except Exception as e:
            print(f"Error al cargar estadísticas del caso: {e}")

    def display_no_case(self):
        """Mostrar estado cuando no hay caso seleccionado"""
        # Estado
        self.status_label.config(text="Ningún caso seleccionado", foreground='gray', font=('', 12))

        # Limpiar todos los campos
        labels_to_clear = [
            self.id_label, self.caratula_label, self.cliente_label, self.num_exp_label,
            self.anio_label, self.juzgado_label, self.jurisdiccion_label, self.etapa_label,
            self.ruta_label, self.inactividad_label, self.fecha_creacion_label,
            self.num_tareas_label, self.num_partes_label, self.num_audiencias_label,
            self.num_actividades_label
        ]
        
        for label in labels_to_clear:
            label.config(text="", foreground="black")

        # Limpiar texto de etiquetas y notas
        self.etiquetas_text.config(state=tk.NORMAL)
        self.etiquetas_text.delete(1.0, tk.END)
        self.etiquetas_text.config(state=tk.DISABLED)

        self.notas_text.config(state=tk.NORMAL)
        self.notas_text.delete(1.0, tk.END)
        self.notas_text.config(state=tk.DISABLED)

    def _open_case_folder(self, event):
        """Abrir la carpeta del caso"""
        if not self.current_case:
            return

        ruta = self.current_case.get('ruta_documentos', '')
        if not ruta:
            messagebox.showinfo("Sin Carpeta", "No hay carpeta asignada a este caso.")
            return

        import os
        if not os.path.exists(ruta):
            messagebox.showerror("Carpeta no Encontrada", f"La carpeta no existe: {ruta}")
            return

        try:
            import subprocess
            import sys
            
            if sys.platform == "win32":
                os.startfile(ruta)
            elif sys.platform == "darwin":
                subprocess.call(["open", ruta])
            else:
                subprocess.call(["xdg-open", ruta])
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir carpeta: {e}")

    def refresh_data(self):
        """Refrescar los datos del módulo"""
        if self.current_case:
            # Recargar datos del caso actual
            try:
                case_data = self.db_crm.get_case_by_id(self.current_case['id'])
                if case_data:
                    self.current_case = case_data
                    self.display_case_details(case_data)
                else:
                    self.display_no_case()
            except:
                self.display_no_case()

    def get_current_case(self):
        """Obtener el caso actual"""
        return self.current_case
