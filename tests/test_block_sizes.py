from shadow_fuzzer.clients.qlean import QleanParser
from shadow_fuzzer.clients.zeam import ZeamParser
from shadow_fuzzer.stats_shadow import _compute_block_slot_stats


def test_zeam_parser_extracts_publish_block_size_bytes():
    events = ZeamParser().parse_line(
        "published block to network: slot=7 proposer=3 size=12345 bytes",
        ts_ms=2000,
    )

    assert events == [{
        "_kind": "publish_block",
        "ts": 2.0,
        "slot": 7,
        "proposer": 3,
        "source": "zeam_text",
        "size_bytes": 12345,
    }]


def test_zeam_parser_extracts_raw_receive_block_size_bytes():
    events = ZeamParser().parse_line(
        "network-0:: received gossip block slot=7 proposer=3 "
        "(compressed=12000B, raw=12345B) from peer=unknown_peer",
        ts_ms=2000,
    )

    assert events == [{
        "_kind": "receive_block",
        "ts": 2.0,
        "slot": 7,
        "proposer": 3,
        "source": "zeam_text",
        "size_bytes": 12345,
    }]


def test_qlean_parser_extracts_structured_publish_block_size_bytes():
    line = (
        '["LEAN-INTEROP-TEST", 2500, "PUBLISH-BLOCK", '
        '{"slot": 8, "hash": "abc123", "proposer": 4, "size_bytes": 4567}]'
    )

    events = QleanParser().parse_line(line, ts_ms=0)

    assert events == [{
        "ts_ms": 2500,
        "slot": 8,
        "block_hash": "abc123",
        "proposer": 4,
        "source": "qlean_structured",
        "size_bytes": 4567,
        "_kind": "publish_block",
    }]


def test_block_slot_stats_tracks_block_size_per_slot():
    events = {
        "publish_block": {
            "zeam-0": [{
                "ts": 10,
                "slot": 1,
                "proposer": 1,
                "source": "zeam_text",
                "size_bytes": 2048,
            }],
        },
        "receive_block": {
            "zeam-1": [{
                "ts": 10.2,
                "slot": 1,
                "proposer": 1,
                "source": "zeam_text",
            }],
        },
    }

    stats = _compute_block_slot_stats(events, genesis_ms=0)

    assert stats["slots"][0]["block_size_bytes"] == 2048
    assert stats["summary"]["n_with_block_size"] == 1
