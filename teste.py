import streamlit as st
import pandas as pd

# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================
st.set_page_config(layout="wide")

st.title("📋 Dashboard de Estudantes - MSI")
st.caption("Filtros por MOS | Unidade | MSI")

# =========================
# LEITURA DO EXCEL
# =========================
df = pd.read_excel("ESTUDANTES_.xlsx")

# Remove espaços extras dos nomes das colunas
df.columns = df.columns.str.strip()

# =========================
# COLUNAS OFICIAIS
# =========================
col_origem = "MOS"
col_msi = "MSI"
col_unidade = "Unidade"
col_gmetrix = "GMetrix"

# =========================
# VALIDAÇÃO DE COLUNAS
# =========================
colunas_necessarias = [col_origem, col_msi, col_unidade, col_gmetrix]
faltando = [c for c in colunas_necessarias if c not in df.columns]

if faltando:
    st.error(f"❌ Colunas não encontradas: {faltando}")
    st.write("Colunas disponíveis no arquivo:")
    st.write(df.columns.tolist())
    st.stop()

# =========================
# TRATAMENTO DO MSI (NUMÉRICO)
# =========================
df[col_msi] = (
    df[col_msi]
    .astype(str)
    .str.replace("%", "", regex=False)
    .str.replace(",", ".", regex=False)
    .replace("-", None)
)

df[col_msi] = pd.to_numeric(df[col_msi], errors="coerce")

# =========================
# TRATAMENTO DO GMETRIX (TEXTO)
# =========================
df[col_gmetrix] = (
    df[col_gmetrix]
    .fillna("-")
    .astype(str)
    .str.strip()
)

df[col_gmetrix] = df[col_gmetrix].replace("", "-")

# =========================
# SIDEBAR – FILTROS
# =========================
st.sidebar.header("🎛️ Filtros")

# ---------- MOS ----------
lista_mos = ["Todos"] + sorted(df[col_origem].dropna().unique())

mos_sel = st.sidebar.selectbox(
    "MOS",
    lista_mos,
    index=0
)

if mos_sel == "Todos":
    df_mos = df.copy()
else:
    df_mos = df[df[col_origem] == mos_sel]

# ---------- UNIDADE ----------
lista_unidades = ["Todas"] + sorted(df_mos[col_unidade].dropna().unique())

unidade_sel = st.sidebar.selectbox(
    "Unidade",
    lista_unidades,
    index=0
)

if unidade_sel == "Todas":
    df_filtro = df_mos.copy()
else:
    df_filtro = df_mos[df_mos[col_unidade] == unidade_sel]

# =========================
# MÉTRICAS
# =========================
# Contagem de Liberados (ignora maiúsculo/minúsculo)
total_liberados = df_filtro[
    df_filtro[col_gmetrix].str.lower() == "liberado"
].shape[0]

col1, col2, col3 = st.columns(3)

col1.metric("👩‍🎓 Total de Estudantes", len(df_filtro))
col2.metric("✅ GMetrix Liberado", total_liberados)
col3.metric("📈 MSI Médio", round(df_filtro[col_msi].mean(), 2))

# =========================
# TABELA FINAL (SEM NOME DO ESTUDANTE)
# =========================
st.subheader("📋 Resultado")

st.dataframe(
    df_filtro[[col_unidade, col_msi, col_gmetrix]]
    .sort_values(col_msi, ascending=False)
    .rename(columns={
        col_unidade: "Unidade",
        col_msi: "MSI",
        col_gmetrix: "GMetrix"
    }),
    use_container_width=True
)
