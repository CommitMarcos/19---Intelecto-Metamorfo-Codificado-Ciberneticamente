import datetime
import hashlib
import logging
import time
from cryptography.fernet import Fernet
import numpy as np
import streamlit as st

# ==============================================================================
# 1. ARQUITETURA DE SEGURANÇA E GOVERNANÇA DE DADOS (COMPLIANCE LGPD)
# ==============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] SECURITY_AUDIT: %(message)s'
)

if 'crypto_key' not in st.session_state:
    st.session_state.crypto_key = Fernet.generate_key().decode()
if 'audit_logs' not in st.session_state:
    st.session_state.audit_logs = []
if 'user_role' not in st.session_state:
    st.session_state.user_role = "Operador de Campo"

cipher_suite = Fernet(st.session_state.crypto_key.encode())


def registrar_log_auditoria(
    usuario: str, acao: str, modulo: str, criticidade: str
):
    """Registra eventos críticos para fins de compliance regulatório da LGPD."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hash_txt = f"{timestamp}{acao}".encode()
    log_entry = {
        "timestamp": timestamp,
        "usuario": usuario,
        "modulo": modulo,
        "acao": acao,
        "criticidade": criticidade,
        "hash_verificacao": hashlib.sha256(hash_txt).hexdigest()[:16]
    }
    st.session_state.audit_logs.append(log_entry)
    msg = (
        f"User: {usuario} | Action: {acao} | "
        f"Module: {modulo} | Severity: {criticidade}"
    )
    logging.info(msg)


def anonimizar_id(identificador: str) -> str:
    """Aplica Hash SHA-256 para anonimização de dados sensíveis de operadores."""
    return hashlib.sha256(identificador.encode()).hexdigest()[:12].upper()


def encriptar_payload(dados: str) -> str:
    """Criptografa payloads operacionais para persistência segura em cache offline."""
    return cipher_suite.encrypt(dados.encode()).decode()


def decriptar_payload(dados_cripto: str) -> str:
    """Decodifica as cadeias binárias protegidas para processamento interno."""
    return cipher_suite.decrypt(dados_cripto.encode()).decode()


# ==============================================================================
# 2. CONFIGURAÇÃO DE INTERFACE E DESIGN SYSTEM (PALETA AGRONEXUS DARK)
# ==============================================================================
st.set_page_config(
    page_title="AgroNexus Enterprise - Framework Unificado",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS — AgroNexus Dark Premium Design System
st.markdown("""
<style>
/* ── Imports & Variables ───────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Syne:wght@400;600;700;800&display=swap');

:root {
    --bg-base:        #070F0A;
    --bg-surface:     #0D1F12;
    --bg-raised:      #112918;
    --bg-overlay:     #183824;
    --border-subtle:  rgba(77,153,38,0.18);
    --border-default: rgba(77,153,38,0.35);
    --border-strong:  rgba(77,153,38,0.65);
    --green-primary:  #4D9926;
    --green-bright:   #5EC12E;
    --green-muted:    #2E6B17;
    --green-glow:     rgba(77,153,38,0.25);
    --amber:          #D69E2E;
    --red:            #E05252;
    --text-primary:   #EAF5E1;
    --text-secondary: #8AB07A;
    --text-muted:     #4A6B40;
    --radius-sm:      6px;
    --radius-md:      10px;
    --radius-lg:      14px;
    --shadow-card:    0 4px 24px rgba(0,0,0,0.45), 0 1px 4px rgba(77,153,38,0.08);
    --shadow-glow:    0 0 20px rgba(77,153,38,0.15);
    --font-display:   'Syne', sans-serif;
    --font-mono:      'JetBrains Mono', monospace;
}

/* ── Global Reset ──────────────────────────────────────────────────────── */
.stApp {
    background-color: var(--bg-base) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-display);
}

/* Subtle hex-grid texture overlay */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: radial-gradient(
        circle at 1px 1px,
        rgba(77,153,38,0.04) 1px,
        transparent 0
    );
    background-size: 32px 32px;
    pointer-events: none;
    z-index: 0;
}

/* ── Typography ────────────────────────────────────────────────────────── */
h1, h2, h3, h4, h5, h6 {
    font-family: var(--font-display) !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.02em;
}

