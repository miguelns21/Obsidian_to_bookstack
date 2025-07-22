#!/bin/bash

# Script para configurar el entorno virtual de Obsidian to BookStack
# Uso: source setup_env.sh

echo "🚀 Configurando entorno virtual para Obsidian to BookStack..."

# Verificar si el entorno virtual existe
if [ ! -d "obsidian_env" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv obsidian_env
fi

# Activar el entorno virtual
echo "⚡ Activando entorno virtual..."
source obsidian_env/bin/activate

# Verificar si requirements.txt existe e instalar dependencias
if [ -f "requirements.txt" ]; then
    echo "📚 Instalando dependencias..."
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "✅ Dependencias instaladas correctamente"
else
    echo "⚠️  Archivo requirements.txt no encontrado"
fi

echo ""
echo "🎉 ¡Entorno configurado correctamente!"
echo ""
echo "📋 Comandos disponibles:"
echo "  - python test_connection.py --config config.json"
echo "  - python obsidian_to_bookstack.py config.json --dry-run"
echo "  - python obsidian_to_bookstack.py config.json"
echo "  - python ejemplo_uso.py"
echo ""
echo "💡 Para desactivar el entorno virtual: deactivate"
echo "💡 Para activar manualmente: source obsidian_env/bin/activate"