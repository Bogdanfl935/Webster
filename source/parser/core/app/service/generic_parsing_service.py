from app.service import executor_service, cache_service
from bs4.element import ResultSet
import logging, traceback


def process_generic_tag(authenticated_user: str, content_iterable: ResultSet, memory_limit: int, page_url: str, tag: str):
    executor_service.acquire_user_lock(authenticated_user) # Enter critical section

    tag_content_binaries = extract_content(
        authenticated_user = authenticated_user, 
        fetched_content = content_iterable,
        memory_limit = memory_limit, 
        binary_conversion_func = lambda tag_content: str(tag_content).encode(encoding='UTF-8', errors='replace')
    )

    if len(tag_content_binaries) > 0: # At least one tag had been successfully processed
        cache_service.make_memory_usage_post(sum(map(len, tag_content_binaries)))

    executor_service.release_user_lock(authenticated_user) # Exit critical section
    
    # TODO Save tag_content_binaries to parsed_content table

def extract_content(authenticated_user, fetched_content, memory_limit, binary_conversion_func) -> list:
    tag_content_binaries = list()
    current_memory_usage = cache_service.make_memory_usage_get(authenticated_user)
    for tag_content in fetched_content:
        bytes_content = None
        try:
            bytes_content = binary_conversion_func(tag_content)
        except:
            logging.log(level=logging.DEBUG, msg=traceback.format_exc())

        if bytes_content is not None:
            memory_consumption_index = min(memory_limit - current_memory_usage, len(bytes_content))
            assert memory_consumption_index > 0 # Ensure that memory limit is not below current memory usage
            
            current_memory_usage += memory_consumption_index
            tag_content_binaries.append(bytes_content[:memory_consumption_index])
            if memory_consumption_index < len(bytes_content): # Reached memory limit
                break

    return tag_content_binaries

