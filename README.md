# Manual do Usuário e Guia de Manutenção: Painel de Atualização e Análise de Targets

Bem-vindo ao guia de utilização do **Painel de Atualização e Análise de Targets** (FundMap BI). Este aplicativo permite consultar o histórico e cadastrar metas (*targets*) de PPM em três níveis: por Peça (*Part Number*), por Fornecedor ou Meta Geral.

---

## 1. Como Iniciar e Encerrar o Aplicativo

### Iniciando o Aplicativo
1. Dê um duplo clique no ícone do aplicativo (**APP**) para executá-lo.
2. Aguarde alguns instantes: o aplicativo iniciará automaticamente e abrirá uma aba no seu navegador padrão com a tela do painel.

### Encerramento Automático
* **Você não precisa fechar nenhum programa manualmente.** 
* Quando terminar de usar o painel, basta **fechar a aba ou a janela do navegador**. Após cerca de 35 segundos sem detectar a aba aberta, o aplicativo se encerra sozinho em segundo plano para liberar os recursos do seu computador.

---

## 2. Configuração do Banco de Dados (Primeiro Acesso ou Mudança de Pasta)

Por padrão, o aplicativo busca o banco de dados diretamente na pasta da rede (`S:\...\FundMap BI\fundmap.db`). Caso a lista de fornecedores exiba a mensagem **"-- Configure o Banco na Engrenagem ⚙️ --"**, siga os passos abaixo:

1. No canto superior direito da tela (ao lado da logo da Bosch Rexroth), clique no ícone da **Engrenagem (⚙️)**.
2. Na janela **Configurações do Banco**, insira o caminho completo (de rede ou local) onde o arquivo `.db` está armazenado (exemplo: `S:\Pasta\fundmap.db`).
3. Clique em **Salvar Configuração**.
4. O sistema testará a conexão automaticamente:
   * Se o arquivo for encontrado e validado, você verá a mensagem *"Caminho do banco de dados atualizado com sucesso!"* e os dados serão carregados na tela imediatamente.
   * Essa configuração fica salva automaticamente na pasta do aplicativo para os seus próximos acessos.

---

## 3. Passo a Passo de Uso do Painel

A interface está dividida em **3 seções principais** para facilitar a rotina de análise e cadastro:

### Seção 1: Selecione para Atualizar ou Analisar
Nesta área, você define quais itens deseja visualizar ou alterar e qual será a data de referência do lançamento:

1. **Fornecedor:** Selecione o fornecedor desejado na lista suspensa. Ao selecioná-lo, o campo **Código do Fornecedor** será preenchido automaticamente e a tabela de histórico (Seção 3) será filtrada para mostrar apenas os registros desse fornecedor.
2. **Código da Peça (PN):** Após escolher o fornecedor, esta lista será habilitada apenas com as peças vinculadas a ele. Ao escolher um *Part Number*, a **Descrição da Peça** aparecerá automaticamente ao lado e o histórico será refinado para exibir apenas essa peça.
3. **Período do Lançamento:**
   * **Mês Atual Automático (Padrão):** Registra a meta considerando o ano e mês vigentes (formato `AAAA-MM`).
   * **Escolher Outro Mês (Lançamento Retroativo):** Ao marcar esta opção, um seletor de calendário aparecerá ao lado para que você escolha exatamente o mês e o ano desejados antes de salvar qualquer target.

---

### Seção 2: Entrada de Novos Targets
Você pode atualizar metas em três níveis independentes. Caso já exista um valor cadastrado para a mesma combinação no mês escolhido, o sistema **atualizará (sobrescreverá)** o valor anterior automaticamente.

| Campo | Nome | O que faz? | Requisitos antes de salvar |
| :--- | :--- | :--- | :--- |
| **Campo 1** *(Verde)* | **Target PN** | Define uma meta específica para uma única peça de um fornecedor. | Selecionar **Fornecedor** e **Código da Peça (PN)** na Seção 1, digitar o valor e clicar em **Salvar Target PN**. |
| **Campo 2** *(Azul)* | **Target Fornecedor** | Define uma meta global aplicável a todas as peças daquele fornecedor. | Selecionar o **Fornecedor** na Seção 1 (não é necessário escolher PN), digitar o valor e clicar em **Salvar Target Fornec.** |
| **Campo 3** *(Roxo)* | **Target Geral** | Define a meta geral global da área. O cartão exibe no canto superior direito o valor **Atual mais recente** e o mês correspondente. | Não exige seleção de fornecedor ou peça. Basta digitar o valor e clicar em **Alterar Target Geral**. |

> **Importante:** Sempre verifique na **Seção 1** se o **Período do Lançamento** está em *Mês Atual Automático* ou se você selecionou o mês retroativo correto antes de clicar em salvar.

---

### Seção 3: Histórico de Mudanças
Na parte inferior da tela, você acompanha as últimas **150 alterações** registradas no banco de dados, ordenadas da mais recente para a mais antiga:

* **Filtro Dinâmico:** Sempre que um Fornecedor ou *Part Number* estiver selecionado na Seção 1, um selo azul escrito **Filtrado** aparecerá ao lado do título da seção, exibindo apenas o histórico correspondente à sua seleção. Para voltar a ver o histórico de todos os fornecedores, mude o campo Fornecedor na Seção 1 para `-- Todos os Fornecedores --`.
* **Botão Atualizar Resumo:** Clique neste botão amarelo a qualquer momento para recarregar os dados diretamente do banco de dados (útil caso outro usuário tenha feito alterações na rede simultaneamente).

---

## 4. Solução de Problemas Comuns (FAQ)

