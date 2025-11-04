import hashlib
import json
import time
import os
from typing import List, Dict, Any, Optional

DATA_PATH = os.path.join("data", "blockchain.json")


class Block:
    def __init__(self, index: int, timestamp: float, product_id: str, location: str, action: str, previous_hash: str, nonce: int = 0, hash_value: Optional[str] = None):
        self.index = index
        self.timestamp = timestamp
        self.product_id = product_id
        self.location = location
        self.action = action
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = hash_value or self.calculate_hash()

    def calculate_hash(self) -> str:
        block_string = f"{self.index}{self.timestamp}{self.product_id}{self.location}{self.action}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine(self, difficulty: int):
        target = "0" * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "product_id": self.product_id,
            "location": self.location,
            "action": self.action,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Block":
        return Block(
            index=d["index"],
            timestamp=d["timestamp"],
            product_id=d["product_id"],
            location=d["location"],
            action=d["action"],
            previous_hash=d["previous_hash"],
            nonce=d.get("nonce", 0),
            hash_value=d.get("hash")
        )


class FoodTraceChain:
    def __init__(self, data_path: str = DATA_PATH, difficulty: int = 2):
        self.data_path = data_path
        self.difficulty = difficulty
        self.chain: List[Block] = []
        self._ensure_data_dir()
        if os.path.exists(self.data_path):
            self._load()
        else:
            self.chain = [self._create_genesis()]
            self._save()

    def _ensure_data_dir(self):
        d = os.path.dirname(self.data_path)
        if d and not os.path.exists(d):
            os.makedirs(d, exist_ok=True)

    def _create_genesis(self) -> Block:
        return Block(0, time.time(), "GENESIS", "Origin", "Genesis Block", "0")

    def get_latest(self) -> Block:
        return self.chain[-1]

    def add_record(self, product_id: str, location: str, action: str) -> Block:
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            product_id=product_id,
            location=location,
            action=action,
            previous_hash=self.get_latest().hash
        )
        new_block.mine(self.difficulty)
        self.chain.append(new_block)
        self._save()
        return new_block

    def track(self, product_id: str) -> List[Block]:
        return [b for b in self.chain if b.product_id == product_id]

    def all_blocks(self) -> List[Block]:
        return self.chain[:]

    def is_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i - 1]
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != prev.hash:
                return False
        return True

    def tamper(self, index: int, new_action: str = "Tampered!") -> bool:
        if 0 < index < len(self.chain):
            self.chain[index].action = new_action
            self._save()
            return True
        return False

    def export_csv_rows(self) -> List[List[str]]:
        rows = [["Index", "Timestamp", "ProductID", "Location", "Action", "PrevHash", "Hash", "Nonce"]]
        for b in self.chain:
            rows.append([
                str(b.index),
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(b.timestamp)),
                b.product_id, b.location, b.action,
                b.previous_hash, b.hash, str(b.nonce)
            ])
        return rows

    def _save(self):
        serial = [b.to_dict() for b in self.chain]
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(serial, f, indent=2)

    def _load(self):
        with open(self.data_path, "r", encoding="utf-8") as f:
            serial = json.load(f)
        self.chain = [Block.from_dict(d) for d in serial]
