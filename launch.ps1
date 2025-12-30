$OutputEncoding = [System.Text.Encoding]::UTF8

# 检查当前目录下是否存在 .venv 文件夹
if (-not (Test-Path -Path ".\.venv" -PathType Container)) {
    Write-Host "[info] 正在尝试创建虚拟环境..." -ForegroundColor Cyan

    python -m venv .venv

    if ($?) {
        Write-Host "[info] 虚拟环境创建成功，正在安装依赖..." -ForegroundColor Cyan
        # 直接调用虚拟环境内的 pip，无需激活
        & ".\.venv\Scripts\python.exe" -m pip install --upgrade pip
        & ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt
        
        Write-Host "[info] 成功：.venv 环境已创建并完成依赖安装" -ForegroundColor Green
    } else {
        Write-Host "[info] 错误：虚拟环境创建失败。请检查 Python/pip 是否在环境变量中。" -ForegroundColor Red
        pause
        exit
    }
} else {
    Write-Host "[info] 检测到 .venv 目录已存在" -ForegroundColor Yellow
}

# 运行程序
Write-Host "[info] 正在启动程序..." -ForegroundColor Cyan
& ".\.venv\Scripts\Activate.ps1"
& ".\.venv\Scripts\python.exe" ".\bin\main.py"

pause