* **Os fornecedores não carregam ao abrir o APP:**
  Verifique se você está conectado à rede corporativa (VPN/Unidade `S:`) e confira se o caminho do arquivo `fundmap.db` está correto clicando no ícone da **Engrenagem (⚙️)**.
* **Mensagem *"Selecione Fornecedor e Part Number primeiro!"*:**
  Para lançar um **Target PN** (Campo 1), é obrigatório selecionar tanto o fornecedor quanto o código da peça na Seção 1.
* **Como corrigir um lançamento digitado errado?**
  Basta selecionar o mesmo Fornecedor/Peça e o mesmo Mês de Lançamento na Seção 1, digitar o valor correto no campo correspondente e clicar em salvar. O sistema atualizará o registro existente sem duplicar linhas para o mesmo período.
* **Fechei a aba do navegador sem querer e tentei reabrir rápido:**
  Se você fechou a aba há menos de 35 segundos, basta clicar novamente no atalho do aplicativo ou reabrir a aba que foi fechada. Caso já tenha passado esse tempo, dê um duplo clique no executável do APP para iniciá-lo novamente.

---

## 5. Manutenção do Código (Guia para Desenvolvedores)

Caso seja necessário alterar a interface visual, regras de negócio, tabelas do banco de dados ou atualizar a logo do sistema, consulte a estrutura abaixo antes de gerar um novo executável.

### Estrutura dos Arquivos do Projeto

| Arquivo | Função no Projeto |
| :--- | :--- |
| `app.py` | **Backend principal (Flask).** Gerencia a conexão com o SQLite (em modo `WAL` para suportar múltiplos acessos simultâneos na rede), expõe as rotas da API (`/api/itens`, `/api/resumo`, `/api/salvar-target`, `/api/config`), abre o navegador na porta `5000` e controla o encerramento automático por *heartbeat*. |
| `gerar_logo.py` | **Gerador de Template.** Lê o arquivo de imagem `Bosch_Rexroth-Logo.wine.png`, converte para *Base64* e recria automaticamente o arquivo `html.py` com o código HTML/JavaScript embutido. |
| `html.py` | **Frontend embutido.** Contém a variável `HTML_TEMPLATE` importada pelo `app.py`. Estilizado com TailwindCSS e FontAwesome via CDN. |
| `config.json` | **Configuração persistente.** Gerado automaticamente na mesma pasta do executável quando o usuário altera o caminho do banco de dados pela interface. |

---

### Como Alterar a Interface (HTML / CSS / JS) ou a Logo

> **Atenção:** Evite editar apenas o arquivo `html.py` caso pretenda rodar o script `gerar_logo.py` no futuro, pois o `gerar_logo.py` sobrescreve completamente o `html.py`.

1. **Para atualizar o layout, textos ou scripts do Frontend:**
   * Abra o arquivo `gerar_logo.py` e faça as alterações dentro da variável `HTML_CONTENT_TEMPLATE`.
   * Certifique-se de que a imagem `Bosch_Rexroth-Logo.wine.png` esteja na mesma pasta.
   * Execute o script `python gerar_logo.py` para gerar o novo `html.py` atualizado.
2. **Para trocar a imagem da Logo:**
   * Substitua o arquivo `Bosch_Rexroth-Logo.wine.png` na pasta do projeto (ou altere a constante `NOME_IMAGEM` no `gerar_logo.py`) e execute `python gerar_logo.py`.

---

### Estrutura Esperada do Banco de Dados SQLite (`fundmap.db`)

O arquivo `app.py` realiza leituras e gravações nas seguintes tabelas do SQLite:

* **`itens_fornecedor`** *(Leitura)*:
  * Colunas utilizadas: `item`, `descricao`, `cd_fornecedor`, `fornecedor`, `regiao`.
* **`ppm_target_changes`** *(Leitura e Escrita)*:
  * Colunas utilizadas: `part_number`, `cod_fornecedor`, `data` (`YYYY-MM`), `target_pn`, `target_supplier`.
  * Possui restrição de chave única (`ON CONFLICT(part_number, cod_fornecedor, data) DO UPDATE`) para sobrescrever metas lançadas no mesmo mês. Quando o lançamento é de *Target Fornecedor*, o `part_number` é gravado como string vazia (`''`).
* **`target_ppm_geral`** *(Leitura e Escrita)*:
  * Colunas utilizadas: `ano_mes` (`YYYY-MM`), `target`.

---

### Ajustando o Tempo de Encerramento Automático (*Heartbeat*)

O navegador envia um sinal (`POST /api/heartbeat`) a cada **2 segundos**. No arquivo `app.py`, a função `monitor_inatividade()`:
* Aguarda **20 segundos** iniciais na abertura para computadores mais lentos carregarem o navegador.
* Encerra o processo (`os._exit(0)`) caso fique mais de **35 segundos** sem receber resposta da aba. Se necessário, ajuste esses valores diretamente em `monitor_inatividade()`.

---

### Como Compilar um Novo Executável (PyInstaller)

Após realizar e testar suas alterações rodando `python app.py`:

1. Certifique-se de ter as dependências instaladas no ambiente:
   ```bash
   pip install flask pyinstaller
   ```
2. Gere o novo executável em arquivo único e sem janela de terminal preta (`--noconsole` / `-w`):
   ```bash
   pyinstaller --onefile --noconsole --name "Painel_Targets" app.py
   ```
3. O novo aplicativo estará disponível dentro da pasta `dist/`. Basta copiá-lo para a pasta de uso dos usuários (não é necessário levar os arquivos `.py` junto com o `.exe`, pois o `html.py` já fica compilado dentro dele).
