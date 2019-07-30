import requests, json

# class SiconfiErr(Exception, str):
class SiconfiErr(Exception):
#TODO: acrescentar string inicial indicando que foi erro na api do siconfi
    # def __init__(self):
        # self.message = "Erro na API do Siconfi. " + str
        # super().__init__(self)

    pass

class Siconfi():
    """
    API do Siconfi.
    """

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
            raise SiconfiErr("Falha ao tentar acessar a API do Siconfi. " +  
                "Mensagem original: " + str(erro))

        if response.status_code != 200:
            if response.status_code == 404:
                raise SiconfiErr("Endpoint " + endpoint + " não encontrado.")
            else:
                raise SiconfiErr("Erro ao acessar o endpoint " + endpoint + 
                    ". Status code HTTP: " + str(response.status_code))

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
    except SiconfiErr as erro:
        print("erro especifico " + str(erro))
    except Exception as erro:
        print(erro)

