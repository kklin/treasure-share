import key_funcs
import os
import binascii
from coinbase import CoinbaseAccount
from coinbase.models.amount import CoinbaseAmount
import time

def get_account(oauth_token):
	return CoinbaseAccount(oauth2_credentials=oauth_token)

def multisig_create_and_transfer(account, keys, amount, note=""):
	xpubkeys = map(key_funcs.get_public_key, keys)

	response = account.create_multisig_account('Donation', 2, xpubkeys)
	account_id = response['account']['id']
	address = account.receive_address(account_id)
	send_response = account.send(to_address = address, amount = CoinbaseAmount(amount, "USD"), user_fee = '.0002', notes = note)
	return address

def multisig_send_from(account, keys, account_id, address, amount, note = ""):
	send_response = account.send_from_multisig(to_address = address, amount = CoinbaseAmount(amount, "USD"), user_fee = '.0002', notes = note, from_address = account_id)
	transaction_id = send_response['transaction']['id']
	time.sleep(5) # gotta let the transaction freaking propogate
	print('account_id: ' + account_id)
	print('transaction_id: ' + transaction_id)
	multisig_sign_from_transaction(account, keys, transaction_id, account_id)

def multisig_sign_from_transaction(account, keys, transaction_id, account_id):
	sighashes = get_sighashes(account, transaction_id, account_id)
	print(sighashes)
	sighash = sighashes['transaction']['inputs'][0]['input']['sighash']
	required_sigs = []
	for addresses in sighashes['transaction']['inputs'][0]['input']['address']['addresses']:
		required_sigs.append( { 'address': addresses['address']['address'],
					'sighash': sighash,
					'level': int(addresses['address']['node_path'][-1])
				      } )
	sigs = sign_addresses(keys, required_sigs)
	account.send_signatures(sigs, transaction_id)

def sign_addresses(keys, required_sigs):
	signatures = []
	for i, required_sig in enumerate(required_sigs):
		sighash = required_sig['sighash']
		level = required_sig['level']
		key = key_vals[i]
		private_key = binascii.b2a_hex(key.child(level).prvkey())
		signatures.append(key_funcs.bitcoin_sign(private_key, sighash))
	return signatures

def get_sighashes(account, transaction_id, account_id):
	return account.get_sighashes(transaction_id, account_id)
