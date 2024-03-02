import mailbox
import pandas as pd
import os
import re
import csv
from feature_finders import HTMLFormFinder, AttachmentFinder, FlashFinder, IFrameFinder, HTMLContentFinder, URLsFinder, ExternalResourcesFinder, JavascriptFinder, CssFinder, IPsInURLs, AtInURLs, EncodingFinder
import utils_finders as utils

def process_mbox_to_csv(filepath, encoding, phishy=True, limit=500):
    print(f"Processing file: {filepath}")
    data, email_index = [], []
    try:
        mbox = mailbox.mbox(filepath)
    except Exception as e:
        print(f"Error opening file {filepath}: {e}")
        return
    
    finders = [HTMLFormFinder(), AttachmentFinder(), FlashFinder(),
               IFrameFinder(), HTMLContentFinder(), URLsFinder(),
               ExternalResourcesFinder(), JavascriptFinder(),
               CssFinder(), IPsInURLs(), AtInURLs(), EncodingFinder()]

    for i, message in enumerate(mbox, start=1):
        if i > limit: break
        payload = utils.getpayload_dict(message)
        if sum(len(re.sub(r'\s+', '', part["payload"])) for part in payload) < 1:
            continue
        
        email_data = {finder.getFeatureTitle(): finder.getFeature(message) for finder in finders}
        email_data["is_phishy"] = phishy
        data.append(email_data)

        try:
            email_raw = message.as_bytes().decode(encoding, errors='replace')
            email_index.append({"id": i, "message": utils.getpayload(message), "raw": email_raw})
        except (UnicodeEncodeError, AttributeError):
            continue

    pd.DataFrame(data).to_csv(filepath + "-export.csv", index=True, quoting=csv.QUOTE_ALL)
    pd.DataFrame(email_index).to_csv(filepath + "-export-index.csv", index=False, quoting=csv.QUOTE_ALL)

def process_mbox_to_data(filepath, encoding='utf-8', phishy=None, limit=500):
    print(f"Processing file: {filepath}")
    data = []
    try:
        mbox = mailbox.mbox(filepath)
    except Exception as e:
        print(f"Error opening file {filepath}: {e}")
        return pd.DataFrame()

    # Assuming finders are defined and implemented elsewhere
    finders = [HTMLFormFinder(), AttachmentFinder(), FlashFinder(), IFrameFinder(), HTMLContentFinder(), 
               URLsFinder(), ExternalResourcesFinder(), JavascriptFinder(), CssFinder(), IPsInURLs(), 
               AtInURLs(), EncodingFinder()]

    for i, message in enumerate(mbox):
        if i >= limit:
            break
        payload = utils.getpayload_dict(message)
        if sum(len(re.sub(r'\s+', '', part["payload"])) for part in payload) < 1:
            continue
        
        email_data = {finder.getFeatureTitle(): finder.getFeature(message) for finder in finders}
        if phishy is not None:
            email_data["is_phishy"] = int(phishy)
        data.append(email_data)

    return pd.DataFrame(data)

