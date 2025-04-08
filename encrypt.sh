#!/bin/bash

# encrypt_files.sh
# Usage: ./encrypt_files.sh file1.txt file2.jpg ...

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
  echo "Usage: $0 file1 file2 ..." >&2
  exit 1
fi

# Process each file
for file in "$@"; do
  # Check if file exists
  if [[ ! -f "$file" ]]; then
    echo "Warning: '$file' does not exist - skipping" >&2
    continue
  fi

  # Set output filename
  output_file="${file}.gpg"

  # Encrypt the file
  gpg --batch --yes \
      --passphrase "$ENCRYPTION_PASSWORD" \
      --cipher-algo AES256 \
      -o "$output_file" \
      --symmetric "$file"

  # Check encryption status
  if [[ $? -eq 0 ]]; then
    echo "Encrypted: $file → $output_file"
  else
    echo "Error: Failed to encrypt $file" >&2
  fi
done