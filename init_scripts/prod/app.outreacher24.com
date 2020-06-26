server {
    server_name app.outreacher24.com via.outreacher24.com;

    location / {
        root /home/o24user/o24_prod/frontend/dist;
        try_files $uri /index.html;
    }

    location /ot {
        include proxy_params;
        proxy_pass http://unix:/home/o24user/o24-prod.sock;
    }

    location /bs/api {
        include proxy_params;
        proxy_pass http://127.0.0.1:3000;
    }


    location /api {
        include proxy_params;
	    rewrite /api/(.*) /$1 break;
        proxy_pass http://unix:/home/o24user/o24-prod.sock;
    }

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/app.outreacher24.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/app.outreacher24.com/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot




}
server {
    if ($host = app.outreacher24.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

    if ($host = via.outreacher24.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    if ($host = outreacher24.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    listen 80;
    server_name app.outreacher24.com via.outreacher24.com;
    return 404; # managed by Certbot

}
