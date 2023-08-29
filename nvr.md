# The setup - container within container

1. NVR runs as a docker container; docker daemon runs in a Ubuntu LXC container on Proxmox (named "400").

## HW Access

NVR requires access to GPU and Goole Coral - Proxmox -> LXC -> Docker passthrough..
Following [this guide](https://gist.github.com/packerdl/a4887c30c38a0225204f451103d82ac5) and others..:

1. _PROXMOX_ 
    1. Check if GPU is there
    ```sh
    ls -la /dev/dri

    total 0
    drwxr-xr-x  3 root root        100 Jan 11 15:34 .
    drwxr-xr-x 19 root root       4520 Jan 11 15:34 ..
    drwxr-xr-x  2 root root         80 Jan 11 15:34 by-path
    crw-rw----  1 root video  226,   0 Jan 11 15:34 card0
    crw-rw----  1 root render 226, 128 Jan 11 15:34 renderD128
    ```    
    Note the `renderD128` GID/UID -> `226, 128`. Also, we need render group ID for privs mapping later on:
    ```sh
    getent group render | cut -d : -f3
    ```
    Which gives:
    ```
    103
    ```

    1. Check if Google Coral is there
    ```sh
    lsusb -t
    ```
    ```
    /:  Bus 02.Port 1: Dev 1, Class=root_hub, Driver=xhci_hcd/10p, 10000M
    |__ Port 9: Dev 2, If 0, Class=Application Specific Interface, Driver=, 5000M
    /:  Bus 01.Port 1: Dev 1, Class=root_hub, Driver=xhci_hcd/16p, 480M
        |__ Port 14: Dev 2, If 0, Class=Wireless, Driver=btusb, 12M
        |__ Port 14: Dev 2, If 1, Class=Wireless, Driver=btusb, 12M
    ```
    Google Coral is shown as Bus 02 / Dev 2 (Port 9). To get the GID/UID:
    ```sh
    ls -la /dev/bus/usb/002
    ```
    ```
    total 0
    drwxr-xr-x 2 root root       80 Jan 11 15:34 .
    drwxr-xr-x 4 root root       80 Jan 11 15:34 ..
    crw-rw-r-- 1 root root 189, 128 Jan 11 15:34 001
    crw-rw-r-- 1 root root 189, 129 Jan 11 15:34 002
    ```
    So, GID/UID is: `189, 129`

    1. Modify LXC container config
    ```sh
    lxc-ls -f
    ```
    ```
    NAME STATE   AUTOSTART GROUPS IPV4                                                      IPV6 UNPRIVILEGED
    400  RUNNING 0         -      172.17.0.1, 192.168.10.253, 192.168.2.238, 192.168.20.254 -    false
    ```
    So, given conrainer name of `400`, stop it and edit it's config file:
    ```sh
    lxc-stop -n 400
    cat /etc/pve/lxc/400.conf
    ```
    ```
    arch: amd64
    cores: 4
    features: mount=cifs,nesting=1
    hostname: portainer
    memory: 10240
    mp0: /media/data-fs/data,mp=/media/data
    net0: name=eth0,bridge=vmbr0,firewall=1,hwaddr=F2:7C:53:9C:52:4B,ip=dhcp,tag=2,type=veth
    net1: name=eth1,bridge=vmbr0,firewall=1,hwaddr=42:18:E6:7A:09:90,ip=dhcp,tag=10,type=veth
    net2: name=eth2,bridge=vmbr0,firewall=1,hwaddr=BE:99:70:B6:4C:4C,ip=dhcp,tag=20,type=veth
    onboot: 1
    ostype: ubuntu
    rootfs: local-lvm:vm-400-disk-0,size=8G
    swap: 2536
    ```
    ```sh
    nano /etc/pve/lxc/400.conf
    ```
    Add following mappings:
    ```conf
    #
    # GPU access
    lxc.cgroup2.devices.allow: c 226:0 rwm
    lxc.cgroup2.devices.allow: c 226:128 rwm
    lxc.mount.entry: /dev/dri/renderD128 dev/dri/renderD128 none bind,optional,create=file 0, 0
    #
    # USB BUS 002 access
    lxc.cgroup2.devices.allow: c 29:0 rwm
    lxc.cgroup2.devices.allow: c 189:* rwm
    lxc.mount.entry: /dev/bus/usb/002/ dev/bus/usb/002 none bind,optional,create=dir 0, 0

    # lxc.apparmor.profile: unconfined
    # lxc.cgroup2.devices.allow: a
    # lxc.cap.drop:
    # lxc.mount.auto: cgroup:rw
    ```
    * group mappings:
