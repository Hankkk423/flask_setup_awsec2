# Deploying a Flask App on AWS EC2

This guide will walk you through the process of deploying a Flask web application on an AWS EC2 instance running Ubuntu. Follow the steps below to set up your environment and deploy your Flask app.

## Step 1: Create an EC2 Instance on AWS

1. **Name**: AWS EC2 ...
2. **AMI**: Ubuntu
3. **Key Pair**: Create a new one and save it
4. **Network Setting**: Allow all 3 incoming traffics

## Step 2: Connect to the Instance

- Navigate to instance information.
- Click "Connect" on the top-right corner.
- Select "EC2 Instance Connect" option and click "Connect". The CloudShell for this instance will pop up.

## Step 3: Install Git, Python, and pip

Run the following commands to install Git, Python, and pip on your Ubuntu instance:

```bash
sudo apt-get update
sudo apt-get install git python3-pip -y
sudo apt-get install python3.10-venv
```

You will see a "Services Restarted Box." Here's what it means:

1. **Services to Restart**:
   - `[*]` Checkboxes: Services currently running and candidates for restart.
   - `[ ]` Checkboxes: Services not running or not currently active.

2. **Selecting Services to Restart**:
   - Check a checkbox to restart a service.
   - Leave it unchecked to skip restarting.

3. **General Recommendation**:
   - It's generally safe to restart services marked with `[*]`.
   - You can leave unchecked services not running or not needed to restart.

4. **Example**:
   - Typically, restart services like `cron`, `rsyslog`, `sshd` (SSH) marked with `[*]` to apply updates.
   - Services like `dbus` and `networkd-dispatcher` are not running; you can leave them unchecked.

5. **Select and Confirm**:
   - Use arrow keys to navigate, spacebar to select/deselect, and Enter to confirm.

6. **Completion**:
   - Selected services will be restarted during the installation process.

(Note: Services may vary based on your system and updates.)

## Step 4-1: Create Python Files (Manually)

1. Create a directory:
   ```bash
   mkdir helloworld
   cd helloworld
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```

3. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

4. Install Flask:
   ```bash
   pip install flask flask_cors
   ```

5. Create a Simple Flask API:
   ```bash
   sudo nano app.py
   ```

6. Add the following code to `app.py`:

   ```python
   from flask import Flask
   from flask_cors import CORS, cross_origin

   app = Flask(__name__)
   CORS(app)

   @app.route('/')
   @cross_origin()
   def hello_world():
       return 'Hello World!'

   if __name__ == "__main__":
       app.run(debug=True)
   ```

7. Verify if it works by running:
   ```bash
   python3 app.py
   ```

## Step 4-2: Create Python Files (GitHub Clone)

1. Clone code from GitHub:
   ```bash
   git clone https://github.com/your-github-username/your-repo-name.git
   ```

2. Navigate to your app directory:
   ```bash
   cd your-repo-name
   ```

3. Create the virtual environment:
   ```bash
   python3 -m venv venv
   ```

4. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. Make necessary code changes in files:
   ```bash
   sudo nano path/to/file
   ```

7. Verify if it works by running:
   ```bash
   python3 app.py
   ```

## Step 5: Run Gunicorn WSGI Server
Run Gunicorn WSGI server to serve the Flask Application When you “run” flask, you are actually running Werkzeug’s development WSGI server, which forward requests from a web server. Since Werkzeug is only for development, we have to use Gunicorn, which is a production-ready WSGI server, to serve our application.

1. Install Gunicorn:
   ```bash
   pip install gunicorn
   ```

2. Run Gunicorn:
   ```bash
   gunicorn -b 0.0.0.0:8000 app:app
   ```

   Gunicorn is running (Ctrl + C to exit)!

3. Use systemd to manage Gunicorn:
Use systemd to manage Gunicorn Systemd is a boot manager for Linux. We are using it to restart gunicorn if the EC2 restarts or reboots for some reason. We create a .service file in the /etc/systemd/system folder, and specify what would happen to gunicorn when the system reboots. We will be adding 3 parts to systemd Unit file — Unit, Service, Install

Unit — This section is for description about the project and some dependencies Service — To specify user/group we want to run this service after. Also some information about the executables and the commands. Install — tells systemd at which moment during boot process this service should start. With that said, create an unit file in the /etc/systemd/system directory

   Create a unit file:
   ```bash
   sudo nano /etc/systemd/system/helloworld.service
   ```

   Then add the following into the file:

   ```plaintext
   [Unit]
   Description=Gunicorn instance for a simple hello world app
   After=network.target

   [Service]
   User=ubuntu
   Group=www-data
   WorkingDirectory=/home/ubuntu/helloworld
   ExecStart=/home/ubuntu/helloworld/venv/bin/gunicorn -b localhost:8000 app:app
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   Then enable the service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start helloworld
   sudo systemctl enable helloworld
   ```

   Check if the app is running with:
   ```bash
   curl localhost:8000
   ```

## Step 6: Run Nginx Webserver
Run Nginx Webserver to accept and route request to Gunicorn. Finally, we set up Nginx as a reverse-proxy to accept the requests from the user and route it to gunicorn.

