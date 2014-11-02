
_keys = {}
_creation_time = 0

def __init__(self, donor, charities, initial_amount, dribble):
    self._donor = donor
    self._charities = charities
    self._amount = initial_amount
    self._keys = gen_keys([donor] + charities)
    self._dribble = dribble

def create_wallet(self):
    pass

def gen_keys(self, users):
    for user in users:
        key_pair = RSA.generate(2048)
        self._keys[user] = key_pair

# distributes the keys
def notify_charities(self):
    for charity in _charities:
        notify_charity(charity, _keys[charity])

def notify_charity(self, charity_name, key):
    # email(notify_charity_template(charity_name, key))
    print(notify_charity_template(charity_name, key))

def notify_charity_template(charity_name, key):
    template = '''
                Hey $charity!
                $donor has decided to donate $amount BTC to you, but this money
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
    template_values[charity] = charity_name
    template_values[donor] = _donor
    template_values[amount] = _amount
    template_values[other_charities] = " ".join(_charities.remove(charity_name))
    template_values[delay] = _dribble.delay
    template_values[dribble] = _dribble.percentage*100 + "% / " + _dribble.frequency
    template_values[key] = key
    template_values[wallet] = _wallet_id
    return string.Template(template).substitute(template_values) % template_values

def set_dribble(self, dribble):
    self.dribble = _dribble

def get_dribble(self):
    return self._dribble

def apply_dribble(self):
    pass
