rule GoldenRule {
    meta:
        description = "Testing the yara analyzer"
        author = "Nils Kuhnert, CERT-Bund"
    strings:
        $a = "FIND_ME"
    condition:
        1 of them
}