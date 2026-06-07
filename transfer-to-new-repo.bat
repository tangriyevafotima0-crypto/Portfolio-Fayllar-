@echo off
chcp 65001 >nul 2>&1
setlocal EnableDelayedExpansion

:: ============================================================
:: PORTFOLIO TRANSFER SCRIPT
:: Mualif: Portfolio-Fayllar- -> Portfolio-FAYLLAR-
:: Bu skript barcha fayllarni yangi repoga ko'chiradi
:: ============================================================

title Portfolio Transfer Script - Fayllarni Ko'chirish

:: Ranglar uchun
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║         PORTFOLIO FAYLLARNI KO'CHIRISH SKRIPTI              ║
echo ║                                                              ║
echo ║  Manba:  tangriyevafotima0-crypto/Portfolio-Fayllar-         ║
echo ║  Manzil: zafarbekjamolovsl-art/Portfolio-FAYLLAR-            ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

:: ============================================================
:: KONFIGURATSIYA / CONFIGURATION
:: ============================================================
set "SOURCE_REPO=https://github.com/tangriyevafotima0-crypto/Portfolio-Fayllar-.git"
set "TARGET_REPO=https://github.com/zafarbekjamolovsl-art/Portfolio-FAYLLAR-.git"
set "WORK_DIR=%TEMP%\portfolio-transfer-%RANDOM%"
set "BRANCH=main"
set "MAX_RETRIES=3"
set "RETRY_DELAY=5"

:: ============================================================
:: 1-QADAM: GIT MAVJUDLIGINI TEKSHIRISH
:: Step 1: Check if Git is installed
:: ============================================================
echo [1/6] Git tekshirilmoqda... (Checking Git installation...)
echo.

call :check_git
if !ERRORLEVEL! NEQ 0 (
    echo [XATO] Git topilmadi! Git o'rnatilmoqda...
    echo [ERROR] Git not found! Attempting to install Git...
    call :install_git
    if !ERRORLEVEL! NEQ 0 (
        echo.
        echo ╔══════════════════════════════════════════════════════════════╗
        echo ║  [XATO] Git o'rnatib bo'lmadi!                              ║
        echo ║  Iltimos, qo'lda o'rnating: https://git-scm.com/download    ║
        echo ║                                                              ║
        echo ║  [ERROR] Could not install Git!                              ║
        echo ║  Please install manually: https://git-scm.com/download       ║
        echo ╚══════════════════════════════════════════════════════════════╝
        echo.
        goto :error_exit
    )
)

:: Git versiyasini ko'rsatish
for /f "tokens=*" %%i in ('git --version 2^>nul') do set "GIT_VERSION=%%i"
echo [OK] Git topildi: !GIT_VERSION!
echo.

:: ============================================================
:: 2-QADAM: ISHCHI PAPKANI TAYYORLASH
:: Step 2: Prepare working directory
:: ============================================================
echo [2/6] Ishchi papka tayyorlanmoqda... (Preparing work directory...)
echo      Papka: !WORK_DIR!
echo.

if exist "!WORK_DIR!" (
    rmdir /s /q "!WORK_DIR!" 2>nul
)
mkdir "!WORK_DIR!" 2>nul
if !ERRORLEVEL! NEQ 0 (
    echo [XATO] Ishchi papka yaratib bo'lmadi!
    goto :error_exit
)
echo [OK] Ishchi papka tayyor!
echo.

:: ============================================================
:: 3-QADAM: MANBA REPONI KLONLASH (BIR NECHA METOD)
:: Step 3: Clone source repo (multiple methods)
:: ============================================================
echo [3/6] Manba repo klonlanmoqda... (Cloning source repository...)
echo      Manba: !SOURCE_REPO!
echo.

set "CLONE_SUCCESS=0"

:: --- METOD 1: Oddiy git clone ---
echo      [Metod 1] git clone ishlatilmoqda...
call :retry_command "git clone !SOURCE_REPO! !WORK_DIR!\source" !MAX_RETRIES!
if !ERRORLEVEL! EQU 0 (
    set "CLONE_SUCCESS=1"
    echo      [OK] Metod 1 muvaffaqiyatli!
    goto :clone_done
)
echo      [XATO] Metod 1 ishlamadi, keyingi metod sinab ko'rilmoqda...
echo.

