from bs4.element import ResultSet
from app.service import executor_service
from urllib.parse import ParseResult, urlparse, urlunparse

def process_anchors(authenticated_user: str, content_iterable: ResultSet, referrer: str):
    raw_anchor_hrefs = (urlparse(anchor_href) for anchor in content_iterable if (anchor_href := anchor.get('href')) is not None)
    executor_service.acquire_user_lock(authenticated_user) # Enter critical section

    # TODO Wrap in try except
    filtered_anchor_hrefs = _filter_same_page_anchors(raw_anchor_hrefs)
    anchor_hrefs = list(map(lambda anchor: _prepend_anchor_url_content(anchor, referrer), filtered_anchor_hrefs))

    executor_service.release_user_lock(authenticated_user) # Exit critical section

    # TODO unparse anchor hrefs
    # TODO Save anchor hrefs to next_links table
    # TODO Save anchor hrefs to parsed_content table

def _filter_same_page_anchors(anchors):
    return (anchor for anchor in anchors if anchor.path not in ('', '/'))
    

def _prepend_anchor_url_content(anchor: ParseResult, referrer):
    parsed_referrer_url = urlparse(referrer)
    scheme = anchor.scheme if anchor.scheme else parsed_referrer_url.scheme
    netloc = anchor.netloc if anchor.netloc else parsed_referrer_url.netloc 
    # Appends scheme and netloc of referrer to anchor element if any of them are missing
    return urlparse(urlunparse((
        scheme, 
        netloc, 
        anchor.path,
        anchor.params,
        anchor.query,
        anchor.fragment
    )))