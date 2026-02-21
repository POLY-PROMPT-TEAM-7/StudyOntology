{pkgs, lib, config, ...}: 
let 
  py = pkgs.python313Packages;
in {
  packages.default = py.study-ontology;
  devShells.default = pkgs.mkShell {
    packages = (with py; [
      study-ontology
      python
      pip
    ]);
  };
}