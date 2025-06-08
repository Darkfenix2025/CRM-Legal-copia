
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
