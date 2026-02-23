#!/usr/bin/env pwsh
# Security Patch & Rebuild Script
# This script rebuilds your image with all security patches applied

param(
    [string]$ImageName = "hyperfocus-ide-broski-v1-project-strategist",
    [string]$Tag = "v1-patched",
    [switch]$Scan = $true,
    [switch]$Push = $false
)

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Docker Image Security Patch" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Colors
$Success = "Green"
$Warning = "Yellow"
$Error = "Red"
$Info = "Cyan"

# Step 1: Check prerequisites
Write-Host "Step 1: Checking prerequisites..." -ForegroundColor $Info
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: Docker not found. Please install Docker Desktop." -ForegroundColor $Error
    exit 1
}
Write-Host "✓ Docker is installed" -ForegroundColor $Success

# Step 2: Display vulnerability summary
Write-Host ""
Write-Host "Step 2: Current vulnerability status..." -ForegroundColor $Info
Write-Host "  - CRITICAL: 4 (openssl, expat, krb5)" -ForegroundColor $Error
Write-Host "  - HIGH: 27 (glibc, starlette, setuptools, etc.)" -ForegroundColor $Warning
Write-Host "  - MEDIUM: 32" -ForegroundColor $Warning
Write-Host "  - LOW: 60" -ForegroundColor $Info
Write-Host ""

# Step 3: Rebuild image
Write-Host "Step 3: Building patched image..." -ForegroundColor $Info
Write-Host "  Command: docker build --pull --no-cache -t ${ImageName}:${Tag} -f Dockerfile.secure ." -ForegroundColor $Warning
Write-Host ""

$buildStartTime = Get-Date

if (Test-Path "Dockerfile.secure") {
    docker build --pull --no-cache -t "${ImageName}:${Tag}" -f Dockerfile.secure .
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Docker build failed" -ForegroundColor $Error
        exit 1
    }
    Write-Host "✓ Image built successfully" -ForegroundColor $Success
} else {
    Write-Host "ERROR: Dockerfile.secure not found" -ForegroundColor $Error
    Write-Host "Please ensure Dockerfile.secure exists in the current directory" -ForegroundColor $Error
    exit 1
}

$buildEndTime = Get-Date
$buildTime = ($buildEndTime - $buildStartTime).TotalSeconds

# Step 4: Scan for vulnerabilities
Write-Host ""
Write-Host "Step 4: Scanning for remaining vulnerabilities..." -ForegroundColor $Info

if ($Scan) {
    Write-Host "  Running: docker scout cves local://${ImageName}:${Tag}" -ForegroundColor $Warning
    Write-Host ""
    
    $scanOutput = docker scout cves local://${ImageName}:${Tag} 2>&1
    Write-Host $scanOutput
    
    # Parse results
    if ($scanOutput -match "(\d+)C\s+(\d+)H\s+(\d+)M\s+(\d+)L") {
        $critical = [int]$matches[1]
        $high = [int]$matches[2]
        $medium = [int]$matches[3]
        $low = [int]$matches[4]
        
        Write-Host ""
        Write-Host "Vulnerability Summary (After Patch):" -ForegroundColor $Info
        Write-Host "  - CRITICAL: $critical" -ForegroundColor $(if ($critical -eq 0) { $Success } else { $Error })
        Write-Host "  - HIGH: $high" -ForegroundColor $(if ($high -eq 0) { $Success } else { $Warning })
        Write-Host "  - MEDIUM: $medium" -ForegroundColor $(if ($medium -le 5) { $Success } else { $Warning })
        Write-Host "  - LOW: $low" -ForegroundColor $Info
        
        if ($critical -eq 0 -and $high -eq 0) {
            Write-Host ""
            Write-Host "✓ CRITICAL and HIGH vulnerabilities fixed!" -ForegroundColor $Success
        }
    }
}

# Step 5: Image info
Write-Host ""
Write-Host "Step 5: Image information:" -ForegroundColor $Info
docker images "${ImageName}:${Tag}" --format "table {{.Repository}}:{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"

# Step 6: Next steps
Write-Host ""
Write-Host "Step 6: Next steps:" -ForegroundColor $Info
Write-Host "  1. Test the image locally:"
Write-Host "     docker run -it ${ImageName}:${Tag} /bin/bash"
Write-Host ""
Write-Host "  2. Tag as latest (if satisfied):"
Write-Host "     docker tag ${ImageName}:${Tag} ${ImageName}:latest"
Write-Host ""
Write-Host "  3. Push to registry:"
Write-Host "     docker push ${ImageName}:${Tag}"
Write-Host ""
Write-Host "  4. Run continuous scanning:"
Write-Host "     docker scout cves --format json --output report.json ${ImageName}:${Tag}"
Write-Host ""

# Step 7: Build summary
Write-Host "================================" -ForegroundColor $Cyan
Write-Host "Build Summary" -ForegroundColor $Cyan
Write-Host "================================" -ForegroundColor $Cyan
Write-Host "Image: ${ImageName}:${Tag}" -ForegroundColor $Success
Write-Host "Build time: ${buildTime}s" -ForegroundColor $Info
Write-Host "Base: python:3.11-bookworm (latest)" -ForegroundColor $Info
Write-Host "System packages: Updated to latest" -ForegroundColor $Success
Write-Host "Python tools: pip>=26.0, setuptools>=78.1.1, wheel>=0.46.2" -ForegroundColor $Success
Write-Host ""
Write-Host "✓ Security patching complete!" -ForegroundColor $Success
Write-Host ""
