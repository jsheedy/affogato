'use strict';
angular.module('affogatoApp')
  .directive('affogatoChart', function(affogatoAPI) {
    var controller = function($scope, $element) {
      var width = d3.select('.affogato-chart').node().getBoundingClientRect().width;
      var height = 800;
      var barWidth = width / 1461;//width / $scope.data.data.length;
      var x = d3.time.scale()
        .domain([
          d3.time.format('%Y-%m-%d').parse('2012-10-01'),
          new Date()])
        .range([0,width]);
      var y = d3.scale.linear()
        .domain([0,5555])
        .range([height,0]);
      var ymax = 0;
      var svg = d3.select('.affogato-chart svg')
        .attr('width', width)
        .attr('height', height);

      $scope.$watch('counter', function() {
        if (! $scope.counter) {
          return;
        }

        var updateData = function() {
          var max = d3.max($scope.data.data, function(x) {return x['bike_north'];})
          if (max > ymax) {
            ymax = max;
            y = d3.scale.linear()
              .domain([0,ymax])
              .range([height,0]);
          }

          var bars = svg.selectAll('rect')
            .data($scope.data.data, function(d) {return d['datetime'];})
          bars.enter()
            .append('rect')
            .attr('x', function(d, i) { return x(d3.time.format('%Y-%m-%d').parse(d['datetime'])); })
            .attr('width', barWidth);

          bars.transition()
            .attr('y', function(d) { return y(d['bike_north']) ; })
            .attr("height", function(d) { return height - y(d['bike_north']); });

          bars.exit().remove();
        };
        $scope.data = affogatoAPI.CounterData.get({id: $scope.counter.id}, updateData);
      });
  };
  return {
    replace: true,
    restrict: 'E',
    scope: {
      counter: '='
    },
    templateUrl: 'views/affogato-chart.html',
    controller: controller
  };
});
