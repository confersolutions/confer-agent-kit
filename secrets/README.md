# Confer Agent Kit Secrets Workspace

**DO NOT COMMIT SECRETS** - This directory is git-ignored.

## Structure

\`\`\`
secrets/
  _intake/              # Raw dumps and parse reports (timestamped)
  global/               # Reusable cross-project secrets
    .env.global         # Global environment variables
    credentials.csv     # Username/password pairs (masked)
    tokens.csv          # Bearer/JWT tokens (masked)
    endpoints.csv       # Service URLs
    ssh/                # SSH keys
  services/             # Service-specific secrets
    <service>/          # Per-service directory
      .env.local        # Service env vars
      README.md         # Documentation
  registry.yaml         # Master index
  README.md             # This file
\`\`\`

## Usage

### Global vs Service-Scoped Secrets

**Global secrets** (`.env.global`): Reusable across projects
- API keys for external services (OpenAI, Groq, etc.)
- Universal tokens
- Shared credentials

**Service-scoped secrets** (`services/<service>/.env.local`): Specific to one service
- Database connection strings for a specific service
- Service-specific API keys
- Local development overrides

### How to Reference

**Locally:**
\`\`\`bash
# Source global secrets
source secrets/global/.env.global

# Or source service-specific
source secrets/services/openai/.env.local
\`\`\`

**In platforms (Coolify/Vercel/Replit):**
- **DO NOT** upload raw `.env.global` or `.env.local` files
- Instead, add individual environment variables through platform UI
- Use the keys from `.env.global` or service `.env.local` files

### Recommended Secret Managers

For team sharing, use:
- **1Password** - Secure team vaults
- **Bitwarden** - Open-source password manager
- **Doppler** - Developer-first secret management
- **AWS Secrets Manager** / **GCP Secret Manager** - Cloud-native

### Rotation Checklist

- [ ] Review `secrets/_intake/` for new additions
- [ ] Update platform env vars when rotating keys
- [ ] Update `registry.yaml` when adding services
- [ ] Remove old keys from `.env.global` or service `.env.local`
- [ ] Verify no secrets in git history: `git log --all --full-history -- "**/*.env*"`

## Parse History

**Total Intake Runs:** 2
**Latest Parse:** 20251101_2244 (2025-11-01 22:44:59)

## Detected Services

The following services have been detected across all parse runs:

cloudflare, contabo, coolify, qdrant, snapshot, ssh

## Safety

- **All files under `secrets/` are git-ignored**
- **Never commit secrets** - use platform env vars instead
- **Rotate keys regularly** - check `registry.yaml` for active keys
- **Mask in logs** - secrets are masked (first 4 + last 2 chars) in reports
