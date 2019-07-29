# import urllib, json
import requests

#TODO: colocar todas as funções num arquivo só

# class SiconfiErr(Exception, str):
class SiconfiErr(Exception):
#TODO: acrescentar string inicial indicando que foi erro na api do siconfi
    # def __init__(self):
        # self.message = "Erro na API do Siconfi. " + str
        # super().__init__(self)

    pass

class Siconfi():
    """
    Acesso à API do Siconfi.
    """

    def __init__(self):
        self.__entes = ""

    @property
    def entes(self):
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
        if self.__entes != "":
            return self.__entes

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

        self.__entes = response.json()
        return self.__entes


#TODO: fazer setter para entes que retorne tipo notimplemented


if __name__ == "__main__":
    try:
        print("instancia")
        siconfi = Siconfi()
        print("primeiro")
        siconfi.entes
        print("segundo")
        siconfi.entes
    except SiconfiErr as erro:
        print("erro especifico " + str(erro))
    except Exception as erro:
        print(erro)

