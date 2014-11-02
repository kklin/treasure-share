import key_funcs
import os
import binascii
from coinbase import CoinbaseAccount
from coinbase.models.amount import CoinbaseAmount
from secrets import OAUTH_TOKEN

account = CoinbaseAccount(oauth2_credentials=OAUTH_TOKEN)
test_seeds = ['10', '20']

def make_keys(n):
	keys = {}
	for _ in range(n):
		#seed = os.urandom(256/8)
		seed = test_seeds[_]
		key = key_funcs.make_key(seed)
		key_address = key.address()
		keys[key_address] = key
	return keys

def multisig_create_and_send_to():
	key_mappings = make_keys(2)
	keys = key_mappings.values()

	xpubkeys = map(key_funcs.get_public_key, keys)

	print("Public keys:")
	print("\n".join(xpubkeys))
	response = account.create_multisig_account('multisig test', 2, xpubkeys)
	created_at = response['account']['created_at']
	account_id = response['account']['id']
	print(account_id)
	address = account.receive_address(account_id)
	send_respose = account.send(to_address = address, amount = CoinbaseAmount('0.4', "USD"), notes='test send')

def multisig_send_from(keys, account_id, address):
	send_response = account.send_from_multisig(from_address = account_id, to_address = address, amount = CoinbaseAmount('0.4', "USD"), notes='test send')
	print(send_response)
	sighash = send_response['transaction']['inputs']['sighash']
	required_sigs = []
	for addresses in send_response['transaction']['inputs']['address']['addresses']:
		required_sigs.append( { 'address': addresses['address']['address'],
					'sighash': sighash,
					'level': addresses['address']['node_path']
				      } )
	sigs = sign_addresses(keys, required_sigs)
	account.put_signatures(sigs)

def sign_addresses(keys, required_sigs):
	signatures = []
	for required_sig in required_sigs:
		address = required_sig['address']
		sighash = required_sig['sighash']
		level = required_sig['level']
		key = keys[address]		
		private_key = binascii.b2a_hex(key.child(level).prvkey())
		signatures.append(key_funcs.bitcoin_sign(private_key, sighash))
	return signatures

#multisig_send_from('5455ffa3d420119475000010', 'kevinlin@berkeley.edu')
keys = make_keys(2)
required_sigs = [ { 'address': '17rayYCwAPsoxqokhpDeW5whXENWKrtfdk',
		    'sighash': '1000',
		    'level': 4
		  },
		  { 'address': '1PYSBUimNnihuWkUibgY1JrZvHwoCbyLcY',
		    'sighash': '1000',
	  	    'level': 4
		  }
		]
sigs = sign_addresses(keys, required_sigs)
print(keys)
print(sigs)
#multisig_create_and_send_to()
