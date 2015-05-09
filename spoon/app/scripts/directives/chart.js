'use strict';
angular.module('affogatoApp')
  .directive('affogatoChart', function(affogatoAPI) {
    var controller = function($scope, $element) {
      var container = d3.select($element[0]);
      var width = container.node().getBoundingClientRect().width;
      var height = container.node().getBoundingClientRect().height;
      var x = d3.time.scale()
        .domain([
          d3.time.format('%Y-%m-%d').parse('2012-10-01'),
          new Date()])
        .range([0,width]);

      var svg = container.select('svg');
      svg
        .attr('width', width)
        .attr('height', height);

      $scope.$watch('counter', function() {
        if (! $scope.counter) {
          return;
        }

        var updateData = function() {
          var barWidth = width / $scope.data.data.length;
          var max = d3.max($scope.data.data, function(x) {return x[1];})
          var y = d3.scale.linear()
            .domain([0,max])
            .range([height,0]);

          var bars = svg.selectAll('rect')
            .data($scope.data.data, function(d) {return d[0];})
          bars.enter()
            .append('rect')
            .attr('x', function(d, i) { return x(d3.time.format('%Y-%m-%d').parse(d[0])); })
            .attr('width', barWidth);

          bars.transition()
            .attr('y', function(d) { return y(d[1]) ; })
            .attr("height", function(d) { return height - y(d[1]); });

          bars.exit().remove();
        };
        if ($scope.type === 'raw') {
          $scope.data = affogatoAPI.CounterData.get({id: $scope.counter.id}, updateData);
        } else if ($scope.type === 'deseasonalized') {
          $scope.data = affogatoAPI.CounterDataDeseasonalized.get({id: $scope.counter.id}, updateData);
        }
      });
  };
  return {
    replace: true,
    restrict: 'E',
    scope: {
      counter: '=',
      type: '@'
    },
    templateUrl: 'views/affogato-chart.html',
    controller: controller
  };
});
