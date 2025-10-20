# Script to create database and run migrations

Write-Host "============================================" -ForegroundColor Cyan
Write-Host " Student Management System - Setup Script" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Create database
Write-Host "[STEP 1] Creating MySQL database..." -ForegroundColor Yellow
Write-Host "Please run this SQL command in your MySQL/PhpMyAdmin:" -ForegroundColor Green
Write-Host ""
Write-Host "CREATE DATABASE student_management_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" -ForegroundColor White
Write-Host ""
Write-Host "After creating the database, press Enter to continue..." -ForegroundColor Yellow
Read-Host

# Step 2: Activate virtual environment
Write-Host "[STEP 2] Activating virtual environment..." -ForegroundColor Yellow
.\.venv\Scripts\activate

# Step 3: Run migrations
Write-Host "[STEP 3] Running migrations..." -ForegroundColor Yellow
python manage.py migrate

# Step 4: Import sample data (optional)
Write-Host ""
Write-Host "[STEP 4] Do you want to import sample data from database_xampp.sql? (Y/N)" -ForegroundColor Yellow
$import = Read-Host

if ($import -eq "Y" -or $import -eq "y") {
    Write-Host "Please import database_xampp.sql using PhpMyAdmin or MySQL command line:" -ForegroundColor Green
    Write-Host "mysql -u root -p student_management_system < database_xampp.sql" -ForegroundColor White
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Setup completed!" -ForegroundColor Green
Write-Host "Run: python manage.py runserver" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Cyan
