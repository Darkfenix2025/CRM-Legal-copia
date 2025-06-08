# casos_ui.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os

class CasosTab(ttk.Frame):
    def __init__(self, parent, app_controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.app_controller = app_controller
        self.db_crm = self.app_controller.db_crm
        self.selected_case = None
        self.current_client_id = None
        self._create_widgets()

    def _create_widgets(self):
        # Configurar el frame principal
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Frame principal para casos
        main_frame = ttk.Frame(self)
        main_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)  # Lista de casos
        main_frame.rowconfigure(1, weight=0)  # Botones

        # --- Lista de Casos ---
        case_list_frame = ttk.LabelFrame(main_frame, text="Casos del Cliente", padding="5")
        case_list_frame.grid(row=0, column=0, sticky='nsew', pady=(0, 5))
        case_list_frame.columnconfigure(0, weight=1)
        case_list_frame.rowconfigure(0, weight=1)

        # TreeView de casos
        case_cols = ('ID', 'Carátula', 'Nº Expediente', 'Año', 'Juzgado', 'Etapa', 'Etiquetas')
        self.case_tree = ttk.Treeview(case_list_frame, columns=case_cols, show='headings', selectmode='browse')
        
        self.case_tree.heading('ID', text='ID')
        self.case_tree.heading('Carátula', text='Carátula')
        self.case_tree.heading('Nº Expediente', text='Nº Exp.')
        self.case_tree.heading('Año', text='Año')
        self.case_tree.heading('Juzgado', text='Juzgado')
        self.case_tree.heading('Etapa', text='Etapa')
        self.case_tree.heading('Etiquetas', text='Etiquetas')

        self.case_tree.column('ID', width=50, stretch=tk.NO, anchor=tk.CENTER)
        self.case_tree.column('Carátula', width=300, stretch=True)
        self.case_tree.column('Nº Expediente', width=80, stretch=tk.NO)
        self.case_tree.column('Año', width=60, stretch=tk.NO)
        self.case_tree.column('Juzgado', width=150, stretch=True)
        self.case_tree.column('Etapa', width=120, stretch=tk.NO)
        self.case_tree.column('Etiquetas', width=150, stretch=True)

        # Scrollbars para la lista de casos
        case_scrollbar_y = ttk.Scrollbar(case_list_frame, orient=tk.VERTICAL, command=self.case_tree.yview)
        self.case_tree.configure(yscrollcommand=case_scrollbar_y.set)
        case_scrollbar_y.grid(row=0, column=1, sticky='ns')

        case_scrollbar_x = ttk.Scrollbar(case_list_frame, orient=tk.HORIZONTAL, command=self.case_tree.xview)
        self.case_tree.configure(xscrollcommand=case_scrollbar_x.set)
        case_scrollbar_x.grid(row=1, column=0, sticky='ew')

        self.case_tree.grid(row=0, column=0, sticky='nsew')

        # Bind para selección de caso
        self.case_tree.bind('<<TreeviewSelect>>', self.on_case_select)

        # --- Botones de Acción ---
        case_buttons_frame = ttk.Frame(main_frame)
        case_buttons_frame.grid(row=1, column=0, sticky='ew', pady=5)
        case_buttons_frame.columnconfigure(0, weight=1)
        case_buttons_frame.columnconfigure(1, weight=1)
        case_buttons_frame.columnconfigure(2, weight=1)
        case_buttons_frame.columnconfigure(3, weight=1)
        case_buttons_frame.columnconfigure(4, weight=1)

        self.add_case_btn = ttk.Button(case_buttons_frame, text="Alta", command=lambda: self.open_case_dialog(), state=tk.DISABLED)
        self.add_case_btn.grid(row=0, column=0, sticky='ew', padx=(0, 5))

        self.edit_case_btn = ttk.Button(case_buttons_frame, text="Modificar", command=lambda: self.open_case_dialog(self.selected_case['id'] if self.selected_case else None), state=tk.DISABLED)
        self.edit_case_btn.grid(row=0, column=1, sticky='ew', padx=5)

        self.delete_case_btn = ttk.Button(case_buttons_frame, text="Eliminar", command=self.delete_case, state=tk.DISABLED)
        self.delete_case_btn.grid(row=0, column=2, sticky='ew', padx=5)

        self.select_folder_btn = ttk.Button(case_buttons_frame, text="Carpeta", command=self.select_case_folder, state=tk.DISABLED)
        self.select_folder_btn.grid(row=0, column=3, sticky='ew', padx=5)

        self.open_folder_btn = ttk.Button(case_buttons_frame, text="Abrir Carpeta", command=self.open_case_folder, state=tk.DISABLED)
        self.open_folder_btn.grid(row=0, column=4, sticky='ew', padx=(5, 0))

    def load_cases_by_client(self, client_id):
        """Cargar casos del cliente especificado"""
        self.current_client_id = client_id
        
        # Limpiar el TreeView
        for item in self.case_tree.get_children():
            self.case_tree.delete(item)

        if not client_id:
            self.disable_case_buttons()
            return

        try:
            cases = self.db_crm.get_cases_by_client(client_id)
            for case in cases:
                self.case_tree.insert('', 'end', values=(
                    case['id'],
                    case.get('caratula', ''),
                    case.get('num_expediente', ''),
                    case.get('anio_caratula', ''),
                    case.get('juzgado', ''),
                    case.get('etapa_procesal', ''),
                    case.get('etiquetas', '')
                ))
            
            # Habilitar botón de alta una vez que hay un cliente seleccionado
            self.add_case_btn.config(state=tk.NORMAL)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar casos: {e}")

    def clear_case_list(self):
        """Limpiar la lista de casos"""
        for item in self.case_tree.get_children():
            self.case_tree.delete(item)
        self.selected_case = None
        self.current_client_id = None
        self.disable_case_buttons()

    def on_case_select(self, event):
        """Manejar la selección de un caso"""
        selected_items = self.case_tree.selection()
        if selected_items:
            selected_item = selected_items[0]
            case_id = self.case_tree.item(selected_item, 'values')[0]
            
            try:
                case_data = self.db_crm.get_case_by_id(case_id)
                if case_data:
                    self.selected_case = case_data
                    self.enable_case_buttons()
                    # Notificar al controlador principal sobre la selección
                    if hasattr(self.app_controller, 'on_case_selected'):
                        self.app_controller.on_case_selected(case_data)
                else:
                    self.selected_case = None
                    self.disable_case_buttons()
            except Exception as e:
                messagebox.showerror("Error", f"Error al obtener detalles del caso: {e}")
        else:
            self.selected_case = None
            self.disable_case_buttons()

    def enable_case_buttons(self):
        """Habilitar botones cuando hay un caso seleccionado"""
        self.edit_case_btn.config(state=tk.NORMAL)
        self.delete_case_btn.config(state=tk.NORMAL)
        self.select_folder_btn.config(state=tk.NORMAL)
        
        # Habilitar "Abrir Carpeta" solo si hay una ruta válida
        if self.selected_case and self.selected_case.get('ruta_documentos') and os.path.exists(self.selected_case['ruta_documentos']):
            self.open_folder_btn.config(state=tk.NORMAL)
        else:
            self.open_folder_btn.config(state=tk.DISABLED)

    def disable_case_buttons(self):
        """Deshabilitar botones cuando no hay caso seleccionado"""
        self.edit_case_btn.config(state=tk.DISABLED)
        self.delete_case_btn.config(state=tk.DISABLED)
        self.select_folder_btn.config(state=tk.DISABLED)
        self.open_folder_btn.config(state=tk.DISABLED)

    def open_case_dialog(self, case_id=None):
        """Abrir diálogo para crear o editar caso"""
        if not self.current_client_id and not case_id:
            messagebox.showwarning("Sin Cliente", "Seleccione un cliente primero.")
            return

        dialog = tk.Toplevel(self.app_controller.root)
        dialog.title("Alta/Edición de Caso")
        dialog.transient(self.app_controller.root)
        dialog.grab_set()
        dialog.geometry("600x500")
        dialog.resizable(False, False)

        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Variables para los campos
        caratula_var = tk.StringVar()
        num_exp_var = tk.StringVar()
        anio_var = tk.StringVar()
        juzgado_var = tk.StringVar()
        jurisdiccion_var = tk.StringVar()
        etapa_var = tk.StringVar()
        notas_var = tk.StringVar()
        ruta_var = tk.StringVar()
        inact_days_var = tk.StringVar()
        inact_enabled_var = tk.BooleanVar()
        etiquetas_var = tk.StringVar()

        # Cliente ID (si estamos editando, obtenerlo del caso)
        cliente_id = self.current_client_id
        if case_id:
            try:
                case_data = self.db_crm.get_case_by_id(case_id)
                if case_data:
                    cliente_id = case_data['cliente_id']
                    caratula_var.set(case_data.get('caratula', ''))
                    num_exp_var.set(case_data.get('num_expediente', ''))
                    anio_var.set(case_data.get('anio_caratula', ''))
                    juzgado_var.set(case_data.get('juzgado', ''))
                    jurisdiccion_var.set(case_data.get('jurisdiccion', ''))
                    etapa_var.set(case_data.get('etapa_procesal', ''))
                    notas_var.set(case_data.get('notas', ''))
                    ruta_var.set(case_data.get('ruta_documentos', ''))
                    inact_days_var.set(str(case_data.get('inactividad_dias', 0)))
                    inact_enabled_var.set(bool(case_data.get('alerta_inactividad', False)))
                    etiquetas_var.set(case_data.get('etiquetas', ''))
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar datos del caso: {e}")
                dialog.destroy()
                return

        # Campos del formulario
        row = 0
        
        ttk.Label(main_frame, text="Carátula:").grid(row=row, column=0, sticky=tk.W, pady=5)
        caratula_entry = ttk.Entry(main_frame, textvariable=caratula_var, width=50)
        caratula_entry.grid(row=row, column=1, columnspan=2, sticky=tk.EW, pady=5, padx=(10, 0))
        row += 1

        ttk.Label(main_frame, text="Nº Expediente:").grid(row=row, column=0, sticky=tk.W, pady=5)
        num_exp_entry = ttk.Entry(main_frame, textvariable=num_exp_var, width=20)
        num_exp_entry.grid(row=row, column=1, sticky=tk.W, pady=5, padx=(10, 0))

        ttk.Label(main_frame, text="Año:").grid(row=row, column=2, sticky=tk.W, pady=5, padx=(20, 0))
        anio_entry = ttk.Entry(main_frame, textvariable=anio_var, width=10)
        anio_entry.grid(row=row, column=3, sticky=tk.W, pady=5, padx=(10, 0))
        row += 1

        ttk.Label(main_frame, text="Juzgado:").grid(row=row, column=0, sticky=tk.W, pady=5)
        juzgado_entry = ttk.Entry(main_frame, textvariable=juzgado_var, width=50)
        juzgado_entry.grid(row=row, column=1, columnspan=2, sticky=tk.EW, pady=5, padx=(10, 0))
        row += 1

        ttk.Label(main_frame, text="Jurisdicción:").grid(row=row, column=0, sticky=tk.W, pady=5)
        jurisdiccion_entry = ttk.Entry(main_frame, textvariable=jurisdiccion_var, width=50)
        jurisdiccion_entry.grid(row=row, column=1, columnspan=2, sticky=tk.EW, pady=5, padx=(10, 0))
        row += 1

        ttk.Label(main_frame, text="Etapa Procesal:").grid(row=row, column=0, sticky=tk.W, pady=5)
        etapa_entry = ttk.Entry(main_frame, textvariable=etapa_var, width=50)
        etapa_entry.grid(row=row, column=1, columnspan=2, sticky=tk.EW, pady=5, padx=(10, 0))
        row += 1

        ttk.Label(main_frame, text="Notas:").grid(row=row, column=0, sticky=tk.NW, pady=5)
        notas_text = tk.Text(main_frame, height=4, width=50)
        notas_text.grid(row=row, column=1, columnspan=2, sticky=tk.EW, pady=5, padx=(10, 0))
        if notas_var.get():
            notas_text.insert('1.0', notas_var.get())
        row += 1

        ttk.Label(main_frame, text="Ruta Documentos:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ruta_entry = ttk.Entry(main_frame, textvariable=ruta_var, width=40)
        ruta_entry.grid(row=row, column=1, sticky=tk.EW, pady=5, padx=(10, 0))
        ttk.Button(main_frame, text="Seleccionar", 
                  command=lambda: self._select_folder_for_dialog(ruta_var)).grid(row=row, column=2, pady=5, padx=(5, 0))
        row += 1

        # Alerta de inactividad
        inact_frame = ttk.Frame(main_frame)
        inact_frame.grid(row=row, column=0, columnspan=3, sticky=tk.EW, pady=5)
        
        inact_check = ttk.Checkbutton(inact_frame, text="Alerta de Inactividad", variable=inact_enabled_var)
        inact_check.pack(side=tk.LEFT)
        
        ttk.Label(inact_frame, text="Días:").pack(side=tk.LEFT, padx=(10, 5))
        inact_days_entry = ttk.Entry(inact_frame, textvariable=inact_days_var, width=10)
        inact_days_entry.pack(side=tk.LEFT)
        row += 1

        ttk.Label(main_frame, text="Etiquetas:").grid(row=row, column=0, sticky=tk.W, pady=5)
        etiquetas_entry = ttk.Entry(main_frame, textvariable=etiquetas_var, width=50)
        etiquetas_entry.grid(row=row, column=1, columnspan=2, sticky=tk.EW, pady=5, padx=(10, 0))
        
        ttk.Label(main_frame, text="(Separadas por comas)", font=('', 8)).grid(row=row+1, column=1, sticky=tk.W, padx=(10, 0))
        row += 2

        # Configurar expansión de columnas
        main_frame.columnconfigure(1, weight=1)

        # Botones
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=row, column=0, columnspan=3, pady=20)

        ttk.Button(buttons_frame, text="Guardar", 
                  command=lambda: self.save_case(case_id, cliente_id, caratula_var.get(), num_exp_var.get(),
                                                anio_var.get(), juzgado_var.get(), jurisdiccion_var.get(),
                                                etapa_var.get(), notas_text.get('1.0', tk.END).strip(),
                                                ruta_var.get(), inact_days_var.get(), inact_enabled_var.get(),
                                                etiquetas_var.get(), dialog)).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(buttons_frame, text="Cancelar", command=dialog.destroy).pack(side=tk.LEFT)

        # Focus en el primer campo
        caratula_entry.focus_set()

    def _select_folder_for_dialog(self, ruta_var):
        """Seleccionar carpeta para el diálogo"""
        folder = filedialog.askdirectory(title="Seleccionar Carpeta de Documentos")
        if folder:
            ruta_var.set(folder)

    def save_case(self, case_id, cliente_id, caratula, num_exp, anio, juzgado, jurisdiccion, etapa, notas, ruta, inact_days, inact_enabled, etiquetas_str, dialog):
        """Guardar caso (crear o actualizar)"""
        if not caratula.strip():
            messagebox.showwarning("Campo Requerido", "La carátula del caso es obligatoria.")
            return

        try:
            # Validar días de inactividad
            try:
                inact_days_int = int(inact_days) if inact_days.strip() else 0
            except ValueError:
                inact_days_int = 0

            if case_id:  # Editar caso existente
                self.db_crm.update_case(case_id, cliente_id, caratula, num_exp, anio, juzgado, 
                                       jurisdiccion, etapa, notas, ruta, inact_days_int, inact_enabled, etiquetas_str)
                messagebox.showinfo("Éxito", "Caso actualizado correctamente.")
            else:  # Crear nuevo caso
                self.db_crm.add_case(cliente_id, caratula, num_exp, anio, juzgado, 
                                    jurisdiccion, etapa, notas, ruta, inact_days_int, inact_enabled, etiquetas_str)
                messagebox.showinfo("Éxito", "Caso creado correctamente.")

            dialog.destroy()
            self.load_cases_by_client(self.current_client_id)  # Recargar la lista
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar caso: {e}")

    def delete_case(self):
        """Eliminar el caso seleccionado"""
        if not self.selected_case:
            messagebox.showwarning("Sin Selección", "Por favor, seleccione un caso para eliminar.")
            return

        # Confirmar eliminación
        response = messagebox.askyesno("Confirmar Eliminación", 
                                     f"¿Está seguro de que desea eliminar el caso '{self.selected_case['caratula']}'?\n\n"
                                     "ADVERTENCIA: Se eliminarán también todas las tareas, partes y actividades asociadas.")

        if response:
            try:
                self.db_crm.delete_case(self.selected_case['id'])
                messagebox.showinfo("Éxito", "Caso eliminado correctamente.")
                self.load_cases_by_client(self.current_client_id)  # Recargar la lista
                self.selected_case = None
                self.disable_case_buttons()
                
                # Notificar al controlador principal
                if hasattr(self.app_controller, 'on_case_deleted'):
                    self.app_controller.on_case_deleted()
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar caso: {e}")

    def select_case_folder(self):
        """Seleccionar carpeta de documentos para el caso"""
        if not self.selected_case:
            messagebox.showwarning("Sin Selección", "Seleccione un caso primero.")
            return

        folder = filedialog.askdirectory(title="Seleccionar Carpeta de Documentos del Caso")
        if folder:
            try:
                self.db_crm.update_case_folder(self.selected_case['id'], folder)
                messagebox.showinfo("Éxito", f"Carpeta asignada: {folder}")
                
                # Actualizar el caso seleccionado
                case_data = self.db_crm.get_case_by_id(self.selected_case['id'])
                if case_data:
                    self.selected_case = case_data
                    self.enable_case_buttons()  # Esto habilitará "Abrir Carpeta" si la ruta existe
                    
                    # Notificar al controlador principal
                    if hasattr(self.app_controller, 'on_case_folder_updated'):
                        self.app_controller.on_case_folder_updated(case_data)
                        
            except Exception as e:
                messagebox.showerror("Error", f"Error al asignar carpeta: {e}")

    def open_case_folder(self):
        """Abrir la carpeta de documentos del caso"""
        if not self.selected_case or not self.selected_case.get('ruta_documentos'):
            messagebox.showwarning("Sin Carpeta", "No hay carpeta asignada a este caso.")
            return

        folder_path = self.selected_case['ruta_documentos']
        if not os.path.exists(folder_path):
            messagebox.showerror("Carpeta no Encontrada", f"La carpeta no existe: {folder_path}")
            return

        try:
            import subprocess
            import sys
            
            if sys.platform == "win32":
                os.startfile(folder_path)
            elif sys.platform == "darwin":
                subprocess.call(["open", folder_path])
            else:
                subprocess.call(["xdg-open", folder_path])
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir carpeta: {e}")

    def refresh_data(self):
        """Refrescar los datos del módulo"""
        if self.current_client_id:
            self.load_cases_by_client(self.current_client_id)
            
            if self.selected_case:
                # Intentar mantener la selección actual
                try:
                    case_data = self.db_crm.get_case_by_id(self.selected_case['id'])
                    if case_data:
                        self.selected_case = case_data
                        self.enable_case_buttons()
                    else:
                        self.selected_case = None
                        self.disable_case_buttons()
                except:
                    self.selected_case = None
                    self.disable_case_buttons()

    def get_selected_case(self):
        """Obtener el caso seleccionado actualmente"""
        return self.selected_case

    def on_client_changed(self, client_data):
        """Manejar cambio de cliente seleccionado"""
        if client_data:
            self.load_cases_by_client(client_data['id'])
        else:
            self.clear_case_list()
