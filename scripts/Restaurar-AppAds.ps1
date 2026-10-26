# Comprobar app-ads.txt de Veltora Studio en Cloudflare Pages.
# Pega el bloque completo en Windows PowerShell 5.1 o superior.
$adsOldErrorAction = $ErrorActionPreference
$adsOldTls = [Net.ServicePointManager]::SecurityProtocol
$ErrorActionPreference = 'Stop'

try {
    [Net.ServicePointManager]::SecurityProtocol = $adsOldTls -bor [Net.SecurityProtocolType]::Tls12
    $adsWebsite = 'https://veltorastudio.pages.dev/'
    $adsUrl = $adsWebsite + 'app-ads.txt'
    $adsExpected = 'google.com, pub-1246957925783081, DIRECT, f08c47fec0942fa0'
    $adsResponse = Invoke-WebRequest -Uri $adsUrl -UseBasicParsing -TimeoutSec 20
    if ($adsResponse.StatusCode -ne 200) {
        throw 'El servidor no ha devuelto el archivo correctamente.'
    }
    $adsLines = [regex]::Split([string]$adsResponse.Content, '\r?\n') | ForEach-Object { $_.Trim() }
    if ($adsLines -notcontains $adsExpected) {
        throw 'El archivo no contiene la linea correcta de tu cuenta de AdMob.'
    }

    Write-Host "ARCHIVO ACCESIBLE Y CONTENIDO CORRECTO: $adsUrl" -ForegroundColor Green
    Write-Host "Web del desarrollador para Google Play: $adsWebsite"
    Write-Host 'En AdMob: Aplicaciones > Ver todas las aplicaciones > app-ads.txt > Buscar actualizaciones.'
    Write-Host 'Esta comprobacion confirma el archivo publico. La verificacion de AdMob se consulta en su panel.'
    Start-Process $adsUrl
} catch {
    Write-Host ('COMPROBACION PENDIENTE: ' + $_.Exception.Message) -ForegroundColor Yellow
    Write-Host 'Comprueba que Cloudflare haya terminado el despliegue y que la direccion del proyecto sea la correcta.'
} finally {
    [Net.ServicePointManager]::SecurityProtocol = $adsOldTls
    $ErrorActionPreference = $adsOldErrorAction
}