h1 { font-size: 1.75rem !important; font-weight: 800 !important; }
h2 { font-size: 1.25rem !important; font-weight: 700 !important; }
h3 { font-size: 1.05rem !important; font-weight: 600 !important; }

p, li, label, .stMarkdown {
    color: var(--text-secondary) !important;
    font-size: 0.9rem;
    line-height: 1.65;
}

/* ── Sidebar ───────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--bg-surface) 0%, var(--bg-base) 100%) !important;
    border-right: 1px solid var(--border-subtle) !important;
}

[data-testid="stSidebar"] .stMarkdown h3 {
    font-size: 0.7rem !important;
    font-family: var(--font-mono) !important;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--green-primary) !important;
    margin-bottom: 8px;
    opacity: 0.8;
}

/* ── Metrics ───────────────────────────────────────────────────────────── */
[data-testid="stMetricValue"] {
    font-family: var(--font-mono) !important;
    font-size: 1.8rem !important;
    font-weight: 600 !important;
    color: var(--green-bright) !important;
    letter-spacing: -0.03em;
}

[data-testid="stMetricLabel"] {
    font-size: 0.72rem !important;
    font-family: var(--font-mono) !important;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-muted) !important;
}

[data-testid="stMetricDelta"] {
    font-family: var(--font-mono) !important;
    font-size: 0.75rem !important;
}

[data-testid="metric-container"] {
    background: var(--bg-raised) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-md) !important;
    padding: 16px 18px !important;
    box-shadow: var(--shadow-card) !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

[data-testid="metric-container"]:hover {
    border-color: var(--border-default) !important;
    box-shadow: var(--shadow-glow) !important;
}

/* ── Tabs ──────────────────────────────────────────────────────────────── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: var(--bg-surface) !important;
    border-bottom: 1px solid var(--border-subtle) !important;
    gap: 4px;
    padding: 0 4px;
    border-radius: var(--radius-md) var(--radius-md) 0 0;
}

[data-testid="stTabs"] [data-baseweb="tab"] {
    font-family: var(--font-display) !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    color: var(--text-muted) !important;
    letter-spacing: 0.04em;
    padding: 10px 18px !important;
    border-radius: var(--radius-sm) var(--radius-sm) 0 0 !important;
    border: none !important;
    background: transparent !important;
    transition: color 0.2s ease, background 0.2s ease;
}

[data-testid="stTabs"] [aria-selected="true"] {
    color: var(--green-bright) !important;
    background: var(--bg-raised) !important;
    border-bottom: 2px solid var(--green-primary) !important;
}

[data-testid="stTabs"] [data-baseweb="tab"]:hover {
    color: var(--text-primary) !important;
    background: var(--bg-overlay) !important;
}

[data-testid="stTabsContent"] {
    background: var(--bg-raised) !important;
    border: 1px solid var(--border-subtle) !important;
    border-top: none !important;
    border-radius: 0 0 var(--radius-md) var(--radius-md) !important;
    padding: 24px !important;
}

/* ── Buttons ───────────────────────────────────────────────────────────── */
div.stButton > button {
    background: linear-gradient(135deg, var(--green-primary), var(--green-muted)) !important;
    color: #fff !important;
    font-family: var(--font-display) !important;
    font-weight: 700 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    border-radius: var(--radius-sm) !important;
    padding: 10px 22px !important;
    border: 1px solid var(--border-strong) !important;
    box-shadow: 0 2px 12px rgba(77,153,38,0.3) !important;
    transition: all 0.2s ease !important;
}

div.stButton > button:hover {
    background: linear-gradient(135deg, var(--green-bright), var(--green-primary)) !important;
    box-shadow: 0 4px 20px rgba(77,153,38,0.5) !important;
    transform: translateY(-1px) !important;
}

div.stButton > button:active {
    transform: translateY(0px) !important;
}

