# Restaurar app-ads.txt de Veltora Studio.
# Compatible con Windows PowerShell 5.1. Pega el bloque completo.
$adsOldErrorAction = $ErrorActionPreference
$adsOldTls = [Net.ServicePointManager]::SecurityProtocol
$ErrorActionPreference = 'Stop'

function Test-VeltoraAppAds([string]$Url, [string]$Expected) {
    try {
        $adsResponse = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 10
        return ($adsResponse.StatusCode -eq 200 -and ([string]$adsResponse.Content).Trim() -eq $Expected)
    } catch {
        return $false
    }
}

try {
    [Net.ServicePointManager]::SecurityProtocol = $adsOldTls -bor [Net.SecurityProtocolType]::Tls12
    $adsLine = 'google.com, pub-1246957925783081, DIRECT, f08c47fec0942fa0'
    $adsUrl = 'https://frankyx1991.github.io/app-ads.txt'
    $adsRepoName = 'frankyx1991.github.io'
    $adsRepoUrl = 'https://github.com/Frankyx1991/' + $adsRepoName
    $adsReady = Test-VeltoraAppAds $adsUrl $adsLine

    if (-not $adsReady) {
        $adsFolder = Join-Path $env:USERPROFILE ('VeltoraStudio-AppAds\' + (Get-Date -Format 'yyyyMMdd-HHmmss') + '-' + [guid]::NewGuid().ToString('N').Substring(0,8))
        New-Item -ItemType Directory -Path $adsFolder -Force | Out-Null
        $adsEncoding = New-Object System.Text.UTF8Encoding($false)
        [IO.File]::WriteAllText((Join-Path $adsFolder 'app-ads.txt'), $adsLine + [Environment]::NewLine, $adsEncoding)
        $adsIndex = @'
<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Veltora Studio</title>
<meta http-equiv="refresh" content="0;url=https://frankyx1991.github.io/veltorastudio/">
<link rel="canonical" href="https://frankyx1991.github.io/veltorastudio/">
</head>
<body>
<p><a href="https://frankyx1991.github.io/veltorastudio/">Entrar en Veltora Studio</a></p>
</body>
</html>
'@
        [IO.File]::WriteAllText((Join-Path $adsFolder 'index.html'), $adsIndex, $adsEncoding)
        Write-Host "Archivos preparados en: $adsFolder" -ForegroundColor Green
        Start-Process -FilePath explorer.exe -ArgumentList ('"' + $adsFolder + '"')

        Write-Host 'PASO 1: en GitHub crea un repositorio con estos datos:' -ForegroundColor Cyan
        Write-Host '  Owner: Frankyx1991'
        Write-Host "  Repository name: $adsRepoName"
        Write-Host '  Visibility: Public'
        Write-Host '  Add README: activado'
        Write-Host '  Pulsa Create repository. Si ya existe, abre ese repositorio.'
        Start-Process 'https://github.com/new'
        [void](Read-Host 'Cuando el repositorio este creado y tenga README, pulsa Intro aqui')

        Write-Host 'PASO 2: sube app-ads.txt e index.html desde la carpeta abierta.' -ForegroundColor Cyan
        Write-Host 'Selecciona los dos archivos, sin una carpeta que los contenga.'
        Write-Host 'Guarda con Commit changes en la rama main.'
        Start-Process ($adsRepoUrl + '/upload/main')
        [void](Read-Host 'Cuando los dos archivos esten guardados en GitHub, pulsa Intro aqui')

        Write-Host 'PASO 3: configura GitHub Pages:' -ForegroundColor Cyan
        Write-Host '  Source: Deploy from a branch'
        Write-Host '  Branch: main'
        Write-Host '  Folder: / (root)'
        Write-Host '  Pulsa Save.'
        Start-Process ($adsRepoUrl + '/settings/pages')
        [void](Read-Host 'Despues de pulsar Save, vuelve aqui y pulsa Intro')

        Write-Host 'Comprobando el archivo publico; GitHub puede tardar unos minutos...'
        for ($adsAttempt = 1; $adsAttempt -le 36 -and -not $adsReady; $adsAttempt++) {
            $adsReady = Test-VeltoraAppAds $adsUrl $adsLine
            if (-not $adsReady) {
                if ($adsAttempt % 6 -eq 0) {
                    Write-Host 'Publicacion todavia pendiente. Los archivos locales estan guardados.'
                }
                Start-Sleep -Seconds 5
            }
        }
    }

    if ($adsReady) {
        Write-Host "ARCHIVO PUBLICADO Y COMPROBADO: $adsUrl" -ForegroundColor Green
        Start-Process $adsUrl
        Write-Host 'En AdMob: Aplicaciones > Ver todas las aplicaciones > app-ads.txt > Buscar actualizaciones.'
        Write-Host 'La comprobacion de AdMob puede tardar hasta 24 horas.'
    } else {
        Write-Host 'No se ha podido confirmar la publicacion. Comprueba Pages mas tarde.' -ForegroundColor Yellow
        Write-Host "Direccion que debe mostrar la linea de Google: $adsUrl"
        Write-Host "Ajustes: $adsRepoUrl/settings/pages"
    }
} catch {
    Write-Host ('PROCESO DETENIDO: ' + $_.Exception.Message) -ForegroundColor Red
} finally {
    [Net.ServicePointManager]::SecurityProtocol = $adsOldTls
    $ErrorActionPreference = $adsOldErrorAction
}
