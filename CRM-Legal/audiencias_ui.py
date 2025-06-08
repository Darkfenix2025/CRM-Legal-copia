# audiencias_ui.py
import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import re
import threading
import webbrowser
import urllib.parse
from tkcalendar import Calendar, DateEntry

class AudienciasTab(ttk.Frame):
    def __init__(self, parent, app_controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.app_controller = app_controller
        self.db_crm = self.app_controller.db_crm
        self.selected_audiencia_id = None
        self.fecha_seleccionada_agenda = datetime.date.today().strftime("%Y-%m-%d")
        self._create_widgets()

    def _create_widgets(self):
        # Configurar el frame principal
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # --- Panel Izquierdo: Calendario ---
        calendar_frame = ttk.LabelFrame(self, text="Calendario de Audiencias", padding="5")
        calendar_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 5))
        calendar_frame.columnconfigure(0, weight=1)
        calendar_frame.rowconfigure(0, weight=1)
        calendar_frame.rowconfigure(1, weight=0)

        # Calendario
        self.calendar = Calendar(calendar_frame, selectmode='day', date_pattern='yyyy-mm-dd')
        self.calendar.grid(row=0, column=0, sticky='nsew', pady=(0, 10))
        self.calendar.bind("<<CalendarSelected>>", self.actualizar_lista_audiencias)

        # Botón para agregar audiencia
        self.add_audiencia_btn = ttk.Button(calendar_frame, text="Agregar Audiencia", 
                                          command=lambda: self.abrir_dialogo_audiencia(), state=tk.NORMAL)
        self.add_audiencia_btn.grid(row=1, column=0, sticky='ew')

        # --- Panel Derecho: Lista y Detalles ---
        right_panel = ttk.Frame(self)
        right_panel.grid(row=0, column=1, sticky='nsew', padx=(5, 0))
        right_panel.columnconfigure(0, weight=1)
        right_panel.rowconfigure(0, weight=1)  # Lista de audiencias
        right_panel.rowconfigure(1, weight=0)  # Botones
        right_panel.rowconfigure(2, weight=0)  # Detalles

        # --- Lista de Audiencias ---
        audiencias_list_frame = ttk.LabelFrame(right_panel, text="Audiencias del Día", padding="5")
        audiencias_list_frame.grid(row=0, column=0, sticky='nsew', pady=(0, 5))
        audiencias_list_frame.columnconfigure(0, weight=1)
        audiencias_list_frame.rowconfigure(0, weight=1)

        # TreeView de audiencias
        audiencias_cols = ('ID', 'Hora', 'Caso', 'Descripción')
        self.audiencias_tree = ttk.Treeview(audiencias_list_frame, columns=audiencias_cols, show='headings', selectmode='browse')
        
        self.audiencias_tree.heading('ID', text='ID')
        self.audiencias_tree.heading('Hora', text='Hora')
        self.audiencias_tree.heading('Caso', text='Caso')
        self.audiencias_tree.heading('Descripción', text='Descripción')

        self.audiencias_tree.column('ID', width=40, stretch=tk.NO, anchor=tk.CENTER)
        self.audiencias_tree.column('Hora', width=80, stretch=tk.NO, anchor=tk.CENTER)
        self.audiencias_tree.column('Caso', width=200, stretch=True)
        self.audiencias_tree.column('Descripción', width=250, stretch=True)

        # Scrollbars para audiencias
        audiencias_scrollbar_y = ttk.Scrollbar(audiencias_list_frame, orient=tk.VERTICAL, command=self.audiencias_tree.yview)
        self.audiencias_tree.configure(yscrollcommand=audiencias_scrollbar_y.set)
        audiencias_scrollbar_y.grid(row=0, column=1, sticky='ns')

        self.audiencias_tree.grid(row=0, column=0, sticky='nsew')

        # Bind para selección y doble click
        self.audiencias_tree.bind('<<TreeviewSelect>>', self.on_audiencia_tree_select)
        self.audiencias_tree.bind('<Double-1>', self.abrir_link_audiencia_seleccionada)

        # --- Botones de Acción ---
        audiencias_buttons_frame = ttk.Frame(right_panel)
        audiencias_buttons_frame.grid(row=1, column=0, sticky='ew', pady=5)
        audiencias_buttons_frame.columnconfigure(0, weight=1)
        audiencias_buttons_frame.columnconfigure(1, weight=1)
        audiencias_buttons_frame.columnconfigure(2, weight=1)
        audiencias_buttons_frame.columnconfigure(3, weight=1)

        self.edit_audiencia_btn = ttk.Button(audiencias_buttons_frame, text="Editar", 
                                           command=self.editar_audiencia_seleccionada, state=tk.DISABLED)
        self.edit_audiencia_btn.grid(row=0, column=0, sticky='ew', padx=(0, 5))

        self.delete_audiencia_btn = ttk.Button(audiencias_buttons_frame, text="Eliminar", 
                                             command=self.eliminar_audiencia_seleccionada, state=tk.DISABLED)
        self.delete_audiencia_btn.grid(row=0, column=1, sticky='ew', padx=5)

        self.open_link_btn = ttk.Button(audiencias_buttons_frame, text="Abrir Link", 
                                       command=self.abrir_link_audiencia_seleccionada, state=tk.DISABLED)
        self.open_link_btn.grid(row=0, column=2, sticky='ew', padx=5)

        self.share_btn = ttk.Button(audiencias_buttons_frame, text="Compartir", 
                                   command=self.mostrar_menu_compartir_audiencia, state=tk.DISABLED)
        self.share_btn.grid(row=0, column=3, sticky='ew', padx=(5, 0))

        # --- Detalles de Audiencia ---
        detalles_frame = ttk.LabelFrame(right_panel, text="Detalles de la Audiencia", padding="5")
        detalles_frame.grid(row=2, column=0, sticky='ew', pady=(5, 0))
        detalles_frame.columnconfigure(1, weight=1)

        ttk.Label(detalles_frame, text="Fecha:").grid(row=0, column=0, sticky=tk.W, pady=2, padx=5)
        self.audiencia_fecha_lbl = ttk.Label(detalles_frame, text="")
        self.audiencia_fecha_lbl.grid(row=0, column=1, sticky=tk.EW, pady=2, padx=5)

        ttk.Label(detalles_frame, text="Hora:").grid(row=1, column=0, sticky=tk.W, pady=2, padx=5)
        self.audiencia_hora_lbl = ttk.Label(detalles_frame, text="")
        self.audiencia_hora_lbl.grid(row=1, column=1, sticky=tk.EW, pady=2, padx=5)

        ttk.Label(detalles_frame, text="Caso:").grid(row=2, column=0, sticky=tk.W, pady=2, padx=5)
        self.audiencia_caso_lbl = ttk.Label(detalles_frame, text="", wraplength=250)
        self.audiencia_caso_lbl.grid(row=2, column=1, sticky=tk.EW, pady=2, padx=5)

        ttk.Label(detalles_frame, text="Descripción:").grid(row=3, column=0, sticky=tk.NW, pady=2, padx=5)
        self.audiencia_desc_lbl = ttk.Label(detalles_frame, text="", wraplength=250)
        self.audiencia_desc_lbl.grid(row=3, column=1, sticky=tk.EW, pady=2, padx=5)

        ttk.Label(detalles_frame, text="Link:").grid(row=4, column=0, sticky=tk.W, pady=2, padx=5)
        self.audiencia_link_lbl = ttk.Label(detalles_frame, text="", foreground="blue", cursor="hand2", wraplength=250)
        self.audiencia_link_lbl.grid(row=4, column=1, sticky=tk.EW, pady=2, padx=5)
        self.audiencia_link_lbl.bind("<Button-1>", self.abrir_link_audiencia_seleccionada)

        # Cargar audiencias del día actual
        self.cargar_audiencias_fecha_actual()

    def cargar_audiencias_fecha_actual(self):
        """Cargar audiencias de la fecha actual"""
        self.fecha_seleccionada_agenda = datetime.date.today().strftime("%Y-%m-%d")
        self.actualizar_lista_audiencias()
        self.marcar_dias_audiencias_calendario()

    def actualizar_lista_audiencias(self, event=None):
        """Actualizar la lista de audiencias para la fecha seleccionada"""
        if hasattr(self.calendar, 'selection_get'):
            try:
                fecha_sel = self.calendar.selection_get()
                self.fecha_seleccionada_agenda = fecha_sel.strftime("%Y-%m-%d")
            except:
                self.fecha_seleccionada_agenda = datetime.date.today().strftime("%Y-%m-%d")

        # Limpiar TreeView
        for item in self.audiencias_tree.get_children():
            self.audiencias_tree.delete(item)

        try:
            audiencias = self.db_crm.get_audiencias_by_date(self.fecha_seleccionada_agenda)
            for audiencia in audiencias:
                # Obtener datos del caso
                caso_info = "Sin caso"
                if audiencia.get('caso_id'):
                    try:
                        caso = self.db_crm.get_case_by_id(audiencia['caso_id'])
                        if caso:
                            caso_info = f"{caso.get('caratula', 'Sin carátula')}"
                    except:
                        caso_info = f"Caso ID: {audiencia['caso_id']}"

                self.audiencias_tree.insert('', 'end', values=(
                    audiencia['id'],
                    audiencia.get('hora', ''),
                    caso_info,
                    audiencia.get('descripcion', '')
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar audiencias: {e}")

    def marcar_dias_audiencias_calendario(self):
        """Marcar en el calendario los días que tienen audiencias"""
        try:
            fechas_con_audiencias = self.db_crm.get_dates_with_audiencias()
            
            # Limpiar marcas anteriores
            self.calendar.calevent_remove('all')
            
            # Marcar fechas con audiencias
            for fecha_str in fechas_con_audiencias:
                try:
                    fecha = datetime.datetime.strptime(fecha_str, "%Y-%m-%d").date()
                    self.calendar.calevent_create(fecha, "Audiencia", "audiencia")
                except:
                    continue
                    
            # Configurar el estilo para las audiencias
            self.calendar.tag_config("audiencia", background="lightblue", foreground="darkblue")
            
        except Exception as e:
            print(f"Error al marcar días con audiencias: {e}")

    def on_audiencia_tree_select(self, event=None):
        """Manejar selección de audiencia"""
        selected_items = self.audiencias_tree.selection()
        if selected_items:
            selected_item = selected_items[0]
            audiencia_id = self.audiencias_tree.item(selected_item, 'values')[0]
            
            try:
                self.selected_audiencia_id = audiencia_id
                self.mostrar_detalles_audiencia(audiencia_id)
                self.habilitar_botones_audiencia()
            except Exception as e:
                messagebox.showerror("Error", f"Error al obtener detalles de la audiencia: {e}")
        else:
            self.selected_audiencia_id = None
            self.limpiar_detalles_audiencia()
            self.deshabilitar_botones_audiencia()

    def mostrar_detalles_audiencia(self, audiencia_id):
        """Mostrar detalles de la audiencia seleccionada"""
        try:
            audiencia = self.db_crm.get_audiencia_by_id(audiencia_id)
            if audiencia:
                self.audiencia_fecha_lbl.config(text=audiencia.get('fecha', ''))
                self.audiencia_hora_lbl.config(text=audiencia.get('hora', ''))
                self.audiencia_desc_lbl.config(text=audiencia.get('descripcion', ''))
                
                # Información del caso
                caso_info = "Sin caso asociado"
                if audiencia.get('caso_id'):
                    try:
                        caso = self.db_crm.get_case_by_id(audiencia['caso_id'])
                        if caso:
                            caso_info = f"{caso.get('caratula', 'Sin carátula')}"
                    except:
                        caso_info = f"Caso ID: {audiencia['caso_id']}"
                self.audiencia_caso_lbl.config(text=caso_info)
                
                # Link
                link = audiencia.get('link', '')
                self.audiencia_link_lbl.config(text=link if link else "Sin link")
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar detalles: {e}")

    def limpiar_detalles_audiencia(self):
        """Limpiar los detalles de audiencia"""
        self.audiencia_fecha_lbl.config(text="")
        self.audiencia_hora_lbl.config(text="")
        self.audiencia_caso_lbl.config(text="")
        self.audiencia_desc_lbl.config(text="")
        self.audiencia_link_lbl.config(text="")

    def habilitar_botones_audiencia(self):
        """Habilitar botones cuando hay una audiencia seleccionada"""
        self.edit_audiencia_btn.config(state=tk.NORMAL)
        self.delete_audiencia_btn.config(state=tk.DISABLED)  # Deshabilitado temporalmente por seguridad
        
        # Habilitar "Abrir Link" solo si hay link
        try:
            if self.selected_audiencia_id:
                audiencia = self.db_crm.get_audiencia_by_id(self.selected_audiencia_id)
                if audiencia and audiencia.get('link'):
                    self.open_link_btn.config(state=tk.NORMAL)
                    self.share_btn.config(state=tk.NORMAL)
                else:
                    self.open_link_btn.config(state=tk.DISABLED)
                    self.share_btn.config(state=tk.NORMAL)  # Compartir siempre disponible
        except:
            self.open_link_btn.config(state=tk.DISABLED)
            self.share_btn.config(state=tk.NORMAL)

    def deshabilitar_botones_audiencia(self):
        """Deshabilitar botones cuando no hay audiencia seleccionada"""
        self.edit_audiencia_btn.config(state=tk.DISABLED)
        self.delete_audiencia_btn.config(state=tk.DISABLED)
        self.open_link_btn.config(state=tk.DISABLED)
        self.share_btn.config(state=tk.DISABLED)

    def abrir_dialogo_audiencia(self, audiencia_id=None):
        """Abrir diálogo para crear o editar audiencia"""
        dialog = tk.Toplevel(self.app_controller.root)
        dialog.title("Alta/Edición de Audiencia")
        dialog.transient(self.app_controller.root)
        dialog.grab_set()
        dialog.geometry("500x600")
        dialog.resizable(False, False)

        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Variables para los campos
        caso_var = tk.StringVar()
        fecha_var = tk.StringVar()
        hora_var = tk.StringVar()
        link_var = tk.StringVar()
        desc_var = tk.StringVar()
        recordatorio_var = tk.BooleanVar()
        minutos_var = tk.StringVar(value="30")

        # Si estamos editando, cargar datos existentes
        if audiencia_id:
            try:
                audiencia_data = self.db_crm.get_audiencia_by_id(audiencia_id)
                if audiencia_data:
                    caso_var.set(str(audiencia_data.get('caso_id', '')))
                    fecha_var.set(audiencia_data.get('fecha', ''))
                    hora_var.set(audiencia_data.get('hora', ''))
                    link_var.set(audiencia_data.get('link', ''))
                    desc_var.set(audiencia_data.get('descripcion', ''))
                    recordatorio_var.set(bool(audiencia_data.get('recordatorio_activo', False)))
                    minutos_var.set(str(audiencia_data.get('recordatorio_minutos', 30)))
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar datos de la audiencia: {e}")
                dialog.destroy()
                return
        else:
            # Valores por defecto para nueva audiencia
            fecha_var.set(self.fecha_seleccionada_agenda)

        # Campos del formulario
        row = 0

        # Caso
        ttk.Label(main_frame, text="Caso ID:").grid(row=row, column=0, sticky=tk.W, pady=5)
        
        caso_frame = ttk.Frame(main_frame)
        caso_frame.grid(row=row, column=1, sticky=tk.EW, pady=5, padx=(10, 0))
        caso_frame.columnconfigure(0, weight=1)
        
        caso_entry = ttk.Entry(caso_frame, textvariable=caso_var, width=30)
        caso_entry.grid(row=0, column=0, sticky=tk.EW)
        
        ttk.Button(caso_frame, text="Seleccionar", 
                  command=lambda: self._seleccionar_caso_para_audiencia(caso_var)).grid(row=0, column=1, padx=(5, 0))
        row += 1

        # Fecha
        ttk.Label(main_frame, text="Fecha:").grid(row=row, column=0, sticky=tk.W, pady=5)
        fecha_entry = DateEntry(main_frame, textvariable=fecha_var, date_pattern='yyyy-mm-dd')
        fecha_entry.grid(row=row, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        row += 1

        # Hora
        ttk.Label(main_frame, text="Hora (HH:MM):").grid(row=row, column=0, sticky=tk.W, pady=5)
        hora_entry = ttk.Entry(main_frame, textvariable=hora_var, width=20)
        hora_entry.grid(row=row, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        row += 1

        # Link
        ttk.Label(main_frame, text="Link (opcional):").grid(row=row, column=0, sticky=tk.W, pady=5)
        link_entry = ttk.Entry(main_frame, textvariable=link_var, width=50)
        link_entry.grid(row=row, column=1, sticky=tk.EW, pady=5, padx=(10, 0))
        row += 1

        # Descripción
        ttk.Label(main_frame, text="Descripción:").grid(row=row, column=0, sticky=tk.NW, pady=5)
        desc_text = tk.Text(main_frame, height=6, width=50)
        desc_text.grid(row=row, column=1, sticky=tk.EW, pady=5, padx=(10, 0))
        if desc_var.get():
            desc_text.insert('1.0', desc_var.get())
        row += 1

        # Recordatorio
        recordatorio_frame = ttk.LabelFrame(main_frame, text="Recordatorio", padding="5")
        recordatorio_frame.grid(row=row, column=0, columnspan=2, sticky=tk.EW, pady=10)
        recordatorio_frame.columnconfigure(1, weight=1)

        recordatorio_check = ttk.Checkbutton(recordatorio_frame, text="Activar recordatorio", variable=recordatorio_var)
        recordatorio_check.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=2)

        ttk.Label(recordatorio_frame, text="Minutos antes:").grid(row=1, column=0, sticky=tk.W, pady=2)
        minutos_entry = ttk.Entry(recordatorio_frame, textvariable=minutos_var, width=10)
        minutos_entry.grid(row=1, column=1, sticky=tk.W, pady=2, padx=(10, 0))
        row += 1

        # Configurar expansión de columnas
        main_frame.columnconfigure(1, weight=1)

        # Botones
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=row, column=0, columnspan=2, pady=20)

        ttk.Button(buttons_frame, text="Guardar", 
                  command=lambda: self.guardar_audiencia(audiencia_id, caso_var.get(), fecha_var.get(),
                                                        hora_var.get(), link_var.get(), desc_text.get('1.0', tk.END).strip(),
                                                        recordatorio_var.get(), minutos_var.get(), dialog)).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(buttons_frame, text="Cancelar", command=dialog.destroy).pack(side=tk.LEFT)

        # Focus en el primer campo
        caso_entry.focus_set()

    def _seleccionar_caso_para_audiencia(self, caso_var):
        """Abrir diálogo para seleccionar un caso"""
        # Simplificado: pedir ID del caso
        caso_id = tk.simpledialog.askstring("Seleccionar Caso", "Ingrese el ID del caso:")
        if caso_id and caso_id.isdigit():
            try:
                caso = self.db_crm.get_case_by_id(int(caso_id))
                if caso:
                    caso_var.set(caso_id)
                    messagebox.showinfo("Caso Seleccionado", f"Caso: {caso.get('caratula', 'Sin carátula')}")
                else:
                    messagebox.showerror("Error", "Caso no encontrado")
            except Exception as e:
                messagebox.showerror("Error", f"Error al buscar caso: {e}")

    def guardar_audiencia(self, audiencia_id, caso_id, fecha_str, hora_str, link, desc, r_act, r_min, dialog):
        """Guardar audiencia (crear o actualizar)"""
        # Validaciones
        if not fecha_str:
            messagebox.showwarning("Campo Requerido", "La fecha es obligatoria.")
            return

        if not hora_str:
            messagebox.showwarning("Campo Requerido", "La hora es obligatoria.")
            return

        # Validar formato de hora
        if not self.parsear_hora(hora_str):
            messagebox.showwarning("Formato Incorrecto", "La hora debe estar en formato HH:MM (24 horas).")
            return

        try:
            # Validar minutos de recordatorio
            try:
                minutos_int = int(r_min) if r_min.strip() else 30
            except ValueError:
                minutos_int = 30

            # Validar caso_id
            caso_id_int = None
            if caso_id and caso_id.strip():
                try:
                    caso_id_int = int(caso_id)
                    # Verificar que el caso existe
                    caso = self.db_crm.get_case_by_id(caso_id_int)
                    if not caso:
                        messagebox.showerror("Error", "El caso especificado no existe.")
                        return
                except ValueError:
                    messagebox.showerror("Error", "El ID del caso debe ser un número.")
                    return

            if audiencia_id:  # Editar audiencia existente
                self.db_crm.update_audiencia(audiencia_id, caso_id_int, fecha_str, hora_str, link, desc, r_act, minutos_int)
                messagebox.showinfo("Éxito", "Audiencia actualizada correctamente.")
            else:  # Crear nueva audiencia
                self.db_crm.add_audiencia(caso_id_int, fecha_str, hora_str, link, desc, r_act, minutos_int)
                messagebox.showinfo("Éxito", "Audiencia creada correctamente.")

            dialog.destroy()
            self.actualizar_lista_audiencias()  # Recargar la lista
            self.marcar_dias_audiencias_calendario()  # Actualizar calendario
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar audiencia: {e}")

    def parsear_hora(self, hora_str):
        """Validar y parsear formato de hora HH:MM"""
        patron = r'^([0-1]?[0-9]|2[0-3]):([0-5][0-9])$'
        match = re.match(patron, hora_str.strip())
        if match:
            horas, minutos = match.groups()
            return f"{int(horas):02d}:{int(minutos):02d}"
        return None

    def editar_audiencia_seleccionada(self):
        """Editar la audiencia seleccionada"""
        if not self.selected_audiencia_id:
            messagebox.showwarning("Sin Selección", "Seleccione una audiencia para editar.")
            return
        self.abrir_dialogo_audiencia(self.selected_audiencia_id)

    def eliminar_audiencia_seleccionada(self):
        """Eliminar la audiencia seleccionada"""
        if not self.selected_audiencia_id:
            messagebox.showwarning("Sin Selección", "Seleccione una audiencia para eliminar.")
            return

        # Confirmar eliminación
        response = messagebox.askyesno("Confirmar Eliminación", 
                                     "¿Está seguro de que desea eliminar esta audiencia?")

        if response:
            try:
                self.db_crm.delete_audiencia(self.selected_audiencia_id)
                messagebox.showinfo("Éxito", "Audiencia eliminada correctamente.")
                self.actualizar_lista_audiencias()  # Recargar la lista
                self.marcar_dias_audiencias_calendario()  # Actualizar calendario
                self.selected_audiencia_id = None
                self.limpiar_detalles_audiencia()
                self.deshabilitar_botones_audiencia()
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar audiencia: {e}")

    def abrir_link_audiencia_seleccionada(self, event=None):
        """Abrir el link de la audiencia seleccionada"""
        if not self.selected_audiencia_id:
            return

        try:
            audiencia = self.db_crm.get_audiencia_by_id(self.selected_audiencia_id)
            if audiencia and audiencia.get('link'):
                link = audiencia['link']
                if link.startswith(('http://', 'https://')):
                    webbrowser.open(link)
                else:
                    # Asumir que es un link web y agregar protocolo
                    webbrowser.open(f"https://{link}")
            else:
                messagebox.showinfo("Sin Link", "Esta audiencia no tiene un link asociado.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir link: {e}")

    def mostrar_menu_compartir_audiencia(self):
        """Mostrar menú de opciones para compartir audiencia"""
        if not self.selected_audiencia_id:
            return

        # Crear menú contextual
        menu = tk.Menu(self.app_controller.root, tearoff=0)
        menu.add_command(label="Compartir por Email", command=self._compartir_audiencia_por_email)
        menu.add_command(label="Compartir por WhatsApp", command=self._compartir_audiencia_por_whatsapp)
        
        # Mostrar menú en la posición del cursor
        try:
            menu.tk_popup(self.app_controller.root.winfo_pointerx(), self.app_controller.root.winfo_pointery())
        finally:
            menu.grab_release()

    def _formatear_texto_audiencia_para_compartir(self, audiencia):
        """Formatear texto de audiencia para compartir"""
        caso_info = "Sin caso asociado"
        if audiencia.get('caso_id'):
            try:
                caso = self.db_crm.get_case_by_id(audiencia['caso_id'])
                if caso:
                    caso_info = f"{caso.get('caratula', 'Sin carátula')}"
            except:
                caso_info = f"Caso ID: {audiencia['caso_id']}"

        texto = f"""🏛️ AUDIENCIA PROGRAMADA

📅 Fecha: {audiencia.get('fecha', '')}
🕐 Hora: {audiencia.get('hora', '')}
📁 Caso: {caso_info}
📋 Descripción: {audiencia.get('descripcion', '')}"""

        if audiencia.get('link'):
            texto += f"\n🔗 Link: {audiencia['link']}"

        return texto

    def _compartir_audiencia_por_email(self):
        """Compartir audiencia por email"""
        try:
            audiencia = self.db_crm.get_audiencia_by_id(self.selected_audiencia_id)
            if audiencia:
                texto = self._formatear_texto_audiencia_para_compartir(audiencia)
                # Crear URL de email
                subject = f"Audiencia - {audiencia.get('fecha', '')} {audiencia.get('hora', '')}"
                body = urllib.parse.quote(texto)
                email_url = f"mailto:?subject={urllib.parse.quote(subject)}&body={body}"
                webbrowser.open(email_url)
        except Exception as e:
            messagebox.showerror("Error", f"Error al compartir por email: {e}")

    def _compartir_audiencia_por_whatsapp(self):
        """Compartir audiencia por WhatsApp"""
        try:
            audiencia = self.db_crm.get_audiencia_by_id(self.selected_audiencia_id)
            if audiencia:
                texto = self._formatear_texto_audiencia_para_compartir(audiencia)
                # Crear URL de WhatsApp
                whatsapp_url = f"https://wa.me/?text={urllib.parse.quote(texto)}"
                webbrowser.open(whatsapp_url)
        except Exception as e:
            messagebox.showerror("Error", f"Error al compartir por WhatsApp: {e}")

    def refresh_data(self):
        """Refrescar los datos del módulo"""
        self.actualizar_lista_audiencias()
        self.marcar_dias_audiencias_calendario()
        
        if self.selected_audiencia_id:
            # Intentar mantener la selección actual
            try:
                audiencia = self.db_crm.get_audiencia_by_id(self.selected_audiencia_id)
                if audiencia:
                    self.mostrar_detalles_audiencia(self.selected_audiencia_id)
                    self.habilitar_botones_audiencia()
                else:
                    self.selected_audiencia_id = None
                    self.limpiar_detalles_audiencia()
                    self.deshabilitar_botones_audiencia()
            except:
                self.selected_audiencia_id = None
                self.limpiar_detalles_audiencia()
                self.deshabilitar_botones_audiencia()

    def get_selected_audiencia(self):
        """Obtener la audiencia seleccionada actualmente"""
        if self.selected_audiencia_id:
            try:
                return self.db_crm.get_audiencia_by_id(self.selected_audiencia_id)
            except:
                return None
        return None
