import streamlit as st
import pandas as pd
import pydeck as pdk
import streamlit.components.v1 as components

import db_sqlite
import db_mongo
import geoprocessamento

st.set_page_config(
    page_title="Explorador de Pontos Turísticos",
    layout="wide"
)

db_sqlite.inicializa_db()

st.sidebar.header("Área de Cadastros")

with st.sidebar.form("form_cidade", clear_on_submit=True):
    st.subheader("Cadastrar Nova Cidade")
    nome_cidade_sqlite = st.text_input("Nome da Cidade")
    estado_sqlite = st.text_input("Estado (UF)", max_chars=2)

    submit_cidade = st.form_submit_button("Cadastrar Cidade")
    if submit_cidade:
        if nome_cidade_sqlite and estado_sqlite:
            if db_sqlite.adicionar_cidade(nome_cidade_sqlite, estado_sqlite.upper()):
                st.sidebar.success(f"Cidade '{nome_cidade_sqlite} - {estado_sqlite.upper()}' cadastrada!")
            else:
                st.sidebar.error("Essa cidade já existe no banco de dados.")
        else:
            st.sidebar.warning("Por favor, preencha todos os campos.")

with st.sidebar.form("form_local", clear_on_submit=True):
    st.subheader("Cadastrar Novo Local de Interesse")
    nome_local_mongo = st.text_input("Nome do Local")
    cidade_local_mongo = st.text_input("Cidade do Local")
    descricao_mongo = st.text_area("Descrição")
    lat_mongo = st.number_input("Latitude", format="%.6f")
    lon_mongo = st.number_input("Longitude", format="%.6f")

    submit_local = st.form_submit_button("Cadastrar Local")
    if submit_local:
        if nome_local_mongo and cidade_local_mongo and lat_mongo and lon_mongo:
            dados_local = {
                "nome_local": nome_local_mongo,
                "cidade": cidade_local_mongo,
                "coordenadas": {"latitude": lat_mongo, "longitude": lon_mongo},
                "descricao": descricao_mongo
            }
            if db_mongo.adicionar_local(dados_local):
                st.sidebar.success(f"Local '{nome_local_mongo}' cadastrado com sucesso!")
            else:
                st.sidebar.error("Erro ao cadastrar local no MongoDB.")
        else:
            st.sidebar.warning("Preencha todos os campos obrigatórios.")

st.title("🗺️ Explorador de Pontos Turísticos")
st.markdown("Projeto avaliativo da disciplina de Tendências em Ciência da Computação com o tema Persistência Poliglota.")
st.markdown("Aluno: **Emerson de Azevedo Silva Bezerra**")
st.markdown("RGM: **44968132**")

st.header("Visualização de Locais por Cidade")

lista_cidades = db_sqlite.listar_cidades()
opcoes_cidades = [f"{nome} - {estado}" for id, nome, estado in lista_cidades]

if not opcoes_cidades:
    st.info("Nenhuma cidade cadastrada. Adicione uma cidade na barra lateral para começar.")
else:
    cidade_selecionada_str = st.selectbox("Selecione uma cidade:", opcoes_cidades)
    nome_cidade_selecionada = cidade_selecionada_str.split(" - ")[0]

    locais_na_cidade = db_mongo.listar_locais_por_cidade(nome_cidade_selecionada)

    if locais_na_cidade:
        df_locais = pd.DataFrame(locais_na_cidade)

        if '_id' in df_locais.columns:
            df_locais = df_locais.drop(columns=['_id'])

        df_locais['latitude'] = df_locais['coordenadas'].apply(lambda c: c['latitude'])
        df_locais['longitude'] = df_locais['coordenadas'].apply(lambda c: c['longitude'])

        st.write(f"Exibindo {len(df_locais)} local(is) em **{nome_cidade_selecionada}**.")
        st.dataframe(df_locais[['nome_local', 'descricao']])

        if not df_locais.empty:
            midpoint = (
                df_locais['latitude'].mean(),
                df_locais['longitude'].mean()
            )
            scatter_layer = pdk.Layer(
                "ScatterplotLayer",
                data=df_locais,
                get_position='[longitude, latitude]',
                get_color='[200, 30, 0, 160]',
                get_radius=100,
                pickable=True,
            )
            view_state = pdk.ViewState(
                latitude=midpoint[0],
                longitude=midpoint[1],
                zoom=10,
                pitch=0,
            )
            st.pydeck_chart(pdk.Deck(
                layers=[scatter_layer],
                initial_view_state=view_state,
                tooltip={"text": "{nome_local}\n{descricao}"}
            ))
    else:
        st.info(f"Nenhum local de interesse cadastrado para a cidade de {nome_cidade_selecionada}.")

query_params = st.query_params
default_lat = float(query_params.get("lat", [-7.1195])[0])
default_lon = float(query_params.get("lon", [-34.8454])[0])

components.html(
    """
    <script>
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(pos) {
            const lat = pos.coords.latitude;
            const lon = pos.coords.longitude;
            const params = new URLSearchParams(window.location.search);
            if (!params.has("lat") || !params.has("lon")) {
                params.set("lat", lat);
                params.set("lon", lon);
                window.location.search = params.toString();
            }
        });
    }
    </script>
    """,
    height=0,
)

st.header("Busca de Locais por Proximidade")

col1, col2, col3 = st.columns(3)
with col1:
    lat_central = st.number_input("Sua Latitude", format="%.6f", value=default_lat)
with col2:
    lon_central = st.number_input("Sua Longitude", format="%.6f", value=default_lon)
with col3:
    raio_km = st.slider("Raio em KM", min_value=1, max_value=100, value=10)

ponto_central = (lat_central, lon_central)
todos_os_locais = db_mongo.listar_todos_os_locais()

if st.button(f"Buscar locais em um raio de {raio_km} km"):
    if not todos_os_locais:
        st.warning("Não há locais cadastrados no para realizar a busca.")
    else:
        locais_proximos = geoprocessamento.listar_locais_proximos(ponto_central, todos_os_locais, raio_km)

        if locais_proximos:
            df_proximos = pd.DataFrame(locais_proximos)
            df_proximos['latitude'] = df_proximos['coordenadas'].apply(lambda c: c['latitude'])
            df_proximos['longitude'] = df_proximos['coordenadas'].apply(lambda c: c['longitude'])

            st.write(f"Encontrados {len(df_proximos)} locais:")
            st.dataframe(df_proximos[['nome_local', 'cidade', 'distancia_km']])
            st.map(df_proximos, latitude='latitude', longitude='longitude')
        else:
            st.info("Nenhum local encontrado no raio especificado.")
