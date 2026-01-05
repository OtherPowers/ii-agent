from datetime import datetime, timezone, timedelta
from pathlib import Path
import os

from otherpowers_governance.registry import FormationValidator


class SeasonalPulse:
    """
    The Metabolic Heartbeat of the OtherPowers ii-Agent.

    This ritual witnesses the state of the substrate and invites
    human recommitment once per season. It does not enforce.
    It records posture.
    """

    SEASON_DURATION = timedelta(days=90)
    VITALS_FILE = Path("VITALS.md")

    def __init__(self):
        self.validator = FormationValidator()

    def run_ritual(self):
        print("\n--- Seasonal Pulse: Ritual of Re-reading ---\n")

        findings = self._witness_substrate()
        posture = self._determine_posture(findings)

        last_pulse = self._get_last_pulse_time()
        elapsed = datetime.now(timezone.utc) - last_pulse

        print(f"Time since last witness: {elapsed.days} days.")
        print(f"Current field posture: {posture}")

        if elapsed >= self.SEASON_DURATION:
            self._perform_recommitment(posture, findings)
        else:
            remaining = self.SEASON_DURATION.days - elapsed.days
            print(f"Next ritual window in ~{remaining} days.")
            self._record_vitals(posture, findings, testimony=None)

    def _witness_substrate(self):
        """
        Witnesses linguistic and structural gravity without enforcement.
        """
        print("Witnessing formations of the substrate...")
        findings = []

        for root, _, files in os.walk("otherpowers_governance"):
            for file in files:
                if file.endswith(".py"):
                    path = os.path.join(root, file)
                    with open(path, "r", encoding="utf-8", errors="replace") as f:
                        findings.extend(
                            self.validator.validate_module(path, f.read())
                        )

        if findings:
            print(f"⚠ Witnessed {len(findings)} gravity traces.")
        else:
            print("✓ No hierarchical gravity surfaced.")

        return findings

    def _determine_posture(self, findings):
        """
        Determines relational posture based on witnessed gravity.
        """
        if findings:
            return "Diapause / Needs Tending"
        return "Open / Tended"

    def _perform_recommitment(self, posture, findings):
        """
        Invites human witness and reflection.
        """
        print("\n--- Seasonal Recommitment ---")
        print("The season has turned. The field invites witness.")

        if findings:
            print("\nGravity was witnessed in this season.")
            print("Recommitment may include repair, restraint, or pause.")

        testimony = input(
            "\nPlease offer an Amber Testimony for this season\n"
            "(reflection, not explanation; silence is allowed):\n> "
        ).strip()

        self._record_vitals(posture, findings, testimony)
        print("\n✓ Pulse recorded. The field continues in care.")

    def _record_vitals(self, posture, findings, testimony):
        """
        Writes a non-evaluative seasonal record.
        """
        timestamp = datetime.now(timezone.utc).isoformat()

        with open(self.VITALS_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n## Pulse — {timestamp}\n")
            f.write(f"**Posture:** {posture}\n")
            f.write(f"**Gravity Observed:** {len(findings)} traces\n")

            if findings:
                f.write("**Formations Touched:**\n")
                for finding in findings:
                    f.write(
                        f"- {finding.module_path} "
                        f"(formation: {finding.formation.value}, "
                        f"trace: {finding.substring})\n"
                    )

            if testimony:
                f.write(f"**Amber Testimony:**\n{testimony}\n")
            else:
                f.write("**Amber Testimony:** (silent)\n")

            f.write("---\n")

    def _get_last_pulse_time(self):
        """
        Parses VITALS.md for last pulse timestamp.
        Defaults to distant past if no record exists.
        """
        if not self.VITALS_FILE.exists():
            return datetime(1970, 1, 1, tzinfo=timezone.utc)

        lines = self.VITALS_FILE.read_text(encoding="utf-8").splitlines()
        for line in reversed(lines):
            if line.startswith("## Pulse"):
                try:
                    ts = line.split("—", 1)[1].strip()
                    return datetime.fromisoformat(ts)
                except Exception:
                    continue

        return datetime(1970, 1, 1, tzinfo=timezone.utc)


if __name__ == "__main__":
    SeasonalPulse().run_ritual()

