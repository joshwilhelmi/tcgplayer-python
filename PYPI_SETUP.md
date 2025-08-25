# PyPI Publishing Setup

This guide explains how to set up automatic PyPI publishing for the TCGplayer
Client package.

## 🚀 Quick Start

### 1. **Create PyPI Account**

- Go to [pypi.org](<https://pypi.org)> and create an account
- Verify your email address

### 2. **Generate API Token**

- Go to [PyPI Account Settings](<https://pypi.org/manage/account/)>
- Click "Add API token"
- Give it a name (e.g., "tcgplayer-client-automation")
- Select "Entire account (all projects)"
- Copy the token (it starts with `pypi-`)

### 3. **Configure GitHub Secrets**

- Go to your GitHub repository:
`<https://github.com/joshwilhelmi/tcgplayer-python>`
- Click "Settings" → "Secrets and variables" → "Actions"
- Click "New repository secret"
- Name: `PYPI_TOKEN`
- Value: Your PyPI API token (e.g., `pypi-...`)

## 🔄 How It Works

### **Automatic Publishing Flow**

1. **Create Release Tag**: `git tag v2.0.2`
2. **Push Tag**: `git push origin v2.0.2`
3. **GitHub Actions Trigger**: Automatically runs publish workflow
4. **Quality Checks**: Runs full CI pipeline
5. **Build Package**: Creates distribution files
6. **Publish to PyPI**: Automatically uploads to PyPI
7. **Create GitHub Release**: Creates release notes

### **Manual Publishing (if needed)**

```bash

# Build package

make build

# Publish to PyPI

twine upload dist/*

```

## 📋 Release Process

### **Option 1: Automated Release (Recommended)**

```bash
# 1. Ensure all changes are committed
git add . && git commit -m "Prepare for release v2.0.2"

# 2. Run automated release script
python scripts/release.py

# 3. The script will
#    - Run full CI pipeline
#    - Build package
#    - Create and push git tag
#    - Trigger automatic PyPI publishing
```

### **Option 2: Manual Release**

```bash
# 1. Run full CI locally
make ci

# 2. Build package
make build

# 3. Create git tag
git tag v2.0.2

# 4. Push tag (triggers GitHub Actions)
git push origin v2.0.2
```

### **Option 3: GitHub Release**

1. Go to GitHub repository
2. Click "Releases" → "Create a new release"
3. Tag version: `v2.0.2`
4. Release title: `Release v2.0.2`
5. Add release notes
6. Click "Publish release"

## 🔧 Configuration Files

### **GitHub Actions Workflow** (`.github/workflows/publish.yml`)

- Triggers on git tags (`v*`)
- Runs full CI pipeline
- Builds package
- Publishes to PyPI
- Creates GitHub release

### **Package Configuration** (`pyproject.toml`)

- Package metadata
- Dependencies
- Build configuration
- Already configured and ready!

### **Release Script** (`scripts/release.py`)

- Automated release process
- Pre-release validation
- Git tag management
- User confirmation

## 🚨 Troubleshooting

### **Common Issues**

#### **PyPI Authentication Failed**

```text
HTTPError: 403 Client Error: Invalid or non-existent authentication information
```

**Solution**: Check that `PYPI_TOKEN` is correctly set in GitHub Secrets

#### **Package Already Exists**

```text
HTTPError: 400 Client Error: File already exists
```

**Solution**: Increment version number in `tcgplayer_client/__init__.py`

#### **Build Failed**

```text
ERROR: Failed building wheel for tcgplayer_client
```

**Solution**: Run `make ci` locally to catch issues before tagging

#### **GitHub Actions Not Triggered**

**Solution**: Ensure you're pushing a tag that matches the pattern `v*` (e.g.,
`v2.0.2`)

### **Debugging Steps**

1. **Check GitHub Actions**: Go to Actions tab in repository
2. **Check Secrets**: Verify `PYPI_TOKEN` is set
3. **Check Tag Format**: Ensure tag starts with `v` (e.g., `v2.0.2`)
4. **Check Local Build**: Run `make build` locally first

## 📊 Monitoring

### **GitHub Actions**

- URL: `<https://github.com/joshwilhelmi/tcgplayer-python/actions>`
- Shows publish workflow status
- Logs for debugging

### **PyPI**

- URL: `<https://pypi.org/project/tcgplayer-client/>`
- Shows published versions
- Download statistics

### **GitHub Releases**

- URL: `<https://github.com/joshwilhelmi/tcgplayer-python/releases>`
- Shows release notes
- Download links

## 🔒 Security

### **API Token Security**

- **Never commit** PyPI tokens to code
- Use GitHub Secrets for secure storage
- Rotate tokens periodically
- Use least-privilege access

### **Package Verification**

- All packages are built from source code
- CI pipeline ensures quality
- No external dependencies in build process

## 📈 Best Practices

### **Version Management**

- Use semantic versioning (e.g., `2.0.2`)
- Update version in `tcgplayer_client/__init__.py`
- Tag releases with `v` prefix
- Keep changelog updated

### **Release Process**

- Always run `make ci` before releasing
- Test package installation locally
- Review release notes
- Monitor GitHub Actions progress

### **Quality Assurance**

- All tests must pass
- Code formatting must be correct
- Type checking must pass
- Security scanning must pass

## 🎯 Next Steps

1. **Set up PyPI account** and API token
2. **Configure GitHub Secrets** with your token
3. **Test the workflow** with a small version bump
4. **Monitor the process** to ensure everything works
5. **Celebrate** your first automatic PyPI release! 🎉

---

**Need Help?** Check the GitHub Actions logs or run `make help` for available
commands.
