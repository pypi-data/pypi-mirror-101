osso-docktool :: HDD administration and maintenance
===================================================

*osso-docktool* provides tools to register disks to the OSSO dashboard, to
print labels and wipe disks.

Requirements (``apt install --no-install-recommends``)::

    coreutils       # dd
    pwgen           # pwgen
    smartmontools   # smartctl
    nvme-cli        # nvme
    hdparm          # hdparm
    sdparm          # sdparm

    # FIXME: /usr/local/bin/run-lessrandom
    # FIXME: /usr/local/bin/run-zero-disk

Example usage (as root)::

    osso-docktool /dev/sdb

Example setup (as root)::

    pip3 install osso-docktool

    install -dm0700 /etc/osso-docktool
    install /usr/local/share/doc/osso-docktool/local_settings.py.template \
            /etc/osso-docktool/local_settings.py

    ${EDITOR:-vi} /etc/osso-docktool/local_settings.py
    # ^-- fix hostnames, fix tokens
    #     get 1 shared token from:
    #     https://account.example.com/admin/usertoken/token/

Example automation:

``/etc/sudoers`` (amend, using visudo)::

    osso ALL=NOPASSWD: /usr/local/sbin/spawn-root-dbus

``/usr/local/sbin/spawn-root-dbus`` (0700)::

    #!/bin/sh

    # Quick hack to wait for Xauth file to arrive..
    sleep 10

    /bin/mkdir -p /run/user/0
    exec /usr/bin/env -i \
    DISPLAY=:0 TERM=xterm \
    LC_ALL=en_US.UTF-8 \
    XAUTHORITY=/run/user/1000/gdm/Xauthority \
    /usr/bin/dbus-daemon --session --address="unix:path=/run/user/0/bus"

``/usr/local/sbin/inv-connect.sh`` (0700)::

    #!/bin/sh
    logger "Inventory disk $1 inserted"

    DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/0/bus \
    DISPLAY=:0 \
    LC_ALL=en_US.UTF-8 \
    TERM=xterm-256color \
    XAUTHORITY=/run/user/1000/gdm/Xauthority \
    gnome-terminal -- /usr/local/bin/osso-docktool "$1" || sleep 60

``/usr/local/sbin/inv-disconnect.sh`` (0700)::

    #!/bin/sh
    exec logger "Inventory USB disk removed"

``/usr/local/bin/run-zero-disk`` (0700)::

    #!/bin/bash

    path=$1
    if test -z $path; then
        echo "please supply path as argument"
        exit 1
    fi
    output=$(dd if=/dev/zero \
       of=$path \
       bs=32M \
       conv=fsync 2>&1)
    ret=$?

    # Checking output as DD does not exit clean even if whole disk is wiped

    if [[ $ret -eq 0 ]]; then
        exit 0
    else
        if [[ $output == *'No space left on device'* ]]; then
            echo "Disk $path has been zeroed"
            exit 0
        else
            echo "Something went wrong while writing to $path"
            echo $output
            exit 1
        fi
    fi

Compile lessrandom.c and move lessrandom to ``/usr/local/bin/lessrandom`` (0700)::

    lessrandom.c:

    #include <stdio.h>
    #include <time.h>
    #define BUF 4096
    int main() {
        FILE *f;
        char buf[BUF];
        f = fopen("/dev/urandom", "rb");
        while (1) {
            if (fread(buf, 1, BUF, f) == BUF) {
                int i;
                for (i = 0; i <= buf[0]; ++i) {
                    fwrite(buf, 1, BUF - 1, stdout);
                }
            }
        }
        fclose(f);
        return 0;
    }


    gcc -Wall lessrandom.c -o lessrandom


``/usr/local/bin/run-lessrandom`` (0700)::

    #!/bin/bash

    path=$1
    if test -z $path; then
        echo "please supply path as argument"
        exit 1
    fi
    output=$(dd if=<(/usr/local/bin/lessrandom) \
       of=$path \
       bs=32M \
       conv=fsync 2>&1)
    ret=$?

    # Checking output as DD does not exit clean even if whole disk is wiped

    if [[ $ret -eq 0 ]]; then
        exit 0
    else
        if [[ $output == *'No space left on device'* ]]; then
            echo "Disk $path has been wiped"
            exit 0
        else
            echo "Something went wrong while writing to $path"
            echo $output
            exit 1
        fi
    fi


``/etc/udev/rules.d/10-osso-docktool.rules``::

    KERNEL=="sd[b-z]", SUBSYSTEM=="block", SUBSYSTEMS=="scsi", ACTION=="add", PROGRAM="/usr/local/sbin/inv-connect.sh %k"
    SUBSYSTEM=="block", SUBSYSTEMS=="usb", NAME="invdisk", SYMLINK+="invdisk%n", ACTION=="remove",RUN+="/usr/local/sbin/inv-disconnect.sh"

Make sure there is a root dbus-daemon child of our user-systemd.

``.config/systemd/user/spawn-root-dbus.service``::

    [Unit]
    Description=Auto-start root-dbus
    After=graphical.target

    [Service]
    ExecStart=/usr/bin/sudo /usr/local/sbin/spawn-root-dbus
    Restart=always

    [Install]
    WantedBy=default.target

Enable it::

    systemd --user daemon-reload
    systemd --user start spawn-root-dbus.service
    systemd --user enable spawn-root-dbus.service
