# Usar tu imagen ya construida en GitHub Container Registry
FROM ghcr.io/anystorm9/sikuvertice:v2

# Exponer puertos necesarios (VNC y SSH)
EXPOSE 5901
EXPOSE 22

