import os
from config.settings import REPORTS_DIR, ASSETS_DIR


def clear_generated_reports():
    """Busca y elimina físicamente todos los archivos Excel y PNG para limpiar el sistema."""
    # Lista de las carpetas que el conserje debe limpiar
    target_folders = [REPORTS_DIR, ASSETS_DIR]
    files_deleted = 0

    for folder in target_folders:
        # Verificar primero si la carpeta físicamente existe en el disco
        if folder.exists():
            # Listar todos los elementos que están dentro de la carpeta
            for filename in os.listdir(folder):
                file_path = folder / filename

                # Blindaje: Asegurar que sea un archivo real antes de borrar
                if file_path.is_file():
                    try:
                        os.remove(file_path)
                        files_deleted += 1
                    except Exception as e:
                        print(f"[ERROR] No se pudo borrar {filename}: {e}")

    if files_deleted > 0:
        print(f"[INFO] Limpieza exitosa: Se eliminaron {files_deleted} archivos viejos.")
    else:
        print("[INFO] Nada que limpiar: Las carpetas de reportes ya estaban vacías.")