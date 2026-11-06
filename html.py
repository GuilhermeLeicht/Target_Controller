# -*- coding: utf-8 -*-\n\n
# 
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Target Controller</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        .hover-spin i {
            transition: transform 0.3s ease;
        }

        .hover-spin:hover i {
            transform: rotate(45deg);
        }
    </style>
</head>
<body class="bg-gray-50 font-sans text-gray-800">

    <div class="min-h-screen flex flex-col">
        <!-- Header -->
        <header class="bg-blue-800 text-white py-4 px-6 shadow-md">
            <div class="max-w-7xl mx-auto flex justify-between items-center">
                <div class="flex items-center space-x-3">
                    <i class="fa-solid fa-chart-line text-2xl text-blue-300"></i>
                    <h1 class="text-xl font-bold tracking-wide">PAINEL DE ATUALIZAÇÃO E ANÁLISE DE TARGETS</h1>
                </div>
                
                <!-- Logo e Botão de Configuração -->
                <div class="flex items-center space-x-4">
                    <!-- Botão de Configuração de Engrenagem -->
                    <button id="btn-config" class="text-gray-200 hover:text-white transition-transform duration-300 hover-spin p-2 rounded shadow-sm" title="Configurações do Banco de Dados">
                        <i class="fa-solid fa-gear text-2xl"></i>
                    </button>
                    
                    <!-- Logo da Bosch Rexroth em fundo branco arredondado (Aumentada para h-14) -->
                    <div class="bg-white px-4 py-1.5 rounded flex items-center shadow-sm h-14">
                        <img src="/static/logo.png" class="h-10 md:h-11" alt="Bosch Rexroth">
                    </div>
                </div>
            </div>
        </header>

        <!-- Main Content -->
        <main class="flex-grow max-w-7xl w-full mx-auto p-4 md:p-6 space-y-6">
            
            <!-- Secção 1: Selecionar Fornecedor e Peça -->
            <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 space-y-4">
                <h2 class="text-md font-semibold text-gray-700 border-b pb-3 flex items-center">
                    <span class="w-1.5 h-5 bg-blue-600 rounded-full mr-2"></span>
                    1. SELECIONE PARA ATUALIZAR OU ANALISAR
                </h2>
                
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                    <div>
                        <label class="block text-xs font-bold text-gray-600 uppercase mb-1">Fornecedor</label>
                        <select id="select-fornecedor" onchange="onSupplierChange()" class="w-full bg-gray-50 border border-gray-300 rounded px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none">
                            <option value="">Carregando fornecedores...</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-xs font-bold text-gray-600 uppercase mb-1">Código da Peça (PN)</label>
                        <select id="select-pn" onchange="onPNChange()" class="w-full bg-gray-50 border border-gray-300 rounded px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none" disabled>
                            <option value="">Selecione um Fornecedor primeiro</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-xs font-bold text-gray-600 uppercase mb-1">Descrição da Peça</label>
                        <input id="desc-peca" type="text" class="w-full bg-gray-100 border border-gray-200 rounded px-3 py-2 text-gray-500 cursor-not-allowed" readonly placeholder="-">
                    </div>
                    <div>
                        <label class="block text-xs font-bold text-gray-600 uppercase mb-1">Código do Fornecedor</label>
                        <input id="cod-fornecedor" type="text" class="w-full bg-gray-100 border border-gray-200 rounded px-3 py-2 text-gray-500 cursor-not-allowed" readonly placeholder="-">
                    </div>
                </div>

                <!-- Configuração de Data -->
                <div class="bg-blue-50/50 rounded-lg p-4 border border-blue-100 flex flex-col md:flex-row md:items-center space-y-3 md:space-y-0 md:space-x-6">
                    <span class="text-sm font-bold text-blue-900 flex items-center">
                        <i class="fa-regular fa-calendar-days mr-2"></i> Período do Lançamento:
                    </span>
                    <div class="flex items-center space-x-2">
                        <input type="radio" id="date-auto" name="tipo_data" value="auto" checked onchange="toggleDateSelector()" class="focus:ring-blue-500 text-blue-600">
                        <label for="date-auto" class="text-sm font-medium text-gray-700">Mês Atual Automático</label>
                    </div>
                    <div class="flex items-center space-x-2">
                        <input type="radio" id="date-manual" name="tipo_data" value="manual" onchange="toggleDateSelector()" class="focus:ring-blue-500 text-blue-600">
                        <label for="date-manual" class="text-sm font-medium text-gray-700 font-semibold text-yellow-700">Escolher Outro Mês (Lançamento Retroativo)</label>
                    </div>
                    <input id="input-data-custom" type="month" class="hidden border border-gray-300 rounded px-2.5 py-1 text-sm bg-white focus:ring-2 focus:ring-blue-500 focus:outline-none">
                </div>
            </div>

            <!-- Secção 2: Entrada de Novos Targets -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <!-- Target PN -->
                <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-5 flex flex-col justify-between">
                    <div>
                        <span class="bg-green-100 text-green-800 text-xs font-semibold px-2.5 py-0.5 rounded">Campo 1</span>
                        <h3 class="text-sm font-bold text-gray-700 mt-2 mb-1">Target PN</h3>
                        <p class="text-xs text-gray-500 mb-4">Insere target específico para a peça e fornecedor selecionados.</p>
                        <input id="input-target-pn" type="number" class="w-full border border-gray-300 rounded px-3 py-2 mb-4 focus:ring-2 focus:ring-green-500 focus:outline-none" placeholder="Digite o valor">
                    </div>
                    <button onclick="salvarTarget('pn')" class="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-2 px-4 rounded transition duration-150">
                        Salvar Target PN
                    </button>
                </div>

                <!-- Target Fornecedor -->
                <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-5 flex flex-col justify-between">
                    <div>
                        <span class="bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-0.5 rounded">Campo 2</span>
                        <h3 class="text-sm font-bold text-gray-700 mt-2 mb-1">Target Fornecedor</h3>
                        <p class="text-xs text-gray-500 mb-4">Insere target global aplicável a todas as peças do fornecedor.</p>
                        <input id="input-target-supplier" type="number" class="w-full border border-gray-300 rounded px-3 py-2 mb-4 focus:ring-2 focus:ring-blue-500 focus:outline-none" placeholder="Digite o valor">
                    </div>
                    <button onclick="salvarTarget('supplier')" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded transition duration-150">
                        Salvar Target Fornec.
                    </button>
                </div>

                <!-- Target Geral -->
                <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-5 flex flex-col justify-between">
                    <div>
                        <div class="flex justify-between items-start">
                            <span class="bg-purple-100 text-purple-800 text-xs font-semibold px-2.5 py-0.5 rounded">Campo 3</span>
                            <div class="text-right">
                                <span class="text-[10px] text-gray-400 block font-semibold uppercase">Atual mais recente</span>
                                <span id="badge-target-geral" class="bg-purple-600 text-white text-xs font-bold px-2 py-0.5 rounded">-</span>
                            </div>
                        </div>
                        <h3 class="text-sm font-bold text-gray-700 mt-2 mb-1">Target Geral</h3>
                        <p class="text-xs text-gray-500 mb-4">Define a meta geral global que vai para a tabela target_ppm_geral.</p>
                        <input id="input-target-geral" type="number" class="w-full border border-gray-300 rounded px-3 py-2 mb-4 focus:ring-2 focus:ring-purple-500 focus:outline-none" placeholder="Digite o valor">
                    </div>
                    <button onclick="salvarTarget('geral')" class="w-full bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-4 rounded transition duration-150">
                        Alterar Target Geral
                    </button>
                </div>
            </div>

            <!-- Secção 3: Histórico Recente e Visão Geral -->
            <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center border-b pb-3 mb-4 space-y-2 sm:space-y-0">
                    <h2 class="text-md font-semibold text-gray-700 flex items-center">
                        <span class="w-1.5 h-5 bg-yellow-500 rounded-full mr-2"></span>
                        3. HISTÓRICO DE MUDANÇAS <span id="status-filtro" class="ml-2 text-xs text-blue-600 font-bold bg-blue-50 px-2 py-0.5 rounded hidden">Filtrado</span>
                    </h2>
                    <div class="flex flex-wrap gap-2 items-center self-end">
                        <button onclick="exportarExcel('todos')" class="text-xs bg-emerald-600 hover:bg-emerald-700 text-white px-3 py-2 rounded font-semibold transition duration-150">
                            <i class="fa-solid fa-file-excel mr-1"></i> Exportar todo o histórico
                        </button>
                        <button onclick="exportarExcel('filtrado')" class="text-xs bg-blue-600 hover:bg-blue-700 text-white px-3 py-2 rounded font-semibold transition duration-150">
                            <i class="fa-solid fa-filter mr-1"></i> Exportar com os filtros selecionados
                        </button>
                        <button id="btn-excluir-registro" onclick="excluirRegistroSelecionado()" disabled
                            class="text-xs bg-red-600 hover:bg-red-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-white px-3 py-2 rounded font-semibold transition duration-150">
                            <i class="fa-solid fa-trash mr-1"></i> Excluir registro selecionado
                        </button>
                    </div>
                </div>
                
                <p class="text-xs text-gray-500 mb-3">Clique em uma linha do histórico para selecioná-la e habilitar a exclusão. A exclusão é permanente e exige confirmação.</p>
                <div class="overflow-x-auto">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="bg-gray-100 text-gray-600 uppercase text-xs font-semibold">
                                <th class="p-3 border-b">Part Number</th>
                                <th class="p-3 border-b">Fornecedor</th>
                                <th class="p-3 border-b">Cod Fornecedor</th>
                                <th class="p-3 border-b">Data</th>
                                <th class="p-3 border-b text-right">Target PN</th>
                                <th class="p-3 border-b text-right">Target Fornecedor</th>
                            </tr>
                        </thead>
                        <tbody id="tabela-historico" class="divide-y text-sm text-gray-600">
                            <!-- Inserido dinamicamente -->
                        </tbody>
                    </table>
                </div>
            </div>

        </main>
    </div>

    <!-- Modal de Configurações (Caminho do Banco de Dados) -->
    <div id="modal-config" class="fixed inset-0 bg-gray-900 bg-opacity-50 flex items-center justify-center z-50 hidden transition-opacity duration-200">
        <div class="bg-white rounded-lg shadow-xl border border-gray-200 max-w-lg w-full m-4 overflow-hidden transform scale-95 transition-transform duration-200" id="modal-container">
            <!-- Header -->
            <div class="bg-blue-800 text-white px-6 py-4 flex justify-between items-center">
                <h3 class="text-lg font-bold flex items-center">
                    <i class="fa-solid fa-gear mr-2"></i> Configurações do Banco
                </h3>
                <button id="close-config" class="text-white hover:text-gray-200 text-2xl focus:outline-none">&times;</button>
            </div>
            <!-- Body -->
            <div class="p-6 space-y-4">
                <div>
                    <label for="db-path-input" class="block text-sm font-bold text-gray-700 mb-2">Caminho do arquivo de Banco de Dados (.db):</label>
                    <input type="text" id="db-path-input" class="w-full bg-gray-50 border border-gray-300 rounded px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none font-mono" placeholder="Ex: S:\\Pasta\\fundmap.db">
                    <p class="text-xs text-gray-500 mt-2">Insira o caminho de rede UNC ou local completo onde o arquivo SQLite (.db) está armazenado.</p>
                </div>
            </div>
            <!-- Footer -->
            <div class="bg-gray-50 px-6 py-4 flex justify-end space-x-3 border-t border-gray-100">
                <button id="btn-cancelar-config" class="bg-gray-400 hover:bg-gray-500 text-white font-semibold py-2 px-4 rounded transition duration-150 text-sm">
                    Cancelar
                </button>
                <button id="btn-salvar-config" class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded transition duration-150 text-sm font-bold">
                    Salvar Configuração
                </button>
            </div>
        </div>
    </div>

    <script>
        let dbData = [];
        let historicoCompleto = [];
        let registroSelecionado = null;

        // Mantem o executavel vivo enquanto alguma aba do painel estiver aberta.
        // Ao fechar a aba, sendBeacon funciona mesmo durante o descarregamento.
        // Um recarregamento (F5) e tolerado pelo servidor durante alguns segundos.
        function avisarAtividade() {
            fetch('/api/heartbeat', { method: 'POST', cache: 'no-store', keepalive: true })
                .catch(() => {});
        }
        window.addEventListener('pagehide', () => {
            const url = '/api/navegador-fechado';
            if (navigator.sendBeacon) {
                navigator.sendBeacon(url, new Blob([], { type: 'text/plain' }));
            } else {
                fetch(url, { method: 'POST', keepalive: true }).catch(() => {});
            }
        });

        document.addEventListener("DOMContentLoaded", () => {
            avisarAtividade();
            setInterval(avisarAtividade, 3000);
            carregarItens();
            carregarResumo();
            
            const hoje = new Date();
            const mesFormatado = hoje.getFullYear() + "-" + String(hoje.getMonth() + 1).padStart(2, '0');
            document.getElementById("input-data-custom").value = mesFormatado;
        });

        // Seletores do Modal
        const modal = document.getElementById("modal-config");
        const btnConfig = document.getElementById("btn-config");
        const btnClose = document.getElementById("close-config");
        const btnCancelar = document.getElementById("btn-cancelar-config");
        const btnSalvar = document.getElementById("btn-salvar-config");
        const dbPathInput = document.getElementById("db-path-input");

        if (btnConfig) {
            btnConfig.addEventListener("click", function() {
                fetch('/api/config')
                    .then(res => res.json())
                    .then(data => {
                        dbPathInput.value = data.db_path || '';
                        modal.classList.remove("hidden");
                    })
                    .catch(err => alert("Erro ao carregar o caminho atual: " + err));
            });
        }

        function fecharModal() {
            modal.classList.add("hidden");
        }
        if (btnClose) btnClose.addEventListener("click", fecharModal);
        if (btnCancelar) btnCancelar.addEventListener("click", fecharModal);

        if (btnSalvar) {
            btnSalvar.addEventListener("click", function() {
                const novoCaminho = dbPathInput.value.trim();
                if (!novoCaminho) {
                    alert("Por favor, digite um caminho de banco de dados válido!");
                    return;
                }

                fetch('/api/salvar-config', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ db_path: novoCaminho })
                })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        alert(data.message);
                        fecharModal();
                        carregarItens();
                        carregarResumo();
                    } else {
                        alert("Erro ao salvar: " + data.error);
                    }
                })
                .catch(err => alert("Erro ao salvar configuração: " + err));
            });
        }

        function toggleDateSelector() {
            const manual = document.getElementById("date-manual").checked;
            const customInput = document.getElementById("input-data-custom");
            if (manual) {
                customInput.classList.remove("hidden");
            } else {
                customInput.classList.add("hidden");
            }
        }

        async function carregarItens() {
            try {
                const response = await fetch('/api/itens');
                const result = await response.json();
                if (result.success) {
                    dbData = result.data;
                    popularFornecedores();
                } else {
                    document.getElementById("select-fornecedor").innerHTML = '<option value="">-- Configure o Banco na Engrenagem ⚙️ --</option>';
                }
            } catch (err) {
                console.error(err);
                document.getElementById("select-fornecedor").innerHTML = '<option value="">-- Configure o Banco na Engrenagem ⚙️ --</option>';
            }
        }

        async function carregarResumo() {
            try {
                const response = await fetch('/api/resumo');
                const result = await response.json();
                if (result.success) {
                    historicoCompleto = result.changes;
                    limparSelecaoHistorico();
                    const badge = document.getElementById("badge-target-geral");
                    badge.textContent = result.geral_atual + (result.geral_mes ? " (" + result.geral_mes + ")" : "");
                    aplicarFiltrosNoHistórico();
                }
            } catch (err) {
                console.error(err);
            }
        }

        function limparSelecaoHistorico() {
            registroSelecionado = null;
            const botao = document.getElementById('btn-excluir-registro');
            if (botao) botao.disabled = true;
        }

        async function excluirRegistroSelecionado() {
            if (!registroSelecionado) return;
            const linha = historicoCompleto.find(r => r.id_registro === registroSelecionado);
            if (!linha) return;
            const identificacao = `PN: ${linha.part_number || '(meta do fornecedor)'} | Fornecedor: ${linha.cod_fornecedor} | Mês: ${linha.data}`;
            if (!confirm(`Excluir permanentemente o registro abaixo?\n\n${identificacao}\n\nEsta ação não pode ser desfeita.`)) return;
            const botao = document.getElementById('btn-excluir-registro');
            botao.disabled = true;
            try {
                const response = await fetch('/api/excluir-registro', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({id_registro: registroSelecionado})
                });
                const resultado = await response.json();
                if (!response.ok || !resultado.success) throw new Error(resultado.error || 'Erro ao excluir registro.');
                limparSelecaoHistorico();
                await carregarResumo();
                alert('Registro excluído com sucesso.');
            } catch (erro) {
                alert('Não foi possível excluir: ' + (erro instanceof TypeError ? 'Não foi possível contatar o servidor Flask. Verifique se o terminal Python continua aberto e se http://127.0.0.1:5000 está acessível.' : erro.message));
                botao.disabled = false;
            }
        }

        async function exportarExcel(modo) {
            const parametros = new URLSearchParams({modo});
            if (modo === 'filtrado') {
                parametros.set('fornecedor', document.getElementById('select-fornecedor').value);
                parametros.set('pn', document.getElementById('select-pn').value);
            }
            try {
                const resposta = await fetch('/api/exportar-excel?' + parametros.toString());
                if (!resposta.ok) {
                    const erro = await resposta.json().catch(() => ({}));
                    throw new Error(erro.error || 'Não foi possível exportar.');
                }
                const blob = await resposta.blob();
                const url = URL.createObjectURL(blob);
                const elemento = document.createElement('a');
                elemento.href = url;
                const cabecalho = resposta.headers.get('Content-Disposition') || '';
                const nome = cabecalho.match(/filename="?([^";]+)"?/i);
                elemento.download = nome ? nome[1] : 'resumo_targets.xlsx';
                document.body.appendChild(elemento);
                elemento.click();
                elemento.remove();
                setTimeout(() => URL.revokeObjectURL(url), 2000);
            } catch (erro) {
                alert('Erro ao exportar Excel: ' + erro.message);
            }
        }

        function aplicarFiltrosNoHistórico() {
            const selectSupplier = document.getElementById("select-fornecedor").value;
            const selectPN = document.getElementById("select-pn").value;
            const statusFiltro = document.getElementById("status-filtro");
            
            let dadosFiltrados = [...historicoCompleto];
            
            if (selectSupplier || selectPN) {
                statusFiltro.classList.remove("hidden");
            } else {
                statusFiltro.classList.add("hidden");
            }

            if (selectSupplier) {
                dadosFiltrados = dadosFiltrados.filter(row => {
                    const itemDb = dbData.find(item => item.fornecedor === selectSupplier);
                    const codMatch = itemDb ? itemDb.cd_fornecedor : null;
                    return row.fornecedor === selectSupplier || row.cod_fornecedor === codMatch;
                });
            }

            if (selectPN) {
                dadosFiltrados = dadosFiltrados.filter(row => row.part_number === selectPN);
            }

            limparSelecaoHistorico();
            const tbody = document.getElementById("tabela-historico");
            tbody.innerHTML = "";
            
            if (dadosFiltrados.length === 0) {
                tbody.innerHTML = `<tr><td colspan="6" class="p-4 text-center text-gray-400">Nenhum registro encontrado com os filtros aplicados.</td></tr>`;
                return;
            }

            dadosFiltrados.forEach(row => {
                const tr = document.createElement("tr");
                tr.className = "hover:bg-blue-50 cursor-pointer transition duration-75";
                tr.setAttribute('tabindex', '0');
                tr.setAttribute('role', 'button');
                tr.setAttribute('aria-label', 'Selecionar registro para exclusão');
                const selecionar = () => {
                    tbody.querySelectorAll('tr').forEach(t => t.classList.remove('bg-blue-100', 'ring-1', 'ring-blue-500'));
                    registroSelecionado = row.id_registro;
                    tr.classList.add('bg-blue-100', 'ring-1', 'ring-blue-500');
                    document.getElementById('btn-excluir-registro').disabled = false;
                };
                tr.addEventListener('click', selecionar);
                tr.addEventListener('keydown', e => {
                    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); selecionar(); }
                });
                
                let nomeFornecedor = row.fornecedor;
                if (!nomeFornecedor && row.cod_fornecedor) {
                    const found = dbData.find(i => i.cd_fornecedor === row.cod_fornecedor);
                    nomeFornecedor = found ? found.fornecedor : '-';
                }

                tr.innerHTML = `
                    <td class="p-3 border-b font-mono font-semibold text-gray-700">${row.part_number || '-'}</td>
                    <td class="p-3 border-b truncate max-w-[220px]" title="${nomeFornecedor || ''}">${nomeFornecedor || '-'}</td>
                    <td class="p-3 border-b font-mono text-xs">${row.cod_fornecedor || '-'}</td>
                    <td class="p-3 border-b text-xs font-semibold text-gray-500">${row.data}</td>
                    <td class="p-3 border-b text-right font-bold text-green-700">${row.target_pn !== null ? row.target_pn : '-'}</td>
                    <td class="p-3 border-b text-right font-bold text-blue-700">${row.target_supplier !== null ? row.target_supplier : '-'}</td>
                `;
                tbody.appendChild(tr);
            });
        }

        function popularFornecedores() {
            const selectSupplier = document.getElementById("select-fornecedor");
            const suppliers = [...new Set(dbData.map(item => item.fornecedor))].sort();
            
            selectSupplier.innerHTML = '<option value="">-- Todos os Fornecedores --</option>';
            suppliers.forEach(sup => {
                const option = document.createElement("option");
                option.value = sup;
                option.textContent = sup;
                selectSupplier.appendChild(option);
            });
        }

        function onSupplierChange() {
            const selectSupplier = document.getElementById("select-fornecedor");
            const selectPN = document.getElementById("select-pn");
            const codFornecedorInput = document.getElementById("cod-fornecedor");
            const descPecaInput = document.getElementById("desc-peca");
            
            const selectedSupplier = selectSupplier.value;
            
            selectPN.innerHTML = '<option value="">-- Todas as Peças (PN) --</option>';
            selectPN.disabled = true;
            codFornecedorInput.value = "-";
            descPecaInput.value = "-";

            if (!selectedSupplier) {
                aplicarFiltrosNoHistórico();
                return;
            }

            const supplierItens = dbData.filter(item => item.fornecedor === selectedSupplier);
            if (supplierItens.length > 0) {
                codFornecedorInput.value = supplierItens[0].cd_fornecedor;
            }

            selectPN.disabled = false;
            supplierItens.forEach(item => {
                const option = document.createElement("option");
                option.value = item.item;
                option.textContent = item.item;
                selectPN.appendChild(option);
            });

            aplicarFiltrosNoHistórico();
        }

        function onPNChange() {
            const selectPN = document.getElementById("select-pn");
            const descPecaInput = document.getElementById("desc-peca");
            const selectedPN = selectPN.value;
            
            if (!selectedPN) {
                descPecaInput.value = "-";
                aplicarFiltrosNoHistórico();
                return;
            }
            
            const itemMatch = dbData.find(item => item.item === selectedPN);
            if (itemMatch) {
                descPecaInput.value = itemMatch.descricao;
            }
            aplicarFiltrosNoHistórico();
        }

        async function salvarTarget(tipo) {
            let targetValue = 0;
            const part_number = document.getElementById("select-pn").value;
            const cod_fornecedor = document.getElementById("cod-fornecedor").value;

            let dataLancamento = "";
            const manualDateChecked = document.getElementById("date-manual").checked;
            if (manualDateChecked) {
                dataLancamento = document.getElementById("input-data-custom").value;
                if (!dataLancamento) {
                    alert("Selecione um mês válido para o lançamento retroativo!");
                    return;
                }
            }

            if (tipo === 'pn') {
                targetValue = document.getElementById("input-target-pn").value;
                if (!part_number || cod_fornecedor === '-') {
                    alert("Selecione Fornecedor e Part Number primeiro!");
                    return;
                }
            } else if (tipo === 'supplier') {
                targetValue = document.getElementById("input-target-supplier").value;
                if (cod_fornecedor === '-') {
                    alert("Selecione um Fornecedor primeiro!");
                    return;
                }
            } else if (tipo === 'geral') {
                targetValue = document.getElementById("input-target-geral").value;
            }

            if (!targetValue) {
                alert("Por favor, preencha o valor do target!");
                return;
            }

            try {
                const response = await fetch('/api/salvar-target', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        part_number: tipo === 'pn' ? part_number : '',
                        cod_fornecedor: cod_fornecedor !== '-' ? cod_fornecedor : '',
                        target_value: parseFloat(targetValue),
                        tipo: tipo,
                        data_definida: dataLancamento
                    })
                });
                
                const result = await response.json();
                if (result.success) {
                    alert(result.message || "Target atualizado com sucesso!");
                    if(tipo === 'pn') document.getElementById("input-target-pn").value = '';
                    if(tipo === 'supplier') document.getElementById("input-target-supplier").value = '';
                    if(tipo === 'geral') document.getElementById("input-target-geral").value = '';
                    carregarResumo();
                } else {
                    alert("Erro ao salvar: " + result.error);
                }
            } catch (err) {
                console.error(err);
                alert("Erro ao realizar requisição.");
            }
        }
    </script>
</body>
</html>
"""