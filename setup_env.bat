@echo off
REM Script para configurar el entorno virtual de Obsidian to BookStack en Windows
REM Uso: setup_env.bat

echo 🚀 Configurando entorno virtual para Obsidian to BookStack...

REM Verificar si el entorno virtual existe
if not exist "obsidian_env" (
    echo 📦 Creando entorno virtual...
    python -m venv obsidian_env
)

REM Activar el entorno virtual
echo ⚡ Activando entorno virtual...
call obsidian_env\Scripts\activate.bat

REM Verificar si requirements.txt existe e instalar dependencias
if exist "requirements.txt" (
    echo 📚 Instalando dependencias...
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    echo ✅ Dependencias instaladas correctamente
) else (
    echo ⚠️  Archivo requirements.txt no encontrado
)

echo.
echo 🎉 ¡Entorno configurado correctamente!
echo.
echo 📋 Comandos disponibles:
echo   - python test_connection.py --config config.json
echo   - python obsidian_to_bookstack.py config.json --dry-run
echo   - python obsidian_to_bookstack.py config.json
echo   - python ejemplo_uso.py
echo.
echo 💡 Para desactivar el entorno virtual: deactivate
echo 💡 Para activar manualmente: obsidian_env\Scripts\activate.bat
echo.
pause