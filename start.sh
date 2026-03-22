#!/bin/bash

# Set the USER environment variable. This is critical for vncserver.
export USER=root

# --- VNC Server Setup ---

# 1. Forcefully clean up any leftover VNC server processes and lock files
#    from a previous container run. This is critical for handling `docker restart`.
/usr/bin/vncserver -kill :1 > /dev/null 2>&1 || true
rm -rf /tmp/.X1-lock /tmp/.X11-unix/X1
echo "Cleaned up previous VNC session files."

# 2. Create the directory for VNC configurations.
mkdir -p /root/.vnc

# 3. Create a custom xstartup file.
# This script is executed when the VNC session starts.
cat > /root/.vnc/xstartup << 'EOF'
#!/bin/bash
# This file is executed by VNC when the graphical session starts.

# Start the XFCE desktop environment in the background.
startxfce4 &

# Give the desktop a moment to stabilize before launching applications.
sleep 5

# --- Autostart Applications ---
# The commands below will run automatically after the desktop is ready.

# 1. Launch Firefox
#    - We disable the content sandbox for compatibility in some container environments.
#    - It launches maximized and goes to a specific URL.
#    - Output is redirected to a log file for debugging.
export MOZ_DISABLE_CONTENT_SANDBOX=1
firefox https://link-target.net/3995761/bgPZqtt3wH5e > /tmp/firefox.log 2>&1 &

# 2. Launch SikuliX Script
#    - Runs the specified SikuliX script.
#    - Output is redirected to a log file for debugging.
java -jar /usr/local/bin/sikulixide.jar -r /sikuvertice.py > /tmp/sikuli.log 2>&1 &

EOF

# 4. Make the xstartup script executable.
chmod 755 /root/.vnc/xstartup

# 5. Set the VNC password non-interactively.
echo 'vncpass' | vncpasswd -f > /root/.vnc/passwd

# 6. Set correct permissions for the password file.
chmod 600 /root/.vnc/passwd

# 7. Start the VNC server.
/usr/bin/vncserver :1 -geometry 1280x800 -depth 24

echo "VNC Server started on display :1 (Port 5901)"


# --- Core Services & Cloudflare Tunnels ---

# Start OpenSSH server for terminal access.
service ssh start

echo "SSH service started."
echo "Launching Cloudflare Tunnels..."

# Launch the SSH tunnel in the background.
cloudflared tunnel --url ssh://localhost:22 > /tmp/ssh_tunnel.log 2>&1 &

sleep 8 # Wait for the tunnel to establish.

# Display the SSH connection URL.
echo "#####################################################################"
echo "## Your SSH connection URL is:"
cat /tmp/ssh_tunnel.log | grep -o 'https://[a-z-]*\.trycloudflare.com'
echo "##"
echo "## Use: ssh root@<URL_ABOVE_WITHOUT_HTTPS>"
echo "## Password: yourpassword"
echo "#####################################################################"

# Launch the VNC tunnel in the foreground.
# This is the primary process that keeps the container running.
echo ""
echo "Launching VNC tunnel. The URL will be displayed below:"
exec cloudflared tunnel --url tcp://localhost:5901
