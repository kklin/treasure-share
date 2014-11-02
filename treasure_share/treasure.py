from datetime import date, timedelta
import key_funcs, multisig

class Donation:
    def __init__(self, donor, charities, initial_amount, dribble, oauth_token):
        self._charities = charities
        self.amount = initial_amount # in USD
        self._keys = key_funcs.make_keys(len(charities))
        self._dribble = dribble
        self.creation_time = date.today()

	self._account = multisig.get_account(oauth_token)
	self._donor = self._account.receive_address()
        self.multisig_address = self.create_wallet()
        self.notify_charities()
        print("Donation made")

    # creates a multisig wallet and returns the address of the wallet
    def create_wallet(self):
	return multisig.multisig_create_and_transfer(account = self._account, keys = self._keys, amount = self.amount, note = "Donation :)")

    # distributes the keys
    def notify_charities(self):
        for i, charity in enumerate(self._charities):
            self.notify_charity(charity, self._keys[i])

    def notify_charity(self, charity, key):
        # email(notify_charity_template(charity_name, key))
        print(self.notify_charity_template(charity, key))

    def notify_charity_template(self, charity, key):
        template = '''
                    Hey $charity_name!
                    $donor_name has decided to donate $amount BTC to you, but this money
                    is conditional upon you working with $other_charities.
                    You cannot access this money until you come to some agreement
                    with the them about how you're going to use this money.
                    Furthermore, after $delay, the money will begin returning back
                    to the donor at $dribble, so work fast to maximize the funds!
                    All we're giving you for now is your private key and the address
                    of the bitcoin wallet. The other charities also have their own
                    private keys, but an individual private key is useless without
                    the others.
                    Your private key: $key
                    Wallet id: $wallet

                    Much love,
                    Treasure Share
                   '''
	template_values = {}
        template_values['charity_name'] = charity.name
        template_values['donor_name'] = self._donor
        template_values['amount'] = self.amount
        template_values['other_charities'] = " ".join(self._charities.remove(charity))
        template_values['delay'] = self._dribble.delay
        template_values['dribble'] = self._dribble.percentage*100 + "% / " + self._dribble.frequency
        template_values['key'] = key
        template_values['wallet'] = self.multisig_address
        return string.Template(template).substitute(template_values) % template_values

    def get_dribble(self):
        return self._dribble

    def apply_dribble(self):
	dribble_amount = _dribble.percentage * amount
	multisig.multisig_send_from(account = _account, keys = _keys, account_id = multisig_address, address = donor, amount = dribble_amount, note = "Dribbling back..")
        new_amount = amount * (1 - _dribble.percentage)
        amount = new_amount
        donation.last_dribbled = date.today()
