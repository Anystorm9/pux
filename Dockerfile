# Base Image: Use Debian Bullseye for a stable and common base.
FROM debian:bullseye

# Install necessary packages for XFCE, SSH, VNC, and tunneling.2
# We use --no-install-recommends to keep the image slim.
# xfonts-base is CRITICAL: It provides the 'fixed' font that VNC server needs.
RUN apt-get update && apt-get install -y --no-install-recommends \
    openssh-server \
    xfce4 \
    xfce4-goodies \
    dbus-x11 \
    curl \
    sudo \
    ca-certificates \
    tightvncserver \
    xfonts-base \
    wget \
    default-jre \
    firefox-esr \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Download SikuliXs IDE
RUN wget -O /usr/local/bin/sikulixide.jar https://launchpad.net/sikuli/sikulix/2.0.5/+download/sikulixide-2.0.5.jar && \
    chmod +x /usr/local/bin/sikulixide.jar

# Install Cloudflared for secure tunneling.
# This downloads thefff latest version, installs it, and cleans up.
RUN curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb && \
    dpkg -i cloudflared.deb && \
    rm cloudflared.deb

# Configure SSH.
# - Set a password for the root user ('yourpassword').
# - Allow root login via SSH with a password.
RUN echo 'root:yourpassword' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Configure XFCE to be the default window manager for VNC.
# This creates the .xsession file that VNC's X server will read on startup.
RUN echo "xfce4-session" > /etc/skel/.xsession

# Create a .xsession file for the root user as well.
RUN mkdir -p /root && \
    echo "xfce4-session" > /root/.xsession && \
    chown root:root /root /root/.xsession

# Copy SikuliX scridsfdpt and images
COPY 1.png 2.png 3.png 4.png 5.png 6.png 7.png 8.png 9.png 10.png 16.png 17.png 18.png 19.png 20.png sikuvertice.py start.sh /
RUN chmod +x /start.sh
# Expose ports for VNC and SSH.
EXPOSE 5901
EXPOSE 22

# The command that will be executed when the container starts.
CMD ["/start.sh"]
