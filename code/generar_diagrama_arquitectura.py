#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

# Configurar matplotlib para manejar fuentes adecuadamente
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# Crear figura con tamaño amplio
fig, ax = plt.subplots(1, 1, figsize=(16, 12))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Colores del esquema
color_main = '#2E86AB'      # Azul principal
color_modules = '#A23B72'   # Rosa/púrpura para módulos
color_db = '#F18F01'        # Naranja para base de datos
color_ai = '#C73E1D'        # Rojo para IA
color_system = '#7FB069'    # Verde para sistema

# Título principal
ax.text(5, 9.5, 'Arquitectura Actual del CRM Legal', 
        fontsize=20, fontweight='bold', ha='center', va='center')
ax.text(5, 9.1, 'Branch: fix/dialogo-ia-botones - Estado: COMPLETAMENTE FUNCIONAL', 
        fontsize=12, ha='center', va='center', style='italic')

# 1. Aplicación Principal (main_app.py)
main_app = FancyBboxPatch((0.5, 7), 9, 1.5, 
                         boxstyle="round,pad=0.1", 
                         facecolor=color_main, 
                         edgecolor='black', 
                         linewidth=2,
                         alpha=0.8)
ax.add_patch(main_app)
ax.text(5, 7.75, 'APLICACIÓN PRINCIPAL (main_app.py)', 
        fontsize=14, fontweight='bold', ha='center', va='center', color='white')
ax.text(5, 7.4, '2,319 líneas • Diseño 3 columnas • Notebook con pestañas modulares', 
        fontsize=11, ha='center', va='center', color='white')
ax.text(5, 7.1, 'Gestión: Clientes, Casos, Audiencias, Calendario, Backup, Bandeja Sistema', 
        fontsize=10, ha='center', va='center', color='white')

# 2. Módulos UI (Pestañas)
modules_y = 5.5
module_width = 1.7
module_height = 1.2

# Módulo Partes
partes_box = FancyBboxPatch((0.3, modules_y), module_width, module_height, 
                           boxstyle="round,pad=0.05", 
                           facecolor=color_modules, 
                           edgecolor='black',
                           alpha=0.8)
ax.add_patch(partes_box)
ax.text(1.15, modules_y + 0.8, 'PARTES', fontsize=11, fontweight='bold', ha='center', va='center', color='white')
ax.text(1.15, modules_y + 0.5, 'partes_ui.py', fontsize=9, ha='center', va='center', color='white')
ax.text(1.15, modules_y + 0.3, '218 líneas', fontsize=8, ha='center', va='center', color='white')
ax.text(1.15, modules_y + 0.1, 'Gestión completa', fontsize=8, ha='center', va='center', color='white')

# Módulo Tareas
tareas_box = FancyBboxPatch((2.2, modules_y), module_width, module_height, 
                           boxstyle="round,pad=0.05", 
                           facecolor=color_modules, 
                           edgecolor='black',
                           alpha=0.8)
ax.add_patch(tareas_box)
ax.text(3.05, modules_y + 0.8, 'TAREAS', fontsize=11, fontweight='bold', ha='center', va='center', color='white')
ax.text(3.05, modules_y + 0.5, 'tareas_ui.py', fontsize=9, ha='center', va='center', color='white')
ax.text(3.05, modules_y + 0.3, '344 líneas', fontsize=8, ha='center', va='center', color='white')
ax.text(3.05, modules_y + 0.1, 'Plazos + Recordatorios', fontsize=8, ha='center', va='center', color='white')

# Módulo Seguimiento
seguimiento_box = FancyBboxPatch((4.1, modules_y), module_width, module_height, 
                                boxstyle="round,pad=0.05", 
                                facecolor=color_modules, 
                                edgecolor='black',
                                alpha=0.8)
ax.add_patch(seguimiento_box)
ax.text(4.95, modules_y + 0.8, 'SEGUIMIENTO', fontsize=11, fontweight='bold', ha='center', va='center', color='white')
ax.text(4.95, modules_y + 0.5, 'seguimiento_ui.py', fontsize=9, ha='center', va='center', color='white')
ax.text(4.95, modules_y + 0.3, '237 líneas', fontsize=8, ha='center', va='center', color='white')
ax.text(4.95, modules_y + 0.1, 'Actividades casos', fontsize=8, ha='center', va='center', color='white')

# Documentos y Detalles (dentro de main_app)
docs_box = FancyBboxPatch((6, modules_y), module_width, module_height, 
                         boxstyle="round,pad=0.05", 
                         facecolor=color_main, 
                         edgecolor='black',
                         alpha=0.6)
