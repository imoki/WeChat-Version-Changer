# -*- coding: utf-8 -*-

"""
    作者：imoki
    仓库：https://github.com/imoki/WeChat-Version-Changer
    时间：2024年10月14日
    功能：动态修改内存中的微信版本号，需要启动微信并且在未登录时进行修改
    备注：代码中“自行修改”部分需自己改动。下次再登录前也需要进行修改。可以将微信加入自启动，并将脚本也加入自启动。
"""

from pymem import Pymem

# 需要修改为的微信版本
versionNew = "3.9.12.15"    # 自行修改

# 需要修改的偏移地址
offsetArray = [0x2367624, 0x2385AF0, 0x2385C44, 0x239C98C, 0x239EAFC, 0x23A1604]  # 自行修改，用CE可查看

# 版本号按字节分割
# 0x63090A13 -> 3.9.10.19
# 0x63090217 -> 3.9.2.23
# 0x63090c0f-> 3.9.12.15

# 待修改的偏移地址，可用CE获取
# WeChatWin.`cereal::detail::StaticObject<cereal::detail::PolymorphicCasters>::create'::`2'::$TSS0+1678
# WeChatWin.TXBugReport::pfPreBugReport+B3AC
# WeChatWin.TXBugReport::pfPreBugReport+B500
# WeChatWin.dll+239C98C
# WeChatWin.dll+239EAFC
# WeChatWin.dll+23A1604

# 十六进制转版本号
def hexToVersion(versionHex):
    # versionHex = versionHex[2:]   # 去掉前缀 '0x'
    # print(versionHex)
    binary_str = bin(int(versionHex, 16))[6:].zfill(32)   # 将十六进制转换为二进制字符串，去掉前缀 '0b'和0110 并确保是32位
    #print(binary_str)
    byte_parts = [binary_str[i:i+8] for i in range(0, len(binary_str), 8)]  # 分割二进制字符串为四个字节
    decimal_parts = [str(int(byte, 2)) for byte in byte_parts]  # 将每个字节转换为十进制，并用 '.' 连接
    version = '.'.join(decimal_parts)
    return version

# 版本号转十六进制
def versionToHex(version):
    version_parts = version.split('.')  # 将版本号字符串拆分成各个部分
    binary_parts = []
    i = 0
    for part in version_parts:
        if i == 0:
            part = int(part) + 0b01100000   # 十六进制最高位为6
        part = bin(int(part)).replace('0b', '').zfill(8)
        binary_parts.append(part)
        i += 1
    # binary_parts = [bin(int(part)).replace('0b', '').zfill(8) for part in version_parts]  
    # print(binary_parts)  
    binary_str = ''.join(binary_parts)
    versionHex = hex(int(binary_str, 2))
    # hex_str = hex(int(binary_str, 2))[2:].zfill(8)
    return versionHex

def changeVersion(pm: Pymem):
    WeChatWindllBase = 0
    for m in list(pm.list_modules()):
        path = m.filename
        if path.endswith("WeChatWin.dll"):
            WeChatWindllBase = m.lpBaseOfDll
            break
            
    i = 0
    for offset in offsetArray:
        addr = WeChatWindllBase + offset
        
        if i == 0:
            # 获取当前微信版本，只输出一次
            versionHexOld = pm.read_uint(addr)  # 十进制
            versionOld = hexToVersion(hex(versionHexOld))
            print("当前版本：", versionOld) 
        
        versionNewChange = versionToHex(versionNew)
        pm.write_uint(addr, int(versionNewChange, 16))  # 写入新的微信版本
        
        if i == 0:
            print("微信版本号已修改为：" + versionNew)
            i += 1

def test():
    versionNewHex = versionToHex(versionNew)
    print(versionNewHex)
    print(hexToVersion(versionNewHex))

if __name__ == "__main__":
    # try:
    pm = Pymem("WeChat.exe")
    changeVersion(pm)
    # except Exception as e:
    #     print(f"{e}，请先启动微信，再运行此脚本")

    # test()
