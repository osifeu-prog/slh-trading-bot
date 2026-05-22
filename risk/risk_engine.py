class RiskEngine:
    def __init__(self, rules):
        self.rules = rules

    def approve(self, context, signal):
        for rule in self.rules:
            ok, reason = rule.validate(context, signal)
            if not ok:
                return False, f"{rule.__class__.__name__}: {reason}"
        return True, ""