:: --- METOD 2: --depth 1 bilan clone (shallow) ---
echo      [Metod 2] Shallow clone ishlatilmoqda...
if exist "!WORK_DIR!\source" rmdir /s /q "!WORK_DIR!\source" 2>nul
call :retry_command "git clone --depth 1 !SOURCE_REPO! !WORK_DIR!\source" !MAX_RETRIES!
if !ERRORLEVEL! EQU 0 (
    set "CLONE_SUCCESS=1"
    echo      [OK] Metod 2 muvaffaqiyatli!
    goto :clone_done
)
echo      [XATO] Metod 2 ishlamadi, keyingi metod sinab ko'rilmoqda...
echo.

:: --- METOD 3: GitHub CLI (gh) bilan clone ---
echo      [Metod 3] GitHub CLI (gh) ishlatilmoqda...
where gh >nul 2>&1
if !ERRORLEVEL! EQU 0 (
    if exist "!WORK_DIR!\source" rmdir /s /q "!WORK_DIR!\source" 2>nul
    call :retry_command "gh repo clone tangriyevafotima0-crypto/Portfolio-Fayllar- !WORK_DIR!\source" !MAX_RETRIES!
    if !ERRORLEVEL! EQU 0 (
        set "CLONE_SUCCESS=1"
        echo      [OK] Metod 3 muvaffaqiyatli!
        goto :clone_done
    )
    echo      [XATO] Metod 3 ishlamadi!
) else (
    echo      [INFO] GitHub CLI (gh) o'rnatilmagan, tashlab o'tilmoqda...
)
echo.

:: --- METOD 4: ZIP orqali yuklab olish ---
echo      [Metod 4] ZIP arxiv orqali yuklab olish...
where curl >nul 2>&1
if !ERRORLEVEL! EQU 0 (
    if exist "!WORK_DIR!\source" rmdir /s /q "!WORK_DIR!\source" 2>nul
    mkdir "!WORK_DIR!\source" 2>nul
    curl -L -o "!WORK_DIR!\source.zip" "https://github.com/tangriyevafotima0-crypto/Portfolio-Fayllar-/archive/refs/heads/main.zip" 2>nul
    if exist "!WORK_DIR!\source.zip" (
        echo      ZIP yuklab olindi, ochilmoqda...
        powershell -Command "Expand-Archive -Path '!WORK_DIR!\source.zip' -DestinationPath '!WORK_DIR!\source_temp' -Force" 2>nul
        if !ERRORLEVEL! EQU 0 (
            :: Move contents from extracted folder
            for /d %%d in ("!WORK_DIR!\source_temp\*") do (
                xcopy "%%d\*" "!WORK_DIR!\source\" /E /I /H /Y >nul 2>&1
            )
            rmdir /s /q "!WORK_DIR!\source_temp" 2>nul
            del "!WORK_DIR!\source.zip" 2>nul
            set "CLONE_SUCCESS=1"
            echo      [OK] Metod 4 muvaffaqiyatli!
            goto :clone_done
        )
    )
    echo      [XATO] Metod 4 ishlamadi!
) else (
    echo      [INFO] curl topilmadi, tashlab o'tilmoqda...
)
echo.

:: --- METOD 5: PowerShell orqali yuklab olish ---
echo      [Metod 5] PowerShell bilan yuklab olish...
if exist "!WORK_DIR!\source" rmdir /s /q "!WORK_DIR!\source" 2>nul
mkdir "!WORK_DIR!\source" 2>nul
powershell -Command "try { Invoke-WebRequest -Uri 'https://github.com/tangriyevafotima0-crypto/Portfolio-Fayllar-/archive/refs/heads/main.zip' -OutFile '!WORK_DIR!\source.zip' -UseBasicParsing; Expand-Archive -Path '!WORK_DIR!\source.zip' -DestinationPath '!WORK_DIR!\source_temp' -Force; Get-ChildItem '!WORK_DIR!\source_temp' | Get-ChildItem | Copy-Item -Destination '!WORK_DIR!\source' -Recurse -Force; exit 0 } catch { exit 1 }" 2>nul
if !ERRORLEVEL! EQU 0 (
    rmdir /s /q "!WORK_DIR!\source_temp" 2>nul
    del "!WORK_DIR!\source.zip" 2>nul
    set "CLONE_SUCCESS=1"
    echo      [OK] Metod 5 muvaffaqiyatli!
    goto :clone_done
)
echo      [XATO] Metod 5 ishlamadi!
echo.

