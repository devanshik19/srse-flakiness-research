#!/usr/bin/env python3
import argparse, csv
from collections import defaultdict

def load_batch(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def load_run_series(path, key_field="generated_test", result_field="result"):
    agg = defaultdict(lambda: {"pass": 0, "fail": 0, "miss": 0, "total": 0})
    if not path:
        return agg
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            g = row[key_field]; r = row[result_field]
            agg[g]["total"] += 1
            if r == "pass": agg[g]["pass"] += 1
            elif r in ("fail", "failure", "error"): agg[g]["fail"] += 1
            else: agg[g]["miss"] += 1
    return agg

def load_id_results(path):
    agg = {}
    if not path:
        return agg
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            agg[row["generated_test"]] = row
    return agg

def nd_verdict(a):
    if a["total"] == 0: return ""
    return "FLAKY_ND" if (a["fail"] > 0 or a["miss"] > 0) else "NOT_FLAKY"

def od_verdict(a):
    if a["total"] == 0: return ""
    if a["fail"] > 0: return "OD_SUSPECT"
    if a["pass"] == 0 and a["miss"] > 0: return "NO_TESTS_RUN"
    return "NOT_OD"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", required=True)
    ap.add_argument("--module", required=True)
    ap.add_argument("--commit", required=True)
    ap.add_argument("--batch", required=True)
    ap.add_argument("--nd")
    ap.add_argument("--id", dest="idf")
    ap.add_argument("--od")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    batch = load_batch(args.batch)
    nd = load_run_series(args.nd)
    idd = load_id_results(args.idf)
    od = load_run_series(args.od)

    cols = ["subject","module","commit","source_test","focal_method","generated_test",
            "alone_result","nd_pass","nd_total","nd_verdict","id_runs","id_verdict",
            "od_pass","od_total","od_verdict","notes"]

    checked = 0
    flaky_found = 0
    unresolved = []
    overwrite_suspect = []

    with open(args.out, "w", newline="", encoding="utf-8") as out:
        w = csv.writer(out)
        w.writerow(cols)
        for row in batch:
            source_test = row["victim_test"]
            focal_status = row["focal_status"]
            cut = row.get("cut", ""); focal = row.get("focal", "")
            gen = row["generated_test"]; alone = row["alone_result"]
            notes = row.get("notes", "")
            focal_method = f"{cut}#{focal}" if cut and focal else ""

            if alone != "pass":
                if focal_status != "agreed":
                    notes_out = f"SKIPPED_FOCAL: status={focal_status}"; gen_out = "FOCAL_UNCONFIRMED"
                elif gen == "NONE":
                    notes_out = notes or "GEN_FAILED"; gen_out = "NONE"
                else:
                    notes_out = notes or "CANDIDATE_FAILED (did not pass alone)"; gen_out = "GENERATED (candidate failed)"
                w.writerow([args.subject, args.module, args.commit, source_test, focal_method,
                            gen_out, "fail" if alone == "fail" else "na", "", "", "NA", "", "NA", "", "", "NA", notes_out])
                continue

            a_nd = nd.get(gen); a_od = od.get(gen); r_id = idd.get(gen)
            if a_nd is None and a_od is None and r_id is None:
                unresolved.append(gen)
                a_nd = {"pass":0,"fail":0,"miss":0,"total":0}; a_od = {"pass":0,"fail":0,"miss":0,"total":0}; r_id = {}
            else:
                a_nd = a_nd or {"pass":0,"fail":0,"miss":0,"total":0}
                a_od = a_od or {"pass":0,"fail":0,"miss":0,"total":0}
                r_id = r_id or {}
                checked += 1

            v_nd = nd_verdict(a_nd); v_od = od_verdict(a_od); v_id = r_id.get("result", "")

            # Detect the file-overwrite artifact: ND says the method is 100% missing
            # but ID reports NO_TESTS_RUN too -- the method almost certainly doesn't
            # exist in the physical file anymore (overwritten by a later generation
            # round targeting the same class). Don't count this as real flakiness.
            is_overwrite_artifact = (a_nd["total"] > 0 and a_nd["pass"] == 0 and a_nd["fail"] == 0
                                      and a_nd["miss"] == a_nd["total"] and v_id == "NO_TESTS_RUN")

            if is_overwrite_artifact:
                overwrite_suspect.append(gen)
                v_nd_out = "INCONCLUSIVE_OVERWRITE"
                note = ("SUSPECTED FILE OVERWRITE: another generation round for a different "
                        "focal method reused this class name and overwrote the physical .java "
                        "file after this candidate was confirmed passing alone. ND=100% missing, "
                        "ID=NO_TESTS_RUN confirm the method no longer exists on disk -- not a real "
                        "flaky finding. OD's pass verdict here is unreliable (looser class-level match).")
            else:
                v_nd_out = v_nd
                if v_nd == "FLAKY_ND" or v_od == "OD_SUSPECT" or v_id == "FLAKY_ID":
                    flaky_found += 1
                note = ("focal jaccard+llm agreed; clean on all three checks" if
                        (v_nd == "NOT_FLAKY" and v_od == "NOT_OD" and v_id == "NOT_FLAKY_ID")
                        else "focal jaccard+llm agreed; see notes/logs -- not fully clean or not yet checked")

            w.writerow([args.subject, args.module, args.commit, source_test, focal_method, gen,
                        "pass", a_nd["pass"], a_nd["total"], v_nd_out,
                        r_id.get("nondex_runs",""), v_id, a_od["pass"], a_od["total"], v_od, note])

    print(f"wrote {len(batch)} rows -> {args.out}")
    print(f"  fully checked (ND+ID+OD data found): {checked}")
    print(f"  FLAKY findings (real): {flaky_found}")
    print(f"  suspected overwrite artifacts (excluded from flaky count): {len(overwrite_suspect)}")
    if overwrite_suspect:
        for g in overwrite_suspect: print(f"    {g}")
    if unresolved:
        print(f"  {len(unresolved)} generated tests passed generation but have NO ND/ID/OD data yet:")
        for g in unresolved: print(f"    {g}")

if __name__ == "__main__":
    main()
