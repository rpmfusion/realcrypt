What is realcrypt?
====================


The realcrypt application in the RPM Fusion repo is an encryption application based on truecrypt, freely available at http://www.truecrypt.org/. It differs from truecrypt in only the following ways:

 * The name truecrypt is changed to realcrypt throughout the application, as requested by the truecrypt License:
 * All original graphics are replaced with entirely original new ones, as requested by the truecrypt License:

 * A small patch allows alternative optimization flags to those specified in the original buildsystem to be used during compilation, and the binary package is compiled using Fedora's standard optimization flags.

 * Additional support scripts and configuration files are included that allow the application to run through consolehelper. This simply means that you can attempt to run the application as a regular user, and it will prompt you for the administrator password and then launch the application with administrator privileges.

 * A menu entry for the application is added

It does not differ from truecrypt in any other respect; in particular, no code relating to actual encryption or decryption is modified. Nevertheless, the truecrypt License requires that we ask you to report any and all bugs you find to [https://bugzilla.rpmfusion.org/ RPM Fusion's Bugzilla] and not to the truecrypt project.


----

Creating a New Volume that can be mounted by a normal user.
=============================================================


realcrypt has a GUI, but in order to create a volume that can be mounted by ordinary users, you have to use the command line.

All actions are performed as 'root'


[root@localhost ~]# realcrypt -t -c
Volume type:
 1) Normal
 2) Hidden
Select [1]: 

Enter volume path: /root/realcrypt ## enter file or device path for new volume:

Enter volume size (sizeK/size[M]/sizeG): 100M

Encryption algorithm:
 1) AES
 2) Serpent
 3) Twofish
 4) AES-Twofish
 5) AES-Twofish-Serpent
 6) Serpent-AES
 7) Serpent-Twofish-AES
 8) Twofish-Serpent
Select [1]: 

Hash algorithm:
 1) RIPEMD-160
 2) SHA-512
 3) Whirlpool
Select [1]: ##the default is 1 - just hit <enter>

Filesystem:
 1) FAT
 2) None
Select [1]: 2

Enter password: ## enter your desired password 
Re-enter password: 

Enter keyfile path [none]: ## just hit <enter> we haven’t created a keyfile 

Please type at least 320 randomly chosen characters and then press Enter:
Characters remaining: 15


Done: 100.000%  Speed:   28 MB/s  Left: 0 s          

The RealCrypt volume has been successfully created.





We’ve now created an unformated volume, we’re going to map the volume so that we can format it with ext3 in the next section.




[root@localhost ~]# realcrypt -t --mount --filesystem=none /root/realcrypt ## enter your chosen file or device path

Enter password for /root/realcrypt:  ##Enter the Password you chose and hit <enter>

Enter keyfile [none]:  ## Hit <enter>

Protect hidden volume (if any)? (y=Yes/n=No) [No]: ## Hit <enter>




Let’s check to make sure the volume was mapped. Issue the command below and you should see a similar output




[root@localhost ~]# realcrypt -t -l

1: /root/realcrypt /dev/mapper/realcrypt1 -




Now we’ll format the volume with ext3




[root@localhost ~]# mkfs.ext3 /dev/mapper/realcrypt1
mke2fs 1.41.4 (27-Jan-2009)
Filesystem label=
OS type: Linux
Block size=1024 (log=0)
Fragment size=1024 (log=0)
25584 inodes, 102144 blocks
5107 blocks (5.00%) reserved for the super user
First data block=1
Maximum filesystem blocks=67371008
13 block groups
8192 blocks per group, 8192 fragments per group
1968 inodes per group
Superblock backups stored on blocks: 
	8193, 24577, 40961, 57345, 73729

Writing inode tables: done                            
Creating journal (4096 blocks): done
Writing superblocks and filesystem accounting information: done

This filesystem will be automatically checked every 39 mounts or
180 days, whichever comes first.  Use tune2fs -c or -i to override.




Now that we’ve formated the volume we’ll create a directory in which we’ll mount the volume, then mount the
volume, create a directory, and then take ownership of that directory. In the forth command below replace user1:user1 with your user:group.


[root@localhost ~]# mkdir /home/user1/safe

[root@localhost ~]# mount /dev/mapper/realcrypt1 /home/user1/safe

[root@localhost ~]# mkdir /home/user1/safe/my_safe

[root@localhost ~]# chown user1:user1 /home/user1/safe/my_safe



Now we’ll change directories and check the ownership


[root@localhost ~]# cd /home/user1/safe

[root@localhost safe] ls -l

total 13

drwx—— 2 root root 12288 2008-01-16 10:58 lost+found/

drwxr-xr-x 2 user1 user1 1024 2008-01-16 10:59 my_safe/



You’ve now successfully created a normal volume, formated the volume, created the safe directory to be the mount point, mounted the volume and created a directory within it that we took ownership of so that we can write to the volume as a normal user. While mounted, you can use your file browser and create/copy any data like you would in any normal directory.
To continue on the howto example a little further in konsole, we’ll change to the my_safe directory we created and took ownership of and create a file named test.txt. We’ll no longer need to use ’sudo’ as ownership of the directory is now our normal user account.



[user1@localhost safe]# cd my_safe

[user1@localhost my_safe]# touch test.txt

[user1@localhost my_safe]# ls -l

total 1

-rw-r–r– 1 user1 user1 0 2008-01-16 11:00 test.txt



To un-mount the volume, we’ll need to change directory out of the mounted volume which we did in the above step, then un-mount the volume, and then double check that no volumes are mapped.


[user1@localhost my_safe]# cd ~



Then as root


[root@localhost ~]# umount /dev/mapper/realcrypt1

[root@localhost ~]# realcrypt -d

[root@localhost ~]# realcrypt -l

[root@localhost ~]#



We’re done with the creation process, when you want to map and mount the volume to use it regularly the process would be as follows



[root@localhost ~]# realcrypt -t --mount --filesystem=ext3 /root/realcrypt /home/user1/safe
 
Enter password for /root/realcrypt:  ##Enter the password you chose

Enter keyfile [none]: ##Hit <enter> 

Protect hidden volume (if any)? (y=Yes/n=No) [No]: ##Hit <enter> 
[root@localhost ~]#



Once you’re done using the volume, dismount and unmap it.


[root@localhost ~]# realcrypt -d


For more usage info.
====================

http://www.truecrypt.org/docs/
