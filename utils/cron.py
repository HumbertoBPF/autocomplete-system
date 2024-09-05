from datetime import datetime, timedelta
from typing import List, Optional

import boto3
from mongoengine import disconnect

from database.config import connect_mongodb
from database.models import Trie, WordCounter


def get_query_id(client):
    end_time = datetime.now()
    start_time = end_time - timedelta(days=7)
    query_string = 'fields @message | parse @message \'{\"query\": \"*\"}\' as word | stats count(*) by word'

    response = client.start_query(
        logGroupName='autocomplete',
        startTime=int(start_time.timestamp()),
        endTime=int(end_time.timestamp()),
        queryString=query_string,
        limit=10000
    )

    if "queryId" not in response:
        raise KeyError("Response from start_query did not return a query id")

    return response["queryId"]


def get_results(client, query_id: str):
    counter = 0

    while counter < 60:
        response = client.get_query_results(
            queryId=query_id
        )

        if response["status"] != "Running":
            return response["results"]

        counter += 1

    raise TimeoutError("Timeout when fetching the results on Cloudwatch")


def deserialize(results: List):
    deserialized_results = []

    for result in results:
        deserialized_results.append({
            "word": result[0]["value"],
            "count": int(result[1]["value"])
        })

    return deserialized_results


class TrieNode:

    def __init__(self):
        self.children: List[Optional["TrieNode"]] = [None]*26
        self.is_end: bool = False
        self.count: int = 0

    def insert(self, word: str, count: int):
        current_node = self

        for letter in word:
            idx = ord(letter) - ord("a")

            if current_node.children[idx] is None:
                current_node.children[idx] = TrieNode()

            current_node = current_node.children[idx]

        current_node.is_end = True
        current_node.count = count

    def get_words_below(self, node: "TrieNode", word: str, words: List):
        if node.is_end:
            words.append((word, node.count))

        children = node.children

        for i in range(26):
            child = children[i]

            if child is not None:
                self.get_words_below(child, word + chr(97 + i), words)

    def dfs(self, node: "TrieNode", prefix):
        children = node.children

        for i in range(26):
            child = children[i]

            if child is not None:
                words = []
                new_prefix = prefix + chr(97 + i)

                self.get_words_below(child, new_prefix, words)

                words.sort(key=lambda x: x[1], reverse=True)

                trie = Trie(
                    prefix=new_prefix,
                    most_frequent_words=[WordCounter(word=word, counter=counter) for word, counter in words[:5]]
                )
                trie.save()

                self.dfs(child, new_prefix)

    def update_trie_db(self):
        # TODO can be improved with DP
        connect_mongodb()
        Trie.objects.delete()
        self.dfs(self, "")
        disconnect()


def update_trie():
    client = boto3.client("logs")

    query_id = get_query_id(client)
    results = get_results(client, query_id)

    deserialized_results = deserialize(results)

    root = TrieNode()

    for result in deserialized_results:
        root.insert(result["word"], result["count"])

    root.update_trie_db()


update_trie()
