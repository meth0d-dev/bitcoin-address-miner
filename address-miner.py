from bitcoin import *
import requests, winsound

print('     _       _     _                     __  __ _                 ')
print('    / \   __| | __| |_ __ ___  ___ ___  |  \/  (_)_ __   ___ _ __ ')
print('   / _ \ / _` |/ _` | \'__/ _ \/ __/ __| | |\/| | | \'_ \ / _ \ \'__|')
print('  / ___ \ (_| | (_| | | |  __/\__ \__ \ | |  | | | | | |  __/ |   ')
print(' /_/   \_\__,_|\__,_|_|  \___||___/___/ |_|  |_|_|_| |_|\___|_|   ')
print('                                                      Developed by meth0d.dev ')
print('------------------------------------------------------------------------------')
print('')

## CREATE A NEW FILE WITH THE 
def createFile(filename, content):
    f = open(filename + '.txt', 'w+')
    for line in content:
        f.write(line)
        f.write('\n')
    f.close

def backupBalanceVerifier(address):
    urls = ['https://insight.bitpay.com/api/addr/{address}/?noTxList=1', 'https://api.blockcypher.com/v1/btc/main/addrs/{address}/balance']

    url = random.choice(urls)

    r = requests.get(url.replace('{address}', address))
 
    if r.status_code == 200:
        data = r.json()
    else:
        print('Error while try to check balance via API. Error code: ' + str(r.status_code))
        data = {'balance': 0}

    return data

## VERIFY IF THERE'S ANY FUNDS
def verifyBalance(address): 
    r = requests.get('https://www.bitgo.com/api/v1/address/' + address)

    if r.status_code == 200:
        data = r.json()
    else:
        data = backupBalanceVerifier(address)

    if 'balance' in data:
        return data['balance']
    else:
        print('Error logged, skipping address')
        return 0


if __name__ == '__main__':
    i = 1
    #while (i < 2):
    while True:
        time2wait = 0.4 # TIME TO WAIT BETWEEN REQUESTS - 0.05 TO 1
        
        privkey = random_key()
        wif = encode_privkey(privkey, 'wif')
        pubkey = privtopub(privkey)
        addr = pubtoaddr(pubkey)

        privkey_comp = privkey + '01'
        wif_comp = encode_privkey(decode_privkey(privkey_comp, 'hex'), 'wif')
        pubkey_comp = privtopub(privkey_comp)
        addr_comp = pubtoaddr(pubkey_comp)
        
        balancee = verifyBalance(addr)
        time.sleep(time2wait)
        balancee_comp = verifyBalance(addr_comp)

        content = ['Address: ' + addr, 'Balance: ' + str(balancee), 'WIF: ' + wif, 'PubKey: ' + pubkey, 'PrivKey: ' + privkey]
        content_comp = ['Address: ' + addr_comp, 'Balance: ' + str(balancee_comp), 'WIF: ' + wif_comp, 'PubKey: ' + pubkey_comp, 'PrivKey: ' + privkey_comp]

        frequency = 1500  # Set Frequency To 2500 Hertz
        duration = 250  # Set Duration To 1000 ms == 1 second
        
        if balancee > 0:
            createFile(addr + '-' + str(balancee), content)
            print('Wallet with funds found.')
            winsound.Beep(frequency, duration)
        elif balancee_comp > 0:
            createFile(addr_comp + '-' + str(balancee_comp), content_comp)
            print('Wallet with funds found.')
            winsound.Beep(frequency, duration)
        else:
            print('No wallet with funds found... Attempt: ' + str(i))

        time.sleep(time2wait)

        i += 1

input('')
