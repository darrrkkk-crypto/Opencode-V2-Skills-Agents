# PDF conversion

Choose a converter that supports the source format and required layout quality. Another suitable tool may be used directly or as a fallback if the selected converter is unavailable, fails, or produces unsuitable output. The LibreOffice route below is one option.

Run conversion in the task's execution environment. Keep local files on the device unless the user requests a transfer to the cloud.

## LibreOffice option

LibreOffice can convert DOCX, XLSX, and PPTX to PDF. When choosing it, reuse an existing installation and the document's required fonts on the execution machine. The source document may have been created or edited with any suitable tool.

**Native desktop conversion needs no Docker.** LibreOffice runs directly on macOS, Windows, and Linux. Use the native installation on the user's computer; `--headless` performs conversion without opening its graphical interface. Microsoft Office, a browser, and a cloud conversion API are not prerequisites. Docker is a dependency of optional container services such as Gotenberg, not of this native LibreOffice workflow. If you choose this route and LibreOffice is missing, see [script-based setup](environment-setup.md#libreoffice).

1. **Locate LibreOffice and check its version.** Try `soffice --version`; if unresolved, follow [discovery and setup](environment-setup.md#libreoffice). Use the verified command for conversion. Preinstallation is a recommendation, not a guarantee about the execution machine.

2. **Save edits, then convert.** Save the source with the tool used to edit it. If an OfficeCLI resident holds pending edits, use the resolved OfficeCLI path (`save <file>` or `close <file>`) first. Substitute the actual source file below; the same conversion command accepts `.docx`, `.xlsx`, and `.pptx`:

   ```bash
   soffice --headless --convert-to pdf --outdir "./pdf-output" "report.docx"
   ```

   Use the LibreOffice command available in the execution environment; on Windows prefer `soffice.com` for console output. Python may invoke it with `subprocess`; LibreOffice must still be installed. Use a writable output directory and avoid collisions between inputs with the same filename stem. For CSV, prepare the table's print layout as needed; the [OfficeCLI import route](../xlsx.md#csv--bulk-import) is one way to create an XLSX workbook for conversion.

## Verify the generated PDF

For any chosen converter, confirm the expected PDF output was newly written and can be opened. Check required page count and text, then inspect rendered pages for clipping, font substitutions, and layout differences. A successful command alone is insufficient. If a conversion times out, inspect its job and output before retrying; stop only the job/process started for this conversion.

See [LibreOffice command-line parameters](https://help.libreoffice.org/latest/en-US/text/shared/guide/start_parameters.html) for conversion options and a separate writable `-env:UserInstallation=<file-URL>` profile when concurrent conversions or an existing LibreOffice instance require isolation.
