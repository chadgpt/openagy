#!/usr/bin/env python3
"""Write the search CLI for the reconstructed module into <gosrc>/cmd/symsearch/.

Kept separate from gen_gosrc.py so the generator stays a pure function of
seeds.txt. Run via rebuild-gosrc.sh.
"""
import os
import sys

OUT = sys.argv[1]
DST = os.path.join(OUT, "cmd", "symsearch")
os.makedirs(DST, exist_ok=True)

MAIN = '''// Command symsearch searches the symbol index recovered from the agy binary.
//
// The index (symbols.tsv) is what makes this reconstruction useful: every
// declaration in this module maps back to the virtual address it occupied in the
// original binary, so a string or a crash address found anywhere can be traced
// back to the package and function that produced it.
//
// Usage:
//
//	symsearch <substring>            search every field
//	symsearch -pkg <substring>       restrict to import-path matches
//	symsearch -addr 0x10262f660      look up one address
//	symsearch -exported              only exported declarations
package main

import (
	"encoding/csv"
	"flag"
	"fmt"
	"io"
	"os"
	"strings"
)

func main() {
	var (
		pkgQuery = flag.String("pkg", "", "only import paths containing this substring")
		addr     = flag.String("addr", "", "look up this exact address (hex, with or without 0x)")
		exported = flag.Bool("exported", false, "only exported declarations")
		limit    = flag.Int("limit", 200, "max rows to print")
	)
	flag.Usage = func() {
		fmt.Fprintln(os.Stderr, "usage: symsearch [flags] <substring>")
		flag.PrintDefaults()
	}
	flag.Parse()

	f, err := os.Open("symbols.tsv")
	if err != nil {
		fmt.Fprintln(os.Stderr, "symsearch:", err)
		os.Exit(1)
	}
	defer f.Close()

	query := strings.ToLower(strings.Join(flag.Args(), " "))

	r := csv.NewReader(f)
	r.Comma = '\\t'
	r.FieldsPerRecord = -1
	r.Comment = '#'
	r.ReuseRecord = true
	if _, err := r.Read(); err != nil { // header
		fmt.Fprintln(os.Stderr, "symsearch: bad index:", err)
		os.Exit(1)
	}

	shown := 0
	for {
		rec, err := r.Read()
		if err == io.EOF {
			break
		}
		if err != nil {
			fmt.Fprintln(os.Stderr, "symsearch:", err)
			break
		}
		if len(rec) < 5 {
			continue
		}
		addrField, pkg, kind, recv, name := rec[0], rec[1], rec[2], rec[3], rec[4]

		if *addr != "" {
			want := strings.ToLower(strings.TrimPrefix(*addr, "0x"))
			got := strings.ToLower(strings.TrimPrefix(addrField, "0x"))
			if got != want {
				continue
			}
		}
		if *pkgQuery != "" && !strings.Contains(strings.ToLower(pkg), strings.ToLower(*pkgQuery)) {
			continue
		}
		if *exported && !isExported(name) {
			continue
		}
		if query != "" && !strings.Contains(strings.ToLower(strings.Join(rec, " ")), query) {
			continue
		}

		recv = strings.TrimSpace(recv)
		if recv != "" {
			recv = "(" + recv + ")."
		}
		kindLabel := "func"
		if kind == "method" {
			kindLabel = "method"
		}
		fmt.Printf("%s  %-7s %s.%s%s\\n", addrField, kindLabel, pkg, recv, name)

		shown++
		if shown >= *limit {
			fmt.Fprintf(os.Stderr, "... truncated at %d rows\\n", *limit)
			break
		}
	}
	if shown == 0 {
		fmt.Fprintln(os.Stderr, "symsearch: no matches")
		os.Exit(1)
	}
}

func isExported(name string) bool {
	if name == "" {
		return false
	}
	if i := strings.IndexByte(name, '['); i >= 0 {
		name = name[:i]
	}
	c := name[0]
	return c >= 'A' && c <= 'Z'
}
'''

with open(os.path.join(DST, "main.go"), "w") as f:
    f.write(MAIN)

print(f"wrote {os.path.join(DST, 'main.go')}")