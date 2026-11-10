# Mở báo cáo bằng Microsoft Word, cập nhật mục lục + danh mục hình/bảng, lưu lại và xuất PDF.
# Chạy (PowerShell): powershell -ExecutionPolicy Bypass -File docs\report\finalize_report.ps1 [-Pdf]
param([switch]$Pdf)
$ErrorActionPreference = "Stop"
$docx = Join-Path $PSScriptRoot "BaoCao_DoAn_SANCTUARY.docx"
$pdfPath = Join-Path $PSScriptRoot "BaoCao_DoAn_SANCTUARY.pdf"
# File khoá "~$..." còn sót (Word bị tắt ngang) làm Word mở file ở chế độ chỉ đọc -> xoá trước
$lock = Join-Path $PSScriptRoot ("~$" + (Split-Path $docx -Leaf).Substring(2))
if (Test-Path -LiteralPath $lock) { Remove-Item -LiteralPath $lock -Force }
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    # Open(file, ConfirmConversions=false, ReadOnly=false, AddToRecentFiles=false)
    $doc = $word.Documents.Open($docx, $false, $false, $false)
    if ($doc.ReadOnly) { throw "File dang mo o che do chi doc (co the dang mo trong Word). Hay dong file roi chay lai." }
    Write-Output "Opened"
    # Cập nhật 2 lần: lần 1 tạo mục lục (số trang có thể đổi), lần 2 cập nhật lại số trang cho đúng
    for ($k = 0; $k -lt 2; $k++) {
        foreach ($toc in $doc.TablesOfContents) { $toc.Update() }
        $doc.Fields.Update() | Out-Null
        $doc.Repaginate()
        Write-Output "Updated pass $($k + 1)"
    }
    $pages = $doc.Content.Information(4)    # 4 = wdNumberOfPagesInDocument
    Write-Output "Pages: $pages"
    # File do python-docx tạo ở chế độ tương thích (Word 2010): nâng lên chế độ Word hiện tại (15) rồi lưu .docx trước
    $doc.SetCompatibilityMode(15)
    $doc.Save()
    Write-Output "Saved"
    # Xuất PDF chỉ khi chạy kèm -Pdf (trên một số máy, xuất PDF từ Word ẩn bị treo; khi đó mở file bằng Word
    # rồi chọn File > Save As > PDF)
    if ($Pdf) {
        $doc.ExportAsFixedFormat($pdfPath, 17, $false, 0)
        Write-Output "Exported PDF"
    }
    $doc.Close([ref]0)
    Write-Output "Saved: $docx"
    if ($Pdf) { Write-Output "PDF:   $pdfPath" }
} finally {
    $word.Quit()
}
