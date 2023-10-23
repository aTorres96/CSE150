def chop(s):
    s = txt.split()
    ip = ""
    mask = ""
    for i in range(len(s)):
        if(s[i][0].isdigit()):
            ip += s[i]
            ip += ' '
        elif(s[i][0] == '/'):
            mask = s[i]
    mask = mask.split('/')
    mask = int(mask[1])
    ip = ip.split()
    return ip, mask
def tobin(x):
    y = ""
    if x == 0:
        y = "00000000"
        return y
    while(x > 0):
        y = str(x % 2) + y
        x = int(x / 2)
    if(len(y) < 8):
        for i in range(8-len(y)):
            y = '0' + y
    return y

print("Input to see if an IP address is valid on a subnet.")
txt = input()
s = chop(txt)
mask = s[1]
subnet = s[0][0].split('.')
test = s[0][1].split('.')
final = True;
subnet = [int(i) for i in subnet]
testip = [int(i) for i in test]
sub, test = '', ''
for i in range(len(subnet)):
    sub += tobin(subnet[i])
    test += tobin(testip[i])
if(sub[:mask] != test[:mask]):
    final = False
if(final):
    print(s[0][1], "is valid on subnet", s[0][0])
else:
    print(s[0][1], "is invalid on subnet", s[0][0])