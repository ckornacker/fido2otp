# Fido2OTP

A simple tool that uses FIDO2's `hmac-secret` extension to create resident credentials and static challenge responses to encrypt TOTP secrets. The secrets are stored using the D-Bus Secret Service API (GNOME Keyring) and decrypting and deriving TOTP tokens requires user verification.

Inspired by [SoloKey](https://github.com/solokeys/solo-python/blob/master/README.md#challenge-response) and tested with [OpenSK](https://github.com/google/OpenSK)

## Usage

1. Store base32 TOTP secret encrypted with the security key's static response in the keyring

    ```shell
    fido2otp push my-service NZKHGK6DVNZSEY56
    ```

2. Generate TOTP token for my-service. Requires user verification.

    ```shell
    fido2otp get my-service
    ```

