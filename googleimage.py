# search for the first count images tagged by query to folder folder
def main(inputarg):
    gcs = GoogleCustomSearch()
    gcs.count, gcs.folder, gcs.query = gcs.parse_args(inputarg)
    gcs.search()

# class to initialize GCS with appropriate keys, search, and download
class GoogleCustomSearch(HDBase):

    def __init__ (self, syntax=""):
        syntax = "python3 googleimage.py -q <query> -f <destination folder> -c 100"
        # how does the code fill in the <>s

        # making this unknown when I commit because I forgot the secret thing and don't want to mess it up
        self.api_key = "ignoreignoreignore"
        self.search_engine_id = "ignoreignore"
        HDBase.__init__(self, syntax)

    # gets links to corresponding query
    def get_image_links(self, response):
        # what is response
        for item in response["items"]:
            if "pagemap" in item:
                page_map = item["pagemap"]
                if "cse_image" in page_map:
                    #not self.link?
                    link = page_map["cse_image"][0]["src"]
                    self.download_link(link)

    # takes link and actually searches corresponding link to the image
    # response is in JSON - it parses through that
    def search_image(self):
        # how does one find the page_size value and why do you need it
        page_size = 10
        start = 1
        service = build("customsearch", "v1", developerKey=self.api_key)

        while start < self.count:
            response = service.cse().list(
                q=self.query,
                cx=self.search_engine_id,
                start=start).execute()

            self.get_image_links(response)

            # also like what is you doing code?
            if self.count - start < page_size:
                start += self.count - start
            else:
                start += page_size
