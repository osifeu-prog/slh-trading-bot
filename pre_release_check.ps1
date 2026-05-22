Write-Host "========================================" -ForegroundColor Cyan
Write-Host " PRE-RELEASE SECURITY CHECKLIST" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Follow these steps before going public:" -ForegroundColor White
Write-Host ""
Write-Host "1. ROTATE ALL TOKENS & KEYS" -ForegroundColor Magenta
Write-Host "   a. Binance Testnet API keys: go to https://testnet.binance.vision/"
Write-Host "      - Delete the old key, create a new one."
Write-Host "      - Update BINANCE_API_KEY and BINANCE_SECRET_KEY in .env"
Write-Host "   b. Telegram bot tokens: both @SLH_Test_bot and @SLH_Supervisor_bot"
Write-Host "      - Go to @BotFather, revoke and generate new tokens."
Write-Host "      - Update TELEGRAM_TOKEN and SUPERVISOR_BOT_TOKEN in .env"
Write-Host ""
Write-Host "2. VERIFY .gitignore INCLUDES .env" -ForegroundColor Magenta
Write-Host "   - Run: git check-ignore .env"
Write-Host "   - If not, add .env to .gitignore and commit."
Write-Host ""
Write-Host "3. CHECK DOCKER CONTAINER IS SECURE" -ForegroundColor Magenta
Write-Host "   - No sensitive files mounted unnecessarily."
Write-Host "   - Ports only exposed as needed."
Write-Host ""
Write-Host "4. CONFIRM TELEGRAM PRIVACY MODE IS OFF" -ForegroundColor Magenta
Write-Host "   - Via @BotFather, both bots should have Group Privacy turned OFF."
Write-Host ""
Write-Host "5. FINAL BACKUP" -ForegroundColor Magenta
Write-Host "   - Run: .\backup.ps1"
Write-Host ""
Write-Host "6. TEST ALL COMMANDS" -ForegroundColor Magenta
Write-Host "   - /start, /myid, /status on both bots"
Write-Host "   - Dashboard accessible via Ngrok"
Write-Host ""
Write-Host "7. REMOVE ANY HARDCODED SECRETS" -ForegroundColor Magenta
Write-Host "   - Search code for passwords, keys."
Write-Host "   - Replace with environment variables."
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " After completing all steps, the system is ready for public use." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
pause
