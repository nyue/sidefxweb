import sidefx
import requests
import hashlib
import shutil
import os


if __name__ == '__main__':

    assert('SESI_CLIENT_ID' in os.environ)
    assert('SESI_CLIENT_SECRET_KEY' in os.environ)
    # This service object retrieve a token using your Application ID and secret
    service = sidefx.service(
        access_token_url="https://www.sidefx.com/oauth2/application_token",
        client_id=os.environ['SESI_CLIENT_ID'],
        client_secret_key=os.environ['SESI_CLIENT_SECRET_KEY'],
        endpoint_url="https://www.sidefx.com/api/",
    )

    # Retrieve the daily builds list, if you want the latest production
    # you can skip this step
    releases_list = service.download.get_daily_builds_list(
        product='houdini', version='17.0', platform='linux')

    # Retrieve the latest daily build available
    latest_release = service.download.get_daily_build_download(
        product='houdini', version='17.0', build=releases_list[0]['build'], platform='linux')

    # Download the file
    local_filename = '/tmp/' + latest_release['filename']
    r = requests.get(latest_release['download_url'], stream=True)
    if r.status_code == 200:
        with open(local_filename, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    else:
        raise Exception('Error downloading file!')

    # Verify the file checksum is matching
    file_hash = hashlib.md5()
    with open(local_filename, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            file_hash.update(chunk)
    if file_hash.hexdigest() != latest_release['hash']:
        raise Exception('Checksum does not match!')
