from scrapy.contracts import Contract
from scrapy.exceptions import ContractFail

class PastPlayersMinCountContract(Contract):
    """Contract used to check if output list has at least number(arg[0]) of past players"""

    name = 'past_players_min_count'

    def post_process(self, output):
        min_count = int(self.args[0])
        past_players_count = len(output[0]['past_players'])
        if min_count > past_players_count:
            raise ContractFail('Output has too few arguments')
