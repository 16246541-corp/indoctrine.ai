# Publishing Guide for indoctrine.ai

This guide details how to build, verify, and publish the `indoctrine.ai` package to PyPI and Homebrew.

## Prerequisites

Ensure you have the following tools installed:

```bash
pip install build twine
brew install brew-create-formula
```

## 1. Build the Package

Clean previous builds and generate the distribution archives:

```bash
rm -rf dist/
python3 -m build
```

This will create `dist/indoctrine.ai-0.1.0-py3-none-any.whl` and `dist/indoctrine.ai-0.1.0.tar.gz`.

## 2. Publish to PyPI

### TestPyPI (Optional but Recommended)

Upload to TestPyPI first to verify everything looks correct:

```bash
python3 -m twine upload --repository testpypi dist/*
```

### Production PyPI

When ready, upload to the real PyPI:

```bash
python3 -m twine upload dist/*
```

## 3. Publish to Homebrew

To allow users to install via `brew install indoctrine.ai`, you need to create a Homebrew formula.

1.  **Get the SHA256 checksum** of the tarball hosted on PyPI (after step 2):

    ```bash
    curl -sL https://pypi.io/packages/source/i/indoctrine.ai/indoctrine.ai-0.1.0.tar.gz | shasum -a 256
    ```

2.  **Create/Update the Formula**:

    Create a file named `indoctrine.ai.rb`:

    ```ruby
    class IndoctrineAi < Formula
      include Language::Python::Virtualenv

      desc "The Open-Source Framework for Agentic Ethics & AI Agent Values"
      homepage "https://github.com/16246541-corp/indoctrine.ai"
      url "https://pypi.io/packages/source/i/indoctrine.ai/indoctrine.ai-0.1.0.tar.gz"
      sha256 "<INSERT_SHA256_HERE>"
      license "MIT"

      depends_on "python@3.10"

      def install
        virtualenv_install_with_resources
      end

      test do
        system "#{bin}/indoctrinate", "--version"
      end
    end
    ```

3.  **Push to a Tap**:

    Create a new repository called `homebrew-tap` in your GitHub organization, add this file, and push it. Users can then install via:

    ```bash
    brew tap 16246541-corp/tap
    brew install indoctrine.ai
    ```

## 4. Git Release

Tag the release in git:

```bash
git tag v0.1.0
git push origin v0.1.0
```
