# Hosting UI and Models separately

Sometimes, it's beneficial to host Ollama, separate from the UI, but retain the RAG and RBAC support features shared across users:

# Open WebUI Configuration

## UI Configuration

For the UI configuration, you can set up the Apache VirtualHost as follows:

```
# Assuming you have a website hosting this UI at "server.com"
<VirtualHost 192.168.1.100:80>
    ServerName server.com
    DocumentRoot /home/server/public_html

    ProxyPass / http://server.com:3000/ nocanon
    ProxyPassReverse / http://server.com:3000/
    # Needed after 0.5
    ProxyPass / ws://server.com:3000/ nocanon
    ProxyPassReverse / ws://server.com:3000/

</VirtualHost>
```

Enable the site first before you can request SSL:

`a2ensite server.com.conf` # this will enable the site. a2ensite is short for "Apache 2 Enable Site"

```
# For SSL
<VirtualHost 192.168.1.100:443>
    ServerName server.com
    DocumentRoot /home/server/public_html

    ProxyPass / http://server.com:3000/ nocanon
    ProxyPassReverse / http://server.com:3000/
    # Needed after 0.5
    ProxyPass / ws://server.com:3000/ nocanon
    ProxyPassReverse / ws://server.com:3000/

    SSLEngine on
    SSLCertificateFile /etc/ssl/virtualmin/170514456861234/ssl.cert
    SSLCertificateKeyFile /etc/ssl/virtualmin/170514456861234/ssl.key
    SSLProtocol all -SSLv2 -SSLv3 -TLSv1 -TLSv1.1

    SSLProxyEngine on
    SSLCACertificateFile /etc/ssl/virtualmin/170514456865864/ssl.ca
</VirtualHost>

```

I'm using virtualmin here for my SSL clusters, but you can also use certbot directly or your preferred SSL method. To use SSL:

### Prerequisites.

Run the following commands:

`snap install certbot --classic`
`snap apt install python3-certbot-apache` (this will install the apache plugin).

Navigate to the apache sites-available directory:

`cd /etc/apache2/sites-available/`

Create server.com.conf if it is not yet already created, containing the above `<virtualhost>` configuration (it should match your case. Modify as necessary). Use the one without the SSL:

Once it's created, run `certbot --apache -d server.com`, this will request and add/create an SSL keys for you as well as create the server.com.le-ssl.conf

# Configuring Ollama Server

On your latest installation of Ollama, make sure that you have setup your api server from the official Ollama reference:

[Ollama FAQ](https://github.com/jmorganca/ollama/blob/main/docs/faq.md)

### TL;DR

The guide doesn't seem to match the current updated service file on linux. So, we will address it here:

Unless when you're compiling Ollama from source, installing with the standard install `curl https://ollama.com/install.sh | sh` creates a file called `ollama.service` in /etc/systemd/system. You can use nano to edit the file:

```
sudo nano /etc/systemd/system/ollama.service
```

Add the following lines:

```
Environment="OLLAMA_HOST=0.0.0.0:11434" # this line is mandatory. You can also specify
```

For instance:

```
[Unit]
Description=Ollama Service
After=network-online.target

[Service]
ExecStart=/usr/local/bin/ollama serve
Environment="OLLAMA_HOST=0.0.0.0:11434" # this line is mandatory. You can also specify 192.168.254.109:DIFFERENT_PORT, format
Environment="OLLAMA_ORIGINS=http://192.168.254.106:11434,https://models.server.city" # this line is optional
User=ollama
Group=ollama
Restart=always
RestartSec=3
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/s>

[Install]
WantedBy=default.target
```

Save the file by pressing CTRL+S, then press CTRL+X

When your computer restarts, the Ollama server will now be listening on the IP:PORT you specified, in this case 0.0.0.0:11434, or 192.168.254.106:11434 (whatever your local IP address is). Make sure that your router is correctly configured to serve pages from that local IP by forwarding 11434 to your local IP server.

This page previously described Ollama server and virtual host setup. In the lite version, Ollama support is removed.
