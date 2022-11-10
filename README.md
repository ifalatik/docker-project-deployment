Role Name
=========

This role allows you to deploy docker projects via docker compose files.

Requirements
------------

`docker` and `docker-compose` (or `docker compose` - adjust via `docker_compose_command` variable)

Role Variables
--------------

The default version of docker-compsose files. Can be overridden on a per project basis.

    docker_compose_file_version: "2"

The command to use to start and stop the containers via docker-compose

    docker_compose_command: "docker-compose"

Configure where to store the project files:

    docker_project_base_path: "/opt/docker_projects"

Configure owner and access modes:

    docker_file_mode: "0664"
    docker_directory_mode: "0775"
    docker_secret_file_mode: "0660"
    docker_secret_directory_mode: "0770"

    docker_owner: "{{ ansible_user }}"
    docker_group: "{{ ansible_user }}"

The docker projects to be deployed:

    docker_projects:
      project1:
        docker_compose_file_version: 
        services:
          service1:
            key: value
            key:
              - list_item
            logging:
              ...
            healthcheck:
              ...
          service2:
          ...
        external_networks:
          - network1
          - ...
        regex_secret_remote_paths:
          - regex1
          - ...
      project2:

Currently supported docker-compose keys are:
- image
- platform
- container_name
- privileged
- init
- command
- mem_limit
- network_mode
- entrypoint
- stop_grace_period
- stop_signal
- runtime
- scale
- restart
- networks
- depends_on
- dns
- dns_opt
- dns_search
- environment
- env_file
- expose
- ports
- devices
- labels
- volumes
- sysctls
- logging
- healthcheck

### files and templates
TODO:

**Currently only external networks are supported!**

For more information take a look at `defaults/main.yml`

Dependencies
------------

A list of other roles hosted on Galaxy should go here
- plus any details in regards to parameters that may need to be set for other roles
- or variables that are used from other roles.

Example Playbook
----------------
Example deployment of [traefik](https://github.com/traefik/traefik-library-image).

This would require for the files `traefik.yml`, `dynamic_conf.yml` and the directory `certs`, including a certificate for SSL to exists under this playbook's base directory + `/docker-project-deployment/` + (`files/traefik/` || `templates/traefik/` || `host_files/{{ inventory_hostname }}/traefik/`).

```yaml
- hosts: all

  vars:
    docker_projects:
      traefik:
        services:
      docker-proxy:
        image: "tecnativa/docker-socket-proxy"
        container_name: "docker-proxy"
        privileged: true
        networks: ["docker-proxy"]
        mem_limit: "128m"
        environment: ["CONTAINERS=1"]
        volumes: ["/var/run/docker.sock:/var/run/docker.sock"]
        healthcheck:
          test: "wget --quiet -O/dev/null http://localhost:2375/containers/json?limit=1"
          interval: "10s"
          timeout: "3s"
          retries: 10
        restart: unless-stopped
      traefik:
        image: "traefik"
        container_name: "traefik"
        command: "-c /etc/traefik/traefik.yml"
        networks: ["traefik", "docker-proxy"]
        depends_on: ["docker-proxy"]
        volumes:
          - "/etc/timezone:/etc/timezone"
          - "/etc/localtime:/etc/localtime"
          - "./traefik.yml:/etc/traefik/traefik.yml"
          - "./dynamic_conf.yml:/etc/traefik/dynamic_conf.yml"
          - "./certs:/certs:ro"
        labels:
          - "traefik.enable=true"
          - "traefik.http.routers.dashboard.rule=Host(`{{ ansible_host) }}`) && (PathPrefix(`/api`) || PathPrefix(`/dashboard`))"
          - "traefik.http.routers.dashboard.service=api@internal"
          - "traefik.http.routers.dashboard.entrypoints=web,websecure"
          - "traefik.http.routers.dashboard.tls=true"
        ports:
          - "80:80"
          - "443:443"
        logging:
          driver: "json-file"
          options:
            max-size: "100m"
            max-file: "3"
        restart: unless-stopped
    external_networks: ["traefik", "docker-proxy"]
    regex_secret_remote_paths:
      - '.*/certs.*'

  roles:
      - docker-project-deployment
```

License
-------

MIT

