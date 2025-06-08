# documentos_ui.py
import tkinter as tk
from tkinter import ttk, messagebox
import os
import subprocess
import sys

class DocumentosTab(ttk.Frame):
    def __init__(self, parent, app_controller, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.app_controller = app_controller
        self.db_crm = self.app_controller.db_crm
        self.current_case = None
        self.current_folder_path = None
        self._create_widgets()

    def _create_widgets(self):
        # Configurar el frame principal
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)  # Información del caso
        self.rowconfigure(1, weight=1)  # Lista de documentos

        # --- Información del Caso Actual ---
        info_frame = ttk.LabelFrame(self, text="Información del Caso", padding="5")
        info_frame.grid(row=0, column=0, sticky='ew', pady=(0, 5))
        info_frame.columnconfigure(1, weight=1)

        ttk.Label(info_frame, text="Caso:").grid(row=0, column=0, sticky=tk.W, pady=2, padx=5)
        self.case_info_lbl = ttk.Label(info_frame, text="Ningún caso seleccionado", wraplength=400)
        self.case_info_lbl.grid(row=0, column=1, sticky=tk.EW, pady=2, padx=5)

        ttk.Label(info_frame, text="Carpeta:").grid(row=1, column=0, sticky=tk.W, pady=2, padx=5)
        self.folder_path_lbl = ttk.Label(info_frame, text="Sin carpeta asignada", wraplength=400, foreground="gray")
        self.folder_path_lbl.grid(row=1, column=1, sticky=tk.EW, pady=2, padx=5)

        # --- Lista de Documentos ---
        docs_frame = ttk.LabelFrame(self, text="Documentos del Caso", padding="5")
        docs_frame.grid(row=1, column=0, sticky='nsew', pady=(5, 0))
        docs_frame.columnconfigure(0, weight=1)
        docs_frame.rowconfigure(0, weight=1)
        docs_frame.rowconfigure(1, weight=0)

        # TreeView de documentos
        docs_cols = ('Nombre', 'Tipo', 'Tamaño', 'Modificado')
        self.docs_tree = ttk.Treeview(docs_frame, columns=docs_cols, show='tree headings', selectmode='browse')
        
        # Configurar columnas
        self.docs_tree.heading('#0', text='Estructura')
        self.docs_tree.heading('Nombre', text='Nombre')
        self.docs_tree.heading('Tipo', text='Tipo')
        self.docs_tree.heading('Tamaño', text='Tamaño')
        self.docs_tree.heading('Modificado', text='Última Modificación')

        self.docs_tree.column('#0', width=200, stretch=True)
        self.docs_tree.column('Nombre', width=250, stretch=True)
        self.docs_tree.column('Tipo', width=100, stretch=tk.NO)
        self.docs_tree.column('Tamaño', width=100, stretch=tk.NO)
        self.docs_tree.column('Modificado', width=150, stretch=tk.NO)

        # Scrollbars para documentos
        docs_scrollbar_y = ttk.Scrollbar(docs_frame, orient=tk.VERTICAL, command=self.docs_tree.yview)
        self.docs_tree.configure(yscrollcommand=docs_scrollbar_y.set)
        docs_scrollbar_y.grid(row=0, column=1, sticky='ns')

        docs_scrollbar_x = ttk.Scrollbar(docs_frame, orient=tk.HORIZONTAL, command=self.docs_tree.xview)
        self.docs_tree.configure(xscrollcommand=docs_scrollbar_x.set)
        docs_scrollbar_x.grid(row=1, column=0, sticky='ew')

        self.docs_tree.grid(row=0, column=0, sticky='nsew')

        # Bind para doble click
        self.docs_tree.bind('<Double-1>', self.on_document_double_click)

        # --- Botones de Acción ---
        buttons_frame = ttk.Frame(docs_frame)
        buttons_frame.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(10, 0))
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)
        buttons_frame.columnconfigure(2, weight=1)
        buttons_frame.columnconfigure(3, weight=1)

        self.refresh_btn = ttk.Button(buttons_frame, text="Actualizar", command=self.refresh_documents)
        self.refresh_btn.grid(row=0, column=0, sticky='ew', padx=(0, 5))

        self.open_btn = ttk.Button(buttons_frame, text="Abrir", command=self.open_selected_document, state=tk.DISABLED)
        self.open_btn.grid(row=0, column=1, sticky='ew', padx=5)

        self.open_folder_btn = ttk.Button(buttons_frame, text="Abrir Carpeta", command=self.open_current_folder, state=tk.DISABLED)
        self.open_folder_btn.grid(row=0, column=2, sticky='ew', padx=5)

        self.show_path_btn = ttk.Button(buttons_frame, text="Mostrar Ruta", command=self.show_selected_path, state=tk.DISABLED)
        self.show_path_btn.grid(row=0, column=3, sticky='ew', padx=(5, 0))

        # Bind para selección
        self.docs_tree.bind('<<TreeviewSelect>>', self.on_document_select)

        # Estado inicial
        self.update_display_for_no_case()

    def on_case_changed(self, case_data):
        """Manejar cambio de caso seleccionado"""
        self.current_case = case_data
        if case_data:
            self.update_display_for_case(case_data)
            self.load_case_documents(case_data.get('ruta_documentos'))
        else:
            self.update_display_for_no_case()

    def update_display_for_case(self, case_data):
        """Actualizar visualización cuando hay un caso seleccionado"""
        caratula = case_data.get('caratula', 'Sin carátula')
        self.case_info_lbl.config(text=f"{caratula} (ID: {case_data['id']})")
        
        ruta = case_data.get('ruta_documentos', '')
        if ruta and os.path.exists(ruta):
            self.folder_path_lbl.config(text=ruta, foreground="black")
            self.current_folder_path = ruta
            self.open_folder_btn.config(state=tk.NORMAL)
        else:
            self.folder_path_lbl.config(text="Sin carpeta asignada o carpeta no existe", foreground="red")
            self.current_folder_path = None
            self.open_folder_btn.config(state=tk.DISABLED)

    def update_display_for_no_case(self):
        """Actualizar visualización cuando no hay caso seleccionado"""
        self.case_info_lbl.config(text="Ningún caso seleccionado")
        self.folder_path_lbl.config(text="Sin carpeta asignada", foreground="gray")
        self.current_folder_path = None
        self.clear_document_list()
        self.open_folder_btn.config(state=tk.DISABLED)

    def load_case_documents(self, folder_path):
        """Cargar documentos del caso desde la carpeta especificada"""
        self.clear_document_list()
        
        if not folder_path or not os.path.exists(folder_path):
            # Insertar mensaje de que no hay carpeta
            self.docs_tree.insert('', 'end', text="No hay carpeta asignada o la carpeta no existe", 
                                 values=('', '', '', ''), tags=('no_folder',))
            self.docs_tree.tag_configure('no_folder', foreground='red')
            return

        try:
            self._load_directory_recursive(folder_path, '')
            
            # Si no hay documentos, mostrar mensaje
            if not self.docs_tree.get_children():
                self.docs_tree.insert('', 'end', text="Carpeta vacía", 
                                     values=('', '', '', ''), tags=('empty',))
                self.docs_tree.tag_configure('empty', foreground='gray')
                
        except PermissionError:
            self.docs_tree.insert('', 'end', text="Sin permisos para acceder a la carpeta", 
                                 values=('', '', '', ''), tags=('error',))
            self.docs_tree.tag_configure('error', foreground='red')
        except Exception as e:
            self.docs_tree.insert('', 'end', text=f"Error al cargar documentos: {str(e)}", 
                                 values=('', '', '', ''), tags=('error',))
            self.docs_tree.tag_configure('error', foreground='red')

    def _load_directory_recursive(self, directory_path, parent_item, max_depth=3, current_depth=0):
        """Cargar directorio de forma recursiva con límite de profundidad"""
        if current_depth >= max_depth:
            return

        try:
            items = os.listdir(directory_path)
            items.sort()  # Ordenar alfabéticamente

            # Separar directorios y archivos
            directories = []
            files = []
            
            for item in items:
                item_path = os.path.join(directory_path, item)
                if os.path.isdir(item_path):
                    directories.append(item)
                else:
                    files.append(item)

            # Insertar directorios primero
            for directory in directories:
                dir_path = os.path.join(directory_path, directory)
                try:
                    # Contar items en el directorio
                    item_count = len(os.listdir(dir_path))
                    dir_node = self.docs_tree.insert(parent_item, 'end', 
                                                   text=f"📁 {directory}",
                                                   values=(directory, 'Carpeta', f"{item_count} elementos", 
                                                          self._get_modification_time(dir_path)),
                                                   tags=('directory',))
                    
                    # Cargar subdirectorios recursivamente
                    self._load_directory_recursive(dir_path, dir_node, max_depth, current_depth + 1)
                    
                except PermissionError:
                    self.docs_tree.insert(parent_item, 'end', 
                                        text=f"📁 {directory} (Sin acceso)",
                                        values=(directory, 'Carpeta', 'Sin acceso', ''),
                                        tags=('no_access',))

            # Insertar archivos
            for file in files:
                file_path = os.path.join(directory_path, file)
                try:
                    file_size = self._format_file_size(os.path.getsize(file_path))
                    file_ext = os.path.splitext(file)[1].lower()
                    file_type = self._get_file_type_description(file_ext)
                    
                    # Icono según el tipo de archivo
                    icon = self._get_file_icon(file_ext)
                    
                    self.docs_tree.insert(parent_item, 'end',
                                        text=f"{icon} {file}",
                                        values=(file, file_type, file_size, 
                                               self._get_modification_time(file_path)),
                                        tags=('file',))
                except (PermissionError, OSError):
                    self.docs_tree.insert(parent_item, 'end',
                                        text=f"📄 {file} (Error)",
                                        values=(file, 'Error', 'N/A', ''),
                                        tags=('error',))

            # Configurar tags
            self.docs_tree.tag_configure('directory', foreground='blue')
            self.docs_tree.tag_configure('file', foreground='black')
            self.docs_tree.tag_configure('no_access', foreground='red')
            self.docs_tree.tag_configure('error', foreground='red')

        except Exception as e:
            print(f"Error al cargar directorio {directory_path}: {e}")

    def _get_modification_time(self, file_path):
        """Obtener tiempo de modificación formateado"""
        try:
            import datetime
            timestamp = os.path.getmtime(file_path)
            return datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M")
        except:
            return "N/A"

    def _format_file_size(self, size_bytes):
        """Formatear tamaño de archivo en formato legible"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"

    def _get_file_type_description(self, extension):
        """Obtener descripción del tipo de archivo"""
        file_types = {
            '.pdf': 'PDF',
            '.doc': 'Word',
            '.docx': 'Word',
            '.xls': 'Excel',
            '.xlsx': 'Excel',
            '.ppt': 'PowerPoint',
            '.pptx': 'PowerPoint',
            '.txt': 'Texto',
            '.rtf': 'RTF',
            '.jpg': 'Imagen',
            '.jpeg': 'Imagen',
            '.png': 'Imagen',
            '.gif': 'Imagen',
            '.bmp': 'Imagen',
            '.tiff': 'Imagen',
            '.zip': 'Archivo',
            '.rar': 'Archivo',
            '.7z': 'Archivo',
            '.mp4': 'Video',
            '.avi': 'Video',
            '.mov': 'Video',
            '.mp3': 'Audio',
            '.wav': 'Audio',
            '.html': 'Web',
            '.htm': 'Web',
            '.xml': 'XML',
            '.json': 'JSON',
            '.csv': 'CSV'
        }
        return file_types.get(extension, 'Documento')

    def _get_file_icon(self, extension):
        """Obtener icono para el tipo de archivo"""
        icons = {
            '.pdf': '📄',
            '.doc': '📝',
            '.docx': '📝',
            '.xls': '📊',
            '.xlsx': '📊',
            '.ppt': '📽️',
            '.pptx': '📽️',
            '.txt': '📄',
            '.rtf': '📄',
            '.jpg': '🖼️',
            '.jpeg': '🖼️',
            '.png': '🖼️',
            '.gif': '🖼️',
            '.bmp': '🖼️',
            '.tiff': '🖼️',
            '.zip': '📦',
            '.rar': '📦',
            '.7z': '📦',
            '.mp4': '🎬',
            '.avi': '🎬',
            '.mov': '🎬',
            '.mp3': '🎵',
            '.wav': '🎵',
            '.html': '🌐',
            '.htm': '🌐',
            '.xml': '⚙️',
            '.json': '⚙️',
            '.csv': '📊'
        }
        return icons.get(extension, '📄')

    def clear_document_list(self):
        """Limpiar la lista de documentos"""
        for item in self.docs_tree.get_children():
            self.docs_tree.delete(item)

    def on_document_select(self, event):
        """Manejar selección de documento"""
        selected_items = self.docs_tree.selection()
        if selected_items:
            selected_item = selected_items[0]
            item_tags = self.docs_tree.item(selected_item, 'tags')
            
            # Habilitar botones según el tipo de item seleccionado
            if 'file' in item_tags:
                self.open_btn.config(state=tk.NORMAL)
                self.show_path_btn.config(state=tk.NORMAL)
            elif 'directory' in item_tags:
                self.open_btn.config(state=tk.NORMAL)  # Puede abrir carpetas también
                self.show_path_btn.config(state=tk.NORMAL)
            else:
                self.open_btn.config(state=tk.DISABLED)
                self.show_path_btn.config(state=tk.DISABLED)
        else:
            self.open_btn.config(state=tk.DISABLED)
            self.show_path_btn.config(state=tk.DISABLED)

    def on_document_double_click(self, event):
        """Manejar doble click en documento"""
        self.open_selected_document()

    def open_selected_document(self):
        """Abrir el documento seleccionado"""
        selected_items = self.docs_tree.selection()
        if not selected_items:
            return

        selected_item = selected_items[0]
        file_path = self._get_full_path_from_tree_item(selected_item)
        
        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("Error", "El archivo o carpeta seleccionado no existe.")
            return

        try:
            if sys.platform == "win32":
                os.startfile(file_path)
            elif sys.platform == "darwin":
                subprocess.call(["open", file_path])
            else:
                subprocess.call(["xdg-open", file_path])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{e}")

    def _get_full_path_from_tree_item(self, item):
        """Obtener la ruta completa de un item del TreeView"""
        if not self.current_folder_path:
            return None

        # Construir la ruta navegando hacia arriba en el árbol
        path_parts = []
        current_item = item
        
        while current_item:
            item_text = self.docs_tree.item(current_item, 'text')
            # Remover iconos del texto
            item_text = item_text.replace('📁 ', '').replace('📄 ', '').replace('🖼️ ', '').replace('📝 ', '').replace('📊 ', '').replace('📽️ ', '').replace('📦 ', '').replace('🎬 ', '').replace('🎵 ', '').replace('🌐 ', '').replace('⚙️ ', '')
            
            # Limpiar sufijos como "(Sin acceso)" o "(Error)"
            if ' (' in item_text:
                item_text = item_text.split(' (')[0]
            
            path_parts.insert(0, item_text)
            current_item = self.docs_tree.parent(current_item)

        # Construir ruta completa
        full_path = self.current_folder_path
        for part in path_parts:
            if part:  # Evitar partes vacías
                full_path = os.path.join(full_path, part)

        return full_path

    def open_current_folder(self):
        """Abrir la carpeta actual del caso"""
        if not self.current_folder_path or not os.path.exists(self.current_folder_path):
            messagebox.showerror("Error", "No hay carpeta asignada o la carpeta no existe.")
            return

        try:
            if sys.platform == "win32":
                os.startfile(self.current_folder_path)
            elif sys.platform == "darwin":
                subprocess.call(["open", self.current_folder_path])
            else:
                subprocess.call(["xdg-open", self.current_folder_path])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la carpeta:\n{e}")

    def show_selected_path(self):
        """Mostrar la ruta completa del elemento seleccionado"""
        selected_items = self.docs_tree.selection()
        if not selected_items:
            return

        selected_item = selected_items[0]
        file_path = self._get_full_path_from_tree_item(selected_item)
        
        if file_path:
            # Crear diálogo para mostrar la ruta
            dialog = tk.Toplevel(self.app_controller.root)
            dialog.title("Ruta del Archivo")
            dialog.transient(self.app_controller.root)
            dialog.grab_set()
            dialog.geometry("600x150")
            dialog.resizable(True, False)

            main_frame = ttk.Frame(dialog, padding="20")
            main_frame.pack(fill=tk.BOTH, expand=True)

            ttk.Label(main_frame, text="Ruta completa:").pack(anchor=tk.W)
            
            # Entry para mostrar la ruta (permite copiar)
            path_var = tk.StringVar(value=file_path)
            path_entry = ttk.Entry(main_frame, textvariable=path_var, state='readonly', width=80)
            path_entry.pack(fill=tk.X, pady=(5, 10))

            # Botón para copiar al portapapeles
            def copy_to_clipboard():
                dialog.clipboard_clear()
                dialog.clipboard_append(file_path)
                messagebox.showinfo("Copiado", "Ruta copiada al portapapeles.")

            ttk.Button(main_frame, text="Copiar al Portapapeles", command=copy_to_clipboard).pack()

    def refresh_documents(self):
        """Refrescar la lista de documentos"""
        if self.current_case and self.current_case.get('ruta_documentos'):
            self.load_case_documents(self.current_case['ruta_documentos'])
        else:
            self.clear_document_list()

    def refresh_data(self):
        """Refrescar los datos del módulo"""
        self.refresh_documents()

    def get_current_case(self):
        """Obtener el caso actual"""
        return self.current_case

    def get_current_folder_path(self):
        """Obtener la ruta de la carpeta actual"""
        return self.current_folder_path
