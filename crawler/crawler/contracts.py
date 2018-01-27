from scrapy.contracts import Contract
from scrapy.exceptions import ContractFail

class FieldMinCountContract(Contract):
    """Contract used to check if output list has elements of key greater than minimum
    arg[0] - key
    arg[1] - count
    """

    name = 'field_min_count'

    def post_process(self, output):
        key = self.args[0]
        min_count = int(self.args[1])
        past_players_count = len(output[0][key])
        if min_count > past_players_count:
            raise ContractFail('Output has too few arguments')
