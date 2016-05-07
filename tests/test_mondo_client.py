import os
import json

import pytest

TEST_WEBHOOK_URL = 'http://example.com/mondotestwebhooks'


@pytest.yield_fixture()
def webhook(client):
    webhook = client.create_webhook(webhook_url=TEST_WEBHOOK_URL)

    yield webhook

    client.remove_webhook(webhook_id=webhook['id'])


class TestMondoClient:

    def test_update_tokens(self, client):
        client.access_token = None
        client.refresh_token = None
        client.expires_at = None
        client.account_id = None
        base_dir = os.path.dirname(__file__)
        with open(os.path.join(base_dir, 'token_info.json')) as data_file:
            tokens = json.load(data_file)
        client.update_tokens(**tokens)

        assert client.access_token
        assert client.refresh_token
        assert client.expires_at
        assert client.account_id

    def test_whoami(self, client):
        whoami = client.whoami()
        assert whoami
        assert 'user_id' in whoami
        assert 'authenticated' in whoami
        assert 'client_id' in whoami

    def test_list_accounts(self, client):
        accounts = client.list_accounts()
        assert len(accounts) > 0

    def test_get_balance(self, client):
        balance = client.get_balance()
        assert 'currency' in balance
        assert 'balance' in balance
        assert 'spend_today' in balance

    def test_list_transactions(self, client):
        transactions = client.list_transactions()
        assert len(transactions) > 0

    def test_get_transaction(self, client):
        transactions = client.list_transactions()
        assert len(transactions) > 0
        transaction_id = transactions[0]['id']
        transaction = client.get_transaction(transaction_id)
        assert transaction['id'] == transactions[0]['id']

    def test_annotate_transaction(self, client):
        # annotate = client.annotate_transaction()
        pass

    def test_remove_annotations(self, client):
        # remove_annotations()
        pass

    def test_create_feed_item(self, client):
        # feed_item = client.create_feed_item()
        pass

    def test_list_webhooks(self, client, webhook):
        webhooks = client.list_webhooks()
        assert len(webhooks) > 0

    def test_create_webhook(self, client):
        webhook = client.create_webhook(webhook_url=TEST_WEBHOOK_URL)
        assert webhook['url'] == TEST_WEBHOOK_URL
        assert webhook['account_id'] == client.account_id

        webhook = client.remove_webhook(webhook_id=webhook['id'])

    def test_delete_webhook(self, client, webhook):
        webhook = client.create_webhook(webhook_url=TEST_WEBHOOK_URL)
        current_webhooks = client.list_webhooks()
        number_of_hooks = len(current_webhooks)
        client.remove_webhook(webhook_id=webhook['id'])
        webhooks = client.list_webhooks()
        assert len(webhooks) < number_of_hooks

    def test_add_attachment(self, client):
        # attachment = client.add_attachment()
        pass

    def test_remove_attachment(self, client):
        # attachment = client.remove_attachment()
        pass