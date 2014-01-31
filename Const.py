'''
Created on 2014-1-30

@author: bell
'''
AES_KEY = {'jp': {'res': 'A1dPUcrvur2CRQyl', 'helper':
                  'A1dPUcrvur2CRQyl', 'crypt': 'uH9JF2cHf6OppaC1'}}
RSA_KEY_POOL = [
    "MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBANV2ohKiVs/2cOiGN7TICmQ/NbkuellbTtcKbuDbIlBMocH+Eu0n2nBYZQ2xQbAv+E9na8K2FyMyVY4+RIYEJ+0CAwEAAQ==",
    "MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAOLtTe70uQZ2BAneeTyNezMH/yn/uDu6qabQ3XHhmqqW8C4ZLxG7uW6bNmUdZQSUk8dO2+7ZTbN5lQw/u70Av2ECAwEAAQ==",
    "MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAM5U06JAbYWdRBrnMdE2bEuDmWgUav7xNKm7i8s1Uy/fvpvfxLeoWowLGIBKz0kDLIvhuLV8Lv4XV0+aXdl2j4kCAwEAAQ==",
    "MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAL1mnz5vCQEa1xPeyIUQ2WHIzKIsZp9PKAzJ6etXV2NpyxoGheqlDZ5rXQVLEY2JSY2nBlt/QBdo9xkp8XcFgUsCAwEAAQ==",
    "MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAKFTx5sYAmW9kFineXZj6NwGPGA6QSgui+nwb9ru30oeoYviC6e5iHD/Qk7Gc8JPpIA335YHo6K1/U8U9gM3BncCAwEAAQ==",
    "MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAL3EP/qaJ9XGmpEia4KqoJkCYFvgpJtWK3zPZ7d/qCF1GbQSSzPI+FUnuJjAXSZ43vvYYmQNHNYg791C9SrSOT0CAwEAAQ==",
    "MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBANWNwx1kRSlR5sl3dHkPtW//F5KlRQMPWbrLG3ZyCI1q3NUMOC+xdC87gGiINs4WC3S28j0/DrrocIXS7zf2MdECAwEAAQ==",
    "MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBANzMvdAQ/lmyAQQ3S0B1BkzlwvR8mYrCiATLRV0t/HeudLvhUgbkWm2UNr4M84f0wA52XqFPABMyp+o59D4DEwUCAwEAAQ==",
    "MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBANr/4m+Z7qKlr2kmyZmgNjf49LSgm6QP5JZwk+Wi2m8E68sUMyfKkhr1t2OXlvNAEfQrSYHu6rlXqpSf2o1zvSkCAwEAAQ==",
    "MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBANqJlJznVfrsXd/Nnn4L7E7Kcz2u1YwIExrJC3uyxsEk+HiCnNJ8ZUFtkc7XeZKEyw2UFfiQ73SOFAzhVfkCCS0CAwEAAQ==",
]

SERVER_ADDRESS = {'jp': 'http://web.million-arthurs.com/connect/app/'}

APP_ADDRESS = {'area':'exploration/area?cyt=1',
               'login':'login?cyt=1',
               'check_inspection':'check_inspection?cyt=1',
               'floor':'exploration/floor?cyt=1',
               'get_floor':'exploration/get_floor?cyt=1',
               'guild_explore':'exploration/guild_explore?cyt=1'}

HEADER = {'Accept-Encoding': 'gzip, deflate',
          'User-Agent': 'Million/250 (SBM203SH; SBM203SH; 4.1.2) SBM/SBM203SH/SBM203SH:4.1.2/S0024/00.00.00:user/release-keys GooglePlay',
          'Content-Type': 'application/x-www-form-urlencoded'
          }
