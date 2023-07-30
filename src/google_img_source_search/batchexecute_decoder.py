# https://github.com/pndurette/pybatchexecute/blob/main/pybatchexecute/decode.py

import json
import re
from typing import List, Tuple

__all__ = ["decode"]


class BatchExecuteDecodeException(Exception):
    pass


def _decode_rt_compressed(
    raw: str, strict: bool = False
) -> List[Tuple[int, str, list]]:
    """Decode a raw response from a ``batchexecute`` RPC
    made with an ``rt`` (response type) of ``c`` (compressed)

    Raw responses are of the form::

        )]}'

        <lenght (int of bytes) of envelope 0>
        <envelope 0>
        <...>
        <lenght (int of bytes) of envelope n>
        <envelope n>

    Envelopes are a JSON array wrapped in an array, of the form (e.g.)::

        [["wrb.fr","jQ1olc","[\"abc\"]\n",null,null,null,"generic"]]
          ^^^^^^^^  ^^^^^^   ^^^^^^^^^^^^                 ^^^^^^^^^
          [0][0]    [0][1]   [0][2]                       [0][6]
          constant  rpc id   rpc response                 envelope index or
          (str)     (str)    (json str)                   "generic" if single envelope
                                                          (str)

    Args:
        raw (str): The raw response from a ``batchexecute`` RPC

    Returns:
        list: A list of tuples, each tuple containing:
            index (int): The index of the response
            rpcid (str): The ``rpcid`` of the response
            data (list): The decoded JSON data of the response

    Raises:
        BatchExecuteDecodeException: If any response data is not a valid JSON string
        BatchExecuteDecodeException: If any response data is empty (if ``strict`` is ``True``)

    """

    # Regex pattern to extract raw data responses (envelopes)
    p = re.compile(
        pattern=r"""
            (\d+\n)            # <number><\n>
            (?P<envelope>.+?)  # 'envelope': anything incl. <\n> (re.DOTALL)
            (?=\d+\n|$)        # until <number><\n> or <end>
        """,
        flags=re.DOTALL | re.VERBOSE,
    )

    decoded = []

    for item in p.finditer(raw):
        # An 'envelope' group is a json string
        # e.g.: '[["wrb.fr","jQ1olc","[\"abc\"]\n",null,null,null,"generic"]]'
        #          ^^^^^^^^  ^^^^^^   ^^^^^^^^^^^^                 ^^^^^^^^^
        #          [0][0]    [0][1]   [0][2]                       [0][6]
        #          constant  rpc id   rpc response                 envelope index or
        #          (str)     (str)    (json str)                   "generic" if single envelope
        #                                                          (str)
        envelope_raw = item.group("envelope")
        envelope = json.loads(envelope_raw)

        # Ignore envelopes that don't have 'wrb.fr' at [0][0]
        # (they're not rpc reponses but analytics etc.)
        if envelope[0][0] != "wrb.fr":
            continue

        # index (at [0][6], string)
        # index is 1-based
        # index is "generic" if the response contains a single envelope
        if envelope[0][6] == "generic":
            index = 1
        else:
            index = int(envelope[0][6])

        # rpcid (at [0][1])
        # rpcid's response (at [0][2], a json string)
        rpcid = envelope[0][1]

        try:
            data = json.loads(envelope[0][2])
        except json.decoder.JSONDecodeError as e:
            raise BatchExecuteDecodeException(
                f"Envelope {index} ({rpcid}): data is not a valid JSON string. "
                + "JSON decode error was: "
                + str(e)
            )

        if strict and data == []:
            raise BatchExecuteDecodeException(
                f"Envelope {index} ({rpcid}): data is empty (strict)."
            )

        # Append as tuple
        decoded.append((index, rpcid, data))

    return decoded


