import argparse
from pathlib import Path

def find_null_bytes(root: Path):
    results = []
    for p in root.rglob("*.py"):
        try:
            data = p.read_bytes()
        except Exception as e:
            results.append((p, "ERROR", str(e)))
            continue
        if b'\x00' in data:
            positions = []
            start = 0
            while True:
                idx = data.find(b'\x00', start)
                if idx == -1:
                    break
                positions.append(idx)
                start = idx + 1
            results.append((p, "NULLS", positions))
    return results

def make_clean_copy(path: Path):
    data = path.read_bytes()
    cleaned = data.replace(b'\x00', b'')
    clean_path = path.with_suffix(path.suffix + ".clean")
    clean_path.write_bytes(cleaned)
    return clean_path

def main():
    parser = argparse.ArgumentParser(description="Buscar null bytes en archivos .py del proyecto")
    parser.add_argument("--root", "-r", default=".", help="Directorio raíz (por defecto: proyecto actual)")
    parser.add_argument("--clean", action="store_true", help="Generar copias limpias (.clean) de los archivos que contienen null bytes")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    print(f"Buscando null bytes en: {root}")
    results = find_null_bytes(root)

    if not results:
        print("No se encontraron archivos .py con null bytes.")
        return

    for item in results:
        path, status, info = item
        if status == "ERROR":
            print(f"[ERROR] {path}: {info}")
        else:
            print(f"[FOUND] {path}: {len(info)} null byte(s) at positions {info[:5]}{'...' if len(info)>5 else ''}")
            if args.clean:
                clean_path = make_clean_copy(path)
                print(f"  -> Copia limpia creada: {clean_path}")

    print("Hecho. Revisa los archivos reportados y las copias '.clean' si las generaste.")

if __name__ == "__main__":
    main()
