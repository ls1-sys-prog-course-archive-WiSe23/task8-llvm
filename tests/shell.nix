{ pkgs ? import <nixpkgs> {} }:

with pkgs;

stdenvNoCC.mkDerivation {
  name = "ci-deps";
  buildInputs = [
    python3
    llvmPackages_16.llvm
    lit
  ];
}
