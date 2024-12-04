FROM nginx:alpine

# Copiar archivo de configuración de NGINX
COPY nginx.conf /etc/nginx/nginx.conf

# Copiar certificados SSL
COPY certs /etc/nginx/certs

# Exponer puertos HTTP y HTTPS
EXPOSE 80 443