:clone_done
if "!CLONE_SUCCESS!"=="0" (
    echo.
    echo ╔══════════════════════════════════════════════════════════════╗
    echo ║  [XATO] Hech bir metod bilan repo klonlab bo'lmadi!         ║
    echo ║  Internet aloqangizni tekshiring va qayta urinib ko'ring.    ║
    echo ║                                                              ║
    echo ║  [ERROR] All clone methods failed!                           ║
    echo ║  Check your internet connection and try again.               ║
    echo ╚══════════════════════════════════════════════════════════════╝
    goto :error_exit
)
echo.

:: ============================================================
:: 4-QADAM: .git PAPKASINI O'CHIRISH VA QAYTA INIT QILISH
:: Step 4: Remove .git and re-initialize
:: ============================================================
echo [4/6] Git tarixini tozalash va qayta sozlash...
echo      (Removing old git history and reinitializing...)
echo.

cd /d "!WORK_DIR!\source"

:: Eski .git papkasini o'chirish
if exist ".git" (
    rmdir /s /q ".git" 2>nul
    echo      [OK] Eski .git papkasi o'chirildi
)

:: Yangi git repo init qilish
git init >nul 2>&1
if !ERRORLEVEL! NEQ 0 (
    echo [XATO] git init bajarib bo'lmadi!
    goto :error_exit
)
echo      [OK] Yangi git repo yaratildi

:: Default branch nomi
git branch -M main >nul 2>&1
echo      [OK] Branch nomi: main

:: Barcha fayllarni qo'shish
git add -A >nul 2>&1
if !ERRORLEVEL! NEQ 0 (
    echo [XATO] git add bajarib bo'lmadi!
    goto :error_exit
)
echo      [OK] Barcha fayllar qo'shildi

:: Commit qilish
git commit -m "Portfolio fayllarni ko'chirish - Initial transfer from Portfolio-Fayllar-" >nul 2>&1
if !ERRORLEVEL! NEQ 0 (
    echo [XATO] git commit bajarib bo'lmadi!
    echo      Git konfiguratsiyasini tekshirish...
    git config user.email "transfer@portfolio.local" >nul 2>&1
    git config user.name "Portfolio Transfer" >nul 2>&1
    git add -A >nul 2>&1
    git commit -m "Portfolio fayllarni ko'chirish - Initial transfer" >nul 2>&1
    if !ERRORLEVEL! NEQ 0 (
        echo [XATO] Commit hali ham bajarilmadi!
        goto :error_exit
    )
)
echo      [OK] Commit muvaffaqiyatli!
echo.

:: ============================================================
:: 5-QADAM: YANGI REPOGA PUSH QILISH (BIR NECHA METOD)
:: Step 5: Push to target repo (multiple methods)
:: ============================================================
echo [5/6] Yangi repoga yuklash... (Pushing to target repository...)
echo      Manzil: !TARGET_REPO!
echo.

set "PUSH_SUCCESS=0"

:: --- PUSH METOD 1: Oddiy push ---
echo      [Metod 1] git push ishlatilmoqda...
git remote add origin "!TARGET_REPO!" >nul 2>&1
call :retry_command "git push -u origin main --force" !MAX_RETRIES!
if !ERRORLEVEL! EQU 0 (
    set "PUSH_SUCCESS=1"
    echo      [OK] Push metod 1 muvaffaqiyatli!
    goto :push_done
)
echo      [XATO] Push metod 1 ishlamadi, keyingi metod...
echo.

:: --- PUSH METOD 2: master branch nomi bilan ---
echo      [Metod 2] master branch bilan sinab ko'rilmoqda...
git branch -M master >nul 2>&1
call :retry_command "git push -u origin master --force" !MAX_RETRIES!
if !ERRORLEVEL! EQU 0 (
    set "PUSH_SUCCESS=1"
    echo      [OK] Push metod 2 muvaffaqiyatli!
    goto :push_done
)
echo      [XATO] Push metod 2 ishlamadi, keyingi metod...
git branch -M main >nul 2>&1
echo.

