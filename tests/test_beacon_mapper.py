from src.beacon_mapper import get_request_body
import json

def test_beacon_is_mapped_correctly():
  beacon = {}
  expected_request = {}

  with open('tests/beacon.json') as file:
    beacon = json.load(file)

  with open('tests/expected_beacon_request.json') as file:
    expected_request = json.load(file)

  assert get_request_body(beacon) == expected_request

