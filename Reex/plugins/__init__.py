import glob
import os

def __list_all_modules():
    work_dir = os.path.dirname(__file__)
    # Cari semua file .py di dalam subfolder di plugins
    mod_paths = glob.glob(os.path.join(work_dir, "*", "*.py"))

    all_modules = []
    for f in mod_paths:
        if os.path.isfile(f) and not f.endswith("__init__.py"):
            # Dapatkan path relatif terhadap work_dir
            rel_path = os.path.relpath(f, work_dir)
            # Ganti separator path ke titik (.) untuk import
            module_name = rel_path.replace(os.path.sep, ".")[:-3]  # hilangkan ".py"
            all_modules.append(module_name)

    return all_modules

ALL_MODULES = sorted(__list_all_modules())
__all__ = ALL_MODULES + ["ALL_MODULES"]
