#!/usr/bin/perl
# FASTA parsing + cleaning + basic stats using BioPerl.
# Usage: perl parse_fasta.pl input.fasta > stats.tsv
use strict;
use warnings;
use Bio::SeqIO;

my $file = shift or die "Usage: $0 input.fasta\n";
my $in = Bio::SeqIO->new(-file => $file, -format => 'fasta');

print join("\t", qw(id description raw_length clean_length removed_chars cleaned_seq)), "\n";

while (my $rec = $in->next_seq) {
    my $raw   = uc($rec->seq // '');
    my $clean = $raw;
    $clean =~ s/[^ACDEFGHIKLMNPQRSTVWY]//g;   # keep only the 20 standard amino acids
    my $desc = $rec->desc // '';
    $desc =~ s/[\t\r\n]+/ /g;
    printf "%s\t%s\t%d\t%d\t%d\t%s\n",
        $rec->id, $desc, length($raw), length($clean),
        length($raw) - length($clean), $clean;
}