/* ── Inputs & Selects ──────────────────────────────────────────────────── */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] > div > div {
    background: var(--bg-surface) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.85rem !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus {
    border-color: var(--green-primary) !important;
    box-shadow: 0 0 0 2px var(--green-glow) !important;
}

/* ── Alerts ────────────────────────────────────────────────────────────── */
[data-testid="stAlert"] {
    border-radius: var(--radius-md) !important;
    border-width: 1px !important;
    font-family: var(--font-display) !important;
    font-size: 0.85rem !important;
}

[data-testid="stAlert"][data-baseweb="notification"] {
    background: rgba(224,82,82,0.12) !important;
    border-color: rgba(224,82,82,0.4) !important;
}

/* Warning override */
div[data-baseweb="notification"][kind="warning"],
.stWarning {
    background: rgba(214,158,46,0.12) !important;
    border-color: rgba(214,158,46,0.4) !important;
}

/* ── Progress Bar ──────────────────────────────────────────────────────── */
[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(
        90deg, var(--green-muted), var(--green-primary), var(--green-bright)
    ) !important;
    border-radius: 99px !important;
}

[data-testid="stProgressBar"] > div {
    background: var(--bg-overlay) !important;
    border-radius: 99px !important;
    height: 10px !important;
}

/* ── Expander ──────────────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    background: var(--bg-surface) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-md) !important;
    overflow: hidden;
}

[data-testid="stExpander"] summary {
    font-family: var(--font-display) !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    color: var(--text-secondary) !important;
    padding: 12px 16px !important;
    background: var(--bg-raised) !important;
    transition: background 0.2s ease;
}

[data-testid="stExpander"] summary:hover {
    background: var(--bg-overlay) !important;
    color: var(--text-primary) !important;
}

/* ── Toggle ────────────────────────────────────────────────────────────── */
[data-testid="stToggle"] span[data-checked="true"] {
    background: var(--green-primary) !important;
}

/* ── Divider ───────────────────────────────────────────────────────────── */
hr {
    border-color: var(--border-subtle) !important;
    margin: 20px 0 !important;
}

/* ── Scrollbar ─────────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb {
    background: var(--green-muted);
    border-radius: 99px;
}
::-webkit-scrollbar-thumb:hover { background: var(--green-primary); }

/* ── Custom Components ─────────────────────────────────────────────────── */

/* Section header label */
.section-label {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--green-primary);
    opacity: 0.7;
    margin-bottom: 4px;
}

/* Status badge */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 3px 10px;
    border-radius: 99px;
    font-family: var(--font-mono);
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

.badge-green {
    background: rgba(77,153,38,0.15);
    border: 1px solid rgba(77,153,38,0.4);
    color: #5EC12E;
}

.badge-amber {
    background: rgba(214,158,46,0.15);
    border: 1px solid rgba(214,158,46,0.4);
    color: #D69E2E;
}

.badge-red {
    background: rgba(224,82,82,0.15);
    border: 1px solid rgba(224,82,82,0.45);
    color: #E05252;
}

/* Fleet card */
.fleet-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-lg);
    padding: 16px 20px;
    margin-bottom: 12px;
    box-shadow: var(--shadow-card);
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
    position: relative;
    overflow: hidden;
}

.fleet-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    border-radius: 99px 0 0 99px;
}

.fleet-card.crit-none::before  { background: var(--green-primary); }
.fleet-card.crit-media::before { background: var(--amber); }
.fleet-card.crit-alta::before  { background: var(--red); }

.fleet-card:hover {
    border-color: var(--border-default);
    box-shadow: var(--shadow-glow);
}

.fleet-card .fc-id {
    font-family: var(--font-mono);
    font-size: 0.68rem;
    color: var(--text-muted);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 2px;
}

.fleet-card .fc-name {
    font-family: var(--font-display);
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 10px;
}

.fleet-card .fc-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.fleet-card .fc-meta {
    font-family: var(--font-mono);
    font-size: 0.75rem;
    color: var(--text-secondary);
}

.fleet-card .fc-meta span {
    color: var(--text-muted);
    margin-right: 4px;
}

/* Network status pill */
.net-pill {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 14px;
    border-radius: var(--radius-sm);
    font-family: var(--font-mono);
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-top: 6px;
}

.net-pill.online {
    background: rgba(77,153,38,0.12);
    border: 1px solid rgba(77,153,38,0.35);
    color: #5EC12E;
}

.net-pill.offline {
    background: rgba(214,158,46,0.12);
    border: 1px solid rgba(214,158,46,0.35);
    color: #D69E2E;
}

.net-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    flex-shrink: 0;
    animation: pulse-dot 1.8s ease-in-out infinite;
}

.net-dot.green { background: #5EC12E; box-shadow: 0 0 6px #5EC12E; }
.net-dot.amber { background: #D69E2E; box-shadow: 0 0 6px #D69E2E; }

@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.5; transform: scale(0.75); }
}

