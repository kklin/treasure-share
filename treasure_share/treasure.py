from datetime import date, timedelta
import key_funcs, multisig

class Donation:
    def __init__(self, donor, charities, initial_amount, dribble):
        self._donor = donor # the donor's bitcoin address
        self._charities = charities
        self.amount = initial_amount # in USD
        self._keys = key_funcs.make_keys(len(charities))
        self._dribble = dribble
        self.creation_time = date.today()


        self.multisig_address = create_wallet()
        notify_charities()
        print("Donation made")

    # creates a multisig wallet and returns the address of the wallet
    def create_wallet(self):
	return multisig.create_and_transfer(account = _account, keys = _keys, amount = amount, note = "Donation :)")

    # distributes the keys
    def notify_charities(self):
        for i, charity in enumerate(_charities):
            notify_charity(charity, _keys[i])

    def notify_charity(self, charity, key):
        # email(notify_charity_template(charity_name, key))
        print(notify_charity_template(charity, key))

    def notify_charity_template(charity, key):
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
        template_values[charity_name] = charity.name
        template_values[donor_name] = _donor.name
        template_values[amount] = amount
        template_values[other_charities] = " ".join(_charities.remove(charity_name))
        template_values[delay] = _dribble.delay
        template_values[dribble] = _dribble.percentage*100 + "% / " + _dribble.frequency
        template_values[key] = key
        template_values[wallet] = _wallet_id
        return string.Template(template).substitute(template_values) % template_values

    def get_dribble(self):
        return self._dribble

    def apply_dribble(self):
	dribble_amount = _dribble.percentage * amount
	multisig.multisig_send_from(keys = _keys, account_id = donor, address = multisig_address, amount = dribble_amount, note = "Dribbling back..", account = _account)
        new_amount = amount * (1 - _dribble.percentage)
        amount = new_amount
        donation.last_dribbled = date.today()