ax.add_patch(docs_box)
ax.text(6.85, modules_y + 0.8, 'DOCUMENTOS', fontsize=11, fontweight='bold', ha='center', va='center', color='white')
ax.text(6.85, modules_y + 0.5, 'En main_app.py', fontsize=9, ha='center', va='center', color='white')
ax.text(6.85, modules_y + 0.3, 'Gestión archivos', fontsize=8, ha='center', va='center', color='white')
ax.text(6.85, modules_y + 0.1, 'por caso', fontsize=8, ha='center', va='center', color='white')

# Detalles del Caso
detalles_box = FancyBboxPatch((7.9, modules_y), module_width, module_height, 
                             boxstyle="round,pad=0.05", 
                             facecolor=color_main, 
                             edgecolor='black',
                             alpha=0.6)
ax.add_patch(detalles_box)
ax.text(8.75, modules_y + 0.8, 'DETALLES', fontsize=11, fontweight='bold', ha='center', va='center', color='white')
ax.text(8.75, modules_y + 0.5, 'En main_app.py', fontsize=9, ha='center', va='center', color='white')
ax.text(8.75, modules_y + 0.3, 'Info completa', fontsize=8, ha='center', va='center', color='white')
ax.text(8.75, modules_y + 0.1, 'del caso', fontsize=8, ha='center', va='center', color='white')

# 3. Sistema de IA Local
ai_box = FancyBboxPatch((0.5, 3.5), 4, 1.2, 
                       boxstyle="round,pad=0.1", 
                       facecolor=color_ai, 
                       edgecolor='black',
                       linewidth=2,
                       alpha=0.8)
ax.add_patch(ai_box)
ax.text(2.5, 4.3, 'SISTEMA DE IA LOCAL (mcp_server.py)', 
        fontsize=12, fontweight='bold', ha='center', va='center', color='white')
ax.text(2.5, 4.0, 'Servidor Flask • Puerto 5000 • Ollama/LM Studio', 
        fontsize=10, ha='center', va='center', color='white')
ax.text(2.5, 3.75, 'Endpoint: /api/reformular_hechos • Modelo: gemma3:4b', 
        fontsize=10, ha='center', va='center', color='white')

# 4. Base de Datos
db_box = FancyBboxPatch((5.5, 3.5), 4, 1.2, 
                       boxstyle="round,pad=0.1", 
                       facecolor=color_db, 
                       edgecolor='black',
                       linewidth=2,
                       alpha=0.8)
ax.add_patch(db_box)
ax.text(7.5, 4.3, 'BASE DE DATOS (crm_database.py)', 
        fontsize=12, fontweight='bold', ha='center', va='center', color='white')
ax.text(7.5, 4.0, 'SQLite • 10 tablas • Foreign Keys • Índices optimizados', 
        fontsize=10, ha='center', va='center', color='white')
ax.text(7.5, 3.75, 'clientes, casos, partes, tareas, actividades, audiencias, etiquetas', 
        fontsize=9, ha='center', va='center', color='white')

# 5. Servicios del Sistema
system_y = 2
system_width = 1.8
system_height = 1

# Bandeja Sistema
bandeja_box = FancyBboxPatch((0.5, system_y), system_width, system_height, 
                            boxstyle="round,pad=0.05", 
                            facecolor=color_system, 
                            edgecolor='black',
                            alpha=0.8)
ax.add_patch(bandeja_box)
ax.text(1.4, system_y + 0.7, 'BANDEJA', fontsize=10, fontweight='bold', ha='center', va='center', color='white')
ax.text(1.4, system_y + 0.5, 'pystray', fontsize=9, ha='center', va='center', color='white')
ax.text(1.4, system_y + 0.3, 'Threading', fontsize=8, ha='center', va='center', color='white')
ax.text(1.4, system_y + 0.1, 'Notificaciones', fontsize=8, ha='center', va='center', color='white')

# Backup
backup_box = FancyBboxPatch((2.6, system_y), system_width, system_height, 
                           boxstyle="round,pad=0.05", 
                           facecolor=color_system, 
                           edgecolor='black',
                           alpha=0.8)
ax.add_patch(backup_box)
ax.text(3.5, system_y + 0.7, 'BACKUP', fontsize=10, fontweight='bold', ha='center', va='center', color='white')
ax.text(3.5, system_y + 0.5, 'shutil.copy2', fontsize=9, ha='center', va='center', color='white')
ax.text(3.5, system_y + 0.3, 'Timestamp', fontsize=8, ha='center', va='center', color='white')
ax.text(3.5, system_y + 0.1, 'automático', fontsize=8, ha='center', va='center', color='white')

# Calendario
calendario_box = FancyBboxPatch((4.7, system_y), system_width, system_height, 
                               boxstyle="round,pad=0.05", 
                               facecolor=color_system, 
                               edgecolor='black',
                               alpha=0.8)
