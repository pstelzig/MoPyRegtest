package FlawedModels "Modelica models that do not translate or do not run"
    extends Modelica.Icons.ExamplesPackage;
    model DoesNotBuild
        extends Modelica.Icons.Example;
        Real x(start = 0);
        Real y(start = 1);
    equation
        der(x) = x*y;
    end DoesNotBuild;

    model DoesNotFinish
        extends Modelica.Icons.Example;
        Real x(start = 1);
    equation
        der(x) = sqrt(0.5-time);
    annotation(
      experiment(StartTime = 0, StopTime = 2, Tolerance = 1e-06, Interval = 0.002));
end DoesNotFinish;
end FlawedModels;