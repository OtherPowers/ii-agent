import sys

from otherpowers_governance.signals.field_attunement import attune_posture_field


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else None
    print(attune_posture_field(path))


if __name__ == "__main__":
    main()

