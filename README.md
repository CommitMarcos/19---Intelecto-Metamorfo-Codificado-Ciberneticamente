# 19---Intelecto-Metamorfo-Codificado-Cibernéticamente
Projeto do CodeRace2026

Link dos slides:
https://canva.link/u4r6gjos1w98ny9

Link do Vídeo (Pitch):
https://youtube.com/shorts/rr5GuyLR4AM?si=RTfTu1qawtb4xlag

Funções dos integrantes:

1-Marcos- Scrum Master e Programador principal
2-Celso- Programador auxiliar
3-Eduarda- Product Owner e analista de negócios
4-Kaueli- Designer
5-Diuliana- Designer 

Problemas

1-Imprevisões climáticas (o que resulta na perda de grandes plantios);
2-Altos custos de investimento (acarreta em poucas vendas e baixa de lucro);
3-Má gestão de produtos a serem coletados e/ou estocados (perda de mercadorias).

Soluções

1-Busca de previsões climáticas via satélite (temperatura, vento, umidade, chuva, etc);
2-Busca de melhores preços do mercado para investimentos pecuários via internet atualizado a cada 24h;
3-Avisos semanais e diários para colheita e gestão de estoque dos produtos coletados, evitando o desperdício de mercadorias;
4-Monitoramento de máquinas em funcionamento ou em manutenção para prevenção de imprevistos e melhor gestão do agronegócio.

Linguagem

A linguagem de programação utilizada foi a Python que oferece Criptografia, o que fornece segurança dos dados pessoais e garante que ninguém roube os dados dos usuários.

Frameworks

1-Streamlit que configura o título, layout, ícone, barra lateral de navegação, controle de acesso, abas de navegação e blocos visuais prontos para mostrar indicadores (como temperatura e umidade);
2-Design System Customizado (CSS), ele altera completamente o visual padrão do Streamlit para criar a interface futurista; e o Fernet que funciona como um framework/padrão de segurança para garantir que os dados sejam criptografados usando a especificação AES-256 de forma simples e segura.

Bibliotecas

1-Streamlit que é a biblioteca principal para criar a tela do sistema. Ela gera a página web, os botões, os gráficos de barras, as abas de navegação e os cartões visuais que o usuário final vê e interage;
2-Cryptography que é uma biblioteca robusta de segurança. O submódulo fernet é usado especificamente para fazer a criptografia simétrica, garantindo que ninguém leia as informações sem autorização; 
3-Hashlib que faz parte das bibliotecas padrão do Python. Ela serve para criar hashes. No código, ela é usada para aplicar o algoritmo SHA-256 e esconder dados sensíveis atendendo às regras da LGPD;
4-Numpy que é a biblioteca mais famosa do Python para computação científica e matemática. Ela foi usada para gerar uma simulação estatística realista de variação de temperatura para os sensores climáticos; 
5-Datetime que é usado para capturar o ano, mês, dia, hora e segundo exatos em que um evento aconteceu; 
6-Time que é usado junto com o Numpy para ajudar a criar uma semente de números aleatórios baseada no relógio do computador;
8-Logging que também é uma biblioteca padrão do Python. Ela serve para salvar mensagens de texto em um arquivo de histórico no servidor. No código, ela registra eventos críticos para que os administradores possam rastrear tudo o que acontece no sistema. 

APIs

1-do Streamlit (para configurar propriedades da página do navegador, gerenciamento de estado, criar elementos de navegação por abas, desenhar blocos de métricas/KPIs na tela e injetar código HTML e estilização CSS customizada na página.);
2-da Criptografia do Fernet (que gera uma chave criptográfica segura de 32 bytes codificada em base64, transforma o texto comum em um texto cifrado usando AES-256 e faz o processo inverso, recuperando o texto original a partir do código cifrado.);
3-do Hashlib (que calcula o algoritmo SHA-256 sobre uma string e retorna o resultado formatado como uma cadeia de caracteres hexadecimais.);
4-do Logging (que faz configuração inicial do sistema de logs e grava uma mensagem com o nível informativo de segurança.);
5-do NumPy (que define a semente inicial para o gerador de números aleatórios e gera números aleatórios baseados em uma distribuição normal, simulando a flutuação da temperatura do sensor.)

Arquitetura

+-------------------------------------------------------------------------+
|                       CAMADA DE APRESENTAÇÃO (UI)                       |
|  [ Sidebar (RBAC) ]   [ Tab 1: Central ]   [ Tab 2: Frota ]   [ Tab 3 ] |
+----------------------------------------------------+--------------------+
                                                     |
                         Injeção de Estilo (CSS)     | Entrada de Dados /
                         e Componentes HTML          | Interação do Usuário
                                                     v
+-------------------------------------------------------------------------+
|                       CAMADA DE REGULAMENTAÇÃO & BI                     |
|  - NumPy (Métricas/KPIs)                - Logging (Auditoria do Sistema)|
+----------------------------------------------------+--------------------+
                                                     |
                                                     | Payload Operacional
                                                     v
+-------------------------------------------------------------------------+
|                       CAMADA DE SEGURANÇA (COMPLIANCE)                  |
|  - Hashlib (SHA-256): Anonimização de IDs / CPFs                        |
|  - Cryptography (Fernet): Criptografia Simétrica AES-256                |
+----------------------------------------------------+--------------------+
                                                     |
                                                     | Dados Protegidos
                                                     v
+-------------------------------------------------------------------------+
|                    CAMADA DE PERSISTÊNCIA EM MEMÓRIA                    |
|             Se Link WAN = Ativo  --> st.session_state.silo_control      |
|             Se Link WAN = Queda  --> st.session_state.db_offline_queue  |
+-------------------------------------------------------------------------+

Situação do projeto

Tudo o que planejamos, acreditamos que ocorreu bem.
