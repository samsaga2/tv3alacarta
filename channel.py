class Channel:
    def __init__(self, base_url, addon_handle, args):
        self.base_url = base_url
        self.addon_handle = addon_handle
        self.args = args
        
    def call(self):
        mode = self.args.get('mode', None)
        mode = mode[0] if mode else None
        
        if mode is None:
            self.mode__mainmenu()
        else:
            func_name = 'mode__' + mode
            func = getattr(self, func_name)
            func()
