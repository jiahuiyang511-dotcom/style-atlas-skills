"""Package the catalogue-listed style skills; keep the authoring workflow local."""
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
def catalogue_skills():
    data = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    names, ids = [], set()
    for item in data["styles"]:
        relative = Path(item["skillPath"])
        if relative.is_absolute() or len(relative.parts) != 2 or relative.parts[0] != "skills" or relative.name in {".", ".."}:
            raise ValueError("Invalid Skill path: " + str(relative))
        if item["id"] in ids or relative.name in names: raise ValueError("Duplicate catalogue ID or Skill path")
        if not item.get("classification", {}).get("path"): raise ValueError("Missing source classification")
        if not (ROOT / relative / "SKILL.md").is_file(): raise ValueError("Missing catalogue Skill: " + str(relative))
        ids.add(item["id"]); names.append(relative.name)
    return tuple(names)


SKILLS = catalogue_skills()


def package(output):
    actual = {p.name for p in (ROOT / "skills").iterdir() if p.is_dir()}
    if actual != set(SKILLS):
        raise ValueError("Skill directories differ from catalog.json")
    output.mkdir(parents=True, exist_ok=False)
    results = []
    for name in SKILLS:
        directory = ROOT / "skills" / name
        if not (directory / "SKILL.md").is_file():
            raise ValueError(f"Missing SKILL.md: {name}")
        archive = output / f"{name}.zip"
        count = 0
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
            for source in sorted(directory.rglob("*")):
                if not source.is_file() or "__pycache__" in source.parts or source.suffix == ".pyc":
                    continue
                info = zipfile.ZipInfo((Path(name) / source.relative_to(directory)).as_posix())
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                bundle.writestr(info, source.read_bytes(), compresslevel=6)
                count += 1
        with zipfile.ZipFile(archive) as bundle:
            if bundle.testzip() is not None:
                raise ValueError(f"Corrupt ZIP: {name}")
        results.append({"skill": name, "files": count, "bytes": archive.stat().st_size,
                        "sha256": hashlib.sha256(archive.read_bytes()).hexdigest()})
    (output / "SHA256SUMS.txt").write_text(
        "".join(f"{item['sha256']}  {item['skill']}.zip\n" for item in results), encoding="utf-8")
    return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "release-assets")
    arguments = parser.parse_args()
    print(json.dumps(package(arguments.output.resolve()), ensure_ascii=False, indent=2))