ax.add_patch(calendario_box)
ax.text(5.6, system_y + 0.7, 'CALENDARIO', fontsize=10, fontweight='bold', ha='center', va='center', color='white')
ax.text(5.6, system_y + 0.5, 'tkcalendar', fontsize=9, ha='center', va='center', color='white')
ax.text(5.6, system_y + 0.3, 'Audiencias', fontsize=8, ha='center', va='center', color='white')
ax.text(5.6, system_y + 0.1, 'Recordatorios', fontsize=8, ha='center', va='center', color='white')

# Firebase
firebase_box = FancyBboxPatch((6.8, system_y), system_width, system_height, 
                             boxstyle="round,pad=0.05", 
                             facecolor=color_system, 
                             edgecolor='black',
                             alpha=0.8)
ax.add_patch(firebase_box)
ax.text(7.7, system_y + 0.7, 'FIREBASE', fontsize=10, fontweight='bold', ha='center', va='center', color='white')
ax.text(7.7, system_y + 0.5, 'Admin SDK', fontsize=9, ha='center', va='center', color='white')
ax.text(7.7, system_y + 0.3, 'Configurado', fontsize=8, ha='center', va='center', color='white')
ax.text(7.7, system_y + 0.1, 'Ready', fontsize=8, ha='center', va='center', color='white')

# Conexiones entre componentes
# Main app a módulos
for x_pos in [1.15, 3.05, 4.95, 6.85, 8.75]:
    arrow = ConnectionPatch((x_pos, 7), (x_pos, modules_y + module_height), 
                           "data", "data", 
                           arrowstyle="->", 
                           shrinkA=5, shrinkB=5, 
                           mutation_scale=20, 
                           fc="black", 
                           alpha=0.6)
    ax.add_patch(arrow)

# Main app a IA
arrow_ai = ConnectionPatch((2.5, 7), (2.5, 4.7), 
                          "data", "data", 
                          arrowstyle="<->", 
                          shrinkA=5, shrinkB=5, 
                          mutation_scale=20, 
                          fc="red", 
                          alpha=0.8,
                          linewidth=2)
ax.add_patch(arrow_ai)

# Main app a DB
arrow_db = ConnectionPatch((7.5, 7), (7.5, 4.7), 
                          "data", "data", 
                          arrowstyle="<->", 
                          shrinkA=5, shrinkB=5, 
                          mutation_scale=20, 
                          fc="orange", 
                          alpha=0.8,
                          linewidth=2)
ax.add_patch(arrow_db)

# Módulos a DB
for x_pos in [1.15, 3.05, 4.95]:
    arrow = ConnectionPatch((x_pos, modules_y), (7.5, 4.7), 
                           "data", "data", 
                           arrowstyle="->", 
                           shrinkA=5, shrinkB=5, 
                           mutation_scale=15, 
                           fc="orange", 
                           alpha=0.5)
    ax.add_patch(arrow)

# Leyenda
legend_elements = [
    mpatches.Patch(color=color_main, label='Aplicación Principal'),
    mpatches.Patch(color=color_modules, label='Módulos UI Especializados'),
    mpatches.Patch(color=color_ai, label='Sistema de IA Local'),
    mpatches.Patch(color=color_db, label='Base de Datos'),
    mpatches.Patch(color=color_system, label='Servicios del Sistema')
]

ax.legend(handles=legend_elements, loc='lower center', ncol=3, 
         bbox_to_anchor=(0.5, -0.05), fontsize=10)

# Información adicional
ax.text(0.5, 0.7, 'FUNCIONALIDADES CRÍTICAS IMPLEMENTADAS:', 
        fontsize=12, fontweight='bold', ha='left', va='center')
ax.text(0.5, 0.4, '✅ Sistema de IA con reformulación de hechos jurídicos', 
        fontsize=10, ha='left', va='center', color='darkgreen')
ax.text(0.5, 0.2, '✅ Gestión completa de partes intervinientes', 
        fontsize=10, ha='left', va='center', color='darkgreen')
ax.text(0.5, 0.0, '✅ Sistema avanzado de tareas y plazos procesales', 
        fontsize=10, ha='left', va='center', color='darkgreen')

ax.text(5.5, 0.4, '✅ Seguimiento completo de actividades', 
        fontsize=10, ha='left', va='center', color='darkgreen')
ax.text(5.5, 0.2, '✅ Calendario de audiencias con recordatorios', 
        fontsize=10, ha='left', va='center', color='darkgreen')
ax.text(5.5, 0.0, '✅ Sistema de etiquetas (base de datos lista)', 
        fontsize=10, ha='left', va='center', color='darkgreen')

plt.tight_layout()
plt.savefig('/workspace/charts/arquitectura_crm_legal_actual.png', 
           dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close()

print("✅ Diagrama de arquitectura generado: /workspace/charts/arquitectura_crm_legal_actual.png")
