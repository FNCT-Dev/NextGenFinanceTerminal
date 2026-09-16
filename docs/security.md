# Security

The planned PIN is local UI access control, not a bank PIN, disk encryption, credential-encryption master key, or defense against a compromised OS account. Phase 1 supplies strict six-ASCII-digit validation and a PIN service boundary but stores no PIN. Phase 2 will use Argon2 hashes, confirmation, verification, change, and progressive lockout.

GUI credentials will use the OS keyring through `CredentialStore`, never normal configuration. Logs redact common credential fields; no path may emit PINs, full hashes, secrets, Authorization headers, or tokens. Forgotten-PIN recovery will be an explicit local security reset, with no master PIN or automatic destruction.