def _decode_rt_default(raw: str, strict: bool = False) -> List[Tuple[int, str, list]]:
    """Decode a raw response from a ``batchexecute`` RPC
    made with no ``rt`` (response type) value

    Raw response is a JSON array (minus the first two lines) of the form::

        )]}'

        [<envelope 0>,<...>,<envelope n>]

    Envelopes are a JSON arrat of the form (e.g.)::

        ["wrb.fr","jQ1olc","[\"abc\"]\n",null,null,null,"generic"]
         ^^^^^^^^  ^^^^^^   ^^^^^^^^^^^^                 ^^^^^^^^^
         [0][0]    [0][1]   [0][2]                       [0][6]
         constant  rpc id   rpc response                 envelope index or
         (str)     (str)    (json str)                   "generic" if single envelope
                                                         (str)


    Args:
        raw (str): The raw response from a ``batchexecute`` RPC

    Returns:
        list: A list of tuples, each tuple containing:
            index (int): The index of the response
            rpcid (str): The ``rpcid`` of the response
            data (list): The decoded JSON data of the response

    Raises:
        BatchExecuteDecodeException: If any response data is not a valid JSON string
        BatchExecuteDecodeException: If any response data is empty (if ``strict`` is ``True``)

    """

    # Trim the first 2 lines
    # ")]}'" and an empty line
    envelopes_raw = "".join(raw.split("\n")[2:])

    # Load all envelopes JSON (list of envelopes)
    envelopes = json.loads(envelopes_raw)

    decoded = []

    for envelope in envelopes:
        # Ignore envelopes that don't have 'wrb.fr' at [0]
        # (they're not rpc reponses but analytics etc.)
        if envelope[0] != "wrb.fr":
            continue

        # index (at [6], string)
        # index is 1-based
        # index is "generic" if the response contains a single envelope
        if envelope[6] == "generic":
            index = 1
        else:
            index = int(envelope[6])

        # rpcid (at [1])
        # rpcid's response (at [2], a json string)
        rpcid = envelope[1]

        try:
            data = json.loads(envelope[2])
        except json.decoder.JSONDecodeError as e:
            raise BatchExecuteDecodeException(
                f"Envelope {index} ({rpcid}): data is not a valid JSON string. "
                + "JSON decode error was: "
                + str(e)
            )

        if strict and data == []:
            raise BatchExecuteDecodeException(
                f"Envelope {index} ({rpcid}): data is empty (strict)."
            )

        # Append as tuple
        decoded.append((index, rpcid, data))

    return decoded


def decode(raw: str, rt: str = None, strict: bool = False, expected_rpcids: list = []):
    """Decode a raw response from a ``batchexecute`` RPC

    Args:
        raw (str): The raw response text from a ``batchexecute`` RPC
        rt (str): The ``rt`` parameter used in the ``batchexecute`` RPC (default: ``None``)
        strict (bool): Whether to raise an exception if the response is empty
            or the input ``rpcid``s are different from the output ``rpcid``s (default: ``False``)
        expected_rpcids (list): A list of expected ``rpcid`` values,
            ignored if ``strict`` is ``False`` (default: ``[]``)

    Returns:
        list: A list of tuples, each tuple containing:
            * ``index`` (int): The index of the response
            * ``rpcid`` (str): The ``rpcid`` of the response
            * ``data`` (list): The JSON data returned by the ``rpcid`` function

    Raises:
        ValueError: If ``rt`` is not ``"c"``, ``"b"``, or ``None``
        BatchExecuteDecodeException: If nothing could be decoded
        BatchExecuteDecodeException: If the count of input and output ``rpcid``s is different
            (if ``strict`` is ``True``)
        BatchExecuteDecodeException: If the input and out ``rpcid``s are different
            (if ``strict`` is ``True``)

    """
    if rt == "c":
        decoded = _decode_rt_compressed(raw, strict=strict)
    elif rt == "b":
        raise ValueError("Decoding 'rt' as 'b' (ProtoBuf) is not implemented")
    elif rt is None:
        decoded = _decode_rt_default(raw, strict=strict)
    else:
        raise ValueError("Invalid 'rt' value")

    # Nothing was decoded
    if len(decoded) == 0:
        raise BatchExecuteDecodeException(
            "Could not decode any envelope. Check format of 'raw'."
        )

    # Sort responses by index ([0])
    decoded = sorted(decoded, key=lambda envelope: envelope[0])

    if strict:
        in_rpcids = expected_rpcids
        out_rpcids = [rpcid for _, rpcid, _ in decoded]

        in_len = len(in_rpcids)
        out_len = len(out_rpcids)

        if in_len != out_len:
            raise BatchExecuteDecodeException(
                "Strict: mismatch in/out rcpids count, "
                + f"expected: {in_len}, got: {out_len}."
            )

        in_set = sorted(set(in_rpcids))
        out_set = sorted(set(out_rpcids))

        if in_set != out_set:
            raise BatchExecuteDecodeException(
                "Strict: mismatch in/out rcpids, "
                + f"expected: {in_set}, got: {out_set}."
            )

    return decoded