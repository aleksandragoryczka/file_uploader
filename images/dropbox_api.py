import datetime

from dropbox import Dropbox
from dropbox.sharing import SharedLinkSettings, LinkAudience, RequestedLinkAccessLevel

from file_uploader import settings


class DropboxAPI:
    def __init__(self):
        self.dbx = Dropbox(oauth2_refresh_token=settings.DROPBOX_OAUTH2_REFRESH_TOKEN, app_key=settings.DROPBOX_APP_KEY,
                           app_secret=settings.DROPBOX_APP_SECRET)

    def create_expiring_link(self, image, expiration_time_sec):
        expiration_date = datetime.datetime.now() + datetime.timedelta(seconds=int(expiration_time_sec))
        shared_link_settings = SharedLinkSettings(expires=expiration_date, require_password=False,
                                                  audience=LinkAudience.public,
                                                  access=RequestedLinkAccessLevel.max,
                                                  allow_download=True)
        shared_link_metadata = self.dbx.sharing_create_shared_link_with_settings(path=image,
                                                                                 settings=shared_link_settings)
        return [shared_link_metadata.url, shared_link_metadata.expires]
