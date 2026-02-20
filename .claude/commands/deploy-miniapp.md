Build and deploy Mini App to production:
1. cd /opt/gg-hookah-v2/miniapp && npm run build
2. sudo rm -rf /var/www/gghokah.delivery/*
3. sudo cp -r dist/* /var/www/gghokah.delivery/
4. sudo chown -R www-data:www-data /var/www/gghokah.delivery
5. Verify: curl -s https://gghookah.delivery | head -5
Report result.
