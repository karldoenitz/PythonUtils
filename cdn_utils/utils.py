# -*-encoding:utf-8-*-
"""

utils
~~~~~

introduction
this module contains some utils, convert image to webpack, upload file to fds.

Usage
=====
>>> upload_file_to_fds("/tmp/splash.png")
http://127.0.0.1:9203//10007/0/ce1dc201a670c527c67d46ba991d13a7.webp

"""
import Image
import logging
import os
import requests
import time
import urllib


FDS_PROXY_URL = "http://127.0.0.1:9203/fds/upload/file?url=%s&type=%s&app=10007"


def convert_image_to_webp(image_path):
    """ convert image to webpack

    :param image_path: image's path
    :return: webpack's path

    """
    im = Image.open(image_path)
    webp_image_path = os.path.join('/tmp/', '%s.webp' % image_path.split('/')[-1])
    im.save(webp_image_path, "WEBP", quality=85)
    return webp_image_path


def upload_file_to_fds(file_path, file_type=None, fds_url=None, mode_webp=True):
    """ upload file to fds

    :param file_path: file's path
    :param file_type: file's extension
    :param fds_url: fds' url
    :param mode_webp: webpack mode
    :return: the url of the source in fds

    """

    if not file_type:
        file_type = ['jpg', 'png', 'jpeg', 'gif', 'gz', 'apk', 'html', 'webp', 'zip', 'mp4']

    try:
        ext = file_path.split('.')[-1].lower()
        if ext not in list(file_type):
            logging.error('unsupported file format: %s' % ext)
            return None
        if ext == 'jpeg':
            ext = 'jpg'
        try:
            if mode_webp and ext in ['jpg', 'png', 'jpeg']:
                file_path = convert_image_to_webp(file_path)
                ext = 'webp'
        except Exception as e:
            logging.error("Convert image [%s] to webp failed, Reason: %s" % (file_path, str(e)))
    except:
        return None
    try:
        upload_url = (fds_url or FDS_PROXY_URL) % (urllib.quote(file_path), ext)
    except:
        return None
    print "uploading", upload_url, "to FDS"
    nb_retries = 0
    max_retry_times = 3
    while nb_retries <= max_retry_times:
        try:
            nb_retries += 1
            r = requests.get(upload_url, verify=False)
            if r.status_code == 200:
                print "Send %s with status:%s" % (upload_url, r.status_code)
                response = r.json()
                if response.get('url'):
                    md5_hex = response.get('md5', None)
                    if md5_hex:
                        md5_hex = md5_hex.lower().strip()
                    return {
                        'url': response['url'],
                        'md5': md5_hex,
                    }
                else:
                    logging.info("Send %s does not succeed:%s, we'll retry it" % (upload_url, r.status_code))
                    time.sleep(3)
                    continue
            else:
                logging.info("Send %s occur error:%s" % (upload_url, r.status_code))
                return None
        except Exception as ex:
            logging.info("Send file [%s] failed, due to: %s" % (file_path, str(ex)))
    return None