:: --- PUSH METOD 3: GitHub CLI bilan push ---
echo      [Metod 3] GitHub CLI bilan push...
where gh >nul 2>&1
if !ERRORLEVEL! EQU 0 (
    git remote remove origin >nul 2>&1
    git remote add origin "!TARGET_REPO!" >nul 2>&1
    call :retry_command "git push origin main --force" !MAX_RETRIES!
    if !ERRORLEVEL! EQU 0 (
        set "PUSH_SUCCESS=1"
        echo      [OK] Push metod 3 muvaffaqiyatli!
        goto :push_done
    )
    echo      [XATO] Push metod 3 ishlamadi!
) else (
    echo      [INFO] GitHub CLI mavjud emas, tashlab o'tilmoqda...
)
echo.

:: --- PUSH METOD 4: HTTPS token bilan ---
echo      [Metod 4] GitHub token bilan push...
if defined GITHUB_TOKEN (
    set "TOKEN_URL=https://!GITHUB_TOKEN!@github.com/zafarbekjamolovsl-art/Portfolio-FAYLLAR-.git"
    git remote remove origin >nul 2>&1
    git remote add origin "!TOKEN_URL!" >nul 2>&1
    call :retry_command "git push -u origin main --force" !MAX_RETRIES!
    if !ERRORLEVEL! EQU 0 (
        set "PUSH_SUCCESS=1"
        echo      [OK] Push metod 4 muvaffaqiyatli!
        goto :push_done
    )
    echo      [XATO] Push metod 4 ishlamadi!
) else (
    echo      [INFO] GITHUB_TOKEN o'rnatilmagan, tashlab o'tilmoqda...
    echo      [MASLAHAT] Token bilan ishlash uchun:
    echo                 set GITHUB_TOKEN=ghp_sizning_tokeningiz
    echo                 keyin skriptni qayta ishga tushiring
)
echo.

:push_done
if "!PUSH_SUCCESS!"=="0" (
    echo.
    echo ╔══════════════════════════════════════════════════════════════╗
    echo ║  [XATO] Push muvaffaqiyatsiz!                                ║
    echo ║                                                              ║
    echo ║  Mumkin sabablar:                                            ║
    echo ║  1. GitHub'ga kirish huquqi yo'q (login qiling)              ║
    echo ║  2. Token noto'g'ri yoki muddati o'tgan                     ║
    echo ║  3. Repo mavjud emas yoki ruxsat yo'q                        ║
    echo ║                                                              ║
    echo ║  Yechimlar:                                                  ║
    echo ║  - "git credential-manager" ni o'rnating                     ║
    echo ║  - GITHUB_TOKEN ni environment variable sifatida o'rnating   ║
    echo ║  - GitHub Desktop orqali login qiling                        ║
    echo ║                                                              ║
    echo ║  [ERROR] Push failed! Possible reasons:                      ║
    echo ║  1. Not authenticated to GitHub                              ║
    echo ║  2. Token is invalid or expired                              ║
    echo ║  3. Target repo does not exist or no write access            ║
    echo ╚══════════════════════════════════════════════════════════════╝
    echo.
    echo  Fayllar quyidagi papkada saqlangan:
    echo  !WORK_DIR!\source
    echo.
    echo  Qo'lda push qilish uchun:
    echo  cd "!WORK_DIR!\source"
    echo  git push -u origin main --force
    echo.
    goto :error_exit
)
echo.

:: ============================================================
:: 6-QADAM: TOZALASH VA YAKUNLASH
:: Step 6: Cleanup and finish
:: ============================================================
echo [6/6] Tozalash... (Cleaning up...)
echo.

cd /d "%TEMP%"
rmdir /s /q "!WORK_DIR!" 2>nul
echo      [OK] Vaqtinchalik fayllar o'chirildi
echo.

:: ============================================================
:: MUVAFFAQIYAT!
:: ============================================================
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║          MUVAFFAQIYAT! / SUCCESS!                            ║
echo ║                                                              ║
echo ║  Barcha fayllar muvaffaqiyatli ko'chirildi!                  ║
echo ║  All files have been transferred successfully!               ║
echo ║                                                              ║
echo ║  Yangi repo:                                                 ║
echo ║  https://github.com/zafarbekjamolovsl-art/Portfolio-FAYLLAR- ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo Istalgan tugmani bosing... (Press any key to exit...)
pause >nul
goto :eof

