import sys
from pathlib import Path as path

p=path(__file__).parent.parent / "src/"

sys.path.insert(0, str(p) )

import bizzar_containers as bc


