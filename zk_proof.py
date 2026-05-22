import json, hashlib, os, time
from datetime import datetime

def generate_did(agent_name):
    """Simulate DID generation (Polygon ID style)."""
    raw = f"{agent_name}:{time.time()}"
    did = "did:polygonid:" + hashlib.sha256(raw.encode()).hexdigest()[:32]
    return did

def generate_credential(agent_did, agent_type, risk_limit):
    """Simulate Verifiable Credential with ZK proof."""
    proof_seed = f"{agent_did}:{risk_limit}:{datetime.utcnow().isoformat()}"
    proof_hash = hashlib.sha256(proof_seed.encode()).hexdigest()
    credential = {
        "@context": ["https://www.w3.org/2018/credentials/v1"],
        "type": ["VerifiableCredential", "SLHRiskCredential"],
        "issuer": "did:slh:supervisor",
        "issuanceDate": datetime.utcnow().isoformat() + "Z",
        "credentialSubject": {
            "id": agent_did,
            "agentType": agent_type,
            "riskLimitUSD": risk_limit,
            "proofHash": proof_hash
        },
        "proof": {
            "type": "zk-SNARK-simulation",
            "algorithm": "sha256(salt+risk)",
            "proofValue": proof_hash
        }
    }
    return credential

if __name__ == "__main__":
    os.makedirs("zk_credentials", exist_ok=True)
    agents = [
        {"name": "MainBot", "type": "trading", "risk": 50},
        {"name": "Supervisor", "type": "monitor", "risk": 100},
        {"name": "OnboardingAgent", "type": "onboarding", "risk": 0}
    ]
    for a in agents:
        did = generate_did(a["name"])
        cred = generate_credential(did, a["type"], a["risk"])
        filename = f"zk_credentials/{a['name'].lower()}_credential.json"
        with open(filename, "w") as f:
            json.dump(cred, f, indent=2)
        print(f"? Credential for {a['name']} saved to {filename}")
    print("ZK-PoC completed. Agents have verifiable credentials.")