:: ============================================================
:: YORDAMCHI FUNKSIYALAR / HELPER FUNCTIONS
:: ============================================================

:: --- Git mavjudligini tekshirish ---
:check_git
where git >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    :: PATH da izlash
    if exist "C:\Program Files\Git\bin\git.exe" (
        set "PATH=%PATH%;C:\Program Files\Git\bin"
        exit /b 0
    )
    if exist "C:\Program Files (x86)\Git\bin\git.exe" (
        set "PATH=%PATH%;C:\Program Files (x86)\Git\bin"
        exit /b 0
    )
    if exist "%LOCALAPPDATA%\Programs\Git\bin\git.exe" (
        set "PATH=%PATH%;%LOCALAPPDATA%\Programs\Git\bin"
        exit /b 0
    )
    exit /b 1
)
exit /b 0

:: --- Git o'rnatish ---
:install_git
echo.
echo      Git o'rnatilmoqda... (Installing Git...)
echo.

:: Metod 1: winget bilan
echo      [1] winget bilan o'rnatish...
where winget >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    winget install --id Git.Git -e --source winget --accept-package-agreements --accept-source-agreements >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        set "PATH=%PATH%;C:\Program Files\Git\bin"
        echo      [OK] Git winget orqali o'rnatildi!
        exit /b 0
    )
)
echo      [INFO] winget bilan o'rnatib bo'lmadi...

:: Metod 2: Chocolatey bilan
echo      [2] Chocolatey bilan o'rnatish...
where choco >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    choco install git -y >nul 2>&1
    if %ERRORLEVEL% EQU 0 (
        set "PATH=%PATH%;C:\Program Files\Git\bin"
        echo      [OK] Git chocolatey orqali o'rnatildi!
        exit /b 0
    )
)
echo      [INFO] Chocolatey bilan o'rnatib bo'lmadi...

:: Metod 3: PowerShell bilan yuklab olish
echo      [3] PowerShell bilan Git yuklab olinmoqda...
set "GIT_INSTALLER=%TEMP%\git-installer.exe"
powershell -Command "try { [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri 'https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe' -OutFile '%GIT_INSTALLER%' -UseBasicParsing; exit 0 } catch { exit 1 }" 2>nul
if %ERRORLEVEL% EQU 0 (
    if exist "%GIT_INSTALLER%" (
        echo      Git o'rnatuvchi yuklab olindi, o'rnatilmoqda...
        "%GIT_INSTALLER%" /VERYSILENT /NORESTART /NOCANCEL /SP- /CLOSEAPPLICATIONS /RESTARTAPPLICATIONS /COMPONENTS="icons,ext\reg\shellhere,assoc,assoc_sh" 2>nul
        if %ERRORLEVEL% EQU 0 (
            set "PATH=%PATH%;C:\Program Files\Git\bin"
            del "%GIT_INSTALLER%" 2>nul
            echo      [OK] Git o'rnatildi!
            exit /b 0
        )
        del "%GIT_INSTALLER%" 2>nul
    )
)
echo      [XATO] Git o'rnatib bo'lmadi!
exit /b 1

:: --- Buyruqni qayta urinish funksiyasi ---
:retry_command
set "CMD=%~1"
set "RETRIES=%~2"
set "ATTEMPT=0"

:retry_loop
set /a ATTEMPT+=1
if !ATTEMPT! GTR !RETRIES! (
    exit /b 1
)

if !ATTEMPT! GTR 1 (
    echo      [QAYTA URINISH] Urinish !ATTEMPT!/!RETRIES! - !RETRY_DELAY! soniya kutilmoqda...
    timeout /t !RETRY_DELAY! /nobreak >nul 2>&1
)

%CMD% >nul 2>&1
if !ERRORLEVEL! EQU 0 (
    exit /b 0
)
goto :retry_loop

:: --- Xato bilan chiqish ---
:error_exit
echo.
echo ══════════════════════════════════════════════════════════════
echo  Skript xato bilan tugatildi. / Script ended with an error.
echo  Yordam: GitHub Issues orqali murojaat qiling.
echo ══════════════════════════════════════════════════════════════
echo.
echo Istalgan tugmani bosing... (Press any key to exit...)
pause >nul
exit /b 1
