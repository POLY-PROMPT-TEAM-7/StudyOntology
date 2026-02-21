final: prev: {
  python313Packages = prev.python313Packages.override {
    overrides = pyFinal: pyPrev: {
      study-ontology = pyFinal.buildPythonApplication rec {
        pname = "StudyOntology";
        version = "1.0.0";
        format = "pyproject";
        src = ../.;
        build-system = with pyFinal; [
          setuptools
          wheel
        ];
        propagatedBuildInputs = (with pyFinal; [
          pydantic
        ]);
        doCheck = false;
      };
    };
  };
}
