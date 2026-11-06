# -*- coding: utf-8 -*-
"""Utilitário de migração controlada do SQLite para journal DELETE.
Execute SOMENTE com outros usuários/conexões fechados.
Cria backup consistente via API de backup do SQLite antes de mudar o modo.
"""
from pathlib import Path
from datetime import datetime
import json
import sqlite3
import sys

PASTA = Path(__file__).resolve().parent
CAMINHO_PADRAO = r"S:\Dir_Financeira\Compras\Seg_Qualidade\3.Processos\3.Gerenciamento PUQ1\20_EvoSend\FundMap BI\fundmap.db"


def caminho_banco():
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    cfg = PASTA / 'config.json'
    if cfg.exists():
        return Path(json.loads(cfg.read_text(encoding='utf-8')).get('db_path', CAMINHO_PADRAO))
    return Path(CAMINHO_PADRAO)


def preparar():
    banco = caminho_banco()
    if not banco.is_file():
        raise FileNotFoundError(f'Banco inexistente: {banco}')
    print(f'Banco: {banco}')
    print('IMPORTANTE: feche TODOS os aplicativos que acessam esse banco.')
    if input('Digite CONVERTER para prosseguir: ').strip() != 'CONVERTER':
        print('Cancelado sem mudanças.')
        return
    backup = banco.with_name(f'{banco.stem}_backup_{datetime.now():%Y%m%d_%H%M%S}.db')
    if backup.exists():
        raise FileExistsError(f'Já existe backup com esse nome: {backup}')
    # Aplica backup transacional, inclusive quando a origem está em modo WAL.
    with sqlite3.connect(str(banco), timeout=30.0) as conn:
        with sqlite3.connect(str(backup)) as saida:
            conn.backup(saida)
        print(f'Backup criado: {backup}')
        # Não avançar se a origem acusar problema de integridade.
        resultado = conn.execute('PRAGMA quick_check').fetchone()[0]
        if resultado != 'ok':
            raise RuntimeError(f'Verificação de integridade falhou: {resultado}')
        modo = conn.execute('PRAGMA journal_mode=DELETE').fetchone()[0].lower()
        if modo != 'delete':
            raise RuntimeError(f'Não foi possível ativar DELETE (modo atual: {modo}). Feche outros acessos.')
        print('Sucesso: modo DELETE configurado. Backup preservado.')


if __name__ == '__main__':
    try:
        preparar()
    except (Exception) as exc:
        print(f'ERRO: {exc}')
        sys.exit(1)
