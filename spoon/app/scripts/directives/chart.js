'use strict';
angular.module('affogatoApp')
.directive('affogatoChart', function(affogatoAPI) {
  var controller = function($scope, $element) {
    $scope.$watch('counter', function() {
      if (! $scope.counter) {
        return;
      }
      var i=0;
      var updateData = function() {
        var width =  800;
        var height = 800;
        var barWidth = width / $scope.data.data.length;
        var max = d3.max($scope.data.data, function(x) {return x['bike_north'];})
        var y = d3.scale.linear()
            .domain([0,max])
            .range([height,0]);

        var svg = d3.select('.affogato-chart svg')
          .attr('width', width)
          .attr('height', height);
        svg.selectAll("*").remove();

        var bars = svg.selectAll('rect')
          .data($scope.data.data);
        bars.enter()
         .append('rect')
         .attr('x', function(d, i) { return i * barWidth; })
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
