import key_funcs
import os
import binascii
from coinbase import CoinbaseAccount
from coinbase.models.amount import CoinbaseAmount
from secrets import OAUTH_TOKEN
import time

account = CoinbaseAccount(oauth2_credentials=OAUTH_TOKEN)
test_seeds = ['206', '207']

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

	response = account.create_multisig_account('deposit here2', 2, xpubkeys)
	print(response)
	created_at = response['account']['created_at']
	account_id = response['account']['id']
	print(account_id)
	address = account.receive_address(account_id)
	send_respose = account.send(to_address = address, amount = CoinbaseAmount('1.00', "USD"), user_fee = '.0002', notes='test send')
	transaction = account.transactions(count=1)[0]
	print(transaction)

def multisig_send_from(keys, account_id, address):
	send_response = account.send_from_multisig(from_address = account_id, to_address = address, amount = CoinbaseAmount('0.04', "USD"), user_fee = '.0002', notes='test send')
	print(send_response)
	transaction_id = send_response['transaction']['id']
	time.sleep(5) # gotta let the transaction freaking propogate
	multisig_sign_from_transaction(transaction_id, account_id)

def multisig_sign_from_transaction(transaction_id, account_id):
	sighashes = get_sighashes(transaction_id, account_id)
	print(sighashes)
	sighash = sighashes['transaction']['inputs'][0]['input']['sighash']
	required_sigs = []
	for addresses in sighashes['transaction']['inputs'][0]['input']['address']['addresses']:
		required_sigs.append( { 'address': addresses['address']['address'],
					'sighash': sighash,
					'level': int(addresses['address']['node_path'][-1])
				      } )
	sigs = sign_addresses(keys, required_sigs)
	print(account.send_signatures(sigs, transaction_id))

def sign_addresses(keys, required_sigs):
	key_vals = keys.values()
	signatures = []
	for i, required_sig in enumerate(required_sigs):
		sighash = required_sig['sighash']
		level = required_sig['level']
		key = key_vals[i]
		private_key = binascii.b2a_hex(key.child(level).prvkey())
		signatures.append(key_funcs.bitcoin_sign(private_key, sighash))
	return signatures

def get_sighashes(transaction_id, account_id):
	return account.get_sighashes(transaction_id, account_id)

keys = make_keys(2)
#transaction = account.transactions(count=30)[0]
#print(get_sighashes('545644aed602e6abcd00001e', '5456289bd42011781000000a'))
#multisig_send_from(keys, '545648c0fbb87d1c7a000030', 'gordonmslai@gmail.com')
multisig_sign_from_transaction("545684ddfc477ac6f6000006", "38sHDJr5bJ4TTcqE9YmwhNHHmiAMqxZ1vE")
#print(get_sighashes('54563b870b6947bddb000012'))
# required_sigs = [ { 'address': '17rayYCwAPsoxqokhpDeW5whXENWKrtfdk',
# 		    'sighash': '1000',
# 		    'level': 4
# 		  },
# 		  { 'address': '1PYSBUimNnihuWkUibgY1JrZvHwoCbyLcY',
# 		    'sighash': '1000',
# 	  	    'level': 4
# 		  }
# 		]
# sigs = sign_addresses(keys, required_sigs)
# print(keys)
# print(sigs)
#multisig_create_and_send_to()
