@echo off
chcp 65001 >nul 2>&1
setlocal EnableDelayedExpansion

:: ============================================================
:: AUTO-TRANSFER.BAT
:: Git avtomatik o'rnatish va fayllarni ko'chirish skripti
:: Foydalanuvchi faqat ikki marta bosadi - hamma narsa avtomatik
:: ============================================================

title Auto Transfer - Git O'rnatish va Fayllarni Ko'chirish

color 0A

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║         AUTO TRANSFER - AVTOMATIK KO'CHIRISH                ║
echo ║                                                              ║
echo ║  1. Git tekshiriladi va kerak bo'lsa o'rnatiladi             ║
echo ║  2. Manba repo klonlanadi                                    ║
echo ║  3. .git o'chiriladi va yangi init qilinadi                  ║
echo ║  4. Manzil repoga push qilinadi                              ║
echo ║                                                              ║
echo ║  Manba:  tangriyevafotima0-crypto/Portfolio-Fayllar-         ║
echo ║  Manzil: zafarbekjamolovsl-art/Portfolio-FAYLLAR-            ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: ============================================================
:: KONFIGURATSIYA
:: ============================================================
set "SOURCE_REPO=https://github.com/tangriyevafotima0-crypto/Portfolio-Fayllar-.git"
set "TARGET_REPO=https://github.com/zafarbekjamolovsl-art/Portfolio-FAYLLAR-.git"
set "WORK_DIR=%TEMP%\auto-transfer-%RANDOM%"
set "GIT_INSTALLER=%TEMP%\git-installer.exe"
set "GIT_DOWNLOAD_URL=https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe"

:: ============================================================
:: 1-QADAM: GIT MAVJUDLIGINI TEKSHIRISH
:: ============================================================
echo [1/5] Git tekshirilmoqda...
echo.

:: Avval PATH dagi git ni tekshirish
where git >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo      [OK] Git allaqachon o'rnatilgan!
    goto :git_ready
)

:: Standart joylarda qidirish
if exist "C:\Program Files\Git\bin\git.exe" (
    set "PATH=%PATH%;C:\Program Files\Git\bin"
    echo      [OK] Git topildi: C:\Program Files\Git\bin
    goto :git_ready
)
if exist "C:\Program Files (x86)\Git\bin\git.exe" (
    set "PATH=%PATH%;C:\Program Files (x86)\Git\bin"
    echo      [OK] Git topildi: C:\Program Files (x86)\Git\bin
    goto :git_ready
)
if exist "%LOCALAPPDATA%\Programs\Git\bin\git.exe" (
    set "PATH=%PATH%;%LOCALAPPDATA%\Programs\Git\bin"
    echo      [OK] Git topildi: %LOCALAPPDATA%\Programs\Git\bin
    goto :git_ready
)

:: Git topilmadi - o'rnatish kerak
echo      [!] Git topilmadi! Avtomatik o'rnatish boshlanmoqda...
echo.

:: ============================================================
:: GIT O'RNATISH (3 ta metod)
:: ============================================================
echo      Git o'rnatilmoqda... Bu bir necha daqiqa vaqt olishi mumkin.
echo.

:: --- Metod 1: winget bilan o'rnatish ---
echo      [Metod 1] winget bilan sinab ko'rilmoqda...
where winget >nul 2>&1
if !ERRORLEVEL! EQU 0 (
    echo      winget topildi, Git o'rnatilmoqda...
    winget install --id Git.Git -e --source winget --accept-package-agreements --accept-source-agreements >nul 2>&1
    if !ERRORLEVEL! EQU 0 (
        set "PATH=!PATH!;C:\Program Files\Git\bin"
        where git >nul 2>&1
        if !ERRORLEVEL! EQU 0 (
            echo      [OK] Git winget orqali muvaffaqiyatli o'rnatildi!
            goto :git_ready
        )
    )
    echo      [XATO] winget bilan o'rnatib bo'lmadi
)
echo.

:: --- Metod 2: PowerShell bilan yuklab olib o'rnatish ---
echo      [Metod 2] PowerShell bilan Git yuklab olinmoqda...
echo      URL: !GIT_DOWNLOAD_URL!
echo      Bu jarayon 2-5 daqiqa davom etishi mumkin...
echo.

powershell -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; try { Invoke-WebRequest -Uri '!GIT_DOWNLOAD_URL!' -OutFile '!GIT_INSTALLER!' -UseBasicParsing; exit 0 } catch { Write-Host $_.Exception.Message; exit 1 }"
if !ERRORLEVEL! NEQ 0 (
    echo      [XATO] Git yuklab olib bo'lmadi!
    echo      Internet aloqangizni tekshiring.
    goto :git_install_failed
)

