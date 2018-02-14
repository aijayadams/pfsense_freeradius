import click
import pfsense
import string
import random

pfs = pfsense.pfSenseCaller("[<IPADDR>]", "<USER>", "<PASS>")
pfs.login()

def pw_gen(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@click.command()
@click.argument('action')
@click.option('--username', default=None, help='username to perform action on')
@click.option('--userfile', default=None, help='file to read users from')

def main(action, username, userfile):

    if action == "add":
        if username is None:
            print("Username required")
            exit()
        pw = pw_gen()
        pfs.add_user(username, pw)
        print("{}\t{}".format(username, pw))

    elif action == "bulk_add":
        if userfile is None:
            print("File name required")
            exit()

        output = {}
        with open(userfile) as fd:
            lines = fd.readlines()
            for l in lines:
                output[l.strip()] = pw_gen()

            for username, pw in output.items():
                pfs.add_user(username, pw)
                print("{}\t{}".format(username, pw))

    elif action == "del":
        if username is None:
            print("Username required")
            exit()
        pfs.del_user_by_name(username)
    else:
        for user in pfs.list_users():
            print(user)

if __name__ == "__main__":
    main()
