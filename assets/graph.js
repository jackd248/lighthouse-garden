document.addEventListener("DOMContentLoaded", function() {
    var classes = document.getElementsByClassName("graph");
var layout = {
  showlegend: false,
  height: 50,
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
    b: 0
  },
};
var i;
for (i = 0; i < classes.length; i++) {
  var values = classes[i].getAttribute('data-values').split(',');
  var id = classes[i].getAttribute('id');
  var trace1 = {
  y: values,
  type: 'lines'
};
  var data = [trace1];
  
  Plotly.newPlot(id, data, layout, {displayModeBar: false});
}
  });

