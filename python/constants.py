from sh_game import Event

claim_map = {
    Event.CHANCELLOR_CLAIM: "wasChancellor",
    Event.PEEK_CLAIM: "didPolicyPeek",
    Event.PRESIDENT_CLAIM: "wasPresident",
}

inv_claim_map = {value: key for key, value in claim_map.items()}
