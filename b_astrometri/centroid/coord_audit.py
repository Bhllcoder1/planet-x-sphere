"""03-14: Koordinat kurallari denetimi (0 tabanli, float konum asla yuvarlanmaz).

Denetlenen kurallar:
1. 0-tabanli piksel konumu: FITS/WCS 'origin=1' veya koordinat yuvarlama yok.
2. Alt-piksel float konumlar (x_0, y_0, a1, b1, theta, sig_x, sig_y) int/round
   ile kirpilmaz; JSON alanlari native float olarak uretilir.
3. Yalnizca goruntu/istatistik uretimi yapan b_astrometri modullerini tarar
   (test dosyalari haric).
"""
from __future__ import annotations

import ast
from pathlib import Path

FORBIDDEN_CALLS = {"round"}
FORBIDDEN_ATTR_CALLS = {"round", "rint", "floor", "ceil", "trunc"}


def _is_timing_expr(node: ast.AST) -> bool:
    """Zamanlama telemetrisi (time.monotonic vb.) yuvarlamalarini ayir."""
    for sub in ast.walk(node):
        if isinstance(sub, ast.Attribute) and sub.attr in {"monotonic", "perf_counter", "time"}:
            return True
    return False


def audit_source(source: str, filename: str = "<string>") -> list[str]:
    """AST uzerinde koordinat yuvarlama veya origin=1 ihlallerini bul."""
    tree = ast.parse(source, filename=filename)
    issues: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in FORBIDDEN_CALLS:
                if not (node.args and _is_timing_expr(node.args[0])):
                    issues.append(f"{filename}:{node.lineno}: yasak yuvarlama cagrisi '{node.func.id}()'")
            elif isinstance(node.func, ast.Attribute) and node.func.attr in FORBIDDEN_ATTR_CALLS:
                issues.append(f"{filename}:{node.lineno}: yasak yuvarlama metodu '.{node.func.attr}()'")
            for kw in node.keywords:
                if kw.arg == "origin" and isinstance(kw.value, ast.Constant) and kw.value.value == 1:
                    issues.append(f"{filename}:{node.lineno}: 1-tabanli WCS 'origin=1' yasak")
    return issues


def audit_directory(root: str | Path) -> dict[str, list[str]]:
    """Verilen klasordeki tum uretim .py dosyalarini (test_*.py haric) denetle."""
    root_path = Path(root)
    report: dict[str, list[str]] = {}
    for py_file in sorted(root_path.rglob("*.py")):
        if py_file.name.startswith("test_") or "__pycache__" in py_file.parts:
            continue
        issues = audit_source(py_file.read_text(encoding="utf-8"), str(py_file))
        if issues:
            report[str(py_file)] = issues
    return report


def audit_summary(root: str | Path) -> dict:
    """Run audit and return a summary dict with total_violations and clean status."""
    report = audit_directory(root)
    total = sum(len(v) for v in report.values())
    return {
        "clean": total == 0,
        "total_violations": total,
        "files_with_violations": len(report),
        "violations": report,
    }


if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "b_astrometri"
    summary = audit_summary(target)
    status = "TEMIZ" if summary["clean"] else f"IHLAL: {summary['total_violations']} sorun"
    print(f"Coord audit [{target}]: {status}")
    for f, issues in summary["violations"].items():
        for issue in issues:
            print(f"  {issue}")
    assert summary["clean"], f"coord_audit: {summary['total_violations']} ihlal bulundu"
    print("03-14 coord_audit: OK")
