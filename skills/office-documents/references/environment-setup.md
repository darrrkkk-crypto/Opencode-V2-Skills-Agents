# Environment setup and reuse

Use this reference when you choose to set up one of the documented tools or reuse its dependencies across sessions. Another suitable tool may be used instead. Run detection and installation on the machine that will execute the document task.

## Reuse before installing

1. Probe without failing the whole command. Do **not** chain `officecli --version` or `officecli help ...` onto a missing binary in the same shell line. For OfficeCLI, resolve a working path as below. For LibreOffice, `command -v soffice || true` (on Windows prefer `soffice.com`).
2. Reuse a working installation that meets the task's requirements. Install only a missing dependency; repair or upgrade only when the task requires it. Loading a skill or starting a new session does not itself require installing software.
3. After installation, re-run the probe and verify **that path** with `--version` before document commands. If the new binary is not on `PATH`, keep using the absolute path. A stale `PATH` is not a reason to reinstall.

Let official installers and package managers choose and manage installation locations. Reuse their installation in the same environment (OS and OS user) across sessions. A previous task's shell activation or temporary environment is not a reusable installation; neither is an installation on a different computer, in a different cloud container, or across Windows host vs WSL.

## OfficeCLI

Do not call a bare `officecli` until a probe for the **current OS** has printed a working absolute path. Probe by OS; invoke by shell. Later commands may run in a new shell, so copy that printed path literally (or re-run the probe). Do not assume a `$CLI` variable survives.

Decide the OS with `uname -s` (the same test `install.sh` uses). Do not infer the current shell from `uname`. This table is the only probe-routing source:

- `Linux` → Linux/WSL: bash probe and `install.sh`. Install the Linux build into `$HOME/.local/bin`. `uname -r` containing `microsoft`/`WSL` only confirms WSL; it does not change the branch. Do not reuse a Win32 `officecli.exe`.
- `Darwin` → macOS: bash probe and `install.sh`.
- `MINGW*` / `MSYS*` / `CYGWIN*` → native Windows: PowerShell probe and `install.ps1`. If the current shell is not already PowerShell, run the probe with `powershell -NoProfile -Command`. `uname` can also come from Git on PATH inside PowerShell or cmd; that does not mean you are in Git Bash. Do not run `install.sh`; it exits on `mingw64_nt-*`.
- no `uname` → native Windows PowerShell or cmd: PowerShell probe and `install.ps1`.
- any other `uname -s` → this skill does not cover that OS; switch to another suitable tool.

- **Invoke:** quote the printed path. PowerShell needs `& "C:\...\officecli.exe" …`. Git Bash must not use `&`; convert to a forward-slash path such as `"/c/Users/you/AppData/Local/OfficeCLI/officecli.exe" …`. cmd quotes the Windows path and does not use `&`.
- Format-guide recipes (heredocs, `$(…)`, pipelines) assume a POSIX shell. On native Windows, run those in Git Bash after probing. WSL is not a Windows fallback: probe and install there as Linux.

**1. Probe (this command must succeed even when OfficeCLI is missing).**

macOS / Linux:

```bash
CLI=""
for p in \
  "$(command -v officecli || true)" \
  "$HOME/.local/bin/officecli" \
  "$HOME/.officecli/bin/officecli" \
  /opt/homebrew/bin/officecli \
  /usr/local/bin/officecli
do
  [ -n "$p" ] || continue
  if [ -x "$p" ] && "$p" --version >/dev/null 2>&1; then
    CLI="$p"
    break
  fi
done
printf 'CLI=%s\n' "${CLI:-}"
```

Windows (PowerShell):

```powershell
$CLI = ''
$candidates = @()
$cmd = Get-Command officecli, officecli.exe -ErrorAction SilentlyContinue | Select-Object -First 1
if ($cmd) { $candidates += $cmd.Source }
if ($env:LOCALAPPDATA) {
  $candidates += (Join-Path $env:LOCALAPPDATA 'OfficeCLI\officecli.exe')
}
foreach ($p in $candidates) {
  if (-not $p) { continue }
  if (-not (Test-Path -LiteralPath $p)) { continue }
  $code = -1
  try {
    & $p --version *> $null
    $code = $LASTEXITCODE
  } catch {
    $code = -1
  }
  if ($code -eq 0) {
    $CLI = $p
    break
  }
}
Write-Output ("CLI={0}" -f $CLI)
```

