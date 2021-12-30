from bs4.element import ResultSet
from app.constants import parsing_constants
from app.service import executor_service, cache_service, storage_service, generic_parsing_service
from urllib.parse import ParseResult, urlparse, urlunparse

def process_anchors(authenticated_user: str, content_iterable: ResultSet, memory_limit: int, referrer: str):
    raw_anchor_hrefs = (urlparse(anchor_href) for anchor in content_iterable if (anchor_href := anchor.get('href')) is not None)
    filtered_anchor_hrefs = _filter_same_page_anchors(raw_anchor_hrefs)

    executor_service.acquire_user_lock(authenticated_user) # Enter critical section
    try:
        tag_content_binaries = generic_parsing_service.extract_content(
            authenticated_user=authenticated_user,
            fetched_content=filtered_anchor_hrefs,
            memory_limit=memory_limit,
            binary_conversion_func=lambda tag_content: str(_prepend_anchor_url_content(
                tag_content, referrer)).encode(encoding=parsing_constants.ENCODING, errors='ignore')
        )

        if len(tag_content_binaries) > 0:  # At least one tag had been successfully processed
            memory_usage = sum(map(len, tag_content_binaries))
            cache_service.make_memory_usage_post(authenticated_user, memory_usage)
            cache_service.make_last_parsed_post(authenticated_user, parsing_constants.ANCHOR_TAG, referrer, memory_usage)
            storage_service.make_url_storage_post(authenticated_user, list(
                map(lambda binary_content: binary_content.decode(
                    encoding=parsing_constants.ENCODING), tag_content_binaries)))
            storage_service.make_parsed_content_post(authenticated_user, tag_content_binaries, parsing_constants.ANCHOR_TAG)
    finally:
        executor_service.release_user_lock(authenticated_user) # Exit critical section

def _filter_same_page_anchors(anchors):
    return list(set((anchor for anchor in anchors if anchor.path not in ('', '/'))))
    

def _prepend_anchor_url_content(anchor: ParseResult, referrer):
    parsed_referrer_url = urlparse(referrer)
    scheme = anchor.scheme if anchor.scheme else parsed_referrer_url.scheme
    netloc = anchor.netloc if anchor.netloc else parsed_referrer_url.netloc 
    # Appends scheme and netloc of referrer to anchor element if any of them are missing
    return urlunparse((
        scheme, 
        netloc, 
        anchor.path,
        anchor.params,
        anchor.query,
        anchor.fragment
    ))