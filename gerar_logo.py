# -*- coding: utf-8 -*-
"""Atualiza somente o arquivo estático do logotipo; não altera html.py."""
from pathlib import Path
import shutil

base = Path(__file__).resolve().parent
origem = base / "Bosch_Rexroth-Logo.wine.png"
destino = base / "static" / "logo.png"

if __name__ == "__main__":
    if not origem.is_file():
        print(f"Arquivo não encontrado: {origem}")
    else:
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origem, destino)
        print(f"Logotipo atualizado em {destino}")
