Add-Type -AssemblyName System.Drawing
$outDir = "C:\Users\Administrator\Desktop\PinGPT\output\gemgen_batch"
$prefix = "ranpin"

# First, rename UUID files (no extension) to JPEG based on magic bytes, then convert to clean PNG
$counter = 1

# Process UUID files (no extension) first
$uuidFiles = Get-ChildItem $outDir -File | Where-Object { $_.Extension -eq '' } | Sort-Object LastWriteTime
foreach ($f in $uuidFiles) {
    Write-Host "Processing UUID file: $($f.Name) ($([math]::Round($f.Length / 1024))KB)"
    try {
        $srcImg = [System.Drawing.Image]::FromFile($f.FullName)
        $cleanBmp = New-Object System.Drawing.Bitmap($srcImg.Width, $srcImg.Height)
        $g = [System.Drawing.Graphics]::FromImage($cleanBmp)
        $g.DrawImage($srcImg, 0, 0, $srcImg.Width, $srcImg.Height)
        $g.Dispose()
        $srcImg.Dispose()
        
        # Find next available counter
        while (Test-Path (Join-Path $outDir "${prefix}_${counter}.png")) { $counter++ }
        
        $pngPath = Join-Path $outDir "${prefix}_${counter}.png"
        $cleanBmp.Save($pngPath, [System.Drawing.Imaging.ImageFormat]::Png)
        $cleanBmp.Dispose()
        Remove-Item $f.FullName
        Write-Host "  -> Saved as ${prefix}_${counter}.png"
        $counter++
    } catch {
        Write-Host "  -> ERROR: $_"
    }
}

# Process existing PNG files (strip metadata)
$pngFiles = Get-ChildItem $outDir -File -Filter "*.png" | Sort-Object LastWriteTime
foreach ($f in $pngFiles) {
    Write-Host "Stripping metadata from: $($f.Name)"
    try {
        $srcImg = [System.Drawing.Image]::FromFile($f.FullName)
        $cleanBmp = New-Object System.Drawing.Bitmap($srcImg.Width, $srcImg.Height)
        $g = [System.Drawing.Graphics]::FromImage($cleanBmp)
        $g.DrawImage($srcImg, 0, 0, $srcImg.Width, $srcImg.Height)
        $g.Dispose()
        $srcImg.Dispose()
        
        $tmpPath = Join-Path $outDir "tmp_clean.png"
        $cleanBmp.Save($tmpPath, [System.Drawing.Imaging.ImageFormat]::Png)
        $cleanBmp.Dispose()
        Remove-Item $f.FullName
        Rename-Item $tmpPath $f.Name
        Write-Host "  -> Done"
    } catch {
        Write-Host "  -> ERROR: $_"
    }
}

# Final report
$finalFiles = Get-ChildItem $outDir -File -Filter "*.png" | Sort-Object Name
Write-Host "`n=== FINAL FILES ==="
foreach ($f in $finalFiles) {
    $img = [System.Drawing.Image]::FromFile($f.FullName)
    Write-Host "  $($f.Name) - $($img.Width)x$($img.Height) - $([math]::Round($f.Length / 1024))KB"
    $img.Dispose()
}
Write-Host "Total: $($finalFiles.Count) images"
