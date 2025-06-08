#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Configurar matplotlib para fuentes
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# Crear figura con subplots
fig = plt.figure(figsize=(16, 10))

# Datos de las branches
branches = ['main', 'feature/seguimiento-casos', 'feature/gestion-partes', 'feature/modulo-tareas', 'fix/dialogo-ia-botones']
main_app_lines = [918, 918, 1000, 1200, 2319]

# Funcionalidades por branch
funcionalidades = {
    'main': ['Base CRM', 'Audiencias', 'Seguimiento básico', 'Bandeja sistema'],
    'feature/seguimiento-casos': ['Base CRM', 'Audiencias', 'Seguimiento v1', 'Bandeja sistema'],
    'feature/gestion-partes': ['Base CRM', 'Audiencias', 'Seguimiento', 'Bandeja sistema', 'Partes completo'],
    'feature/modulo-tareas': ['Base CRM', 'Audiencias', 'Seguimiento', 'Bandeja sistema', 'Partes completo', 'Tareas completo'],
    'fix/dialogo-ia-botones': ['Base CRM', 'Audiencias', 'Seguimiento avanzado', 'Bandeja sistema', 'Partes completo', 'Tareas completo', 'Sistema IA', 'Firebase', 'Backup avanzado']
}

# Subplot 1: Evolución del código
ax1 = plt.subplot(2, 2, 1)
colors = ['#3498db', '#e74c3c', '#f39c12', '#2ecc71', '#9b59b6']
bars = ax1.bar(range(len(branches)), main_app_lines, color=colors, alpha=0.8)

# Agregar valores en las barras
for i, (bar, lines) in enumerate(zip(bars, main_app_lines)):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + 50,
             f'{lines}', ha='center', va='bottom', fontweight='bold')

ax1.set_title('Evolución del Código (main_app.py)', fontsize=14, fontweight='bold')
ax1.set_ylabel('Líneas de Código', fontsize=12)
ax1.set_xticks(range(len(branches)))
ax1.set_xticklabels([b.replace('feature/', 'f/').replace('origin/', '') for b in branches], 
                    rotation=45, ha='right')
ax1.grid(axis='y', alpha=0.3)

# Subplot 2: Archivos únicos por branch
ax2 = plt.subplot(2, 2, 2)
archivos_unicos = {
    'main': 0,
    'feature/seguimiento-casos': 0,
    'feature/gestion-partes': 1,  # partes_ui.py
    'feature/modulo-tareas': 1,   # tareas_ui.py
    'fix/dialogo-ia-botones': 2   # mcp_server.py + firebase
}

archivos_data = [archivos_unicos[b] for b in branches]
bars2 = ax2.bar(range(len(branches)), archivos_data, color=colors, alpha=0.8)

for i, (bar, count) in enumerate(zip(bars2, archivos_data)):
    if count > 0:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                 f'{count}', ha='center', va='bottom', fontweight='bold')

ax2.set_title('Archivos Únicos por Branch', fontsize=14, fontweight='bold')
ax2.set_ylabel('Cantidad de Archivos Únicos', fontsize=12)
ax2.set_xticks(range(len(branches)))
ax2.set_xticklabels([b.replace('feature/', 'f/').replace('origin/', '') for b in branches], 
                    rotation=45, ha='right')
ax2.grid(axis='y', alpha=0.3)

# Subplot 3: Número de funcionalidades
ax3 = plt.subplot(2, 2, 3)
num_funcionalidades = [len(funcionalidades[b]) for b in branches]
bars3 = ax3.bar(range(len(branches)), num_funcionalidades, color=colors, alpha=0.8)

for i, (bar, count) in enumerate(zip(bars3, num_funcionalidades)):
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height + 0.1,
             f'{count}', ha='center', va='bottom', fontweight='bold')

ax3.set_title('Número Total de Funcionalidades', fontsize=14, fontweight='bold')
ax3.set_ylabel('Cantidad de Funcionalidades', fontsize=12)
ax3.set_xticks(range(len(branches)))
ax3.set_xticklabels([b.replace('feature/', 'f/').replace('origin/', '') for b in branches], 
                    rotation=45, ha='right')
ax3.grid(axis='y', alpha=0.3)

# Subplot 4: Matriz de funcionalidades
ax4 = plt.subplot(2, 2, 4)

# Crear matriz de funcionalidades
todas_funcionalidades = ['Base CRM', 'Audiencias', 'Seguimiento básico', 'Seguimiento v1', 
                        'Seguimiento avanzado', 'Bandeja sistema', 'Partes completo', 
                        'Tareas completo', 'Sistema IA', 'Firebase', 'Backup avanzado']

matriz = np.zeros((len(branches), len(todas_funcionalidades)))

funcionalidades_map = {
    'main': [1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0],
    'feature/seguimiento-casos': [1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0],
    'feature/gestion-partes': [1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0],
    'feature/modulo-tareas': [1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0],
    'fix/dialogo-ia-botones': [1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1]
}

