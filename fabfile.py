from fabric.api import local, run, env, put, sudo, cd

env.user = "pi"
env.password = "raspberry"

# Sign Pi IP here
env.hosts = ["signhostname.local"]


# def change_password():
#     sudo('echo "pi:newpassword" | chpasswd')


def set_hostname():
    name = "signhostname"
    sudo('echo "{}" > /etc/hostname'.format(name))


def shutdown():
    sudo("shutdown -h now", warn_only=True)


def setup():
    sudo("apt-get update -y")
    sudo(
        "apt-get -qq install -y usbmount python-dev python-imaging python-pip python-rpi.gpio"
    )
    sudo("apt-get -qq install -y python-scipy libasound-dev portaudio19-dev")
    sudo("mkdir -p /opt/sign")
    put("dotstar.c", "/opt/sign/", mode="744")
    put("Makefile", "/opt/sign/", mode="744")
    with cd("/opt/sign"):
        run("make")
    sudo("chown -R pi:pi /opt/sign")
    run("pip install Flask pyaudio")
    run("wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip")
    run("unzip ngrok-stable-linux-arm.zip")
    run("rm ngrok-stable-linux-arm.zip")
    setup_services()


def setup_services():
    put("sign.service", "/lib/systemd/system/", use_sudo=True)
    put("ngrok.service", "/lib/systemd/system/", use_sudo=True)
    sudo("systemctl daemon-reload")
    sudo("systemctl enable sign", warn_only=True)
    sudo("systemctl restart sign", warn_only=True)
    sudo("systemctl enable ngrok", warn_only=True)
    sudo("systemctl start ngrok", warn_only=True)
    deploy()


def deploy():
    put("sign.py", "/opt/sign/", mode="744")
    put("sign_api.py", "/opt/sign/", mode="744")
    put("signal_processing.py", "/opt/sign/", mode="744")
    put("index.html", "/opt/sign/", mode="744")
    # put('set_colour.py', '/opt/sign/', mode="744")  # unused
    sudo("systemctl restart sign", warn_only=True)
