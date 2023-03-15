import binascii


def xor_func(input1AsString, input2AsString, in_code=16):
    input1AsInteger = int(input1AsString, in_code)
    input2AsInteger = int(input2AsString, in_code)
    result = input1AsInteger ^ input2AsInteger
    resultAsHex = hex(result)
    resultAsHex = resultAsHex.upper()
    resultAsHex = resultAsHex[2:]
    if len(resultAsHex) != len(input1AsString):
        for i in range(len(input1AsString) - len(resultAsHex)):
            resultAsHex = '0' + resultAsHex
    return resultAsHex


def convert_base(num, to_base=10, from_base=10):
    if isinstance(num, str):
        n = int(num, from_base)
    else:
        n = int(num)
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if n < to_base:
        return alphabet[n]
    else:
        return convert_base(n // to_base, to_base) + alphabet[n % to_base]


galua_coef = [148, 32, 133, 16, 194, 192, 1, 251, 1, 192, 194, 16, 133, 32, 148, 1]
galua_coef_reverse = [1, 148, 32, 133, 16, 194, 192, 1, 251, 1, 192, 194, 16, 133, 32, 148]
galua_fields = [1, 2, 4, 8, 16, 32, 64, 128, 195, 69, 138, 215, 109, 218, 119, 238, 31, 62, 124, 248, 51, 102, 204, 91,
                182, 175, 157, 249, 49, 98, 196, 75, 150, 239, 29, 58, 116, 232, 19, 38, 76, 152, 243, 37, 74, 148, 235,
                21, 42, 84, 168, 147, 229, 9, 18, 36, 72, 144, 227, 5, 10, 20, 40, 80, 160, 131, 197, 73, 146, 231, 13,
                26, 52, 104, 208, 99, 198, 79, 158, 255, 61, 122, 244, 43, 86, 172, 155, 245, 41, 82, 164, 139, 213,
                105, 210, 103, 206, 95, 190, 191, 189, 185, 177, 161, 129, 193, 65, 130, 199, 77, 154, 247, 45, 90, 180,
                171, 149, 233, 17, 34, 68, 136, 211, 101, 202, 87, 174, 159, 253, 57, 114, 228, 11, 22, 44, 88, 176,
                163, 133, 201, 81, 162, 135, 205, 89, 178, 167, 141, 217, 113, 226, 7, 14, 28, 56, 112, 224, 3, 6, 12,
                24, 48, 96, 192, 67, 134, 207, 93, 186, 183, 173, 153, 241, 33, 66, 132, 203, 85, 170, 151, 237, 25, 50,
                100, 200, 83, 166, 143, 221, 121, 242, 39, 78, 156, 251, 53, 106, 212, 107, 214, 111, 222, 127, 254, 63,
                126, 252, 59, 118, 236, 27, 54, 108, 216, 115, 230, 15, 30, 60, 120, 240, 35, 70, 140, 219, 117, 234,
                23, 46, 92, 184, 179, 165, 137, 209, 97, 194, 71, 142, 223, 125, 250, 55, 110, 220, 123, 246, 47, 94,
                188, 187, 181, 169, 145, 225, 1]


def linear_transformation(num, move='straight'):
    numIfNull = 257

    for i in range(16):
        coefs = []
        nums = []

        for j in range(len(galua_coef)):
            if move == 'reverse':
                coefs.append(galua_fields.index(galua_coef_reverse[len(galua_coef_reverse) - j - 1]))
            else:
                coefs.append(galua_fields.index(galua_coef[len(galua_coef) - j - 1]))
            if int(convert_base(num[j * 2: j * 2 + 2], from_base=16)) == 0:
                nums.append(numIfNull)
            else:
                nums.append(galua_fields.index(int(convert_base(num[j * 2: j * 2 + 2], from_base=16))))

        galua = []

        for j in range(len(galua_coef)):
            if nums[j] != numIfNull:
                if nums[j] + coefs[j] <= 255:
                    galua.append(galua_fields[nums[j] + coefs[j]])
                else:
                    galua.append(galua_fields[(nums[j] + coefs[j]) % 255])

        galua_num = galua[0]
        if len(galua) != 1:
            for j in range(len(galua) - 1):
                galua_num = int(xor_func(str(galua_num), str(galua[j + 1]), in_code=10), 16) % 256
        galua_num = hex(galua_num)[2:]
        if len(str(galua_num)) == 1:
            galua_num = '0' + str(galua_num)

        if move == 'reverse':
            num = galua_num + num[:len(num) - 2]
        else:
            num = num[2:] + galua_num
    return num


nonlinear_coef = [252, 238, 221, 17, 207, 110, 49, 22, 251, 196, 250, 218, 35, 197, 4, 77, 233, 119, 240, 219, 147, 46,
                  153, 186, 23, 54, 241, 187, 20, 205, 95, 193, 249, 24, 101, 90, 226, 92, 239, 33, 129, 28, 60, 66,
                  139, 1, 142, 79, 5, 132, 2, 174, 227, 106, 143, 160, 6, 11, 237, 152, 127, 212, 211, 31, 235, 52, 44,
                  81, 234, 200, 72, 171, 242, 42, 104, 162, 253, 58, 206, 204, 181, 112, 14, 86, 8, 12, 118, 18, 191,
                  114, 19, 71, 156, 183, 93, 135, 21, 161, 150, 41, 16, 123, 154, 199, 243, 145, 120, 111, 157, 158,
                  178, 177, 50, 117, 25, 61, 255, 53, 138, 126, 109, 84, 198, 128, 195, 189, 13, 87, 223, 245, 36, 169,
                  62, 168, 67, 201, 215, 121, 214, 246, 124, 34, 185, 3, 224, 15, 236, 222, 122, 148, 176, 188, 220,
                  232, 40, 80, 78, 51, 10, 74, 167, 151, 96, 115, 30, 0, 98, 68, 26, 184, 56, 130, 100, 159, 38, 65,
                  173, 69, 70, 146, 39, 94, 85, 47, 140, 163, 165, 125, 105, 213, 149, 59, 7, 88, 179, 64, 134, 172, 29,
                  247, 48, 55, 107, 228, 136, 217, 231, 137, 225, 27, 131, 73, 76, 63, 248, 254, 141, 83, 170, 144, 202,
                  216, 133, 97, 32, 113, 103, 164, 45, 43, 9, 91, 203, 155, 37, 208, 190, 229, 108, 82, 89, 166, 116,
                  210, 230, 244, 180, 192, 209, 102, 175, 194, 57, 75, 99, 182]
nonlinear_coef_reverse = [165, 45, 50, 143, 14, 48, 56, 192, 84, 230, 158, 57, 85, 126, 82, 145, 100, 3, 87, 90, 28, 96,
                          7, 24, 33, 114, 168, 209, 41, 198, 164, 63, 224, 39, 141, 12, 130, 234, 174, 180, 154, 99, 73,
                          229, 66, 228, 21, 183, 200, 6, 112, 157, 65, 117, 25, 201, 170, 252, 77, 191, 42, 115, 132,
                          213, 195, 175, 43, 134, 167, 177, 178, 91, 70, 211, 159, 253, 212, 15, 156, 47, 155, 67, 239,
                          217, 121, 182, 83, 127, 193, 240, 35, 231, 37, 94, 181, 30, 162, 223, 166, 254, 172, 34, 249,
                          226, 74, 188, 53, 202, 238, 120, 5, 107, 81, 225, 89, 163, 242, 113, 86, 17, 106, 137, 148,
                          101, 140, 187, 119, 60, 123, 40, 171, 210, 49, 222, 196, 95, 204, 207, 118, 44, 184, 216, 46,
                          54, 219, 105, 179, 20, 149, 190, 98, 161, 59, 22, 102, 233, 92, 108, 109, 173, 55, 97, 75,
                          185, 227, 186, 241, 160, 133, 131, 218, 71, 197, 176, 51, 250, 150, 111, 110, 194, 246, 80,
                          255, 93, 169, 142, 23, 27, 151, 125, 236, 88, 247, 31, 251, 124, 9, 13, 122, 103, 69, 135,
                          220, 232, 79, 29, 78, 4, 235, 248, 243, 62, 61, 189, 138, 136, 221, 205, 11, 19, 152, 2, 147,
                          128, 144, 208, 36, 52, 203, 237, 244, 206, 153, 16, 68, 64, 146, 58, 1, 38, 18, 26, 72, 104,
                          245, 129, 139, 199, 214, 32, 10, 8, 0, 76, 215, 116]


def nonlinear_transformation(num, move='straight'):
    for i in range(16):
        if move == 'reverse':
            nonlinear_table = nonlinear_coef_reverse
        else:
            nonlinear_table = nonlinear_coef

        num_for_replace = num[i * 2: i * 2 + 2]
        convert_num = convert_base(num_for_replace, to_base=10, from_base=16)
        num_for_replace = convert_base(nonlinear_table[int(convert_num)], to_base=16, from_base=10)
        if len(num_for_replace) == 1:
            num_for_replace = '0' + num_for_replace

        num = num[: i * 2] + num_for_replace + num[i * 2 + 2:]
    return num


X = xor_func
S = nonlinear_transformation
L = linear_transformation


def utf8ToHex(text):
    text = binascii.hexlify(text.encode('utf8')).decode('utf8')
    return text


def transformKey(key):
    key = binascii.hexlify(key.encode('utf8')).decode('utf8')
    while len(key) < 64:
        key += key
    return key[:64]


def hexToUtf8(text):
    try:
        text = binascii.unhexlify(text).decode('utf8')
    except:
        pass
    return text


def getKeys(key):
    key = transformKey(key)

    C = []
    F = []
    K = [key[:int(len(key) / 2)], key[int(len(key) / 2):]]

    for i in range(32):
        if len(hex(i + 1)[2:]) == 1:
            C.append(L('0' + hex(i + 1)[2:] + '000000000000000000000000000000').upper())
        else:
            C.append(L(hex(i + 1)[2:] + '000000000000000000000000000000').upper())

    F.append([K[1], X(L(S(X(K[0], C[0]))), K[1])])
    for i in range(32):
        K = [F[i][1], X(L(S(X(F[i][0], C[i]))), F[i][1])]
        F.append(K)

    K = [key[:int(len(key) / 2)], key[int(len(key) / 2):]]

    for i in range(len(F)):
        if (i + 1) % 8 == 0:
            K.append(F[i][0])
            K.append(F[i][1])
    return (K)


def encrypt(text, K):
    text = utf8ToHex(text)

    count = 32 - len(text) % 32
    if count != 0 and count != 32:
        for i in range(count):
            text += '0'
    textArray = []
    for i in range(int(len(text) / 32)):
        textArray.append(text[i * 32: i * 32 + 32])

    textEncrypt = []
    for j in textArray:
        textEncrypted = j
        for i in range(9):
            textEncrypted = L(S(X(textEncrypted, K[i])))
        textEncrypted = X(textEncrypted, K[9])
        textEncrypt.append(textEncrypted)
    return (''.join(textEncrypt))


def decrypt(text, K):
    textArray = []
    for i in range(int(len(text) / 32)):
        textArray.append(text[i * 32: i * 32 + 32])

    textDecrypt = []
    for j in textArray:
        textDecrypted = j
        for i in range(9, 0, -1):
            textDecrypted = S(L(X(textDecrypted, K[i]), 'reverse'), 'reverse')
        textDecrypted = X(textDecrypted, K[0])
        textDecrypt.append(textDecrypted)
    return (hexToUtf8(''.join(textDecrypt)))
