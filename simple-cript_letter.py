import simplecrypt
crypt_file = open(r"D:\Python\encrypted.bin", "rb")
password_file = open(r"D:\Python\passwords.crypt_text")
crypt_text = crypt_file.read()
print("crypt_text: ", crypt_text)
for i in range(10):
    print(i)
    passw = password_file.readline()
    print("passw ", passw)
    try:
        enctxt = simplecrypt.decrypt(passw, crypt_text).decode('utf8')
        print("ancwer:", enctxt)
    except simplecrypt.DecryptionException:
        print("exception")
        continue