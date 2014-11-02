import key_funcs
import os
import binascii
from coinbase import CoinbaseAccount
from coinbase.models.amount import CoinbaseAmount

def get_account(oauth_token):
	return CoinbaseAccount(oauth2_credentials=oauth_token)

def multisig_create_and_transfer(account, keys, amount, note=""):
	xpubkeys = map(key_funcs.get_public_key, keys)

	response = account.create_multisig_account('multisig test', 2, xpubkeys)
	account_id = response['account']['id']
	address = account.receive_address(account_id)
	send_respose = account.send(to_address = address, amount = CoinbaseAmount(amount, "USD"), note = note)
	return address

def multisig_send_from(account, keys, account_id, address, amount, note = ""):
	send_response = account.send_from_multisig(to_address = address, amount = CoinbaseAmount(amount, "USD"), note = note)
	print(send_response)
	sighash = send_response['transaction']['inputs']['sighash']
	required_sigs = []
	for addresses in send_response['transaction']['inputs']['address']['addresses']:
		required_sigs.append( { 'address': addresses['address']['address'],
					'sighash': sighash,
					'level': addresses['address']['node_path']
				      } )
	sigs = key_funcs.sign_addresses(keys, required_sigs)
	account.put_signatures(sigs)
