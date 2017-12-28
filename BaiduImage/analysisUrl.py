'''
百度图片在搜索的第一屏上，图片的地址是 objURL,图片的base64编码也在。
第n屏（n>=2)是通过XHR 动态加载，返回json数据，objURL是加密字符串
    秘钥是一个字符的对应关系，有2种映射：
    （1）多个字符映射为一个字符，'_z2C$q'=>':','_z&e3B'=>'.','AzdH3F'=>'/'。
    （2）单个字符映射为单字符。
        static char table[128] = {0};  
          table['w'] = 'a';  
          table['k'] = 'b';  
          table['v'] = 'c';  
          table['1'] = 'd';  
          table['j'] = 'e';  
          table['u'] = 'f';  
          table['2'] = 'g';  
          table['i'] = 'h';  
          table['t'] = 'i';  
          table['3'] = 'j';  
          table['h'] = 'k';  
          table['s'] = 'l';  
          table['4'] = 'm';  
          table['g'] = 'n';  
          table['5'] = 'o';  
          table['r'] = 'p';  
          table['q'] = 'q';  
          table['6'] = 'r';  
          table['f'] = 's';  
          table['p'] = 't';  
          table['7'] = 'u';  
          table['e'] = 'v';  
          table['o'] = 'w';  
          table['8'] = '1';  
          table['d'] = '2';  
          table['n'] = '3';  
          table['9'] = '4';  
          table['c'] = '5';  
          table['m'] = '6';  
          table['0'] = '7';  
          table['b'] = '8';  
          table['l'] = '9';  
          table['a'] = '0';  
'''
url = r'ippr_z2C$qAzdH3FAzdH3Ffl_z&e3Bftgwt42_z&e3BvgAzdH3F4omlaAzdH3Faa8W3ZyEpymRmx3Y1p7bb&mla'
dictChar = {
    'w' : 'a',  
    'k' : 'b',  
    'v' : 'c',  
    '1' : 'd',  
    'j' : 'e',  
    'u' : 'f',  
    '2' : 'g',  
    'i' : 'h',  
    't' : 'i',  
    '3' : 'j',  
    'h' : 'k',  
    's' : 'l',  
    '4' : 'm',  
    'g' : 'n',  
    '5' : 'o',  
    'r' : 'p',  
    'q' : 'q',  
    '6' : 'r',  
    'f' : 's',  
    'p' : 't',  
    '7' : 'u',  
    'e' : 'v',  
    'o' : 'w',  
    '8' : '1',  
    'd' : '2',  
    'n' : '3',  
    '9' : '4',  
    'c' : '5',  
    'm' : '6',  
    '0' : '7',  
    'b' : '8',  
    'l' : '9',  
    'a' : '0'
}
# str 的translate方法需要用单个字符的十进制unicode编码作为key
# value 中的数字会被当成十进制unicode编码转换成字符
# 也可以直接用字符串作为value
dictChar = {ord(key):ord(value) for key, value in dictChar.items()}

dictStr = {'_z2C$q':':', '_z&e3B':'.', 'AzdH3F':'/'}

for key, value in dictStr.items():
    url = url.replace(key, value)
    print(url)
url = url.translate(dictKey)
print(url)
