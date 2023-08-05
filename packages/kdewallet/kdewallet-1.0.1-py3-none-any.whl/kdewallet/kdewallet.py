from subprocess import getstatusoutput
from collections import namedtuple
from re import compile as rcompile, match, search

WALLET = 'kdewallet'
FOLDER = 'Passwords'

output_attrs = namedtuple('Output', ('code', 'msg'))
cmd = lambda bash_cmd: output_attrs(*getstatusoutput(bash_cmd))

class _DynamicAttribute(type):
    """
    this allows the inheriting class to
    return an initialized instance of itself
    with the first argument passed to the constructor
    having a value of whatever attribute you try to access
    """
    def __getattr__(cls, key):
        return cls(key)


class KDEWallet(metaclass=_DynamicAttribute):
    wallet_err = rcompile('Wallet .* not found')
    folder_err = rcompile('The folder .* does not exist!')
    entry_err  = rcompile('Failed to read entry .* value from the .* wallet.')
    
    def __class_getitem__(cls, key):
        """
        This is almost the same as what the metaclass is doing just with brackets instead of dot notation
        """
        return cls(key)

    
    def __init__(s, wallet=None, folder=None):
        s.wallet, s.folder = wallet, folder

        
    def __getattr__(s, key):
        return s[key]

    
    def __getitem__(s, key):
        if not s.wallet:
            return KDEWallet(key, s.folder)
        if not s.folder:
            return KDEWallet(s.wallet, key)

        return s.query(key, s.folder, s.wallet)


    def __setattr__(s, key, val):
        if key not in {'folder', 'wallet', 'entry'}:
            s.set_entry(key, val, s.folder, s.wallet)
        super().__setattr__(key, val)

    
    def query(s, entry, folder=None, wallet=None):
        """
        return the value that is stored under the specified entry
        """
        folder = folder or s.folder or FOLDER
        wallet = wallet or s.wallet or WALLET
        res = cmd(f"kwallet-query -r '{entry}' -f '{folder or s.folder}' '{wallet or s.folder}'")
        if res.code == 1 or search(s.folder_err, res.msg) or search(s.entry_err, res.msg):
            raise AttributeError(res.msg)
        return res.msg
    

    def set_entry(s, entry, val, folder=None, wallet=None):
        folder = folder or s.folder or FOLDER
        wallet = wallet or s.wallet or FOLDER
        if entry not in s.get_entries():
            raise AttributeError(f'the entry {entry} was not found in this wallet/folder')
        # todo find more secure way of passing pw to kwallet-query
        res = cmd(f"printf '{val}' | kwallet-query -w '{entry}' -f '{folder}' '{wallet}'")


    def get_entries(s, wallet=None, folder=None):
        """                                                                                                                    
        return a list of possibe entries from a wallet folder combination
        the default wallet is 'kdewallet' and the defualt folder is 'Passwords'
        """
        folder = folder or s.folder or FOLDER
        wallet = wallet or s.wallet or WALLET
        res = cmd(f"kwallet-query -l '{wallet}' -f '{folder}'")
        if res.code != 0 or res.msg.endswith('does not exist!'):
            raise AttributeError(res.msg)
        return res.msg.split('\n')
