# clean ssh known_hosts


Over the years know_hosts is starting to be full of dead items. It's not so bad, but my autocomletion uses it to complete ssh command and this completion list starts to be full of shitty dead hosts.

This command cleans all "dead" hotst (not resolving, not connecting, refusing connections and so on) from the known_hosts file.

Just run and all dead or inaccessible items will be removed
