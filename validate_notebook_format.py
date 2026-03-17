"""
Валидация формата Jupyter notebook (nbformat v4).
Шаги: начальная валидация -> исправления -> финишная валидация.
"""
import json
import os
import sys

# --- Зависимость nbformat ---
try:
    import nbformat
    from nbformat import validate
except ModuleNotFoundError:
    print("Установите nbformat: pip install nbformat", file=sys.stderr)
    sys.exit(1)


def get_notebook_path():
    """Путь к .ipynb: из аргумента или по умолчанию."""
    if len(sys.argv) > 1 and sys.argv[1].strip().lower().endswith(".ipynb"):
        return os.path.abspath(sys.argv[1].strip())
    # workspace = родитель каталога .vscode (скрипт в .vscode/scripts/)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # workspace = os.path.dirname(os.path.dirname(script_dir))
    return os.path.join(script_dir, "DLS_Speech_HW", "Homework_1_add_5_to_cnn_save.ipynb")


# ---------------------------------------------------------------------------
# 1. Начальная валидация
# ---------------------------------------------------------------------------
def run_initial_validation(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)
    validate(nb)
    print("Начальная валидация: OK")


# ---------------------------------------------------------------------------
# 2. Исправления (JSON)
# ---------------------------------------------------------------------------
ALLOWED_KEYS = {
    "stream": {"name", "output_type", "text"},
    "execute_result": {"data", "metadata", "output_type", "execution_count"},
    "display_data": {"data", "metadata", "output_type"},
    "error": {"ename", "evalue", "output_type", "traceback"},
}


def apply_fixes(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    for cell in nb.get("cells", []):
        if cell.get("cell_type") in ("markdown", "raw"):
            cell.pop("outputs", None)
            cell.pop("execution_count", None)
            continue

        if cell.get("cell_type") != "code":
            continue

        cell_ec = cell.get("execution_count")
        for out in cell.get("outputs", []):
            if not isinstance(out, dict):
                continue
            ot = out.get("output_type")

            if ot == "execute_result":
                if "metadata" not in out:
                    out["metadata"] = {}
                if "execution_count" not in out:
                    out["execution_count"] = cell_ec
            elif ot == "display_data":
                if "metadata" not in out:
                    out["metadata"] = {}
            elif ot == "stream":
                out.pop("metadata", None)

            allow = ALLOWED_KEYS.get(ot, set())
            if allow:
                for k in list(out.keys()):
                    if k not in allow:
                        out.pop(k)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    print("Исправления применены.")


# ---------------------------------------------------------------------------
# 3. Финишная валидация
# ---------------------------------------------------------------------------
def run_final_validation(path: str) -> None:
    with open(path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)
    validate(nb)
    print("Финишная валидация: OK")


# ---------------------------------------------------------------------------
# Запуск
# ---------------------------------------------------------------------------
def main() -> None:
    path = get_notebook_path()
    if not os.path.isfile(path):
        print(f"Файл не найден: {path}", file=sys.stderr)
        sys.exit(1)

    # 1. Начальная валидация
    try:
        run_initial_validation(path)
    except nbformat.validator.NotebookValidationError as e:
        print(f"Начальная валидация: ошибка\n{e}", file=sys.stderr)
        sys.exit(1)

    # 2. Исправления
    apply_fixes(path)

    # 3. Финишная валидация
    try:
        run_final_validation(path)
    except nbformat.validator.NotebookValidationError as e:
        print(f"Финишная валидация: ошибка\n{e}", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
