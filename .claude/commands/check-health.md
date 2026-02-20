Quick health check of all GG Hookah services:
1. systemctl status gg-hookah-api gg-hookah-admin gg-hookah-bot --no-pager
2. curl http://127.0.0.1:5001/health
3. curl http://127.0.0.1:5002/health
4. sudo journalctl -u gg-hookah-api -n 5 --no-pager
5. sudo journalctl -u gg-hookah-admin -n 5 --no-pager
6. sudo journalctl -u gg-hookah-bot -n 5 --no-pager
Report summary.
