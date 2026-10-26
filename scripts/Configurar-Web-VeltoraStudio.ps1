# Veltora Studio: copia local y comprobacion de GitHub Pages.
# Pega el bloque completo en Windows PowerShell 5.1 o superior.
$veltoraOldErrorAction = $ErrorActionPreference
$veltoraOldTls = [Net.ServicePointManager]::SecurityProtocol
$ErrorActionPreference = 'Stop'

function Test-VeltoraPublicada([string]$Url, [string]$Release) {
    try {
        $veltoraResponse = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 12
        $veltoraMarker = '<meta name="veltora-release" content="' + $Release + '">'
        return $veltoraResponse.StatusCode -eq 200 -and $veltoraResponse.Content.Contains($veltoraMarker)
    } catch {
        return $false
    }
}

try {
    [Net.ServicePointManager]::SecurityProtocol = $veltoraOldTls -bor [Net.SecurityProtocolType]::Tls12
    $veltoraUrl = 'https://frankyx1991.github.io/veltorastudio/'
    $veltoraSettings = 'https://github.com/Frankyx1991/veltorastudio/settings/pages'
    $veltoraArchive = 'https://github.com/Frankyx1991/veltorastudio/archive/refs/heads/main.zip'
    $veltoraFolder = Join-Path $env:USERPROFILE ('VeltoraStudio-Web\' + (Get-Date -Format 'yyyyMMdd-HHmmss') + '-' + [guid]::NewGuid().ToString('N').Substring(0,8))
    New-Item -ItemType Directory -Path $veltoraFolder -Force | Out-Null
    $veltoraZip = Join-Path $veltoraFolder 'VeltoraStudio-Web.zip'

    Write-Host 'Descargando la web desde el nuevo repositorio...' -ForegroundColor Cyan
    Invoke-WebRequest -Uri $veltoraArchive -OutFile $veltoraZip -UseBasicParsing -TimeoutSec 90
    Expand-Archive -LiteralPath $veltoraZip -DestinationPath $veltoraFolder
    $veltoraSource = Get-ChildItem -LiteralPath $veltoraFolder -Directory | Where-Object {
        Test-Path -LiteralPath (Join-Path $_.FullName 'data\studio.json') -PathType Leaf
    } | Select-Object -First 1
    if (-not $veltoraSource) {
        throw 'No se encuentra la estructura completa de la web en el ZIP.'
    }
    $veltoraConfig = Get-Content -LiteralPath (Join-Path $veltoraSource.FullName 'data\studio.json') -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($veltoraConfig.repository -ne 'Frankyx1991/veltorastudio' -or $veltoraConfig.repository_id -ne 1434680925) {
        throw 'El archivo no corresponde al nuevo repositorio de Veltora Studio.'
    }
    Write-Host "Copia completa guardada en: $($veltoraSource.FullName)" -ForegroundColor Green

    $veltoraReady = Test-VeltoraPublicada $veltoraUrl $veltoraConfig.release
    if (-not $veltoraReady) {
        Write-Host 'Falta activar o terminar la publicacion de GitHub Pages.' -ForegroundColor Yellow
        Write-Host 'Se abriran los ajustes del repositorio. Si lo solicita, inicia sesion en GitHub.'
        Write-Host 'En Build and deployment selecciona:'
        Write-Host '  Source: Deploy from a branch'
        Write-Host '  Branch: main'
        Write-Host '  Folder: / (root)'
        Write-Host 'Pulsa Save. Esta ventana comprobara la publicacion durante unos minutos.'
        Start-Process $veltoraSettings
        for ($veltoraAttempt = 1; $veltoraAttempt -le 60 -and -not $veltoraReady; $veltoraAttempt++) {
            Start-Sleep -Seconds 5
            $veltoraReady = Test-VeltoraPublicada $veltoraUrl $veltoraConfig.release
            if (-not $veltoraReady -and $veltoraAttempt % 6 -eq 0) {
                Write-Host 'GitHub Pages todavia esta pendiente. La copia local ya esta guardada.'
            }
        }
    }

    if ($veltoraReady) {
        Write-Host "WEB PUBLICADA Y COMPROBADA: $veltoraUrl" -ForegroundColor Green
        Start-Process $veltoraUrl
    } else {
        Write-Host 'La publicacion sigue pendiente; GitHub puede tardar mas tiempo.' -ForegroundColor Yellow
        Write-Host "Comprueba despues: $veltoraUrl"
        Write-Host "Ajustes de publicacion: $veltoraSettings"
    }

    $veltoraRootAds = 'https://frankyx1991.github.io/app-ads.txt'
    try {
        $veltoraAds = Invoke-WebRequest -Uri $veltoraRootAds -UseBasicParsing -TimeoutSec 12
        if ($veltoraAds.StatusCode -ne 200 -or $veltoraAds.Content.Trim() -ne 'google.com, pub-1246957925783081, DIRECT, f08c47fec0942fa0') {
            throw 'Contenido app-ads.txt distinto al esperado.'
        }
        Write-Host 'app-ads.txt disponible en la raiz del dominio.' -ForegroundColor Green
    } catch {
        Write-Host "AdMob: falta restaurar el archivo en $veltoraRootAds" -ForegroundColor Yellow
        Write-Host 'El nuevo repositorio incluye el archivo y una carpeta infrastructure/domain-root preparada para esa ruta.'
    }
} catch {
    Write-Host ('PROCESO DETENIDO: ' + $_.Exception.Message) -ForegroundColor Red
} finally {
    [Net.ServicePointManager]::SecurityProtocol = $veltoraOldTls
    $ErrorActionPreference = $veltoraOldErrorAction
}
