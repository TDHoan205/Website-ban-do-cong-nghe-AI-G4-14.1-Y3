$ErrorActionPreference = "Stop"
try {
    $conn = New-Object System.Data.SqlClient.SqlConnection
    $conn.ConnectionString = "Server=localhost\SQLEXPRESS;Database=master;Trusted_Connection=True;TrustServerCertificate=True"
    $conn.Open()

    $cmd = $conn.CreateCommand()
    $cmd.CommandText = "SELECT name FROM sys.databases WHERE name = 'TechShopWebsite2'"
    $reader = $cmd.ExecuteReader()
    if ($reader.Read()) {
        Write-Host "Database 'TechShopWebsite2' EXISTS"
        $reader.Close()

        $cmd2 = $conn.CreateCommand()
        $cmd2.CommandText = "USE TechShopWebsite2; SELECT COUNT(*) AS TableCount FROM INFORMATION_SCHEMA.TABLES"
        $count = $cmd2.ExecuteScalar()
        Write-Host "Number of tables: $count"
    } else {
        Write-Host "Database 'TechShopWebsite2' does NOT exist yet"
    }

    $conn.Close()
} catch {
    Write-Host "Error: $($_.Exception.Message)"
}
