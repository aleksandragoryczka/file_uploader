import dropbox
from dropbox import Dropbox
from dropbox.files import SharedLinkFileInfo, PathOrLink, ThumbnailFormat
from dropbox.sharing import SharedLinkSettings, LinkAudience, RequestedLinkAccessLevel

from file_uploader import settings


class DropboxAPI:
    def __init__(self):
        self.dbx = Dropbox(oauth2_refresh_token=settings.DROPBOX_OAUTH2_REFRESH_TOKEN, app_key=settings.DROPBOX_APP_KEY,
                           app_secret=settings.DROPBOX_APP_SECRET)

    def get_url_from_shared_link_metadata(self, shared_link_metadata, thumbnail_size):
        shared_link_file_info = SharedLinkFileInfo(url=shared_link_metadata.url)
        preview_result_tuple = self.dbx.files_get_thumbnail_v2(
            resource=PathOrLink.link(shared_link_file_info),
            format=getattr(ThumbnailFormat, shared_link_metadata.name.split('.')[-1]),
            size=getattr(dropbox.files.ThumbnailSize, thumbnail_size, None))
        return preview_result_tuple[0].link_metadata.url

    def generate_thumbnail_url(self, image_path, size):

        try:
            shared_link_settings = SharedLinkSettings(require_password=False,
                                                      audience=LinkAudience.public,
                                                      access=RequestedLinkAccessLevel.max,
                                                      allow_download=True)
            shared_link_metadata = self.dbx.sharing_create_shared_link_with_settings(image_path,
                                                                                     settings=shared_link_settings)
            return self.get_url_from_shared_link_metadata(shared_link_metadata, size)
        except Exception as e:
            shared_links = self.dbx.sharing_list_shared_links(path=image_path, direct_only=True)
            shared_link_metadata = shared_links.links[0]
            return self.get_url_from_shared_link_metadata(shared_link_metadata, size)
