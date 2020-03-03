import json
from _sha1 import sha1
from base64 import b64encode
from datetime import datetime

import requests

from common import boto_utils
from common.constant import TransactionStatus
from verification.config import JUMIO_CALLBACK_URL, JUMIO_SUBMIT_URL, REGION_NAME, \
    JUMIO_API_SECRET_SSM_KEY, JUMIO_API_TOKEN_SSM_KEY, JUMIO_INITIATE_URL
from verification.constants import JumioVerificationStatus, JumioTransactionStatus
from verification.domain.models.jumio import JumioVerification
from verification.exceptions import UnableToInitiateException


class JumioService:

    def __init__(self, repo):
        self.repo = repo
        self.boto_utils = boto_utils.BotoUtils(region_name=REGION_NAME)

    def initiate(self, username, verification_id):
        current_time = datetime.utcnow()
        user_reference_id = generate_sha_hash(username)
        jumio_verification = JumioVerification(
            verification_id=verification_id, username=username, user_reference_id=user_reference_id,
            verification_status=JumioVerificationStatus.PENDING.value, created_at=current_time,
            transaction_date=current_time, transaction_status=TransactionStatus.PENDING)
        payload = {
            "customerInternalReference": verification_id,
            "userReference": user_reference_id,
            "successUrl": JUMIO_SUBMIT_URL.format(verification_id),
            "errorUrl": JUMIO_SUBMIT_URL.format(verification_id),
            "callbackUrl": JUMIO_CALLBACK_URL.format(verification_id),
            "workflowId": 200,
        }
        body = json.dumps(payload)
        authorization = generate_basic_auth(
            self.boto_utils.get_ssm_parameter(JUMIO_API_TOKEN_SSM_KEY),
            self.boto_utils.get_ssm_parameter(JUMIO_API_SECRET_SSM_KEY))

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Content-Length": str(len(body)),
            "User-Agent": "Publisher Dapp",
            "Authorization": authorization
        }
        response = requests.post(JUMIO_INITIATE_URL, data=body, headers=headers)
        if response.status_code != 200:
            raise UnableToInitiateException()
        response_body = response.json()
        jumio_verification.redirect_url = response_body["redirectUrl"]
        jumio_verification.jumio_reference_id = response_body["transactionReference"]
        return jumio_verification

    def submit(self, verification_id, transaction_status):
        verification = self.repo.update_transaction_status(verification_id, transaction_status)
        return verification

    def callback(self, verification_id, verification_details):
        verification_status = verification_details["verificationStatus"]
        callback_date = verification_details["callbackDate"]

        if verification_status == JumioVerificationStatus.NO_ID_UPLOADED.value:
            transaction_status = JumioTransactionStatus.FAILED.value
        else:
            transaction_status = JumioTransactionStatus.DONE.value
        verification = self.repo.update_verification_and_transaction_status(
            verification_id, verification_status, transaction_status, callback_date)
        return verification


def generate_basic_auth(username, password):
    encoded_user_pass = b64encode(bytes(username + ':' + password, "utf-8")).decode("ascii")
    return f"Basic {encoded_user_pass}"


def generate_sha_hash(target_string):
    return sha1(target_string.encode("utf-8")).hexdigest()
