
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
