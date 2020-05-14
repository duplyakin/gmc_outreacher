server {
    server_name outreacher24.com dv.outreacher24.com;

    location / {
	root /home/o24user/o24_dev/frontend/dist;
	try_files $uri /index.html;
    }

    location /api {
        include proxy_params;
        proxy_pass http://unix:/home/o24user/o24-dev.sock;
    }

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/outreacher24.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/outreacher24.com/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot


}
server {
    if ($host = dv.outreacher24.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    if ($host = outreacher24.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    listen 80;
    server_name outreacher24.com dv.outreacher24.com;
    return 404; # managed by Certbot




}
