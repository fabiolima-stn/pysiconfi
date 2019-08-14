import requests, json


"""
Classes de erros da biblioteca.
"""
class ErroSiconfi(Exception):
    pass

class ErroEndpointNaoEncontrado(ErroSiconfi):
    pass

class ErroServicoIndisponivel(ErroSiconfi):
    pass

class ErroEndpoint(ErroSiconfi):
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
    def __executa_request(cls, endpoint):
        """
        Executa uma requisição à API.

        Parâmetro:
            endpoint: endpoint da API a ser requisitado.

        Retorna uma lista de dicionários com a resposta da requisição ou uma 
        execeção em caso de erro.
        """

	#TODO: tratar possível paginação, de preferência num método à parte que possa ser reaproveitado

        try:
            response = requests.get(endpoint)
        except Exception as erro:
            raise ErroEndpoint(endpoint)

        if response.status_code != 200:
            if response.status_code == 404:
                raise ErroEndpointNaoEncontrado(endpoint)
            elif response.status_code == 503:
                raise ErroServicoIndisponivel
            else:
                raise ErroEndpoint(endpoint, response.status_code)

        json_data = json.loads(response.text)
        return json_data["items"]

    @classmethod
    def _obtem_entes(cls):
        """
        Busca todos os entes cadastrados no SICONFI.

        Retorna uma lista com o seguinte dicionário:
            'cod_ibge': código IBGE do ente
            'ente': nome do ente
            'capital': flag indicativa se o ente é uma capital de Estado ou não 
                (0 = não, 1 = sim)
            'regiao': sigla da região política do ente
            	('BR' no caso da União)
            'uf': sigla da UF "pai" do ente
            	('BR' no caso de um Estado e None no caso da União) 
            'esfera': esfera do ente
            	('U' = União, 'E' = Estado, 'M' = Município).

        Dispara uma execeção em casso de erro.
        """

        # só executa o endpoint uma vez
        if len(cls.__entes) != 0:
            return cls.__entes

        endpoint = "http://apidatalake.tesouro.gov.br/ords/siconfi/tt/entes"

        cls.__entes = cls.__executa_request(endpoint)
        return cls.__entes


    # @staticmethod
    @classmethod
    def rel_completo(cls):
        pass


# cria uma instância e exporta seus métodos para serem chamados pelo programa
# que importar este módulo de maneira transparente, como se fossem funções 
# independentes de uma classe
_inst = Siconfi()
# ex.: 
# func = _inst.func
obtem_entes = _inst._obtem_entes


if __name__ == "__main__":
    #TODO: complementar
    pass

