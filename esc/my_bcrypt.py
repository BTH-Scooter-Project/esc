import bcrypt
import sys

# password = b"super secret password"

password = sys.argv[1]
print(password)

# Hash a password for the first time, with a certain number of rounds
hashed = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(10))
# Check that a unhashed password matches one that has previously been
#   hashed
if bcrypt.checkpw(password.encode('utf-8'), hashed):
    print("It Matches!")
else:
    print("It Does not Match :(")

print("bcrypt hash: ", hashed)
