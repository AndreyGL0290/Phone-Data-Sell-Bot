from crypto.ethereum import Ethereum
from crypto.payment_link import PaymentLink

class User():
    def __init__(self, tg_id) -> None:
        self.id = tg_id
        self.crypto_currencies = {'Ethereum': self.ethereum}

    def addresses_output(self) -> str:
        output = ''
        for name, object in self.crypto_currencies.items():
            output += f"{name} - {object.address}\n"
        output.strip('\n')

        return output
    
    @property
    def ethereum(self) -> Ethereum:
        return Ethereum(self.id)
    
    @property
    def payment_link(self):
        return PaymentLink(self.id)