1. Install Nginx:
   ```bash
   sudo apt-get install nginx
   ```

2. Start Nginx and enable it:
Start the Nginx service and go to the Public IP address of your EC2 on the browser to see the `default nginx landing page`
   ```bash
   sudo systemctl start nginx
   sudo systemctl enable nginx
   ```

3. Edit the default Nginx file:
   ```bash
   sudo nano /etc/nginx/sites-available/default
   ```

4. Add the following code at the top (below the default comments):

   ```bash
   upstream flaskhelloworld {
       server 127.0.0.1:8000;
   }
   ```

   Add a proxy_pass to flaskhelloworld at location /
   ```bash
   location / {
       proxy_pass http://flaskhelloworld;
   }
   ```

5. Restart Nginx:
   ```bash
   sudo systemctl restart nginx
   ```

Your Flask app is up and running publicly with the `Instance PublichIPs`!

---

## Common Command-Line Commands on AWS Ubuntu

Here's a list of some commonly used command-line commands and their descriptions for an AWS Ubuntu system:

1. **`ls`**: List files and directories in the current directory.

   Example:
   ```bash
   ls
   ```

2. **`cd`**: Change the current directory.

   Example:
   ```bash
   cd /path/to/directory
   ```

3. **`pwd`**: Print the current working directory.

   Example:
   ```bash
   pwd
   ```

4. **`mkdir`**: Create a new directory.

   Example:
   ```bash
   mkdir mydirectory
   ```

5. **`touch`**: Create an empty file.

   Example:
   ```bash
   touch myfile.txt
   ```

6. **`rm`**: Remove files and directories.

   Example (remove a file):
   ```bash
   rm myfile.txt
   ```

   Example (remove a directory and its contents):
   ```bash
   rm -r mydirectory
   ```

7. **`sudo`**: Execute a command with superuser (root) privileges.

   Example:
   ```bash
   sudo apt-get update
   ```

8. **`apt`**: Package management command for Ubuntu to install, update, and manage software packages.

   Example (update package lists):
   ```bash
   sudo apt update
   ```

   Example (install a package):
   ```bash
   sudo apt install package-name
   ```

9. **`dpkg`**: Package management command for querying and managing Debian packages.

   Example (query package information):
   ```bash
   dpkg -l | grep package-name
   ```

10. **`ps`**: List running processes.

    Example:
    ```bash
    ps aux
    ps aux | grep python
    ```

11. **`kill`**: Terminate processes by their process ID (PID).

    Example (terminate a process by PID):
    ```bash
    kill -9 PID
    ```

12. **`nano`**: Text editor for editing files from the command line.

    Example:
    ```bash
    nano filename.txt
    ```

    ### Basic `nano` Commands:

    Once you've opened a file in `nano`, you can use the following basic commands:

    - **Navigation**: Use the arrow keys to move the cursor.
    - **Editing**: Type and edit the text as needed.
    - **Save**: Press `Ctrl` + `O` to save changes, and press `Enter`.
    - **Exit**: Press `Ctrl` + `X` to exit `nano`.

    ### Saving Changes:

    To save changes to the file you're editing in `nano`, follow these steps:

    1. Make your edits to the file as needed.

    2. Press `Ctrl` + `O` (Hold the `Ctrl` key and press `O`). This will prompt you to confirm the filename to save to. By default, `nano` will suggest the filename you originally opened.

    3. Press Enter to confirm the filename.

    4. You may also add or change the filename if you want to save the file with a different name. After entering the desired filename, press Enter.

    5. `nano` will save the changes and return you to the editing interface.

    ### Exiting `nano`:

    To exit `nano` after saving your changes, follow these steps:

    1. Press `Ctrl` + `X`. This will exit `nano`.

    2. If you have unsaved changes, `nano` will prompt you to save them before exiting. Press `Y` (for Yes) to save changes, or `N` (for No) to discard changes.

    3. If you chose to save changes, `nano` will ask for confirmation of the filename (similar to the save process). Press Enter to confirm the filename.

    4. `nano` will then exit.

13. **`vim`**: Powerful text editor for editing files from the command line.

    Example:
    ```bash
    vim filename.txt
    ```

14. **`chmod`**: Change file permissions.

    Example (give read and write permissions to a file):
    ```bash
    chmod +rw filename.txt
    ```

15. **`chown`**: Change file ownership.

    Example (change the owner of a file):
    ```bash
    chown new-owner filename.txt
    ```

16. **`scp`**: Securely copy files between local and remote systems.

    Example (copy a file to a remote server):
    ```bash
    scp local-file.txt user@remote-server:/path/on/remote/
    ```

17. **`wget`**: Download files from the internet.

    Example (download a file):
    ```bash
    wget https://example.com/file.zip
    ```

18. **`tar`**: Archive utility for compressing and extracting files.

    Example (create a tar archive):
    ```bash
    tar -czvf archive.tar.gz directory/
    ```

19. **`gzip`**: Compression utility.

    Example (compress a file):
    ```bash
    gzip filename.txt
    ```

20. **`unzip`**: Extract files from a zip archive.

    Example:
    ```bash
    unzip archive.zip
    ```
---
