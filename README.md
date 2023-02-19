# Pi-hole Sync

This is a simple tool I've created to synchronize two or more Pi-hole instances. The design was created based on the idea that you'd have a primary instance (the one you change the settings) and one or more secondary instances (the ones that copy the settings from the primary).

Most of the existing tools require major system access or do this on an odd way. This tool, however, uses the Teleporter to apply the changes. It first exports the backup of the primary instance, applies whatever patches it needs to, and then uploads it to the other instances, restarting their DNS servers after it. This allow for a more seamless process and do not rely on specifiy architecture designs of the Pi-hole (besides the API, of course).

Finally, this tool also supports calling webhooks. This is just a simple `GET` call to the specified endpoints, but together with [Healthchecks](https://github.com/healthchecks/healthchecks) this can be very useful to get alerts in case something goes wrong.

# Usage

You may build the Docker image yourself, pull it from GHCR, or run the script locally. An example configuration file is provided with all the information you need to start your syncing.

### Using public image

To run it from GHCR, you may run the following command:

```shell
docker run -d \
  -v /path/to/config.json:/app/config.json \
  ghcr.io/rgsilva/pihole-sync:latest
```

You can also use docker compose for this. A `docker-compose.yml` is provided as an example in this repository.

### Building locally

To build the image locally, you need to run `docker build`. For example:

```shell
docker build . -t local/pihole-sync
```

Then you may run your container using the image `local/pihole-sync`.

### Running locally

To run without containers, you need to install the dependencies first:

```shell
pip3 install -r src/requirements.txt
```

And then you can run the application:

```shell
python3 src/main.py
```

You may want to do this inside a virtualenv.

Have fun!

# Disclaimer

Please note this is just a tool I use at home, and as such I offer **no support** if this breaks your Pi-hole instances, network, or if it burns down your house. You have been warned. This is, however, an open-source project, so feel free to fork and modify it to your own needs. If you create a new project based off this one, I'd love to hear about it (and maybe to be part of the footnotes of it)! :)

This is the full legal disclaimer:

> This software is provided "as is" and without any express or implied warranties, including, without limitation, the implied warranties of merchantability and fitness for a particular purpose.
>
> In no event shall the authors or copyright holders be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the software or the use or other dealings in the software.
>
> The use of this software is at your own risk and you assume full responsibility for any damages that may result from its use.
