"""Pinned sources and asset file digests for the Windows CPU distribution."""
import hashlib
from pathlib import Path
import shutil

PYTHON = "python-3.12.10-embed-amd64.zip"
PYTHON_HASH = "4acbed6dd1c744b0376e3b1cf57ce906f9dc9e95e68824584c8099a63025a3c3"
ENGINE = "llama-cpu.zip"
ENGINE_HASH = "b6baf2eae7a6bd53cdeaf132a19c8a7d9eca24cfb02f4089f007e87c50769ded"
CHAT = "qwen2.5-0.5b-instruct-q4_k_m.gguf"
CHAT_HASH = "74a4da8c9fdbcd15bd1f6d01d621410d31c6fc00986f5eb687824e7b93d7a9db"
EMBED = "Qwen3-Embedding-0.6B-Q8_0.gguf"
EMBED_HASH = "06507c7b42688469c4e7298b0a1e16deff06caf291cf0a5b278c308249c3e439"
CHAT_SKILLS = {"literature-search", "paper-analysis", "research-report"}
MATTER_SKILLS = {"structure-optimization", "phonon-analysis"}

CRYSTAL = ("ckpt.pt", "models/crystallm_v1_small/ckpt.pt",
           "eeaa5ccb6597da856dfd5007bccea83d40f3bfad10c8837931307fd70a9a0163")
MATTER = ("mattersim-v1.0.0-1M.pth", "models/mattersim-v1.0.0-1M.pth",
          "28b0b0b0f13efefee06b47ea4c9105a26bd3e2c8396da193430da96b3b49a8be")
KAPPA = [
    ("Bulk modulus (GPa)-pre-trained.pth.tar", "bfc8eb09e819ec307a0420b3b37bae64cac657474ba04a219126adda80a33ea7"),
    ("Shear modulus (GPa)-pre-trained.pth.tar", "3a7366e13cc1640d6f06078dd45b5eea14a41c3b081726a1ae09a08734acb83b"),
    ("atom_init.json", "cb90bd2257dbf8cfc4e6b2b6d4348d4616e8e9680f1339b1461137032e0f1894"),
]


def sha256(path):
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def checked(file, expected):
    if sha256(file) != expected:
        raise ValueError(f"SHA-256 mismatch: {file.name}")
    return file


def models_for(skill):
    if skill == "crystal-generation":
        return [CRYSTAL]
    if skill in MATTER_SKILLS:
        return [MATTER]
    if skill == "thermal-conductivity":
        return [(name, "models/kappa/" + name, digest) for name, digest in KAPPA]
    if skill in CHAT_SKILLS:
        return [(CHAT, f"models/{CHAT}", CHAT_HASH)]
    if skill == "literature-knowledge":
        return [(EMBED, f"models/{EMBED}", EMBED_HASH)]
    return []


def copy_models(skill, assets, dest):
    for original, target, digest in models_for(skill):
        output = dest / target
        output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(checked(assets / original, digest), output)
