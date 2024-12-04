# Servidor web para la creación de certificados SSL con una CA

## Añadir CA Windows dede PowerShell
Import-Certificate -FilePath "C:\ruta\a\tu\certificado\ca.crt" -CertStoreLocation "Cert:\LocalMachine\Root"