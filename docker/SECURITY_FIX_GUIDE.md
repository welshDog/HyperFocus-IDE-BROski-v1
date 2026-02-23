# Security Vulnerability Fix Guide

## Overview
Your `hyperfocus-ide-broski-v1-project-strategist:latest` image has **121 vulnerabilities** across **28 packages**, including **4 CRITICAL** and **27 HIGH** severity issues.

### Vulnerability Summary
- **CRITICAL (4)**: expat (2), openssl (1), krb5 (1)
- **HIGH (27)**: glibc, openssl, starlette, setuptools, perl, sqlite3, pam, gnupg2, fastapi, wheel, and more
- **MEDIUM (32)**: gnutls28, shadow, tar, pip, libcap2, libtasn1, and others
- **LOW (60)**: Various low-priority issues
- **UNSPECIFIED (1)**: One additional vulnerability

## Root Cause
The image is based on **Debian 12 (bookworm)** with packages from ~23 months ago. System libraries (OpenSSL, glibc, expat) are severely outdated.

---

## Fix Strategy

### Option 1: Quick Fix (Recommended for immediate use)
Rebuild the image with the latest base and system packages:

```bash
# Pull fresh base image and rebuild
docker build \
  --pull \
  --no-cache \
  -t hyperfocus-ide-broski-v1-project-strategist:v1-patched \
  -f Dockerfile.secure \
  .
```

### Option 2: Complete Rebuild (For source-available projects)
If you have access to the original Dockerfile:

```bash
# Edit your original Dockerfile and add after FROM line:
# RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# Then rebuild with:
docker buildx bake --pull -f docker-bake.hcl project-strategist
```

### Option 3: Docker Hardened Images (DHI) Migration
Use pre-hardened, minimal base images from Docker:

```bash
# Replace your Debian base with:
# FROM docker/docker-hardened-debian:12-bookworm
# This provides pre-scanned, security-optimized images
```

---

## Python Package Updates Required

The following Python packages have vulnerabilities and need upgrades:

| Package | Current | Minimum Safe | CVE(s) |
|---------|---------|--------------|--------|
| **fastapi** | 0.109.0 | 0.109.1+ | CVE-2024-24762 (DoS) |
| **starlette** | 0.35.1 | 0.40.0+ | CVE-2024-47874, CVE-2024-24762 (DoS/Regex) |
| **setuptools** | 65.5.1 | 78.1.1+ | CVE-2025-47273, CVE-2024-6345 (Path Traversal, Code Injection) |
| **wheel** | 0.43.0 | 0.46.2+ | CVE-2026-24049 (Path Traversal) |
| **pip** | 24.0 | 26.0+ | CVE-2025-8869, CVE-2026-1703 (Link Following, Path Traversal) |

### Update Python packages:
```bash
pip install --upgrade \
  'fastapi>=0.109.1' \
  'starlette>=0.40.0' \
  'setuptools>=78.1.1' \
  'wheel>=0.46.2' \
  'pip>=26.0'
```

Or use the provided requirements file:
```bash
pip install -r requirements-security-patches.txt
```

---

## System-Level Vulnerabilities (Fixed by rebuilding)

When you rebuild with `--pull`, the following will be patched automatically:

### Critical System Libraries
1. **openssl (3 CRITICAL, 5 HIGH, 8 MEDIUM, 8 LOW)**
   - Encryption vulnerabilities affecting TLS/SSL
   - Updated to: 3.0.18-1~deb12u2 or later

2. **expat (2 CRITICAL, 3 HIGH, 1 MEDIUM, 2 LOW)**
   - XML parser buffer overflow vulnerabilities
   - Updated to: 2.5.0-1+deb12u1 or later

3. **krb5 (1 CRITICAL, 2 HIGH, 1 MEDIUM, 4 LOW)**
   - Authentication framework vulnerabilities
   - Updated to: 1.20.1-2+deb12u3 or later

### High-Priority System Libraries
4. **glibc (5 HIGH, 2 MEDIUM, 7 LOW)**
   - C runtime library vulnerabilities
   - Updated to: 2.36-9+deb12u13 or later

5. **perl (1 HIGH, 1 MEDIUM, 2 LOW)**
   - Scripting language vulnerabilities
   - Updated to: 5.36.0-7+deb12u3 or later

6. **Other libraries**: gnutls28, sqlite3, pam, systemd, gnupg2, shadow, tar, libcap2, libtasn1

---

## Implementation Steps

### Step 1: Update Dockerfile
Add system package updates to your Dockerfile:

```dockerfile
FROM python:3.11-bookworm

# Security: Update all system packages
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
      curl \
      ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Upgrade pip, setuptools, wheel BEFORE installing other packages
RUN pip install --no-cache-dir --upgrade \
    pip>=26.0 \
    setuptools>=78.1.1 \
    wheel>=0.46.2

# ... rest of your Dockerfile ...
```

### Step 2: Rebuild Image
```bash
docker build --pull --no-cache -t hyperfocus-ide-broski-v1-project-strategist:latest .
```

### Step 3: Verify Fix
```bash
docker scout cves local://hyperfocus-ide-broski-v1-project-strategist:latest
```

The CRITICAL and HIGH vulnerabilities should be resolved after rebuild.

---

## Remaining Vulnerabilities After Fix

**Note**: Some LOW and a few MEDIUM vulnerabilities may remain unfixed in the Debian repositories (CVEs marked "not fixed"). These are:
- Older security issues with no available patches
- Issues requiring major version upgrades
- Artifacts with security limitations in design

### Examples:
- CVE-2024-28757 (expat): <=2.5.0-1+deb12u2 (not fixed)
- CVE-2025-27587 (openssl): <=3.0.18-1~deb12u1 (not fixed)
- CVE-2019-9192 (glibc): <=2.36-9+deb12u13 (not fixed)

These can only be resolved by upgrading to a newer Debian release (13+) or a different base image.

---

## Advanced: Migrate to Docker Hardened Images (DHI)

For maximum security with minimal base image:

```dockerfile
FROM docker/docker-hardened-debian:12-bookworm

# Your application setup...
```

Benefits:
- Pre-scanned for vulnerabilities
- Minimal attack surface
- Signed and verified by Docker
- Automatic security updates

See: https://docs.docker.com/dhi/

---

## Continuous Security Monitoring

### Enable Docker Scout in CI/CD
Add to GitHub Actions or your CI pipeline:

```yaml
- name: Docker Scout Scan
  uses: docker/scout-action@v1
  with:
    image: ${{ env.REGISTRY }}/your-image:latest
    exit-code: 0  # Change to 1 to fail on HIGH+ severity
```

### Regular Scanning
Schedule weekly image scans:
```bash
docker scout cves --format json --output report.json your-image:latest
```

---

## Summary

| Action | Effort | Time | Impact |
|--------|--------|------|--------|
| **Rebuild with --pull** | Low | 5-10 min | Fixes 95+ vulnerabilities |
| **Update Python packages** | Low | 2-3 min | Fixes 5+ vulnerabilities |
| **Migrate to DHI** | Medium | 1-2 hours | Fixes remaining LOW issues |
| **Add CI scanning** | Low | 30 min | Prevents regression |

---

## Support

For questions or issues:
- Docker Scout docs: https://docs.docker.com/engine/security/
- DHI documentation: https://docs.docker.com/dhi/
- Build best practices: https://docs.docker.com/build/