if not exist "!GIT_INSTALLER!" (
    echo      [XATO] Installer fayli topilmadi!
    goto :git_install_failed
)

echo      [OK] Git installer yuklab olindi!
echo      O'rnatilmoqda (silent mode)...
echo.

:: Silent o'rnatish - admin huquqisiz ham ishlaydi (user installga tushadi)
"!GIT_INSTALLER!" /VERYSILENT /NORESTART /NOCANCEL /SP- /CLOSEAPPLICATIONS /RESTARTAPPLICATIONS /COMPONENTS="icons,ext\reg\shellhere,assoc,assoc_sh" 2>nul
if !ERRORLEVEL! NEQ 0 (
    :: Admin huquqisiz variant
    echo      Admin huquqisiz o'rnatish sinab ko'rilmoqda...
    "!GIT_INSTALLER!" /VERYSILENT /NORESTART /NOCANCEL /SP- /DIR="%LOCALAPPDATA%\Programs\Git" 2>nul
)

:: Installer ni o'chirish
del "!GIT_INSTALLER!" 2>nul

:: PATH yangilash
set "PATH=!PATH!;C:\Program Files\Git\bin;%LOCALAPPDATA%\Programs\Git\bin;C:\Program Files\Git\cmd;%LOCALAPPDATA%\Programs\Git\cmd"

:: Tekshirish
where git >nul 2>&1
if !ERRORLEVEL! EQU 0 (
    echo      [OK] Git muvaffaqiyatli o'rnatildi!
    goto :git_ready
)

:: Qo'shimcha PATH tekshirish
if exist "C:\Program Files\Git\bin\git.exe" (
    set "PATH=!PATH!;C:\Program Files\Git\bin"
    echo      [OK] Git o'rnatildi va topildi!
    goto :git_ready
)
if exist "%LOCALAPPDATA%\Programs\Git\bin\git.exe" (
    set "PATH=!PATH!;%LOCALAPPDATA%\Programs\Git\bin"
    echo      [OK] Git o'rnatildi va topildi!
    goto :git_ready
)

:: --- Metod 3: Chocolatey bilan ---
echo      [Metod 3] Chocolatey bilan sinab ko'rilmoqda...
where choco >nul 2>&1
if !ERRORLEVEL! EQU 0 (
    choco install git -y >nul 2>&1
    set "PATH=!PATH!;C:\Program Files\Git\bin"
    where git >nul 2>&1
    if !ERRORLEVEL! EQU 0 (
        echo      [OK] Git chocolatey orqali o'rnatildi!
        goto :git_ready
    )
)

:git_install_failed
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║  [XATO] Git o'rnatib bo'lmadi!                              ║
echo ║                                                              ║
echo ║  Qo'lda o'rnatish uchun:                                    ║
echo ║  1. https://git-scm.com/download/win ga o'ting               ║
echo ║  2. "64-bit Git for Windows Setup" ni yuklab oling           ║
echo ║  3. O'rnating (default sozlamalar bilan)                     ║
echo ║  4. Kompyuterni qayta yoqing                                 ║
echo ║  5. Bu skriptni qayta ishga tushiring                        ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
goto :error_exit

:git_ready
:: Git versiyasini ko'rsatish
for /f "tokens=*" %%i in ('git --version 2^>nul') do set "GIT_VER=%%i"
echo      Versiya: !GIT_VER!
echo.

:: ============================================================
:: 2-QADAM: ISHCHI PAPKANI TAYYORLASH
:: ============================================================
echo [2/5] Ishchi papka tayyorlanmoqda...

if exist "!WORK_DIR!" rmdir /s /q "!WORK_DIR!" 2>nul
mkdir "!WORK_DIR!"
if !ERRORLEVEL! NEQ 0 (
    echo      [XATO] Ishchi papka yaratib bo'lmadi!
    goto :error_exit
)
echo      [OK] Papka: !WORK_DIR!
echo.

:: ============================================================
:: 3-QADAM: MANBA REPONI KLONLASH
:: ============================================================
echo [3/5] Manba repo klonlanmoqda...
echo      !SOURCE_REPO!
echo.

