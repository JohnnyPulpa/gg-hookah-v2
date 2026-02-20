Restart all GG Hookah services and verify:
1. sudo systemctl restart gg-hookah-api
2. sudo systemctl restart gg-hookah-admin
3. sudo systemctl restart gg-hookah-bot
4. Sleep 3 seconds
5. curl http://127.0.0.1:5001/health
6. curl http://127.0.0.1:5002/health
7. systemctl status gg-hookah-bot --no-pager | head -5
Report all results.