If the printed `CLI=` line is non-empty, skip to step 3. An empty probe means the binary is not installed in a known location. `command not found` / exit 127 on a later bare `officecli` is the same signal: continue setup or switch tools; it is not a device-offline failure. If a candidate exists but `--version` fails, do not reuse that file — run the official installer.

**2. If the probe printed empty and setup is in scope, run the official installer, then re-run step 1.** The installer places the binary in a stable location such as `$HOME/.local/bin` (Unix) or `$env:LOCALAPPDATA\OfficeCLI` (Windows); both are already in the matching probe list. Do not download a second copy into the task directory, and do not depend on the installer mutating this shell's `PATH`.

```bash
# macOS / Linux
curl -fsSL https://d.officecli.ai/install.sh | bash
```

```powershell
# Windows
irm https://d.officecli.ai/install.ps1 | iex
```

The Windows script deploys the native CLI executable without a graphical EXE setup wizard. These scripts download releases when run, so execute them conditionally rather than in every session. Sources: [Unix installer](https://raw.githubusercontent.com/iOfficeAI/OfficeCLI/main/install.sh), [PowerShell installer](https://d.officecli.ai/install.ps1). If the installer fails or step 1 is still empty afterward, switch to another suitable tool instead of retrying `officecli`.

On first install the official scripts may copy an upstream `officecli` skill into other agent skill directories that already exist on the machine. That copy starts with a bare `officecli --version`. When this Manus skill is in use, follow this document and ignore that co-located skill; do not delete it.

**3. Invoke only via the printed absolute path.** Choose the form for the **current shell**, not the OS:

```bash
# POSIX (macOS, Linux, WSL)
"/Users/you/.local/bin/officecli" help pptx table
```

```bash
# Git Bash (Win32 path, forward slashes; do not use &)
"/c/Users/you/AppData/Local/OfficeCLI/officecli.exe" help pptx table
```

```powershell
# PowerShell
& "C:\Users\you\AppData\Local\OfficeCLI\officecli.exe" help pptx table
```

cmd:

```
"C:\Users\you\AppData\Local\OfficeCLI\officecli.exe" help pptx table
```

Format-guide examples that write `officecli ...` mean that invocation. On native Windows, run those POSIX recipes in Git Bash. Do not take a Win32 binary into WSL. If the next command is a new shell, paste the same path or re-run step 1; an empty `"$CLI"` is worse than a bare `officecli` on a machine that already has it on `PATH`.

## LibreOffice

When choosing LibreOffice, reuse an available `soffice` command; on Windows prefer `soffice.com` for console output. If it needs installation, use the command-line route within the authorized setup scope. Provision the document's required fonts when preparing the environment.

macOS with [Homebrew](https://formulae.brew.sh/cask/libreoffice):

```bash
brew install --cask libreoffice
```

Debian/Ubuntu, with the required package-management privileges:

```bash
apt-get update
apt-get install -y libreoffice
```

Use the corresponding native package manager on other Linux distributions. Managed cloud environments can provision LibreOffice in their image for reuse.

Windows with winget:

```powershell
winget install --id TheDocumentFoundation.LibreOffice --exact --source winget --silent --disable-interactivity --accept-package-agreements --accept-source-agreements
```

WinGet selects the installer and declared prerequisites. Silent mode suppresses installer UI; machine installation may still require administrator elevation. See [WinGet installation options](https://learn.microsoft.com/en-us/windows/package-manager/winget/install).

If winget is unavailable, use PowerShell to download the matching MSI from the [official LibreOffice site](https://www.libreoffice.org/download/), verify it, and invoke `msiexec /i <downloaded-msi> /qn /norestart`. Wait for completion and check the result before verifying LibreOffice. Report missing privileges or a required restart instead of repeatedly reinstalling. See [msiexec options](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/msiexec).

Script-based setup still installs the native software and its prerequisites; it removes the need to manually click through an installation wizard. LibreOffice's Windows MSI is managed by the [package manifest](https://github.com/microsoft/winget-pkgs/tree/master/manifests/t/TheDocumentFoundation/LibreOffice).

## Additional Python or Node libraries

OfficeCLI editing and native LibreOffice conversion do not require a Python or Node wrapper. Install additional libraries only when the document workflow uses them.

For cross-session reuse, use a persistent environment with a known interpreter and compatible dependencies, preferably one provided by the host. Invoke that environment explicitly and check required imports before installing packages again. Keep incompatible dependency sets separate. A package download cache and a previous shell's venv activation do not establish that a new session has a working environment.
