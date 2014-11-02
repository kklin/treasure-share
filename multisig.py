import key_funcs
import os
import binascii
from coinbase import CoinbaseAccount
from coinbase.models.amount import CoinbaseAmount
from secrets import OAUTH_TOKEN

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

def multisig_create_and_transfer(account, keys, amount):
	xpubkeys = map(key_funcs.get_public_key, keys)

	response = account.create_multisig_account('multisig test', 2, xpubkeys)
	account_id = response['account']['id']
	address = account.receive_address(account_id)
	send_respose = account.send(to_address = address, amount = CoinbaseAmount(amount, "USD"))
	return address

def multisig_send_from(keys, account_id, address, amount):
	send_response = account.send_from_multisig(from_address = account_id, to_address = address, amount = CoinbaseAmount(amount, "USD"))
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
