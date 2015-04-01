# Facebook Authentication for SSH

Secure and convenient cloud authentication for server administration

(c) 2015-04-01 [Jens Erat] <email@jenserat.de>, MIT License

[Jens Erat]: https://www.jenserat.de

## Facebook Login is Convenient

No more managing different passwords for user accounts, exchange of SSH keys. Simply authenticate with your Facebook password. You even don't need to validate host keys any more: now Facebook is doing all this for you!

Also administrators, rejoice! No more forgotten passwords, no more hacked accounts. Just add the user's mail address, and let Facebook handle all the annoying user interaction!

## Facebook Login is Secure

Facebook is secure. [Studies show, users sell company credentials for a few bucks.](https://www.sailpoint.com/news/marketpulsesurvey-passwords) Don't expect this to happen with their Facebook accounts: nobody wants to give access to his pictures being drunk at a party and chats with the last fling. And since Facebook has superior fraud detection, since they know everything about you and your devices.

## Try now!

Connect to the demo installation now:

    ssh -p 5022 facebook@facebook-auth.erat.systems

## Easy to Install, Easy to Use

The Facebook module can be set up within a few easy steps.

1. Sign up as [Facebook developer](https://developers.facebook.com/) and register a new App.
2. Install dependencies: `apt-get install libpam-python python-requests-oauthlib python-pyfiglet toilet-fonts`.
3. Put the `oauth.py` file wherever you'd like to, for example `/opt`.
4. Edit the configuration and add the credentials received from Facebook.
5. Configure PAM to use the newly added module, eg. by adding `auth	[success=1 default=ignore]	pam_python.so /opt/oauth.py` as first line to `/etc/pam.d/sshd`.
6. Add the mail address allowed to login for each user to the comment field of the `/etc/passwd` file, for example by running `chfn -o root@example.org [user]`.

That's it, you're done!
