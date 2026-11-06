# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, render_template_string, send_file
import sqlite3
import os
import sys
import webbrowser
import threading
import time
import json
import re
from datetime import datetime
from io import BytesIO
from exportar_excel import criar_excel, preparar_resumo_anual

# Importa o template HTML separado para manter o código limpo
from html import HTML_TEMPLATE

app = Flask(__name__)

# No PyInstaller onedir, os arquivos empacotados ficam em _internal.
# A configuração deve ficar ao lado do .exe, onde o usuário pode editá-la.
BASE_DIR = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
DEFAULT_DB_PATH = r""

def obter_caminho_db():
    """Lê o caminho do banco de dados do config.json ou usa o padrão."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                caminho = config.get("db_path", DEFAULT_DB_PATH)
                if caminho.strip():
                    return caminho
        except Exception as e:
            print("Erro ao ler config.json, usando padrão:", e)
    return DEFAULT_DB_PATH

def get_db_connection():
    db_path = obter_caminho_db()
    conn = sqlite3.connect(db_path, timeout=15.0)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA journal_mode=WAL;")
    except Exception as e:
        print("Aviso modo WAL:", e)
    return conn

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/config', methods=['GET'])
def get_config():
    """Retorna o caminho atual do banco de dados para a interface."""
    return jsonify({"db_path": obter_caminho_db()})

@app.route('/api/salvar-config', methods=['POST'])
def salvar_config():
    """Valida o novo caminho e salva no config.json."""
    data = request.get_json(silent=True) or {}
    novo_caminho = data.get('db_path', '').strip()
    if not novo_caminho:
        return jsonify({"success": False, "error": "O caminho do banco não pode ser vazio."}), 400
    
    # Abre SOMENTE um banco existente para leitura, evitando criar um .db vazio
    # por engano quando uma unidade de rede nao estiver disponivel.
    if not os.path.isfile(novo_caminho):
        return jsonify({"success": False, "error":
            "Arquivo .db nao encontrado neste computador. Verifique se a unidade de rede "
            "esta conectada ou utilize o caminho UNC (\\servidor\\pasta\\fundmap.db)."}), 400
    try:
        # Caminhos de rede UNC (\\servidor\compartilhamento) e unidades
        # mapeadas (S:\...) devem ser passados diretamente ao SQLite.
        # Converter um caminho UNC para file:// causa "invalid uri authority".
        conn = sqlite3.connect(novo_caminho, timeout=3.0)
        try:
            conn.execute("SELECT name FROM sqlite_master LIMIT 1").fetchone()
        finally:
            conn.close()
    except Exception as e:
        return jsonify({
            "success": False, 
            "error": f"Não foi possível conectar ao arquivo .db. Verifique o caminho digitado.\\nDetalhes: {str(e)}"
        }), 400

    # Grava o JSON de forma limpa
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump({"db_path": novo_caminho}, f, ensure_ascii=False, indent=4)
        return jsonify({"success": True, "message": "Caminho do banco de dados atualizado com sucesso!"})
    except Exception as e:
        return jsonify({"success": False, "error": f"Erro ao escrever no config.json: {str(e)}"}), 500

# Monitoramento da janela do navegador: ao fechar a ultima aba, o processo
# encerra. Um pequeno intervalo evita desligar o app durante F5/reload.
# O limite mais longo e uma seguranca para encerramentos sem envio do beacon.
_atividade_lock = threading.Lock()
_ultimo_heartbeat = time.monotonic()
_ultimo_fechamento = None
_TEMPO_REABERTURA = 6.0  # segundos para permitir recarregar a pagina
_LIMITE_SEM_NAVEGADOR = 90.0  # fallback para fechamentos sem aviso


def _encerrar_se_fechou(instante_fechamento):
    time.sleep(_TEMPO_REABERTURA)
    with _atividade_lock:
        encerrar = (_ultimo_fechamento == instante_fechamento and
                    _ultimo_heartbeat <= instante_fechamento)
    if encerrar:
        os._exit(0)  # encerra o EXE/Flask mesmo no --noconsole


@app.route('/api/heartbeat', methods=['POST'])
def heartbeat():
    global _ultimo_heartbeat, _ultimo_fechamento
    with _atividade_lock:
        _ultimo_heartbeat = time.monotonic()
        _ultimo_fechamento = None
    return jsonify({"status": "ok"})


@app.route('/api/navegador-fechado', methods=['POST'])
def navegador_fechado():
    global _ultimo_fechamento
    with _atividade_lock:
        _ultimo_fechamento = time.monotonic()
        instante = _ultimo_fechamento
    threading.Thread(target=_encerrar_se_fechou, args=(instante,), daemon=True).start()
    return ('', 204)


def monitorar_navegador():
    # Comeca com tolerancia para o navegador iniciar.
    while True:
        time.sleep(5)
        with _atividade_lock:
            sem_contato = time.monotonic() - _ultimo_heartbeat
        if sem_contato > _LIMITE_SEM_NAVEGADOR:
            os._exit(0)

@app.route('/api/itens', methods=['GET'])
def get_itens():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT item, descricao, cd_fornecedor, fornecedor, regiao FROM itens_fornecedor")
            rows = cursor.fetchall()
            itens = [dict(ix) for ix in rows]
        return jsonify({"success": True, "data": itens})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/resumo', methods=['GET'])
def get_resumo():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.ROWID AS id_registro, p.part_number, p.cod_fornecedor, p.data, p.target_pn, p.target_supplier, i.fornecedor
                FROM ppm_target_changes p
                LEFT JOIN itens_fornecedor i ON p.part_number = i.item AND p.cod_fornecedor = i.cd_fornecedor
                ORDER BY p.data DESC, p.ROWID DESC LIMIT 150
            """)
            changes = [dict(ix) for ix in cursor.fetchall()]
            
            cursor.execute("SELECT ano_mes, target FROM target_ppm_geral ORDER BY ano_mes DESC LIMIT 1")
            geral_recente = cursor.fetchone()
            geral_valor = geral_recente['target'] if geral_recente else '-'
            geral_mes = geral_recente['ano_mes'] if geral_recente else ''
            
        return jsonify({
            "success": True, 
            "changes": changes, 
            "geral_atual": geral_valor,
            "geral_mes": geral_mes
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/salvar-target', methods=['POST'])
def salvar_target():
    data = request.json
    part_number = data.get('part_number', '').strip()
    cod_fornecedor = data.get('cod_fornecedor', '').strip() or None
    target_value = data.get('target_value')
    tipo = data.get('tipo')
    
    data_definida = data.get('data_definida', '').strip()
    if not data_definida:
        data_definida = datetime.now().strftime("%Y-%m")
    
    if target_value is None or target_value == '':
        return jsonify({"success": False, "error": "O valor do Target é obrigatório."}), 400

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            if tipo == 'geral':
                # Mantem a linha apenas quando ela ALTERA o target vigente.
                # Ex.: 2026-01=8000, 2026-11=3000; salvar 2026-11=8000
                # remove a linha redundante de novembro.
                try:
                    novo_valor = float(target_value)
                    if not (float('-inf') < novo_valor < float('inf')):
                        raise ValueError()
                except (ValueError, TypeError):
                    return jsonify({"success": False, "error": "Target Geral deve ser um número válido."}), 400
                if not re.fullmatch(r'\d{4}-(0[1-9]|1[0-2])', data_definida):
                    return jsonify({"success": False, "error": "Período inválido. Use AAAA-MM."}), 400
                anterior = cursor.execute(
                    "SELECT target FROM target_ppm_geral WHERE ano_mes < ? "
                    "ORDER BY ano_mes DESC LIMIT 1", (data_definida,)
                ).fetchone()
                if anterior is not None and float(anterior['target']) == novo_valor:
                    # Mes ja existente ou novo: nao deve manter meta igual a anterior.
                    cursor.execute("DELETE FROM target_ppm_geral WHERE ano_mes = ?", (data_definida,))
                    mensagem = "Target Geral igual ao anterior: registro redundante removido (ou não criado)."
                else:
                    cursor.execute("SELECT 1 FROM target_ppm_geral WHERE ano_mes = ?", (data_definida,))
                    exists = cursor.fetchone()
                    if exists:
                        cursor.execute("UPDATE target_ppm_geral SET target = ? WHERE ano_mes = ?", (target_value, data_definida))
                    else:
                        cursor.execute("INSERT INTO target_ppm_geral (ano_mes, target) VALUES (?, ?)", (data_definida, target_value))
                    mensagem = "Target Geral atualizado com sucesso!"
                
            elif tipo == 'pn':
                if not part_number or not cod_fornecedor:
                    return jsonify({"success": False, "error": "Part Number e Fornecedor são obrigatórios para Target PN."}), 400
                
                cursor.execute("""
                    INSERT INTO ppm_target_changes (part_number, cod_fornecedor, data, target_pn, target_supplier)
                    VALUES (?, ?, ?, ?, NULL)
                    ON CONFLICT(part_number, cod_fornecedor, data) DO UPDATE SET
                        target_pn = excluded.target_pn
                """, (part_number, cod_fornecedor, data_definida, target_value))
                
            elif tipo == 'supplier':
                if not cod_fornecedor:
                    return jsonify({"success": False, "error": "Fornecedor é obrigatório para Target Fornecedor."}), 400
                
                cursor.execute("""
                    INSERT INTO ppm_target_changes (part_number, cod_fornecedor, data, target_pn, target_supplier)
                    VALUES ('', ?, ?, NULL, ?)
                    ON CONFLICT(part_number, cod_fornecedor, data) DO UPDATE SET
                        target_supplier = excluded.target_supplier
                """, (cod_fornecedor, data_definida, target_value))
                
            conn.commit()
        return jsonify({"success": True, "message": mensagem if tipo == "geral" else "Target atualizado com sucesso!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/excluir-registro', methods=['POST'])
def excluir_registro():
    """Exclui somente o registro explicitamente escolhido no histórico."""
    dados = request.get_json(silent=True) or {}
    identificador = dados.get('id_registro')
    if type(identificador) is not int or identificador <= 0:
        return jsonify({"success": False, "error": "Registro inválido."}), 400
    try:
        with get_db_connection() as conn:
            cursor = conn.execute(
                "DELETE FROM ppm_target_changes WHERE ROWID = ?", (identificador,)
            )
            if cursor.rowcount != 1:
                return jsonify({"success": False, "error": "Registro não encontrado. Atualize a página."}), 404
            conn.commit()
        return jsonify({"success": True, "message": "Registro excluído."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/api/exportar-excel', methods=['GET'])
def exportar_excel():
    """Exporta todo o banco, sem o limite de 150 registros da tabela visual."""
    modo = request.args.get('modo', 'todos')
    if modo not in ('todos', 'filtrado'):
        return jsonify({"success": False, "error": "Modo de exportação inválido."}), 400
    nome_fornecedor = (request.args.get('fornecedor') or '').strip() if modo == 'filtrado' else ''
    pn = (request.args.get('pn') or '').strip() if modo == 'filtrado' else ''
    if modo == 'filtrado' and pn and not nome_fornecedor:
        return jsonify({"success": False, "error": "Selecione um fornecedor para filtrar por PN."}), 400
    try:
        with get_db_connection() as conn:
            catalogo = [dict(r) for r in conn.execute(
                'SELECT item, cd_fornecedor, fornecedor FROM itens_fornecedor'
            ).fetchall()]
            codigos = {str(r['cd_fornecedor']) for r in catalogo if r['fornecedor'] == nome_fornecedor} if nome_fornecedor else set()
            if modo == 'filtrado' and nome_fornecedor and not codigos:
                return jsonify({"success": False, "error": "Fornecedor não encontrado."}), 404
            registros = [dict(r) for r in conn.execute(
                'SELECT ROWID AS id_registro, part_number, cod_fornecedor, data, target_pn, target_supplier '
                'FROM ppm_target_changes ORDER BY data ASC, ROWID ASC'
            ).fetchall()]
            gerais = [dict(r) for r in conn.execute(
                'SELECT ano_mes, target FROM target_ppm_geral ORDER BY ano_mes ASC'
            ).fetchall()] if not nome_fornecedor and not pn else []
        linhas, anos = preparar_resumo_anual(registros, catalogo, gerais,
            codigos if nome_fornecedor else None, pn if pn else None)
        if not linhas:
            return jsonify({"success": False, "error": "Não há metas para exportar com esses filtros."}), 404
        arquivo = BytesIO(criar_excel(linhas, anos))
        arquivo.seek(0)
        sufixo = 'filtrado' if modo == 'filtrado' else 'completo'
        nome = f'targets_resumo_{sufixo}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        return send_file(arquivo, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                         as_attachment=True, download_name=nome)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


def abrir_navegador():
    time.sleep(1.2)
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == '__main__':
    threading.Thread(target=abrir_navegador, daemon=True).start()
    threading.Thread(target=monitorar_navegador, daemon=True).start()
    app.run(host='127.0.0.1', port=5000, debug=False)
