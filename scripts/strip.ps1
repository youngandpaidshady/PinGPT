Add-Type -AssemblyName System.Drawing
$outDir = "C:\Users\Administrator\Desktop\PinGPT\output\gemgen_batch"

$counter = 1
Get-ChildItem $outDir -File | Where-Object { $_.Extension -eq '.png' } | Sort-Object LastWriteTime | ForEach-Object {
    $srcImg = [System.Drawing.Image]::FromFile($_.FullName)
    $cleanBmp = New-Object System.Drawing.Bitmap($srcImg.Width, $srcImg.Height)
    $g = [System.Drawing.Graphics]::FromImage($cleanBmp)
    $g.DrawImage($srcImg, 0, 0, $srcImg.Width, $srcImg.Height)
    $g.Dispose()
    $srcImg.Dispose()
    
    $pngPath = Join-Path $outDir "clean_${counter}.png"
    $cleanBmp.Save($pngPath, [System.Drawing.Imaging.ImageFormat]::Png)
    $cleanBmp.Dispose()
    
    $oldName = $_.Name
    Remove-Item $_.FullName
    Rename-Item -Path $pngPath -NewName $oldName
    $counter++
}
Write-Host "Metadata stripped."
