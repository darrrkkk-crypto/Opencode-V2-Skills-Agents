# Optional SSH

Read only for an SSH request. Keep tailnet/SSH policies unchanged unless a specific change is authorized.

## Selected computer to a peer

Use normal SSH directly in kernel mode. In userspace mode, use the existing local proxy and the user-selected device/account. Check that nc supports `-X/-x`, or use another verified proxy-capable client:

```sh
ssh -o 'ProxyCommand=nc -X 5 -x 127.0.0.1:1055 %h %p' <user>@<peer>
```

## Peer to the selected computer

Userspace mode supports inbound TCP; missing tailscale0 does not make SSH impossible. Inspect actual local users, RunSSH, and sshd/ssh.socket. Socket activation can explain an inactive ssh.service. Do not unlock accounts or guess passwords.

For user-authorized Tailscale SSH, run `sudo tailscale set --ssh` using the configured socket/environment. Confirm RunSSH, Running and online state. This uses tailnet identity/SSH policy rather than the sandbox user's password. Obtain any tool-required remote-access confirmation; enrollment consent alone does not grant SSH access. Report policy failures without weakening policy.

## Client VPN conflict

If asked to avoid conflict with Cloudflare WARP or another VPN, use a separate userspace Tailscale client on the user's computer, with persistent process management, separate state/socket paths and its own device authorization:

```sh
tailscaled --tun=userspace-networking \
  --state=<private-directory>/tailscaled.state \
  --socket=<private-directory>/tailscaled.sock \
  --socks5-server=127.0.0.1:<free-port>
tailscale --socket=<actual-socket> up --accept-dns=false --accept-routes=false \
  --hostname=<client-name> --timeout=20s
```

Verify actual paths/ports and use that client's proxy for SSH. Admin website login alone does not connect a client. Never copy private Tailscale state between devices.

## Verify

Keep host-key verification enabled. Obtain the server's public fingerprint through its trusted terminal and compare the actual handshake; Tailscale SSH and OpenSSH keys need not match. Verify a real login using `id -un`, `hostname`, and `uname -s`; a reachable port is insufficient. Complete any Tailscale SSH check authorization through normal browser confirmation.

[Official SSH documentation](https://tailscale.com/docs/features/tailscale-ssh)
