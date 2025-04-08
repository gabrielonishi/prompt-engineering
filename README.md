# prompt-engineering

### Symmetric Encryption (Password Only)

1. Add password to `.env` file:

```bash
echo 'ENCRYPTION_PASSWORD="your_strong_password"' > .env
```

2. Make encryption and decryption files executable:

```bash
chmod +x decrypt.sh encrypt.sh
```

3. To encrypt files:

```bash
./encrypt.sh slides/*.pdf
```

4. To decrypt files:

```bash
./decrypt.sh slides/*.gpg
```
