from geopy.distance import geodesic


def calcular_distancia(coord_1, coord_2):
    """
    Calcula a distância geodésica entre dois pontos (latitude, longitude).

    Args:
        coord_1 (tuple): Tupla contendo (latitude, longitude) do primeiro ponto.
        coord_2 (tuple): Tupla contendo (latitude, longitude) do segundo ponto.

    Returns:
        float: A distância entre os dois pontos em quilômetros.
    """
    # A função geodesic da biblioteca geopy calcula a distância precisa
    # levando em conta o formato da Terra.
    distancia = geodesic(coord_1, coord_2).kilometers
    return distancia


def listar_locais_proximos(ponto_central, lista_de_locais, raio_km):
    """
    Filtra uma lista de locais, retornando apenas aqueles dentro de um raio
    a partir de um ponto central.

    Args:
        ponto_central (tuple): Tupla com (latitude, longitude) do ponto de referência.
        lista_de_locais (list): Lista de dicionários, onde cada dicionário é um local
                                 com uma chave 'coordenadas'.
        raio_km (float): A distância máxima (em km) para incluir um local.

    Returns:
        list: Uma nova lista contendo apenas os locais próximos.
    """
    locais_filtrados = []

    for local in lista_de_locais:
        # Pega as coordenadas do dicionário do local, que vem do MongoDB
        coords_local = (
            local['coordenadas']['latitude'],
            local['coordenadas']['longitude']
        )

        # Calcula a distância entre o ponto central e o local atual
        distancia = calcular_distancia(ponto_central, coords_local)

        # Se a distância for menor ou igual ao raio, adiciona o local à lista
        if distancia <= raio_km:
            # Adicionamos a distância calculada ao dicionário para exibi-la na interface
            local['distancia_km'] = round(distancia, 2)
            locais_filtrados.append(local)

    return locais_filtrados