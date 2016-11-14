var w = 800,
    h = 600;

var treemap = d3.layout.treemap()
    .size([w, h])
    .sticky(true)
    .value(function(d) { return d.size; });

//var colorScaleType='Greens';
var colorScaleType='RdYlGn';
var colorScale = d3.scale.quantize()
        .domain([100, 0])
        .range(colorbrewer[colorScaleType][9]);

var div = d3.select("#chart").append("div")
    .style("position", "relative")
    .style("width", w + "px")
    .style("height", h + "px");

d3.json("treemap.pfxcount.json", function(json) {
  var divs = div.data([json]).selectAll("rect")
      .data(treemap.nodes)
      .enter().append("rect")
      .attr("class", "cell")
      .style("background", function(d) { return d.children ? null : colorScale(d.pct) })
      .attr("title", txt_from_data )
      .call(cell)
      // .text(function(d) { return d.children ? null : d.parent.name; })
      .text(function(d) { return d.name } ) // children ? null : d.parent.name; })
      ;
   }
);

function txt_from_data(d) {
   var txt = '';
   txt += 'AS' + d.name + '\n' ;
   txt += 'pfx count: ' + d.size + '\n';
   txt += 'deagg: ' + d.pct + '%';
   return txt;
}
/*
  d3.select("#size").on("click", function() {
    div.selectAll("div")
        .data(treemap.value(function(d) { return d.size; }))
      .transition()
        .duration(1500)
        .call(cell);

    d3.select("#size").classed("active", true);
    d3.select("#count").classed("active", false);
  });

  d3.select("#count").on("click", function() {
    div.selectAll("div")
        .data(treemap.value(function(d) { return 1; }))
      .transition()
        .duration(1500)
        .call(cell);
    d3.select("#size").classed("active", false);
    d3.select("#count").classed("active", true);
  });
*/

function cell() {
  this
      .style("left", function(d) { return d.x + "px"; })
      .style("top", function(d) { return d.y + "px"; })
      .style("width", function(d) { return Math.max(0, d.dx - 1) + "px"; })
      .style("height", function(d) { return Math.max(0, d.dy - 1) + "px"; });
}
