import re
from . import troj_client
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from requests import Session
from tqdm import tqdm
from typing import Any, Dict, List
import os
import sys
from google.resumable_media.requests import ResumableUpload
from google.resumable_media.common import InvalidResponse, DataCorruption

retry_strategy = Retry(
    total=2,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    method_whitelist=["HEAD", "GET", "PUT",
                      "POST", "DELETE", "OPTIONS", "TRACE"],

)
retry_adapter = HTTPAdapter(max_retries=retry_strategy)
requests_retry = Session()
requests_retry.mount("https://", retry_adapter)
requests_retry.mount("http://", retry_adapter)
tempdir_ttl_days = 1

# MAX_FRAMES_PER_BATCH = 1000
# MAX_CHUNK_SIZE = int(pow(2, 23))  # 8 MiB

def assert_valid_name(name: str):
    is_valid = re.match(r"^[A-Za-z0-9_]+$", name)
    if not is_valid:
        raise Exception(
            f"'{name}' must only contain alphanumeric and underscore characters."
        )


# TODO:
# Different exceptions thrown so far:
# (no header) Exception: HTTP Error received: Forbidden: 403 | Not authenticated
# (bad id_token) Exception: HTTP Error received: Forbidden: 403 | JWK invalid
# If resp.json().detail is 'Not authenticated'
# Direct them to check their id_token or use id_token and refresh_token to generate new id_token?


def raise_resp_exception_error(resp):
    if not resp.ok:
        message = None
        try:
            r_body = resp.json()
            message = r_body.get("message") or r_body.get("msg")
        except:
            # If we failed for whatever reason (parsing body, etc.)
            # Just return the code
            if resp.status_code == 500:
                raise Exception(
                    f"HTTP Error received: {resp.reason}: {str(resp.status_code)}"
                )
            else:
                raise Exception(
                    f"HTTP Error received: {resp.reason}: {str(resp.status_code)} | {resp.json()['detail']}"
                )
                # return resp.json()['detail']
        if message:
            raise Exception(f"Error: {message}")
        else:
            # Don't really need this if, can be removed and keep what's in the else
            if resp.status_code == 500:
                raise Exception(
                    f"HTTP Error received: {resp.reason}: {str(resp.status_code)}"
                )
            else:
                raise Exception(
                    f"HTTP Error received: {resp.reason}: {str(resp.status_code)} | {resp.json()['detail']}"
                )
                # return resp.json()['detail']

def _upload_local_files(
    file_names: List[str],
    get_upload_path: str,
    headers: Dict[str, Any],
    upload_prefix: str,
    upload_suffix: str,
    delete_after_upload: bool = True,
):
    """This uploads a set of files with a reader, and then deletes it.

    Args:
        file_names (str): The local file_names (files to be uploaded)
        get_upload_path (str): The URL that generates upload URLs
        headers (Dict[str, Any]): Headers for the get_upload_path request
        upload_prefix (str): Prefix for the filepath (once uploaded)
        upload_suffix (str): Suffix for the filepath (once uploaded)
        delete_after_upload (bool): Whether to delete the file after upload

    Return:
        A list of download URLs for the uploaded files
    """
    xml_api_headers = {
        "content-type": "application/octet-stream",
    }

    download_urls = []
    if len(file_names) == 0:
        return download_urls

    all_files_bytes = sum([os.path.getsize(file_name) for file_name in file_names])
    with tqdm(
        total=all_files_bytes,
        file=sys.stdout,
        unit="B",
        unit_scale=True,
        desc="Upload Progress",
    ) as pbar:
        for count, file_name in enumerate(file_names, start=1):
            upload_filename = (
                f"{upload_prefix}_batch_{str(count).zfill(6)}{upload_suffix}"
            )

            params = {
                "upload_filename": upload_filename,
                "resumable_upload": "true",
            }
            upload_url_resp = requests_retry.get(
                get_upload_path, headers=headers, params=params
            )
            raise_resp_exception_error(upload_url_resp)
            urls = upload_url_resp.json()
            put_url = urls["put_url"]
            download_url = urls["download_url"]
            download_urls.append(download_url)

            pbar.write(
                f"Uploading file {str(count).zfill(len(str(len(file_names))))}/{str(len(file_names))}"
            )

            #TODO: REWRITE?
            MAX_CHUNK_SIZE = int(pow(2, 24))  # 16 MiB
            upload = ResumableUpload(put_url, MAX_CHUNK_SIZE, headers=xml_api_headers)

            with open(file_name, "rb") as content_reader:
                upload.initiate(
                    requests_retry, content_reader, {}, "application/octet-stream"
                )
                last_upload_bytes = 0
                while not upload.finished:
                    try:
                        upload.transmit_next_chunk(requests_retry)
                    except (InvalidResponse, DataCorruption): # InvalidResponse, DataCorruption
                        if upload.invalid:
                            upload.recover(requests_retry)
                        continue
                    except ConnectionError:
                        upload.recover(requests_retry)
                        continue
                    pbar.update(upload.bytes_uploaded - last_upload_bytes)
                    last_upload_bytes = upload.bytes_uploaded

            if delete_after_upload:
                os.remove(file_name)

            # TODO: END REWRITE

    return download_urls


#HOW TO USE SAMPLE:

# Get upload / download URLs
# download_urls = []
# get_upload_path = (
#     f"{self.api_endpoint}/collection_campaigns/{campaign_id}/get_upload_url"
# )
#
# frame_batch_filepaths = [
#     save_batch(batched_frames)
#     for batched_frames in batches(collection_frames, MAX_FRAMES_PER_BATCH)
# ]
#
# download_urls = _upload_local_files(
#     frame_batch_filepaths,
#     get_upload_path,
#     self._get_creds_headers(),
#     frame_batch_uuid,
#     ".jsonl",
#     delete_after_upload=True,
# )

# return download_urls