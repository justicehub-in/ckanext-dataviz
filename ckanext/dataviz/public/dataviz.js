this.ckan.module('dataviz_view', function (jQuery) {
  return {
    initialize: function() {
    console.log(this.options);
    $.post( "/dataviz_view/ajax/" + this.options.resourceView.id,
    { fields: this.options.resourceView.x_axis}).done(function (response) {

    var data = JSON.parse(response)["value"];
    console.log(data);

    const width = 1000;
    const height = 600;
    const margin = {'top': 20, 'right': 20, 'bottom': 100, 'left': 100};
    const graphWidth = width - margin.left - margin.right;
    const graphHeight = height - margin.top - margin.bottom;


const svg = d3.select('.canvas')
  .append('svg')
  .attr('width', width)
  .attr('height', height);
  const graph = svg.append('g')
  .attr('width', graphWidth)
  .attr('height', graphHeight)
  .attr('transform', `translate(${margin.left}, ${margin.top})`);
  const gXAxis = graph.append('g')
  .attr('transform', `translate(0, ${graphHeight})`);
  const gYAxis = graph.append('g')

  const y = d3.scaleLinear()
    .domain([0, d3.max(data, d => Object.values(d)[0])])
    .range([graphHeight, 0]);

  const x = d3.scaleBand()
    .domain(data.map(item => Object.keys(item)[0]))
    .range([0, 500])
    .paddingInner(0.2)
    .paddingOuter(0.2);  const rects = graph.selectAll('rect')
    .data(data);  rects.attr('width', x.bandwidth)
    .attr('class', 'bar-rect')
    .attr('height', d => graphHeight - y(Object.values(d)[0]))
    .attr('x', d => x(Object.keys(d)[0]))
    .attr('y', d => y(Object.values(d)[0]));

    rects.enter()
    .append('rect')
    .attr('class', 'bar-rect')
    .attr('width', x.bandwidth)
    .attr('height', d => graphHeight - y(Object.values(d)[0]))
    .attr('x', d => x(Object.keys(d)[0]))
    .attr('y', d => y(Object.values(d)[0]));

  const xAxis = d3.axisBottom(x);
  const yAxis = d3.axisLeft(y)
    .ticks(10)
    .tickFormat(d => d);  gXAxis.call(xAxis);
  gYAxis.call(yAxis);  gXAxis.selectAll('text')
    .style('font-size', 14);

  gYAxis.selectAll('text')
    .style('font-size', 14);

});


    }
  }
});