for i, branch in enumerate(branches):
    matriz[i] = funcionalidades_map[branch]

im = ax4.imshow(matriz, cmap='RdYlGn', aspect='auto', alpha=0.8)
ax4.set_title('Matriz de Funcionalidades por Branch', fontsize=14, fontweight='bold')
ax4.set_yticks(range(len(branches)))
ax4.set_yticklabels([b.replace('feature/', 'f/').replace('origin/', '') for b in branches])
ax4.set_xticks(range(len(todas_funcionalidades)))
ax4.set_xticklabels(todas_funcionalidades, rotation=45, ha='right')

# Agregar texto en las celdas
for i in range(len(branches)):
    for j in range(len(todas_funcionalidades)):
        text = '✓' if matriz[i, j] == 1 else '✗'
        color = 'white' if matriz[i, j] == 1 else 'red'
        ax4.text(j, i, text, ha='center', va='center', 
                color=color, fontweight='bold', fontsize=10)

# Título general
fig.suptitle('Análisis Comparativo Completo - Todas las Branches del CRM Legal', 
             fontsize=16, fontweight='bold', y=0.95)

# Información adicional
info_text = """
ANÁLISIS COMPLETADO: 5 branches analizadas (100%)
RESULTADO CLAVE: fix/dialogo-ia-botones contiene TODAS las funcionalidades + IA
RECOMENDACIÓN: Usar como base única para integración del sistema financiero
"""

plt.figtext(0.02, 0.02, info_text, fontsize=10, 
           bbox=dict(boxstyle="round,pad=0.5", facecolor='lightblue', alpha=0.8))

plt.tight_layout()
plt.subplots_adjust(top=0.9, bottom=0.15)
plt.savefig('/workspace/charts/comparativo_completo_branches.png', 
           dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close()

print("✅ Gráfico comparativo completo generado: /workspace/charts/comparativo_completo_branches.png")

# Crear segundo gráfico: Timeline de desarrollo
fig2, ax = plt.subplots(1, 1, figsize=(14, 8))

# Datos del timeline
timeline_data = {
    'main': {'pos': 0, 'fecha': 'Base', 'funcionalidades': 4, 'color': '#3498db'},
    'feature/seguimiento-casos': {'pos': 1, 'fecha': 'Desarrollo\nSeguimiento', 'funcionalidades': 4, 'color': '#e74c3c'},
    'feature/gestion-partes': {'pos': 2, 'fecha': 'Desarrollo\nPartes', 'funcionalidades': 5, 'color': '#f39c12'},
    'feature/modulo-tareas': {'pos': 3, 'fecha': 'Desarrollo\nTareas', 'funcionalidades': 6, 'color': '#2ecc71'},
    'fix/dialogo-ia-botones': {'pos': 4, 'fecha': 'Integración\nFinal + IA', 'funcionalidades': 9, 'color': '#9b59b6'}
}

# Dibujar timeline
for i, (branch, data) in enumerate(timeline_data.items()):
    # Círculo principal
    circle = plt.Circle((data['pos'], 0), 0.15, color=data['color'], alpha=0.8)
    ax.add_patch(circle)
    
    # Línea de conexión
    if i < len(timeline_data) - 1:
        ax.plot([data['pos'] + 0.15, data['pos'] + 0.85], [0, 0], 
               color='gray', linewidth=2, alpha=0.6)
    
    # Etiquetas
    ax.text(data['pos'], -0.4, data['fecha'], ha='center', va='center', 
           fontsize=10, fontweight='bold')
    ax.text(data['pos'], 0.35, f"{data['funcionalidades']}\nfuncionalidades", 
           ha='center', va='center', fontsize=9)
    
    # Nombre de branch
    branch_display = branch.replace('feature/', '').replace('origin/', '')
    ax.text(data['pos'], -0.7, branch_display, ha='center', va='center', 
           fontsize=8, style='italic')

ax.set_xlim(-0.5, 4.5)
ax.set_ylim(-1, 0.6)
ax.set_aspect('equal')
ax.axis('off')

ax.set_title('Timeline de Desarrollo del CRM Legal\nEvolución Incremental de Funcionalidades', 
            fontsize=16, fontweight='bold', pad=20)

# Agregar leyenda de hitos importantes
hitos = [
    "✓ Base estable con CRM básico",
    "✓ Módulo de seguimiento modular", 
    "✓ Sistema completo de partes",
    "✓ Sistema completo de tareas/plazos",
    "✓ Integración maestra + IA local"
]

for i, hito in enumerate(hitos):
    ax.text(-0.3, 0.4 - i*0.08, hito, fontsize=9, 
           bbox=dict(boxstyle="round,pad=0.3", facecolor=list(timeline_data.values())[i]['color'], alpha=0.3))

plt.tight_layout()
plt.savefig('/workspace/charts/timeline_desarrollo_branches.png', 
           dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close()

print("✅ Timeline de desarrollo generado: /workspace/charts/timeline_desarrollo_branches.png")
