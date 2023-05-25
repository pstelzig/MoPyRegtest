model SineNoisy
  extends Modelica.Blocks.Interfaces.SO;
  Modelica.Blocks.Sources.Sine sine(f = 1) annotation(
    Placement(visible = true, transformation(origin = {-10, 30}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Noise.UniformNoise uniformNoise(samplePeriod = 0.05,y_max = 1, y_min = 0) annotation(
    Placement(visible = true, transformation(origin = {-10, -30}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Math.Add add(k2 = 1e-2) annotation(
    Placement(visible = true, transformation(origin = {30, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  inner Modelica.Blocks.Noise.GlobalSeed globalSeed annotation(
    Placement(visible = true, transformation(origin = {52, 80}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
equation
  connect(sine.y, add.u1) annotation(
    Line(points = {{2, 30}, {10, 30}, {10, 6}, {18, 6}}, color = {0, 0, 127}));
  connect(uniformNoise.y, add.u2) annotation(
    Line(points = {{2, -30}, {10, -30}, {10, -6}, {18, -6}}, color = {0, 0, 127}));
  connect(add.y, y) annotation(
    Line(points = {{42, 0}, {110, 0}}, color = {0, 0, 127}));
  annotation(
    uses(Modelica(version = "4.0.0")),
    experiment(StartTime = 0, StopTime = 1, Tolerance = 1e-06, Interval = 0.02));
end SineNoisy;