git clone "!SOURCE_REPO!" "!WORK_DIR!\repo" 2>&1
if !ERRORLEVEL! NEQ 0 (
    echo      Oddiy clone ishlamadi, shallow clone sinab ko'rilmoqda...
    rmdir /s /q "!WORK_DIR!\repo" 2>nul
    git clone --depth 1 "!SOURCE_REPO!" "!WORK_DIR!\repo" 2>&1
    if !ERRORLEVEL! NEQ 0 (
        echo.
        echo      [XATO] Repo klonlab bo'lmadi!
        echo      Internet aloqangizni tekshiring.
        goto :error_exit
    )
)
echo      [OK] Repo muvaffaqiyatli klonlandi!
echo.

:: ============================================================
:: 4-QADAM: .git O'CHIRISH VA QAYTA INIT
:: ============================================================
echo [4/5] Git tarixini tozalash va yangi repo yaratish...
echo.

cd /d "!WORK_DIR!\repo"

:: .git papkasini o'chirish
if exist ".git" (
    rmdir /s /q ".git"
    echo      [OK] .git papkasi o'chirildi
)

:: Yangi git init
git init >nul 2>&1
echo      [OK] git init bajarildi

:: Branch nomini main qilish
git branch -M main >nul 2>&1
echo      [OK] Branch: main

:: Git config sozlash (agar oldin sozlanmagan bo'lsa)
git config user.email >nul 2>&1
if !ERRORLEVEL! NEQ 0 (
    git config user.email "user@transfer.local"
    git config user.name "Transfer Script"
)

:: Fayllarni qo'shish
git add -A >nul 2>&1
echo      [OK] Barcha fayllar staged

:: Commit
git commit -m "Transfer: Portfolio fayllarini ko'chirish" >nul 2>&1
if !ERRORLEVEL! NEQ 0 (
    git config user.email "user@transfer.local"
    git config user.name "Transfer Script"
    git commit -m "Transfer: Portfolio fayllarini ko'chirish" >nul 2>&1
)
echo      [OK] Commit yaratildi
echo.

:: ============================================================
:: 5-QADAM: MANZIL REPOGA PUSH QILISH
:: ============================================================
echo [5/5] Manzil repoga push qilinmoqda...
echo      !TARGET_REPO!
echo.

git remote add origin "!TARGET_REPO!" >nul 2>&1
git push -u origin main --force 2>&1
if !ERRORLEVEL! NEQ 0 (
    echo.
    echo      main branch bilan ishlamadi, master sinab ko'rilmoqda...
    git branch -M master >nul 2>&1
    git push -u origin master --force 2>&1
    if !ERRORLEVEL! NEQ 0 (
        echo.
        echo ╔══════════════════════════════════════════════════════════════╗
        echo ║  [XATO] Push qilib bo'lmadi!                                ║
        echo ║                                                              ║
        echo ║  Ehtimoliy sabablar:                                         ║
        echo ║  - GitHub hisobingizga kirmagan bo'lishingiz mumkin          ║
        echo ║  - Manzil repoga yozish huquqi yo'q                          ║
        echo ║  - Internet muammo                                           ║
        echo ║                                                              ║
        echo ║  Yechim:                                                     ║
        echo ║  1. GitHub Desktop o'rnating va login qiling                 ║
        echo ║  2. Yoki: git config --global credential.helper manager      ║
        echo ║  3. Keyin bu skriptni qayta ishga tushiring                  ║
        echo ╚══════════════════════════════════════════════════════════════╝
        echo.
        echo  Fayllar shu yerda saqlangan: !WORK_DIR!\repo
        echo  Qo'lda push: cd "!WORK_DIR!\repo" ^&^& git push -u origin main --force
        echo.
        goto :error_exit
    )
)

:: ============================================================
:: TOZALASH
:: ============================================================
echo.
cd /d "%TEMP%"
rmdir /s /q "!WORK_DIR!" 2>nul

:: ============================================================
:: MUVAFFAQIYAT!
:: ============================================================
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║              MUVAFFAQIYAT! / SUCCESS!                        ║
echo ║                                                              ║
echo ║  Barcha fayllar muvaffaqiyatli ko'chirildi!                  ║
echo ║                                                              ║
echo ║  Yangi repo:                                                 ║
echo ║  https://github.com/zafarbekjamolovsl-art/Portfolio-FAYLLAR- ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo Istalgan tugmani bosing... (Press any key...)
pause >nul
exit /b 0

:: ============================================================
:: XATO BILAN CHIQISH
:: ============================================================
:error_exit
echo.
echo  Skript xato bilan tugatildi.
echo  Muammo bo'lsa GitHub Issues orqali yozing.
echo.
echo Istalgan tugmani bosing... (Press any key...)
pause >nul
exit /b 1
