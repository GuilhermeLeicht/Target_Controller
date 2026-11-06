# -*- coding: utf-8 -*-
"""Resumo anual de targets e XLSX sem dependências adicionais."""
from collections import defaultdict
from io import BytesIO
from xml.sax.saxutils import escape
from zipfile import ZipFile, ZIP_DEFLATED
import re


def preparar_resumo_anual(registros, catalogo, gerais=(), codigos_filtrados=None, pn_filtrado=None):
    """Retorna (linhas, anos), com último lançamento até dezembro de cada ano.

    As metas de fornecedor são apresentadas com PART_NUMBER vazio; meta geral
    aparece com SUPPLIER='TARGET GERAL' apenas nas exportações sem filtros.
    """
    fornecedores = {}
    for item in catalogo:
        codigo = str(item.get('cd_fornecedor') or '').strip()
        if codigo and item.get('fornecedor') and codigo not in fornecedores:
            fornecedores[codigo] = str(item['fornecedor'])

    series = defaultdict(list)
    anos_com_lancamento = set()
    for r in registros:
        codigo = str(r.get('cod_fornecedor') or '').strip()
        pn = str(r.get('part_number') or '').strip()
        if codigos_filtrados is not None and codigo not in codigos_filtrados:
            continue
        if pn_filtrado is not None and pn != pn_filtrado:
            continue
        data = str(r.get('data') or '')
        if not re.fullmatch(r'\d{4}-\d{2}', data) or not 1 <= int(data[5:]) <= 12:
            continue
        if pn and r.get('target_pn') is not None:
            series[(pn, codigo)].append((data, r['target_pn'], r.get('id_registro', 0)))
            anos_com_lancamento.add(int(data[:4]))
        if not pn and pn_filtrado is None and r.get('target_supplier') is not None:
            series[('', codigo)].append((data, r['target_supplier'], r.get('id_registro', 0)))
            anos_com_lancamento.add(int(data[:4]))

    if codigos_filtrados is None and pn_filtrado is None:
        for r in gerais:
            data = str(r.get('ano_mes') or '')
            if re.fullmatch(r'\d{4}-\d{2}', data) and 1 <= int(data[5:]) <= 12 and r.get('target') is not None:
                series[('', '__GERAL__')].append((data, r['target'], 0))
                anos_com_lancamento.add(int(data[:4]))

    if not anos_com_lancamento:
        return [], []
    anos = list(range(min(anos_com_lancamento), max(anos_com_lancamento) + 1))
    linhas = []
    for (pn, codigo), eventos in sorted(series.items(), key=lambda x: (fornecedores.get(x[0][1], x[0][1]).casefold(), x[0][0])):
        eventos.sort(key=lambda e: (e[0], e[2]))
        valores = []
        atual = None
        idx = 0
        for ano in anos:
            while idx < len(eventos) and int(eventos[idx][0][:4]) <= ano:
                atual = eventos[idx][1]
                idx += 1
            valores.append(atual)
        nome = 'TARGET GERAL' if codigo == '__GERAL__' else fornecedores.get(codigo, f'Cód. {codigo}')
        linhas.append([pn, nome] + valores)
    return linhas, anos


def _coluna(n):
    r = ''
    while n:
        n, digit = divmod(n - 1, 26)
        r = chr(65 + digit) + r
    return r


def _celula(value, endereco, cabecalho=False):
    sty = ' s="1"' if cabecalho else ''
    if value is None:
        return f'<c r="{endereco}"{sty}/>'
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return f'<c r="{endereco}"{sty}><v>{value}</v></c>'
    # Inline strings also prevent Excel from interpreting PN identifiers as numbers/formulas.
    s = escape(str(value), {'"': '&quot;'})
    return f'<c r="{endereco}"{sty} t="inlineStr"><is><t xml:space="preserve">{s}</t></is></c>'


def criar_excel(linhas, anos):
    """Gera um XLSX válido (OOXML) com tabela, filtro, largura e cabeçalho fixo."""
    cabecalho = ['PART_NUMBER', 'SUPPLIER'] + [str(a) for a in anos]
    dados = [cabecalho] + linhas
    if len(dados) > 1048576:
        raise ValueError('Limite de linhas do Excel ultrapassado.')
    if len(cabecalho) > 16384:
        raise ValueError('Limite de colunas do Excel ultrapassado.')
    ultima_coluna = _coluna(len(cabecalho))
    ultima_linha = len(dados)
    linhas_xml = []
    for i, row in enumerate(dados, 1):
        celulas = ''.join(_celula(val, f'{_coluna(j)}{i}', cabecalho=(i == 1)) for j, val in enumerate(row, 1))
        linhas_xml.append(f'<row r="{i}"{(" ht=\"25\" customHeight=\"1\"" if i == 1 else "")}>{celulas}</row>')
    colunas_xml = '<col min="1" max="1" width="23" customWidth="1"/><col min="2" max="2" width="38" customWidth="1"/>'
    if len(cabecalho) > 2:
        colunas_xml += f'<col min="3" max="{len(cabecalho)}" width="16" customWidth="1"/>'
    ws = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
          f'<dimension ref="A1:{ultima_coluna}{ultima_linha}"/>'
          '<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>'
          '<sheetFormatPr defaultRowHeight="18"/>'
          f'<cols>{colunas_xml}</cols>'
          f'<sheetData>{"".join(linhas_xml)}</sheetData>'
          f'<autoFilter ref="A1:{ultima_coluna}{ultima_linha}"/>'
          '</worksheet>')
    styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
              '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
              '<fonts count="2"><font><sz val="11"/><name val="Calibri"/></font>'
              '<font><b/><color rgb="FFFFFFFF"/><sz val="11"/><name val="Calibri"/></font></fonts>'
              '<fills count="3"><fill><patternFill patternType="none"/></fill>'
              '<fill><patternFill patternType="gray125"/></fill>'
              '<fill><patternFill patternType="solid"><fgColor rgb="FF1E40AF"/><bgColor indexed="64"/></patternFill></fill></fills>'
              '<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
              '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
              '<cellXfs count="2"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>'
              '<xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1"/></cellXfs>'
              '<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>'
              '</styleSheet>')
    arquivos = {
        '[Content_Types].xml': ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
            '<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
            '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
            '</Types>'),
        '_rels/.rels': ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
            '</Relationships>'),
        'xl/workbook.xml': ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            '<sheets><sheet name="Resumo Anual" sheetId="1" r:id="rId1"/></sheets></workbook>'),
        'xl/_rels/workbook.xml.rels': ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
            '</Relationships>'),
        'xl/styles.xml': styles,
        'xl/worksheets/sheet1.xml': ws,
    }
    buffer = BytesIO()
    with ZipFile(buffer, 'w', ZIP_DEFLATED) as z:
        for caminho, texto in arquivos.items():
            z.writestr(caminho, texto)
    return buffer.getvalue()
