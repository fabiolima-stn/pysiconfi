import requests, json


"""
Classes de erros da biblioteca.
"""
class ErroSiconfi(Exception):
    pass

class ErroSiconfiEndpointNaoEncontrado(ErroSiconfi):
    pass

class ErroSiconfiAcessoEndpoint(ErroSiconfi):
    """Erro genérico no acesso ao endpoint."""

    def __init__(self, endpoint, resposta_http = None):
        self.endpoint = endpoint
        self.resposta_http = resposta_http


class Siconfi():
    """
    Encapsulamento da API do Siconfi.
    """

    # lista com todos os entes do Siconfi
    __entes = []


    @classmethod
    def _obtem_entes(cls):
        """
        Retorna todos os entes cadastrados no SICONFI.

        Retorna um JSON com o código IBGE do ente, seu nome, flag indicativa se é 
        uma capital de Estado ou não (0 = não, 1 = sim), sigla da região ("BR" no 
        caso da União), sigla da UF "pai" ("BR" no caso de um Estado e null no caso
        da União) e esfera ("U" = União, "E" = Estado", "M" = Município).

        Em caso de erro na requisição, dispara uma exceção.
        """

        # só executa o endpoint uma vez
        if len(cls.__entes) != 0:
            return cls.__entes

        endpoint = "http://apidatalake.tesouro.gov.br/ords/siconfi/tt/entes"
        try:
            response = requests.get(endpoint)
        except Exception as erro:
            raise ErroSiconfiAcessoEndpoint(endpoint)

        if response.status_code != 200:
            if response.status_code == 404:
                raise ErroSiconfiEndpointNaoEncontrado(endpoint)

            else:
                raise ErroSiconfiAcessoEndpoint(endpoint, response.status_code)

        json_data = json.loads(response.text)
        cls.__entes = json_data["items"]

        return cls.__entes


    # @staticmethod
    @classmethod
    def rel_completo(cls):
        pass


if __name__ == "__main__":
    try:
        Siconfi._obtem_entes()
    except ErroSiconfi as erro:
        print(str(erro))
    except Exception as erro:
        print(erro)

