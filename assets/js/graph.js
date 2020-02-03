document.addEventListener("DOMContentLoaded", function() {
    var classes = document.getElementsByClassName("graph");
var layout = {
  showlegend: false,
  height: 80,
  width: 300,
  xaxis: {
    showline: false,
    showgrid: false,
    showticklabels: false,
    linecolor: 'rgb(204,204,204)',
    linewidth: 2,
    autotick: false,
    ticks: 'outside',
    tickcolor: 'rgb(204,204,204)',
    tickwidth: 0,
    ticklen: 0,
  },
  yaxis: {
    showgrid: false,
    zeroline: false,
    showline: false,
    showticklabels: false
  },
  autosize: false,
  margin: {
    autoexpand: false,
    l: 0,
    r: 0,
    t: 0,
    b: 30
  },
};
var i;
for (i = 0; i < classes.length; i++) {
  var values_y = classes[i].getAttribute('data-values-y').split(',');
  var values_x = classes[i].getAttribute('data-values-x').split(',');
  var id = classes[i].getAttribute('id');
  var trace1 = {
  y: values_y,
  x: values_x,
  type: 'lines'
};
  var data = [trace1];
  
  Plotly.newPlot(id, data, layout, {displayModeBar: false});
}
  });

