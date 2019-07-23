# import urllib, json
import requests

#TODO: criar exceção específica para siconfi
#TODO: colocar todas as funções num arquivo só

def obtem_entes():
    """
    Retorna todos os entes cadastrados no SICONFI.

    Retorna um JSON com o código IBGE do ente, seu nome, flag indicativa se é 
    uma capital de Estado ou não (0 = não, 1 = sim), sigla da região ("BR" no 
    caso da União), sigla da UF "pai" ("BR" no caso de um Estado e null no caso
    da União) e esfera ("U" = União, "E" = Estado", "M" = Município).

    Em caso de erro, dispara uma exceção.
    """

    # url = "http://apidatalake.tesouro.gov.br/ords/siconfi/tt/entes"
    # response = urllib.urlopen(url)
    # return json.loads(response.read())

    try:
        response = requests.get("http://apidatalake.tesouro.gov.br/ords/siconfi/tt/entes")
    except:
        raise

    if response.status_code != 200:
        raise Exception("Erro ao acessar a API do Siconfi. Código do erro: "
            + str(response.status_code))
    else:
        print("\nLog: "); print(response)
        # return response.json()


if __name__ == "__main__":
    try:
        entes = obtem_entes()
        # print(entes)
    except Exception as erro:
        print(erro)

