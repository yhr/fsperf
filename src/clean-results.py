from ResultData import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--labels", nargs='*', type=str, default=[],
                    help="Labels to delete the results for")
parser.add_argument("--config", type=str,
                    help="Configs to delete the results for")
parser.add_argument("--test", type=str,
                    help="Test name to delete results for")
args = parser.parse_args()

if not args.labels and not args.config and not args.test:
    print("Must specify either labels or configs to delete from")
    sys.exit(1)

engine = create_engine('sqlite:///fsperf-results.db')
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

for p in args.labels:
    results = session.query(Run).\
            outerjoin(FioResult).\
            outerjoin(DbenchResult).\
            outerjoin(TimeResult).\
            outerjoin(Fragmentation).\
            outerjoin(LatencyTrace).\
            outerjoin(BtrfsCommitStats).\
            outerjoin(MountTiming).\
            filter(Run.purpose == p).all()
    for r in results:
        session.delete(r)
    session.commit()

if args.test is not None:
    results = session.query(Run).\
            outerjoin(FioResult).\
            outerjoin(DbenchResult).\
            outerjoin(TimeResult).\
            outerjoin(Fragmentation).\
            outerjoin(LatencyTrace).\
            outerjoin(BtrfsCommitStats).\
            outerjoin(MountTiming).\
            filter(Run.name == args.test).all()
    for r in results:
        session.delete(r)
    session.commit()

if args.config is not None:
    results = session.query(Run).\
            outerjoin(FioResult).\
            outerjoin(DbenchResult).\
            outerjoin(TimeResult).\
            outerjoin(Fragmentation).\
            outerjoin(LatencyTrace).\
            outerjoin(BtrfsCommitStats).\
            outerjoin(MountTiming).\
            filter(Run.config == args.config).all()
    for r in results:
        session.delete(r)
    session.commit()
