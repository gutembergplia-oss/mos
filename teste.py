import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.title("📋 Dashboard de Estudantes - MSI")
st.caption("Filtros por MOS | Unidade | MSI")

# =========================
# LEITURA DO EXCEL
# =========================
df = pd.read_excel(
    r"C:\Users\ss1057289\OneDrive - SESISENAISP - Corporativo\Arquivos uteis\Sistema_Robótica\ESTUDANTES_.xlsx"
)

df.columns = df.columns.str.strip()

# =========================
# COLUNAS OFICIAIS
# =========================
col_origem = "MOS"
col_msi = "MSI"
col_unidade = "Unidade"

# =========================
# VALIDAÇÃO
# =========================
colunas_necessarias = [col_origem, col_msi, col_unidade]
faltando = [c for c in colunas_necessarias if c not in df.columns]

if faltando:
    st.error(f"❌ Colunas não encontradas: {faltando}")
    st.write("Colunas disponíveis no arquivo:")
    st.write(df.columns.tolist())
    st.stop()

# =========================
# TRATAMENTO DO MSI
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


# MÉTRICAS 
col1, col2, col3 = st.columns(3)

col1.metric("👩‍🎓 Total de Estudantes", len(df_filtro))
#col2.metric("🏫 Total de Unidades", df_filtro[col_unidade].nunique())
col3.metric("📈 MSI Médio", round(df_filtro[col_msi].mean(), 2))


# TABELA FINAL (SEM NOME DO ESTUDANTE)

st.subheader("📋 Resultado")

st.dataframe(
    df_filtro[[col_unidade, col_msi]]
    .sort_values(col_msi, ascending=False)
    .rename(columns={
        col_unidade: "Unidade",
        col_msi: "MSI"
    }),
    use_container_width=True
)
