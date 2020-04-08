import simplecrypt
crypt_file = open(r"D:\Python\encrypted.bin", "rb")
password_file = open(r"D:\Python\passwords.txt")
crypt_text = crypt_file.read().strip()
print("crypt_text: ", crypt_text)
for i in range(10):
    print(i)
    password = password_file.readline().strip()
    print("password ", password)
    try:
        enctxt = simplecrypt.decrypt(password, crypt_text).decode('utf8')
        print("answer:", enctxt)
    except simplecrypt.DecryptionException:
        print("exception")
        continue
crypt_file.close()
password_file.close()