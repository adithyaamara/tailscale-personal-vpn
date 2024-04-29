# tailscale-personal-vpn
A Personal, Free VPN service powered by Tailscale.

**This python script automatically deploys an authenticated tailscale exit node into a [PlayWithDocker](https://labs.play-with-docker.com/) lab instance.**

# Pre Requisites

1. A docker hub account -> Create at: https://hub.docker.com/signup [Only use email, username, password method, as we need these 2 in later steps]
2. A TailScale account -> Cretae at: https://login.tailscale.com/
3. A TailScale Tag, ACL Rule. [Pending Doc]
   > In tailscale, Newly added exit nodes must be approved by manually logging into admin console, To avoid that, we can create a tag, ACL Rule that makes tailscale to auto approve newly created exit node.
4. A TailScale Auth_Key -> Create at: https://login.tailscale.com/admin/settings/keys
   - Click on 'Generate auth Key'
   - Select Options as shown in screenshot
   - ![image](https://github.com/adithyaamara/tailscale-personal-vpn/assets/86059202/a05ef750-6554-4c32-94dc-66b4e4ff08b3)

## Usage

1. Install requirements with `pip install -r requirements.txt`
2. Create a `.env` file in current directory with following keys set.
```env
docker_username="dockerhub_username"
docker_password="dockerhub_password"
tailscale_auth_key="createThis@https://login.tailscale.com/admin/settings/keys"
```
3. Run the script: `python deploy.py`
   > As soon as the script runs, you will see a new exit node device (named `node1`) in your [tailscale dashboard](https://login.tailscale.com/admin/machines).
4. Open Tailscale app in your Android / any client device that is logged into tailscale, Select "Use Exit Node" in Options, select "node1" as exit node.
5. You can confirm if VPN Is working or not by visiting https://whatismyipaddress.com/ website and check IP Location. Do this before connecting to tailscale, and after connecting to exit node, you should notice a different location.
