# compatibility_wrapper.py
"""
Wrapper de compatibilidad temporal para el CRM Legal
Este archivo proporciona las funciones que faltan en crm_database.py
"""

import crm_database as db

# Crear aliases para las funciones con nombres diferentes
def get_dates_with_audiencias():
    """Alias para get_fechas_con_audiencias"""
    return db.get_fechas_con_audiencias()

def get_audiencias_by_date(fecha):
    """Alias para get_audiencias_by_fecha"""
    return db.get_audiencias_by_fecha(fecha)

def get_all_etiquetas_safe():
    """Obtiene etiquetas de forma segura sin columnas que podrían no existir"""
    try:
        return db.get_todas_las_etiquetas()
    except Exception as e:
        print(f"Error obteniendo etiquetas: {e}")
        return []

# Hacer que este módulo actúe como proxy de crm_database
def __getattr__(name):
    """Delega cualquier función no definida aquí al módulo original"""
    return getattr(db, name)
