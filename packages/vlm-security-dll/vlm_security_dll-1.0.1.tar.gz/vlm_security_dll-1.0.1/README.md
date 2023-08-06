- [註冊](#註冊)
- [安裝](#安裝)
- [建立產品](#建立產品)
- [用戶模式](#用戶模式)
- [推廣策略](#推廣策略)
- [API使用](#api使用)
- [驗證卡號方式](#驗證卡號方式)
- [加值卡](#加值卡)
- [儲值](#儲值)


## 註冊
1. 進入[VLM後台](https://my.vlm-security.com/) ，註冊帳號，並到信箱接收驗證信。


## 安裝
1 . [下載開發包](https://sdk.vlm-security.com/)。


2 . 解壓縮後，將 CallInterface/DLL/Win32/VAuth.dll 複製到 C:\Windows\System32


3 . 將 CallInterface/VServerGroup.vnc 複製到Python的編譯器同層下。
 
舉例：我的是在 C:\Users\user1\.virtualenvs\vlm_security_dll_python\Scripts

**注意：其他資料夾也有VServerGroup.vnc只能使用CallInterface的VServerGroup.vnc**
 
4 . 從Pypi 安裝

`pip install vlm-security-dll`
 
    
   
## 建立產品
1. 登入VLM控制台：
    * 登入程式在開發包裡的 VLM 管理端 ManageTerminal\Developer Terminal\VLM_Develop.exe
    * 打開 VLM 管理端，並且登入您剛剛註冊的帳號密碼
    ![](https://i.imgur.com/lsfNatC.png)
1. 建立產品：
    * 新建一個產品
    * 產品編號: 具有唯一性，用於識別產品，也可以做為試用卡號
    * 產品名稱: 作者自定義，用於識別管理產品
    * 上傳更新: 支援自動更新，程式需要調用Update 函數，並且攜帶FileReplace.exe
    ![](https://i.imgur.com/TeiafEd.png)


1. 設定產品保護認證加密： 
    * 建立產品後，切換頁籤到保護設定。
    ![](https://i.imgur.com/VGOWLny.png)
    * 選擇想要的算法，輸入加密所需密鑰。
    ![](https://i.imgur.com/pru6SkQ.png)
    * 也可以設置多層加密
    ![](https://i.imgur.com/Y3Y6U5E.png)
    
1. 建立註冊碼
    * 建立認證加密後，切換頁籤到註冊碼。
    ![](https://i.imgur.com/WrlWg5h.png)
    * 選擇你的產品，點選建立，輸入註冊碼的相關參數
    ![](https://i.imgur.com/Lf5HmkA.png)
    * 提交後就會創建相對的註冊碼
    ![](https://i.imgur.com/DaV6TZF.png)
    
## 用戶模式
1. 需對應產品管理的充值卡，使用充值卡可以對使用者或者註冊碼添加時間

    ![](https://i.imgur.com/XSmBE8P.png)
    ![](https://i.imgur.com/D9mJJ41.png)

## 推廣策略

   ![](https://i.imgur.com/cpIuaA7.png)

## API使用

* 使用測試編號
    ```
    vlm_obj = VLM_security.auth_trial()
    ```
* 使用自己的產品編號
    ```
    vlm_obj = VLM_security(r"C:\Windows\VAuth.dll", "your product code")
    ```

* 初始化

    大於等於0表示成功。（連接了某台伺服器並返回伺服器編號），小於0表示連接失敗。失敗時應提示使用者無法連接驗證服務器並退出程序。
    ```    
    result = vlm_obj.init()
    ```
* 獲取校驗碼

    調用Auth並返回成功後調用此函數可獲取返回的校驗碼。
    ```
    return_value = vlm_obj.get_code()
    ```
* 取插件的版本號

    如果你使用的是普通dll版，此功能函數請參考: 純Dll接口說明-取插件版本。
    return_value = 返回插件版本號。
    ```
    return_value = vlm_obj.get_ver()
    ```
* 驗證碼模式，驗證註冊碼是否有效。

    試用卡：是産品編號，則當作測試 用卡處理。
    return_value = 0 成功 -1 失敗 -2 註冊碼被禁用 -3 綁定機器超出數量 -4 註冊碼已在線 -5 已過期
    ```
    return_value = vlm_obj.auth('your register code')
    ```

* 加密 string encrypt(BYTE type, string src, string key)

    對GUID字串進行加密，type byte 加密算法 0 表示AES算法，1表示MD5算法，src string GUID字串，需要加密的字串，key string 加密鍵值 type 為1(MD5)加密時此參數無意義。
    return_value = 加密結果，GUID格式的字串
    ```
    return_value = vlm_obj.encrypt(0,'str', '456')
    ```
    
* 解密 string decrypt(BYTE type, string src, string key)

    對GUID字串進行解密， type byte 加密算法 0 表示AES算法，1表示MD5算法，src string GUID字串，需要加密的字串，key string 加密鍵值 type 為1(MD5)加密時此參數無意義。
    return_value = GUID格式的字串
    ```
    return_value = vlm_obj.decrypt(0,'str', '456')
    ```
    
* 使用者模式，驗證使用者是否有效

    return_value = 0 成功 -1 失敗 -2 註冊碼被禁用 -3 綁定機器超限 -4 註冊碼已在線 -5 已過期 -6 使用者餘額不足 -7 使用者無效
    ```
    return_value = vlm_obj.user_auth("user", "password")
    ```
* 取卡或使用者的使用到期時間。測試卡無到期時間
    ```
    return_value = vlm_obj.get_validity()
    ```
* 使用者註冊

    return_value = 0 成功 ；-1 失敗 ；-8 使用者名重複
    ```
    return_value = vlm_obj.user_register(string user, string pwd,int type, int bind, int multi,int point)
    ```
* 使用者密碼修改

    return_value = 0 表示成功 非0失敗
    ```
    return_value = vlm_obj.change_password(string Old,string New)
    ```
* 檢查是否到了無效狀態

    這函數是為無法回響COM事件的語言比如易語言裡使用的，每隔幾秒調用一次，在可以回響COM事件的語言裡無需此函數，回響OnInvalid事件即可。
    return_value = Bool true:有效 false:無效
    ```
    return_value = vlm_obj.is_valid()
    ```
* 對此機器進行解綁操作，在驗證成功後方可調用。

    return_value = 0:成功 非0失敗
    ```
    return_value = vlm_obj.unbind()
    ```
    
*  加時
    
     return_value = 0 成功 -1 不存在 -7 無效：已被使用或非加時卡（比如:註冊碼）等等
     ```
     return_value = vlm_obj.add_time('card_id','user_id','Recommender_id')
     ```
    
* 扣除時間

    返回剩餘計數
    ```
    return_value = vlm_obj.deduct_point(int point）
    ```
* 扣取點數

    返回剩餘計數，不能傳小數（比如：0.5）
    ```
    return_value = vlm_obj.deduct_hour(int hour)
    ```
* 關閉 VLM

    調用此函數VLM將停止工作，用於關閉Process前調用（必須調用否則有機率卡死）
    ```
    vlm_obj.release()
    ```
    
## 驗證卡號方式
*  舉例
    我的加密順序是使用第一次密鑰test123，第二次密鑰456test

    ![](https://i.imgur.com/nLZ9DZy.png)
    
    1. 解碼法驗證時，必須反過來必須先使用密鑰456test解碼

        ```
        encode = vlm_obj.decrypt(0,encode, '456test')
        ```
        
    2. 再使用密鑰test123解碼

        ```
        encode = vlm_obj.decrypt(0,encode, 'test123')
        ```

*  注意事項

    請在專案個檢察處設定暗樁，請不要把以下的程式碼包裝成函式，並且在一些關鍵的邏輯間，插入以下程式碼

    ```
    encode = vlm_obj.get_code()
    encode = vlm_obj.decrypt(0,encode, '456')
    encode = vlm_obj.decrypt(0, encode, '123')
    if encode != vlm_obj.auth_code:
        exit()
    ```

## 加值卡
1. 建立產品加密後，切換頁籤到充值卡。
![](https://i.imgur.com/7ctHcCW.png)
1. 輸入天數，點數，數量，點選建立。
![](https://i.imgur.com/wDwgRMD.png)
1. 提交後就會創建相對的充值卡
![](https://i.imgur.com/EdY7OPZ.png)
