#!/bin/bash

# decrypt_files.sh
# Usage: ./decrypt_files.sh encrypted_file1.gpg encrypted_file2.gpg ...

# Load environment variables
source .env 2>/dev/null || {
  echo "Error: .env file not found or not readable" >&2
  exit 1
}

# Check if encryption password is set
if [[ -z "$ENCRYPTION_PASSWORD" ]]; then
  echo "Error: ENCRYPTION_PASSWORD not set in .env" >&2
  exit 1
fi

# Check if any arguments were provided
if [[ $# -eq 0 ]]; then
  echo "Error: No files specified" >&2
  echo "Usage: $0 encrypted_file1.gpg encrypted_file2.gpg ..." >&2
  exit 1
fi

# Process each file
for encrypted_file in "$@"; do
  # Check if file exists
  if [[ ! -f "$encrypted_file" ]]; then
    echo "Warning: '$encrypted_file' does not exist - skipping" >&2
    continue
  fi

  # Set output filename (remove .gpg extension if present)
  output_file="${encrypted_file%.gpg}"

  # Decrypt the file
  gpg --batch --yes \
      --passphrase "$ENCRYPTION_PASSWORD" \
      -o "$output_file" \
      --decrypt "$encrypted_file"

  # Check decryption status
  if [[ $? -eq 0 ]]; then
    echo "Decrypted: $encrypted_file → $output_file"
  else
    echo "Error: Failed to decrypt $encrypted_file" >&2
  fi
done