from pgpdump import AsciiData
from base64 import b64encode, encodebytes, standard_b64encode
import binascii

from pgp.pgpFileHelper import writePrivateKeyASC
from pgp.pgpManipulateKeyfile_helper import printDSAKeyPaket

keyfile = open('bob-dsa-private-keyasc.sec','rb')
keyasc_data = keyfile.read()
keydata = AsciiData(keyasc_data)
keypackets = list(keydata.packets())

keydatabytes = keypackets[0].data
privatekeypaket = ''

j = len(keydatabytes)

# From keydatabytes to privatekeypacket which is string
# Privatekeypaket is String and used for replacing the private key
while j > 0:
    privatekeypaket += ''.join('{:02x}'.format(keydatabytes[len(keydatabytes) - j]))
    j -= 1


#print('keydatabytes: ' + privatekeypaket)

# Analyzes the DSA key paket and prints all relevant data
# If Checksum doesn't fit the conditions there will be a new one calculated and returned
printDSAKeyPaket(keydatabytes)

print('OLD_keydatabytes: ' + privatekeypaket)

# length of 18b0b0dead is 160(dec) and a0(hex)
# changes the private key
privatekeypaket = privatekeypaket.replace('a08d5d6a83d840ed591623768bb89e60602529651a',
                                          'a000000000000000000000000000000000b0b0dead')

keydatabytes = bytearray()

# put the new privatekeypacket with changed private key into the keydatabytes
# could have been done direktly on the bytes
# more or less parsing string to bytes
count = 0
while count < len(privatekeypaket):
    summ = 0
    val = privatekeypaket[count] + privatekeypaket[count + 1]
    count += 2
    summ = summ + int(val, 16)
    keydatabytes.append(summ)

print('NEW_keydatabytes: ' + privatekeypaket)

newCheckSum = printDSAKeyPaket(keydatabytes)

keydatabytes[len(keydatabytes)-1] = newCheckSum.to_bytes(2, byteorder='big')[1]
keydatabytes[len(keydatabytes)-2] = newCheckSum.to_bytes(2, byteorder='big')[0]

printDSAKeyPaket(keydatabytes)


print('---')
print(binascii.hexlify(keydatabytes))
print('---')
print(binascii.hexlify(keypackets[0].data))
print('---')
print(binascii.hexlify(keydata.data))
keydata.data = keydata.data.replace(keypackets[0].data, keydatabytes)
print('---')
print(binascii.hexlify(keydata.data))

print(b64encode(keydata.data))
print(standard_b64encode(keydata.data))
print(encodebytes(keydata.data))

# writes manipulated pakets to file
writePrivateKeyASC("bob-dsa-private-keyasc-AUTOgenerated.sec",
                   keydata.data)

print("done")
