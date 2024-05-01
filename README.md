# tailscale-personal-vpn
A Personal, Free VPN service powered by Tailscale.

**This python selenium script automatically deploys an authenticated tailscale exit node into a [PlayWithDocker](https://labs.play-with-docker.com/) lab instance.**

> Script tested on windows PC, Chrome WebDriver selenium automation.


## Pre-Reads
1. Familiarize yourslef with PlayWithDocker -> [Docs](https://www.docker.com/play-with-docker/) , [Lab](https://labs.play-with-docker.com/)
2. Familiarize yourslef with Tailscale -> [TailScale-WebSite](https://tailscale.com/), [Docs](https://tailscale.com/kb/1017/install), [ExitNode Private VPN](https://tailscale.com/kb/1103/exit-nodes)

## Pre Requisites

1. A docker hub account -> Create at: https://hub.docker.com/signup [Only use email, username, password method, as we need these 2 in later steps]
2. A TailScale account -> Cretae at: https://login.tailscale.com/
3. A TailScale Tag, ACL Rule. [Just one time activity, to avoid manual intervention]
   > In tailscale, Newly added exit nodes must be manually approved by logging into admin console, To avoid that, we can create a tag, ACL Rule once, that makes tailscale to auto approve newly created exit node.
   - Go to https://login.tailscale.com/admin/acls/file
   - Paste the following code snippets inside ACL file. [Do Not overwrite existing code, just add this snippets only]
   - The following snippet creats new tag named `autoApproveExitNode`, assigns youself as owner of that tag. Ensure to use the same email id here as you have used to create tailscale account.
   ```
     "tagOwners": {
   		"tag:autoApproveExitNode": ["same-email-id-you-used-to-create-tailscale-account@gmail.com"],
   	},
   ```
   - The following snippet specifies that "Any new exit node created using the tag `autoApproveExitNode` to be automatically approoved for exit node, without any manual approoval."
   ```
   	"autoApprovers": {
   		"exitNode": ["tag:autoApproveExitNode"],
   	},
   ```
   - After adding above 2 snippets, click `save` to save and apply the new Tailscale ACL Configuration.
5. A TailScale Auth_Key -> Create at: https://login.tailscale.com/admin/settings/keys
   - Click on 'Generate auth Key'
   - Select Options as shown in screenshot [Please make sure to select `autoApproveExitNode` as tag for devices created using this Auth Key, as shown in the screenshot]
   - ![image](https://github.com/adithyaamara/tailscale-personal-vpn/assets/86059202/a05ef750-6554-4c32-94dc-66b4e4ff08b3)
   - Click `Generate Key` and save the displayed key somewhere.

## Usage

1. Install requirements with `pip install -r requirements.txt`
2. Create a `.env` file in current directory with following keys set.
```env
docker_username="dockerhub_username"
docker_password="dockerhub_password"
tailscale_auth_key="createThis@https://login.tailscale.com/admin/settings/keys"
```
3. Run the script: `python deploy.py` [You will see chrome tabs opening, ui actions performed automatically, a docker run command running in a PWD VM terminal]
   > As soon as the script runs, you will see a new exit node device (named `node1`) in your [tailscale dashboard](https://login.tailscale.com/admin/machines).
4. Open Tailscale app in your Android / any client device that is logged into tailscale, Select "Use Exit Node" in Options, select "node1" as exit node.
5. You can confirm if VPN Is working or not by visiting https://whatismyipaddress.com/ website and check IP Location. Do this before connecting to tailscale, and after connecting to exit node, you should notice a different location.


## Conclusion
1. The device where you are using "Use Exit Node" option, All the device traffic will flow through this newly procured docker container in PWD VM.
2. Evidently from above setup, This VPN is currently single node, your public IP shows up as public ip of Play With Docker VM running your exit node container [Location is somewhere random server in USA] Verify by visiting https://whatismyipaddress.com/ website.
3. Means, you still get access to certain services that are geo location restricted.
4. PWD has a limit of 4 hour session, so you need to repeat the process if the session temrinates.
> You get a single node VPN for free for a max of uninterrupted 4 hour sessions : )
