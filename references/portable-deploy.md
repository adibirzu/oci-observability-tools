# Portable local demos

Local demos bind to `127.0.0.1`, never all interfaces. Select a starting port, probe it with `nc -z 127.0.0.1 $port`, and increment on collision for at most 20 attempts. Print the selected port so the user can connect explicitly.

This repository ships guidance only and no deployment script. Do not add network-dependent demo tests.
