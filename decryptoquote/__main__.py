from .decryptoquote import (
    getCrypto,
    displayPlaintext
    )
# Replace project_name and needed_imports as appropriate


def main():
    crypto = input("Enter cryptoquote: ")
    plaintext = decryptQuote(crypto)
    print(plaintext)


if __name__ == "__main__":
    main()
