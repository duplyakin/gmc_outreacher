import base64
#from Crypto.Cipher import AES
#import o24.config as config


#def encode_password(password_string):
#    b_pass = password_string.encode('utf-8').rjust(32)
#    cipher = AES.new(config.AES_SECRET,AES.MODE_ECB)

#    encrypted = base64.b64encode(cipher.encrypt(b_pass))
#    if not encrypted:
#        raise Exception("Can't encrypt password")
    
#    return encrypted

#def decode_password(encoded_password):
#    cipher = AES.new(config.AES_SECRET,AES.MODE_ECB)
    
#    decrypted = cipher.decrypt(base64.b64decode(encoded_password))
#    if not decrypted:
#        raise Exception("Can't decrypt password or password is empty")
    
#    return decrypted