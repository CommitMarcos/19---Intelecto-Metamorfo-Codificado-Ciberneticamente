from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AgroNexusAPI")

# CORS ativado para permitir que o site do frontend acesse esta API de qualquer servidor com segurança
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# BANCO EM MEMÓRIA SIMULADO
# =========================

clima = {
    "temperatura": 29,
    "condicao": "Chuva Forte",
    "risco": True,
    "alerta": "Risco de chuva severa nas próximas 24h. Antecipe a colheita do Talhão A."
}

colheita = [
    {"talhao": "Talhão A", "progresso": 75, "volume": 220},
    {"talhao": "Talhão B", "progresso": 45, "volume": 130},
    {"talhao": "Talhão C", "progresso": 20, "volume": 80}
]

silos = {
    "capacidade_total": 1000,
    "ocupado": 850
}

logistica = [
    {"id": 1, "empresa": "Frete Campo Sul", "veiculo": "Bitrem Graneleiro", "capacidade": "40 Ton"},
    {"id": 2, "empresa": "AgroTrans", "veiculo": "Rodotrem", "capacidade": "55 Ton"}
]

mercado = {
    "graos": [
        {"produto": "Soja", "preco": 165.40},
        {"produto": "Milho", "preco": 72.30},
        {"produto": "Algodão", "preco": 132.00}
    ],
    "insumos": [
        {"nome": "NPK 20-05-20", "preco": 2900, "tendencia": "Baixa"},
        {"nome": "Ureia", "preco": 2450, "tendencia": "Alta"}
    ]
}

maquinas = [
    {"id": 1, "nome": "John Deere S790", "horimetro": 3520, "status": "Em Campo"},
    {"id": 2, "nome": "Case Axial Flow", "horimetro": 4100, "status": "Manutenção Preventiva"},
    {"id": 3, "nome": "Trator 8R 410", "horimetro": 5800, "status": "Parado por Falha"}
]

ordens_servico = []

# =========================
# ENDPOINTS DA REST API
# =========================

@app.get("/api/clima")
def obter_clima(): 
    return clima

@app.get("/api/colheita")
def obter_colheita(): 
    return colheita

@app.get("/api/silos")
def obter_silos(): 
    return silos

@app.get("/api/logistica")
def obter_logistica(): 
    return logistica

@app.get("/api/mercado")
def obter_mercado(): 
    return mercado

@app.get("/api/maquinas")
def obter_maquinas(): 
    return maquinas

@app.post("/api/maquinas")
def registrar_os(payload: dict):
    ordens_servico.append(payload)
    return {
        "success": True, 
        "mensagem": "Ordem de serviço registrada",
        "total": len(ordens_servico)
    }

@app.post("/api/simulador")
def simulador(payload: dict):
    hectares = float(payload["hectares"])
    custo_ha = float(payload["custo"])
    total = hectares * custo_ha
    return {
        "hectares": hectares,
        "custo_por_ha": custo_ha,
        "total": total
    }
