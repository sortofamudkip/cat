# cat
Processes data from Reddit's greatest social phenomena, /r/catsstandingup.

Specifically, it finds the upvote percentage and distribution of votes of comments in the sub.

## Prerequisites

You need the following modules:
* `praw`
* `numpy`
* `matplotlib`
* `scipy`

In addition, you will need to have registed a Reddit bot, which can be done [here.](https://praw.readthedocs.io/en/latest/getting_started/authentication.html)

## The module itself

The module contains one class, **Cat**.

### Constructor
Its constructor takes **all** of the following parameters:

`username, password, client_id, client_secret, user_agent, subreddit_name`

You should know `username`, `password`, `client_id`, `client_secret`, and `user_agent` from your bot registration. The `subreddit_name` is the name of the subreddit you want to access.

### Class functions

`run_default(self, _type="hot", limit=10)`
* Use this when you just want everything done for you.
* Specifically, it will call the following functions:
    * `collect_data`
    * `process_data`
    * `show_plot`
    * `print_stats`

`collect_data(self, _type, limit)`
* Gathers data from the the specified subreddit.
* `_type` is which category you want, namely `"hot"` or `"top"`.
* `limit` is how many posts to fetch.
* returns `upvote_list` and `stats`. The first one is a list of comment scores and the second is a dictionary containing `upvote_pc` (upvote percentage), `post_count`, and `comment_total`, all integers.

`process_data(self)`
* Extracts mean, standard deviation, max, and min from the data, and inserts them into `stats`.
* returns `stats`.

`show_plot(self)`
* self-explanatory.

`print_stats(self)`
* prints the `stats` dictionary.