# WeChat-Version-Changer
动态修改内存中的微信版本号

## 可自行修改地方 
1. 微信版本号  
versionNew = "3.9.12.15"    # 自行修改  
  
2. 微信版本号在内存中的地址  
offsetArray = [0x2367624, 0x2385AF0, 0x2385C44, 0x239C98C, 0x239EAFC, 0x23A1604]  # 自行修改，用CE可查看
CE中搜索定位到WeChatWin即可看到这些地址，一般6-7个。也可根据你当前的版本号（十六进制）检索这些地址。

## 原理 
版本号按字节分割，十六进制转十进制，最高位4比特保持为0110，如：    
0x63090A13 -> 3.9.10.19  
0x63090217 -> 3.9.2.23  
0x63090c0f-> 3.9.12.15  
通过在内存中修改这些值即可达到动态修改版本号的效果，在设置中可实时查看修改后的微信版本。  
