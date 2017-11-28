---
layout: post
title: Editing remote projects with atom
description: Short description
tags: [editor, coding]
modified: 2017-05-29
image:
  feature: thoughts.jpg
  credit: ensc
---

Working on files on a remote server will never be as straight forwards as working with local folders.
The most straight forward way would be of course to start a remote session on the server and start up a text editing software there.
This will lead to many complications if you, have grown accustom to multiple text-editing plugins that enhances certain editing experiences.
For example, [Scientific Linux](https://www.scientificlinux.org/) version 6, which is still a common distribution on research machines, only ships with [`python2.6`](http://ftp.scientificlinux.org/linux/scientific/6.9/x86_64/os/Packages/) by default, with many of the more fancy plugins for vim requiring at least `python2.7`, sometimes even `python3`.
In this case, one way to patch this would be to compile you own version of the packages required for your favourite text editing environment on your remote machines.
But not only is this time consuming, additional problems may also occur if your remote machine has floating environment settings, such as loading a new `glibc/python` path when loading specific packages, which may or may not conflict with your private compiled libraries.
My opinion is that your editing experience should be something that could be set up one your own local machine once, and be shared among all of the projects you are working on, remote or otherwise.
While the solution provided isn't the silver bullet for solving every use case, it did help me in most of my problems when working on remote projects with my editor of preference: [atom](https://atom.io/).

Before starting any flame wars, I must say that I am only providing a vim solution and not a emacs one simply because I have no experience with emacs. While I do not doubt that emacs has a perfectly splendid solution to the issue I have stated above, I simply cannot recommend something I have no experience with.

## Simple VIM solution: edit via `scp`
As of version 6.0, vim can actually edit remote files [out-of-the-box](http://vim.wikia.com/wiki/Editing_remote_files_via_scp_in_vim) via the command:

```
:edit scp://<remoteuser>@<server.url>//absolute/path/to/file
```

If you are already familiar with `ssh/scp` commands, the layout of this command shouldn't be difficult to understand. One cool feature about this settings is that is uses the settings stored in `~/.ssh/config`. So if you already have aliases setup for machines that might be tedious to get to (long URL, multiple machine tunnelling,... etc.),  you have full access to what ever you have setup.

While this method might be easy to perform small edits, if you have a project in development on a remote machine, this method is still rather tedious when you might need to edit multiple files in one editing session.
Also, tab auto-complete for the remote path doesn't work out-of-the-box, so navigating through a project tree might be a bit irritating.

## Atom package - [remote-sync](https://atom.io/packages/remote-sync)
One method would be to create a local copy of the remote directory onto your local machine, and attempt to sync whenever a file is changed.
While are multiple tools for achieving this via UNIX command lines (`rsync`, `sshfs`... etc), in atom the package [remote-sync](https://atom.io/packages/remote-sync) encapsulates all of this in a easy-to-edit, easy-to-read configuration files to setup.
In you local directory, setup a `.remote-sync.json` file like:

```json
{
  "transport": "scp",
  "username": "user",
  "hostname": "server.url",
  "port": "22",
  "target": "/absolute/remote/path/",
  "ignore": [
    "*.txt",
    "*.pyc"
  ],
  "uploadOnSave": true,
  "deleteLocal": false,
  "useAtomicWrites": false,
  "keyfile": "/your/.ssh/id_rsa_keyfile",
  "watch": []
}
```

Which tell atom to attempt to sync the contents in `user@server.url:/absolute/remote/path` with the contents where `.remote-sync.json` is situated on your local machine.
You can call the command to initiate a first sync via `Remote Sync: Upload folder` or `Remote Sync: Download folder`, depending on the direction of the first sync.
Then you can enjoy the snappiness of local editing while the `uploadOnSave` option automatically save your files remotely as well!
For a full documentation of the `json` file options, see the [official documentation](https://atom.io/packages/remote-sync).

One down side of this package is that it currently does not use the common `ssh` settings found in the `~/.ssh` directory. Meaning that one cannot edit on machines hidden behind another gateway machine. Another issue is that if you remote locations does not support key-file logins, you will have to leave your password in plain text in the configuration file, something I find incredibly hairy.

All in all, I would say that given the remote machines settings, you may or may not enjoy using this package. For me at least, I was still miles better than running either a sluggish vim that constantly interrupts the editing flow or a vim I feel doesn't deliver what it could.