/* Session signature */
.session-sig {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-sm);
    padding: 10px 14px;
    margin-top: 8px;
}

.session-sig .sig-label {
    font-family: var(--font-mono);
    font-size: 0.62rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 4px;
}

.session-sig .sig-value {
    font-family: var(--font-mono);
    font-size: 0.78rem;
    color: var(--green-primary);
    letter-spacing: 0.04em;
}

/* Dashboard page title */
.dash-title-block {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 6px;
}

.dash-title-block .dash-icon {
    font-size: 1.6rem;
    line-height: 1;
}

.dash-title-block h1 {
    margin: 0 !important;
    padding: 0 !important;
}

/* Status bar */
.status-bar {
    display: flex;
    align-items: center;
    gap: 20px;
    padding: 8px 16px;
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-sm);
    margin-bottom: 24px;
    flex-wrap: wrap;
}

.status-bar .sb-item {
    display: flex;
    align-items: center;
    gap: 6px;
    font-family: var(--font-mono);
    font-size: 0.7rem;
    color: var(--text-muted);
    letter-spacing: 0.05em;
}

.status-bar .sb-item strong {
    color: var(--text-secondary);
}

/* Audit log table */
.audit-row {
    display: grid;
    grid-template-columns: 160px 1fr 1fr 80px;
    gap: 12px;
    padding: 10px 14px;
    border-bottom: 1px solid var(--border-subtle);
    font-family: var(--font-mono);
    font-size: 0.75rem;
    color: var(--text-secondary);
    transition: background 0.15s ease;
}

.audit-row:hover { background: var(--bg-raised); }

