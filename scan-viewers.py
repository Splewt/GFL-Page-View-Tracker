import requests
from lxml import html
from collections import OrderedDict
import datetime
from time import time, sleep
import texttable as tt


class ViewerTracker:
    """
    Tracks all the unique viewers of any page on GFLClan.com and when they most recently visited, in order.
    Obviously if a user is still viewing the web page, their most recent time will be updated until they are no longer
    viewing it.
    """
    def __init__(self):
        self.viewers = OrderedDict()  # key is user, value is most recent time they visited.
        #self.web_page = "https://gflclan.com/forums/topic/49835-splewt-has-applied-for-developer/"
        self.web_page = "https://gflclan.com/forums/"
        self.content_to_view = '//ul[@class=\'ipsList_inline ipsList_csv ipsList_noSpacing ipsType_normal\']/li/a/span/text()'

    def get_viewers(self):
        """
        Uses http GET on specified web page, converts into single html element, and uses
        :return: list of current viewers on web page.
        """
        resp = requests.get(self.web_page)
        tree = html.fromstring(resp.content)
        viewers = tree.xpath(self.content_to_view)
        return viewers[::-1]  # most recent viewers are at front of list

    def update_viewers(self):
        """
        updates unique ordered dictionary (name: time). If user already exists in the hash map, pop them out, and
        put them back in with their updated time.
        :return: None
        """
        viewer_list = self.get_viewers()
        for viewer in viewer_list:
            if viewer in self.viewers:
                self.viewers.pop(viewer)

            self.viewers[viewer] = datetime.datetime.now().strftime("%m/%d/%YT%H:%M:%SZ")

        return None

    def see_n_most_recent(self, n):
        """
        prints out n most recent viewers
        :return: list of top n most recent viewers, oldest to newest.
        """
        # reverse the list to get by order of most recent, take the top 5, and reverse back.
        return list(self.viewers.items())[::-1][:n][::-1]

    def get_num_viewers(self):
        """
        :return: total number of unique viewers on page.
        """
        return len(list(self.viewers.items()))

    def track_viewers(self, update_time=10.0, n_users=5):
        """
        Prints out the total number of unique viewers and the n most recent viewers.
        :param n_users: the top n most recent viewers of web page
        :param update_time: the amount of time in seconds you want it to automatically update. Default: 10 seconds
        :return: None
        """
        try:
            tab_header = ["USERNAME", "TIME"]
            start_time = time()

            while True:
                tab = tt.Texttable()
                tab.header(tab_header)

                self.update_viewers()
                n_viewers = self.see_n_most_recent(n_users)
                total_viewers = self.get_num_viewers()

                print("Total Number of Unique Viewers: {0}".format(total_viewers))

                for viewer in n_viewers:
                    tab.add_row([viewer[0], viewer[1]])

                print(tab.draw())

                sleep(update_time - ((time() - start_time) % update_time))
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    tracker = ViewerTracker()
    tracker.track_viewers()

