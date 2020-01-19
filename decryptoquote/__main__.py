from .decryptoquote import (
    decrypt_quote)
# Replace project_name and needed_imports as appropriate


def main():
    crypto = input("Enter cryptoquote: ")
    plaintext = decrypt_quote(crypto)
    print(plaintext)


if __name__ == "__main__":
    main()
