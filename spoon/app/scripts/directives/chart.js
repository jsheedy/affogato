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
        var width =  400;
        var height = 400;
        var barWidth = width / $scope.data.data.length;
        var y = d3.scale.linear()
            .domain([0,4])
            .range([height,0]);

        var svg = d3.select('.affogato-chart svg')
          .attr('width', width)
          .attr('height', height);
        var bars = svg.selectAll('rect')
            .data($scope.data.data);
       bars.enter()
             .append('rect')
             .attr('x', function(d, i) { return i * barWidth; })
             .attr('width', barWidth);

        bars.transition()
              .attr('y', function(d) { return y(d[1]) ; })
              .attr("height", function(d) { return height - y(d[1]); });

        bars.exit().remove();

      };
      $scope.data = affogatoAPI.CounterData.get({id: $scope.counter}, updateData);
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
