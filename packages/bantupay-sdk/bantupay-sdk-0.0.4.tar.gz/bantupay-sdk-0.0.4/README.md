# BantuPay SDK

## Installation

Using pip to include bantupay-sdk in your own project:

```shell
 $ pip install bantupay-sdk

```

## Getting started

- Use the following code to create key pair.

```python
from bantupay_sdk import account

keyPair = account() # keyPair will now contain this structure {secret: '', publicKey: ''}
```

- Use the folowing code to sign http data

```python
from bantupay_sdk import sign_http

http_Sign = sign_http(
  '/v2/user/',
  '{username: "proxie"}',
  'SBVNK4S2NU2QSBDZBKQCGR7DX5FTQFDJVKGWVCZLIEOV4QMANLQYSLNI'
); # Secret key gotten from the create account method.
```

- Use this to Sign a transaction

```python
from bantupay_sdk import sign_txn

const signTxn = bantuSDK.signTxn(
  "SDBG73M4LPCPCQ6NQ4CP4LCF7MOOQGUFJRRBD26P6QKIHW2ESP5R7DDN",
  "AAAAAOKtdgWGQ02FzacmAD1WhAhI5Dp7kPRojOGjNQj3FBWvAAAAZAAcmBgAAAAEAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAANQmFudHUuTmV0d29yawAAAAAAAAAAAAAAAAAAAA==",
  "Bantu Testnet"
);
```