.audit-row.header {
    color: var(--text-muted);
    font-size: 0.65rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    border-bottom: 1px solid var(--border-default);
    padding-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. GERENCIADOR DE ESTADO OPERACIONAL (DATASTORE EM MEMÓRIA SECRETA)
# ==============================================================================
if 'db_offline_queue' not in st.session_state:
    st.session_state.db_offline_queue = []
if 'network_state' not in st.session_state:
    st.session_state.network_state = True
if 'frotas_db' not in st.session_state:
    st.session_state.frotas_db = [
        {
            "id": "JD-790",
            "nome": "John Deere S790",
            "horimetro": 3520,
            "status": "Em Campo",
            "criticidade": "Nenhuma"
        },
        {
            "id": "CASE-410",
            "nome": "Case Axial Flow 8250",
            "horimetro": 4100,
            "status": "Maint preventiva",
            "criticidade": "Média"
        },
        {
            "id": "TR-8R",
            "nome": "Trator Valmet 8R 410",
            "horimetro": 5800,
            "status": "Parado por Falha",
            "criticidade": "Alta"
        }
    ]
if 'silo_control' not in st.session_state:
    st.session_state.silo_control = {"ocupado": 850.0, "max": 1000.0}

# ==============================================================================
# 4. PAINEL LATERAL (CONTROLE DE ACESSO RBAC E SIMULAÇÃO DE INFRAESTRUTURA)
# ==============================================================================
with st.sidebar:
    st.markdown(
        "<div style='padding:18px 0 8px;'>"
        "<span style='font-family:var(--font-display,sans-serif);"
        "font-size:1.15rem;font-weight:800;color:#4D9926;letter-spacing:-0.02em;'>"
        "🛡️ AgroNexus</span>"
        "<span style='font-family:var(--font-mono,monospace);font-size:0.62rem;"
        "color:#4A6B40;letter-spacing:0.1em;display:block;margin-top:2px;'>"
        "ENTERPRISE GATEWAY v3.1</span></div>",
        unsafe_allow_html=True
    )
    st.markdown("---")

    st.markdown("### 🔐 Controle de Acesso (RBAC)")
    usuario_ativo = st.text_input(
        "ID do Usuário Autenticado", value="PRODUTOR_BR_451"
    )
    perfis = ["Operador de Campo", "Gerente Geral", "Auditor de Segurança"]
    st.session_state.user_role = st.selectbox(
        "Perfil de Acesso Governamental", perfis
    )

    st.markdown("---")
    st.markdown("### 🌐 Infraestrutura de Rede")
    chk_net = st.toggle(
        "Link de Conexão Ativo (WAN)",
        value=st.session_state.network_state
    )

    if chk_net != st.session_state.network_state:
        st.session_state.network_state = chk_net
        acao_net = (
            "Restabelecimento de Link" if chk_net else "Queda de Sinal WAN"
        )
        registrar_log_auditoria(
            usuario_ativo, acao_net, "Infraestrutura", "Alta"
        )

    if st.session_state.network_state:
        st.markdown(
            "<div class='net-pill online'>"
            "<div class='net-dot green'></div>"
            "📡 Link Seguro · TLS 1.3 Ativo"
            "</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "<div class='net-pill offline'>"
            "<div class='net-dot amber'></div>"
            "⚠️ Sinal em Queda · Buffer Local"
            "</div>",
            unsafe_allow_html=True
        )

    st.markdown("---")
    hash_sessao = hashlib.sha256(
        st.session_state.crypto_key.encode()
    ).hexdigest()[:10]
    st.markdown(
        f"<div class='session-sig'>"
        f"<div class='sig-label'>Assinatura Digital da Sessão</div>"
        f"<div class='sig-value'>SHA256:{hash_sessao.upper()}</div>"
        f"</div>",
        unsafe_allow_html=True
    )

# ==============================================================================
# 5. DASHBOARD PRINCIPAL - ESTRUTURA DE TABS
# ==============================================================================
st.markdown(
    "<div class='dash-title-block'>"
    "<span class='dash-icon'>🛡️</span>"
    "<h1>Dashboard Operacional Integrado</h1>"
    "</div>",
    unsafe_allow_html=True
)

hash_sessao_display = hashlib.sha256(
    st.session_state.crypto_key.encode()
).hexdigest()[:10]

st.markdown(
    f"<div class='status-bar'>"
    f"<div class='sb-item'>🔒 <strong>Criptografia</strong> Simétrica Ativa</div>"
    f"<div class='sb-item'>👤 <strong>Perfil</strong> {st.session_state.user_role}</div>"
    f"<div class='sb-item'>🔑 <strong>Sessão</strong> SHA256:{hash_sessao_display.upper()}</div>"
    f"</div>",
    unsafe_allow_html=True
)

tabs_nomes = [
    "📊 Central de Operações",
    "🚜 Frota e Maquinário",
    "🕵️ Auditoria (LGPD)",
    "📚 Arquitetura"
]
tab_dashboard, tab_frota, tab_auditoria, tab_documentacao = st.tabs(tabs_nomes)

# ── TAB 1 — Central de Operações ───────────────────────────────────────────
with tab_dashboard:
    col_esquerda, col_direita = st.columns([1.1, 0.9], gap="large")

    with col_esquerda:
        # — Módulo Agroclimático —
        st.markdown(
            "<div class='section-label'>🌤️ Módulo Agroclimático de Precisão</div>",
            unsafe_allow_html=True
        )
        st.markdown("#### Telemetria Climática Regional")

        np.random.seed(int(time.time()) // 10)
        variacao_temp = np.random.normal(0, 0.5)
        temp_atual = round(28.5 + variacao_temp, 1)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric(
                label="Temp. Sensor",
                value=f"{temp_atual} °C",
                delta="Estabilizado"
            )
        with c2:
            st.metric(
                label="Umidade Solo",
                value="38.2 %",
                delta="-1.4 %",
                delta_color="inverse"
            )
        with c3:
            st.metric(
                label="Vel. Vento",
                value="14.5 km/h",
                delta="Normal"
            )

        st.markdown("<br>", unsafe_allow_html=True)
        st.error(
            "⚠️ **ALERTA CRÍTICO — MANEJO:** Precipitação severa prevista para as "
            "próximas 24h na coordenada vinculada. Risco iminente de perdas por "
            "lixiviação no **Talhão A**."
        )

        st.markdown("---")

        # — Logística de Silos —
        st.markdown(
            "<div class='section-label'>🌾 Logística e Armazenamento</div>",
            unsafe_allow_html=True
        )
        st.markdown("#### Controle de Silos Cooperativos")

        silo = st.session_state.silo_control
        percentual_ocupado = int((silo["ocupado"] / silo["max"]) * 100)

        c_silo1, c_silo2, c_silo3 = st.columns(3)
        with c_silo1:
            st.metric(
                "Volume Atual",
                f"{silo['ocupado']:.0f} t",
                help="Toneladas armazenadas atualmente."
            )
        with c_silo2:
            st.metric(
                "Disponível",
                f"{silo['max'] - silo['ocupado']:.0f} t"
            )
        with c_silo3:
            st.metric("Ocupação", f"{percentual_ocupado}%")

        st.progress(
            percentual_ocupado / 100,
            text=f"Capacidade Total Utilizada: {percentual_ocupado}%"
        )

        with st.expander("📝 Registrar Nova Entrada de Carga"):
            if st.session_state.user_role == "Operador de Campo":
                st.warning(
                    "🔒 Operadores de Campo possuem permissão de escrita "
                    "limitada por RBAC."
                )

            form_peso = st.number_input(
                "Peso da Carga (t)",
                min_value=1.0, max_value=100.0, value=25.0
            )
            form_motorista = st.text_input(
                "CPF/ID do Motorista", value="452.128.932-11"
            )

            if st.button("✅ Confirmar Entrada e Encriptar"):
                if silo["ocupado"] + form_peso > silo["max"]:
                    st.error(
                        "❌ Transbordo de segurança! "
                        "Capacidade máxima do silo excedida."
                    )
                else:
                    id_anonimo = anonimizar_id(form_motorista)
                    payload_bruto = (
                        f"Carga:{form_peso}t|Motorista_Hash:{id_anonimo}"
                    )
                    payload_cripto = encriptar_payload(payload_bruto)

                    if st.session_state.network_state:
                        st.session_state.silo_control["ocupado"] += form_peso
                        registrar_log_auditoria(
                            usuario_ativo,
                            f"Entrada de {form_peso}t registrada",
                            "Logística/Silos",
                            "Média"
                        )
                        st.success(
                            f"✅ Carga de **{form_peso}t** confirmada. "
                            f"Motorista anonimizado: `{id_anonimo}`"
                        )
                    else:
                        st.session_state.db_offline_queue.append(payload_cripto)
                        st.warning(
                            "📦 Payload encriptado e adicionado à fila "
                            "offline para sincronização posterior."
                        )

    with col_direita:
        # — Indicadores KPI —
        st.markdown(
            "<div class='section-label'>📈 Indicadores Operacionais</div>",
            unsafe_allow_html=True
        )
        st.markdown("#### KPIs da Operação Atual")

        kpi1, kpi2 = st.columns(2)
        with kpi1:
            st.metric("Máquinas Ativas", "2 / 3", delta="-1 Parada")
        with kpi2:
            st.metric("Alertas Abertos", "1", delta_color="inverse", delta="Alta")

        kpi3, kpi4 = st.columns(2)
        with kpi3:
            st.metric("Logs de Auditoria", len(st.session_state.audit_logs))
        with kpi4:
            fila = len(st.session_state.db_offline_queue)
            st.metric("Fila Offline", fila, help="Payloads aguardando sync")

        st.markdown("---")
        st.markdown(
            "<div class='section-label'>🚨 Frota — Resumo Crítico</div>",
            unsafe_allow_html=True
        )
        st.markdown("#### Status de Alta Prioridade")

        for maq in st.session_state.frotas_db:
            if maq["criticidade"] in ("Média", "Alta"):
                crit_cls = (
                    "crit-alta" if maq["criticidade"] == "Alta"
                    else "crit-media"
                )
                badge_cls = (
                    "badge-red" if maq["criticidade"] == "Alta"
                    else "badge-amber"
                )
                st.markdown(
                    f"<div class='fleet-card {crit_cls}'>"
                    f"<div class='fc-id'>{maq['id']}</div>"
                    f"<div class='fc-name'>{maq['nome']}</div>"
                    f"<div class='fc-row'>"
                    f"<div class='fc-meta'>"
                    f"<span>Horímetro</span>{maq['horimetro']:,} h"
                    f"</div>"
                    f"<div class='badge {badge_cls}'>"
                    f"⚠ {maq['criticidade']}</div>"
                    f"</div></div>",
                    unsafe_allow_html=True
                )

# ── TAB 2 — Frota e Maquinário ─────────────────────────────────────────────
with tab_frota:
    st.markdown(
        "<div class='section-label'>🚜 Gestão de Frota e Maquinário</div>",
        unsafe_allow_html=True
    )
    st.markdown("#### Inventário Completo de Ativos")
    st.markdown("<br>", unsafe_allow_html=True)

    for maq in st.session_state.frotas_db:
        crit = maq["criticidade"]
        if crit == "Alta":
            crit_cls, badge_cls, dot = "crit-alta", "badge-red", "🔴"
        elif crit == "Média":
            crit_cls, badge_cls, dot = "crit-media", "badge-amber", "🟡"
        else:
            crit_cls, badge_cls, dot = "crit-none", "badge-green", "🟢"

        st.markdown(
            f"<div class='fleet-card {crit_cls}'>"
            f"<div class='fc-id'>{dot} {maq['id']}</div>"
            f"<div class='fc-name'>{maq['nome']}</div>"
            f"<div class='fc-row'>"
            f"<div class='fc-meta'>"
            f"<span>Horímetro</span>{maq['horimetro']:,} h &nbsp;·&nbsp; "
            f"<span>Status</span>{maq['status']}"
            f"</div>"
            f"<div class='badge {badge_cls}'>Criticidade: {crit}</div>"
            f"</div></div>",
            unsafe_allow_html=True
        )

# ── TAB 3 — Registro de Auditoria ──────────────────────────────────────────
with tab_auditoria:
    st.markdown(
        "<div class='section-label'>🕵️ Registro de Auditoria — Compliance LGPD</div>",
        unsafe_allow_html=True
    )
    st.markdown("#### Trilha de Auditoria Imutável")

    if not st.session_state.audit_logs:
        st.info(
            "ℹ️ Nenhum evento registrado nesta sessão ainda. "
            "Interaja com o sistema para gerar logs."
        )
    else:
        st.markdown(
            "<div class='audit-row header'>"
            "<span>Timestamp</span><span>Ação</span>"
            "<span>Módulo</span><span>Criticidade</span>"
            "</div>",
            unsafe_allow_html=True
        )
        for log in reversed(st.session_state.audit_logs):
            crit = log["criticidade"]
            badge_cls = (
                "badge-red" if crit == "Alta"
                else "badge-amber" if crit == "Média"
                else "badge-green"
            )
            st.markdown(
                f"<div class='audit-row'>"
                f"<span style='color:var(--text-muted)'>{log['timestamp']}</span>"
                f"<span>{log['acao']}</span>"
                f"<span>{log['modulo']}</span>"
                f"<span class='badge {badge_cls}'>{crit}</span>"
                f"</div>",
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)
        st.caption(
            f"Total de eventos registrados nesta sessão: "
            f"**{len(st.session_state.audit_logs)}**"
        )

# ── TAB 4 — Arquitetura do Sistema ─────────────────────────────────────────
with tab_documentacao:
    st.markdown(
        "<div class='section-label'>📚 Arquitetura e Documentação Técnica</div>",
        unsafe_allow_html=True
    )
    st.markdown("#### Visão Geral do Sistema AgroNexus Enterprise")

    col_doc1, col_doc2 = st.columns(2, gap="large")

    with col_doc1:
        st.markdown("**Camada de Segurança**")
        st.markdown("""
- Criptografia simétrica **Fernet (AES-256-CBC + HMAC-SHA256)**
- Hash **SHA-256** para anonimização de dados pessoais (LGPD Art. 12)
- Controle de acesso baseado em perfis (**RBAC** — 3 níveis)
- Trilha de auditoria imutável com hash de verificação por evento
- Sessões assinadas digitalmente por fingerprint SHA-256
        """)

        st.markdown("**Infraestrutura de Dados**")
        st.markdown("""
- Estado gerenciado via `st.session_state` (in-memory, escopo de sessão)
- Fila offline criptografada para operação sem conectividade WAN
- Simulador de link WAN com log automático de eventos de rede
        """)

    with col_doc2:
        st.markdown("**Módulos Funcionais**")
        st.markdown("""
- 🌤️ **Agroclimático** — Telemetria de temperatura, umidade e vento
- 🌾 **Silos** — Controle de entrada de carga com RBAC e anonimização
- 🚜 **Frota** — Inventário de ativos com criticidade e horímetro
- 🕵️ **Auditoria** — Trilha de compliance LGPD em tempo real
        """)

        st.markdown("**Stack Tecnológico**")
        st.markdown("""
- **Frontend:** Streamlit · CSS Custom Design System
- **Crypto:** `cryptography.fernet` · `hashlib` SHA-256
- **Data:** `numpy` · `st.session_state`
- **Compliance:** LGPD · RBAC · Audit Trail
        """)

