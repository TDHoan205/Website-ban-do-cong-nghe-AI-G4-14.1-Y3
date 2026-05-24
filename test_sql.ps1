$ErrorActionPreference = "Stop"
try {
    $conn = New-Object System.Data.SqlClient.SqlConnection
    $conn.ConnectionString = "Server=localhost\SQLEXPRESS;Database=master;Trusted_Connection=True;TrustServerCertificate=True"
    $conn.Open()
    Write-Host "Connected to SQL Server successfully!"
    $conn.Close()
} catch {
    Write-Host "Error: $($_.Exception.Message)"
}
